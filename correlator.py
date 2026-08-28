#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║    DeepOmnisint — Cross-Platform Correlation Engine            ║
║    يربط الحسابات عبر المنصات المختلفة باستخدام:               ║
║    • الاسم (Name) — exact + partial + fuzzy                    ║
║    • البايو (Bio) — word overlap + embedding                   ║
║    • الموقع (Location) — exact + hierarchical                  ║
║    • الإيميل (Email) — exact match = 100%                      ║
║    • الصورة (Avatar) — same URL = same person                  ║
║    • الموقع الإلكتروني (Website) — same domain                 ║
║    • الهاتف (Phone) — exact                                    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import urlparse
from dataclasses import dataclass, field

log = logging.getLogger("omnisint.correlator")


@dataclass
class CorrelationResult:
    """نتيجة رابط بين حسابين."""
    site_a: str
    site_b: str
    confidence: float = 0.0
    matched_fields: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


class CorrelationEngine:
    """
    محرك ربط الحسابات — يكتشف إن كان حسابان على منصتين مختلفتين
    يعودان لنفس الشخص.
    """
    
    # أوزان كل حقل
    WEIGHTS = {
        "email_exact": 1.0,
        "phone_exact": 0.95,
        "name_exact": 0.6,
        "name_fuzzy": 0.4,
        "avatar_exact": 0.7,
        "website_exact": 0.5,
        "website_domain": 0.4,
        "bio_exact": 0.5,
        "bio_similar": 0.3,
        "location_exact": 0.4,
        "location_city": 0.3,
        "name_reversed": 0.3,
        "social_link": 0.6,
    }
    
    def __init__(self, min_confidence: float = 0.3, use_fuzzy: bool = True):
        self.min_confidence = min_confidence
        self.use_fuzzy = use_fuzzy
    
    def correlate(self, profiles: Dict[str, Dict]) -> List[CorrelationResult]:
        """
        ربط جميع الحسابات مع بعضها البعض.
        
        Args:
            profiles: قاموس {site_name: profile_data}
            
        Returns:
            قائمة من الارتباطات مرتبة حسب الثقة
        """
        results = []
        sites = list(profiles.keys())
        
        for i in range(len(sites)):
            for j in range(i + 1, len(sites)):
                site_a, site_b = sites[i], sites[j]
                profile_a = profiles.get(site_a, {})
                profile_b = profiles.get(site_b, {})
                
                if not profile_a or not profile_b:
                    continue
                
                result = self._compare_profiles(site_a, site_b, profile_a, profile_b)
                if result.confidence >= self.min_confidence:
                    results.append(result)
        
        # ترتيب حسب الثقة
        results.sort(key=lambda r: r.confidence, reverse=True)
        return results
    
    def _compare_profiles(self, site_a: str, site_b: str,
                          pa: Dict, pb: Dict) -> CorrelationResult:
        """مقارنة حسابين وحساب الثقة."""
        result = CorrelationResult(site_a=site_a, site_b=site_b)
        confidence = 0.0
        matched = []
        
        # ─── 1. مقارنة الإيميل ───
        email_a = (pa.get("email") or "").lower().strip()
        email_b = (pb.get("email") or "").lower().strip()
        if email_a and email_b and email_a == email_b:
            confidence += self.WEIGHTS["email_exact"]
            matched.append("email_exact")
            result.details["email"] = email_a
        
        # ─── 2. مقارنة الهاتف ───
        phone_a = (pa.get("phone") or "").strip()
        phone_b = (pb.get("phone") or "").strip()
        if phone_a and phone_b and phone_a == phone_b:
            confidence += self.WEIGHTS["phone_exact"]
            matched.append("phone_exact")
        
        # ─── 3. مقارنة الاسم ───
        name_a = (pa.get("name") or "").lower().strip()
        name_b = (pb.get("name") or "").lower().strip()
        if name_a and name_b:
            if name_a == name_b:
                confidence += self.WEIGHTS["name_exact"]
                matched.append("name_exact")
            elif self.use_fuzzy:
                # تطابق جزئي
                words_a = set(name_a.split())
                words_b = set(name_b.split())
                if words_a & words_b:  # تقاطع
                    overlap = len(words_a & words_b) / max(len(words_a | words_b), 1)
                    if overlap >= 0.5:
                        confidence += self.WEIGHTS["name_fuzzy"] * overlap
                        matched.append("name_fuzzy")
        
        # ─── 4. مقارنة الصورة ───
        avatar_a = (pa.get("avatar") or "").strip()
        avatar_b = (pb.get("avatar") or "").strip()
        if avatar_a and avatar_b:
            if avatar_a == avatar_b:
                confidence += self.WEIGHTS["avatar_exact"]
                matched.append("avatar_exact")
        
        # ─── 5. مقارنة الموقع الإلكتروني ───
        web_a = (pa.get("website") or "").lower().strip()
        web_b = (pb.get("website") or "").lower().strip()
        if web_a and web_b:
            if web_a == web_b:
                confidence += self.WEIGHTS["website_exact"]
                matched.append("website_exact")
            else:
                domain_a = urlparse(web_a).netloc
                domain_b = urlparse(web_b).netloc
                if domain_a and domain_b and domain_a == domain_b:
                    confidence += self.WEIGHTS["website_domain"]
                    matched.append("website_domain")
        
        # ─── 6. مقارنة البايو ───
        bio_a = (pa.get("bio") or "").lower().strip()
        bio_b = (pb.get("bio") or "").lower().strip()
        if bio_a and bio_b and len(bio_a) > 10 and len(bio_b) > 10:
            if bio_a == bio_b:
                confidence += self.WEIGHTS["bio_exact"]
                matched.append("bio_exact")
            else:
                words_a = set(bio_a.split())
                words_b = set(bio_b.split())
                overlap = len(words_a & words_b)
                if overlap >= 3:
                    sim = overlap / max(len(words_a | words_b), 1)
                    confidence += self.WEIGHTS["bio_similar"] * sim
                    matched.append("bio_similar")
        
        # ─── 7. مقارنة الموقع الجغرافي ───
        loc_a = (pa.get("location") or "").lower().strip()
        loc_b = (pb.get("location") or "").lower().strip()
        if loc_a and loc_b:
            if loc_a == loc_b:
                confidence += self.WEIGHTS["location_exact"]
                matched.append("location_exact")
            else:
                # مقارنة أجزاء (مدينة، دولة)
                parts_a = set(loc_a.split(","))
                parts_b = set(loc_b.split(","))
                if parts_a & parts_b:
                    confidence += self.WEIGHTS["location_city"]
                    matched.append("location_city")
        
        # ─── 8. مقارنة الروابط الاجتماعية ───
        social_a = pa.get("social_links", {}) or {}
        social_b = pb.get("social_links", {}) or {}
        if isinstance(social_a, dict) and isinstance(social_b, dict):
            for platform, url in social_a.items():
                if platform in social_b and social_b[platform] == url:
                    confidence += self.WEIGHTS["social_link"]
                    matched.append(f"social_{platform}")
                    result.details[f"social_{platform}"] = url
        
        # ─── تطبيع الثقة ───
        result.confidence = round(min(confidence, 1.0), 2)
        result.matched_fields = matched
        
        log.debug(f"الارتباط {site_a} ↔ {site_b}: {result.confidence*100:.0f}% "
                  f"[{', '.join(matched)}]")
        
        return result
