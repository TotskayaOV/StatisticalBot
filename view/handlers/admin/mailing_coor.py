import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, CallbackQuery
from datetime import datetime

from loader import dp, admin_id
from view.keyboards import kb_cancel_fsm, kb_yesno
from controller import get_mail_for_date


class MailStats(StatesGroup):
    general_date = State()
    yes_no = State()
    admin_comment = State()
    finish = State()

@dp.message_handler(commands=['mail'], state=None)
async def add_user(message: Message, admin: bool):
    if admin or int(admin_id) == message.from_user.id:
        await message.answer(text='Напишите дату в формате 2023-01-31', reply_markup=kb_cancel_fsm)
        await MailStats.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=MailStats.general_date, content_types=ContentTypes.ANY)
async def general_date_catch(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        up_data = datetime.strptime(data_obj, '%Y-%m-%d')
        await state.update_data({'general_date': up_data})
        await message.answer(text='Хотите написать комментарий к рассылке?', reply_markup=kb_yesno)
        await MailStats.yes_no.set()
    except:
        await message.answer(text='Ошибка ввода даты')

@dp.message_handler(state=MailStats.yes_no)
async def finish_state(message: Message, state: FSMContext):
    if message.text in ['Да']:
        await message.answer(text='Напишите комментарий')
        await MailStats.finish.set()
    else:
        try:
            data = await state.get_data()
            data_obj = data.get('general_date').strftime('%d-%m-%Y')
            await get_mail_for_date(data_obj, data.get('general_date'), '')
            await message.answer(text='Рассылка прошла успешно')
            await state.reset_data()
            await state.finish()
        except Exception as err:
            await message.answer(text=f'Рассылка не прошла. Ошибка {err}', reply_markup=kb_cancel_fsm)
            await state.reset_data()
            await state.finish()

@dp.message_handler(state=MailStats.finish, content_types=ContentTypes.ANY)
async def general_date_catch(message: Message, state: FSMContext):
    try:
        text1 = message.text
        comment = '\n' + text1
        data = await state.get_data()
        data_obj = data.get('general_date').strftime('%d-%m-%Y')
        await get_mail_for_date(data_obj, data.get('general_date'), comment)
        await message.answer(text='Рассылка прошла успешно')
        await MailStats.next()
    except Exception as err:
        await message.answer(text=f'Ошибка: {err}', reply_markup=kb_cancel_fsm)
        await state.reset_data()
        await state.finish()
