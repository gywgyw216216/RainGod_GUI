#!usr/bin/env python
# -*- coding: utf-8 -*-

'''
gui.py
'''

from tkinter import Tk, ttk, Toplevel, Canvas, StringVar, messagebox, BOTH, PhotoImage
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from crawler import get_province_data, get_city_data, get_weather_data
from visualization import draw_weather_forecast_line_chart
from tools import print_log, print_traceback_error



# 定义全局变量
TITLE = '雨师——基于Python的气象大数据可视化系统'  # UI界面标题
RAIN_GOD_IMAGE_PATH = 'resources/RainGod256x256.png'  # 雨师图标路径
BACKGROUND_IMAGE_PATH = 'resources/background.png'  # 背景图片路径
PRECIPITATION_IMAGE_PATH = 'resources/Precipitation256x256.png'  # 降水量图片路径
WIND_IMAGE_PATH = 'resources/Wind256x256.png'  # 风图片路径
RELATIVE_HUMIDITY_IMAGE_PATH = 'resources/RelativeHumidity256x256.png'  # 相对湿度图片路径
SENSIBLE_TEMPERATURE_IMAGE_PATH = 'resources/SensibleTemperature256x256.png'  # 体感温度图片路径
AQI_IMAGE_PATH = 'resources/AQI256x256.png'  # 空气质量图片路径
COMFORT_IMAGE_PATH = 'resources/Comfort256x256.png'  # 舒适度图片路径



