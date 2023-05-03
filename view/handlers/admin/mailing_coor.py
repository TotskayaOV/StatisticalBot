import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes
from datetime import datetime

from loader import dp, admin_id
from view.keyboards import kb_cancel_fsm
from controller import get_mail_for_date


class MailStats(StatesGroup):
    general_date = State()

@dp.message_handler(commands=['mail'], state=None)
async def add_user(message: Message, admin: bool):
    if admin or int(admin_id) == message.from_user.id:
        await message.answer(text='Напишите дату в формате 2023-01-01', reply_markup=kb_cancel_fsm)
        await MailStats.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=MailStats.general_date, content_types=ContentTypes.ANY)
async def general_date_catch(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        up_data = datetime.strptime(data_obj, '%Y-%m-%d')
        await state.update_data({'general_date': up_data})
        await get_mail_for_date(data_obj, up_data)
        await message.answer(text='Рассылка прошла успешно')
        await MailStats.next()
    except:
        await message.answer(text='Ошибка ввода даты')