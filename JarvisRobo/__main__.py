# <============================================== IMPORTS =========================================================>
import importlib
import re
import time
import asyncio
from platform import python_version as y
from sys import argv
from pyrogram import __version__ as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

import JarvisRobo.modules.no_sql.users_db as sql
from JarvisRobo import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    START_IMG,
    HELP_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)
from JarvisRobo.modules import ALL_MODULES
from JarvisRobo.modules.helper_funcs.chat_status import is_user_admin
from JarvisRobo.modules.helper_funcs.misc import paginate_modules

# <=======================================================================================================>

# <============================================== FUNCTIONS =========================================================>

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

# <============================================== STRINGS =========================================================>

PM_START_TEX = """
merhaba `{}`, nasılsın \n biraz beklermisin kardeşim. . . 
"""


PM_START_TEXT = """ 
*ʜᴇʏ* {}  

* > ben * {} !
telegramın en kaliteli grup Yönetim botuyum☺️.
─────────────────
   * kullanıcı »* {}
   * gruplar »* {}
─────────────────
* yardım komutları ve destek için aşağıdaki butonları tıklaya bilirsiniz.*
"""

buttons = [
   [
        InlineKeyboardButton(
            text="♻️beni grubuna ekle♻️",
            url=f"https://t.me/{dispatcher.bot.username}?startgroup=true",
        ),
    ],
   [
        InlineKeyboardButton(text=🍃 "komutlar 🍃", callback_data="help_back"),
    ],
    [
        InlineKeyboardButton(text=" 🍃detaylar🍃 ", callback_data="Jarvis_"),
        InlineKeyboardButton(text="✨ destej ✨", url=f"https://t.me/JARVIS_V_SUPPORT"),
    ],
   [
        InlineKeyboardButton(text="🥀 geliştirici 🥀", url=f"tg://user?id={OWNER_ID}"),
        InlineKeyboardButton(text="☁️ kaynak kod ☁️", callback_data="source_"),
    ],
]

HELP_STRINGS = f"""
» {BOT_NAME}  Belirli komut hakkında açıklama almak için aşağıdaki düğmeye tıklayın"""


# <============================================================= NO USE BEGIN ========================================================================>
DONATE_STRING = f"""merhaba bebeğim,
  Bağış yapmak istediğini duyduğuma sevindim.

deceloper'ımla doğrudan iletişime geçebilirsiniz @Mehmettbeydiyeceksinizz\_V2 bağış yapmak için veya destek sohbetimi ziyaret edebilirsiniz @Armageddonsohbet\_2024 ve bağış konusunda aşk var."""
# <============================================================= NO USE END ========================================================================>
# <============================================== STRINGS END =========================================================>

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("JarvisRobo.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module



# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_photo(
        chat_id=chat_id,
        photo=START_IMG,
        caption=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard,
    )
# <============================================== BAŞLADI =========================================================>

def start(update: Update, context: CallbackContext):
    args = context.args
    global uptime
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="🍃 geri 🍃", callback_data="help_back")]]
                    ),
                )
            elif args[0].lower() == "markdownhelp":
                IMPORTED["exᴛʀᴀs"].markdown_help_sender(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rᴜʟᴇs" in IMPORTED:
                IMPORTED["rᴜʟᴇs"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_sticker(
                "CAACAgEAAx0Cfbdm0QACATNmC-1-nl8Unb8cLRS-8qfLllewvwACPwMAAtKbsEQsyzfIkYLVGx4E"
            )
            usr = update.effective_user
            lol = update.effective_message.reply_text(
                PM_START_TEX.format(usr.first_name), parse_mode=ParseMode.MARKDOWN
            )
            time.sleep(1.25)
            lol.edit_text("⚰️")
            time.sleep(1.0)
            lol.edit_text("bot başlatılıyor... ")
            time.sleep(0.5)
            lol.delete()
            
            update.effective_message.reply_photo(START_IMG, PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME, sql.num_users(), sql.num_chats()),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            START_IMG,
            caption="hayattayım bebeğim !\n<b>o zamandan beri uyumadım🥺​:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )

# <============================================== START END =========================================================>

def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors

# <============================================== HELP =========================================================>

def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "» *için mevcut komutlar​​* *{}* :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_caption(text,
                parse_mode=ParseMode.MARKDOWN,
                
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text="🍃geri🍃", callback_data="help_back")]
                    ]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass
