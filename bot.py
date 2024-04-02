from dotenv import load_dotenv

load_dotenv(
    "config.env",
    override=True,
)
import asyncio
import os
import shutil
import time

import psutil
import pyromod
from PIL import Image
from pyrogram import Client, filters,enums
from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    PeerIdInvalid,
    UserIsBlocked,
)
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    User,
)

from __init__ import (
    AUDIO_EXTENSIONS,
    BROADCAST_MSG,
    LOGGER,
    MERGE_MODE,
    SUBTITLE_EXTENSIONS,
    UPLOAD_AS_DOC,
    UPLOAD_TO_DRIVE,
    VIDEO_EXTENSIONS,
    bMaker,
    formatDB,
    gDict,
    queueDB,
    replyDB,
)
from config import Config
from helpers.database import database
from helpers.forcesub import ForceSub
from helpers.utils import UserSettings, get_readable_file_size, get_readable_time

botStartTime = time.time()
parent_id = Config.GDRIVE_FOLDER_ID


class MergeBot(Client):
    def start(self):
        super().start()
        try:
            self.send_message(chat_id=int(Config.OWNER), text="<b>Bᴏᴛ sᴛᴀʀᴛᴇᴅ .!</b>")
        except Exception as err:
            LOGGER.error("Bᴏᴏᴛ ᴀʟᴇʀᴛ ғᴀɪʟᴇᴅ! Pʟᴇᴀsᴇ sᴛᴀʀᴛ ʙᴏᴛ ɪɴ PM")
        return LOGGER.info("Bᴏᴛ Sᴛᴀʀᴛᴇᴅ!")

    def stop(self):
        super().stop()
        return LOGGER.info("Bᴏᴛ Sᴛᴏᴘᴘᴇᴅ")


mergeApp = MergeBot(
    name=Config.SESSION_NAME,
    api_hash=Config.API_HASH,
    api_id=int(Config.TELEGRAM_API),
    bot_token=Config.BOT_TOKEN,
    workers=300,
    plugins=dict(root="plugins"),
    app_version="5.0+yash-mergebot",
)


if os.path.exists("downloads") == False:
    os.makedirs("downloads")


@mergeApp.on_message(filters.command(["log"]) & filters.user(Config.OWNER_USERNAME))
async def sendLogFile(c: Client, m: Message):
    await m.reply_document(document="./mergebotlog.txt")
    return


@mergeApp.on_message(filters.command(["login"]) & filters.private)
async def loginHandler(c: Client, m: Message):
    Fsub = await ForceSub(c, m)
    if Fsub == 400:
        return
    user = UserSettings(m.from_user.id, m.from_user.first_name)
    if user.banned:
        await m.reply_text(text=f"**Bᴀɴɴᴇᴅ ᴜsᴇʀ ᴅᴇᴛᴇᴄᴛᴇᴅ!**\n  Message Here For Login Key @i_manjot_sidhu\n\nCᴏɴᴛᴀᴄᴛ: 🈲 @{Config.OWNER_USERNAME}", quote=True)
        return
    if user.user_id == int(Config.OWNER):
        user.allowed = True
    if user.allowed:
        await m.reply_text(text=f"**Dᴏɴᴛ sᴘᴀᴍ**\n  ⚡ Yᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ!!", quote=True)
    else:
        try:
            passwd = m.text.split(" ", 1)[1]
        except:
            await m.reply_text("**Cᴏᴍᴍᴀɴᴅ:**\n  `/login <password>`\n\n**Usᴀɢᴇ:**\n  `password`: Geᴛ ᴛʜᴇ ᴘᴀssᴡᴏʀᴅ ғʀᴏᴍ ᴏᴡɴᴇʀ",quote=True,parse_mode=enums.parse_mode.ParseMode.MARKDOWN)
        passwd = passwd.strip()
        if passwd == Config.PASSWORD:
            user.allowed = True
            await m.reply_text(
                text=f"**Aᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ  ✅,**\n  ⚡ Nᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ!!", quote=True
            )
        else:
            await m.reply_text(
                text=f"**Aᴄᴄᴇss ᴅᴇɴɪᴇᴅ ❌,**\n  Message Here For Login Key @i_manjot_sidhu\n\nCᴏɴᴛᴀᴄᴛ: 🈲 @{Config.OWNER_USERNAME}",
                quote=True,
            )
    user.set()
    del user
    return


