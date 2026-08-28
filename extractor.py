#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║    DeepOmnisint — Deep Profile Extractor Engine                ║
║    يستخرج: الاسم، البايو، الصورة، الموقع، المتابعين،          ║
║    الإيميل، الهاتف، الموقع الإلكتروني، تاريخ الانضمام،        ║
║    روابط اجتماعية، JSON-LD، OpenGraph، Twitter Cards           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import re
import json
from typing import Dict, List, Optional, Any, Set, Tuple
from urllib.parse import urljoin, urlparse
import logging

log = logging.getLogger("omnisint.extractor")


class DeepExtractor:
    """
    مستخرج البيانات العميق — أقوى بكثير من maigret.
    يستخدم: CSS Selectors + Meta Tags + JSON-LD + OpenGraph + Regex
    """
    
    # أنماط Regex للإيميل والهاتف
    EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    PHONE_PATTERNS = [
        re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'),
        re.compile(r'(\+?\d{1,3})?[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'),
    ]
    
    # أنماط مواقع التواصل
    SOCIAL_PATTERNS = {
        "twitter": re.compile(r'(?:https?://)?(?:www\.)?(?:twitter|x)\.com/([a-zA-Z0-9_]+)'),
        "instagram": re.compile(r'(?:https?://)?(?:www\.)?instagram\.com/([a-zA-Z0-9_.]+)/?'),
        "github": re.compile(r'(?:https?://)?(?:www\.)?github\.com/([a-zA-Z0-9-]+)'),
        "linkedin": re.compile(r'(?:https?://)?(?:www\.)?linkedin\.com/in/([a-zA-Z0-9-]+)'),
        "youtube": re.compile(r'(?:https?://)?(?:www\.)?youtube\.com/@?([a-zA-Z0-9_-]+)'),
        "facebook": re.compile(r'(?:https?://)?(?:www\.)?facebook\.com/([a-zA-Z0-9.]+)'),
        "telegram": re.compile(r'(?:https?://)?(?:t\.me|telegram\.me)/([a-zA-Z0-9_]+)'),
        "tiktok": re.compile(r'(?:https?://)?(?:www\.)?tiktok\.com/@([a-zA-Z0-9_.]+)'),
        "snapchat": re.compile(r'(?:https?://)?(?:www\.)?snapchat\.com/add/([a-zA-Z0-9_-]+)'),
        "discord": re.compile(r'(?:https?://)?(?:www\.)?discord(?:app)?\.com/users/(\d+)'),
    }

    @classmethod
    def extract(cls, html: str, site: Any, base_url: str) -> Dict[str, Any]:
        """
        استخراج كل البيانات الممكنة من صفحة HTML.
        
        Args:
            html: محتوى الصفحة HTML
            site: تعريف الموقع (Site object)
            base_url: URL الأساسي للصفحة
            
        Returns:
            قاموس بكل البيانات المستخرجة
        """
        if not html or not BeautifulSoup:
            return {}
        
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, "lxml")
        profile = {}
        
        # ─── 1. استخراج الاسم ───
        profile["name"] = cls._extract_field(soup, site, "name", site.name_selectors)
        
        # ─── 2. استخراج البايو ───
        profile["bio"] = cls._extract_field(soup, site, "bio", site.bio_selectors)
        
        # ─── 3. استخراج الصورة ───
        profile["avatar"] = cls._extract_attr(soup, site, "avatar", site.avatar_selectors, "src")
        if profile["avatar"]:
            profile["avatar"] = urljoin(base_url, profile["avatar"])
        
        # ─── 4. استخراج الموقع الجغرافي ───
        profile["location"] = cls._extract_field(soup, site, "location", site.location_selectors)
        
        # ─── 5. استخراج المتابعين ───
        profile["followers"] = cls._extract_field(soup, site, "followers", site.followers_selectors)
        
        # ─── 6. استخراج المتابَعين ───
        profile["following"] = cls._extract_field(soup, site, "following", site.following_selectors)
        
        # ─── 7. استخراج الإيميل ───
        profile["email"] = cls._extract_field(soup, site, "email", site.email_selectors)
        if not profile["email"]:
            profile["email"] = cls._extract_email_from_html(html)
        
        # ─── 8. استخراج الهاتف ───
        profile["phone"] = cls._extract_field(soup, site, "phone", site.phone_selectors)
        if not profile["phone"]:
            profile["phone"] = cls._extract_phone_from_html(html)
        
        # ─── 9. استخراج الموقع الإلكتروني ───
        profile["website"] = cls._extract_attr(soup, site, "website", site.website_selectors, "href")
        
        # ─── 10. استخراج تاريخ الانضمام ───
        profile["joined"] = cls._extract_field(soup, site, "joined", site.joined_selectors)
        
        # ─── 11. استخراج الروابط الاجتماعية ───
        profile["social_links"] = cls._extract_social_links(soup)
        if site.social_links_selectors:
            social_text = cls._extract_field(soup, site, "social_links", site.social_links_selectors)
            if social_text:
                profile["social_links_text"] = social_text
        
        # ─── 12. استخراج JSON-LD ───
        profile["json_ld"] = cls._extract_json_ld(soup)
        
        # ─── 13. استخراج OpenGraph ───
        profile["opengraph"] = cls._extract_opengraph(soup)
        
        # ─── 14. استخراج Twitter Cards ───
        profile["twitter_cards"] = cls._extract_twitter_cards(soup)
        
        # ─── 15. استخراج Meta Tags ───
        profile["meta"] = cls._extract_meta(soup)
        
        # ─── 16. استخراج Schema.org ───
        profile["schema"] = cls._extract_schema(soup)
        
        # ─── 17. استخراج By Hugo (مؤلف المقال لو وجد) ───
        profile["author"] = cls._extract_author(soup)
        
        # ─── 18. استخراج العمر (لو موجود) ───
        profile["age"] = cls._extract_age(soup)
        
        # ─── تنظيف وإزالة القيم الفارغة ───
        profile = {k: v for k, v in profile.items() if v is not None and v != {} and v != []}
        
        log.debug(f"استخراج {len(profile)} حقل من {base_url}")
        return profile
    
    @classmethod
    def _extract_field(cls, soup: BeautifulSoup, site: Any, field_name: str,
                       selectors: List[str]) -> Optional[str]:
        """استخراج حقل نصي باستخدام CSS selectors ومن ثم Meta tags."""
        
        # 1. CSS Selectors
        for selector in selectors:
            try:
                if selector.startswith("meta"):
                    tag = soup.select_one(selector)
                    if tag and tag.get("content"):
                        value = tag["content"].strip()
                        if value and " — " not in value:  # تجنب القيم الافتراضية للمواقع
                            return value[:500]
                else:
                    tag = soup.select_one(selector)
                    if tag:
                        value = tag.get_text(strip=True)
                        if value:
                            return value[:500]
            except:
                continue
        
        # 2. Meta tags عامة
        meta_props = {
            "name": ["og:title", "twitter:title", "profile:username", "title"],
            "bio": ["og:description", "twitter:description", "description"],
            "avatar": ["og:image", "twitter:image"],
            "location": ["place:location:latitude", "geo.position"],
        }
        
        if field_name in meta_props:
            for prop in meta_props[field_name]:
                for attr in ["property", "name"]:
                    tag = soup.select_one(f'meta[{attr}="{prop}"]')
                    if tag and tag.get("content"):
                        value = tag["content"].strip()
                        if value:
                            return value[:500]
        
        # 3. Regex أنماط
        if field_name == "email":
            return cls._extract_email_from_html(str(soup))
        if field_name == "phone":
            return cls._extract_phone_from_html(str(soup))
        
        return None
    
    @classmethod
    def _extract_attr(cls, soup: BeautifulSoup, site: Any, field_name: str,
                      selectors: List[str], attr: str = "src") -> Optional[str]:
        """استخراج attribute من عنصر CSS."""
        for selector in selectors:
            try:
                tag = soup.select_one(selector)
                if tag and tag.get(attr):
                    return tag[attr].strip()
            except:
                continue
        return None
    
    @classmethod
    def _extract_email_from_html(cls, html: str) -> Optional[str]:
        """استخراج الإيميل من HTML كامل."""
        # mailto: links
        emails = cls.EMAIL_PATTERN.findall(html)
        valid_emails = [e for e in emails if not e.endswith(('.png', '.jpg', '.gif', '.css', '.js'))
                       and 'example' not in e and 'domain' not in e]
        if valid_emails:
            return valid_emails[0]
        return None
    
    @classmethod
    def _extract_phone_from_html(cls, html: str) -> Optional[str]:
        """استخراج رقم الهاتف من HTML."""
        for pattern in cls.PHONE_PATTERNS:
            match = pattern.search(html)
            if match:
                num = match.group(0).strip()
                if len(num) >= 7:  # أرقام حقيقية
                    return num
        return None
    
    @classmethod
    def _extract_social_links(cls, soup: BeautifulSoup) -> Dict[str, str]:
        """استخراج روابط التواصل الاجتماعي من الصفحة."""
        social = {}
        for name, pattern in cls.SOCIAL_PATTERNS.items():
            for a in soup.select("a[href]"):
                href = a.get("href", "")
                match = pattern.search(href)
                if match:
                    social[name] = href
        return social if social else None
    
    @classmethod
    def _extract_json_ld(cls, soup: BeautifulSoup) -> Optional[Dict]:
        """استخراج JSON-LD (Schema.org) من الصفحة."""
        for script in soup.select("script[type='application/ld+json']"):
            try:
                if script.string:
                    data = json.loads(script.string)
                    if isinstance(data, dict):
                        return data
                    elif isinstance(data, list) and data:
                        return data[0]
            except:
                continue
        return None
    
    @classmethod
    def _extract_opengraph(cls, soup: BeautifulSoup) -> Dict[str, str]:
        """استخراج كل OpenGraph tags من الصفحة."""
        og = {}
        for meta in soup.select("meta[property^='og:']"):
            prop = meta.get("property", "")
            content = meta.get("content", "")
            if prop and content:
                key = prop.replace("og:", "")
                if key not in ["title", "description", "image"]:  # تم استخراجها مسبقاً
                    og[key] = content[:200]
        return og if og else None
    
    @classmethod
    def _extract_twitter_cards(cls, soup: BeautifulSoup) -> Dict[str, str]:
        """استخراج Twitter Cards من الصفحة."""
        tc = {}
        for meta in soup.select("meta[name^='twitter:']"):
            name = meta.get("name", "")
            content = meta.get("content", "")
            if name and content:
                key = name.replace("twitter:", "")
                if key not in ["title", "description", "image"]:
                    tc[key] = content[:200]
        return tc if tc else None
    
    @classmethod
    def _extract_meta(cls, soup: BeautifulSoup) -> Dict[str, str]:
        """استخراج meta tags مهمة."""
        meta = {}
        important_metas = ["author", "keywords", "application-name", "generator",
                          "theme-color", "robots", "viewport"]
        for name in important_metas:
            tag = soup.select_one(f'meta[name="{name}"]')
            if tag and tag.get("content"):
                meta[name] = tag["content"][:200]
        return meta if meta else None
    
    @classmethod
    def _extract_schema(cls, soup: BeautifulSoup) -> Optional[Dict]:
        """استخراج Schema.org data من HTML (مبسط)."""
        schemas = {}
        for itemtype in ["Person", "Organization", "WebSite", "ProfilePage"]:
            for elem in soup.select(f'[itemtype*="{itemtype}"]'):
                props = {}
                for prop in elem.select("[itemprop]"):
                    name = prop.get("itemprop", "")
                    value = (prop.get("content") or prop.get("src") or 
                            prop.get("href") or prop.get_text(strip=True))
                    if name and value:
                        props[name] = value[:200]
                if props:
                    schemas[itemtype] = props
        return schemas if schemas else None
    
    @classmethod
    def _extract_author(cls, soup: BeautifulSoup) -> Optional[str]:
        """استخراج اسم المؤلف من الصفحة."""
        selectors = [
            "meta[name='author']",
            "meta[property='article:author']",
            "a[rel='author']",
            ".author",
            "[itemprop='author']",
            "[class*='author']",
        ]
        for selector in selectors:
            try:
                tag = soup.select_one(selector)
                if tag:
                    value = (tag.get("content") or tag.get_text(strip=True) or "").strip()
                    if value:
                        return value[:100]
            except:
                continue
        return None
    
    @classmethod
    def _extract_age(cls, soup: BeautifulSoup) -> Optional[str]:
        """استخراج العمر من الصفحة."""
        age_patterns = [
            re.compile(r'(\d+)\s*(?:year|yr|سنة|عام)', re.IGNORECASE),
            re.compile(r'(?:age|العمر|سن)\s*:?\s*(\d+)', re.IGNORECASE),
        ]
        text = soup.get_text()
        for pattern in age_patterns:
            match = pattern.search(text)
            if match:
                return match.group(0).strip()[:50]
        return None


# استيراد BeautifulSoup بطريقة آمنة
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None
