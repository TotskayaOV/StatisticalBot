from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from datetime import datetime

from loader import dp, db
from view.keyboards import kb_cancel_fsm


class CallDate(StatesGroup):
    general_date = State()

@dp.message_handler(commands=['call_date'], state=None)
async def add_user(message: Message, admin: bool):
    if admin:
        await message.answer(text='Напишите дату в формате 2023-01-01', reply_markup=kb_cancel_fsm)
        await CallDate.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=CallDate.general_date)
async def general_date_catch(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        up_data = datetime.strptime(data_obj, '%Y-%m-%d')
        temp_list = db.get_call(date=up_data)
        text_str = ''
        if temp_list:
            for i in range(len(temp_list)):
                text_str = text_str + str(temp_list[i][0]) + ' ' + str(temp_list[i][2]) + ' ' + str(temp_list[i][3]) + '\n'
        await message.answer(text=text_str)
        await state.reset_data()
        await state.finish()
    except:
        await message.answer(text='Ошибка ввода даты', reply_markup=kb_cancel_fsm)

