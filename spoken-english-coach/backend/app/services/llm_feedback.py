import json
import ollama

MODEL = "mistral"   # or "llama3"

SYSTEM_PROMPT = """
You are an IELTS Speaking examiner and English teacher.

Given a transcript of spoken English:
1. Find grammar, vocabulary, or fluency mistakes.
2. Provide corrected sentence.
3. Estimate IELTS band (0-9).
4. Give 3-5 improvement tips.

Return ONLY valid JSON in this format:
{
  "corrected": "...",
  "mistakes": [
    {
      "type": "grammar|vocab|fluency",
      "original": "...",
      "suggestion": "...",
      "explanation": "..."
    }
  ],
  "ielts_band_estimate": 6.5,
  "tips": ["...", "..."]
}
"""

def generate_feedback(transcript: str) -> dict:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcript}
        ]
    )

    text = response["message"]["content"]

    # Extract JSON safely
    start = text.find("{")
    end = text.rfind("}") + 1
    json_text = text[start:end]

    return json.loads(json_text)
