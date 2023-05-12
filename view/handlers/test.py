from datetime import datetime, timedelta

from loader import dp, db
from aiogram.types import Message
from controller import summation_data_jira_call, summation_data_general_portal, read_wb_period


@dp.message_handler(commands=['test'])
async def mes_start(message: Message):
    # d1 = '2023-05-01'
    # d2 = '2023-05-10'
    # up_data = datetime.strptime(d1, '%Y-%m-%d')
    # dw_data = datetime.strptime(d2, '%Y-%m-%d')
    # result = summation_data_jira_call({'begin_period': up_data, 'end_period': dw_data, 'get_method': db.get_jira_sla})
    # print(result)
    # result2 = summation_data_jira_call({'begin_period': up_data, 'end_period': dw_data, 'get_method': db.get_jira_count})
    # print(result2)
    # result3 = summation_data_jira_call({'begin_period': up_data, 'end_period': dw_data, 'get_method': db.get_jira_time})
    # time_in_seconds = round(result3.get('time')/result3.get('count') * 60)
    # minutes, seconds = divmod(time_in_seconds, 60)
    # print("Время: {} мин. {} сек.".format(minutes, seconds))
    # print(result3)
    # result4 = summation_data_jira_call({'begin_period': up_data, 'end_period': dw_data, 'get_method': db.get_call})
    # print(result4)
    # result5 = summation_data_general_portal({'begin_period': up_data, 'end_period': dw_data})
    # print(result5)
    # read_wb_period({'name_beg_date': d1, 'name_end_date': d2, 'beg_date': up_data, 'end_date': dw_data})
    await message.answer(f'Привет,  😇')