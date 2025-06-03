# Calorie Watch Prototype

This prototype allows uploading a picture of food and returns estimated calorie information using Google's Generative AI models.

## Running locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Export your API key:
   ```bash
   export GEMINI_API_KEY=your-key-here
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Open `http://localhost:8000` in your browser and upload a food image.

The server uses FastAPI and the `google-generativeai` client. Deploying on Vercel requires a Python runtime.
