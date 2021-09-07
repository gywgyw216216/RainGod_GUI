#!usr/bin/env python
# -*- coding: utf-8 -*-

'''
visualization.py
'''

from matplotlib.pyplot import figure, show
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator
from datetime import datetime

from crawler import get_weather_data
from tools import print_log, print_traceback_error



def draw_weather_forecast_line_chart(date_weathers):
    '''
    绘制7天天气预报折线图
    
    :parameter date_weathers: 日期天气类对象列表
    :type date_weathers: <class 'list'>
    
    :return: root_figure: Matplotlib的Figure类对象
    :rtype: <class 'matplotlib.figure.Figure'>
    
    :exception exception: 7天天气预报折线图可视化错误
    :type exception: <class 'Exception'>
    '''
    
    print_log('Visualizing...... ')
    # 可视化初始化
    x = []  # 创建日期可视化列表
    y1 = []  # 创建最高温度可视化列表
    y2 = []  # 创建最低温度可视化列表
    
    try:
        # 遍历date_weathers列表提取数据添加进各自可视化列表
        for i in date_weathers:
            x.append(datetime(i.get_date().year, i.get_date().month, i.get_date().day))
            
            if i.get_highest_temperature() == '-':
                y1.append(None)
            else:
                y1.append(eval(i.get_highest_temperature()[:-1]))
            
            if i.get_lowest_temperature() == '-':
                y2.append(None)
            else:
                y2.append(eval(i.get_lowest_temperature()[:-1]))
        
        # Matplotlib各项设置
        rcParams['font.sans-serif'] = 'SimHei'  # 设置Matplotlib显示字体：黑体
        rcParams['axes.unicode_minus'] = False  # 设置Matplotlib负号（字符）可视化
        # rcParams['toolbar'] = 'toolbar2'  # 设置Matplotlib工具栏：默认
        root_figure = figure(figsize=(6.67, 5), dpi=120)  # 创建唯一的figure，每英寸像素点120，长6.67英寸，宽5英寸（分辨率：800*600）
        ax = root_figure.add_subplot(1, 1, 1)  # 创建唯一的子图
        ax.set_title('7天天气预报折线图', fontsize=20)  # 设置标题
        ax.set_xlabel('日期')  # 设置x轴标签
        ax.set_ylabel('温度\n（°C）', rotation=0, position=(0, 1.02))  # 设置y轴标签，水平，在y轴上方
        
        # 获取可视化列表最值
        if y2[0] is None:
            y2_minimum = min(y2[1:])
        else:
            y2_minimum = min(y2)
        
        if y1[0] is None:
            y1_maximum = max(y1[1:])
        else:
            y1_maximum = max(y1)
        
        ax.yaxis.set_major_locator(MultipleLocator(1))  # 设置y轴刻度间隔为1
        ax.set_ylim(y2_minimum - 4, y1_maximum + 3)  # 设置y轴范围
        # # 设置网格可视化
        # ax.xaxis.grid(True, which='major')
        # ax.yaxis.grid(True, which='major')
        # ax.grid(b=True, which='major', axis='both', alpha=0.5)
        # 去除边框
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # ax.spines['bottom'].set_visible(False)
        # ax.spines['left'].set_visible(False)
        
        # 遍历date_weathers列表提取数据以及可视化列表生成对应坐标的文本信息
        for i in range(7):
            if y1[i] is not None:
                ax.text(x[i], y1[i], date_weathers[i].get_highest_temperature() + '\n' + date_weathers[
                    i].get_weather_description1() + '\n')
            
            if y2[i] is not None:
                ax.text(x[i], y2[i], date_weathers[i].get_lowest_temperature() + '\n' + date_weathers[
                    i].get_weather_description2() + '\n')
        
        # 绘图
        ax.plot(x, y1, color='r', label='最高温度')  # 绘制最高温度折线图，线段颜色为红色
        ax.plot(x, y2, color='b', label='最低温度')  # 绘制最低温度折线图，线段颜色为蓝色
        ax.plot(x, y1, marker='o', color='r')  # 绘制最高温度圆点图，圆点颜色为红色
        ax.plot(x, y2, marker='o', color='b')  # 绘制最低温度圆点图，圆点颜色为蓝色
        # position = ax.get_position()  # 获取子图位置
        # ax.set_position([position.x0, position.y0, position.width, position.height * 0.9])  # 调整子图位置
        # ax.legend(loc='center', bbox_to_anchor=(0.5, 1.1), ncol=2)  # 显示图例，单行显示，居中，位于子图上方
        ax.legend(loc='lower left')  # 显示图例，位于左下方
        root_figure.tight_layout()  # 自动调整布局，填充整个区域
        # show()  # 显示绘图结果
        
        print_log('Visualization Successfully! ')
        
        return root_figure
    except Exception as exception:
        print_traceback_error(exception, 'Visualization')
        
        return None



if __name__ == '__main__':
    real_time_weather, date_weathers = get_weather_data('http://www.nmc.cn/publish/forecast/ASH/xujiahui.html')
    draw_weather_forecast_line_chart(date_weathers)
