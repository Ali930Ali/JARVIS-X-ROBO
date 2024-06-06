import inspect
import re
from pathlib import Path

from pymongo import MongoClient
from telethon import events

from JarvisRobo import MONGO_DB_URI, telethn

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["managerdb"]
gbanned = db.gban


def register(**args):
    """Yeni bir mesaj kaydeder."""
    pattern = args.get("pattern", None)

    r_pattern = r"^[/!.]"

    eğer pattern is not None ve pattern "(?i)" ile başlamıyorsa:
        args["pattern"] = "(?i)" + pattern

    args["pattern"] = pattern.replace("^/", r_pattern, 1)

    def decorator(func):
        telethn.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator


def chataction(**args):
    """Sohbet eylemlerini kaydeder."""

    def decorator(func):
        telethn.add_event_handler(func, events.ChatAction(**args))
        return func

    return decorator


def userupdate(**args):
    """Kullanıcı güncellemelerini kaydeder."""

    def decorator(func):
        telethn.add_event_handler(func, events.UserUpdate(**args))
        return func

    return decorator


def inlinequery(**args):
    """Satır içi sorgu kaydeder."""
    pattern = args.get("pattern", None)

    eğer pattern is not None ve pattern "(?i)" ile başlamıyorsa:
        args["pattern"] = "(?i)" + pattern

    def decorator(func):
        telethn.add_event_handler(func, events.InlineQuery(**args))
        return func

    return decorator


def callbackquery(**args):
    """Geri çağırma sorgusunu kaydeder."""

    def decorator(func):
        telethn.add_event_handler(func, events.CallbackQuery(**args))
        return func

    return decorator

def Jarvisinline(**args):
    def decorator(func):
        telethn.add_event_handler(func, events.CallbackQuery(**args))
        return func

    return decorator

def bot(**args):
    pattern = args.get("pattern")
    r_pattern = r"^[/]"

    eğer pattern is not None ve pattern "(?i)" ile başlamıyorsa:
        args["pattern"] = "(?i)" + pattern

    args["pattern"] = pattern.replace("^/", r_pattern, 1)
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    reg = re.compile("(.*)")

    eğer pattern is not None:
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
            except BaseException:
                pass

            try:
                FUN_LIST[file_test].append(cmd)
            except BaseException:
                FUN_LIST.update({file_test: [cmd]})
        except BaseException:
            pass

    def decorator(func):
        async def wrapper(check):
            eğer check.edit_date:
                return
            eğer check.fwd_from:
                return
            eğer check.is_group veya check.is_private:
                pass
            else:
                print("kanallarda çalışmıyorum")
                return
            eğer check.is_group:
                eğer check.chat.megagroup:
                    pass
                else:
                    print("küçük sohbetlerde çalışmıyorum")
                    return

            users = gbanned.find({})
            for c in users:
                eğer check.sender_id == c["user"]:
                    return
            try:
                await func(check)
                try:
                    LOAD_PLUG[file_test].append(func)
                except Exception:
                    LOAD_PLUG.update({file_test: [func]})
            except BaseException:
                return
            else:
                pass

        telethn.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator


def JarvisRobo(**args):
    pattern = args.get("pattern", None)
    args.get("disable_edited", False)
    ignore_unsafe = args.get("ignore_unsafe", False)
    unsafe_pattern = r"^[^/!#@\$A-Za-z]"
    args.get("group_only", False)
    args.get("disable_errors", False)
    args.get("insecure", False)
    eğer pattern is not None ve pattern "(?i)" ile başlamıyorsa:
        args["pattern"] = "(?i)" + pattern

    eğer "disable_edited" args içinde ise:
        del args["disable_edited"]

    eğer "ignore_unsafe" args içinde ise:
        del args["ignore_unsafe"]

    eğer "group_only" args içinde ise:
        del args["group_only"]

    eğer "disable_errors" args içinde ise:
        del args["disable_errors"]

    eğer "insecure" args içinde ise:
        del args["insecure"]

    eğer pattern varsa:
        eğer ignore_unsafe değilse:
            args["pattern"] = args["pattern"].replace("^.", unsafe_pattern, 1)
    