@mergeApp.on_message(filters.command(["stats"]) & filters.private)
async def stats_handler(c: Client, m: Message):
    currentTime = get_readable_time(time.time() - botStartTime)
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = (
        f"<b>╭「 💠 ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs 」</b>\n"
        f"<b>│</b>\n"
        f"<b>├⏳ Bᴏᴛ ᴜᴘᴛɪᴍᴇ : {currentTime}</b>\n"
        f"<b>├💾 Tᴏᴛᴀʟ ᴅɪsᴋ sᴘᴀᴄᴇ : {total}</b>\n"
        f"<b>├📀 Tᴏᴛᴀʟ ᴜsᴇᴅ sᴘᴀᴄᴇ : {used}</b>\n"
        f"<b>├💿 Tᴏᴛᴀʟ ғʀᴇᴇ sᴘᴀᴄᴇ : {free}</b>\n"
        f"<b>├🔺 Tᴏᴛᴀʟ ᴜᴘʟᴏᴀᴅ : {sent}</b>\n"
        f"<b>├🔻 Tᴏᴛᴀʟ ᴅᴏᴡɴʟᴏᴀᴅ : {recv}</b>\n"
        f"<b>├🖥 CPU : {cpuUsage}%</b>\n"
        f"<b>├⚙️ RAM : {memory}%</b>\n"
        f"<b>╰💿 DISK : {disk}%</b>"
    )
    await m.reply_text(text=stats, quote=True)


@mergeApp.on_message(
    filters.command(["broadcast"])
    & filters.private
    & filters.user(Config.OWNER_USERNAME)
)
async def broadcast_handler(c: Client, m: Message):
    msg = m.reply_to_message
    if msg is None:
        await m.reply_text("Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ.")
        return
    userList = await database.broadcast()
    len = userList.collection.count_documents({})
    status = await m.reply_text(text=BROADCAST_MSG.format(str(len), "0"), quote=True)
    success = 0
    for i in range(len):
        try:
            uid = userList[i]["_id"]
            if uid != int(Config.OWNER):
                await msg.copy(chat_id=uid)
            success = i + 1
            await status.edit_text(text=BROADCAST_MSG.format(len, success))
            LOGGER.info(f"Message sent to {userList[i]['name']} ")
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await msg.copy(chat_id=userList[i]["_id"])
            LOGGER.info(f"Message sent to {userList[i]['name']} ")
        except InputUserDeactivated:
            await database.deleteUser(userList[i]["_id"])
            LOGGER.info(f"{userList[i]['_id']} - {userList[i]['name']} : Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ\n")
        except UserIsBlocked:
            await database.deleteUser(userList[i]["_id"])
            LOGGER.info(
                f"{userList[i]['_id']} - {userList[i]['name']} : Bʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ\n"
            )
        except PeerIdInvalid:
            await database.deleteUser(userList[i]["_id"])
            LOGGER.info(
                f"{userList[i]['_id']} - {userList[i]['name']} : Usᴇʀ ID ɪɴᴠᴀʟɪᴅ\n"
            )
        except Exception as err:
            LOGGER.warning(f"{err}\n")
        await asyncio.sleep(3)
    await status.edit_text(
        text=BROADCAST_MSG.format(len, success)
        + f"**Fᴀɪʟᴇᴅ: {str(len-success)}**\n\n__🤓 Bʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ sᴜᴄᴇssғᴜʟʟʏ__",
    )
	
@mergeApp.on_message(filters.command(["start"]) & filters.private)
async def start_handler(c: Client, m: Message):
   Fsub = await ForceSub(c, m)
   if Fsub == 400:
        return
   user = UserSettings(m.from_user.id, m.from_user.first_name)
       
        user.allowed = True
        user.set()
    res = await m.reply_text(
        text=f"Hi **{m.from_user.first_name}**\n\n ⚡ I am a file/video merger bot\n\n😎 I can merge Telegram files!, And upload it to telegram\n\n**Owner: 🈲 @i_manjot_sidhu** ",
        quote=True,
    )
    del user


