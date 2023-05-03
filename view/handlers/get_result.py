import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, Document, CallbackQuery
from datetime import datetime

from loader import dp, admin_id
from view.keyboards import kb_cancel_fsm, kb_yesno, kb_yesno_inline, yesno_data, kb_name_files
from controller import read_user_wb_data


class UserStats(StatesGroup):
    user_date = State()
    all_task = State()


@dp.message_handler(commands=['result'], state=None)
async def add_user(message: Message, admin: bool, coordinator: bool):
    if admin or coordinator:
        await message.answer(text='Напишите дату в формате 2023-01-01', reply_markup=kb_cancel_fsm)
        await UserStats.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=UserStats.user_date, content_types=ContentTypes.ANY)
async def date_catch(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        up_data = datetime.strptime(data_obj, '%Y-%m-%d')
        user_id = message.from_user.id
        text_mess = read_user_wb_data(data_obj, up_data, user_id)
        await message.answer(text=text_mess)
        await state.reset_data()
        await state.finish()
    except:
        await message.answer(text='Ошибка ввода даты.\nНапишите дату в формате 2023-01-01',
                             reply_markup=kb_cancel_fsm)
        await UserStats.user_date.set()

