from loader import db, dp
from controller import read_user_wb_data

async def get_mail_for_date(data_obj, date, coor_comment):
    all_user = db.get_user()
    for elem in all_user:
        if elem[2] == 'admin' or elem[2] == 'coordinator':
            text = read_user_wb_data(data_obj, date, elem[0]) + coor_comment
            await dp.bot.send_message(elem[0], text=text)