@mergeApp.on_message(
    (filters.document | filters.video | filters.audio) & filters.private
)
async def files_handler(c: Client, m: Message):
    Fsub = await ForceSub(c, m)
    if Fsub == 400:
        return
    user_id = m.from_user.id
    user = UserSettings(user_id, m.from_user.first_name)
    if user.merge_mode == 4: # extract_mode
        return
    input_ = f"downloads/{str(user_id)}/input.txt"
    if os.path.exists(input_):
        await m.reply_text("Sᴏʀʀʏ ʙʀᴏ,\nAʟʀᴇᴀᴅʏ ᴏɴᴇ ᴘʀᴏᴄᴇss ɪɴ ᴘʀᴏɢʀᴇss!\nDᴏɴ'ᴛ sᴘᴀᴍ.")
        return
    media = m.video or m.document or m.audio
    if media.file_name is None:
        await m.reply_text("File Not Found")
        return
    currentFileNameExt = media.file_name.rsplit(sep=".")[-1].lower()
    if currentFileNameExt in "conf":
        await m.reply_text(
            text="**💾 Cᴏɴғɪɢ ғɪʟᴇ ғᴏᴜɴᴅ, Dᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴀᴠᴇ ɪᴛ?**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("✅ Yᴇs", callback_data=f"rclone_save"),
                        InlineKeyboardButton("❌ Nᴏ", callback_data="rclone_discard"),
                    ]
                ]
            ),
            quote=True,
        )
        return
    # if MERGE_MODE.get(user_id) is None:
    #     userMergeMode = database.getUserMergeSettings(user_id)
    #     if userMergeMode is not None:
    #         MERGE_MODE[user_id] = userMergeMode
    #     else:
    #         database.setUserMergeMode(uid=user_id, mode=1)
    #         MERGE_MODE[user_id] = 1

    if user.merge_mode == 1:

        if queueDB.get(user_id, None) is None:
            formatDB.update({user_id: currentFileNameExt})
        if formatDB.get(
            user_id, None
        ) is not None and currentFileNameExt != formatDB.get(user_id):
            await m.reply_text(
                f"Fɪʀsᴛ ʏᴏᴜ sᴇɴᴛ ᴀ {formatDB.get(user_id).upper()} ғɪʟᴇ sᴏ ɴᴏᴡ sᴇɴᴅ ᴏɴʟʏ ᴛʜᴀᴛ ᴛʏᴘᴇ ᴏғ ғɪʟᴇ.",
                quote=True,
            )
            return
        if currentFileNameExt not in VIDEO_EXTENSIONS:
            await m.reply_text(
                "Tʜɪs ᴠɪᴅᴇᴏ ғᴏʀᴍᴀᴛ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ!\nOɴʟʏ sᴇɴᴅ MP4 ᴏʀ MKV ᴏʀ WEBM.",
                quote=True,
            )
            return
        editable = await m.reply_text("Pʟᴇᴀsᴇ ᴡᴀɪᴛ ...", quote=True)
        MessageText = "Oᴋᴀʏ,\nNᴏᴡ sᴇɴᴅ ᴍᴇ ɴᴇxᴛ ᴠɪᴅᴇᴏ ᴏʀ ᴘʀᴇss **Merge Now** ʙᴜᴛᴛᴏɴ!"

        if queueDB.get(user_id, None) is None:
            queueDB.update({user_id: {"videos": [], "subtitles": [], "audios": []}})
        if (
            len(queueDB.get(user_id)["videos"]) >= 0
            and len(queueDB.get(user_id)["videos"]) < 25
        ):
            queueDB.get(user_id)["videos"].append(m.id)
            queueDB.get(m.from_user.id)["subtitles"].append(None)

            # LOGGER.info(
            #     queueDB.get(user_id)["videos"], queueDB.get(m.from_user.id)["subtitles"]
            # )

            if len(queueDB.get(user_id)["videos"]) == 1:
                reply_ = await editable.edit(
                    "**Sᴇɴᴅ ᴍᴇ sᴏᴍᴇ ᴍᴏʀᴇ ᴠɪᴅᴇᴏs ᴛᴏ ᴍᴇʀɢᴇ ᴛʜᴇᴍ ɪɴᴛᴏ sɪɴɢʟᴇ ғɪʟᴇ**",
                    reply_markup=InlineKeyboardMarkup(
                        bMaker.makebuttons(["Cᴀɴᴄᴇʟ"], ["cancel"])
                    ),
                )
                replyDB.update({user_id: reply_.id})
                return
            if queueDB.get(user_id, None)["videos"] is None:
                formatDB.update({user_id: currentFileNameExt})
            if replyDB.get(user_id, None) is not None:
                await c.delete_messages(
                    chat_id=m.chat.id, message_ids=replyDB.get(user_id)
                )
            if len(queueDB.get(user_id)["videos"]) == 25:
                MessageText = "Oᴋᴀʏ, ɴᴏᴡ ᴊᴜsᴛ ᴘʀᴇss **Merge Now** ʙᴜᴛᴛᴏɴ ᴘʟᴏx!"
            markup = await makeButtons(c, m, queueDB)
            reply_ = await editable.edit(
                text=MessageText, reply_markup=InlineKeyboardMarkup(markup)
            )
            replyDB.update({user_id: reply_.id})
        elif len(queueDB.get(user_id)["videos"]) > 25:
            markup = await makeButtons(c, m, queueDB)
            await editable.text(
                "Mᴀx 𝟷𝟶 ᴠɪᴅᴇᴏs ᴀʟʟᴏᴡᴇᴅ", reply_markup=InlineKeyboardMarkup(markup)
            )

    elif user.merge_mode == 2:
        editable = await m.reply_text("Pʟᴇᴀsᴇ ᴡᴀɪᴛ ...", quote=True)
        MessageText = (
            "Oᴋᴀʏ,\nNᴏᴡ sᴇɴᴅ ᴍᴇ sᴏᴍᴇ ᴍᴏʀᴇ <u>Audios</u> ᴏʀ ᴘʀᴇss **Merge Now** ʙᴜᴛᴛᴏɴ!"
        )

        if queueDB.get(user_id, None) is None:
            queueDB.update({user_id: {"videos": [], "subtitles": [], "audios": []}})
        if len(queueDB.get(user_id)["videos"]) == 0:
            queueDB.get(user_id)["videos"].append(m.id)
            # if len(queueDB.get(user_id)["videos"])==1:
            reply_ = await editable.edit(
                text="Nᴏᴡ, sᴇɴᴅ ᴀʟʟ ᴛʜᴇ ᴀᴜᴅɪᴏs ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴍᴇʀɢᴇ",
                reply_markup=InlineKeyboardMarkup(
                    bMaker.makebuttons(["Cᴀɴᴄᴇʟ"], ["cancel"])
                ),
            )
            replyDB.update({user_id: reply_.id})
            return
        elif (
            len(queueDB.get(user_id)["videos"]) >= 1
            and currentFileNameExt in AUDIO_EXTENSIONS
        ):
            queueDB.get(user_id)["audios"].append(m.id)
            if replyDB.get(user_id, None) is not None:
                await c.delete_messages(
                    chat_id=m.chat.id, message_ids=replyDB.get(user_id)
                )
            markup = await makeButtons(c, m, queueDB)

            reply_ = await editable.edit(
                text=MessageText, reply_markup=InlineKeyboardMarkup(markup)
            )
            replyDB.update({user_id: reply_.id})
        else:
            await m.reply("Tʜɪs ғɪʟᴇᴛʏᴘᴇ ɪs ɴᴏᴛ ᴠᴀʟɪᴅ")
            return

    elif user.merge_mode == 3:

        editable = await m.reply_text("Pʟᴇᴀsᴇ ᴡᴀɪᴛ ...", quote=True)
        MessageText = "Oᴋᴀʏ,\nNᴏᴡ sᴇɴᴅ ᴍᴇ sᴏᴍᴇ ᴍᴏʀᴇ <u>Subtitles</u> ᴏʀ ᴘʀᴇss **Merge Now** ʙᴜᴛᴛᴏɴ!"
        if queueDB.get(user_id, None) is None:
            queueDB.update({user_id: {"videos": [], "subtitles": [], "audios": []}})
        if len(queueDB.get(user_id)["videos"]) == 0:
            queueDB.get(user_id)["videos"].append(m.id)
            # if len(queueDB.get(user_id)["videos"])==1:
            reply_ = await editable.edit(
                text="Nᴏᴡ, sᴇɴᴅ ᴀʟʟ ᴛʜᴇ sᴜʙᴛɪᴛʟᴇs ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴍᴇʀɢᴇ",
                reply_markup=InlineKeyboardMarkup(
                    bMaker.makebuttons(["Cᴀɴᴄᴇʟ"], ["cancel"])
                ),
            )
            replyDB.update({user_id: reply_.id})
            return
        elif (
            len(queueDB.get(user_id)["videos"]) >= 1
            and currentFileNameExt in SUBTITLE_EXTENSIONS
        ):
            queueDB.get(user_id)["subtitles"].append(m.id)
            if replyDB.get(user_id, None) is not None:
                await c.delete_messages(
                    chat_id=m.chat.id, message_ids=replyDB.get(user_id)
                )
            markup = await makeButtons(c, m, queueDB)

            reply_ = await editable.edit(
                text=MessageText, reply_markup=InlineKeyboardMarkup(markup)
            )
            replyDB.update({user_id: reply_.id})
        else:
            await m.reply("Tʜɪs ғɪʟᴇᴛʏᴘᴇ ɪs ɴᴏᴛ ᴠᴀʟɪᴅ")
            return

				
