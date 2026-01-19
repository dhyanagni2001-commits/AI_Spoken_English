from pydantic import BaseModel
from typing import List, Optional

class Mistake(BaseModel):
    type: str   # grammar | vocab | fluency
    original: str
    suggestion: str
    explanation: str

class FeedbackResponse(BaseModel):
    transcript: str
    corrected: str
    mistakes: List[Mistake]
    ielts_band_estimate: Optional[float] = None
    tips: List[str]
