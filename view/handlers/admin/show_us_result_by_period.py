from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, CallbackQuery
from datetime import datetime

from loader import dp, admin_id, db
from view.keyboards import kb_cancel_fsm, kb_yesno
from controller import read_user_period


class PeriodUserStats(StatesGroup):
    begin_date = State()
    str_begin = State()
    end_date = State()
    str_end = State()
    name = State()


@dp.message_handler(commands=['us_period'], state=None)
async def stats_user(message: Message, admin: bool):
    if admin or int(admin_id) == message.from_user.id:
        await message.answer(text='Напишите дату начала периода в формате 2023-01-31', reply_markup=kb_cancel_fsm)
        await PeriodUserStats.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=PeriodUserStats.begin_date)
async def general_date_catch(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        up_data = datetime.strptime(data_obj, '%Y-%m-%d')
        await state.update_data({'begin_date': up_data, 'str_begin': data_obj})
        await message.answer(text='Напишите дату окончания периода в формате 2023-01-31', reply_markup=kb_cancel_fsm)
        await PeriodUserStats.end_date.set()
    except:
        await message.answer(text='Ошибка ввода даты', reply_markup=kb_cancel_fsm)

@dp.message_handler(state=PeriodUserStats.end_date, content_types=ContentTypes.ANY)
async def u_date_catch(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        up_data = datetime.strptime(data_obj, '%Y-%m-%d')
        await state.update_data({'end_date': up_data, 'str_end': data_obj})
        await message.answer(text='Напишите фамилию', reply_markup=kb_cancel_fsm)
        await PeriodUserStats.name.set()
    except:
        await message.answer(text='Ошибка ввода даты')

@dp.message_handler(state=PeriodUserStats.name, content_types=ContentTypes.ANY)
async def uname_catch(message: Message, state: FSMContext):
    try:
        name = message.text
        upd_name = name.lower().title()
        tg_id = db.get_the_user(name=upd_name)[0]
        data = await state.get_data()
        text_list = read_user_period({'name_beg_date': data.get('str_begin'), 'name_end_date': data.get('str_end'),
                                     'beg_date': data.get('begin_date'), 'end_date': data.get('end_date'),
                                      'user_id': tg_id})
        await message.answer(text=text_list)
        await state.reset_data()
        await state.finish()
    except Exception as err:
        await message.answer(text=f'Ошибка: {err}')
        await state.reset_data()
        await state.finish()
