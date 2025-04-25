# Social Ad Copy Generator

A Streamlit app that generates optimized ad copies for multiple social media platforms using OpenAI's GPT models.

## Features

- Generate ad copies for Facebook, Instagram, TikTok, and LinkedIn
- Support for multiple languages
- Customizable AI model selection (GPT-3.5 Turbo or GPT-4)
- Landing page content extraction
- Copy-to-clipboard functionality

## Setup

1. Clone this repository
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app locally:
   ```
   streamlit run streamlit_app.py
   ```

## Deployment

This app is deployed on Streamlit Cloud. To deploy your own version:

1. Fork this repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Select this repository
5. Add your OpenAI API key in the Streamlit Cloud secrets management
6. Deploy!

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Usage

1. Enter your company name
2. Provide the landing page URL
3. Specify the product type
4. Choose the AI model
5. Click "Generate Ad Copies"

The application will generate optimized ad copies for each social media platform.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 