@mergeApp.on_message(filters.photo & filters.private)
async def photo_handler(c: Client, m: Message):
    Fsub = await ForceSub(c, m)
    if Fsub == 400:
        return
    user = UserSettings(m.chat.id, m.from_user.first_name)
    #if m.from_user.id != int(Config.OWNER):
    thumbnail = m.photo.file_id
    msg = await m.reply_text("Sᴀᴠɪɴɢ ᴛʜᴜᴍʙɴᴀɪʟ. . . .", quote=True)
    user.thumbnail = thumbnail
    user.set()
    # await database.saveThumb(m.from_user.id, thumbnail)
    LOCATION = f"downloads/{m.from_user.id}_thumb.jpg"
    await c.download_media(message=m, file_name=LOCATION)
    await msg.edit_text(text="✅ Cᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ sᴀᴠᴇᴅ!")
    del user


@mergeApp.on_message(filters.command(["extract"]) & filters.private)
async def media_extracter(c: Client, m: Message):
    Fsub = await ForceSub(c, m)
    if Fsub == 400:
        return
    user = UserSettings(uid=m.from_user.id, name=m.from_user.first_name)
    if not user.allowed:
        return
    if user.merge_mode == 4:
        if m.reply_to_message is None:
            await m.reply(text="Rᴇᴘʟʏ /extract ᴛᴏ ᴀ ᴠɪᴅᴇᴏ ᴏʀ ᴅᴏᴄᴜᴍᴇɴᴛ ғɪʟᴇ")
            return
        rmess = m.reply_to_message
        if rmess.video or rmess.document:
            media = rmess.video or rmess.document
            mid=rmess.id
            file_name = media.file_name
            if file_name is None:
                await m.reply("Fɪʟᴇ ɴᴀᴍᴇ ɴᴏᴛ ғᴏᴜɴᴅ:)")
                return
            markup = bMaker.makebuttons(
                set1=["Audio", "Subtitle", "Cancel"],
                set2=[f"extract_audio_{mid}", f"extract_subtitle_{mid}", 'cancel'],
                isCallback=True,
                rows=2,
            )
            await m.reply(
                text="Cʜᴏᴏsᴇ ғʀᴏᴍ ʙᴇʟᴏᴡ ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴇxᴛʀᴀᴄᴛ?",
                quote=True,
                reply_markup=InlineKeyboardMarkup(markup),
            )
    else:
        await m.reply(
            text="Cʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs ᴀɴᴅ sᴇᴛ ᴍᴏᴅᴇ ᴛᴏ ᴇxᴛʀᴀᴄᴛ\nᴛʜᴇɴ ᴜsᴇ /extract ᴄᴏᴍᴍᴀɴᴅ"
        )


