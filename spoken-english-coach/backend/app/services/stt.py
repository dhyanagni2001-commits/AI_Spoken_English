import os
import tempfile
from faster_whisper import WhisperModel

# Fast model for MVP
model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        path = f.name

    try:
        segments, _ = model.transcribe(path)
        text = " ".join(seg.text.strip() for seg in segments)
        return text.strip()
    finally:
        os.remove(path)
