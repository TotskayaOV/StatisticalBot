import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, InputFile


from loader import dp
from view.keyboards import kb_cancel_fsm
from controller import difference_between_time


class TimeFiles(StatesGroup):
    time_file = State()

@dp.message_handler(commands=['time'], state=None)
async def add_user(message: Message, admin: bool):
    if admin:
        await message.answer(text='Загрузите файл данных времени изменения статусов на портале',
                             reply_markup=kb_cancel_fsm)
        await TimeFiles.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=TimeFiles.time_file, content_types=ContentTypes.ANY)
async def portal_catch(message: Message, state: FSMContext):
    if document := message.document:
        await state.update_data({'time_file': True})
        await document.download(destination_file=f'./cred/{document.file_name}')
        try:
            os.rename(f'./cred/{document.file_name}', './cred/difference.csv')
        except:
            os.remove('./cred/difference.csv')
            os.rename(f'./cred/{document.file_name}', './cred/difference.csv')
        finally:
            data = await state.get_data()
            try:
                result = difference_between_time()
                text = f"Медиана: {round(result.get('median'), 2)} минут" \
                   f"\nСредне арифметическое: {round(result.get('mean'), 2)} минут"
            except Exception as err:
                await message.answer(text=f'Ошибка загрузки данных. Проверьте файл:'
                                          f'расширение, кодировку, формат данных. (Внимание, все ФИО указнные в файле'
                                          f' должны быть внесены в таблицу пользователей!) \n'
                                          f'Или передайте данные об ошибке: {err}')
                await state.reset_data()
                await state.finish()
            else:
                with open('./cred/dif_dashboard.png', 'rb') as photo:
                    await message.answer_photo(photo=photo, caption=text)
                await message.answer_document(InputFile('./cred/delta_exel.xlsx'))
            finally:
                try:
                    os.remove('./cred/bar.jpg')
                    os.remove('./cred/boxplot.jpg')
                    os.remove('./cred/pie.jpg')
                    os.remove('./cred/dif_dashboard.png')
                    os.remove('./cred/delta_exel.xlsx')
                    os.remove('./cred/difference.csv')
                    await state.reset_data()
                    await state.finish()
                except Exception as err:
                    await message.answer(text=f'Ошибка удаления файлов: {err}')
                    await state.reset_data()
                    await state.finish()
