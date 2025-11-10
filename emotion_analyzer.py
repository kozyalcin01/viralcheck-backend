# emotion_analyzer.py - LITE VERSION (No Heavy Model)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random

router = APIRouter()

class EmotionRequest(BaseModel):
    text: str

@router.post("/emotion-analyze")
async def analyze_emotion(request: EmotionRequest):
    """Basit duygu analizi (demo mode)"""
    try:
        text = request.text
        
        if not text or len(text.strip()) < 3:
            raise HTTPException(status_code=400, detail="Metin çok kısa")
        
        # Demo duygular (gerçek model olmadan)
        emotions = [
            {"label": "joy", "score": random.uniform(0.3, 0.8)},
            {"label": "surprise", "score": random.uniform(0.2, 0.6)},
            {"label": "neutral", "score": random.uniform(0.1, 0.4)},
            {"label": "sadness", "score": random.uniform(0.05, 0.2)},
            {"label": "anger", "score": random.uniform(0.05, 0.2)},
            {"label": "fear", "score": random.uniform(0.05, 0.2)},
            {"label": "disgust", "score": random.uniform(0.05, 0.15)}
        ]
        
        return {
            "success": True,
            "input": text,
            "emotions": emotions,
            "dominant_emotion": max(emotions, key=lambda x: x['score']),
            "note": "Demo mode - using simulated emotions"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def analyze_text_emotion(text: str):
    """Internal kullanım için basit duygu analizi"""
    emotions = [[
        {"label": "joy", "score": random.uniform(0.4, 0.9)},
        {"label": "surprise", "score": random.uniform(0.3, 0.7)},
        {"label": "neutral", "score": random.uniform(0.1, 0.3)},
        {"label": "sadness", "score": random.uniform(0.05, 0.2)},
        {"label": "anger", "score": random.uniform(0.05, 0.2)},
        {"label": "fear", "score": random.uniform(0.05, 0.2)},
        {"label": "disgust", "score": random.uniform(0.05, 0.15)}
    ]]
    return emotions
