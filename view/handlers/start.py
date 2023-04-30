from loader import dp
from aiogram.types import Message
from combining import update_wdb_portal, update_wdb_count_jira, update_wdb_sla_jira
from combining import update_wdb_time_jira, update_wdb_call



@dp.message_handler(commands=['start'])
async def mes_start(message: Message):
    user_id = message.from_user.id
    update_wdb_portal()
    update_wdb_count_jira()
    update_wdb_sla_jira()
    update_wdb_time_jira()
    update_wdb_call()
    await message.answer(f'Привет, твой id {user_id}. '
                         f'Передай его администратору для дальнейшей работы с ботом 😇')