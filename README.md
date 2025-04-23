# Social Ad Copies Generator

A web application that generates optimized ad copies for different social media platforms using AI.

## Features

- Generates ad copies for multiple social media platforms (Facebook, Instagram, TikTok, LinkedIn)
- Uses OpenAI's GPT models for content generation
- Platform-specific character limits and formatting
- Easy-to-use web interface
- Copy-to-clipboard functionality

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd social-ad-copies-generator
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5001`

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
OPENAI_API_KEY=your_api_key_here
```

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