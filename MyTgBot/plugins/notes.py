import json

from MyTgBot import bot
from MyTgBot.help.help_func import get_note_deatils, deserialize_inline_keyboard
from MyTgBot.database.notes_db import get_notes_list, add_note, get_note, delete_note, delete_all_note
from pyrogram import filters

right_format = 'Eg: `/save {notename} reply to text/media` or give text like `{notename} @CuteSerenaBot`'
exists = '**Note Name already exist.\nDelete and try again.**'
not_exists = 'No Notename Saved as `{}`.\nGet the list of notes by `/notes` command.'
added = '**Added!**: `{}`\nGet the note using `/get {}` or `/get num`'
no_notes = '**No Notes Saved in {}**'
get_note_eg = '**Example**:\n`/get {notename}`'
give_note_del = '**Provide note name to deleted**.'
deleted_note = 'Successfully deleted note `{}`.'
deleted_all = '**Successfully deleted all notes from {}**'

@bot.on_message(filters.command('get', ["/", "!", ".", "?"]))
async def get_notes(_, message):
      
      chat_id = message.chat.id     
      reply = message.reply_to_message
     
      if len(message.text.split()) < 2:
            return await message.reply(
                 get_note_eg
            )   
      else:
          note_name = message.text.split()[1].lower()
          note_data = await get_note(               
               name=note_name, chat_id=chat_id
          )
          if not note_data:
                return await message.reply(
                      not_exists.format(note_name)
                )
          note = note_data[0]
          type = note.get('type', '')
          file_id = note.get('file_id', '')
          caption = note.get('caption', None)
          keyboard = None
          keyboard_json = note.get('keyboard', None)
          if keyboard_json:
              serialized_keyboard = json.loads(keyboard_json)
              keyboard = deserialize_inline_keyboard(serialized_keyboard)
          
          text = note.get('text', '')        

          if type == '#STICKER':
               reply_func = reply.reply_sticker if reply else message.reply_sticker
               return await reply_func(
                     sticker=file_id, reply_markup=keyboard
               )
          
          elif type == '#AUDIO':
               reply_func = reply.reply_audio if reply else message.reply_audio
               return await reply_func(
                    audio=file_id,  caption=caption, reply_markup=keyboard
               )

          elif type == '#PHOTO':
               reply_func = reply.reply_photo if reply else message.reply_photo
               return await reply_func(
                    photo=file_id,  caption=caption, reply_markup=keyboard
               )
               
          elif type == '#TEXT':
                reply_func = reply.reply_text if reply else message.reply_text
                return await reply_func(
                     text=text, reply_markup=keyboard
                )
               
          elif type == '#ANIMATION':
                reply_func = reply.reply_animation if reply else message.reply_animation
                return await reply_func(
                     animation=file_id,   caption=caption, reply_markup=keyboard
                )
               
          elif type == '#DOCUMENT':
                reply_func = reply.reply_document if reply else message.reply_document
                return await reply_func(
                     document=file_id,  caption=caption, reply_markup=keyboard
                )
               
          elif type == '#VIDEO':
                reply_func = reply.reply_video if reply else message.reply_video
                return await reply_func(
                     video=file_id, caption=caption, reply_markup=keyboard
                )
          try: await message.delete();
          except: pass
           

@bot.on_message(filters.command('clear', ["/", "!", ".", "?"]))
async def clear_note(_, message):
     chat_id = message.chat.id
     if len(message.text.split()) < 2:
          return await message.reply(
              give_note_del
          )
     else:
          note_name = message.text.split()[1].lower()
          notes = await get_notes_list(chat_id)
          if (not notes is None) and (note_name in notes):
              await delete_note(note_name, chat_id)
              return await message.reply(
                  deleted_note.format(note_name)
              )
          else:
             return await message.reply(
                 not_exists.format(note_name)
)


@bot.on_message(filters.command(['rallnote', 'removeallnote'], ["/", "!", ".", "?"]))
async def delete_chat_notes(_, message):
       chat_id = message.chat.id
       chat_name = message.chat.title if message.chat.title else message.chat.first_name
  
       bot = await delete_all_note(chat_id)
       if bot:
             return await message.reply(
                   deleted_all.format(chat_name)
             )
       else:
             return await message.reply(
                   no_notes.format(chat_name)
             )

     
@bot.on_message(filters.command('notes', ["/", "!", ".", "?"]))
async def get_note_list(_, message):
      chat_id = message.chat.id
      chat_name = message.chat.title if message.chat.title else message.chat.first_name
            
      list = await get_notes_list(chat_id)
      if list is None:
            return await message.reply(
                  no_notes.format(chat_name)
            )                  
      text = f'**Here The List Of Notes In {chat_name}:\n\n**'
      if not list is None:
            for i, name in enumerate(list):
                  text += f'{i+1}, `{name}`\n'
      text += '\nYou can get access the notes by using `/get {notename}`'
      return await message.reply(text)


@bot.on_message(filters.command('save', ["/", "?", ".", "!"]))
async def save_note(_, message):      
     chat_id = message.chat.id
     reply = message.reply_to_message
  
     if not reply:
         if len(message.text.split()) <= 2:
             return await message.reply(
                  right_format
             )
     elif reply:
          if len(message.text.split()) < 2:
              return await message.reply(
                 right_format
              )
     try:
        note = await get_note_deatils(message)
     except Exception as e:
          return await message.reply(
               str(e)
          )
               
     note_name = note['name']
     length = len(await get_notes_list(chat_id)) if await get_notes_list(chat_id) is not None else 0
     available_num = [i + 1 for i in range(length)]
     if note_name.isdigit():
           return await message.reply(
                 "**Hello, sorry you can't store note by digits because you are accessing notes by its number** `/get 1`"
           )
      
     notes_list = await get_notes_list(chat_id)
     if (not notes_list is None) and (note_name in notes_list):
          return await message.reply(
                 exists
          )
     else:
           await add_note(
                chat_id=chat_id, 
                data=note
           )
           return await message.reply(
                added.format(note_name, note_name)
           )
