import os
from .send_messages import TelegramClient


def notify(chat_id: int, text: str):
    """
    Формирует http ссылку для отправки сообщения
    :param chat_id: id пользователя/чата которому будет отправлено сообщение
    :param text: сообщение
    """
    telegram_client = TelegramClient(token=os.getenv('TOKEN'), base_url='https://api.telegram.org')
    my_params = {"chat_id": chat_id, "text": text}
    telegram_client.post(method='sendMessage', params=my_params)

