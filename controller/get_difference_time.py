import polars as pl
from matplotlib import pyplot as plt

from xlsxwriter import Workbook

from modul import reade_between_time, processing_between_time
from creating_graphics import graph_differrence_time

def rewite_from_name_delta(number):
    if number <= 5: return '0-5'
    elif 5 < number <= 10: return '5-10'
    elif 10 < number <= 15: return '10-15'
    elif 15 < number <=20: return '15-20'
    else: return '20...'


def difference_between_time():
    """
    Формирует дата фрейм из из словаря от processing_between_time(). По дельте времени фильтрует в отдельные датафреймы
    для записи в эксель файл на разные листы
    Через polars.Series получаем медианное и среднеарифметическое значения.
    0 - 5 минут 90%
    5 - 10 минут 5%
    10 - 15 минут 3%
    15 - 20 минут 2%
    :return:
    """
    data_dict = processing_between_time(reade_between_time('./cred/difference.csv'))
    df = pl.DataFrame({
        'id_part': [v[0] for k, v in data_dict.items()],
        'up_time': [v[1] for k, v in data_dict.items()],
        'down_time': [v[2] for k, v in data_dict.items()],
        'delta': [v[3] for k, v in data_dict.items()],
    })
    df_4 = df.filter(pl.col('delta') <= 5).sort(pl.col('delta'), descending=True)
    df_9 = df.filter((pl.col('delta') < 10) & (pl.col('delta') > 5)).sort(pl.col('delta'), descending=True)
    df_14 = df.filter((pl.col('delta') < 15) & (pl.col('delta') > 10)).sort(pl.col('delta'), descending=True)
    df_19 = df.filter((pl.col('delta') < 20) & (pl.col('delta') > 15)).sort(pl.col('delta'), descending=True)
    df_21 = df.filter(20 < pl.col('delta')).sort(pl.col('delta'), descending=True)
    with Workbook("./cred/delta_exel.xlsx") as wb:
        df_4.write_excel(workbook=wb, worksheet='до 5', autofit=True)
        df_9.write_excel(workbook=wb, worksheet='5-10', autofit=True)
        df_14.write_excel(workbook=wb, worksheet='10-15', autofit=True)
        df_19.write_excel(workbook=wb, worksheet='15-20', autofit=True)
        df_21.write_excel(workbook=wb, worksheet='больше 20', autofit=True)
    series_delta = df.get_column('delta')
    period_list =[]
    for elem in series_delta.to_list():
        if elem <= 5: period_list.append('0-5')
        elif 5 < elem <= 10: period_list.append('5-10')
        elif 10 < elem <= 15: period_list.append('10-15')
        elif 15 < elem <= 20: period_list.append('15-20')
        else: period_list.append('20-...')
    data = [
        pl.Series("col1", series_delta, dtype=pl.Float32),
        pl.Series("col2", period_list, dtype=pl.Utf8),
    ]
    df = pl.DataFrame(data)
    df = df.groupby("col2", maintain_order=True).count().sort(pl.col('count'), descending=True)
    return graph_differrence_time(df, series_delta)
