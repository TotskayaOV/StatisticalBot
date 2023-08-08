import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, InputFile


from loader import dp
from view.keyboards import kb_cancel_fsm
from controller import difference_between_days


class TimesFiles(StatesGroup):
    times_file = State()

@dp.message_handler(commands=['days'], state=None)
async def add_user(message: Message, admin: bool):
    if admin:
        await message.answer(text='Загрузите файл данных времени изменения статусов на портале',
                             reply_markup=kb_cancel_fsm)
        await TimesFiles.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=TimesFiles.times_file, content_types=ContentTypes.ANY)
async def portal_catch(message: Message, state: FSMContext):
    if document := message.document:
        await state.update_data({'times_file': True})
        await document.download(destination_file=f'./cred/{document.file_name}')
        try:
            os.rename(f'./cred/{document.file_name}', './cred/differences.csv')
        except:
            os.remove('./cred/differences.csv')
            os.rename(f'./cred/{document.file_name}', './cred/differences.csv')
        finally:
            data = await state.get_data()
            try:
                result = difference_between_days()
                text = ''
                for date_keys, data_value in result.items():
                    text += f"{date_keys}\nМедиана: {round(data_value[0], 2)} минут" \
                           f"\nСредне арифметическое: {round(data_value[1], 2)} минут\n\n"
            except Exception as err:
                await message.answer(text=f'Ошибка загрузки данных. Проверьте файл:'
                                          f'расширение, кодировку, формат данных. \n'
                                          f'Или передайте данные об ошибке: {err}')
                await state.reset_data()
                await state.finish()
            else:
                with open('./cred/graph_day.jpg', 'rb') as photo:
                    await message.answer_photo(photo=photo, caption=text)
            finally:
                try:
                    os.remove('./cred/graph_day.jpg')
                    os.remove('./cred/differences.csv')
                    await state.reset_data()
                    await state.finish()
                except Exception as err:
                    await message.answer(text=f'Ошибка удаления файлов: {err}')
                    await state.reset_data()
                    await state.finish()
