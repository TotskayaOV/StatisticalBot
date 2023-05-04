import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, db
from aiogram.types import Message




@dp.message_handler(commands=['show_us'])
async def delete_user(message: Message, admin: bool):
    if admin:
        temp_list = db.get_user()
        text_string = ''
        for i in range(len(temp_list)):
            text_string = text_string + str(temp_list[i][0]) + ' '\
                          + temp_list[i][1] + ' ' + temp_list[i][2] + '\n'
        await message.answer(text=text_string)
    else:
        await message.answer('У вас нет доступа к этой функции')
