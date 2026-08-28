#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║    DeepOmnisint — Advanced Username Permutation Engine         ║
║    يولد أسماء مشابهة بذكاء: Leet + Prefix + Suffix + Transforms ║
╚══════════════════════════════════════════════════════════════════╝
"""

import logging
from typing import List, Set, Callable, Optional
from dataclasses import dataclass, field

log = logging.getLogger("omnisint.permutator")


@dataclass
class PermutationResult:
    """نتيجة توليد اسم مشابه."""
    original: str
    variants: List[str] = field(default_factory=list)
    total_generated: int = 0


class AdvancedPermutator:
    """
    مولد أسماء مشابهة متقدم — أقوى من maigret بكثير.
    يستخدم 7 تقنيات مختلفة لتوليد الأسماء.
    """
    
    # ─── قاموس Leet الكامل ───
    LEET_MAP = {
        'a': ['a', '4', '@', 'á', 'à', 'â', 'ä', 'ã', 'å', 'α', 'Δ', 'λ'],
        'b': ['b', '8', '13', '|3', 'ß', 'β', 'ɓ', '6'],
        'c': ['c', 'k', 's', 'ç', '¢', '©', 'ↄ', '<'],
        'd': ['d', '|)', 'ð', 'đ', 'ɖ', 'cl'],
        'e': ['e', '3', '€', 'é', 'è', 'ê', 'ë', 'ė', 'ę', 'Σ', '£'],
        'f': ['f', 'ph', 'ƒ', '₣', '|=', 'v'],
        'g': ['g', '9', '6', 'ğ', 'ġ', 'ğ', '&'],
        'h': ['h', '#', '|-|', 'ح', 'ħ', ']-[', '}-{'],
        'i': ['i', '1', '!', '|', 'ï', 'î', 'ì', 'í', 'ī', '¡', ']'],
        'j': ['j', '|_|', '_|', 'ʝ', '_]', ']'],
        'k': ['k', '|<', '|{', 'ķ', 'ĸ', 'κ', '](', '|('],
        'l': ['l', '1', '|_', '£', 'ł', 'ĺ', 'ļ', '7'],
        'm': ['m', '|v|', 'IVI', 'M', 'Ɱ', 'מ', '^^', 'nn'],
        'n': ['n', '|\\|', 'И', 'ñ', 'ń', 'ņ', 'π', 'ท'],
        'o': ['o', '0', '()', '[]', 'Ø', 'ō', 'ö', 'ó', 'ò', 'ô', 'õ', 'σ', 'Θ', '0_'],
        'p': ['p', '|*', '|o', '|º', 'ρ', '₱', '9'],
        'q': ['q', '0_', '()_', 'φ', 'Ω', '9'],
        'r': ['r', '|2', 'Я', '®', 'ŕ', 'ŗ', 'ř', 'γ', '12'],
        's': ['s', '5', '$', 'š', 'ş', 'ś', 'ŝ', '∫', 'z'],
        't': ['t', '7', '+', '†', 'ţ', 'ť', 'ŧ', '⊥', '"]["'],
        'u': ['u', '|_|', 'µ', 'ü', 'ú', 'ù', 'û', 'ũ', 'ū', 'υ', '(_)'],
        'v': ['v', '\\/', '|/', '√', 'ν', '▼', '^'],
        'w': ['w', '\\/\\/', 'VV', 'ω', 'Ш', 'ψ', 'uu'],
        'x': ['x', '><', '×', '}{', 'χ', '✕', ')('],
        'y': ['y', '¥', 'ỳ', 'ŷ', 'ÿ', 'ý', 'γ', '`/'],
        'z': ['z', '2', '7_', 'ž', 'ż', 'ź', 'ʒ'],
        
        # أرقام
        '0': ['0', 'o', 'O', 'Ø'],
        '1': ['1', 'l', 'I', '|', '!'],
        '2': ['2', 'z', 'Z', '7'],
        '3': ['3', 'e', 'E', '€'],
        '4': ['4', 'a', 'A', 'h'],
        '5': ['5', 's', 'S', '$'],
        '6': ['6', 'b', 'g', 'G'],
        '7': ['7', 't', 'T', 'L'],
        '8': ['8', 'b', 'B'],
        '9': ['9', 'g', 'q', 'G'],
    }
    
    # ─── البادئات الشائعة ───
    PREFIXES = [
        'the', 'real', 'mr', 'ms', 'mrs', 'dr', 'x',
        'i_am', 'iam', 'its', 'just', 'call_me',
        'hello', 'hi', 'hey', 'yo',
        '0', '00', '000', '_', '-', '.',
        'the_', 'real_', 'mr_', 'ms_',
        'its_', 'just_', 'im_', 'this_is_',
        'x_', 'xx_', 'zz_',
        'official', 'original', 'authentic',
        'alpha', 'beta', 'omega',
        'big', 'little', 'mini', 'super',
        'mega', 'ultra', 'hyper',
        'not_', 'no_', 'un_',
        'my_', 'ur_', 'your_',
        '1_', '2_', '3_',
    ]
    
    # ─── اللواحق الشائعة ───
    SUFFIXES = [
        '1', '12', '123', '1234', '12345',
        '0', '00', '000', '0000',
        '69', '420', '007',
        'x', 'xx', 'xxx',
        'us', 'me', 'io', 'tv', 'gg',
        'of', 'real', 'official',
        'yt', 'tv', 'fan', 'page',
        'blog', 'zone', 'world', 'life',
        '2020', '2021', '2022', '2023', '2024', '2025', '2026',
        '1990', '1991', '1992', '1993', '1994', '1995',
        '1996', '1997', '1998', '1999', '2000',
        '2001', '2002', '2003', '2004', '2005',
        '80', '90', '00', '10', '20',
        '_', '-', '.',
        '!', '!!', '?',
        'a', 'b', 'c', 'z',
    ]
    
    # ─── تحويلات ───
    @staticmethod
    def reverse(s: str) -> str:
        return s[::-1]
    
    @staticmethod
    def capitalize(s: str) -> str:
        return s.capitalize()
    
    @staticmethod
    def upper(s: str) -> str:
        return s.upper()
    
    @staticmethod
    def lower(s: str) -> str:
        return s.lower()
    
    @staticmethod
    def title(s: str) -> str:
        return s.title()
    
    @staticmethod
    def strip_vowels(s: str) -> str:
        return re.sub(r'[aeiouAEIOU]', '', s)
    
    @staticmethod
    def strip_consonants(s: str) -> str:
        return re.sub(r'[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]', '', s)
    
    @staticmethod
    def double_last_char(s: str) -> str:
        if s:
            return s + s[-1]
        return s
    
    @staticmethod
    def swap_case(s: str) -> str:
        return ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s))
    
    @staticmethod
    def remove_duplicates(s: str) -> str:
        result = s[0] if s else ''
        for c in s[1:]:
            if c != result[-1]:
                result += c
        return result
    
    @staticmethod
    def shuffle_words(s: str) -> str:
        words = s.split('_')
        if len(words) > 1:
            words.reverse()
            return '_'.join(words)
        return s
    
    # ─── مجموعة التحويلات ───
    TRANSFORMS = [
        ('lower', lower),
        ('upper', upper),
        ('capitalize', capitalize),
        ('title', title),
        ('reverse', reverse),
        ('swap_case', swap_case),
        ('no_vowels', strip_vowels),
        ('no_duplicates', remove_duplicates),
        ('double_last', double_last_char),
    ]
    
    @classmethod
    def generate(cls, username: str, max_variants: int = 50) -> PermutationResult:
        """
        توليد أسماء مشابهة بكل التقنيات.
        
        Args:
            username: اسم المستخدم الأصلي
            max_variants: الحد الأقصى للتوليدات
            
        Returns:
            PermutationResult يحتوي على جميع الأسماء المشابهة
        """
        variants: Set[str] = set()
        base = username.strip()
        
        if not base:
            return PermutationResult(original=username)
        
        base_lower = base.lower()
        
        # ─── 1. التحويلات الأساسية ───
        for name, transform in cls.TRANSFORMS:
            try:
                v = transform(base_lower)
                if v and len(v) >= 2:
                    variants.add(v)
            except:
                continue
        
        # ─── 2. إضافة البادئات ───
        for prefix in cls.PREFIXES[:10]:  # حد 10 بادئات
            for sep in ['', '_', '-', '.']:
                v = f"{prefix}{sep}{base_lower}"
                if len(v) <= 50:
                    variants.add(v)
                    # عكس الترتيب
                    v2 = f"{base_lower}{sep}{prefix}"
                    if len(v2) <= 50:
                        variants.add(v2)
        
        # ─── 3. إضافة اللواحق ───
        for suffix in cls.SUFFIXES[:15]:  # حد 15 لاحقة
            for sep in ['', '_', '-', '.']:
                v = f"{base_lower}{sep}{suffix}"
                if len(v) <= 50:
                    variants.add(v)
        
        # ─── 4. Leet speak ───
        leet_variants = set()
        for i, ch in enumerate(base_lower):
            if ch in cls.LEET_MAP:
                for sub in cls.LEET_MAP[ch][:2]:  # حد بديلين لكل حرف
                    if sub != ch:
                        v = base_lower[:i] + sub + base_lower[i+1:]
                        if len(v) >= 2 and len(leet_variants) < max_variants // 2:
                            leet_variants.add(v)
                            # تطبيق تحويل آخر على leet
                            for _, transform in cls.TRANSFORMS[:3]:
                                try:
                                    v2 = transform(v)
                                    if v2 and len(v2) >= 2:
                                        leet_variants.add(v2)
                                except:
                                    continue
        
        variants.update(leet_variants)
        
        # ─── 5. تكرار الحروف ───
        variants.add(base_lower * 2)
        variants.add(base_lower[0] * 3 + base_lower)
        variants.add(base_lower + base_lower[-1] * 3)
        
        # ─── 6. إضافة أرقام عشوائية ───
        import random
        for _ in range(5):
            rnd = str(random.randint(10, 999))
            variants.add(f"{base_lower}{rnd}")
            variants.add(f"{rnd}{base_lower}")
        
        # ─── 7. حذف وتعديل ───
        if len(base_lower) > 3:
            variants.add(base_lower[1:])      # احذف أول حرف
            variants.add(base_lower[:-1])     # احذف آخر حرف
            variants.add(base_lower[0] + base_lower[2:])  # احذف الحرف الثاني
        
        # ─── تنظيف وترتيب ───
        variants.discard(base_lower)  # احذف الأصلي
        variants.discard('')
        
        # ترتيب حسب الطول (الأقصر أولاً) ثم أبجدياً
        sorted_variants = sorted(variants, key=lambda x: (len(x), x))
        
        # حد أقصى
        result = sorted_variants[:max_variants]
        
        log.debug(f"تم توليد {len(result)} اسماً مشابهاً من {len(variants)} متغيراً")
        
        return PermutationResult(
            original=username,
            variants=result,
            total_generated=len(variants),
        )
