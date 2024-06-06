from datetime import datetime

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message, User

from JarvisRobo import pbot


def CevapKontrol(message: Message):
    cevap_id = None

    if message.reply_to_message:
        cevap_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        cevap_id = message.message_id

    return cevap_id


bilgitext = (
    "[{full_name}](tg://user?id={user_id})\n\n"
    " ➻ ᴋᴜʟʟᴀɴɪᴄɪ ɪᴅ: `{user_id}`\n"
    " ➻ ɪsɪᴍ: `{first_name}`\n"
    " ➻ ᴠᴇ ᴅᴏɢʀᴜ ɪsɪᴍ: `{last_name}`\n"
    " ➻ ᴋᴜʟʟᴀɴɪᴄɪ ᴀᴅɪ: `@{username}`\n"
    " ➻ ᴠᴇ sᴏɴ ɢᴏʀᴜʟᴇɴ: `{last_online}`"
)


def SonGörülme(kullanıcı: User):
    if kullanıcı.is_bot:
        return ""
    elif kullanıcı.status == "recently":
        return "Son günlerde"
    elif kullanıcı.status == "within_week":
        return "Son bir hafta içinde"
    elif kullanıcı.status == "within_month":
        return "Son bir ay içinde"
    elif kullanıcı.status == "long_time_ago":
        return "Uzun zaman önce :("
    elif kullanıcı.status == "online":
        return "Şu anda çevrimiçi"
    elif kullanıcı.status == "offline":
        return datetime.fromtimestamp(kullanıcı.status.date).strftime(
            "%a, %d %b %Y, %H:%M:%S"
        )


def Tamİsim(kullanıcı: User):
    return kullanıcı.first_name + " " + kullanıcı.last_name if kullanıcı.last_name else kullanıcı.first_name


@pbot.on_message(filters.command("kim"))
async def kim(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        kullanıcı_al = message.from_user.id
    elif len(cmd) == 1:
        kullanıcı_al = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        kullanıcı_al = cmd[1]
        try:
            kullanıcı_al = int(cmd[1])
        except ValueError:
            pass
    try:
        kullanıcı = await client.get_users(kullanıcı_al)
    except PeerIdInvalid:
        await message.reply("Bu kullanıcıyı tanımıyorum.")
        return
    açıklama = await client.get_chat(kullanıcı_al)
    açıklama = açıklama.description
    await message.reply_text(
        bilgitext.format(
            full_name=Tamİsim(kullanıcı),
            user_id=kullanıcı.id,
            user_dc=kullanıcı.dc_id,
            first_name=kullanıcı.first_name,
            last_name=kullanıcı.last_name if kullanıcı.last_name else "",
            username=kullanıcı.username if kullanıcı.username else "",
            last_online=SonGörülme(kullanıcı),
            bio=açıklama if açıklama else "`Boş.`",
        ),
        disable_web_page_preview=True,
    )
    
