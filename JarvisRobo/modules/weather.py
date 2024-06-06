import io
import aiohttp
from telethon.tl import functions, types

from JarvisRobo import telethn as tbot
from JarvisRobo.events import kayıt


async def kayıtlı_yönetici_mi(sohbet, kullanıcı):
    if isinstance(sohbet, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(sohbet, kullanıcı))
            ).katılımcı,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(sohbet, types.InputPeerUser):
        return True


@kayıt(desen="^/havadurumu (.*)")
async def _(etkinlik):
    if etkinlik.fwd_from:
        return

    örnek_url = "https://wttr.in/{}.png"
    giriş_str = etkinlik.desen_eşleme.grup(1)
    async with aiohttp.ClientSession() as oturum:
        yanıt_api_sıfır = await oturum.get(örnek_url.format(giriş_str))
        yanıt_api = await yanıt_api_sıfır.read()
        with io.BytesIO(yanıt_api) as çıkış_dosya:
            await etkinlik.reply(dosya=çıkış_dosya)


__yardım__ = """
Ben tüm şehirlerin hava durumu bilgilerini bulabilirim.

 ❍ /havadurumu <şehir>*:* Gelişmiş hava durumu modülü, kullanımı /weather ile aynıdır.
 ❍ /havadurumu  ay*:* Ay'ın güncel durumunu alır
"""

__mod_adi__ = "✨Hava Durumu✨"