# <============================================== HELP CLOSE =========================================================>

# <============================================== ABOUT CALLBACK =========================================================>

def Jarvis_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Jarvis_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_caption(
            f"merhaba,*🥀\n  *ben {dispatcher.bot.first_name}"
            "\nGrubunuzu kolayca yönetmenize ve grubunuzu dolandırıcılardan ve spam gönderenlerden korumanıza yardımcı olmak için oluşturulmuş güçlü bir grup yönetimi."
            "\nveritabanı olarak sqlalchemy ve mongodb ile python ile yazılmıştır."
            "\n\n────────────────────"
            f"\n*versiyon 1 »* {uptime}"
            f"\n*versiyon 2 »* {sql.num_users()}"
            f"\n*versiyon 3 »* {sql.num_chats()}"
            "\n────────────────────"
            "\n\n➲  kullanıcıları kısıtlayabilirim."
            "\n➲  Gelişmiş bir su baskını önleme sistemine sahip olun."
            "\n➲  Kullanıcıları özelleştirilebilir karşılama mesajlarıyla karşılayabilir ve hatta grup kuralları belirleyebilirim3z."
            "\n➲  Yasaklama, sessize alma vb. gibi önceden tanımlanmış her eylemle kullanıcıları Maksimum Wnrs'ye ulaşana kadar uyarabilirim.."
            "\n➲  Sistemin kara listelerini tutan bir notum ve hatta belirli anahtar kelimelerle ilgili önceden belirlenmiş yanıtlarım var."
            f"\n\n➻ hakkında temel yardım ve bilgi almak için aşağıda verilen düğmelere tıklayın. {dispatcher.bot.first_name}.",
            parse_mode=ParseMode.MARKDOWN,
            
             reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🍃destek🍃", callback_data="Jarvis_support"),
                        InlineKeyboardButton(text="🍃geliştirici🍃", url=f"tg://user?id={OWNER_ID}"),
                    ],
                    [
                        
                        InlineKeyboardButton(text="🍃komutlar🍃", callback_data="help_back"),
                    ],
                    [
                        InlineKeyboardButton(text="🍃geri🍃", callback_data="Jarvis_back"),
                    ],
                ]
            ),
        )
    elif query.data == "Armageddonsohbet":
        query.message.edit_caption("🍃 Yardım ve daha fazla bilgi almak için aşağıda verilen düğmelere tıklayın."
            f"\n\nɪғ ʏᴏᴜ ғᴏᴜɴᴅ ᴀɴʏ ʙᴜɢ ɪɴ {dispatcher.bot.first_name} veya konuyla ilgili geri bildirimde bulunmak istiyorsanız {dispatcher.bot.first_name}, ᴩʟᴇᴀsᴇ ʀᴇᴩᴏʀᴛ ɪᴛ ᴀᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🍃destek🍃", url=f"https://t.me/{SUPPORT_CHAT}"
                        ),
                        InlineKeyboardButton(
                            text="🍃güncelleme 🍃", url=f"https://t.me/JARVIS_V_SUPPORT"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="🍃geliştirici 🍃", url=f"tg://user?id={OWNER_ID}"
                        ),
                        InlineKeyboardButton(
                            text="🍃github🍃", url="https://github.com/doraemon890",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="🍃 geri 🍃", callback_data="Jarvis_"),
                    ],
                ]
            ),
        )
    elif query.data == "Jarvis_back":
        first_name = update.effective_user.first_name 
        query.message.edit_caption(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME,sql.num_users(),sql.num_chats()),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
        )
        
# <============================================== ABOUT CALLBACK END =========================================================>

# <============================================================= NO USE BEGIN ========================================================================>

