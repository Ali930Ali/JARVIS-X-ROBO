
class Config(object):
    LOGGER = True
    # GEREKLİ
    # https://my.telegram.org adresine giriş yapın ve verilen ayrıntılarla bu alanları doldurun

    API_ID = "" # tam sayı değeri, çift tırnak kullanmayın ""
    API_HASH = ""
    TOKEN = ""  # Bu değişken API_KEY iken şimdi TOKEN, buna göre ayarlayın.
    OWNER_ID = "7036733368" # Bilmiyorsanız, botu çalıştırın ve onunla özel sohbetinizde /id yazın, ayrıca tam sayı
    
    SUPPORT_CHAT = "https://t.me/Armageddonsohbet"  # Destek için kendi grubunuz, @ eklemeyin
    START_IMG = ""
    EVENT_LOGS = ()  # gbans, sudo promosyonları, AI etkinleştirme devre dışı bırakma durumları gibi hata ayıklamaya ve benzeri durumlara yardımcı olabilecek bilgileri yazdırır
    MONGO_DB_URI = "mongodb+srv://MANAGERDB:RAJNISHAYUSHI@managerdb.lfnlzdk.mongodb.net/?retryWrites=true&w=majority&appName=managerdb"
    # ÖNERİLEN
    DATABASE_URL = ""  # elephantsql.com'dan bir sql veritabanı url'si
    CASH_API_KEY = (
        "X652FNVGJ0ZXABM0"  # API anahtarınızı https://www.alphavantage.co/support/#api-key adresinden alın
    )
    TIME_API_KEY = "VR8S3BA8ESW3"
    
    # API anahtarınızı https://timezonedb.com/api adresinden alın

    # İsteğe bağlı alanlar
    BL_CHATS = []  # Karalisteye almak istediğiniz grupların listesi.
    DRAGONS = []  # Sudo kullanıcılarının kullanıcı kimliği
    DEV_USERS = []  # Geliştirici kullanıcılarının kullanıcı kimliği
    DEMONS = []  # Destek kullanıcılarının kullanıcı kimliği
    TIGERS = []  # Kaplan kullanıcılarının kullanıcı kimliği
    WOLVES = []  # Beyaz liste kullanıcılarının kullanıcı kimliği

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8
    

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
    
