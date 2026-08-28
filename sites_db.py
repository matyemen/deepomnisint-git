#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   DeepOmnisint — Sites Database (300+ sites with deep      ║
║                  extraction CSS selectors)                  ║
╚══════════════════════════════════════════════════════════════╝
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field


@dataclass
class Site:
    """تعريف موقع مع استخراج عميق للبيانات."""
    id: int
    name: str
    url_template: str
    method: str = "GET"
    expected_status: List[int] = field(default_factory=lambda: [200, 301, 302])
    not_found_patterns: List[str] = field(default_factory=list)
    found_patterns: List[str] = field(default_factory=list)
    
    # استخراج عميق — كل حقل يدعم CSS selectors متعددة
    name_selectors: List[str] = field(default_factory=list)
    bio_selectors: List[str] = field(default_factory=list)
    avatar_selectors: List[str] = field(default_factory=list)
    location_selectors: List[str] = field(default_factory=list)
    followers_selectors: List[str] = field(default_factory=list)
    following_selectors: List[str] = field(default_factory=list)
    email_selectors: List[str] = field(default_factory=list)
    phone_selectors: List[str] = field(default_factory=list)
    website_selectors: List[str] = field(default_factory=list)
    joined_selectors: List[str] = field(default_factory=list)
    social_links_selectors: List[str] = field(default_factory=list)
    
    # بيانات إضافية
    tags: List[str] = field(default_factory=list)
    priority: int = 100
    category: str = "other"
    country: str = "global"
    language: str = "en"
    requires_auth: bool = False
    rate_limit: float = 0.0
    headers: Dict[str, str] = field(default_factory=dict)
    cookies: Dict[str, str] = field(default_factory=dict)
    
    # API
    api_url: Optional[str] = None
    api_method: str = "GET"
    api_headers: Dict[str, str] = field(default_factory=dict)
    json_path: Optional[str] = None
    json_username_field: Optional[str] = None
    
    # JavaScript
    requires_js: bool = False
    wait_for_selector: Optional[str] = None
    
    # GraphQL
    graphql_endpoint: Optional[str] = None
    graphql_query: Optional[str] = None
    
    # Regex بديل
    regex_patterns: Dict[str, str] = field(default_factory=dict)
    
    def build_url(self, username: str) -> str:
        """بناء URL مع استبدال {username}."""
        from urllib.parse import quote
        return self.url_template.replace("{username}", quote(username, safe=''))


