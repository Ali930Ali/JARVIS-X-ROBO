import asyncio
from telethon import events
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from JarvisRobo import telethn as client

spam_chats = []

@client.on(events.NewMessage(pattern=r"^(@tagammmm|@laww|/tygaaaa|@mention) ?(.*)"))
async def mention_all(event):
    chat_id = event.chat_id

    if event.is_private:
        return await event.respond("__Bu komut yalnızca grup ve kanallarda kullanılabilir!__")

    is_admin = False
    try:
        participant = await client(GetParticipantRequest(event.chat_id, event.sender_id))
        if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            is_admin = True
    except UserNotParticipantError:
        pass

    if not is_admin:
        return await event.respond("__sadece adminler bu komutu kullanabilir!__")

    mode = "text_on_cmd"
    msg = None

    if event.pattern_match.group(2):
        msg = event.pattern_match.group(2).strip()
    elif event.is_reply:
        msg = await event.get_reply_message()
        if msg is None:
            return await event.respond("__I can't mention members for older messages!__")

    if msg is None:
        return await event.respond("__Reply to a message or provide some text to mention others!__")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for user in client.iter_participants(chat_id):
        if chat_id not in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{user.first_name}](tg://user?id={user.id}), "
        if usrnum == 15:
            if mode == "text_on_cmd":
                txt = f"{msg}\n{usrtxt}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(usrtxt)
            await asyncio.sleep(3)
            usrnum = 0
            usrtxt = ""

    spam_chats.remove(chat_id)

@client.on(events.NewMessage(pattern=r"^/cancel$"))
async def cancel_spam(event):
    if event.chat_id not in spam_chats:
        return await event.respond("Devam eden bir süreç yok.")

    is_admin = False
    try:
        participant = await client(GetParticipantRequest(event.chat_id, event.sender_id))
        if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            is_admin = True
    except UserNotParticipantError:
        pass

    if not is_admin:
        return await event.respond("__Bu komutu yalnızca yöneticiler yürütebilir!__")

    spam_chats.remove(event.chat_id)
    return await event.respond("etiketleme işlemi durdu.")

__mod_name__ = "✨etiket atmak✨"
__help__ = """
──「  sadece adminler 」──

❍ /utag or @all '(kullanıcıları etiketler.'
"""
