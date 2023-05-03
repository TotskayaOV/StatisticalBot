import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, db, admin_id
from aiogram.types import Message
from view.keyboards import kb_cancel_fsm, kb_role_user


class NewUser(StatesGroup):
    user_id = State()
    name = State()
    user_role = State()


@dp.message_handler(commands=['new_user'], state=None)
async def add_user(message: Message, admin: bool):
    if admin or int(admin_id) == message.from_user.id:
        await message.answer(text='Введите id (только цифры)', reply_markup=kb_cancel_fsm)
        await NewUser.user_id.set()
    else:
        await message.answer('У вас нет доступа к этой функции')


@dp.message_handler(state=NewUser.user_id)
async def id_catch(message: Message, state: FSMContext):
    if db.get_user_access(user_id=message.text):
        await message.answer("Ошибка добавления пользователя!\n"
                             "Данный id уже зарегистрирован в системе", reply_markup=kb_cancel_fsm)
        await state.reset_data()
        await state.finish()
    else:
        await state.update_data({'user_id': message.text})
        await message.answer(text='Введите Фамилию', reply_markup=kb_cancel_fsm)
        await NewUser.next()


@dp.message_handler(state=NewUser.name)
async def name_catch(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await message.answer(text='Выберите роль пользователя', reply_markup=kb_role_user)
    await NewUser.next()


@dp.message_handler(state=NewUser.user_role)
async def name_catch(message: Message, state: FSMContext):
    if message.text in ['admin', 'coordinator', 'deactivated']:
        await state.update_data({'user_role': message.text})
        data = await state.get_data()
        try:
            db.add_user_access(data)
            await message.answer(f"Пользователь {data.get('name')} в роли {data.get('user_role')} успешно добавлен")
        except sqlite3.OperationalError:
            await message.answer("Ошибка добавления пользователя! Проверьте правильность вводимых данных")
        await state.reset_data()
        await state.finish()
    else:
        await message.answer(text='Выберите роль пользователя', reply_markup=kb_role_user)