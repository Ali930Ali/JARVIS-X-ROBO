import random
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from JarvisRobo import pbot

@pbot.on_message(filters.command(["duvar", "duvarKağıdı"]))
async def duvar(_, message: Message):
    "Jarvis tarafından düzeltilmiş duvar kağıdı"
    try:
        text = message.text.split(None, 1)[1]
    except IndexError:
        text = None
    if not text:
        return await message.reply_text("`Lütfen aramak için bir sorgu girin.`")
    m = await message.reply_text("`Duvar kağıtları aranıyor...`")
    try:
        url = requests.get(f"https://api.safone.me/wall?query={text}").json()["results"]
        ran = random.randint(0, 3)
        await message.reply_photo(
            photo=url[ran]["imageUrl"],
            caption=f"🥀 **Talep eden:** {message.from_user.mention}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Bağlantı", url=url[ran]["imageUrl"])],
                ]
            ),
        )
        await m.delete()
    except Exception as e:
        await m.edit_text(
            f"`Duvar kağıdı bulunamadı: `{text}`",
        )
        
