# emotion_analyzer.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import torch

# FastAPI router tanımı
router = APIRouter()

# Giriş verisi modeli
class EmotionRequest(BaseModel):
    text: str

# Modeli yükle (GPU varsa kullan)
print("🔄 Emotion model yükleniyor...")
device = 0 if torch.cuda.is_available() else -1
emotion_model = pipeline(
    "text-classification", 
    model="j-hartmann/emotion-english-distilroberta-base", 
    return_all_scores=True,
    device=device
)
print("✅ Emotion model hazır!")

@router.post("/emotion-analyze")
async def analyze_emotion(request: EmotionRequest):
    """
    Metin üzerinden duygu analizi yap
    
    Örnek:
    POST /emotion-analyze
    {
        "text": "This is amazing! I love it!"
    }
    """
    try:
        text = request.text
        
        if not text or len(text.strip()) < 3:
            raise HTTPException(status_code=400, detail="Metin çok kısa veya boş")
        
        result = emotion_model(text)
        
        return {
            "success": True,
            "input": text,
            "emotions": result[0],  # İlk sonucu al
            "dominant_emotion": max(result[0], key=lambda x: x['score'])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analiz hatası: {str(e)}")

def analyze_text_emotion(text: str):
    """
    Metin duygu analizi (internal kullanım için)
    """
    try:
        result = emotion_model(text)
        return result
    except Exception as e:
        print(f"Duygu analizi hatası: {e}")
        return None