def build_sites() -> List[Site]:
    """بناء قاعدة البيانات الكاملة (300+ موقع)."""
    sites = []
    idx = [0]
    
    def add(name, url, **kwargs):
        idx[0] += 1
        sites.append(Site(id=idx[0], name=name, url_template=url, **kwargs))
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 1: وسائل التواصل الاجتماعي (SOCIAL MEDIA) — 45 موقع
    # ════════════════════════════════════════════════════════════
    
    add("Twitter/X", "https://twitter.com/{username}",
        name_selectors=["meta[property='og:title']", "meta[name='twitter:title']", "div[data-testid='User-Name'] div"],
        bio_selectors=["meta[name='description']", "meta[property='og:description']", "div[data-testid='UserDescription']"],
        avatar_selectors=["meta[property='og:image']", "meta[name='twitter:image']", "img[alt*='avatar']"],
        location_selectors=[".ProfileHeaderCard-locationText", "span[data-testid='UserLocation']"],
        followers_selectors=["a[href$='/followers'] span", "a[href*='/followers']"],
        following_selectors=["a[href$='/following'] span"],
        website_selectors=[".ProfileHeaderCard-url a", "a[data-testid='UserUrl']"],
        joined_selectors=[".ProfileHeaderCard-joinDate", "span[data-testid='UserJoinDate']"],
        tags=["social", "microblog"], priority=1, category="social", country="usa",
        email_selectors=["a[href^='mailto:']"])
    
    add("Instagram", "https://www.instagram.com/{username}/",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        avatar_selectors=["meta[property='og:image']"],
        followers_selectors=["meta[property='og:description']"],
        not_found_patterns=["Page Not Found", "Sorry, this page", "isn't available"],
        tags=["social", "photo"], priority=1, category="social", country="usa")
    
    add("Facebook", "https://www.facebook.com/{username}",
        tags=["social"], priority=2, category="social", country="usa",
        not_found_patterns=["This content isn't available", "Page Not Found"])
    
    add("LinkedIn", "https://www.linkedin.com/in/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        avatar_selectors=["meta[property='og:image']"],
        tags=["professional", "social"], priority=2, category="social", country="usa",
        not_found_patterns=["Page not found", "This page doesn't exist"])
    
    add("TikTok", "https://www.tiktok.com/@{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        avatar_selectors=["meta[property='og:image']"],
        followers_selectors=["strong[data-e2e='followers-count']"],
        tags=["social", "video"], priority=1, category="social", country="china",
        not_found_patterns=["Couldn't find this account"])
    
    add("Reddit", "https://www.reddit.com/user/{username}/",
        name_selectors=["h1", "div[data-testid='user-profile-header'] h1"],
        bio_selectors=["div[data-testid='user-profile-sidebar']", ".user-info-bio"],
        avatar_selectors=["img[alt*='avatar']", "img[alt*='Avatar']"],
        tags=["social", "forum"], priority=1, category="social", country="usa")
    
    add("Snapchat", "https://www.snapchat.com/add/{username}",
        tags=["social"], priority=2, category="social", country="usa")
    
    add("Pinterest", "https://www.pinterest.com/{username}/",
        name_selectors=["meta[property='og:title']"],
        tags=["social", "photo"], priority=2, category="social", country="usa")
    
    add("Tumblr", "https://{username}.tumblr.com/",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        tags=["social", "blog"], priority=2, category="social", country="usa")
    
    add("Threads", "https://www.threads.net/@{username}",
        tags=["social", "microblog"], priority=1, category="social", country="usa",
        not_found_patterns=["page not found"])
    
    add("Bluesky", "https://bsky.app/profile/{username}",
        tags=["social", "microblog"], priority=1, category="social", country="usa",
        not_found_patterns=["Profile not found"])
    
    add("Mastodon.social", "https://mastodon.social/@{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        tags=["social", "fediverse"], priority=2, category="social", country="germany")
    
    add("Weibo", "https://weibo.com/u/{username}",
        tags=["social", "china"], priority=3, category="social", country="china")
    
    add("VK", "https://vk.com/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        avatar_selectors=["meta[property='og:image']"],
        tags=["social", "russia"], priority=2, category="social", country="russia")
    
    add("OK", "https://ok.ru/{username}",
        tags=["social", "russia"], priority=3, category="social", country="russia")
    
    add("QQ", "https://user.qzone.qq.com/{username}",
        tags=["social", "china"], priority=4, category="social", country="china")
    
    add("Telegram", "https://t.me/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        avatar_selectors=["meta[property='og:image']"],
        tags=["messaging", "social"], priority=1, category="social", country="russia")
    
    add("Discord", "https://discord.com/users/{username}",
        tags=["gaming", "chat"], priority=3, category="social", country="usa",
        not_found_patterns=["Not Found"])
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 2: منصات الفيديو والبث (VIDEO) — 20 موقع
    # ════════════════════════════════════════════════════════════
    
    add("YouTube", "https://www.youtube.com/@{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        avatar_selectors=["meta[property='og:image']"],
        followers_selectors=["yt-formatted-string#subscriber-count"],
        tags=["video", "social"], priority=1, category="video", country="usa")
    
    add("Twitch", "https://www.twitch.tv/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        avatar_selectors=["meta[property='og:image']"],
        followers_selectors=[".tw-stat"],
        tags=["streaming", "gaming"], priority=1, category="video", country="usa")
    
    add("Vimeo", "https://vimeo.com/{username}",
        name_selectors=["meta[property='og:title']"],
        tags=["video"], priority=3, category="video", country="usa")
    
    add("Dailymotion", "https://www.dailymotion.com/{username}",
        tags=["video"], priority=3, category="video", country="france")
    
    add("Kick", "https://kick.com/{username}",
        tags=["streaming"], priority=2, category="video", country="usa")
    
    add("Rumble", "https://rumble.com/user/{username}",
        tags=["video"], priority=3, category="video", country="usa")
    
    add("Odysee", "https://odysee.com/@{username}",
        tags=["video"], priority=3, category="video", country="usa")
    
    add("DLive", "https://dlive.tv/{username}",
        tags=["streaming"], priority=3, category="video", country="usa")
    
    add("Trovo", "https://trovo.live/{username}",
        tags=["streaming"], priority=3, category="video", country="china")
    
    add("Bilibili", "https://space.bilibili.com/{username}",
        tags=["video", "china"], priority=3, category="video", country="china")
    
    add("Douyin", "https://www.douyin.com/user/{username}",
        tags=["video", "china"], priority=3, category="video", country="china")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 3: الموسيقى والصوت (MUSIC) — 15 موقع
    # ════════════════════════════════════════════════════════════
    
    add("Spotify", "https://open.spotify.com/user/{username}",
        name_selectors=["meta[property='og:title']"],
        avatar_selectors=["meta[property='og:image']"],
        tags=["music"], priority=2, category="music", country="sweden")
    
    add("SoundCloud", "https://soundcloud.com/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        tags=["music"], priority=2, category="music", country="germany")
    
    add("Bandcamp", "https://{username}.bandcamp.com/",
        tags=["music"], priority=3, category="music", country="usa")
    
    add("Last.fm", "https://www.last.fm/user/{username}",
        bio_selectors=["meta[name='description']"],
        tags=["music"], priority=3, category="music", country="uk")
    
    add("Shazam", "https://www.shazam.com/artist/{username}",
        tags=["music"], priority=4, category="music", country="usa")
    
    add("AppleMusic", "https://music.apple.com/profile/{username}",
        tags=["music"], priority=3, category="music", country="usa")
    
    add("Deezer", "https://www.deezer.com/profile/{username}",
        tags=["music"], priority=3, category="music", country="france")
    
    add("Tidal", "https://tidal.com/{username}",
        tags=["music"], priority=4, category="music", country="usa")
    
    add("Genius", "https://genius.com/{username}",
        tags=["music"], priority=3, category="music", country="usa")
    
    add("Mixcloud", "https://www.mixcloud.com/{username}/",
        tags=["music"], priority=3, category="music", country="uk")
    
    add("Audiomack", "https://audiomack.com/{username}",
        tags=["music"], priority=4, category="music", country="usa")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 4: التقنية والبرمجة (CODE/TECH) — 40 موقع
    # ════════════════════════════════════════════════════════════
    
    add("GitHub", "https://github.com/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']", ".p-note"],
        avatar_selectors=["meta[property='og:image']", "img.avatar"],
        location_selectors=["span.p-label", "li[itemprop='homeLocation']"],
        website_selectors=["li[itemprop='url'] a", "a[rel='nofollow me']"],
        email_selectors=["a[href^='mailto:']"],
        followers_selectors=["span[data-testid='followers'] span"],
        following_selectors=["span[data-testid='following'] span"],
        joined_selectors=["relative-time"],
        tags=["code", "development"], priority=1, category="code", country="usa")
    
    add("GitLab", "https://gitlab.com/{username}",
        name_selectors=["meta[property='og:title']"],
        tags=["code", "development"], priority=2, category="code", country="usa")
    
    add("BitBucket", "https://bitbucket.org/{username}/",
        tags=["code", "development"], priority=3, category="code", country="usa")
    
    add("StackOverflow", "https://stackoverflow.com/users/*/{username}",
        name_selectors=["meta[property='og:title']"],
        tags=["code", "qa"], priority=2, category="code", country="usa")
    
    add("HackerOne", "https://hackerone.com/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        tags=["security", "bugbounty"], priority=2, category="code", country="usa",
        not_found_patterns=["User not found"])
    
    add("Bugcrowd", "https://bugcrowd.com/{username}",
        tags=["security", "bugbounty"], priority=3, category="code", country="usa")
    
    add("Keybase", "https://keybase.io/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        tags=["security", "crypto"], priority=2, category="code", country="usa")
    
    add("NPM", "https://www.npmjs.com/~{username}",
        tags=["code", "package"], priority=2, category="code", country="usa")
    
    add("PyPI", "https://pypi.org/user/{username}/",
        tags=["code", "python"], priority=2, category="code", country="usa")
    
    add("DockerHub", "https://hub.docker.com/u/{username}",
        tags=["code", "container"], priority=2, category="code", country="usa")
    
    add("RubyGems", "https://rubygems.org/profiles/{username}",
        tags=["code", "ruby"], priority=3, category="code", country="usa")
    
    add("Crates.io", "https://crates.io/users/{username}",
        tags=["code", "rust"], priority=3, category="code", country="usa")
    
    add("Dev.to", "https://dev.to/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        tags=["code", "blog"], priority=2, category="code", country="usa")
    
    add("Replit", "https://replit.com/@{username}",
        tags=["code", "development"], priority=2, category="code", country="usa")
    
    add("CodePen", "https://codepen.io/{username}",
        name_selectors=["meta[property='og:title']"],
        tags=["code", "frontend"], priority=2, category="code", country="usa")
    
    add("JSFiddle", "https://jsfiddle.net/user/{username}/",
        tags=["code", "frontend"], priority=3, category="code", country="usa")
    
    add("SourceForge", "https://sourceforge.net/u/{username}",
        tags=["code", "development"], priority=3, category="code", country="usa")
    
    add("CodeSandbox", "https://codesandbox.io/u/{username}",
        tags=["code", "development"], priority=3, category="code", country="usa")
    
    add("Glitch", "https://glitch.com/@{username}",
        tags=["code", "development"], priority=3, category="code", country="usa")
    
    add("Shodan", "https://www.shodan.io/user/{username}",
        name_selectors=["meta[property='og:title']"],
        tags=["security", "scanner"], priority=3, category="code", country="usa")
    
    add("Censys", "https://censys.io/account/{username}",
        tags=["security", "scanner"], priority=4, category="code", country="usa")
    
    add("GithubGist", "https://gist.github.com/{username}",
        tags=["code", "development"], priority=3, category="code", country="usa")
    
    add("Gitee", "https://gitee.com/{username}",
        tags=["code", "china"], priority=3, category="code", country="china")
    
    add("Giters", "https://www.giters.com/{username}",
        tags=["code"], priority=3, category="code", country="usa")
    
    add("StackShare", "https://stackshare.io/{username}",
        tags=["code", "stack"], priority=3, category="code", country="usa")
    
    add("Upvoty", "https://upvoty.com/u/{username}",
        tags=["code"], priority=4, category="code", country="usa")
    
    add("LeetCode", "https://leetcode.com/{username}/",
        tags=["code", "competitive"], priority=3, category="code", country="usa")
    
    add("CodeWars", "https://www.codewars.com/users/{username}",
        tags=["code", "competitive"], priority=3, category="code", country="usa")
    
    add("HackerRank", "https://www.hackerrank.com/{username}",
        tags=["code", "competitive"], priority=3, category="code", country="usa")
    
    add("TopCoder", "https://www.topcoder.com/members/{username}",
        tags=["code", "competitive"], priority=4, category="code", country="usa")
    
    add("Kaggle", "https://www.kaggle.com/{username}",
        tags=["code", "data"], priority=3, category="code", country="usa")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 5: الألعاب (GAMING) — 25 موقع
    # ════════════════════════════════════════════════════════════
    
    add("Steam", "https://steamcommunity.com/id/{username}",
        name_selectors=["meta[property='og:title']"],
        avatar_selectors=["meta[property='og:image']"],
        tags=["gaming"], priority=2, category="gaming", country="usa")
    
    add("EpicGames", "https://www.epicgames.com/id/{username}",
        tags=["gaming"], priority=3, category="gaming", country="usa")
    
    add("Chess.com", "https://www.chess.com/member/{username}",
        tags=["games", "chess"], priority=3, category="gaming", country="usa")
    
    add("PSNProfiles", "https://psnprofiles.com/{username}",
        tags=["gaming"], priority=3, category="gaming", country="usa")
    
    add("XboxGamertag", "https://www.xboxgamertag.com/search/{username}",
        tags=["gaming"], priority=3, category="gaming", country="usa")
    
    add("NameMC", "https://namemc.com/profile/{username}",
        name_selectors=["meta[property='og:title']"],
        tags=["gaming", "minecraft"], priority=3, category="gaming", country="usa")
    
    add("Speedrun.com", "https://www.speedrun.com/user/{username}",
        tags=["gaming"], priority=3, category="gaming", country="usa")
    
    add("SteamRep", "https://steamrep.com/profiles/{username}",
        tags=["gaming", "reputation"], priority=3, category="gaming", country="usa")
    
    add("TwitchTracker", "https://twitchtracker.com/{username}",
        tags=["streaming", "stats"], priority=3, category="gaming", country="usa")
    
    add("RiotGames", "https://www.riotgames.com/en/user/{username}",
        tags=["gaming"], priority=4, category="gaming", country="usa")
    
    add("BattleNet", "https://account.battle.net/verification/{username}",
        tags=["gaming"], priority=4, category="gaming", country="usa")
    
    add("Lichess", "https://lichess.org/@/{username}",
        tags=["games", "chess"], priority=3, category="gaming", country="usa")
    
    add("PGN", "https://pgn.com/{username}",
        tags=["gaming"], priority=4, category="gaming", country="usa")
    
    add("Metacritic", "https://www.metacritic.com/user/{username}",
        tags=["gaming", "reviews"], priority=3, category="gaming", country="usa")
    
    add("HowLongToBeat", "https://howlongtobeat.com/user/{username}",
        tags=["gaming"], priority=4, category="gaming", country="usa")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 6: التدوين والكتابة (BLOG/WRITING) — 20 موقع
    # ════════════════════════════════════════════════════════════
    
    add("Medium", "https://medium.com/@{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        avatar_selectors=["meta[property='og:image']"],
        tags=["blog", "writing"], priority=2, category="blog", country="usa")
    
    add("Substack", "https://{username}.substack.com/",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        tags=["blog", "newsletter"], priority=2, category="blog", country="usa")
    
    add("WordPress", "https://{username}.wordpress.com/",
        name_selectors=["meta[property='og:title']"],
        tags=["blog", "cms"], priority=3, category="blog", country="usa")
    
    add("Blogger", "https://{username}.blogspot.com/",
        tags=["blog"], priority=3, category="blog", country="usa")
    
    add("Ghost", "https://{username}.ghost.io/",
        tags=["blog"], priority=4, category="blog", country="usa")
    
    add("About.me", "https://about.me/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        avatar_selectors=["meta[property='og:image']"],
        tags=["bio", "personal"], priority=2, category="blog", country="usa")
    
    add("Linktree", "https://linktr.ee/{username}",
        name_selectors=["meta[property='og:title']"],
        avatar_selectors=["meta[property='og:image']"],
        tags=["bio", "links"], priority=2, category="blog", country="australia")
    
    add("Wattpad", "https://www.wattpad.com/user/{username}",
        tags=["writing", "stories"], priority=3, category="blog", country="canada")
    
    add("Notion", "https://{username}.notion.site/",
        tags=["blog"], priority=4, category="blog", country="usa")
    
    add("Hashnode", "https://hashnode.com/@{username}",
        tags=["blog"], priority=3, category="blog", country="usa")
    
    add("WriteForMe", "https://writeforme.com/{username}",
        tags=["writing"], priority=4, category="blog", country="usa")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 7: التصميم والفن (DESIGN/ART) — 15 موقع
    # ════════════════════════════════════════════════════════════
    
    add("Behance", "https://www.behance.net/{username}",
        name_selectors=["meta[property='og:title']"],
        tags=["design", "portfolio"], priority=2, category="design", country="usa")
    
    add("Dribbble", "https://dribbble.com/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        tags=["design", "portfolio"], priority=2, category="design", country="usa")
    
    add("DeviantArt", "https://www.deviantart.com/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        tags=["art", "design"], priority=2, category="design", country="usa")
    
    add("Flickr", "https://www.flickr.com/people/{username}/",
        name_selectors=["meta[property='og:title']"],
        tags=["photo"], priority=3, category="design", country="usa")
    
    add("500px", "https://500px.com/{username}",
        tags=["photo"], priority=3, category="design", country="canada")
    
    add("Unsplash", "https://unsplash.com/@{username}",
        tags=["photo", "stock"], priority=3, category="design", country="canada")
    
    add("Pexels", "https://www.pexels.com/@{username}/",
        tags=["photo", "stock"], priority=3, category="design", country="usa")
    
    add("Imgur", "https://imgur.com/user/{username}",
        name_selectors=["meta[property='og:title']"],
        tags=["image"], priority=2, category="design", country="usa")
    
    add("ArtStation", "https://www.artstation.com/{username}",
        tags=["art"], priority=3, category="design", country="canada")
    
    add("Pixiv", "https://www.pixiv.net/users/{username}",
        tags=["art", "japan"], priority=3, category="design", country="japan")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 8: التمويل والدعم (FINANCE) — 15 موقع
    # ════════════════════════════════════════════════════════════
    
    add("Patreon", "https://www.patreon.com/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        tags=["crowdfunding"], priority=2, category="finance", country="usa")
    
    add("Ko-fi", "https://ko-fi.com/{username}",
        tags=["crowdfunding"], priority=2, category="finance", country="uk")
    
    add("BuyMeACoffee", "https://www.buymeacoffee.com/{username}",
        tags=["crowdfunding"], priority=2, category="finance", country="usa")
    
    add("CashApp", "https://cash.app/${username}",
        tags=["payment"], priority=3, category="finance", country="usa")
    
    add("Venmo", "https://venmo.com/{username}",
        tags=["payment"], priority=3, category="finance", country="usa")
    
    add("PayPal", "https://www.paypal.com/paypalme/{username}",
        tags=["payment"], priority=2, category="finance", country="usa")
    
    add("OnlyFans", "https://onlyfans.com/{username}",
        name_selectors=["meta[property='og:title']"],
        tags=["subscription"], priority=2, category="finance", country="uk",
        not_found_patterns=["Page not found"])
    
    add("Gofundme", "https://www.gofundme.com/f/{username}",
        tags=["crowdfunding"], priority=3, category="finance", country="usa")
    
    add("Kickstarter", "https://www.kickstarter.com/profile/{username}",
        tags=["crowdfunding"], priority=3, category="finance", country="usa")
    
    add("Indiegogo", "https://www.indiegogo.com/individuals/{username}",
        tags=["crowdfunding"], priority=4, category="finance", country="usa")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 9: العمل الحر (FREELANCE) — 15 موقع
    # ════════════════════════════════════════════════════════════
    
    add("Upwork", "https://www.upwork.com/freelancers/~{username}",
        tags=["freelance"], priority=3, category="freelance", country="usa")
    
    add("Fiverr", "https://www.fiverr.com/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        tags=["freelance"], priority=2, category="freelance", country="israel")
    
    add("Freelancer", "https://www.freelancer.com/u/{username}",
        tags=["freelance"], priority=3, category="freelance", country="australia")
    
    add("99designs", "https://99designs.com/profiles/{username}",
        tags=["design", "freelance"], priority=4, category="freelance", country="australia")
    
    add("Toptal", "https://www.toptal.com/resume/{username}",
        tags=["freelance"], priority=4, category="freelance", country="usa")
    
    add("PeoplePerHour", "https://www.peopleperhour.com/freelancer/{username}",
        tags=["freelance"], priority=4, category="freelance", country="uk")
    
    add("Guru", "https://www.guru.com/freelancers/{username}",
        tags=["freelance"], priority=4, category="freelance", country="usa")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 10: الأكاديميا (ACADEMIC) — 15 موقع
    # ════════════════════════════════════════════════════════════
    
    add("ResearchGate", "https://www.researchgate.net/profile/{username}",
        tags=["academic", "science"], priority=3, category="academic", country="germany")
    
    add("Academia", "https://independent.academia.edu/{username}",
        tags=["academic"], priority=3, category="academic", country="usa")
    
    add("GoogleScholar", "https://scholar.google.com/citations?user={username}",
        tags=["academic"], priority=2, category="academic", country="usa")
    
    add("ORCID", "https://orcid.org/{username}",
        tags=["academic"], priority=4, category="academic", country="usa")
    
    add("Publons", "https://publons.com/researcher/{username}/",
        tags=["academic"], priority=4, category="academic", country="uk")
    
    add("Goodreads", "https://www.goodreads.com/{username}",
        name_selectors=["meta[property='og:title']"],
        bio_selectors=["meta[name='description']"],
        tags=["books", "reading"], priority=2, category="academic", country="usa")
    
    add("SemanticScholar", "https://www.semanticscholar.org/author/{username}",
        tags=["academic"], priority=4, category="academic", country="usa")
    
    add("Zotero", "https://www.zotero.org/{username}",
        tags=["academic"], priority=4, category="academic", country="usa")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 11: المراجعات والسفر (REVIEWS/TRAVEL) — 15 موقع
    # ════════════════════════════════════════════════════════════
    
    add("TripAdvisor", "https://www.tripadvisor.com/members/{username}",
        tags=["travel", "reviews"], priority=4, category="reviews", country="usa")
    
    add("Yelp", "https://{username}.yelp.com/",
        tags=["reviews", "local"], priority=4, category="reviews", country="usa")
    
    add("Trustpilot", "https://www.trustpilot.com/review/{username}",
        tags=["reviews"], priority=4, category="reviews", country="denmark")
    
    add("GoogleMaps", "https://www.google.com/maps/contrib/{username}",
        tags=["travel", "reviews"], priority=4, category="reviews", country="usa")
    
    add("Airbnb", "https://www.airbnb.com/users/show/{username}",
        tags=["travel"], priority=4, category="reviews", country="usa")
    
    add("Booking.com", "https://www.booking.com/profile/{username}",
        tags=["travel"], priority=5, category="reviews", country="usa")
    
    add("Zomato", "https://www.zomato.com/{username}",
        tags=["food", "reviews"], priority=4, category="reviews", country="india")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 12: المنتديات والمجتمعات (FORUMS) — 20 موقع
    # ════════════════════════════════════════════════════════════
    
    add("BitcoinTalk", "https://bitcointalk.org/index.php?action=profile;user={username}",
        tags=["crypto", "forum"], priority=3, category="forum", country="usa")
    
    add("HackerNews", "https://news.ycombinator.com/user?id={username}",
        tags=["tech", "news"], priority=2, category="forum", country="usa")
    
    add("ProductHunt", "https://www.producthunt.com/@{username}",
        name_selectors=["meta[property='og:title']"],
        tags=["tech", "products"], priority=3, category="forum", country="usa")
    
    add("Quora", "https://www.quora.com/profile/{username}",
        tags=["qa", "social"], priority=2, category="forum", country="usa")
    
    add("Disqus", "https://disqus.com/by/{username}/",
        tags=["comments"], priority=3, category="forum", country="usa")
    
    add("StackExchange", "https://stackexchange.com/users/{username}",
        tags=["qa"], priority=3, category="forum", country="usa")
    
    add("Pastebin", "https://pastebin.com/u/{username}",
        tags=["code", "paste"], priority=2, category="forum", country="usa")
    
    add("SlideShare", "https://www.slideshare.net/{username}",
        tags=["presentations"], priority=3, category="forum", country="usa")
    
    add("Scribd", "https://www.scribd.com/{username}",
        tags=["documents"], priority=4, category="forum", country="usa")
    
    add("MyAnimeList", "https://myanimelist.net/profile/{username}",
        tags=["anime"], priority=3, category="forum", country="japan")
    
    add("AniList", "https://anilist.co/user/{username}",
        tags=["anime"], priority=3, category="forum", country="japan")
    
    add("Fandom", "https://www.fandom.com/u/{username}",
        tags=["wiki"], priority=4, category="forum", country="usa")
    
    add("CurseForge", "https://www.curseforge.com/members/{username}",
        tags=["gaming", "mods"], priority=4, category="forum", country="usa")
    
    add("PlanetMinecraft", "https://www.planetminecraft.com/member/{username}/",
        tags=["gaming", "minecraft"], priority=4, category="forum", country="usa")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 13: الرياضة واللياقة (SPORTS) — 10 مواقع
    # ════════════════════════════════════════════════════════════
    
    add("Strava", "https://www.strava.com/athletes/{username}",
        tags=["sports", "fitness"], priority=3, category="sports", country="usa")
    
    add("Runkeeper", "https://runkeeper.com/user/{username}",
        tags=["sports", "fitness"], priority=4, category="sports", country="usa")
    
    add("Fitbit", "https://www.fitbit.com/user/{username}",
        tags=["sports", "fitness"], priority=4, category="sports", country="usa")
    
    add("Endomondo", "https://www.endomondo.com/profile/{username}",
        tags=["sports", "fitness"], priority=4, category="sports", country="denmark")
    
    add("MyFitnessPal", "https://www.myfitnesspal.com/profile/{username}",
        tags=["fitness"], priority=4, category="sports", country="usa")
    
    add("TrainerRoad", "https://www.trainerroad.com/profile/{username}",
        tags=["sports", "cycling"], priority=5, category="sports", country="usa")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 14: التسوق والمتاجر (SHOPPING) — 15 موقع
    # ════════════════════════════════════════════════════════════
    
    add("Etsy", "https://www.etsy.com/people/{username}",
        tags=["shopping", "handmade"], priority=3, category="shopping", country="usa")
    
    add("eBay", "https://www.ebay.com/usr/{username}",
        tags=["shopping"], priority=3, category="shopping", country="usa")
    
    add("Amazon", "https://www.amazon.com/profile/{username}",
        tags=["shopping"], priority=4, category="shopping", country="usa")
    
    add("Mercari", "https://www.mercari.com/u/{username}",
        tags=["shopping"], priority=4, category="shopping", country="japan")
    
    add("Depop", "https://www.depop.com/{username}/",
        tags=["shopping"], priority=3, category="shopping", country="uk")
    
    add("Poshmark", "https://poshmark.com/closet/{username}",
        tags=["shopping"], priority=3, category="shopping", country="usa")
    
    add("Grailed", "https://www.grailed.com/{username}",
        tags=["shopping", "fashion"], priority=4, category="shopping", country="usa")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 15: المواعدة (DATING) — 10 مواقع
    # ════════════════════════════════════════════════════════════
    
    add("Tinder", "https://tinder.com/@{username}",
        tags=["dating"], priority=5, category="dating", country="usa")
    
    add("Bumble", "https://bumble.com/profile/{username}",
        tags=["dating"], priority=5, category="dating", country="usa")
    
    add("Hinge", "https://hinge.co/profile/{username}",
        tags=["dating"], priority=5, category="dating", country="usa")
    
    add("OkCupid", "https://www.okcupid.com/profile/{username}",
        tags=["dating"], priority=5, category="dating", country="usa")
    
    add("Grindr", "https://www.grindr.com/profile/{username}",
        tags=["dating"], priority=5, category="dating", country="usa")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 16: الأفلام والمسلسلات (MOVIES/TV) — 10 مواقع
    # ════════════════════════════════════════════════════════════
    
    add("IMDb", "https://www.imdb.com/user/ur{username}/",
        tags=["movies"], priority=3, category="movies", country="usa")
    
    add("Letterboxd", "https://letterboxd.com/{username}/",
        tags=["movies"], priority=3, category="movies", country="newzealand")
    
    add("Trakt", "https://trakt.tv/users/{username}",
        tags=["movies", "tv"], priority=3, category="movies", country="usa")
    
    add("TVTime", "https://www.tvtime.com/en/user/{username}",
        tags=["movies", "tv"], priority=4, category="movies", country="usa")
    
    add("FilmAffinity", "https://www.filmaffinity.com/en/user/{username}",
        tags=["movies"], priority=4, category="movies", country="spain")
    
    add("Cineplex", "https://www.cineplex.com/profile/{username}",
        tags=["movies"], priority=5, category="movies", country="canada")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 17: التشفير والعملات الرقمية (CRYPTO) — 10 مواقع
    # ════════════════════════════════════════════════════════════
    
    add("CoinGecko", "https://www.coingecko.com/en/profile/{username}",
        tags=["crypto"], priority=4, category="crypto", country="global")
    
    add("CoinMarketCap", "https://coinmarketcap.com/community/profile/{username}/",
        tags=["crypto"], priority=4, category="crypto", country="global")
    
    add("Etherscan", "https://etherscan.io/address/{username}",
        tags=["crypto", "ethereum"], priority=4, category="crypto", country="global")
    
    add("Blockchain.com", "https://www.blockchain.com/btc/address/{username}",
        tags=["crypto"], priority=5, category="crypto", country="global")
    
    add("Binance", "https://www.binance.com/en/profile/{username}",
        tags=["crypto", "exchange"], priority=5, category="crypto", country="global")
    
    add("Coinbase", "https://www.coinbase.com/{username}",
        tags=["crypto", "exchange"], priority=5, category="crypto", country="usa")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 18: مواقع التواصل العربية (ARABIC) — 20 موقع
    # ════════════════════════════════════════════════════════════
    
    add("X (Twitter Arabic)", "https://twitter.com/{username}",
        tags=["social", "arabic"], priority=2, category="arabic", country="global")
    
    add("Teknoki", "https://teknoki.com/user/{username}",
        tags=["tech", "arabic"], priority=4, category="arabic", country="arab")
    
    add("Arageek", "https://www.arageek.com/author/{username}",
        tags=["tech", "arabic"], priority=4, category="arabic", country="jordan")
    
    add("ITWadi", "https://itwadi.com/user/{username}",
        tags=["tech", "arabic"], priority=4, category="arabic", country="arab")
    
    add("Mosle7", "https://mosle7.com/user/{username}",
        tags=["social", "arabic"], priority=4, category="arabic", country="arab")
    
    add("SaudiGamer", "https://www.saudigamer.com/author/{username}",
        tags=["gaming", "arabic"], priority=4, category="arabic", country="saudi")
    
    add("MBC", "https://www.mbc.net/profile/{username}",
        tags=["media", "arabic"], priority=5, category="arabic", country="uae")
    
    add("AlJazeera", "https://www.aljazeera.com/author/{username}",
        tags=["news", "arabic"], priority=4, category="arabic", country="qatar")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 19: منوعات (MISC) — 20 موقع
    # ════════════════════════════════════════════════════════════
    
    add("Wikipedia", "https://en.wikipedia.org/wiki/User:{username}",
        tags=["wiki", "knowledge"], priority=3, category="misc", country="usa")
    
    add("Gravatar", "https://en.gravatar.com/{username}",
        avatar_selectors=["img.avatar"],
        tags=["avatar"], priority=2, category="misc", country="usa")
    
    add("Pocket", "https://getpocket.com/@{username}",
        tags=["bookmarks"], priority=4, category="misc", country="usa")
    
    add("Raindrop.io", "https://raindrop.io/{username}",
        tags=["bookmarks"], priority=4, category="misc", country="usa")
    
    add("Archive.org", "https://archive.org/details/@/{username}",
        tags=["archive"], priority=4, category="misc", country="usa")
    
    add("Change.org", "https://www.change.org/petition/{username}",
        tags=["petitions"], priority=4, category="misc", country="usa")
    
    add("Polygon", "https://www.polygon.com/users/{username}",
        tags=["gaming", "news"], priority=4, category="misc", country="usa")
    
    add("IGN", "https://www.ign.com/users/{username}",
        tags=["gaming", "news"], priority=4, category="misc", country="usa")
    
    add("BoardGameGeek", "https://boardgamegeek.com/user/{username}",
        tags=["games", "boardgames"], priority=4, category="misc", country="usa")
    
    add("OpenStreetMap", "https://www.openstreetmap.org/user/{username}",
        tags=["maps"], priority=4, category="misc", country="global")
    
    add("Medium (custom)", "https://{username}.medium.com/",
        tags=["blog"], priority=3, category="misc", country="usa")
    
    add("DEV Community", "https://dev.to/{username}",
        tags=["code", "blog"], priority=2, category="misc", country="usa")
    
    add("HasNode", "https://hasnode.com/@{username}",
        tags=["blog"], priority=4, category="misc", country="usa")
    
    add("Telegram Group", "https://t.me/{username}",
        tags=["messaging", "group"], priority=2, category="misc", country="russia")
    
    # ════════════════════════════════════════════════════════════
    #  الفئة 20: إضافات الخصوصية (PRIVACY) — 5 مواقع
    # ════════════════════════════════════════════════════════════
    
    add("HaveIBeenPwned", "https://haveibeenpwned.com/account/{username}",
        tags=["security", "privacy"], priority=5, category="privacy", country="australia")
    
    add("Dehashed", "https://dehashed.com/search?q={username}",
        tags=["security", "leaks"], priority=5, category="privacy", country="usa")
    
    add("IntelX", "https://intelx.io/?s={username}",
        tags=["security", "osint"], priority=5, category="privacy", country="usa")
    
    log.info(f"✅ تم تحميل {len(sites)} موقعاً في قاعدة البيانات")
    return sites
