from pyrogram.types import Message
from pyrogram import filters, errors, enums
from MyTgBot import bot
from pyrogram.errors.exceptions.flood_420 import FloodWait
from MyTgBot.database.db import add_user, add_group, all_users, all_groups, users, remove_user
import asyncio

@bot.on_message(filters.command(["stats", "users"], ["/", "!", ".", "?"]))
async def dbtool(_, m : Message):
    if m.from_user.id !=1666544436:
         return await m.reply_text("`You Don't Have Enough Rights To Run This!`")    
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)    
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)

@bot.on_message(filters.command(["bcast", "broadcast"], ["/", "!", "?", "."]))
async def bcast(_, m : Message):
    if m.from_user.id !=1666544436:
         return await m.reply_text("`You Don't Have Enough Rights To Run This!`")
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if not m.reply_to_message:
                await m.reply_text("`Reply message men`")
            if m.reply_to_message:
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅ Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

@bot.on_message(filters.command(["fcast", "forwardcast"], ["/", "?", "!", "."]))
async def fcast(_, m : Message):
    if m.from_user.id !=1666544436:
         return await m.reply_text("`You Don't Have Enough Rights To Run This!`")
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.reply_to_message:
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅ Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")
