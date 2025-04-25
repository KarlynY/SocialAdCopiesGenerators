from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai
import requests
import json
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Debug: Print environment variable status
print("\n=== Environment Variables Status ===")
print("Current working directory:", os.getcwd())
print(".env file exists:", os.path.exists('.env'))
api_key = os.getenv('OPENAI_API_KEY')
print("API Key loaded:", "Yes" if api_key else "No")
if api_key:
    print("API Key length:", len(api_key))
    print("API Key starts with:", api_key[:5] + "..." if len(api_key) > 5 else api_key)
print("================================\n")

app = Flask(__name__)
CORS(app)

# Configure OpenAI
openai.api_key = api_key

@app.route('/')
def index():
    return render_template('index.html')

def extract_content_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content
        text_content = ' '.join([p.text for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
        return text_content[:2000]  # Limit content length
    except Exception as e:
        return str(e)

def generate_ad_copy(company_name, product_type, landing_page_content, language="en", ai_model="gpt-3.5-turbo"):
    if not openai.api_key:
        return {"error": "OpenAI API key not configured. Please check your .env file."}
    
    platforms = {
        'facebook': {'headline_limit': 40, 'description_limit': 125},
        'instagram': {'headline_limit': 30, 'description_limit': 125},
        'tiktok': {'headline_limit': 100, 'description_limit': 150},
        'linkedin': {'headline_limit': 150, 'description_limit': 600}
    }
    
    # Language mapping for better prompts
    language_names = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'de-ch': 'Swiss German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'nl': 'Dutch',
        'pl': 'Polish',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh-cn': 'Simplified Chinese',
        'zh-tw': 'Traditional Chinese'
    }
    
    ad_copies = {}
    
    for platform, limits in platforms.items():
        try:
            prompt = f"""Create 3 different ad copies for {platform} for {company_name}, a {product_type} company.
            The ad copies should be in {language_names.get(language, 'English')}.
            Use this landing page content as reference: {landing_page_content}
            
            For each ad copy, provide:
            1. Headline (max {limits['headline_limit']} characters)
            2. Description (max {limits['description_limit']} characters)
            3. Call to action
            
            Format the response as JSON with the following structure:
            {{
                "ad1": {{"headline": "", "description": "", "cta": ""}},
                "ad2": {{"headline": "", "description": "", "cta": ""}},
                "ad3": {{"headline": "", "description": "", "cta": ""}}
            }}"""
            
            response = openai.ChatCompletion.create(
                model=ai_model,
                messages=[
                    {"role": "system", "content": f"You are a professional social media advertising copywriter. Always respond with valid JSON. Generate content in {language_names.get(language, 'English')}."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Try to parse the response as JSON to ensure it's valid
            content = response.choices[0].message.content.strip()
            json.loads(content)  # Validate JSON
            ad_copies[platform] = content
            
        except json.JSONDecodeError as e:
            ad_copies[platform] = json.dumps({
                "error": f"Invalid JSON response for {platform}",
                "details": str(e)
            })
        except Exception as e:
            ad_copies[platform] = json.dumps({
                "error": f"Error generating ad copy for {platform}",
                "details": str(e)
            })
    
    return ad_copies

@app.route('/generate-ads', methods=['POST'])
def generate_ads():
    try:
        if not openai.api_key:
            return jsonify({
                "error": "OpenAI API key not configured. Please add your API key to the .env file."
            }), 500
        
        data = request.json
        company_name = data.get('companyName')
        landing_url = data.get('landingUrl')
        product_type = data.get('productType')
        language = data.get('language', 'en')  # Default to English if not specified
        ai_model = data.get('aiModel', 'gpt-3.5-turbo')  # Default to GPT-3.5 if not specified
        
        if not all([company_name, landing_url, product_type]):
            return jsonify({
                "error": "Missing required fields. Please provide company name, landing URL, and product type."
            }), 400
        
        # Extract content from landing page
        landing_page_content = extract_content_from_url(landing_url)
        
        # Generate ad copies with language parameter
        ad_copies = generate_ad_copy(company_name, product_type, landing_page_content, language, ai_model)
        
        # Check if there was an error with the API key
        if "error" in ad_copies:
            return jsonify(ad_copies), 500
            
        return jsonify(ad_copies)
    
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 