from typing import Type
from main import *
from aiogram import Bot, Dispatcher, executor, types
import config

"""Закреп сообщения"""
@dp.message_handler(commands=['pin'])
async def pin(message: types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    
    if member.is_chat_admin() != True:
            await message.answer("У вас нет прав для этого действия")
    else:
        txt = message.text.replace("/pin ", "")
        await message.pin(disable_notification=True)




"""Добавление запрещённого слова"""
@dp.message_handler(commands=['banword'])
async def newBanWord(message: types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)

    if member.is_chat_admin() != True:
        await message.answer("У вас нет прав для этого действия")
    else:
        word = message.text.replace("/banword ", "")
        cursor.execute(f"""INSERT INTO banWords
                  VALUES ('{word}')"""
               )
        conn.commit()
        await message.answer("Слово `" + word + "' добавлено в чёрный список")




"""Добавления юзера в белый список"""
@dp.message_handler(commands=['notdel'])
async def notban(message: types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)

    if member.is_chat_admin() != True:
        await message.answer("У вас нет прав для этого действия")
    else:
        config.notBanned.append(message.text.replace("/notdel ", "").replace("@", ""))
        await message.answer("У пользователя '" + message.text.replace("/notdel ", "").replace("@", "") + "' не будут удаляться запрещённые сообщения")



"""Очистка сообщений по слову"""
@dp.message_handler(commands=['delword'])
async def delword(message: types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    
    if member.is_chat_admin() != True:
        await message.answer("У вас нет прав для этого действия")
    
    else:
        word = message.text.replace('/delword ', "").lower()

        await message.answer("Слово '" + word + "' добавлено в чёрный список и сообщения, включающие это слово удалены")

        cursor.execute(f"""INSERT INTO banWords
                  VALUES ('{word}')"""
               )
        conn.commit()

        sql = f"SELECT * FROM messages WHERE text LIKE '%{word}%'"
        cursor.execute(sql)
        messages = cursor.fetchall()

        for msg in messages:
            print(msg)
            await bot.delete_message(msg[0], msg[1])



@dp.message_handler(commands=['ban'])
async def ban(message: types.Message):
    banned = message.reply_to_message.from_user.id
    config.banned.append(banned)
    await bot.ban_chat_member(message.chat.id, banned)
    await message.answer("Пользователь '" + str(message.reply_to_message.from_user.username) + "' идёт нахуй навсегда")



@dp.message_handler()
async def lol(message: types.Message):
    word = message.text.split(' ')
    member = message.from_user.id
    
    if member in config.banned:
        await bot.ban_chat_member(message.chat.id, member)
    
    for w in word:
        sql = f"SELECT * FROM banWords WHERE word LIKE '%{w}%'"
        cursor.execute(sql)
        messages = cursor.fetchone()
        print(messages)
        if messages:
            if(message.from_user.username in config.notBanned):
                pass
            else:
                if(w == messages[0]):
                    await message.delete()
                else:
                    pass
        else:
            cursor.execute(f"""INSERT INTO messages
                  VALUES ({message.chat.id}, {message.message_id}, '{message.text.lower()}')"""
               )
            conn.commit()


@dp.message_handler(content_types = ['new_chat_members', 'left_chat_member'])
async def delete(message: types.Message):
    members = message.new_chat_members
    for mem in members:
        if mem.id in config.banned:
            await bot.ban_chat_member(message.chat.id, mem.id)
    await message.delete()