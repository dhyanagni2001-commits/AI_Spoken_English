# AI Spoken English Coach

An AI-powered backend that analyzes spoken English audio and returns structured feedback: a transcript, corrected sentence, grammar/vocabulary/fluency mistakes, an estimated IELTS speaking band, and improvement tips.

## How it works

1. Client uploads an audio file to the `/analyze` endpoint.
2. [faster-whisper](https://github.com/SYSTRAN/faster-whisper) transcribes the audio locally (CPU, `base` model, int8).
3. The transcript is sent to a local LLM via [Ollama](https://ollama.com) (default model: `mistral`), which acts as an IELTS examiner and returns structured JSON feedback.
4. The API responds with the transcript, corrected text, a list of mistakes, an IELTS band estimate, and tips.

## Tech stack

- **FastAPI** — HTTP API
- **faster-whisper** — speech-to-text
- **Ollama** — local LLM inference for feedback generation
- **Pydantic** — request/response schemas

## Project structure

```
spoken-english-coach/
└── backend/
    ├── app/
    │   ├── main.py                  # FastAPI app, POST /analyze
    │   ├── schemas.py               # Pydantic models (FeedbackResponse, Mistake)
    │   └── services/
    │       ├── stt.py               # Speech-to-text via faster-whisper
    │       └── llm_feedback.py      # Feedback generation via Ollama
    ├── requirements.txt
    └── .env.example
```

## Setup

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running, with the `mistral` model pulled:
  ```bash
  ollama pull mistral
  ```

### Install

```bash
cd spoken-english-coach/backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set your own values:

```
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4o-mini
```

> **Note:** `.env` is for local secrets only and should never be committed. See the [Security](#security) section below.

### Run

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## API

### `POST /analyze`

Upload an audio file for analysis.

**Request:** `multipart/form-data` with a `file` field (must be an `audio/*` content type).

**Response:**

```json
{
  "transcript": "string",
  "corrected": "string",
  "mistakes": [
    {
      "type": "grammar | vocab | fluency",
      "original": "string",
      "suggestion": "string",
      "explanation": "string"
    }
  ],
  "ielts_band_estimate": 6.5,
  "tips": ["string"]
}
```

Example with `curl`:

```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@sample.wav"
```

## Security

This repo currently has `.env` and `.env.example` committed to git, and `.env.example` contains a live-looking API key rather than a placeholder. **Rotate/revoke that key immediately** if it hasn't been already, then:

- Add `venv/`, `.env`, and `__pycache__/` to `.gitignore`.
- Remove `.env` from version control (`git rm --cached`) and scrub it from history if the repo is/was public.
- Keep only placeholder values in `.env.example`.

## Roadmap / known gaps

- No frontend yet — API only.
- No automated tests.
- `main.py` has a leftover debug `print()` of the API key on startup — remove before deploying.
