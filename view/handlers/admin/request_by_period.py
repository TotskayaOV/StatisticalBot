from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from datetime import datetime

from loader import dp
from view.keyboards import kb_cancel_fsm, kb_yesno
from controller import read_wb_period


class PeriodDate(StatesGroup):
    begin_date = State()
    str_begin = State()
    end_date = State()
    str_end = State()

@dp.message_handler(commands=['period_date'], state=None)
async def add_user(message: Message, admin: bool):
    if admin:
        await message.answer(text='Напишите дату начала периода в формате 2023-01-31', reply_markup=kb_cancel_fsm)
        await PeriodDate.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=PeriodDate.begin_date)
async def general_date_catch(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        up_data = datetime.strptime(data_obj, '%Y-%m-%d')
        await state.update_data({'begin_date': up_data, 'str_begin': data_obj})
        await message.answer(text='Напишите дату окончания периода в формате 2023-01-31', reply_markup=kb_cancel_fsm)
        await PeriodDate.end_date.set()
    except:
        await message.answer(text='Ошибка ввода даты', reply_markup=kb_cancel_fsm)

@dp.message_handler(state=PeriodDate.end_date)
async def general_date_catch(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        up_data = datetime.strptime(data_obj, '%Y-%m-%d')
        await state.update_data({'end_date': up_data, 'str_end': data_obj})
        await message.answer(text='Даты введены верно?', reply_markup=kb_yesno)
        await PeriodDate.str_end.set()
    except:
        await message.answer(text='Ошибка ввода даты', reply_markup=kb_cancel_fsm)

@dp.message_handler(state=PeriodDate.str_end)
async def general_date_catch(message: Message, state: FSMContext):
    if message.text == 'Да':
        try:
            data = await state.get_data()
            result = read_wb_period({'name_beg_date': data.get('str_begin'), 'name_end_date': data.get('str_end'),
                                     'beg_date': data.get('begin_date'), 'end_date': data.get('end_date')})
            for str_elem in result:
                await message.answer(text=str_elem)
            await state.reset_data()
            await state.finish()
        except Exception as err:
            await message.answer(text=f'Ошибка: {err}')
            data = await state.get_data()
            await state.reset_data()
            await state.finish()
