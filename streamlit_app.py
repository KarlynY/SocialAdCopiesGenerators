import streamlit as st
import os
import openai
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pyperclip

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set page config
st.set_page_config(
    page_title="Social Ad Copy Generator",
    page_icon="📝",
    layout="wide"
)

# Initialize session state for copied items
if 'copied_items' not in st.session_state:
    st.session_state.copied_items = set()

# Custom CSS with improved styling
st.markdown("""
<style>
    .main {
        background-color: #f5f6fa;
    }
    .stButton>button {
        background-color: #2374ff;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #1a5acc;
    }
    .platform-tabs {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        border-bottom: 2px solid #dcdde1;
        padding-bottom: 1rem;
        justify-content: center;
    }
    .tab-btn {
        background: none;
        border: 2px solid transparent;
        color: #2c3e50;
        padding: 0.8rem 1.5rem;
        cursor: pointer;
        font-size: 1rem;
        position: relative;
        border-radius: 8px;
        transition: all 0.3s ease;
        min-width: 120px;
        font-weight: 600;
    }
    .ad-copy {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        position: relative;
        border: 2px solid #dcdde1;
        transition: all 0.3s ease;
    }
    .ad-copy:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        border-color: #2374ff;
    }
    .copy-success {
        color: #2ecc71;
        font-weight: bold;
        margin-top: 5px;
    }
    .copy-button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 5px 10px;
        cursor: pointer;
        font-size: 0.9rem;
        margin-top: 10px;
    }
    .copy-button:hover {
        background-color: #2980b9;
    }
</style>
""", unsafe_allow_html=True)

