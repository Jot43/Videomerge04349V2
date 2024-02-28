import os


class Config(object):
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    TELEGRAM_API = os.environ["TELEGRAM_API"]
    OWNER = os.environ.get("OWNER")
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME")
    SESSION_NAME = os.environ.get("SESSION_NAME", "merge-bot")
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL")
    PASSWORD = os.environ.get("PASSWORD")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    LOGCHANNEL = os.environ.get("LOGCHANNEL")  # Add channel id as -100 + Actual ID
    GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID","root")
    USER_SESSION_STRING = os.environ.get("USER_SESSION_STRING", None)
    IS_PREMIUM = True
    MODES = ["video-video", "video-audio", "video-subtitle","extract-streams"]
    UPSTREAM_REPO = "https://github.com/Jot43/Videomerge04349/"
    UPSTREAM_BRANCH = "main"

    START_TEXT = """
Hi Guys, I am Video Merge Bot!
I can Merge Multiple Videos in One Video. Video Formats should be same.

"""
