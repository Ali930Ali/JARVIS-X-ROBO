from asyncio import sleep

from telethon import events
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChatBannedRights

from JarvisRobo import DEMONS, DEV_USERS, DRAGONS, OWNER_ID, telethn

# =================== SABİT ===================

YASAKLANMIŞ_HAKLAR = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


YASAKSIZ_HAKLAR = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


YÖNETİCİLER = [OWNER_ID] + DEV_USERS + DRAGONS + DEMONS 

# Kullanıcının admin haklarına sahip olup olmadığını kontrol edin


async def yönetici_mi(user_id: int, message):
    yönetici = False
    async for user in telethn.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in YÖNETİCİLER:
            yönetici = True
            break
    return yönetici


@telethn.on(events.NewMessage(pattern="^[!/]zombies ?(.*)"))
async def sil_silinmis(show):
    con = show.pattern_match.group(1).lower()
    sil_u = 0
    sil_durumu = "**Grup temiz, 0 silinmiş hesap bulundu.**"
    if con != "clean":
        kontol = await show.reply("`Silinecek hesaplar aranıyor...`")
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                sil_u += 1
                await sleep(1)
        if sil_u > 0:
            sil_durumu = (
                f"**Aranıyor...** `{sil_u}` **Silinmiş hesap/Zombi Bu grupta,"
                "\nKomutla temizle** `/zombies clean`"
            )
        return await kontol.edit(sil_durumu)
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await show.reply("**Üzgünüm, yönetici değilsiniz!**")
    memek = await show.reply("`Silinecek silinmiş hesaplar temizleniyor...`")
    sil_u = 0
    sil_a = 0
    async for user in telethn.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, YASAKLANMIŞ_HAKLAR)
                )
            except ChatAdminRequiredError:
                return await show.edit("`Bu grupta yasaklanmış haklara sahip değil`")
            except UserAdminInvalidError:
                sil_u -= 1
                sil_a += 1
            await telethn(EditBannedRequest(show.chat_id, user.id, YASAKSIZ_HAKLAR))
            sil_u += 1
    if sil_u > 0:
        sil_durumu = f"**Temizlendi** `{sil_u}` **Zombi**"
    if sil_a > 0:
        sil_durumu = (
            f"**Temizlendi** `{sil_u}` **Zombi** "
            f"\n`{sil_a}` **Yönetici zombiler silinmedi.**"
        )
    await memek.edit(sil_durumu)


__yardım__ = """
*Silinmiş hesapları kaldırma*
 ❍ /zombies *:* Grubunuzda silinmiş hesapları aramaya başlar.
 ❍ /zombies clean *:* Grubunuzdaki silinmiş hesapları temizler.
"""


__mod_adı__ = "✨Zombi✨"
            
