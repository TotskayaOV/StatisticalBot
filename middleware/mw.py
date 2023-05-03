from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import db
class AddUserRole(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        try:
            my_set = db.get_the_user(id=message.from_user.id)
            user_role = list(my_set)[2]
            if user_role == 'admin':
                data['admin'] = True
            else:
                data['admin'] = False
            if user_role == 'coordinator':
                data['coordinator'] = True
            else:
                data['coordinator'] = False
        except:
            data['guest'] = True
            data['admin'] = False
            data['coordinator'] = False

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        try:
            my_set = db.get_the_user(id=call.message.chat.id)
            user_role = list(my_set)[2]
            if user_role == 'admin':
                data['admin'] = True
            else:
                data['admin'] = False
            if user_role == 'coordinator':
                data['coordinator'] = True
            else:
                data['coordinator'] = False
        except:
            data['guest'] = True
            data['admin'] = False
            data['coordinator'] = False