@mergeApp.on_message(filters.command(["help"]) & filters.private)
async def help_msg(c: Client, m: Message):
    Fsub = await ForceSub(c, m)
    if Fsub == 400:
        return
    await m.reply_text(
        text="""**Fᴏʟʟᴏᴡ ᴛʜᴇsᴇ sᴛᴇᴘs:

1) Send me the custom thumbnail (optional).
2) Send two or more Your Videos Which you want to merge
3) After sending all files select merge options
4) Select the upload mode.
5) Select rename if you want to give custom file name else press default**""",
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Cʟᴏsᴇ 🔐", callback_data="close")]]
        ),
    )


@mergeApp.on_message(filters.command(["about"]) & filters.private)
async def about_handler(c: Client, m: Message):
    Fsub = await ForceSub(c, m)
    if Fsub == 400:
        return
    await m.reply_text(
        text="""
**Wʜᴀᴛ's ɴᴇᴡ:**
👨‍💻 Bᴀɴ/ᴜɴʙᴀɴ ᴜsᴇʀs
👨‍💻 Exᴛʀᴀᴄᴛ ᴀʟʟ ᴀᴜᴅɪᴏs ᴀɴᴅ sᴜʙᴛɪᴛʟᴇs ғʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇᴅɪᴀ
👨‍💻 Mᴇʀɢᴇ ᴠɪᴅᴇᴏ + ᴀᴜᴅɪᴏ 
👨‍💻 Mᴇʀɢᴇ ᴠɪᴅᴇᴏ + sᴜʙᴛɪᴛʟᴇs
👨‍💻 Uᴘʟᴏᴀᴅ ᴛᴏ ᴅʀɪᴠᴇ ᴜsɪɴɢ ʏᴏᴜʀ ᴏᴡɴ ʀᴄʟᴏɴᴇ ᴄᴏɴғɪɢ
👨‍💻 Mᴇʀɢᴇᴅ ᴠɪᴅᴇᴏ ᴘʀᴇsᴇʀᴠᴇs ᴀʟʟ sᴛʀᴇᴀᴍs ᴏғ ᴛʜᴇ ғɪʀsᴛ ᴠɪᴅᴇᴏ ʏᴏᴜ sᴇɴᴅ (ɪ.ᴇ ᴀʟʟ ᴀᴜᴅɪᴏᴛʀᴀᴄᴋs/sᴜʙᴛɪᴛʟᴇs)
➖➖➖➖➖➖➖➖➖➖➖➖➖
**Fᴇᴀᴛᴜʀᴇs**
🔰 Mᴇʀɢᴇ ᴜᴘᴛᴏ 25 ᴠɪᴅᴇᴏ ɪɴ ᴏɴᴇ 
🔰 Uᴘʟᴏᴀᴅ ᴀs ᴅᴏᴄᴜᴍᴇɴᴛs/ᴠɪᴅᴇᴏ
🔰 Cᴜsᴛᴏᴍs ᴛʜᴜᴍʙɴᴀɪʟ sᴜᴘᴘᴏʀᴛ
🔰 Usᴇʀs ᴄᴀɴ ʟᴏɢɪɴ ᴛᴏ ʙᴏᴛ ᴜsɪɴɢ ᴘᴀssᴡᴏʀᴅ
🔰 Oᴡɴᴇʀ ᴄᴀɴ ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ᴜsᴇʀs
		""",
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
			InlineKeyboardButton("👨‍💻 Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/nordbotz"),
		        InlineKeyboardButton("🤔 Dᴇᴘʟᴏʏᴇᴅ ʙʏ", url=f"https://t.me/{Config.OWNER_USERNAME}")
		],
                [
			InlineKeyboardButton("Cʟᴏsᴇ 🔐", callback_data="close")],
            ]
        ),
    )


