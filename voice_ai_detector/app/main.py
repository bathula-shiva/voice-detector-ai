import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Import your custom logic
from app.audio_utils import extract_features
from app.model import predict_voice

app = FastAPI(
    title="SURAKSHA AI",
    description="Advanced AI vs Human Audio Analysis",
    version="1.0.0"
)

# --- UI CONFIGURATION ---
# This links your 'static' folder (CSS/JS) and 'templates' folder (HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def render_ui(request: Request):
    """Serves the main web page"""
    return templates.TemplateResponse("index.html", {"request": request})


# --- CORE LOGIC ---
@app.post("/detect")
async def detect_voice(file: UploadFile = File(...)):
    # 1. Validate file type
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Upload an audio file.")
    
    # 2. Read file
    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio file")
    
    # 3. Run your logic
    try:
        features = extract_features(audio_bytes)
        prediction = predict_voice(features)
        
        # Returns the exact format the JS expects
        return {
            "prediction": prediction["result"],
            "confidence": prediction["confidence"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Ensure the app runs correctly within the 'app' directory structure
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)