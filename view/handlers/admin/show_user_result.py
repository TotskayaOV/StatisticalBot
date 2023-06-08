import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, CallbackQuery
from datetime import datetime

from loader import dp, admin_id, db
from view.keyboards import kb_cancel_fsm, kb_yesno
from controller import read_user_wb_data


class OneUserStats(StatesGroup):
    general_date = State()
    name = State()


@dp.message_handler(commands=['us_date'], state=None)
async def stats_user(message: Message, admin: bool):
    """
    Показать статистику пользователя за 1 день
    :param message:
    :param admin:
    :return:
    """
    if admin or int(admin_id) == message.from_user.id:
        await message.answer(text='Напишите дату в формате 2023-01-31', reply_markup=kb_cancel_fsm)
        await OneUserStats.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=OneUserStats.general_date, content_types=ContentTypes.ANY)
async def u_date_catch(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        up_data = datetime.strptime(data_obj, '%Y-%m-%d')
        await state.update_data({'general_date': up_data})
        await message.answer(text='Напишите фамилию', reply_markup=kb_cancel_fsm)
        await OneUserStats.next()
    except:
        await message.answer(text='Ошибка ввода даты')

@dp.message_handler(state=OneUserStats.name, content_types=ContentTypes.ANY)
async def uname_catch(message: Message, state: FSMContext):
    try:
        name = message.text
        upd_name = name.lower().title()
        tg_id = db.get_the_user(name=upd_name)[0]
        data = await state.get_data()
        data_obj = data.get('general_date').strftime('%d-%m-%Y')
        text = read_user_wb_data(data_obj, data.get('general_date'), tg_id)
        await message.answer(text=text)
        await state.reset_data()
        await state.finish()
    except Exception as err:
        await message.answer(text=f'Ошибка: {err}', reply_markup=kb_cancel_fsm)
        await state.reset_data()
        await state.finish()
