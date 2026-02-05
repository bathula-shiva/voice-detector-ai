import uvicorn
import os
from dotenv import load_dotenv # You will need to install python-dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Import your custom logic
from app.audio_utils import extract_features
from app.model import predict_voice

# --- SECURE API KEY CONFIGURATION ---
# This loads the key from a hidden .env file instead of hardcoding it
load_dotenv()
API_KEY = os.getenv("SURAKSHA_API_KEY", "demo_mode_active")

app = FastAPI(
    title="SURAKSHA AI",
    description="Advanced AI vs Human Audio Analysis",
    version="1.0.0"
)

# --- UI CONFIGURATION ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def render_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- CORE LOGIC ---
@app.post("/detect")
async def detect_voice(file: UploadFile = File(...)):
    # Check if a key exists (for your safety)
    if API_KEY == "demo_mode_active":
        print("Warning: Running in Demo Mode without a real API Key.")

    # 1. Validate file type
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Upload an audio file.")
    
    # 2. Read file
    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio file")
    
    # 3. Run your logic
    try:
        # Pass the API_KEY to your functions if they require it
        features = extract_features(audio_bytes)
        prediction = predict_voice(features) 
        
        return {
            "prediction": prediction["result"],
            "confidence": prediction["confidence"],
            "mode": "Live" if API_KEY != "demo_mode_active" else "Demo"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
