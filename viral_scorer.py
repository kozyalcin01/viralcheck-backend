# viral_scorer.py
import random
from typing import Dict, List

class ViralScorer:
    """Video için viral potansiyel skoru hesaplar"""
    
    def __init__(self):
        self.weights = {
            "emotion_intensity": 0.30,  # Duygu yoğunluğu
            "engagement_potential": 0.25,  # Etkileşim potansiyeli
            "content_quality": 0.20,  # İçerik kalitesi
            "trending_factors": 0.15,  # Trend faktörleri
            "timing_score": 0.10  # Zamanlama skoru
        }
    
    def calculate_score(self, emotions: List[Dict], video_analysis: Dict = None) -> Dict:
        """
        Viral skor hesapla
        
        Args:
            emotions: Duygu analizi sonuçları
            video_analysis: Wiro'dan gelen video analizi (opsiyonel)
        
        Returns:
            Detaylı skor raporu
        """
        
        # Duygu skorlarını al
        emotion_score = self._calculate_emotion_score(emotions)
        
        # Diğer skorları hesapla
        engagement_score = self._calculate_engagement_score(emotions)
        quality_score = self._calculate_quality_score(video_analysis)
        trending_score = self._calculate_trending_score()
        timing_score = self._calculate_timing_score()
        
        # Ağırlıklı toplam
        total_score = (
            emotion_score * self.weights["emotion_intensity"] +
            engagement_score * self.weights["engagement_potential"] +
            quality_score * self.weights["content_quality"] +
            trending_score * self.weights["trending_factors"] +
            timing_score * self.weights["timing_score"]
        )
        
        # Skoru 0-100 arasına normalize et
        viral_score = int(total_score * 100)
        
        return {
            "viral_score": viral_score,
            "breakdown": {
                "emotion_intensity": int(emotion_score * 100),
                "engagement_potential": int(engagement_score * 100),
                "content_quality": int(quality_score * 100),
                "trending_factors": int(trending_score * 100),
                "timing_score": int(timing_score * 100)
            },
            "dominant_emotions": self._get_dominant_emotions(emotions),
            "recommendations": self._generate_recommendations(viral_score, emotions)
        }
    
    def _calculate_emotion_score(self, emotions: List[Dict]) -> float:
        """Duygu yoğunluğu skoru"""
        if not emotions or not emotions[0]:
            return 0.5
        
        # İlk duygu setini al
        emotion_set = emotions[0]
        
        # En yüksek 3 duyguyu bul
        sorted_emotions = sorted(emotion_set, key=lambda x: x['score'], reverse=True)
        top_3 = sorted_emotions[:3]
        
        # Yüksek skorlu duygular = daha iyi viral potansiyel
        avg_top_3 = sum(e['score'] for e in top_3) / 3
        
        # Surprise, joy, anger gibi güçlü duygular bonusu
        strong_emotions = ['surprise', 'joy', 'anger', 'fear']
        has_strong = any(e['label'] in strong_emotions and e['score'] > 0.3 for e in emotion_set)
        
        score = avg_top_3 * (1.2 if has_strong else 1.0)
        return min(score, 1.0)
    
    def _calculate_engagement_score(self, emotions: List[Dict]) -> float:
        """Etkileşim potansiyeli"""
        if not emotions or not emotions[0]:
            return 0.5
        
        emotion_set = emotions[0]
        
        # Çeşitlilik = daha iyi etkileşim
        unique_emotions = len([e for e in emotion_set if e['score'] > 0.1])
        diversity_score = min(unique_emotions / 7.0, 1.0)
        
        # Güçlü duygu varlığı
        strong_emotion_count = len([e for e in emotion_set if e['score'] > 0.4])
        intensity_score = min(strong_emotion_count / 3.0, 1.0)
        
        return (diversity_score + intensity_score) / 2
    
    def _calculate_quality_score(self, video_analysis: Dict = None) -> float:
        """İçerik kalitesi (şimdilik tahmine dayalı)"""
        if video_analysis:
            # Gelecekte Wiro analizinden kalite bilgisi çekeceğiz
            return 0.75
        # Varsayılan orta kalite
        return 0.65 + random.uniform(-0.1, 0.1)
    
    def _calculate_trending_score(self) -> float:
        """Trend faktörleri (şimdilik rastgele)"""
        # Gelecekte gerçek trend verileri kullanılacak
        return 0.6 + random.uniform(-0.15, 0.15)
    
    def _calculate_timing_score(self) -> float:
        """Zamanlama skoru"""
        from datetime import datetime
        
        now = datetime.now()
        hour = now.hour
        day = now.weekday()  # 0=Pazartesi, 6=Pazar
        
        # En iyi saatler: 10-12, 18-21
        if (10 <= hour <= 12) or (18 <= hour <= 21):
            time_score = 0.9
        elif (7 <= hour <= 9) or (12 <= hour <= 18):
            time_score = 0.7
        else:
            time_score = 0.5
        
        # Hafta içi daha iyi
        day_score = 0.8 if day < 5 else 0.6
        
        return (time_score + day_score) / 2
    
    def _get_dominant_emotions(self, emotions: List[Dict]) -> List[Dict]:
        """En baskın 3 duyguyu getir"""
        if not emotions or not emotions[0]:
            return []
        
        emotion_set = emotions[0]
        sorted_emotions = sorted(emotion_set, key=lambda x: x['score'], reverse=True)
        
        return [
            {
                "emotion": e['label'],
                "score": int(e['score'] * 100),
                "emoji": self._get_emotion_emoji(e['label'])
            }
            for e in sorted_emotions[:3]
        ]
    
    def _get_emotion_emoji(self, emotion: str) -> str:
        """Duygu için emoji"""
        emoji_map = {
            'joy': '😊',
            'sadness': '😢',
            'anger': '😠',
            'fear': '😨',
            'surprise': '😲',
            'disgust': '🤢',
            'neutral': '😐'
        }
        return emoji_map.get(emotion, '🎭')
    
    def _generate_recommendations(self, score: int, emotions: List[Dict]) -> List[str]:
        """Skora göre öneriler üret"""
        recommendations = []
        
        if score >= 80:
            recommendations.append("🎉 Harika! Video yüksek viral potansiyele sahip")
            recommendations.append("✅ Hemen paylaş, trend zamanında paylaşım çok önemli")
        elif score >= 60:
            recommendations.append("👍 İyi bir video, küçük iyileştirmelerle viral olabilir")
            recommendations.append("💡 İlk 3 saniyeyi daha çekici hale getir")
        elif score >= 40:
            recommendations.append("⚠️ Orta seviye potansiyel, bazı değişiklikler gerekli")
            recommendations.append("🎬 Daha güçlü duygusal anlar ekle")
            recommendations.append("🎵 Müzik seçimini gözden geçir")
        else:
            recommendations.append("❌ Düşük viral potansiyel, büyük değişiklikler öneririz")
            recommendations.append("🔄 Konsepti tamamen yeniden düşün")
            recommendations.append("📱 Başarılı viral videoları incele ve analiz et")
        
        # Duygu bazlı öneriler
        if emotions and emotions[0]:
            dominant = max(emotions[0], key=lambda x: x['score'])
            if dominant['label'] == 'neutral' and dominant['score'] > 0.4:
                recommendations.append("😐 Video çok nötr, daha fazla duygu katmayı dene")
            elif dominant['label'] == 'sadness' and dominant['score'] > 0.5:
                recommendations.append("💝 Üzücü içerik - umut veren bir son ekle")
        
        recommendations.append("⏰ En iyi paylaşım zamanı: Hafta içi 10-12 veya 18-21 arası")
        
        return recommendations