#!/bin/bash
# DeepOmnisint — Automated Installer for Kali Linux
# ─────────────────────────────────────────────────

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════╗"
echo "║       DeepOmnisint v3.0 — Kali Installer        ║"
echo "╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

# تحقق من صلاحيات root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ يجب تشغيل السكربت بصلاحيات root: sudo bash install.sh${NC}"
   exit 1
fi

echo -e "${YELLOW}[1/6] تحديث الحزم...${NC}"
apt update -y && apt upgrade -y

echo -e "${YELLOW}[2/6] تثبيت Python 3.11 والحزم الأساسية...${NC}"
apt install -y python3 python3-pip python3-venv git curl wget \
    build-essential libssl-dev libffi-dev python3-dev \
    libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev

echo -e "${YELLOW}[3/6] تثبيت أدوات إضافية...${NC}"
apt install -y tor proxychains4 jq nmap whois dnsutils

echo -e "${YELLOW}[4/6] إنشاء البيئة الافتراضية...${NC}"
python3 -m venv venv
source venv/bin/activate

echo -e "${YELLOW}[5/6] تثبيت تبعيات Python...${NC}"
pip install --upgrade pip setuptools wheel

# تثبيت التبعيات الأساسية
pip install aiohttp aiofiles aiosqlite \
    beautifulsoup4 lxml html5lib \
    jinja2 weasyprint \
    fake-useragent aiodns cchardet \
    python-telegram-bot \
    pillow requests \
    colorama tqdm rich \
    pydantic typing-extensions \
    matplotlib networkx \
    cryptography pycryptodome

# تثبيت اختياري للتصوير
pip install playwright
playwright install chromium 2>/dev/null || echo -e "${YELLOW}⚠️ Playwright يحتاج لتشغيل يدوي: playwright install chromium${NC}"

echo -e "${YELLOW}[6/6] إعداد متغيرات البيئة...${NC}"
cat >> ~/.bashrc << 'EOF'

# DeepOmnisint
export DEEPOMNISINT_HOME="$HOME/deepomnisint"
export PATH="$DEEPOMNISINT_HOME:$PATH"
EOF

source ~/.bashrc

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════╗"
echo "║       ✅ DeepOmnisint جاهز للاستخدام!           ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║  تشغيل:                                         ║"
echo "║  source venv/bin/activate                        ║"
echo "║  python deepomnisint.py johndoe --deep --html    ║"
echo "╚══════════════════════════════════════════════════╝"
echo -e "${NC}"
