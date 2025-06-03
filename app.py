import os
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

try:
    from google import genai
    from google.genai import types
except ImportError:  # pragma: no cover - library might not be available during tests
    genai = None
    types = None

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def analyze_image(image_bytes: bytes) -> str:
    """Call Google Generative AI to analyze the image."""
    if genai is None:
        raise RuntimeError("google-generativeai library not installed")

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    model = "gemini-pro-vision"

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_data(mime_type="image/jpeg", data=image_bytes),
                types.Part.from_text(
                    "Provide the name of the food in this image and an approximate calorie count."
                ),
            ],
        )
    ]

    config = types.GenerateContentConfig(response_mime_type="text/plain")
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )
    return response.text


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    image_bytes = await file.read()
    try:
        result = analyze_image(image_bytes)
    except Exception as exc:  # pragma: no cover - runtime error handling
        result = str(exc)
    return {"result": result}


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
