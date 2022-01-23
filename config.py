import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "BQA5eFzFl7i0-vsHo-cD5cbOyMN0w1BhbapOvuTmbrdwCje5T99nnRAQtCzZIvGWWxf0bVGwpI0LoVV61wuDmtns_Bh1KbLLmmfg2015j2ufs9pIZdhy2kVwQnDUTo6pSWiNLxb_KxuLVlN9g07jubQWhi79xkcy_ye6e3RjwxiEwwtSSUbp6Q7i_F-HhnAbAA7_bIeHxWA920JprTlWumws9gmbxmSCgZ3Eysz4RHsfc-SlMvTs5hY_w0UNyC-YfdexHTQKf4nU8eOXRabGDuKIFFllKX1WYGju_ELFkH9IecYWaGRYoySAwIVDjgKBMiaKvF21LYOcm9jFKfO8IK96f1cFWQA")
BOT_TOKEN = getenv("BOT_TOKEN", "5066166780:AAHqeVMDtEFe56-8s2KL9ZBGHtbdZ7OYysI")
BOT_NAME = getenv("BOT_NAME", "𝗥𝗩𝗛𝗫𝗜 𝗠𝗨𝗦𝗜𝗖")
API_ID = getenv("API_ID", "18090591")
API_HASH = getenv("API_HASH", "ca33cf9726a9d37f18786126fc27c61c")
OWNER_NAME = getenv("OWNER_NAME", "rahkiii")
ALIVE_NAME = getenv("ALIVE_NAME", "𝗥𝗩𝗛𝗫𝗜 𝗠𝗨𝗦𝗜𝗖")
BOT_USERNAME = getenv("BOT_USERNAME", "RahkiiiXRobot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "𝗥𝗩𝗛𝗫𝗜")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "idnsSupportGroup")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "idnschannel")
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", ".").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/file/ad887c0edc78956cde087.jpg")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "90"))
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/d6f92c979ad96b2031cba.png")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/6213d2673486beca02967.png")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/f02efde766160d3ff52d6.png")
IMG_4 = getenv("IMG_4", "https://telegra.ph/file/19ef76c0a097b1a394b00.png")
