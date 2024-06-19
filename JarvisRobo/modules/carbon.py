from pyrogram import filters

from JarvisRobo import pbot
from JarvisRobo.utils.errors import capture_err
from JarvisRobo.utils.functions import make_carbon


@pbot.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if message.reply_to_message:
        if message.reply_to_message.text:
            txt = message.reply_to_message.text
        else:
            return await message.reply_text("bir mesaja cevap ver veya ver.")
    else:
        try:
            txt = message.text.split(None, 1)[1]
        except IndexError:
            return await message.reply_text("bir mesaja cevap verin veya mesaj gönderin.")
    m = await message.reply_text("karbon üretmek...")
    carbon = await make_carbon(txt)
    await m.edit_text("üretilen karbonun yüklenmesi...")
    await pbot.send_photo(
        message.chat.id,
        photo=carbon,
        caption=f"» tarafından talep edildi : {message.from_user.mention}",
    )
    await m.delete()
    carbon.close()

__mod_name__ = "✨kᴀʀʙᴏɴ✨"

__help__ = """

Verilen metnin bir karbonunu yapar ve size gönderir.
❍ /carbon *:* bir metne yanıt vermek karbon yapar

 """
