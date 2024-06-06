from typing import Callable

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from JarvisRobo import DEV_USERS, DRAGONS, pbot


def bilgi_degistirebilir(func: Callable) -> Callable:
    async def admin_degil(_, message: Message):
        if message.from_user.id in DRAGONS:
            return await func(_, message)

        kontrol = await pbot.get_chat_member(message.chat.id, message.from_user.id)
        if kontrol.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text(
                "» Siz bir admin değilsiniz, lütfen sınırlarınızda kalın."
            )

        admin = (
            await pbot.get_chat_member(message.chat.id, message.from_user.id)
        ).privileges
        if admin.can_change_info:
            return await func(_, message)
        else:
            return await message.reply_text(
                "`Grup bilgisini değiştirme izniniz yok."
            )

    return admin_degil


def kisitlayabilir(func: Callable) -> Callable:
    async def admin_degil(_, message: Message):
        if message.from_user.id in DEV_USERS:
            return await func(_, message)

        kontrol = await pbot.get_chat_member(message.chat.id, message.from_user.id)
        if kontrol.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text(
                "» Siz bir admin değilsiniz, lütfen sınırlarınızda kalın."
            )

        admin = (
            await pbot.get_chat_member(message.chat.id, message.from_user.id)
        ).privileges
        if admin.can_restrict_members:
            return await func(_, message)
        else:
            return await message.reply_text(
                "`Bu sohbette kullanıcıları kısıtlama izniniz yok."
            )

    return admin_degil

def terfi_edebilir(func: Callable) -> Callable:
    async def admin_degil(_, message: Message):
        if message.from_user.id in DEV_USERS:
            return await func(_, message)

        kontrol = await pbot.get_chat_member(message.chat.id, message.from_user.id)
        if kontrol.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text(
                "» Siz bir admin değilsiniz, lütfen sınırlarınızda kalın."
            )

        admin = (
            await pbot.get_chat_member(message.chat.id, message.from_user.id)
        ).privileges
        if admin.can_promote_members:
            return await func(_, message)
        else:
            return await message.reply_text(
                "`Bu sohbette kullanıcıları terfi ettirme/düşürme izniniz yok."
            )

    return admin_degil
            
