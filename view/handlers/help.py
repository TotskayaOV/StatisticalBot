from loader import dp
from aiogram.types import Message


@dp.message_handler(commands=['help'])
async def mes_start(message: Message, admin: bool, coordinator: bool):
    if admin:
        await message.answer(f'/new_user - добавить нового пользователя\n/upd_user - обновить роль пользователя\n'
                             f'/show_us - показать пользователей\n/del - удалить пользователя'
                             f' (нинада! лучше деактивировать)\n\n/add - загрузка файлов\n/gs_date - показать всю'
                             f' статистику за дату\n/us_date - показать статистику 1 пользователя за дату\n'
                             f'/period_date - показать полную статистику за период\n/pd_date - показать общую статистику'
                             f'за период\n/us_period - показать статистику пользователя за период\n'
                             f'/mail - рассылка всем активным пользователям\n\nиндивидуальные:\n'
                             f'/result - показать статистику за дату (частная)\n/start - старт\n\nна случай alarm:\n'
                             f'/del_count\t/del_sla\t/del_portal\t/del_count\t/del_time')
    elif coordinator:
        await message.answer(f'/result - посмотреть статистику за определенную дату. Дата вводится после запроса'
                             f'бота в формате год-месяц-день 🤓')
    else:
        await message.answer(f'Обратитесь за помощью к администратору')