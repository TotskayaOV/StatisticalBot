from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from datetime import datetime

from loader import dp, db
from view.keyboards import kb_cancel_fsm


class DelSla(StatesGroup):
    general_date = State()

@dp.message_handler(commands=['del_sla'], state=None)
async def add_user(message: Message, admin: bool):
    if admin:
        await message.answer(text='Напишите дату в формате 2023-01-01', reply_markup=kb_cancel_fsm)
        await DelSla.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=DelSla.general_date)
async def general_date_catch(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        up_data = datetime.strptime(data_obj, '%Y-%m-%d')
        db.remove_sla(up_data)
        await message.answer(text=f'данные SLA за {data_obj} удалены')
        await state.reset_data()
        await state.finish()
    except:
        await message.answer(text='Ошибка ввода даты', reply_markup=kb_cancel_fsm)
