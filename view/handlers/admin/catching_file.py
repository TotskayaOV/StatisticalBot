import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, Document, CallbackQuery
from datetime import datetime

from loader import dp, admin_id
from view.keyboards import kb_cancel_fsm, kb_yesno, kb_yesno_inline, yesno_data, kb_name_files
from controller import read_wb_data

from combining import update_wdb_portal, update_wdb_count_jira, update_wdb_sla_jira
from combining import update_wdb_time_jira, update_wdb_call, update_wdb_general


class NewFiles(StatesGroup):
    general_date = State()
    all_task = State()
    fast_task = State()
    next_step = State()
    next1_step = State()
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
        await message.answer(text='Напишите дату в формате 2023-01-31', reply_markup=kb_cancel_fsm)
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
    await message.answer(text='Выберите тип файла для загрузки или завершите ввод',
                         reply_markup=kb_name_files)
    await NewFiles.next_step.set()


@dp.message_handler(state=NewFiles.next_step, content_types=ContentTypes.ANY)
async def chose_next_step(message: Message, state: FSMContext):
    if message.text == 'Портал':
        await message.answer(text='Загрузите файл данных портала')
        await NewFiles.portal_file.set()
    elif message.text == 'Звонки':
        await message.answer(text='Загрузите файл данных звонков')
        await NewFiles.call_file.set()
    elif message.text == 'Кол-во JIRA':
        await message.answer(text='Загрузите файл данных количества выполненных заявок Jira')
        await NewFiles.count_file.set()
    elif message.text == 'SLA JIRA':
        await message.answer(text='Загрузите файл данных SLA выолнения заявок Jira')
        await NewFiles.sla_file.set()
    elif message.text == 'Time JIRA':
        await message.answer(text='Загрузите файл данных времени выолнения заявок Jira')
        await NewFiles.time_file.set()
    elif message.text == 'Завершить':
        await message.answer(text='Вы хотите завершить загрузку данных?', reply_markup=kb_yesno_inline)
        await NewFiles.yes_no.set()

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
        finally:
            data = await state.get_data()
            try:
                update_wdb_portal(data.get('general_date'))
            except Exception as err:
                await message.answer(text=f'Ошибка загрузки данных. Проверьте файл:'
                                          f'расширение, кодировку, формат данных. (Внимание, все ФИО указнные в файле'
                                          f' должны быть внесены в таблицу пользователей!) \n'
                                          f'Или передайте данные об ошибке: {err}')
                await state.reset_data()
                await state.finish()
            else:
                await message.answer(text='Данные загружены', reply_markup=kb_name_files)
            finally:
                try:
                    os.remove('./cred/portal.csv')
                    await NewFiles.next_step.set()
                except Exception as err:
                    await message.answer(text=f'Ошибка удаления файлов: {err}')
                    await state.reset_data()
                    await state.finish()

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
        finally:
            try:
                update_wdb_count_jira()
            except Exception as err:
                await message.answer(text=f'Ошибка загрузки данных. Проверьте файл:'
                                          f'расширение, кодировку, формат данных. \n'
                                          f'Или передайте данные об ошибке: {err}')
                await state.reset_data()
                await state.finish()
            else:
                await message.answer(text='Данные загружены', reply_markup=kb_name_files)
            finally:
                try:
                    os.remove('./cred/count_jira.csv')
                    await NewFiles.next_step.set()
                except Exception as err:
                    await message.answer(text=f'Ошибка удаления файлов: {err}')
                    await state.reset_data()
                    await state.finish()


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
        finally:
            try:
                update_wdb_sla_jira()
            except Exception as err:
                await message.answer(text=f'Ошибка загрузки данных. Проверьте файл:'
                                          f'расширение, кодировку, формат данных. \n'
                                          f'Или передайте данные об ошибке: {err}')
                await state.reset_data()
                await state.finish()
            else:
                await message.answer(text='Данные загружены', reply_markup=kb_name_files)
            finally:
                try:
                    os.remove('./cred/SLA_jira.csv')
                    await NewFiles.next_step.set()
                except Exception as err:
                    await message.answer(text=f'Ошибка удаления файлов: {err}')
                    await state.reset_data()
                    await state.finish()


@dp.message_handler(state=NewFiles.time_file, content_types=ContentTypes.ANY)
async def time_catch(message: Message, state: FSMContext):
    if document := message.document:
        await state.update_data({'time_file': True})
        await document.download(destination_file=f'./cred/{document.file_name}')
        try:
            os.rename(f'./cred/{document.file_name}', './cred/time_jira.csv')
        except:
            os.remove('./cred/time_jira.csv')
            os.rename(f'./cred/{document.file_name}', './cred/time_jira.csv')
        finally:
            try:
                update_wdb_time_jira()
            except Exception as err:
                await message.answer(text=f'Ошибка загрузки данных. Проверьте файл:'
                                          f'расширение, кодировку, формат данных. \n'
                                          f'Или передайте данные об ошибке: {err}')
                await state.reset_data()
                await state.finish()
            else:
                await message.answer(text='Данные загружены', reply_markup=kb_name_files)
            finally:
                try:
                    os.remove('./cred/time_jira.csv')
                    await NewFiles.next_step.set()
                except Exception as err:
                    await message.answer(text=f'Ошибка удаления файлов: {err}')
                    await state.reset_data()
                    await state.finish()


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
        finally:
            try:
                update_wdb_call()
            except Exception as err:
                await message.answer(text=f'Ошибка загрузки данных. Проверьте файл:'
                                          f'расширение, кодировку, формат данных. \n'
                                          f'Или передайте данные об ошибке: {err}')
                await state.reset_data()
                await state.finish()
            else:
                await message.answer(text='Данные загружены', reply_markup=kb_name_files)
            finally:
                try:
                    os.remove('./cred/call.csv')
                    await NewFiles.next_step.set()
                except Exception as err:
                    await message.answer(text=f'Ошибка удаления файлов: {err}')
                    await state.reset_data()
                    await state.finish()

@dp.callback_query_handler(yesno_data.filter(yes_no='no'), state=NewFiles.yes_no)
async def finish_catch(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.from_user.id
    await dp.bot.send_message(chat_id, text='Продолжите загрузку.', reply_markup=kb_name_files)
    await NewFiles.next_step.set()

@dp.callback_query_handler(yesno_data.filter(yes_no='yes'), state=NewFiles.yes_no)
async def finish_catch(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    update_wdb_general({'date': data.get('general_date'), 'new': data.get('all_task'),
                        'fast': data.get('fast_task')})
    chat_id = callback.from_user.id
    await dp.bot.send_message(chat_id, text='Показать результаты?', reply_markup=kb_yesno)
    await NewFiles.go_message.set()


@dp.message_handler(state=NewFiles.go_message)
# @dp.message_handler(content_types=ContentTypes.ANY)
async def finish_state(message: Message, state: FSMContext):
    if message.text in ['Да']:
        data = await state.get_data()
        up_data = data.get('general_date')
        data_obj = up_data.strftime('%d-%m-%Y')
        texr_result = read_wb_data(data_obj, up_data)
        await message.answer(text=texr_result)
        await state.reset_data()
        await state.finish()
    else:
        await message.answer(text='Ups')
        await state.reset_data()
        await state.finish()
