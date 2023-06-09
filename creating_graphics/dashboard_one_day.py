from matplotlib import pyplot as plt
import polars as pl
import mplcyberpunk
from datetime import datetime
from PIL import Image
import numpy as np

from loader import db

def save_one_image(result_list: list, date_obj: str):
    """
    Image.new('RGB', (ширина, высота, (фон))
    :return: boolean:
                True - файл с данными создан
                False - данных за дату нет
    """
    file_label = ['count', 'sla', 'time', 'call', 'general', 'portal']
    check_size = sum(result_list)
    if check_size:
        for i in range(len(result_list)):
            if result_list[i] == 1:
                img_ch = Image.open(f'./cred/{file_label[i]}-{date_obj}.jpg')
                img_size = img_ch.size
        if check_size == 1:
            new_im = Image.new('RGB', (img_size[0], img_size[1]), (0, 0, 0))
            new_im.paste(img_ch, (0, 0))
        elif check_size == 4 or check_size == 2:
            new_im = Image.new('RGB', (2 * img_size[0], check_size//2 * img_size[1]), (0, 0, 0))
            param2 = 0
            for i in range(len(result_list)):
                if result_list[i] == 1:
                    img_ran = Image.open(f'./cred/{file_label[i]}-{date_obj}.jpg')
                    if param2 < 2:
                        new_im.paste(img_ran, (img_size[0] * param2, 0))
                        param2 +=1
                    else:
                        new_im.paste(img_ran, (img_size[0] * (param2//3), img_size[1]))
                        param2 += 1
        else:
            new_im = Image.new('RGB', (3 * img_size[0], check_size//3 * img_size[1]), (0, 0, 0))
            param2 = 1
            for i in range(len(result_list)):
                if result_list[i] == 1:
                    img_ran = Image.open(f'./cred/{file_label[i]}-{date_obj}.jpg')
                    if param2 < 3:
                        new_im.paste(img_ran, (img_size[0] * (param2 // 2), 0))
                        param2 += 1
                    elif param2 == 3:
                        new_im.paste(img_ran, (img_size[0] * 2, 0))
                        param2 += 1
                    else:
                        new_im.paste(img_ran, (img_size[0] * (param2 // 5), img_size[1]))
                        param2 += 4
        new_im.save(f"./cred/merged_images-{date_obj}.png", "PNG")
        return True
    else:
        return False


def created_bar(db_method, colors: list, t_label: str, f_label: str,
                date_obj: str,  check_autoresponder=False, right_position=False):
    """
    ВНИМАНИЕ в методе .filter() исключается общий показатель по группе. см. по id в users
    check_autoresponder - boolean - нужен для данных JIRA, чтобы исключить автоматически закрытые заявки
    right_position - отображение оси y (False - слева, True - справа)
    :return: boolean:
                True - файл с данными создан
                False - данных за дату нет
    """
    plt.style.use("cyberpunk")
    data_user = db.get_user()
    pl_user = pl.DataFrame({
        'id': [row[0] for row in data_user],
        'name': [row[1] for row in data_user],
    })
    data_request = db_method(date=datetime.strptime(date_obj, '%Y-%m-%d'))
    if data_request:
        pl_request = pl.DataFrame({
            'date': [row[1][:10] for row in data_request],
            'user': [row[2] for row in data_request],
            'value': [row[3] for row in data_request],
        })
        pl_request = pl_request.filter(pl.col('user') != 111121)
        if check_autoresponder:
            data_check = db.get_jira_sla(date=datetime.strptime(date_obj, '%Y-%m-%d'))
            pl_check = pl.DataFrame({
                'user': [row[2] for row in data_check],
            })
            pl_request = pl_request.join(pl_check, left_on="user", right_on='user', how="inner")
        df_inn = pl_request.join(pl_user, left_on="user", right_on='id', how="inner")
        df_inn = df_inn.sort('value', descending=True)
        fig, ax = plt.subplots(figsize=(5, 5), layout='constrained')
        bars = ax.bar(df_inn['name'], df_inn['value'], color=colors, zorder=2)
        plt.xticks(rotation=90)
        if right_position:
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
        plt.title(t_label, fontsize=17)
        mplcyberpunk.add_bar_gradient(bars=bars)
        plt.savefig(f'./cred/{f_label}-{date_obj}.jpg')
        plt.close('all')
        return 1
    else:
        return 0

def horizontal_bar(date_obj):
    plt.style.use("cyberpunk")
    data_user = db.get_user()
    pl_user = pl.DataFrame({
        'id': [row[0] for row in data_user],
        'name': [row[1] for row in data_user],
    })
    data_request = db.get_jira_sla(date=datetime.strptime(date_obj, '%Y-%m-%d'))
    if data_request:
        pl_request = pl.DataFrame({
            'date': [row[1][:10] for row in data_request],
            'user': [row[2] for row in data_request],
            'value': [row[3] for row in data_request],
        })
        pl_request = pl_request.filter(pl.col('user') != 111121)
        df_inn = pl_request.join(pl_user, left_on="user", right_on='id', how="inner")
        df_inn = df_inn.sort('value', descending=True)
        fig, ax = plt.subplots(figsize=(5, 5), layout='constrained')
        bars = ax.barh(df_inn['name'], df_inn['value'], color='green', zorder=2)
        bars1 = ax.barh(df_inn['name'], 1, color='orange', zorder=2)
        plt.xticks(rotation=90)
        plt.title('SLA', fontsize=17)
        mplcyberpunk.add_bar_gradient(bars=bars1)
        mplcyberpunk.add_bar_gradient(bars=bars)
        plt.savefig(f'./cred/sla-{date_obj}.jpg')
        plt.close('all')
        return 1
    else:
        return 0

def general_pie_graf(date_obj: str):
    data_request = db.get_general(date=datetime.strptime(date_obj, '%Y-%m-%d'))
    data_request_portal = db.get_date_portal(date=datetime.strptime(date_obj, '%Y-%m-%d'))
    if data_request and data_request_portal:
        pl_request = pl.DataFrame({
            'new': [row[1] for row in data_request],
            'fast': [row[2] for row in data_request],
            'all':  pl.Series([row[3] for row in data_request_portal]).sum()
        })
        plt.style.use("cyberpunk")
        fig, ax = plt.subplots(figsize=(5, 5), layout='constrained')
        size = 0.2
        vals = np.array([[pl_request.item(0, 'new'), pl_request.item(0, 'new') - pl_request.item(0, 'fast')],
                         [pl_request.item(0, 'all') - pl_request.item(0, 'new'), 0]])
        outer_colors = ['darkgreen', 'darkgreen']
        inner_colors = ['green', 'lime', 'darkgreen', 'darkgreen']
        ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors,
               wedgeprops=dict(width=size, edgecolor='darkgreen'))
        ax.pie(vals.flatten(), radius=1 - size, colors=inner_colors,
               wedgeprops=dict(width=size, edgecolor='darkgreen'))
        ax.set(aspect="equal", title=f"Всего проверок анкет: {pl_request.item(0, 'all')}\n"
                        f"Новых анкет: {pl_request.item(0, 'new')}\n"
                       f"Проверено за 15 минут: {pl_request.item(0, 'fast')}")
        plt.savefig(f'./cred/general-{date_obj}.jpg')
        plt.close('all')
        return 1
    else:
        return 0


def statistic_image_day(date_obj: str):
    param_dict = {'db_method': [db.get_call, db.get_jira_count, db.get_jira_time, db.get_date_portal],
                  'color': [['greenyellow', 'lime', 'chartreuse', 'springgreen', 'lawngreen', 'limegreen', 'green',
                            'forestgreen', 'darkolivegreen', 'darkgreen', 'darkgreen', 'darkgreen', 'darkgreen'],
                            ['darkgreen', 'darkolivegreen', 'forestgreen', 'green','limegreen', 'lawngreen',
                             'springgreen', 'chartreuse', 'lime', 'greenyellow', 'greenyellow', 'greenyellow']],
                  'title_label': ['Звонки', 'Количество заявок', 'Время выполнения заявок', 'Портал'],
                  'file_label': ['call', 'count', 'time', 'portal']}
    counting_for_marge_file = []
    counting_for_marge_file.append(created_bar(param_dict.get('db_method')[1], param_dict.get('color')[0],
                                               param_dict.get('title_label')[1], param_dict.get('file_label')[1],
                                               date_obj, check_autoresponder=True))
    counting_for_marge_file.append(horizontal_bar(date_obj))
    counting_for_marge_file.append(created_bar(param_dict.get('db_method')[2], param_dict.get('color')[1],
                                               param_dict.get('title_label')[2], param_dict.get('file_label')[2],
                                               date_obj, check_autoresponder=True, right_position=True))
    counting_for_marge_file.append(created_bar(param_dict.get('db_method')[0], param_dict.get('color')[0],
                                               param_dict.get('title_label')[0], param_dict.get('file_label')[0],
                                               date_obj))
    counting_for_marge_file.append(general_pie_graf(date_obj))
    counting_for_marge_file.append(created_bar(param_dict.get('db_method')[3], param_dict.get('color')[0],
                                               param_dict.get('title_label')[3], param_dict.get('file_label')[3],
                                               date_obj))
    done_image = save_one_image(counting_for_marge_file, date_obj)
    return done_image
