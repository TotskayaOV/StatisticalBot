from aiogram import executor
from view import dp
from loader import on_startup, on_shutdown
import middleware


async def on_start(_):
    print('Start Bot')


if __name__ == '__main__':
    middleware.setup(dp)
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown)
