from GroupMenter import telethn as bot
from GroupMenter import telethn as tbot
from GroupMenter.events import register
from telethon import *
from telethon import Button, custom, events, functions
from GroupMenter.helper_extra.badmedia import is_nsfw
import requests
import string 
import random 
from GroupMenter.modules.sql_extended.nsfw_watch_sql import add_nsfwatch, rmnsfwatch, get_all_nsfw_enabled_chat, is_nsfwatch_indb
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )
@register(pattern="^/nsfw")
async def nsfw(event):
    if event.is_private:
       return   
    if event.is_group:
            pass
    if is_nsfwatch_indb(str(event.chat_id)):
        await event.reply("`Tbu Sohbet, NSFW izlemeyi Etkinleştirdi`")
    else:
        await event.reply("`NSFW Watch bu sohbet için kapalı`")

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
@register(pattern="^/addnsfw")
async def nsfw_watch(event):
    if event.is_private:
       return   
    if event.is_group:
        if not await can_change_info(message=event):
            return
        else:
            pass
    if is_nsfwatch_indb(str(event.chat_id)):
        await event.reply("`Bu Sohbet Nsfw İzlemeyi Zaten Etkinleştirdi.`")
        return
    add_nsfwatch(str(event.chat_id))
    await event.reply(f"**{event.chat_id} Kimlikli Sohbet {event.chat.title} Veritabanına Eklendi. Bu Gruplar Nsfw İçeriği Silinecek ve Günlük Grubuna Giriş Yapılacaktır**")

@register(pattern="^/rmnsfw ?(.*)")
async def disable_nsfw(event):
    if event.is_private:
       return   
    if event.is_group:
        if not await can_change_info(message=event):
            return
        else:
            pass
    if not is_nsfwatch_indb(str(event.chat_id)):
        await event.reply("Bu Sohbet Nsfw İzlemeyi Etkinleştirmedi.")
        return
    rmnsfwatch(str(event.chat_id))
    await event.reply(f"**{event.chat_id} Kimlikli {event.chat.title} Sohbet Nsfw Watch'tan Kaldırıldı**")
    
@bot.on(events.NewMessage())        
async def ws(event):
    warner_starkz = get_all_nsfw_enabled_chat()
    if len(warner_starkz) == 0:
        return
    if not is_nsfwatch_indb(str(event.chat_id)):
        return
    if not event.media:
        return
    if not (event.gif or event.video or event.video_note or event.photo or event.sticker):
        return
    hmmstark = await is_nsfw(event)
    his_id = event.sender_id
    if hmmstark is True:
        try:
            await event.delete()
            await event.client(EditBannedRequest(event.chat_id, his_id, MUTE_RIGHTS))
        except:
            pass
        lolchat = await event.get_chat()
        ctitle = event.chat.title
        if lolchat.username:
            hehe = lolchat.username
        else:
            hehe = event.chat_id
        wstark = await event.client.get_entity(his_id)
        if wstark.username:
            ujwal = wstark.username
        else:
            ujwal = wstark.id
        try:
            await tbot.send_message(event.chat_id, f"**#NSFW_WATCH** \n**Chat :** `{hehe}` \n**Nsfw Sender - User / Bot :** `{ujwal}` \n**Chat Title:** `{ctitle}`")  
            return
        except:
            return


__help__ = """
Grubu NSFW gönderenlerden koruyabilirim 
❍ /addnsfw*:* Grubu nsfw İzleme Listesine Ekler 
❍ /rmnsfw*:* Grubu NSFW İzleme Listesinden Kaldırır
"""

__mod_name__ = "NSFW"