# Function to extract content from URL
def extract_content_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content
        text_content = ' '.join([p.text for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
        return text_content[:2000]  # Limit content length
    except Exception as e:
        return str(e)

# Function to generate ad copy
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
            }}
            
            IMPORTANT: Your response must be valid JSON. Do not include any text before or after the JSON object."""
            
            response = openai.ChatCompletion.create(
                model=ai_model,
                messages=[
                    {"role": "system", "content": f"You are a professional social media advertising copywriter. Always respond with valid JSON only. Do not include any explanatory text. Generate content in {language_names.get(language, 'English')}."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Get the response content
            content = response.choices[0].message.content.strip()
            
            # Try to parse the response as JSON
            try:
                # Validate JSON
                json_data = json.loads(content)
                
                # Check if it has the expected structure
                if not isinstance(json_data, dict):
                    raise ValueError(f"Expected dictionary, got {type(json_data)}")
                
                # Check if it has at least one ad
                if not any(key.startswith('ad') for key in json_data.keys()):
                    raise ValueError("No ad keys found in response")
                
                # Store the valid JSON
                ad_copies[platform] = content
            except json.JSONDecodeError as e:
                # Create a fallback JSON with error information
                error_json = {
                    "error": f"Invalid JSON response for {platform}",
                    "details": str(e),
                    "raw_content": content[:200] + "..." if len(content) > 200 else content
                }
                ad_copies[platform] = json.dumps(error_json)
            except ValueError as e:
                # Create a fallback JSON with error information
                error_json = {
                    "error": f"Invalid JSON structure for {platform}",
                    "details": str(e),
                    "raw_content": content[:200] + "..." if len(content) > 200 else content
                }
                ad_copies[platform] = json.dumps(error_json)
            
        except Exception as e:
            # Create a fallback JSON with error information
            error_json = {
                "error": f"Error generating ad copy for {platform}",
                "details": str(e)
            }
            ad_copies[platform] = json.dumps(error_json)
    
    return ad_copies

# Header
st.image("https://www.comtogether.com/wp-content/uploads/2019/10/logo_com2_2020-1030x243.png.webp", width=300)
st.title("Social Ad Copy Generator")
st.markdown("Generate optimized ad copies for multiple social media platforms")

# Form
with st.form("ad_form"):
    st.subheader("Ad Copy Generator")
    
    # Input fields
    company_name = st.text_input("Company Name")
    product_type = st.text_input("Product Type")
    landing_url = st.text_input("Landing Page URL")
    language = st.selectbox(
        "Language",
        options=[
            "en", "es", "fr", "de", "de-ch", "it", "pt", "nl", "pl", "ru", 
            "ja", "ko", "zh-cn", "zh-tw"
        ],
        format_func=lambda x: {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "de-ch": "Swiss German",
            "it": "Italian",
            "pt": "Portuguese",
            "nl": "Dutch",
            "pl": "Polish",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh-cn": "Chinese (Simplified)",
            "zh-tw": "Chinese (Traditional)"
        }[x]
    )
    
    ai_model = st.selectbox(
        "AI Model",
        options=["gpt-3.5-turbo", "gpt-4"],
        format_func=lambda x: "GPT-3.5 Turbo" if x == "gpt-3.5-turbo" else "GPT-4"
    )
    
    # Submit button
    submit_button = st.form_submit_button("Generate Ad Copies")
    
    if submit_button:
        if not company_name or not product_type or not landing_url:
            st.error("Please fill in all required fields")
            st.stop()

# Process form submission
if submit_button:
    if not all([company_name, product_type, landing_url]):
        st.error("Please fill in all required fields.")
    else:
        # Show loading state
        with st.spinner("Generating your ad copies..."):
            # Progress bar for countdown
            progress_bar = st.progress(0)
            for i in range(30):
                # Update progress bar
                progress_bar.progress((i + 1) / 30)
                # Simulate processing time
                import time
                time.sleep(1)
            
            # Extract content from landing page
            landing_page_content = extract_content_from_url(landing_url)
            
            # Generate ad copies
            ad_copies = generate_ad_copy(company_name, product_type, landing_page_content, language, ai_model)
            
            # Check if there was an error
            if "error" in ad_copies:
                st.error(ad_copies["error"])
            else:
                # Display results
                st.success("Ad copies generated successfully!")
                
                # Create tabs for platforms
                tabs = st.tabs(["Facebook", "Instagram", "TikTok", "LinkedIn"])
                
                # Display ad copies for each platform
                for i, (platform, content) in enumerate(ad_copies.items()):
                    with tabs[i]:
                        try:
                            # Parse JSON with error handling
                            try:
                                ads = json.loads(content)
                            except json.JSONDecodeError:
                                # Check if it's an error JSON
                                try:
                                    error_data = json.loads(content)
                                    if "error" in error_data:
                                        st.error(f"Error generating {platform} ads: {error_data.get('error', 'Unknown error')}")
                                        continue
                                except:
                                    st.error(f"Unable to generate {platform} ads. Please try again.")
                                continue
                            
                            # Check if ads is a dictionary
                            if not isinstance(ads, dict):
                                st.error(f"Unable to generate {platform} ads. Please try again.")
                                continue
                            
                            # Check if it's an error response
                            if "error" in ads:
                                st.error(f"Error generating {platform} ads: {ads.get('error', 'Unknown error')}")
                                continue
                            
                            # Process each ad
                            for ad_key, ad in ads.items():
                                try:
                                    with st.container():
                                        st.markdown(f"### {ad_key.upper()}")
                                        
                                        # Check if ad is a dictionary
                                        if not isinstance(ad, dict):
                                            continue
                                        
                                        # Check if required keys exist
                                        required_keys = ['headline', 'description', 'cta']
                                        if not all(key in ad for key in required_keys):
                                            continue
                                        
                                        # Create full text
                                        full_text = f"{ad['headline']}\n\n{ad['description']}\n\n{ad['cta']}"
                                        
                                        # Display ad content
                                        st.markdown(f"**Headline:** {ad['headline']}")
                                        st.markdown(f"**Description:** {ad['description']}")
                                        st.markdown(f"**Call to Action:** {ad['cta']}")
                                        
                                        # Display the full text in a code block that can be selected and copied
                                        st.markdown("**Copy this text:**")
                                        st.code(full_text, language=None)
                                        
                                        st.divider()
                                except Exception:
                                    # Silently skip errors for individual ads
                                    continue
                        except Exception:
                            st.error(f"Unable to display {platform} ads. Please try again.") 