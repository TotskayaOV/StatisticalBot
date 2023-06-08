import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, InputMediaPhoto, InputFile
from datetime import datetime

from loader import dp, admin_id
from view.keyboards import kb_cancel_fsm, kb_yesno, kb_yesno_inline, yesno_data, kb_name_files
from controller import read_user_wb_data
from creating_graphics import statistic_image_day


class UserStats(StatesGroup):
    user_date = State()
    all_task = State()


@dp.message_handler(commands=['result'], state=None)
async def add_user(message: Message, admin: bool, coordinator: bool):
    if admin or coordinator:
        await message.answer(text='Напишите дату в формате 2023-01-31', reply_markup=kb_cancel_fsm)
        await UserStats.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=UserStats.user_date, content_types=ContentTypes.ANY)
async def date_catch(message: Message, state: FSMContext):
    try:
        date_obj = message.text
        up_data = datetime.strptime(date_obj, '%Y-%m-%d')
        user_id = message.from_user.id
        text_mess = read_user_wb_data(date_obj, up_data, user_id)
        made_picture = statistic_image_day(date_obj)
        if made_picture is True:
            photo = InputFile(f"./cred/merged_images-{date_obj}.png")
            await dp.bot.send_photo(chat_id=message.chat.id, photo=photo,  caption=text_mess)
        else:
            await message.answer(text=text_mess)
            await state.reset_data()
            await state.finish()
    except:
        await message.answer(text='Ошибка ввода даты.\nНапишите дату в формате 2023-01-01',
                             reply_markup=kb_cancel_fsm)
        await UserStats.user_date.set()
    else:
        if os.path.isfile(f"./cred/merged_images-{date_obj}.png"):
            os.remove(f"./cred/merged_images-{date_obj}.png")
        if os.path.isfile(f'./cred/call-{date_obj}.jpg'):
            os.remove(f'./cred/call-{date_obj}.jpg')
        if os.path.isfile(f'./cred/count-{date_obj}.jpg'):
            os.remove(f'./cred/count-{date_obj}.jpg')
        if os.path.isfile(f'./cred/general-{date_obj}.jpg'):
            os.remove(f'./cred/general-{date_obj}.jpg')
        if os.path.isfile(f'./cred/portal-{date_obj}.jpg'):
            os.remove(f'./cred/portal-{date_obj}.jpg')
        if os.path.isfile(f'./cred/sla-{date_obj}.jpg'):
            os.remove(f'./cred/sla-{date_obj}.jpg')
        if os.path.isfile(f'./cred/time-{date_obj}.jpg'):
            os.remove(f'./cred/time-{date_obj}.jpg')