class RainGod:
    '''
    Rain God类
    '''
    
    
    
    def __init__(self, master):
        '''
        Rain God类初始化
        
        :parameter master: Tkinter GUI界面对象
        :type master: <class 'tkinter.Tk'>
        '''
        
        self.__root = master
        self.__root_width = 1024
        self.__root_height = 768
        self.__root.geometry(
            self.get_center_window_format(self.__root, self.__root_width, self.__root_height))  # 设置窗口大小
        self.__root.title(TITLE)
        self.__root.resizable(False, False)  # 禁止调整窗口大小
        self.__root.iconphoto(True, PhotoImage(file=RAIN_GOD_IMAGE_PATH))  # 加载雨师图标
        self.select_city_form()
    
    
    
    def select_city_form(self):
        '''
        选择天气界面
        '''
        
        self.hide_window()
        self.__province_ids, self.__provinces = get_province_data(
            'http://www.nmc.cn/publish/forecast/ASH/xujiahui.html')
        self.__first_city_urls = ['beijing', 'tianjin', 'shijiazhuang', 'taiyuan', 'huhehaote', 'shenyang',
                                  'changchun',
                                  'haerbin', 'xujiahui', 'nanjing', 'hangzhou', 'hefei', 'fuzhou', 'nanchang',
                                  'jinan',
                                  'zhengzhou', 'wuhan', 'changshashi', 'guangchou', 'nanning', 'haikou',
                                  'shapingba',
                                  'chengdu', 'guiyang', 'kunming', 'lasa', 'xian', 'lanzhou', 'xining', 'yinchuan',
                                  'wulumuqi', 'xianggang', 'aomen', 'taibei']
        self.__city_urls = []
        self.__cities = []
        self.__province = None
        self.__city = None
        self.__real_time_weather = None
        self.__date_weathers = []
        print_log('Rain God Initialization Successfully! ')
        form = Toplevel()  # 创建顶层窗口
        form_width = 480
        form_height = 320
        form.geometry(self.get_center_window_format(form, form_width, form_height))
        form.title(TITLE)
        form.resizable(False, False)
        form.protocol('WM_DELETE_WINDOW', self.exit)  # 自定义窗口右上角关闭按钮事件触发回调函数
        canvas = Canvas(form, width=form_width, height=form_height)  # 创建画布
        self.__image_background = ImageTk.PhotoImage(
            Image.open(BACKGROUND_IMAGE_PATH).resize((form_width, form_height)))  # 创建图片类对象
        canvas.create_image(form_width / 2, form_height / 2, image=self.__image_background)  # 在画布中嵌入图片
        canvas.create_text(240, 50, text='请选择想要查询天气情况的省市：', font=(24))  # 在画布中嵌入文本
        canvas.pack()  # 自动布局
        province_value = StringVar()  # 创建tkinter窗口StringVar类变量接收控件中的字符串值
        province_values = self.__provinces
        combobox_province = ttk.Combobox(form, values=province_values, textvariable=province_value,
                                         state='readonly')  # 创建下拉框
        combobox_province.place(x=50, y=120)  # 绝对坐标布局
        city_value = StringVar()
        combobox_city = ttk.Combobox(form, textvariable=city_value, state='readonly')
        combobox_city.place(x=250, y=120)
        handle1 = lambda x: self.choose_province(combobox_province, province_values, combobox_city)  # 创建匿名函数
        combobox_province.bind("<<ComboboxSelected>>", handle1)  # 绑定下拉框选项被选中虚拟事件触发回调函数
        handle2 = lambda: self.destroy(form, combobox_province, province_values, combobox_city)
        button_selection = ttk.Button(form, text='确定', command=handle2)  # 创建按钮
        button_selection.place(x=120, y=220)
        button_exit = ttk.Button(form, text='退出', command=self.exit)
        button_exit.place(x=250, y=220)
    
    
    
    def get_center_window_format(self, form, form_width, form_height):
        '''
        获取界面窗口中心位置几何函数字符串
        
        :param form: Tkinter GUI界面类对象
        :type form: <class 'tkinter.Tk', 'tkinter.Toplevel'>
        
        :param form_width: 界面窗口宽度
        :type form_width: <class 'int'>
        
        :param form_height: 界面窗口高度
        :type form_height: <class 'int'>
        
        :return: string: 界面窗口中心位置几何函数字符串
        :rtype: <class 'str'>
        '''
        
        center_width = (form.winfo_screenwidth() - form_width) / 2
        center_height = (form.winfo_screenheight() - form_height) / 2
        
        return '%dx%d+%d+%d' % (form_width, form_height, center_width, center_height)
    
    
    
    def choose_province(self, combobox_province, province_values, combobox_city):
        '''
        选择省份
        
        :parameter combobox_province: 省份下拉框对象
        :type combobox_province: <class 'tkinter.ttk.Combobox'>
        
        :parameter province_values: 省份字符串列表
        :type province_values: <class 'list'>
        
        :parameter combobox_city: 城市下拉框对象
        :type combobox_city: <class 'tkinter.ttk.Combobox'>
        
        :exception: exception: 选择省份错误
        :type: <class 'Exception'>
        '''
        
        self.__province = self.__province_ids[province_values.index(combobox_province.get())]
        
        try:
            self.__city_urls, self.__cities = get_city_data(
                'http://www.nmc.cn/publish/forecast/' + self.__province + '/' + self.__first_city_urls[
                    province_values.index(combobox_province.get())] + '.html')
            city_values = self.__cities
            combobox_city['values'] = city_values
            handle = lambda x: self.choose_city(combobox_city, city_values)
            combobox_city.bind("<<ComboboxSelected>>", handle)
            print_log('Choose Province Successfully! ')
        except Exception as exception:
            print_traceback_error(exception, 'Choose Province')
    
    
    
    def choose_city(self, combobox_city, city_values):
        '''
        选择城市
        
        :parameter combobox_city: 城市下拉框对象
        :type combobox_city: <class 'tkinter.ttk.Combobox'>
        
        :parameter city_values: 城市字符串列表
        :type city_values: <class 'list'>
        '''
        
        self.__city = self.__city_urls[city_values.index(combobox_city.get())]
        print_log('Choose City Successfully! ')
    
    
    
    def exit(self):
        '''
        退出界面
        '''
        
        self.__root.destroy()
    
    
    
    def show_window(self):
        '''
        显示主界面
        '''
        
        if self.__real_time_weather is None and self.__date_weathers is None:
            if messagebox.askretrycancel(message='查询气象数据失败！\n请确认网络连接良好后点击“重试”按钮\n点击"取消"按钮则退出系统'):  # 创建重试、取消消息对话框
                self.select_city_form()
            else:
                self.exit()
        else:
            self.add_widget(self.__root)
            self.__root.update()
            self.__root.deiconify()
    
    
    
    def hide_window(self):
        '''
        隐藏主界面
        '''
        
        self.__root.withdraw()
    
    
    
    def destroy(self, form, combobox_province, province_values, combobox_city):
        '''
        销毁选择天气界面
        
        :param form: Tkinter GUI界面类对象
        :type form: <class 'tkinter.Toplevel'>
        
        :parameter combobox_province: 省份下拉框对象
        :type combobox_province: <class 'tkinter.ttk.Combobox'>
        
        :parameter province_values: 省份字符串列表
        :type province_values: <class 'list'>
        
        :parameter combobox_city: 城市下拉框对象
        :type combobox_city: <class 'tkinter.ttk.Combobox'>
        
        :exception: exception: 销毁界面错误
        :type: <class 'Exception'>
        '''
        
        if self.__province_ids is None and self.__provinces is None:
            if messagebox.askretrycancel(message='初始化失败！\n请确认网络连接良好后点击“重试”按钮\n点击"取消"按钮则退出系统'):
                form.destroy()
                self.select_city_form()
            else:
                self.exit()
        elif self.__city_urls is None and self.__cities is None:
            if messagebox.askretrycancel(message='选择省份失败！\n请确认网络连接良好后点击“重试”按钮\n点击"取消"按钮则退出系统'):
                self.choose_province(combobox_province, province_values, combobox_city)
            else:
                self.exit()
        else:
            if self.__province is None:
                messagebox.showinfo('提示', '请选择想要查询天气情况的省份！')  # 创建提示消息对话框
            elif self.__province is not None and self.__city is None:
                messagebox.showinfo('提示', '请选择想要查询天气情况的城市！')
            else:
                try:
                    self.__real_time_weather, self.__date_weathers = get_weather_data(
                        'http://www.nmc.cn/publish/forecast/' + self.__province + '/' + self.__city + '.html')
                    form.destroy()
                    self.show_window()
                except Exception as exception:
                    print_traceback_error(exception, 'Destroy')
    
    
    
    def back(self):
        '''
        主界面返回
        '''
        
        self.exit()
        root = Tk()
        RainGod(root)
        root.mainloop()
    
    
    
    def add_widget(self, root):
        '''
        主界面添加控件
        
        :param root: Tkinter GUI界面对象
        :type root: <class 'tkinter.Tk'>
        '''
        
        notebook = ttk.Notebook(root)  # 创建选项卡
        frame1 = ttk.Frame(notebook)  # 创建框架
        frame2 = ttk.Frame(notebook)
        label_publish_time = ttk.Label(frame1, text=self.__real_time_weather.get_publish_time())  # 创建标签
        label_publish_time.place(x=0, y=10)
        label_publish_time.update()  # 更新
        label_position = ttk.Label(frame1, text=self.__provinces[self.__province_ids.index(self.__province)] +
                                                ' ' + self.__cities[self.__city_urls.index(self.__city)], font=(24))
        label_position.place(x=450, y=50)
        label_position.update()
        label_temperature = ttk.Label(frame1, text=self.__real_time_weather.get_temperature(), font=(24))
        label_temperature.place(x=480, y=100)
        label_temperature.update()
        self.__image_precipitation = ImageTk.PhotoImage(Image.open(PRECIPITATION_IMAGE_PATH).resize((128, 128)))
        self.__label_precipitation_image = ttk.Label(frame1, image=self.__image_precipitation)  # 创建图片标签
        self.__label_precipitation_image.place(x=200, y=150)
        label_precipitation = ttk.Label(frame1, text=self.__real_time_weather.get_precipitation())
        label_precipitation.place(x=250, y=280)
        label_precipitation.update()
        self.__image_wind = ImageTk.PhotoImage(Image.open(WIND_IMAGE_PATH).resize((128, 128)))
        self.__label_wind_image = ttk.Label(frame1, image=self.__image_wind)
        self.__label_wind_image.place(x=440, y=150)
        label_wind_direction = ttk.Label(frame1, text=self.__real_time_weather.get_wind_direction())
        label_wind_direction.place(x=480, y=280)
        label_wind_direction.update()
        label_wind_power = ttk.Label(frame1, text=self.__real_time_weather.get_wind_power())
        label_wind_power.place(x=480, y=300)
        label_wind_power.update()
        self.__image_relative_humidity = ImageTk.PhotoImage(Image.open(RELATIVE_HUMIDITY_IMAGE_PATH).resize((128, 128)))
        self.__label_relative_humidity_image = ttk.Label(frame1, image=self.__image_relative_humidity)
        self.__label_relative_humidity_image.place(x=650, y=150)
        label_relative_humidity = ttk.Label(frame1, text=self.__real_time_weather.get_relative_humidity())
        label_relative_humidity.place(x=700, y=280)
        label_relative_humidity.update()
        self.__image_sensible_temperature = ImageTk.PhotoImage(
            Image.open(SENSIBLE_TEMPERATURE_IMAGE_PATH).resize((128, 128)))
        self.__label_sensible_temperature_image = ttk.Label(frame1, image=self.__image_sensible_temperature)
        self.__label_sensible_temperature_image.place(x=200, y=400)
        label_sensible_temperature = ttk.Label(frame1, text=self.__real_time_weather.get_sensible_temperature())
        label_sensible_temperature.place(x=250, y=540)
        label_sensible_temperature.update()
        self.__image_aqi = ImageTk.PhotoImage(Image.open(AQI_IMAGE_PATH).resize((128, 128)))
        self.__label_aqi_image = ttk.Label(frame1, image=self.__image_aqi)
        self.__label_aqi_image.place(x=440, y=400)
        label_aqi = ttk.Label(frame1, text=self.__real_time_weather.get_aqi())
        label_aqi.place(x=450, y=540)
        label_aqi.update()
        self.__image_comfort = ImageTk.PhotoImage(Image.open(COMFORT_IMAGE_PATH).resize((128, 128)))
        self.__label_comfort_image = ttk.Label(frame1, image=self.__image_comfort)
        self.__label_comfort_image.place(x=650, y=400)
        label_comfort = ttk.Label(frame1, text=self.__real_time_weather.get_comfort())
        label_comfort.place(x=660, y=540)
        label_comfort.update()
        self.__image_background = ImageTk.PhotoImage(
            Image.open(BACKGROUND_IMAGE_PATH).resize((self.__root_width, self.__root_height)))
        self.__label_background_image = ttk.Label(frame2, image=self.__image_background)
        self.__label_background_image.pack()
        figure = draw_weather_forecast_line_chart(self.__date_weathers)  # 创建Matplotlib Figure类对象
        canvas = FigureCanvasTkAgg(figure, frame2)  # 创建能嵌入Matplotlib Figure类对象的画布
        canvas.draw()  # 绘制画布
        canvas.get_tk_widget().place(x=100, y=50)  # 画布绝对布局
        canvas.get_tk_widget().update()  # 画布更新
        frame1.update()
        frame2.update()
        notebook.add(frame1, text='实时天气')  # 设置选项卡标签
        notebook.add(frame2, text='7天天气预报折线图')
        notebook.pack(fill=BOTH, expand=True)  # 选项卡自动布局
        notebook.update()
        frame = ttk.Frame(root).pack()
        button_return = ttk.Button(frame, text='返回', command=self.back)
        button_return.place(x=350, y=700)
        button_exit = ttk.Button(frame, text='退出', command=self.exit)
        button_exit.place(x=580, y=700)



if __name__ == '__main__':
    root = Tk()
    RainGod(root)
    root.mainloop()