@mergeApp.on_message(
    filters.command(["savethumb", "setthumb", "savethumbnail"]) & filters.private
)
async def save_thumbnail(c: Client, m: Message):
    Fsub = await ForceSub(c, m)
    if Fsub == 400:
        return
    if m.reply_to_message:
        if m.reply_to_message.photo:
            await photo_handler(c, m.reply_to_message)
        else:
            await m.reply(text="Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠᴀʟɪᴅ ᴘʜᴏᴛᴏ")
    else:
        await m.reply(text="Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ")
    return


@mergeApp.on_message(filters.command(["showthumbnail"]) & filters.private)
async def show_thumbnail(c: Client, m: Message):
    try:
        user = UserSettings(m.from_user.id, m.from_user.first_name)
        thumb_id = user.thumbnail
        LOCATION = f"downloads/{str(m.from_user.id)}_thumb.jpg"
        if os.path.exists(LOCATION):
            await m.reply_photo(
                photo=LOCATION, caption="🖼️ Yᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ", quote=True
            )
        elif thumb_id is not None :
            await c.download_media(message=str(thumb_id), file_name=LOCATION)
            await m.reply_photo(
                photo=LOCATION, caption="🖼️ Yᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ", quote=True
            )
        else: 
            await m.reply_text(text="❌ Cᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ɴᴏᴛ ғᴏᴜɴᴅ", quote=True)
        del user
    except Exception as err:
        LOGGER.info(err)
        await m.reply_text(text="❌ Cᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ɴᴏᴛ ғᴏᴜɴᴅ", quote=True)
	    
        await m.reply_text(text="❌ Cᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ɴᴏᴛ ғᴏᴜɴᴅ", quote=True)
	    
@mergeApp.on_message(filters.command(["cancel"]) & filters.private)
async def cancel_handler(c: Client, m: Message):
    Fsub = await ForceSub(c, m)
    if Fsub == 400:
        return
    await m.reply_text(
        text="""**Click To Cancel Button 
Note:- You're Task Cancelled But Not Closed Download/Upload Status [@NordBotz]**""",
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Click To Cancel ❌", callback_data="cancel")]]
        ),
    )


@mergeApp.on_message(filters.command(["deletethumbnail"]) & filters.private)
async def delete_thumbnail(c: Client, m: Message):
    try:
        user = UserSettings(m.from_user.id, m.from_user.first_name)
        user.thumbnail = None
        user.set()
        if os.path.exists(f"downloads/{str(m.from_user.id)}"):
            os.remove(f"downloads/{str(m.from_user.id)}")
            await m.reply_text("✅ Dᴇʟᴇᴛᴇᴅ sᴜᴄᴇssғᴜʟʟʏ", quote=True)
            del user
        else: raise Exception("Tʜᴜᴍʙɴᴀɪʟ ғɪʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ")
    except Exception as err:
        await m.reply_text(text="❌ Cᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ɴᴏᴛ ғᴏᴜɴᴅ", quote=True)