def JarvisRobo_Main_Callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Main_help":
        query.message.edit_caption(f"""
 ʜᴇʀᴇ ɪꜱ ʜᴇʟᴘ ᴍᴇɴᴜ ꜰᴏʀ {BOT_NAME}
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="♻️ yönetim ", callback_data="help_back"),
                        InlineKeyboardButton(text="müzik 🎧", callback_data="Music_")
                    ],
                    [
                        InlineKeyboardButton(text="💁 basic ", callback_data="basic_help"),
                        InlineKeyboardButton(text="Exᴘᴇʀᴛ 👮", callback_data="expert_help")
                    ],
                    [
                        InlineKeyboardButton(text="🍹 parti", callback_data="advance_help"),
                        InlineKeyboardButton(text="Dᴏɴᴀᴛɪᴏɴ 🎉", callback_data="donation_help") 
                    ],
                    [InlineKeyboardButton(text="• ana menü •", callback_data="Jarvis_back")]
                ]
            ),
        )
    elif query.data=="basic_help":
        query.message.edit_caption("""basic komutla.
👮🏻 yönetici adminler & monitörler.
🕵🏻adminleri kontrol etme.

👮🏻 /reload botları yeniden başlatır .
🕵🏻 /settings bot grup ayarlarını gosterir.
👮🏻 /ban kullanıcıları yasaklar grubu korur.
👮🏻 /mute kullanıcıları sessize alır .
👮🏻 /kick kullanıcıları gruptan tekmeler.
👮🏻 /unban kullanıcıların yasağını kaldırır.
👮🏻 /info kullanıcıların bilgilerini gösterir .

◽️ /staff grup personelinin tam listesini verir!.""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🍃 geri 🍃", callback_data="Main_help"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="jarvis_support")
                    ]
                ]
            ),
            )
    elif query.data=="Jarvis_back":
        query.message.edit_caption("""uzman komutları

👥 Tüm kullanıcılar tarafından kullanılabilir
👮🏻 yönetici moderatörlerinin kullanımına açıktır.
🕵🏻 yöneticilerin kullanımına açıktır

🕵🏻  /unbanall ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘs
👮🏻  /unmuteall ᴜɴᴍᴜᴛᴇᴀʟʟ ᴀʟʟ ғʀᴏᴍ Yᴏᴜʀ Gʀᴏᴜᴘ

Pɪɴɴᴇᴅ Mᴇssᴀɢᴇs
🕵🏻  /pin [ᴍᴇssᴀɢᴇ] sᴇɴᴅs ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛʜʀᴏᴜɢʜ ᴛʜᴇ Bᴏᴛ ᴀɴᴅ ᴘɪɴs ɪᴛ.
🕵🏻  /pin ᴘɪɴs ᴛʜᴇ ᴍᴇssᴀɢᴇ ɪɴ ʀᴇᴘʟʏ
🕵🏻  /unpin ʀᴇᴍᴏᴠᴇs ᴛʜᴇ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ.
🕵🏻  /adminlist ʟɪsᴛ ᴏғ ᴀʟʟ ᴛʜᴇ sᴘᴇᴄɪᴀʟ ʀᴏʟᴇs ᴀssɪɢɴᴇᴅ ᴛᴏ ᴜsᴇʀs.

◽️ /bug: (ᴍᴇssᴀɢᴇ) ᴛᴏ Sᴇɴᴅ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴇʀʀᴏʀs ᴡʜɪᴄʜ ʏᴏᴜ ᴀʀᴇ ғᴀᴄɪɴɢ 
ᴇx: /bug Hᴇʏ Tʜᴇʀᴇ Is ᴀ Sᴏᴍᴇᴛʜɪɴɢ Eʀʀᴏʀ @username ᴏғ ᴄʜᴀᴛ! .""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="Main_help"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="jarvis_support")
                    ]
                ]
            ),
            )                                        
    elif query.data=="advance_help":
        query.message.edit_caption("""Aᴅᴠᴀɴᴄᴇᴅ Cᴏᴍᴍᴀɴᴅs

👮🏻Aᴠᴀɪʟᴀʙʟᴇ ᴛᴏ Aᴅᴍɪɴs & Mᴏᴅᴇʀᴀᴛᴏʀs.
🕵🏻Aᴠᴀɪʟᴀʙʟᴇ ᴛᴏ Aᴅᴍɪɴs.
🛃 Aᴠᴀɪʟᴀʙʟᴇ ᴛᴏ Aᴅᴍɪɴs & Cʟᴇᴀɴᴇʀs

Wᴀʀɴ Mᴀɴᴀɢᴇᴍᴇɴᴛ
👮🏻  /warn ᴀᴅᴅs ᴀ ᴡᴀʀɴ ᴛᴏ ᴛʜᴇ ᴜsᴇʀ
👮🏻  /unwarn ʀᴇᴍᴏᴠᴇs ᴀ ᴡᴀʀɴ ᴛᴏ ᴛʜᴇ ᴜsᴇʀ
👮🏻  /warns ʟᴇᴛs ʏᴏᴜ sᴇᴇ ᴀɴᴅ ᴍᴀɴᴀɢᴇ ᴜsᴇʀ ᴡᴀʀɴs

🛃  /del ᴅᴇʟᴇᴛᴇs ᴛʜᴇ sᴇʟᴇᴄᴛᴇᴅ ᴍᴇssᴀɢᴇ
🛃  /purge ᴅᴇʟᴇᴛᴇs ғʀᴏᴍ ᴛʜᴇ sᴇʟᴇᴄᴛᴇᴅ ᴍᴇssᴀɢᴇ.""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="Main_help"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="jarvis_support")
                    ]
                ]
            ),
            )
    elif query.data=="expert_help":
        query.message.edit_caption(f"""━━━━━━━━━━━━━━━━━━━━
ᴍᴀᴋᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴇꜰꜰᴇᴄᴛɪᴠᴇ ɴᴏᴡ :
🎉 ᴄᴏɴɢʀᴀɢᴜʟᴀᴛɪᴏɴꜱ 🎉
[{BOT_NAME}]("https://t.me/{BOT_USERNAME}") ɴᴏᴡ ʀᴇᴀᴅʏ ᴛᴏ
ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ.

ᴀᴅᴍɪɴ ᴛᴏᴏʟꜱ :
ʙᴀꜱɪᴄ ᴀᴅᴍɪɴ ᴛᴏᴏʟꜱ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ
ᴘʀᴏᴛᴇᴄᴛ & ᴘᴏᴡᴇʀᴜᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ.
ʏᴏᴜ ᴄᴀɴ ʙᴀɴ, ᴋɪᴄᴋ, ᴘʀᴏᴍᴏᴛᴇ
ᴍᴇᴍʙᴇʀꜱ ᴀꜱ ᴀᴅᴍɪɴ ᴛʜʀᴏᴜɢʜ ʙᴏᴛ.

ɢʀᴇᴇᴛɪɴɢꜱ :
ʟᴇᴛꜱ ꜱᴇᴛ ᴀ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ
ᴡᴇʟᴄᴏᴍᴇ ɴᴇᴡ ᴜꜱᴇʀꜱ ᴄᴏᴍɪɴɢ ᴛᴏ
ʏᴏᴜʀ ɢʀᴏᴜᴘ.
ꜱᴇɴᴅ /setwelcome ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ
ꜱᴇᴛ ᴀ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇ!""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="Main_help"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="jarvis_support")
                    ]
                ]
            ),
            )
    elif query.data=="donation_help":
        query.message.edit_caption("""Aʀᴇ ʏᴏᴜ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ ʜᴇʟᴘɪɴɢ ᴍʏ ᴄʀᴇᴀᴛᴏʀ ᴡɪᴛʜ ʜɪs ᴇғғᴏʀᴛs ᴛᴏ ᴋᴇᴇᴘ ᴍᴇ ɪɴ ᴀᴄᴛɪᴠᴇ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ? Iғ ʏᴇs, Yᴏᴜ'ʀᴇ ɪɴ ᴛʜᴇ ʀɪɢʜᴛ ᴘʟᴀᴄᴇ. 

Wᴇ ᴇᴍᴘʜᴀsɪsᴇ ᴛʜᴇ ɪᴍᴘᴏʀᴛᴀɴᴄᴇ ᴏғ ɴᴇᴇᴅɪɴɢ ғᴜɴᴅs ᴛᴏ ᴋᴇᴇᴘ MᴜᴋᴇsʜRᴏʙᴏᴛ ᴜɴᴅᴇʀ ᴀᴄᴛɪᴠᴇ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ. Yᴏᴜʀ ᴅᴏɴᴀᴛɪᴏɴs ɪɴ ᴀɴʏ ᴀᴍᴏᴜɴᴛ ᴏғ ᴍᴏɴᴇʏ ᴛᴏ MᴜᴋᴇsʜRᴏʙᴏᴛ sᴇʀᴠᴇʀs ᴀɴᴅ ᴏᴛʜᴇʀ ᴜᴛɪʟɪᴛɪᴇs ᴡɪʟʟ ᴀʟʟᴏᴡ ᴜs ᴛᴏ sᴜsᴛᴀɪɴ ᴛʜᴇ ʟɪғᴇsᴘᴀɴ ɪɴ ᴛʜᴇ ʟᴏɴɢ ᴛᴇʀᴍ. Wᴇ ᴡɪʟʟ ᴜsᴇ ᴀʟʟ ᴏғ ᴛʜᴇ ᴅᴏɴᴀᴛɪᴏɴs ᴛᴏ ᴄᴏᴠᴇʀ ғᴜᴛᴜʀᴇ ᴇxᴘᴇɴsᴇs ᴀɴᴅ ᴜᴘɢʀᴀᴅᴇs ᴏғ ᴛʜᴇ sᴇʀᴠᴇʀs ᴄᴏsᴛs. Iғ ʏᴏᴜ'ᴠᴇ ɢᴏᴛ sᴘᴀʀᴇ ᴍᴏɴᴇʏ ᴛᴏ ʜᴇʟᴘ ᴜs ɪɴ ᴛʜɪs ᴇғғᴏʀᴛ, Kɪɴᴅʟʏ ᴅᴏ sᴏ ᴀɴᴅ ʏᴏᴜʀ ᴅᴏɴᴀᴛɪᴏɴs ᴄᴀɴ ᴀʟsᴏ ᴍᴏᴛɪᴠᴀᴛᴇ ᴜs ᴋᴇᴇᴘ ʙʀɪɴɢ ᴏɴ ɴᴇᴡ ғᴇᴀᴛᴜʀᴇs.

Yᴏᴜ ᴄᴀɴ ʜᴇʟᴘ ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ ᴡɪᴛʜ ᴅᴏɴᴀᴛɪᴏɴs""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [ [
        InlineKeyboardButton(text="🏡", callback_data="Jarvis_back"),
        InlineKeyboardButton(text="🛡️", callback_data="jarvis_"),
        InlineKeyboardButton(text="💳", callback_data="source_"),
        InlineKeyboardButton(text="🧑‍💻", url=f"tg://user?id={OWNER_ID}"),
        InlineKeyboardButton(text="🖥️", callback_data="Main_help"),
     ],
                    [
                        InlineKeyboardButton(text="• Dᴏɴᴀᴛᴇ •", url="https://t.me/mukeshbotzone/7"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="jarvis_support")
                    ]
                ]
            ),
            )  
        
