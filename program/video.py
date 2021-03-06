# Copyright (C) 2021 By Veez Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

import asyncio
import re

from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py, user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:70]
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["idnsvplay", f"idnsvplay@{BOT_USERNAME}"]) & other_filters)
async def idnsvplay(c: Client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="πΌπ΄π½π", callback_data="cbmenu"),
                InlineKeyboardButton(text="π²π»πΎππ΄", callback_data="cls"),
            ]
        ]
    )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f To use me, I need to be an **Administrator** with the following **permissions**:\n\nΒ» β __Delete messages__\nΒ» β __Ban users__\nΒ» β __Add users__\nΒ» β __Manage voice chat__\n\nData is **updated** automatically after you **promote me**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "missing required permission:" + "\n\nΒ» β __Manage voice chat__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "missing required permission:" + "\n\nΒ» β __Delete messages__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("missing required permission:" + "\n\nΒ» β __Add users__")
        return
    if not a.can_restrict_members:
        await m.reply_text("missing required permission:" + "\n\nΒ» β __Ban users__")
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **is banned in group** {m.chat.title}\n\nΒ» **unban the userbot first if you want to use this bot.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"β **userbot failed to join**\n\n**reason**:{e}")
                return
        else:
            try:
                pope = await c.export_chat_invite_link(chat_id)
                pepo = await c.revoke_chat_invite_link(chat_id, pope)
                await user.join_chat(pepo.invite_link)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"β **userbot failed to join**\n\n**reason**:{e}"
                )

    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("π₯ **downloading video...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "Β» __only 720, 480, 360 allowed__ \nβ° **now streaming video in 720p**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"β° **Track added to the queue**\n\n[{songname}]({link})\nβ° **πΎπππ© ππ:** `{chat_id}`\nβ° **πππ§π’ππ£π©πππ£ πππ§π:** {requester}\nβ° **ππ€π¨ππ¨π π‘ππ¨π© Β»** `{pos}`",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"β° **πππππ€ ππ©π§πππ’ππ£π πΏπ π’πͺπ‘ππ...**\n\n[{songname}]({link})\nβ° **πΎπππ© ππ:** `{chat_id}`\nβΉοΈ **ππ©ππ©πͺπ¨ π¨πππ© ππ£π:** `Playing`\nβ° **πππ§π’ππ£π©πππ£ πππ§π:** {requester}",
                    reply_markup=keyboard,
                )
        else:
            if len(m.command) < 2:
                await m.reply(
                    "Β» reply to an **video file** or **give something to search.**"
                )
            else:
                loser = await m.reply("π **searching...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("β **no results found.**")
                else:
                    songname = search[0]
                    url = search[1]
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await loser.edit(f"β yt-dl issues detected\n\nΒ» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_1}",
                                caption=f"π‘ **πππππ€ ππ©π§πππ’ππ£π πΏπ π’πͺπ‘ππ...**\n\n[{songname}]({url})\nπ¬ **πΎπππ© ππ:** `{chat_id}`\nπ§ **πππ§π’ππ£π©πππ£ πππ§π:** {requester}\nπ’ **ππ€π¨ππ¨π π‘ππ¨π© Β»** `{pos}`",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().pulse_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=f"{IMG_2}",
                                    caption=f"π‘ **πππππ€ ππ©π§πππ’ππ£π πΏπ π’πͺπ‘ππ....**\n\n[{songname}]({url})\nπ¬ **πΎπππ© ππ:** `{chat_id}`\nβΉοΈ **ππ©ππ©πͺπ¨ π¨πππ© ππ£π:** `Playing`\nπ§ **πππ§π’ππ£π©πππ£ πππ§π:** {requester}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await m.reply_text(f"β error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "Β» reply to an **video file** or **give something to search.**"
            )
        else:
            loser = await m.reply("π **searching...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("β **no results found.**")
            else:
                songname = search[0]
                url = search[1]
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"β yt-dl issues detected\n\nΒ» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=f"{IMG_1}",
                            caption=f"π‘ **Track added to the queue**\n\n[{songname}]({url})\nπ¬ **πΎπππ© ππ:** `{chat_id}`\nπ§ **πππ§π’ππ£π©πππ£ πππ§π:** {requester}\nπ’ **ππ€π¨ππ¨π π‘ππ¨π© Β»** `{pos}`",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_2}",
                                caption=f"π‘ **πππππ€ ππ©π§πππ’ππ£π πΏπ π’πͺπ‘ππ....**\n\n[{songname}]({url})\nπ¬ **πΎπππ© ππ:** `{chat_id}`\nβΉοΈ **ππ©ππ©πͺπ¨ π¨πππ© ππ£π:** `Playing`\nπ§ **πππ§π’ππ£π©πππ£ πππ§π:** {requester}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await m.reply_text(f"β error: `{ep}`")


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & other_filters)
async def vstream(c: Client, m: Message):
    m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Menu", callback_data="cbmenu"),
                InlineKeyboardButton(text="Close", callback_data="cls"),
            ]
        ]
    )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"π‘ To use me, I need to be an **Administrator** with the following **permissions**:\n\nΒ» β __Delete messages__\nΒ» β __Ban users__\nΒ» β __Add users__\nΒ» β __Manage voice chat__\n\nData is **updated** automatically after you **promote me**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "missing required permission:" + "\n\nΒ» β __Manage voice chat__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "missing required permission:" + "\n\nΒ» β __Delete messages__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("missing required permission:" + "\n\nΒ» β __Add users__")
        return
    if not a.can_restrict_members:
        await m.reply_text("missing required permission:" + "\n\nΒ» β __Ban users__")
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **is banned in group** {m.chat.title}\n\nΒ» **unban the userbot first if you want to use this bot.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"β **userbot failed to join**\n\n**reason**:{e}")
                return
        else:
            try:
                pope = await c.export_chat_invite_link(chat_id)
                pepo = await c.revoke_chat_invite_link(chat_id, pope)
                await user.join_chat(pepo.invite_link)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"β **userbot failed to join**\n\n**reason**:{e}"
                )

    if len(m.command) < 2:
        await m.reply("Β» give me a live-link/m3u8 url/youtube link to stream.")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await m.reply("π **processing stream...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "Β» __only 720, 480, 360 allowed__ \nπ‘ **now streaming video in 720p**"
                )
            loser = await m.reply("π **processing stream...**")
        else:
            await m.reply("**/vstream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await loser.edit(f"β yt-dl issues detected\n\nΒ» `{ytlink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"π‘ **Track added to the queue**\nπ¬ **πΎπππ© ππ:** `{chat_id}`\nπ§ *πππ§π’ππ£π©πππ£ πππ§π:** {requester}\nπ’ **ππ€π¨ππ¨π π‘ππ¨π© Β»** `{pos}`",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"π‘ **[πππππ€ ππ©π§πππ’ππ£π]({link}) started.**\nπ¬ **πΎπππ© ππ:** `{chat_id}`\nβΉοΈ **ππ©ππ©πͺπ¨ π¨πππ© ππ£π:** `Playing`\nπ§ **πππ§π’ππ£π©πππ£ πππ§π:** {requester}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await m.reply_text(f"β error: `{ep}`")
