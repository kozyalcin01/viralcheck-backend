# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import shutil
import os
from pathlib import Path

from emotion_analyzer import router as emotion_router, analyze_text_emotion
from viral_scorer import ViralScorer
from report_generator import ReportGenerator
from wiro_client import analyze_video

app = FastAPI(
    title="ViralCheck AI - Video Viral Potansiyel Analizi",
    version="1.0.0",
    description="Videolarınızın viral olma potansiyelini AI ile analiz edin"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload klasörünü oluştur
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Servisler
viral_scorer = ViralScorer()
report_generator = ReportGenerator()

@app.get("/")
async def root():
    """API durumu"""
    return {
        "status": "online",
        "service": "ViralCheck AI",
        "version": "1.0.0",
        "endpoints": {
            "video_analysis": "/analyze-video",
            "quick_score": "/quick-score",
            "emotion_analysis": "/emotion-analyze",
            "health": "/health",
            "test_upload": "/test-upload"
        }
    }

@app.get("/health")
async def health_check():
    """Sağlık kontrolü"""
    return {
        "status": "healthy",
        "models": {
            "emotion_analyzer": "loaded",
            "viral_scorer": "active"
        },
        "upload_dir": str(UPLOAD_DIR),
        "upload_dir_exists": UPLOAD_DIR.exists()
    }

@app.post("/analyze-video", 
    summary="Video Viral Analizi",
    description="Video yükleyip detaylı viral potansiyel analizi alın"
)
async def analyze_video_endpoint(
    file: UploadFile = File(..., description="Video dosyası (mp4, mov, avi, mkv, webm)")
):
    """
    Video yükle ve viral potansiyel analizi yap
    
    Returns:
        - Viral skor (0-100)
        - Duygu analizi
        - Detaylı öneriler
        - En iyi paylaşım zamanı
    """
    try:
        # Dosya kontrolü
        if not file.filename:
            raise HTTPException(status_code=400, detail="Dosya adı boş")
        
        # Dosya uzantısı kontrolü
        allowed_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Desteklenmeyen format. İzin verilenler: {', '.join(allowed_extensions)}"
            )
        
        # Dosyayı kaydet
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"✅ Video kaydedildi: {file.filename}")
        
        # Şimdilik video içeriği yerine dosya adı ve uzantısı üzerinden analiz
        # Gerçek video analizi için Wiro AI kullanılacak (ileride)
        
        # Basit bir metin oluştur (demo için)
        demo_text = f"Video analysis for {file.filename}. Exciting content with surprise elements and joyful moments."
        
        # Duygu analizi yap
        print("🔄 Duygu analizi yapılıyor...")
        emotions = analyze_text_emotion(demo_text)
        
        if not emotions:
            raise HTTPException(status_code=500, detail="Duygu analizi başarısız")
        
        # Viral skor hesapla
        print("🔄 Viral skor hesaplanıyor...")
        viral_data = viral_scorer.calculate_score(emotions)
        
        # Rapor oluştur
        print("🔄 Rapor oluşturuluyor...")
        report = report_generator.generate_report(viral_data, file.filename)
        
        print(f"✅ Analiz tamamlandı! Skor: {viral_data['viral_score']}/100")
        
        return JSONResponse(content={
            "success": True,
            "message": "Video başarıyla analiz edildi",
            "report": report
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analiz hatası: {str(e)}")
    finally:
        # Dosyayı temizle (disk alanı için - opsiyonel)
        # if file_path.exists():
        #     file_path.unlink()
        pass

@app.post("/quick-score",
    summary="Hızlı Viral Skor",
    description="Sadece viral potansiyel skorunu öğrenin"
)
async def quick_score(
    file: UploadFile = File(..., description="Video dosyası")
):
    """
    Hızlı skor - sadece viral potansiyel skoru döndür
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Dosya adı boş")
        
        demo_text = f"Quick analysis for {file.filename}"
        emotions = analyze_text_emotion(demo_text)
        
        if not emotions:
            raise HTTPException(status_code=500, detail="Analiz başarısız")
        
        viral_data = viral_scorer.calculate_score(emotions)
        
        return {
            "success": True,
            "filename": file.filename,
            "viral_score": viral_data['viral_score'],
            "rating": "Yüksek" if viral_data['viral_score'] >= 70 else "Orta" if viral_data['viral_score'] >= 40 else "Düşük",
            "emoji": "🔥" if viral_data['viral_score'] >= 70 else "👍" if viral_data['viral_score'] >= 40 else "⚠️"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test-upload",
    summary="Dosya Yükleme Testi",
    description="Basit dosya yükleme testi - sadece dosya bilgilerini döndürür"
)
async def test_upload(
    file: UploadFile = File(..., description="Herhangi bir dosya")
):
    """
    Basit dosya yükleme testi
    """
    try:
        contents = await file.read()
        return {
            "success": True,
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(contents),
            "size_mb": round(len(contents) / (1024 * 1024), 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Duygu analiz rotasını ekle
app.include_router(emotion_router, tags=["Emotion Analysis"])

if __name__ == "__main__":
    import uvicorn
    print("🚀 ViralCheck AI başlatılıyor...")
    print("📍 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("💡 Test Upload: http://localhost:8000/test-upload")
    uvicorn.run(app, host="0.0.0.0", port=8000)