@mergeApp.on_message(filters.command(["ban","unban"]) & filters.private)
async def ban_user(c:Client,m:Message):
    incoming=m.text.split(' ')[0]
    if incoming == '/ban':
        if m.from_user.id == int(Config.OWNER):
            try:
                abuser_id = int(m.text.split(" ")[1])
                if abuser_id == int(Config.OWNER):
                    await m.reply_text("I ᴄᴀɴ'ᴛ ʙᴀɴ ʏᴏᴜ ᴍᴀsᴛᴇʀ,\nPʟᴇᴀsᴇ ᴅᴏɴ'ᴛ ᴀʙᴀɴᴅᴏɴ ᴍᴇ. ",quote=True)
                else:
                    try:
                        user_obj: User = await c.get_users(abuser_id)
                        udata  = UserSettings(uid=abuser_id,name=user_obj.first_name)
                        udata.banned=True
                        udata.allowed=False
                        udata.set()
                        await m.reply_text(f"Pᴏᴏᴏғ, {user_obj.first_name} ʜᴀs ʙᴇᴇɴ **BANNED**",quote=True)
                        acknowledgement = f"""
Dear {user_obj.first_name},
I found your messages annoying and forwarded them to our team of moderators for inspection. The moderators have confirmed the report and your account is now banned.

While the account is banned, you will not be able to do certain things, like merging videos/audios/subtitles or extract audios from Telegram media.

Your account can be released only by @{Config.OWNER_USERNAME}."""
                        try:
                            await c.send_message(
                                chat_id=abuser_id,
                                text=acknowledgement
                            )
                        except Exception as e:
                            await m.reply_text(f"Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ sᴇɴᴅɪɴɢ ᴀᴄᴋɴᴏᴡʟᴇᴅɢᴇᴍᴇɴᴛ\n\n`{e}`",quote=True)
                            LOGGER.error(e)
                    except Exception as e:
                        LOGGER.error(e)
            except:
                await m.reply_text("**Cᴏᴍᴍᴀɴᴅ:**\n  `/ban <user_id>`\n\n**Usᴀɢᴇ:**\n  `user_id`: Usᴇʀ ID ᴏғ ᴛʜᴇ ᴜsᴇʀ",quote=True,parse_mode=enums.parse_mode.ParseMode.MARKDOWN)
        else:
            await m.reply_text("**(Oɴʟʏ ғᴏʀ ᴏᴡɴᴇʀ 🫅🏻)\nCᴏᴍᴍᴀɴᴅ:**\n  `/ban <user_id>`\n\n**Usᴀɢᴇ:**\n  `user_id`: Usᴇʀ ID ᴏғ ᴛʜᴇ ᴜsᴇʀ",quote=True,parse_mode=enums.parse_mode.ParseMode.MARKDOWN)
        return
    elif incoming == '/unban':
        if m.from_user.id == int(Config.OWNER):
            try:
                abuser_id = int(m.text.split(" ")[1])
                if abuser_id == int(Config.OWNER):
                    await m.reply_text("I ᴄᴀɴ'ᴛ ʙᴀɴ ʏᴏᴜ ᴍᴀsᴛᴇʀ,\nPʟᴇᴀsᴇ ᴅᴏɴ'ᴛ ᴀʙᴀɴᴅᴏɴ ᴍᴇ. ",quote=True)
                else:
                    try:
                        user_obj: User = await c.get_users(abuser_id)
                        udata  = UserSettings(uid=abuser_id,name=user_obj.first_name)
                        udata.banned=False
                        udata.allowed=True
                        udata.set()
                        await m.reply_text(f"Pᴏᴏᴏғ, {user_obj.first_name} ʜᴀs ʙᴇᴇɴ **UN_BANNED**",quote=True)
                        release_notice = f"""
Gᴏᴏᴅ ɴᴇᴡs {user_obj.first_name}, ᴛʜᴇ ʙᴀɴ ʜᴀs ʙᴇᴇɴ ᴜᴘʟɪғᴛᴇᴅ ᴏɴ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ. Yᴏᴜ'ʀᴇ ғʀᴇᴇ ᴀs ᴀ ʙɪʀᴅ!"""
                        try:
                            await c.send_message(
                                chat_id=abuser_id,
                                text=release_notice
                            )
                        except Exception as e:
                            await m.reply_text(f"Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ sᴇɴᴅɪɴɢ ʀᴇʟᴇᴀsᴇ ɴᴏᴛɪᴄᴇ\n\n`{e}`",quote=True)
                            LOGGER.error(e)                      
                    except Exception as e:
                        LOGGER.error(e)
            except:
                await m.reply_text("**Cᴏᴍᴍᴀɴᴅ:**\n  `/unban <user_id>`\n\n**Usᴀɢᴇ:**\n  `user_id`: Usᴇʀ ID ᴏғ ᴛʜᴇ ᴜsᴇʀ",quote=True,parse_mode=enums.parse_mode.ParseMode.MARKDOWN)
        else:
            await m.reply_text("**(Oɴʟʏ ғᴏʀ ᴏᴡɴᴇʀ 🫅🏻)\nCᴏᴍᴍᴀɴᴅ:**\n  `/unban <user_id>`\n\n**Usᴀɢᴇ:**\n  `user_id`: Usᴇʀ ID ᴏғ ᴛʜᴇ ᴜsᴇʀ",quote=True,parse_mode=enums.parse_mode.ParseMode.MARKDOWN)
        return
