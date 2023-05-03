import os
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from modul import DataBase
from config import db_path
from sending_messages import notify


memory = MemoryStorage()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=memory)
db = DataBase(db_path=db_path)
log_id = os.getenv('LOG_ID')
admin_id = os.getenv('ADMIN_ID')


async def on_startup(_):
    notify(log_id, 'Bot started!')
    try:
        db.create_table_users()
        db.create_table_call()
        db.create_table_portal()
        db.create_table_jira_count()
        db.create_table_jira_sla()
        db.create_table_jira_time()
        db.create_table_general_data()
        notify(log_id, 'DataBase .... Ok!')
    except sqlite3.OperationalError:
        notify(log_id, 'DataBase .... фиг вам, а не датабаза')


async def on_shutdown(_):
    db.disconnect()