# <============================================================= NO USE END ========================================================================>

# <============================================== SOURCE CALLBACK =========================================================>

def Source_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_caption(
            f"""
ʜᴇʏ,
 ᴛʜɪs ɪs {BOT_NAME},
ᴀɴ ᴏᴩᴇɴ sᴏᴜʀᴄᴇ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴩ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ.

ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ ᴛʜᴇ ʜᴇʟᴩ ᴏғ : [ᴛᴇʟᴇᴛʜᴏɴ](https://github.com/LonamiWebs/Telethon)
[ᴩʏʀᴏɢʀᴀᴍ](https://github.com/pyrogram/pyrogram)
[ᴩʏᴛʜᴏɴ-ᴛᴇʟᴇɢʀᴀᴍ-ʙᴏᴛ](https://github.com/python-telegram-bot/python-telegram-bot)
ᴀɴᴅ ᴜsɪɴɢ [sǫʟᴀʟᴄʜᴇᴍʏ](https://www.sqlalchemy.org) ᴀɴᴅ [ᴍᴏɴɢᴏ](https://cloud.mongodb.com) ᴀs ᴅᴀᴛᴀʙᴀsᴇ.


ʜᴇʀᴇ ɪs ᴍʏ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ : [ɢɪᴛʜᴜʙ](https://github.com/doraemon890)


{BOT_NAME} ɪs ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ [ᴍɪᴛ ʟɪᴄᴇɴsᴇ](https://github.com/doraemon890/JARVIS-ROBO/blob/master/LICENSE).
© 2024 - 2025 | [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ](https://t.me/{SUPPORT_CHAT}), ᴀʟʟ ʀɪɢʜᴛs ʀᴇsᴇʀᴠᴇᴅ.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
             [
                 InlineKeyboardButton(text="sᴏᴜʀᴄᴇ", url="https://github.com/doraemon890/JARVIS-ROBO")
             ],
                 [InlineKeyboardButton(text="๏ ʙᴀᴄᴋ ๏", callback_data="source_back")]
                ]
            ),
        )
    elif query.data == "source_back":
        first_name = update.effective_user.first_name
        query.message.edit_caption(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME,sql.num_users(),sql.num_chats()),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            
        )
# <============================================== SOURCE CALLBACK END =========================================================>

# <============================================================= NO USE BEGIN ========================================================================>
        
def Music_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Music_":
        query.message.edit_caption(f"""
 ʜᴇʀᴇ ɪꜱ ʜᴇʟᴘ ᴍᴇɴᴜ ꜰᴏʀ ᴍᴜꜱɪᴄ 
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
        InlineKeyboardButton(text="🎧", callback_data="Jarvis_back"),
        InlineKeyboardButton(text="🎛️", callback_data="jarvis_"),
        InlineKeyboardButton(text="🍷", callback_data="source_"),
        InlineKeyboardButton(text="⚰️", url=f"tg://user?id={OWNER_ID}"),
        InlineKeyboardButton(text="🖥️", callback_data="Main_help"),
     ],
                    [
                        InlineKeyboardButton(
                            text="🍃yönetici🍃", callback_data="Music_admin"
                        ),
                        InlineKeyboardButton(
                            text="🍃oynat🍃", callback_data="Music_play"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="🍃bot🍃", callback_data="Music_bot"),
                        InlineKeyboardButton(
                            text=" 🍃ᴇxᴛʀᴀ🍃 ",
                            callback_data="Music_extra",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="🍃 geri 🍃", callback_data="Main_help")
                    ],
                ]
            ),
        )
    elif query.data == "Music_admin":
        query.message.edit_caption(f"*» yönetici komutları «*"
            f"""
kanal için kullanmak üzere komutların başına *c* eklemeniz yeterlidir.

/pause : ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.

/resume : ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ.

/skip : sᴋɪᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ.

/end ᴏʀ /stop : ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ᴇɴᴅ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.

/player : ɢᴇᴛ ᴀ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴩʟᴀʏᴇʀ ᴩᴀɴᴇʟ.

/queue : sʜᴏᴡs ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ʟɪsᴛ.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" ʙᴀᴄᴋ ", callback_data="Music_"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="jarvis_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_play":
        query.message.edit_caption(f"*» ᴘʟᴀʏ ᴄᴏᴍᴍᴀɴᴅꜱ «*"
            f"""
/play or /vplay or /cplay  - ʙᴏᴛ ᴡɪʟʟ ꜱᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ ʏᴏᴜʀ ɢɪᴠᴇɴ ϙᴜᴇʀʏ on ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴏʀ ꜱᴛʀᴇᴀᴍ ʟɪᴠᴇ ʟɪɴᴋꜱ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛꜱ.

/playforce or /vplayforce or /cplayforce -  ғᴏʀᴄᴇ ᴘʟᴀʏ ꜱᴛᴏᴘꜱ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏɪɴɢ ᴛʀᴀᴄᴋ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀɴᴅ ꜱᴛᴀʀᴛꜱ ᴘʟᴀʏɪɴɢ ᴛʜᴇ ꜱᴇᴀʀᴄʜᴇᴅ ᴛʀᴀᴄᴋ ɪɴꜱᴛᴀɴᴛʟʏ ᴡɪᴛʜᴏᴜᴛ ᴅɪꜱᴛᴜʀʙɪɴɢ/clearing queue.

/channelplay [ᴄʜᴀᴛ ᴜꜱᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ] ᴏʀ [ᴅɪꜱᴀʙʟᴇ] - ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ꜱᴛʀᴇᴀᴍ ᴍᴜꜱɪᴄ ᴏɴ ᴄʜᴀɴɴᴇʟ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ғʀᴏᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘ.


*ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ*
 ʙᴏᴛ  ꜱᴇʀᴠᴇʀ ᴘʟᴀʏʟɪꜱᴛꜱ:
/playlist  - ᴄʜᴇᴄᴋ ʏᴏᴜʀ ꜱᴀᴠᴇᴅ ᴘʟᴀʏʟɪꜱᴛ ᴏɴ ꜱᴇʀᴠᴇʀꜱ.
/deleteplaylist - ᴅᴇʟᴇᴛᴇ ᴀɴʏ ꜱᴀᴠᴇᴅ ᴍᴜꜱɪᴄ ɪɴ ʏᴏᴜʀ ᴘʟᴀʏʟɪꜱᴛ
/play  - ꜱᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ ʏᴏᴜʀ ꜱᴀᴠᴇᴅ ᴘʟᴀʏʟɪꜱᴛ ғʀᴏᴍ ꜱᴇʀᴠᴇʀꜱ.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="Music_"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="jarvis_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_bot":
        query.message.edit_caption(f"*» ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ «*"
            f"""
/stats - ɢᴇᴛ ᴛᴏᴘ 10 ᴛʀᴀᴄᴋꜱ ɢʟᴏʙᴀʟ ꜱᴛᴀᴛꜱ, ᴛᴏᴘ 10 ᴜꜱᴇʀꜱ ᴏғ ʙᴏᴛ, ᴛᴏᴘ 10 ᴄʜᴀᴛꜱ ᴏɴ ʙᴏᴛ, ᴛᴏᴘ 10 ᴘʟᴀʏᴇᴅ ɪɴ ᴀ ᴄʜᴀᴛ ᴇᴛᴄ ᴇᴛᴄ.

/sudolist - ᴄʜᴇᴄᴋ sᴜᴅᴏ ᴜsᴇʀs ᴏғ ᴀʙɢ  ʙᴏᴛ

/lyrics [ᴍᴜsɪᴄ ɴᴀᴍᴇ] - sᴇᴀʀᴄʜᴇs ʟʏʀɪᴄs ғᴏʀ ᴛʜᴇ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ᴍᴜsɪᴄ ᴏɴ ᴡᴇʙ.

/song [ᴛʀᴀᴄᴋ ɴᴀᴍᴇ] or [ʏᴛ ʟɪɴᴋ] - ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴʏ ᴛʀᴀᴄᴋ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ɪɴ ᴍᴘ3 or ᴍᴘ4 ғᴏʀᴍᴀᴛꜱ.

/player -  ɢᴇt ᴀ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴘʟᴀʏɪɴɢ ᴘᴀɴᴇʟ.

c ꜱᴛᴀɴᴅꜱ ꜰᴏʀ ᴄʜᴀɴɴᴇʟ ᴘʟᴀʏ.

/queue ᴏʀ /cqueue- ᴄʜᴇᴄᴋ Qᴜᴇᴜᴇ ʟɪꜱᴛ ᴏꜰ ᴍᴜꜱɪᴄ.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" ʙᴀᴄᴋ ", callback_data="Music_"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="jarvis_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_extra":
        query.message.edit_caption(f"*» ᴇxᴛʀᴀ ᴄᴏᴍᴍᴀɴᴅꜱ «*"
            f"""
/mstart - ꜱᴛᴀʀᴛ ᴛʜᴇ ᴍᴜꜱɪᴄ ʙᴏᴛ.
/mhelp  - ɢᴇᴛ ᴄᴏᴍᴍᴀɴᴅꜱ ʜᴇʟᴘᴇʀ ᴍᴇɴᴜ ᴡɪᴛʜ ᴅᴇᴛᴀɪʟᴇᴅ ᴇxᴘʟᴀɴᴀᴛɪᴏɴꜱ ᴏғ ᴄᴏᴍᴍᴀɴᴅꜱ.
/ping- ᴘɪɴɢ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ᴄʜᴇᴄᴋ ʀᴀᴍ, ᴄᴘᴜ ᴇᴛᴄ ꜱᴛᴀᴛꜱ ᴏғ ʙᴏᴛ.

*ɢʀᴏᴜᴘ ꜱᴇᴛᴛɪɴɢꜱ:*
/settings - ɢᴇᴛ a ᴄᴏᴍᴘʟᴇᴛᴇ ɢʀᴏᴜᴘ ꜱᴇᴛᴛɪɴɢꜱ ᴡɪᴛʜ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴꜱ
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" ʙᴀᴄᴋ ", callback_data="Music_"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="jarvis_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_back":
        first_name = update.effective_user.first_name
        query.message.edit_caption(PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,

        )

# <============================================================= NO USE END ========================================================================>

# <============================================== HELP MENU  =========================================================>

def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_photo(HELP_IMG,
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=" ʜᴇʟᴘ ​",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_photo(HELP_IMG,"» Wʜᴇʀᴇ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴏᴘᴇɴ ᴛʜᴇ sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ?.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="👤 ᴏᴩᴇɴ ɪɴ ᴩʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ",
                            url="https://t.me/{}?start=help".format(context.bot.username),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="👥 ᴏᴩᴇɴ ʜᴇʀᴇ",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
               [
                    [InlineKeyboardButton(text="๏ ʙᴀᴄᴋ ๏", callback_data="help_back")]
                ]            
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)

# <============================================== HELP MENU CLOSE =========================================================>

# <============================================== SETTINGS =========================================================>

def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="๏ ʙᴀᴄᴋ ๏",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text("""Hi there! There are quite a few settings for {} - go ahead and pick what "
                you're interested in.""".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(text=
                """Hi there! There are quite a few settings for {} - go ahead and pick what 
                you're interested in.""".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text("""Hi there! There are quite a few settings for {} - go ahead and pick what 
                you're interested in.""".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ᴛʜɪs ᴄʜᴀᴛ's sᴇᴛᴛɪɴɢs ᴀs ᴡᴇʟʟ ᴀs ʏᴏᴜʀs"
            msg.reply_photo(HELP_IMG,text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="sᴇᴛᴛɪɴɢs​",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs"

    else:
        send_settings(chat.id, user.id, True)

# <============================================== SETTINGS MENU CLOSED =========================================================>

# <============================================== NOT USED =========================================================>

def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 7157587567:
            update.effective_message.reply_text(
                f"» ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴩᴇʀ ᴏғ {dispatcher.bot.first_name} sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ɪs [ɢɪᴛʜᴜʙ](https://github.com/doraemon890)"
                f"\n\nʙᴜᴛ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴅᴏɴᴀᴛᴇ ᴛᴏ ᴛʜᴇ ᴩᴇʀsᴏɴ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴜɴɴɪɴɢ ᴍᴇ : [ʜᴇʀᴇ]({DONATE_STRING})",
                parse_mode=ParseMode.MARKDOWN,
                
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                
            )

            update.effective_message.reply_text(
                "ɪ'ᴠᴇ ᴘᴍ'ᴇᴅ ʏᴏᴜ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪɴɢ ᴛᴏ ᴍʏ ᴄʀᴇᴀᴛᴏʀ!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ғɪʀsᴛ ᴛᴏ ɢᴇᴛ ᴅᴏɴᴀᴛɪᴏɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ."
            )
# <============================================== NOT USED END=========================================================>

# <============================================== CHAT MIGRATION USED =========================================================>

def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop
    
# <========================================== CHAT END =============================================================>

# <=================================================== MAIN ====================================================>

def main():
    global x
    x=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🍃beni grubuna ekle bebeğim 🍃",
                            url="https://t.me/uyuyanprensesinki_bot?startgroup=true"
                            )
                       ]
                ]
                     )
    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.send_photo(
                f"@{SUPPORT_CHAT}",
                photo=f"{START_IMG}",
                caption=f"""
✨ㅤ{BOT_NAME} bot aktif bebeğim.
━━━━━━━━━━━━━
**Made by merve**
**versiyon 1:** `{y()}`
**versiyon 2:** `{telever}`
**versiyon 3:** `{tlhver}`
**versiyon 4:** `{pyrover}`
EXPFED🦂 2016
━━━━━━━━━━━━━
""",reply_markup=x,
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                f"Bot isn't able to send message to @{SUPPORT_CHAT}, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)
    start_handler = CommandHandler("start", start, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(
        help_button, pattern=r"help_.*", run_async=True
    )

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(
        settings_button, pattern=r"stngs_", run_async=True
    )

    about_callback_handler = CallbackQueryHandler(
        Jarvis_about_callback, pattern=r"Jarvis_", run_async=True
    )
    source_callback_handler = CallbackQueryHandler(
        Source_about_callback, pattern=r"source_", run_async=True
    )
    music_callback_handler = CallbackQueryHandler(
        Music_about_callback, pattern=r"Music_",run_async=True
    )
    jarvisrobo_main_handler = CallbackQueryHandler(
        JarvisRobo_Main_Callback, pattern=r".*_help",run_async=True)
    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(music_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)
    dispatcher.add_handler(jarvisrobo_main_handler)
    dispatcher.add_error_handler(error_callback)
    dispatcher.add_handler(source_callback_handler)
    LOGGER.info("Using long polling.")
    updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
# <==================================================== END ===================================================>