async def showQueue(c: Client, cb: CallbackQuery):
    try:
        markup = await makeButtons(c, cb.message, queueDB)
        await cb.message.edit(
            text="Oᴋᴀʏ,\nNᴏᴡ sᴇɴᴅ ᴍᴇ ɴᴇxᴛ ᴠɪᴅᴇᴏ ᴏʀ ᴘʀᴇss **Merge Now** ʙᴜᴛᴛᴏɴ!",
            reply_markup=InlineKeyboardMarkup(markup),
        )
    except ValueError:
        await cb.message.edit("Sᴇɴᴅ sᴏᴍᴇ ᴍᴏʀᴇ ᴠɪᴅᴇᴏs")
    return


async def delete_all(root):
    try:
        shutil.rmtree(root)
    except Exception as e:
        LOGGER.info(e)



	    
async def makeButtons(c: Client, m: Message, db: dict):
    Fsub = await ForceSub(c, m)
    if Fsub == 400:
        return
    markup = []
    user = UserSettings(m.chat.id, m.chat.first_name)
    if user.merge_mode == 1:
        for i in await c.get_messages(
            chat_id=m.chat.id, message_ids=db.get(m.chat.id)["videos"]
        ):
            media = i.video or i.document or None
            if media is None:
                continue
            else:
                markup.append(
                    [
                        InlineKeyboardButton(
                            f"{media.file_name}",
                            callback_data=f"showFileName_{i.id}",
                        )
                    ]
                )

    elif user.merge_mode == 2:
        msgs: list[Message] = await c.get_messages(
            chat_id=m.chat.id, message_ids=db.get(m.chat.id)["audios"]
        )
        msgs.insert(
            0,
            await c.get_messages(
                chat_id=m.chat.id, message_ids=db.get(m.chat.id)["videos"][0]
            ),
        )
        for i in msgs:
            media = i.audio or i.document or i.video or None
            if media is None:
                continue
            else:
                markup.append(
                    [
                        InlineKeyboardButton(
                            f"{media.file_name}",
                            callback_data=f"tryotherbutton",
                        )
                    ]
                )

    elif user.merge_mode == 3:
        msgs: list[Message] = await c.get_messages(
            chat_id=m.chat.id, message_ids=db.get(m.chat.id)["subtitles"]
        )
        msgs.insert(
            0,
            await c.get_messages(
                chat_id=m.chat.id, message_ids=db.get(m.chat.id)["videos"][0]
            ),
        )
        for i in msgs:
            media = i.video or i.document or None

            if media is None:
                continue
            else:
                markup.append(
                    [
                        InlineKeyboardButton(
                            f"{media.file_name}",
                            callback_data=f"tryotherbutton",
                        )
                    ]
                )

    markup.append([InlineKeyboardButton("🗂 Mᴇʀɢᴇ ɴᴏᴡ @𝑵𝒐𝒓𝒅𝑩𝒐𝒕𝒛 ", callback_data="merge")])
    markup.append([InlineKeyboardButton("🚫 Cʟᴇᴀʀ ғɪʟᴇs", callback_data="cancel")])
    return markup


LOGCHANNEL = Config.LOGCHANNEL
try:
    if Config.USER_SESSION_STRING is None:
        raise KeyError

    LOGGER.info("Starting USER Session")
    userBot = Client(
        name="merge-bot-user",
        session_string=Config.USER_SESSION_STRING,
        no_updates=True,
    )

except KeyError:
    userBot = None
    LOGGER.warning("No User Session, Default Bot session will be used")



if __name__ == "__main__":
    # with mergeApp:
    #     bot:User = mergeApp.get_me()
    #     bot_username = bot.username
    try:
        with userBot:
            userBot.send_message(
                chat_id=int(LOGCHANNEL),
                text="Bᴏᴛ ʙᴏᴏᴛᴇᴅ ᴡɪᴛʜ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴏᴜɴᴛ,\n\n  Tʜᴀɴᴋs ғᴏʀ ᴜsɪɴɢ <a href='https://t.me/NordBotz'>ᴛʜɪs ʀᴇᴘᴏ</a>",
                disable_web_page_preview=True,
            )
            user = userBot.get_me()
            Config.IS_PREMIUM = user.is_premium
    except Exception as err:
        LOGGER.error(f"{err}")
        Config.IS_PREMIUM = False
        pass

    mergeApp.run()
