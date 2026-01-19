from dotenv import load_dotenv
import os

# Force load .env file
load_dotenv()

# Debug print (remove later)
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.stt import transcribe_audio
from app.services.llm_feedback import generate_feedback
from app.schemas import FeedbackResponse

app = FastAPI(title="AI Spoken English Coach")

@app.post("/analyze", response_model=FeedbackResponse)
async def analyze_speech(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Upload an audio file")

    audio_bytes = await file.read()
    transcript = transcribe_audio(audio_bytes)

    if not transcript:
        raise HTTPException(status_code=400, detail="Could not transcribe audio")

    feedback = generate_feedback(transcript)

    return FeedbackResponse(
        transcript=transcript,
        corrected=feedback.get("corrected"),
        mistakes=feedback.get("mistakes", []),
        ielts_band_estimate=feedback.get("ielts_band_estimate"),
        tips=feedback.get("tips", [])
    )
