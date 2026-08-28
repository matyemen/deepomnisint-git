#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║           DeepOmnisint — Configuration Center              ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ScanMode(Enum):
    FAST = "fast"
    NORMAL = "normal"
    DEEP = "deep"
    STEALTH = "stealth"
    ULTRA = "ultra"  # أعمق وأبطأ مع كل الميزات


@dataclass
class ProxySettings:
    enabled: bool = False
    proxy: Optional[str] = None
    proxy_file: Optional[str] = None
    rotate: bool = False
    check_before_use: bool = False
    protocol: str = "http"  # http, https, socks5


@dataclass
class ScannerSettings:
    concurrency: int = 80
    timeout: int = 25
    max_retries: int = 3
    respect_robots_txt: bool = False
    follow_redirects: bool = True
    verify_ssl: bool = False
    max_redirects: int = 5
    request_delay: float = 0.0  # 0 = auto based on mode
    randomize_delay: bool = True
    
    # User-Agent
    rotate_ua: bool = True
    custom_ua: Optional[str] = None
    
    # Cookies
    load_cookies: bool = False
    cookies_file: Optional[str] = None


@dataclass 
class ExtractionSettings:
    extract_name: bool = True
    extract_bio: bool = True
    extract_avatar: bool = True
    extract_location: bool = True
    extract_followers: bool = True
    extract_following: bool = True
    extract_email: bool = True
    extract_phone: bool = True
    extract_website: bool = True
    extract_joined: bool = True
    extract_social_links: bool = True
    extract_json_ld: bool = True
    extract_opengraph: bool = True
    extract_twitter_cards: bool = True
    extract_meta: bool = True
    extract_schema: bool = True
    extract_headers: bool = False
    
    max_bio_length: int = 500
    max_name_length: int = 100


@dataclass
class CorrelationSettings:
    enabled: bool = True
    min_confidence: float = 0.3
    match_name: bool = True
    match_bio: bool = True
    match_location: bool = True
    match_email: bool = True
    match_avatar: bool = True
    match_website: bool = True
    match_phone: bool = True
    use_fuzzy_matching: bool = True
    fuzzy_threshold: float = 0.8


@dataclass
class PermutationSettings:
    enabled: bool = True
    max_variants: int = 50
    use_leet: bool = True
    use_prefixes: bool = True
    use_suffixes: bool = True
    use_transforms: bool = True
    use_reverse: bool = True
    use_numbers: bool = True
    scan_variants: bool = True
    variant_mode: str = "fast"  # fast, normal, deep


@dataclass
class ReportSettings:
    html: bool = True
    json: bool = True
    csv: bool = True
    pdf: bool = False
    txt: bool = True
    output_dir: str = "reports"
    include_screenshots: bool = False
    compress: bool = False
    open_browser: bool = False
    template_dir: Optional[str] = None


@dataclass
class BotSettings:
    enabled: bool = True
    token: str = ""
    admins: List[int] = field(default_factory=list)
    max_concurrent_scans: int = 5
    max_history: int = 100
    language: str = "ar"  # ar, en
    enable_webhook: bool = False
    webhook_url: Optional[str] = None
    webhook_port: int = 8443


@dataclass
class DatabaseSettings:
    enabled: bool = True
    path: str = "omnisint.db"
    auto_cleanup: bool = True
    cleanup_days: int = 30
    backup_enabled: bool = True
    backup_interval: int = 24  # hours


@dataclass
class GlobalConfig:
    """الإعدادات الكاملة للنظام."""
    
    # Metadata
    app_name: str = "DeepOmnisint"
    version: str = "3.0.0"
    author: str = "Omnisint Team"
    
    # User settings
    username: str = ""
    mode: ScanMode = ScanMode.NORMAL
    tags: List[str] = field(default_factory=list)
    verbose: bool = False
    debug: bool = False
    quiet: bool = False
    
    # Sub-configs
    proxy: ProxySettings = field(default_factory=ProxySettings)
    scanner: ScannerSettings = field(default_factory=ScannerSettings)
    extraction: ExtractionSettings = field(default_factory=ExtractionSettings)
    correlation: CorrelationSettings = field(default_factory=CorrelationSettings)
    permutation: PermutationSettings = field(default_factory=PermutationSettings)
    reports: ReportSettings = field(default_factory=ReportSettings)
    bot: BotSettings = field(default_factory=BotSettings)
    database: DatabaseSettings = field(default_factory=DatabaseSettings)
    
    # Paths
    base_dir: str = str(Path(__file__).parent)
    sites_dir: str = str(Path(__file__).parent / "sites")
    reports_dir: str = "reports"
    logs_dir: str = "logs"
    screenshots_dir: str = "screenshots"
    temp_dir: str = "/tmp/omnisint"
    
    def __post_init__(self):
        """معالجة ما بعد الإنشاء."""
        self.base_dir = str(Path(__file__).parent)
        self.sites_dir = os.path.join(self.base_dir, "sites")
        self.reports_dir = os.path.join(self.base_dir, self.reports_dir)
        self.logs_dir = os.path.join(self.base_dir, "logs")
        self.screenshots_dir = os.path.join(self.base_dir, "screenshots")


# الإعدادات الافتراضية
DEFAULT_CONFIG = GlobalConfig()

# إعدادات الوضع العميق
DEEP_CONFIG = GlobalConfig(
    mode=ScanMode.DEEP,
    scanner=ScannerSettings(concurrency=50, timeout=30, max_retries=3),
    extraction=ExtractionSettings(),
    correlation=CorrelationSettings(enabled=True),
    permutation=PermutationSettings(enabled=True, max_variants=30),
    reports=ReportSettings(html=True, json=True, csv=True, pdf=False),
)

# إعدادات الوضع المتخفي
STEALTH_CONFIG = GlobalConfig(
    mode=ScanMode.STEALTH,
    scanner=ScannerSettings(
        concurrency=5, timeout=40, max_retries=5,
        request_delay=2.0, randomize_delay=True,
        rotate_ua=True,
    ),
    proxy=ProxySettings(enabled=True, rotate=True),
    extraction=ExtractionSettings(),
    reports=ReportSettings(html=True),
)


def load_config(path: Optional[str] = None) -> GlobalConfig:
    """تحميل الإعدادات من ملف JSON."""
    if not path:
        path = os.path.join(DEFAULT_CONFIG.base_dir, "config.json")
    
    config = DEFAULT_CONFIG
    
    if os.path.exists(path):
        import json
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # تحديث القيم (تبسيطاً)
            for key, value in data.items():
                if hasattr(config, key):
                    setattr(config, key, value)
        except:
            pass
    
    return config


def save_config(config: GlobalConfig, path: Optional[str] = None):
    """حفظ الإعدادات إلى ملف JSON."""
    if not path:
        path = os.path.join(config.base_dir, "config.json")
    
    import json
    from dataclasses import asdict
    
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(config), f, indent=2, ensure_ascii=False, default=str)
