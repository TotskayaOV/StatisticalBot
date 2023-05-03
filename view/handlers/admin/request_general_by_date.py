from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from datetime import datetime

from loader import dp
from view.keyboards import kb_cancel_fsm
from controller import read_wb_data


class StatsDate(StatesGroup):
    general_date = State()

@dp.message_handler(commands=['gs_date'], state=None)
async def add_user(message: Message, admin: bool):
    if admin:
        await message.answer(text='Напишите дату в формате 2023-01-01', reply_markup=kb_cancel_fsm)
        await StatsDate.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=StatsDate.general_date)
async def general_date_catch(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        up_data = datetime.strptime(data_obj, '%Y-%m-%d')
        text_result = read_wb_data(data_obj, up_data)
        await message.answer(text=text_result)
        await state.reset_data()
        await state.finish()
    except:
        await message.answer(text='Ошибка ввода даты', reply_markup=kb_cancel_fsm)
