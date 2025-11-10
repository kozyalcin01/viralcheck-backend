# report_generator.py
from typing import Dict
from datetime import datetime

class ReportGenerator:
    """Güzel formatlanmış raporlar üretir"""
    
    def generate_report(self, viral_data: Dict, video_filename: str) -> Dict:
        """
        Kullanıcı dostu rapor oluştur
        
        Args:
            viral_data: Viral skor verileri
            video_filename: Video dosya adı
        
        Returns:
            Formatlanmış rapor
        """
        
        score = viral_data['viral_score']
        
        report = {
            "video_info": {
                "filename": video_filename,
                "analyzed_at": datetime.now().isoformat(),
                "analysis_version": "1.0"
            },
            "viral_score": {
                "overall": score,
                "rating": self._get_rating(score),
                "emoji": self._get_score_emoji(score)
            },
            "score_breakdown": viral_data['breakdown'],
            "dominant_emotions": viral_data['dominant_emotions'],
            "recommendations": viral_data['recommendations'],
            "best_posting_time": self._get_best_posting_time(),
            "summary": self._generate_summary(score, viral_data)
        }
        
        return report
    
    def _get_rating(self, score: int) -> str:
        """Skoru kelime olarak değerlendir"""
        if score >= 80:
            return "Mükemmel - Yüksek Viral Potansiyel"
        elif score >= 60:
            return "İyi - Orta-Yüksek Viral Potansiyel"
        elif score >= 40:
            return "Orta - Orta Viral Potansiyel"
        else:
            return "Düşük - İyileştirme Gerekli"
    
    def _get_score_emoji(self, score: int) -> str:
        """Skora göre emoji"""
        if score >= 80:
            return "🔥"
        elif score >= 60:
            return "👍"
        elif score >= 40:
            return "😐"
        else:
            return "⚠️"
    
    def _get_best_posting_time(self) -> Dict:
        """En iyi paylaşım zamanı önerisi"""
        return {
            "today": "18:00 - 21:00",
            "tomorrow": "10:00 - 12:00",
            "best_days": ["Salı", "Çarşamba", "Perşembe"],
            "avoid": "Pazar gece"
        }
    
    def _generate_summary(self, score: int, viral_data: Dict) -> str:
        """Özet metin oluştur"""
        dominant = viral_data['dominant_emotions'][0] if viral_data['dominant_emotions'] else None
        
        if score >= 80:
            summary = f"Videonuz {score}/100 puan ile yüksek viral potansiyele sahip! "
        elif score >= 60:
            summary = f"Videonuz {score}/100 puan ile iyi bir performans gösteriyor. "
        elif score >= 40:
            summary = f"Videonuz {score}/100 puan aldı. İyileştirme ile viral olabilir. "
        else:
            summary = f"Videonuz {score}/100 puan aldı. Önemli değişiklikler öneriyoruz. "
        
        if dominant:
            summary += f"En baskın duygu: {dominant['emotion']} ({dominant['score']}%). "
        
        return summary