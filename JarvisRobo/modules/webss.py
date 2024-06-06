from base64 import b64decode
from inspect import getfullargspec
from io import BytesIO

from pyrogram import filters
from pyrogram.types import Message

from JarvisRobo import pbot as app
from JarvisRobo.utils.post import post


async def ekran_görüntüsü_al(url: str, tam: bool = False):
    url = "https://" + url if not url.startswith("http") else url
    veri = {
        "url": url,
        "genişlik": 1920,
        "yükseklik": 1080,
        "ölçek": 1,
        "biçim": "jpeg",
    }
    if tam:
        veri["tam"] = True
    veri = await post(
        "https://webscreenshot.vercel.app/api",
        veri=veri,
    )
    if "resim" not in veri:
        return None
    b = veri["resim"].replace("data:image/jpeg;base64,", "")
    dosya = BytesIO(b64decode(b))
    dosya.name = "webss.jpg"
    return dosya


async def cevap_veya_mesaj(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_message(filters.command(["webss", "ss", "webshot"]))
async def ekran_görüntüsü_al_komutu(_, mesaj: Message):
    if len(mesaj.command) < 2:
        return await cevap_veya_mesaj(mesaj, text="Ekran görüntüsü almak için bir URL verin.")

    if len(mesaj.command) == 2:
        url = mesaj.text.split(None, 1)[1]
        tam = False
    elif len(mesaj.command) == 3:
        url = mesaj.text.split(None, 2)[1]
        tam = mesaj.text.split(None, 2)[2].lower().strip() in [
            "evet",
            "e",
            "1",
            "doğru",
        ]
    else:
        return await cevap_veya_mesaj(mesaj, text="Geçersiz komut.")

    m = await cevap_veya_mesaj(mesaj, text="Ekran görüntüsü alınıyor...")

    try:
        fotoğraf = await ekran_görüntüsü_al(url, tam)
        if not fotoğraf:
            return await m.edit("Ekran görüntüsü alınamadı.")

        m = await m.edit("Yükleniyor...")

        if not tam:
            await mesaj.reply_document(fotoğraf)
        else:
            await mesaj.reply_document(fotoğraf)
        await m.delete()
    except Exception as e:
        await m.edit(str(e))


__yardım__ = """
» /webss *:* Verilen URL'nin ekran görüntüsünü gönderir.
"""
__mod_adi__ = "✨Webshot✨"
            
