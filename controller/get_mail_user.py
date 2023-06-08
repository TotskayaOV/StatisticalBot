from aiogram.types import InputFile
import os

from loader import db, dp
from controller import read_user_wb_data
from creating_graphics import statistic_image_day

async def get_mail_for_date(date_obj, date, coor_comment):
    all_user = db.get_user()
    made_picture = statistic_image_day(date.strftime('%Y-%m-%d'))
    if made_picture is True:
        picture_date = date.strftime('%Y-%m-%d')
        for elem in all_user:
            if elem[2] == 'admin' or elem[2] == 'coordinator':
                photo = InputFile(f"./cred/merged_images-{picture_date}.png")
                text = read_user_wb_data(date_obj, date, elem[0]) + coor_comment
                await dp.bot.send_photo(chat_id=elem[0], photo=photo,  caption=text)
        if os.path.isfile(f"./cred/merged_images-{picture_date}.png"):
            os.remove(f"./cred/merged_images-{picture_date}.png")
        if os.path.isfile(f'./cred/call-{picture_date}.jpg'):
            os.remove(f'./cred/call-{picture_date}.jpg')
        if os.path.isfile(f'./cred/count-{picture_date}.jpg'):
            os.remove(f'./cred/count-{picture_date}.jpg')
        if os.path.isfile(f'./cred/general-{picture_date}.jpg'):
            os.remove(f'./cred/general-{picture_date}.jpg')
        if os.path.isfile(f'./cred/portal-{picture_date}.jpg'):
            os.remove(f'./cred/portal-{picture_date}.jpg')
        if os.path.isfile(f'./cred/sla-{picture_date}.jpg'):
            os.remove(f'./cred/sla-{picture_date}.jpg')
        if os.path.isfile(f'./cred/time-{picture_date}.jpg'):
            os.remove(f'./cred/time-{picture_date}.jpg')
    else:
        for elem in all_user:
            if elem[2] == 'admin' or elem[2] == 'coordinator':
                text = read_user_wb_data(date_obj, date, elem[0]) + coor_comment
                await dp.bot.send_message(elem[0], text=text)

