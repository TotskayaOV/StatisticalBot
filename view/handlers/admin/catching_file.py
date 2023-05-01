import sqlite3
import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, Document
from datetime import datetime

from loader import dp, admin_id
from view.keyboards import kb_cancel_fsm, kb_yesno

from combining import update_wdb_portal, update_wdb_count_jira, update_wdb_sla_jira
from combining import update_wdb_time_jira, update_wdb_call, update_wdb_general


class NewFiles(StatesGroup):
    general_date = State()
    all_task = State()
    fast_task = State()
    portal_file = State()
    count_file = State()
    sla_file = State()
    time_file = State()
    call_file = State()
    yes_no = State()
    go_message = State()


@dp.message_handler(commands=['add'], state=None)
async def add_user(message: Message, admin: bool):
    if admin or int(admin_id) == message.from_user.id:
        await message.answer(text='Напишите дату в формате 2023-01-01', reply_markup=kb_cancel_fsm)
        await NewFiles.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=NewFiles.general_date, content_types=ContentTypes.ANY)
async def general_date_catch(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        up_data = datetime.strptime(data_obj, '%Y-%m-%d')
        await state.update_data({'general_date': up_data})
        await message.answer(text='Введите количество новых анкет')
        await NewFiles.next()
    except:
        await message.answer(text='Ошибка ввода даты')
@dp.message_handler(state=NewFiles.all_task, content_types=ContentTypes.ANY)
async def all_task_catch(message: Message, state: FSMContext):
        await state.update_data({'all_task': message.text})
        await message.answer(text='Введите количество верифицированных за 15 минут')
        await NewFiles.next()

@dp.message_handler(state=NewFiles.fast_task, content_types=ContentTypes.ANY)
async def all_task_catch(message: Message, state: FSMContext):
        await state.update_data({'fast_task': message.text})
        await message.answer(text='Загрузите файл данных портала')
        await NewFiles.next()

@dp.message_handler(state=NewFiles.portal_file, content_types=ContentTypes.ANY)
async def portal_catch(message: Message, state: FSMContext):
    if document := message.document:
        await state.update_data({'portal_file': True})
        await document.download(destination_file=f'./cred/{document.file_name}')
        try:
            os.rename(f'./cred/{document.file_name}', './cred/portal.csv')
        except:
            os.remove('./cred/portal.csv')
            os.rename(f'./cred/{document.file_name}', './cred/portal.csv')
        await message.answer(text='Загрузите файл количества Jira')
        await NewFiles.next()
    else:
        await message.answer(text='Ups', reply_markup=kb_cancel_fsm)

@dp.message_handler(state=NewFiles.count_file, content_types=ContentTypes.ANY)
async def count_catch(message: Message, state: FSMContext):
    if document := message.document:
        await state.update_data({'count_file': True})
        await document.download(destination_file=f'./cred/{document.file_name}')
        try:
            os.rename(f'./cred/{document.file_name}', './cred/count_jira.csv')
        except:
            os.remove('./cred/count_jira.csv')
            os.rename(f'./cred/{document.file_name}', './cred/count_jira.csv')
        await message.answer(text='Выберите файл SLA')
        await NewFiles.next()
    else:
        await message.answer(text='Ups', reply_markup=kb_cancel_fsm)

@dp.message_handler(state=NewFiles.sla_file, content_types=ContentTypes.ANY)
async def sla_catch(message: Message, state: FSMContext):
    if document := message.document:
        await state.update_data({'sla_file': True})
        await document.download(destination_file=f'./cred/{document.file_name}')
        try:
            os.rename(f'./cred/{document.file_name}', './cred/SLA_jira.csv')
        except:
            os.remove('./cred/SLA_jira.csv')
            os.rename(f'./cred/{document.file_name}', './cred/SLA_jira.csv')
        await message.answer(text='Загрузите файл времени JIRA')
        await NewFiles.next()
    else:
        await message.answer(text='Ups', reply_markup=kb_cancel_fsm)

@dp.message_handler(state=NewFiles.time_file, content_types=ContentTypes.ANY)
async def sla_catch(message: Message, state: FSMContext):
    if document := message.document:
        await state.update_data({'time_file': True})
        await document.download(destination_file=f'./cred/{document.file_name}')
        try:
            os.rename(f'./cred/{document.file_name}', './cred/time_jira.csv')
        except:
            os.remove('./cred/time_jira.csv')
            os.rename(f'./cred/{document.file_name}', './cred/time_jira.csv')
        await message.answer(text='Загрузите файл звонков')
        await NewFiles.next()
    else:
        await message.answer(text='Ups', reply_markup=kb_cancel_fsm)


@dp.message_handler(state=NewFiles.call_file, content_types=ContentTypes.ANY)
async def call_catch(message: Message, state: FSMContext):
    if document := message.document:
        await state.update_data({'call_file': True})
        await document.download(destination_file=f'./cred/{document.file_name}')
        try:
            os.rename(f'./cred/{document.file_name}', './cred/call.csv')
        except:
            os.remove('./cred/call.csv')
            os.rename(f'./cred/{document.file_name}', './cred/call.csv')
        await message.answer(text='Все файлы загружены.\n⛔️ПРОВЕРЬТЕ ВЕРНО ЛИ ЗАГРУЖЕНЫ ФАЙЛЫ⛔️\n'
                                  'Обновить базу данных? ', reply_markup=kb_yesno)
        await NewFiles.next()
    else:
        await message.answer(text='Ups', reply_markup=kb_cancel_fsm)


@dp.message_handler(state=NewFiles.yes_no)
# @dp.message_handler(content_types=ContentTypes.ANY)
async def finish_catch(message: Message, state: FSMContext):
    if message.text in ['yes']:
        data = await state.get_data()
        update_wdb_portal(data.get('general_date'))
        update_wdb_time_jira()
        update_wdb_sla_jira()
        update_wdb_call()
        update_wdb_count_jira()
        print('done4')
        update_wdb_general({'date': data.get('general_date'), 'new': data.get('all_task'),
                            'fast': data.get('fast_task')})
        await message.answer(text='Отправить результаты координаторам за вчерашний день?', reply_markup=kb_yesno)
    else:
        await message.answer(text='Ups', reply_markup=kb_cancel_fsm)
        # await state.reset_data()
        # await state.finish()

# @dp.message_handler(state=NewFiles.sla_file, content_types=ContentTypes.ANY)
# @dp.message_handler(content_types=ContentTypes.ANY)
# async def sla_catch(message: Message, state: FSMContext):
#     if document := message.document:
#         print('done3')
#         await state.update_data({'sla_file': document.file_name})
#         await message.answer(text='Выберите роль пользователя', reply_markup=kb_cancel_fsm)
#         await NewFiles.next()
#         # await document.download(destination_file=f'{document.file_name}')
#         # await state.reset_data()
#         # await state.finish()
#     else:
#         # await state.update_data({'user_id': message.text})
#         await message.answer(text='Ups', reply_markup=kb_cancel_fsm)
        # await NewUser.next()




# @dp.message_handler(state=NewUser.name)
# async def name_catch(message: Message, state: FSMContext):
#     await state.update_data({'name': message.text})
#     await message.answer(text='Выберите роль пользователя', reply_markup=kb_role_user)
#     await NewUser.next()
#
#
# @dp.message_handler(state=NewUser.user_role)
# async def name_catch(message: Message, state: FSMContext):
#     if message.text in ['admin', 'coordinator', 'divisional_mentor']:
#         await state.update_data({'user_role': message.text})
#         data = await state.get_data()
#         try:
#             db.add_user_access(data)
#             await message.answer(f"Пользователь {data.get('name')} в роли {data.get('user_role')} успешно добавлен")
#         except sqlite3.OperationalError:
#             await message.answer("Ошибка добавления пользователя! Проверьте правильность вводимых данных")
#         await state.reset_data()
#         await state.finish()
#     else:
#         await message.answer(text='Выберите роль пользователя', reply_markup=kb_role_user)
