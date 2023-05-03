import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, db
from aiogram.types import Message
from view.keyboards import kb_cancel_fsm


class DeleteUser(StatesGroup):
    user_id = State()


@dp.message_handler(commands=['del'], state=None)
async def delete_user(message: Message, admin: bool):
    if admin:
        await message.answer(text='Введите id', reply_markup=kb_cancel_fsm)
        await DeleteUser.user_id.set()
    else:
        await message.answer('У вас нет доступа к этой функции')


@dp.message_handler(state=DeleteUser.user_id)
async def id_user_catch(message: Message, state: FSMContext):
    await state.update_data({'user_id': message.text})
    data = await state.get_data()
    user_id = int(data.get('user_id'))
    try:
        db.remove_user(user_id)
        await message.answer(f"Пользователь {user_id} удален")
    except sqlite3.OperationalError:
        await message.answer("Ошибка удаления пользователя! Проверьте правильность вводимых данных")
    await state.reset_data()
    await state.finish()
