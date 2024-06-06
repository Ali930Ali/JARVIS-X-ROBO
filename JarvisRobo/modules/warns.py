import html
import re
from typing import Optional

import telegram
from telegram import (
    CallbackQuery,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ParseMode,
    Update,
    User,
)
from telegram.error import BadRequest
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    DispatcherHandlerStop,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

from JarvisRobo import TIGERS, WOLVES, dispatcher
from JarvisRobo.modules.disable import DisableAbleCommandHandler
from JarvisRobo.modules.helper_funcs.chat_status import (
    bot_admin,
    can_restrict,
    is_user_admin,
    user_admin,
    user_admin_no_reply,
)
from JarvisRobo.modules.helper_funcs.extraction import (
    extract_text,
    extract_user,
    extract_user_and_text,
)
from JarvisRobo.modules.helper_funcs.filters import CustomFilters
from JarvisRobo.modules.helper_funcs.misc import split_message
from JarvisRobo.modules.helper_funcs.string_handling import split_quotes
from JarvisRobo.modules.log_channel import loggable
from JarvisRobo.modules.sql import warns_sql as sql
from JarvisRobo.modules.sql.approve_sql import is_approved

UYARI_HANDLER_GRUP = 9
MEVCUT_UYARI_FİLTRE_METNİ = "<b>Bu sohbetteki mevcut uyarı filtreleri:</b>\n"


# Async değil
def uyarı(
    kullanıcı: User,
    sohbet: Chat,
    sebep: str,
    mesaj: Message,
    uyarıcı: User = None,
) -> str:
    if is_user_admin(sohbet, kullanıcı.id):
        # message.reply_text("Adminler, tek vuruşla olacak kadar uzaktalar!")
        return

    if kullanıcı.id in TIGERS:
        if uyarıcı:
            mesaj.reply_text("Kaplanlar uyarılamaz.")
        else:
            mesaj.reply_text(
                "Bir kaplan, otomatik bir uyarı filtresini tetikledi!\nBen kaplanları uyarılamam, ancak bunun kötüye kullanılmasından kaçınmaları gerekir.",
            )
        return

    if kullanıcı.id in WOLVES:
        if uyarıcı:
            mesaj.reply_text("Kurt felaketleri uyarıya karşı bağışık.")
        else:
            mesaj.reply_text(
                "Kurt Felaketi, otomatik bir uyarı filtresini tetikledi!\nBen kurtları uyarılamam, ancak bunun kötüye kullanılmasından kaçınmaları gerekir.",
            )
        return

    if uyarıcı:
        uyarıcı_etiketi = mention_html(uyarıcı.id, uyarıcı.first_name)
    else:
        uyarıcı_etiketi = "Otomatik uyarı filtresi."

    sınır, yumuşak_uyarı = sql.get_warn_setting(sohbet.id)
    num_uyarılar, sebepler = sql.warn_user(kullanıcı.id, sohbet.id, sebep)
    if num_uyarılar >= sınır:
        sql.reset_warns(kullanıcı.id, sohbet.id)
        if yumuşak_uyarı:  # tekme
            sohbet.unban_member(kullanıcı.id)
            yanıt = (
                f"<code>❕</code><b> Tekme Olayı </b>\n"
                f"<code> </code><b>•  Kullanıcı: </b> {mention_html(kullanıcı.id, kullanıcı.first_name)}\n"
                f"<code> </code><b>•  Sayı: </b> {sınır}"
            )

        else:  # yasak
            sohbet.kick_member(kullanıcı.id)
            yanıt = (
                f"<code>❕</code><b> Yasak Olayı </b>\n"
                f"<code> </code><b>•  Kullanıcı: </b> {mention_html(kullanıcı.id, kullanıcı.first_name)}\n"
                f"<code> </code><b>•  Sayı: </b> {sınır}"
            )

        for uyarı_sebep in sebepler:
            yanıt += f"\n - {html.escape(uyarı_sebep)}"

        # message.bot.send_sticker(sohbet.id, BAN_STICKER)
        klavye = None
        log_sebep = (
            f"<b>{html.escape(sohbet.title)}:</b>\n"
            f"#UYARI_YASAKLA\n"
            f"<b>Yönetici:</b> {uyarıcı_etiketi}\n"
            f"<b>Kullanıcı:</b> {mention_html(kullanıcı.id, kullanıcı.first_name)}\n"
            f"<b>Sebep:</b> {sebep}\n"
            f"<b>Sayılar:</b> <code>{num_uyarılar}/{sınır}</code>"
        )

    else:
        klavye = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✨ ᴜyᴀʀɪ ᴋᴀʟᴅɪʀ ✨",
                        callback_data="rm_warn({})".format(kullanıcı.id),
                    ),
                ],
            ],
        )

        yanıt = (
            f"<code>❕</code><b> Uyarı Olayı </b>\n"
            f"<code> </code><b>•  Kullanıcı: </b> {mention_html(kullanıcı.id, kullanıcı.first_name)}\n"
            f"<code> </code><b>•  Sayı: </b> {num_uyarılar}/{sınır}"
        )
        if sebep:
            yanıt += f"\n<code> </code><b>•  Sebep: </b> {html.escape(sebep)}"

        log_sebep = (
            f"<b>{html.escape(sohbet.title)}:</b>\n"
            f"#UYARI\n"
            f"<b>Yönetici:</b> {uyarıcı_etiketi}\n"
            f"<b>Kullanıcı:</b> {mention_html(kullanıcı.id, kullanıcı.first_name)}\n"
            f"<b>Sebep:</b> {sebep}\n"
            f"<b>Sayılar:</b> <code>{num_uyarılar}/{sınır}</code>"
        )

    try:
        mesaj.reply_text(yanıt, reply_markup=klavye, parse_mode=ParseMode.HTML)
    except BadRequest as excp:
        if excp.message == "Reply message not
        
