import io
import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types
from gtts import gTTS

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELS = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite"]

HELPLINE = "Kisan Call Centre: 1800-180-1551 (toll free)"
TTS_LANG = {"English": "en", "Hindi": "hi", "Kannada": "kn"}

PROMPT = """You are an agricultural assistant for small farmers in India.
Look at the leaf photo. Supported crops: tomato, paddy (rice).
Reply ONLY with JSON in exactly this shape:
{"crop": "...", "disease": "...", "confidence": 0-100,
 "symptoms": "...", "treatment": ["step 1", "step 2"], "safety": "..."}
Rules:
- If the image is unclear, not a leaf, or not a supported crop, set confidence below 40 and explain in "symptoms".
- If the leaf looks healthy, say disease is "Healthy".
- Use simple words a farmer can understand.
- Do not invent pesticide doses. Suggest label-approved options and advise checking with the local agriculture officer.
- Write the values of disease, symptoms, treatment and safety in {lang}."""

app = FastAPI(title="KrishiMitra")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def home():
    return {"status": "KrishiMitra backend is running"}


@app.post("/diagnose")
async def diagnose(image: UploadFile = File(...), lang: str = Form("English")):
    img_bytes = await image.read()
    contents = [
        types.Part.from_bytes(data=img_bytes, mime_type=image.content_type or "image/jpeg"),
        PROMPT.replace("{lang}", lang),
    ]
    last_error = None
    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            result = json.loads(response.text)
            result["model_used"] = model
            if result.get("confidence", 0) < 50:
                result["fallback"] = HELPLINE
            return result
        except Exception as e:
            last_error = str(e)
            print(f"Model {model} failed: {last_error[:200]}")
    return JSONResponse(
        status_code=503,
        content={"error": "AI service is busy. Please try again.", "detail": last_error},
    )


@app.post("/speak")
def speak(text: str = Form(...), lang: str = Form("English")):
    buf = io.BytesIO()
    gTTS(text=text, lang=TTS_LANG.get(lang, "en")).write_to_fp(buf)
    buf.seek(0)
    return StreamingResponse(buf, media_type="audio/mpeg")


app.mount("/app", StaticFiles(directory="frontend", html=True), name="app")