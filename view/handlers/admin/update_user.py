import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, db, admin_id
from aiogram.types import Message
from view.keyboards import kb_cancel_fsm, kb_role_user


class UpdUser(StatesGroup):
    user_id = State()
    user_role = State()


@dp.message_handler(commands=['upd_user'], state=None)
async def upd_user(message: Message, admin: bool):
    if admin or int(admin_id) == message.from_user.id:
        await message.answer(text='Введите id (только цифры)', reply_markup=kb_cancel_fsm)
        await UpdUser.user_id.set()
    else:
        await message.answer('У вас нет доступа к этой функции')


@dp.message_handler(state=UpdUser.user_id)
async def user_id_up_catch(message: Message, state: FSMContext):
    await state.update_data({'user_id': message.text})
    await message.answer(text='Выберите роль пользователя', reply_markup=kb_role_user)
    await UpdUser.next()


@dp.message_handler(state=UpdUser.user_role)
async def name_catch(message: Message, state: FSMContext):
    if message.text in ['admin', 'coordinator', 'deactivated']:
        await state.update_data({'user_role': message.text})
        data = await state.get_data()
        try:
            db.update_user({'id': data.get('user_id'), 'role': data.get('user_role')})
            await message.answer(f"Пользователь {data.get('user_id')} изменен в роли на {data.get('user_role')}")
        except sqlite3.OperationalError:
            await message.answer("Ошибка добавления роли пользователю! Проверьте правильность вводимых данных")
        await state.reset_data()
        await state.finish()
    else:
        await message.answer(text='Выберите роль пользователя', reply_markup=kb_role_user)