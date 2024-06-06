
from pyrogram import filters
from pyrogram.types import Message
from JarvisRobo import BOT_NAME, BOT_USERNAME
from JarvisRobo import pbot as jarvis
import requests

@jarvis.on_message(filters.command("yaz"))
async def el_yazısı(_, message: Message):
    if message.reply_to_message:
        metin = message.reply_to_message.text
    else:
        metin = message.text.split(None, 1)[1]
    yanıt_mesajı = await message.reply_text( "`Lütfen bekleyin...,\n\nMetninizi yazıyorum...`")
    
    yazılmış_resim = requests.get(f"https://apis.xditya.me/write?text={metin}").url

    altyazı = f"""
Metin başarıyla yazıldı 💘
✨ **Yazan :** [{BOT_NAME}](https://t.me/{BOT_USERNAME})
🥀 **İsteyen :** {message.from_user.mention}
"""
    await yanıt_mesajı.delete()
    await message.reply_photo(photo=yazılmış_resim, caption=altyazı)

__mod_name__ = "✨YᴀᴢTᴏᴏʟ✨"

__yardım__ = """

 Verilen metni bir kalemle beyaz bir sayfaya yazar 🖊

❍ /yaz <metin> *:* Verilen metni yazar.
 """
