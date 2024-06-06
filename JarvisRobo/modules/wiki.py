import wikipedia
from telegram import ParseMode, Update
from telegram.ext import CallbackContext
from wikipedia.exceptions import DisambiguationError, PageError

from JarvisRobo import dispatcher
from JarvisRobo.modules.disable import DisableAbleCommandHandler


def wiki(update: Update, context: CallbackContext):
    msg = (
        update.effective_message.reply_to_message
        if update.effective_message.reply_to_message
        else update.effective_message
    )
    sonuç = ""
    if msg == update.effective_message:
        arama = msg.text.split(" ", maxsplit=1)[1]
    else:
        arama = msg.text
    try:
        sonuç = wikipedia.summary(arama)
    except DisambiguationError as e:
        update.message.reply_text(
            "Belirsiz sayfalar bulundu! Sorgunuzu buna göre ayarlayın.\n<i>{}</i>".format(
                e
            ),
            parse_mode=ParseMode.HTML,
        )
    except PageError as e:
        update.message.reply_text(
            "<code>{}</code>".format(e), parse_mode=ParseMode.HTML
        )
    if sonuç:
        result = f"<b>{arama}</b>\n\n"
        result += f"<i>{sonuç}</i>\n"
        result += f"""<a href="https://tr.wikipedia.org/wiki/{arama.replace(" ", "%20")}">Daha fazlasını oku...</a>"""
        if len(result) > 4000:
            with open("sonuç.txt", "w") as f:
                f.write(f"{sonuç}\n\nUwU OwO OmO UmU")
            with open("sonuç.txt", "rb") as f:
                context.bot.send_document(
                    document=f,
                    filename=f.name,
                    reply_to_message_id=update.message.message_id,
                    chat_id=update.effective_chat.id,
                    parse_mode=ParseMode.HTML,
                )
        else:
            update.message.reply_text(
                result, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )


WIKI_HANDLER = DisableAbleCommandHandler("wiki", wiki, run_async=True)
dispatcher.add_handler(WIKI_HANDLER)

__help__ = """
» /wiki (metin) *:* Verilen metin hakkında Wikipedia'da arama yapar.
"""
__mod_name__ = "✨Wɪᴋɪ✨"
