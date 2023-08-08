from matplotlib import pyplot as plt
import polars as pl
import mplcyberpunk
from datetime import datetime
from PIL import Image
import numpy as np


def addlabels2(x,y):
    for i in range(len(x)):
        plt.text(i, y[i]//2,y[i], ha = 'center')

def graph_differrence_time(data_frame, series_time):
    median_time = series_time.median()
    mean_time = series_time.mean()
    inner_colors = ['green', 'forestgreen', 'darkgreen', 'sienna', 'saddlebrown']
    fig, ax = plt.subplots(figsize=(5, 10), layout='constrained')
    ax.boxplot(series_time)
    plt.savefig(f'./cred/boxplot.jpg')
    fig, ax = plt.subplots(figsize=(5, 5), layout='constrained')
    bars = ax.bar(data_frame['col2'], data_frame['count'], color=inner_colors, zorder=2)
    addlabels2(data_frame['col2'], data_frame['count'])
    ax.set_yticks([])
    mplcyberpunk.add_bar_gradient(bars=bars)
    plt.savefig(f'./cred/bar.jpg')
    fig, ax = plt.subplots(figsize=(5, 5), layout='constrained')
    explode = [0, 0.1, 0.2, 0.3, 0.6]
    size_d = len(data_frame['count'])
    ax.pie(data_frame['count'], radius=1, colors=inner_colors, labels=data_frame['col2'],
           autopct='%1.1f%%', shadow=True, explode=explode[:size_d],
           textprops=dict(color='gold', size='x-large'))
    plt.axis('equal')
    plt.savefig(f'./cred/pie.jpg')
    img_ran = Image.open(f'./cred/boxplot.jpg')
    img_size = img_ran.size
    new_im = Image.new('RGB', (img_size[0] * 2, img_size[1]), (0, 0, 0))
    new_im.paste(img_ran, (0, 0))
    img_ran2 = Image.open(f'./cred/bar.jpg')
    new_im.paste(img_ran2, (img_size[0], 0))
    img_ran3 = Image.open(f'./cred/pie.jpg')
    new_im.paste(img_ran3, (img_size[0], img_size[0]))
    new_im.save(f"./cred/dif_dashboard.png", "PNG")
    return {'median': median_time, 'mean': mean_time}


def graph_dif_days(date_dict: dict):
    plt.style.use("cyberpunk")
    x = ['0-5', '5-10', '10-15', '15-20', '20-...']
    dict_for_message = {}
    date_list = []
    for date_str, date_tuple in date_dict.items():
        date_list.append(date_str)
        ddf = date_tuple[0]
        data_list = []
        for elem in x:
            try:
                reslt_df = ddf.row(by_predicate=(pl.col("col2") == elem))
                data_list.append(reslt_df[1])
            except:
                data_list.append(0)
        plt.plot(x, data_list, marker='o')
        plt.legend(date_str)
        median_time = date_tuple[1].median()
        mean_time = date_tuple[1].mean()
        dict_for_message[date_str] = (median_time, mean_time)
    plt.legend(date_list)
    mplcyberpunk.add_glow_effects()
    plt.savefig(f'./cred/graph_day.jpg')
    return dict_for_message