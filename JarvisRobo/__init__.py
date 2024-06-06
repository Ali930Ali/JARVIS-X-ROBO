import logging
import os
import sys
import time
import telegram.ext as tg
from aiohttp import ClientSession
from pyrogram import Client
from telethon import TelegramClient

BaşlangıçZamanı = time.time()

# günlüğü etkinleştir
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

# eğer versiyon < 3.6 ise, botu durdur.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "En az 3.6 python sürümüne sahip OLMALISINIZ! Birçok özellik buna bağlıdır. Bot çıkıyor."
    )
    quit(1)

ENV = bool(os.environ.get("ÇEVRE", False))

if ENV:

    API_ID = int(os.environ.get("API_KİMLİK", None))
    API_HASH = os.environ.get("API_HASH", None)
    
    ALLOW_CHATS = os.environ.get("CHATS_İZİN", True)
    ALLOW_EXCL = os.environ.get("EXCL_İZİN", False)
    CASH_API_KEY = os.environ.get("PARA_API_ANAHTAR", None)
    DB_URI = os.environ.get("VERİTABANI_URL")
    DEL_CMDS = bool(os.environ.get("KOMUTLARI_SİL", False))
    EVENT_LOGS = os.environ.get("OLAY_GÜNLÜKLERİ", None)
    INFOPIC = bool(os.environ.get("BİLGİ_RESMİ", "True"))
    LOAD = os.environ.get("YÜKLE", "").split()
    MONGO_DB_URI = os.environ.get("MONGO_DB_URL", None)
    NO_LOAD = os.environ.get("YÜKLEME", "").split()
    START_IMG = os.environ.get("BAŞLANGIÇ_RESMİ", "")
    HELP_IMG = os.environ.get("YARDIM_RESMİ", "https://telegra.ph/file/61296490da95c55a1d5ee.jpg")
    STRICT_GBAN = bool(os.environ.get("KATI_YASAK", True))
    SUPPORT_CHAT = os.environ.get("DESTEK_SOHBETİ", "Dora_Hub")
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("GEÇİCİ İNDİRME_DİZİNİ", "./")
    TOKEN = os.environ.get("ANAHTAR", None)
    TIME_API_KEY = os.environ.get("ZAMAN_API_ANAHTAR", None)
    WORKERS = int(os.environ.get("ÇALIŞANLAR", 8))

    try:
        OWNER_ID = int(os.environ.get("SAHİP_KİMLİĞİ", None))
    except ValueError:
        raise Exception("SAHİP_KİMLİĞİ env değişkeniniz geçerli bir tamsayı değil.")

    try:
        BL_CHATS = set(int(x) for x in os.environ.get("KARA_LİSTE_SOHBETLER", "").split())
    except ValueError:
        raise Exception("Siyah listeli sohbetler listeniz geçerli tamsayılar içermiyor.")

    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEVS", "7157587567").split())
    except ValueError:
        raise Exception("Sudo veya geliştirici kullanıcılar listeniz geçerli tamsayılar içermiyor.")

    try:
        DEMONS = set(int(x) for x in os.environ.get("DEMONS", "").split())
    except ValueError:
        raise Exception("Destek kullanıcılar listeniz geçerli tamsayılar içermiyor.")

    try:
        TIGERS = set(int(x) for x in os.environ.get("TIGERS", "").split())
    except ValueError:
        raise Exception("Tiger kullanıcılar listeniz geçerli tamsayılar içermiyor.")

    try:
        WOLVES = set(int(x) for x in os.environ.get("WOLVES", "").split())
    except ValueError:
        raise Exception("Beyaz listeli kullanıcılar listeniz geçerli tamsayılar içermiyor.")

else:
    from JarvisRobo.config import Development as Config

    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    ALLOW_CHATS = Config.ALLOW_CHATS
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    DB_URI = Config.DATABASE_URL
    DEL_CMDS = Config.DEL_CMDS
    EVENT_LOGS = Config.EVENT_LOGS
    INFOPIC = Config.INFOPIC
    LOAD = Config.LOAD
    MONGO_DB_URI = Config.MONGO_DB_URI
    NO_LOAD = Config.NO_LOAD
    START_IMG = Config.START_IMG
    HELP_IMG = Config.HELP_IMG
    STRICT_GBAN = Config.STRICT_GBAN
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    TOKEN = Config.TOKEN
    TIME_API_KEY = Config.TIME_API_KEY
    WORKERS = Config.WORKERS

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("SAHİP_KİMLİĞİ değişkeniniz geçerli bir tamsayı değil.")

    try:
        BL_CHATS = set(int(x) for x in Config.BL_CHATS or [])
    except ValueError:
        raise Exception("Siyah listeli sohbetler listeniz geçerli tamsayılar içermiyor.")

    try:
        DRAGONS = set(int(x) for x in Config.DRAGONS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception("Sudo veya geliştirici kullanıcılar listeniz geçerli tamsayılar içermiyor.")

    try:
        DEMONS = set(int(x) for x in Config.DEMONS or [])
    except ValueError:
        raise Exception("Destek kullanıcılar listeniz geçerli tamsayılar içermiyor.")

    try:
        TIGERS = set(int(x) for x in Config.TIGERS or [])
    except ValueError:
        raise Exception("Tiger kullanıcılar listeniz geçerli tamsayılar içermiyor.")

    try:
        WOLVES = set(int(x) for x in Config.WOLVES or [])
    except ValueError:
        raise Exception("Beyaz listeli kullanıcılar listeniz geçerli tamsayılar içermiyor.")


DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)

updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient("jarvis", API_ID, API_HASH)

pbot = Client("JarvisRobo", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN,in_memory=True)
dispatcher = updater.dispatcher
aiohttpsession = ClientSession()

print("[BİLGİ]: Bot Bilgileri Alınıyor...")
BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username

DRAGONS = list(DRAGONS) + list(DEV_USERS) 
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Tüm önceki değişkenlerin ayarlanmasını sağlamak için sona yükle
from JarvisRobo.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# ekstra kwargs'ları alan regex handler'ı almak için emin olun
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
    
