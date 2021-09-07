#!usr/bin/env python
# -*- coding: utf-8 -*-

'''
crawler.py
Define Some Crawler Functions and Some Parser Functions.
1. selenium_initialization()
2. carwler()
3. parser()
4. get_province_data()
5. get_city_data()
6. get_weather_data()
'''

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
from re import compile
from datetime import datetime, timedelta

from weather import RealTimeWeather, DateWeather
from tools import print_log, print_traceback_error



CHROME_WEB_DRIVER_PATH = './resources/chromedriver.exe'  # Global Variable Chrome Web Driver Path



def selenium_initialization(browser_webdriver_path, browser_type, hide=True):
    '''
    初始化Selenium Web Driver

    :parameter browser_webdriver_path: Browser Web Driver路径
    :type browser_webdriver_path: <class 'str'>

    :parameter browser_type: 浏览器类型
    :type browser_type: <class 'str'>

    :parameter hide: 是否不显示浏览器，默认为True
    :type hide: <class 'bool'>

    :return: webdriver: Selenium Web Driver
    :rtype: <class 'selenium.webdriver'>

    :raise: exception: 浏览器类型错误
    :type: <class 'Exception'>

    :exception: exception: Selenium Web Driver初始化错误
    :type: <class 'Exception'>
    '''
    
    try:
        print_log('Selenium Web Driver Initializing...... ')
        
        if browser_type == 'Firefox' or browser_type == 'firefox':
            option = FirefoxOptions()  # 设置Firefox浏览器选项
            option.add_argument('--incognito')  # 以隐私窗口访问
            print_log('Selenium Web Driver Initialization Successfully! ')
            
            return webdriver.Firefox(executable_path=browser_webdriver_path, options=option)
        elif browser_type == 'Chrome' or browser_type == 'chrome':
            option = ChromeOptions()  # 设置Chrome浏览器选项
            option.add_argument('--incognito')  # 以无痕窗口访问
            
            if hide:
                option.add_argument('--headless')  # 不显示浏览器
            
            print_log('Selenium Web Driver Initialization Successfully! ')
            
            return webdriver.Chrome(executable_path=browser_webdriver_path, options=option)
        elif browser_type == 'Safari' or browser_type == 'safari':
            print_log('Selenium Web Driver Initialization Successfully! ')
            
            return webdriver.Safari(executable_path=browser_webdriver_path)
        elif browser_type == 'IE' or browser_type == 'ie' or browser_type == 'Ie':
            print_log('Selenium Web Driver Initialization Successfully! ')
            
            return webdriver.Ie(executable_path=browser_webdriver_path)
        elif browser_type == 'Edge' or browser_type == 'edge':
            print_log('Selenium Web Driver Initialization Successfully! ')
            
            return webdriver.Edge(executable_path=browser_webdriver_path)
        else:
            raise Exception('Browser Type ERROR! ')
    except Exception as exception:
        print_traceback_error(exception, 'Selenium Web Driver Initialization')
        
        return None



def crawler(web_driver, url):
    '''
    爬虫
    
    :parameter web_driver: Selenium Web Driver
    :type web_driver: <class 'selenium.webdriver'>
    
    :parameter url: 爬虫目标地址
    :type url: <class 'str'>
    
    :return: result: 爬虫目标地址HTML源代码
    :rtype: <class 'str'>
    
    :exception: exception: 爬虫错误
    :type: <class 'Exception'>
    '''
    
    print_log('Crawlering...... ')
    
    try:
        web_driver.get(url)
        result = web_driver.page_source
        web_driver.close()
        web_driver.quit()
        print_log('Crawler Successfully! ')
        
        return result
    except Exception as exception:
        print_traceback_error(exception, 'Crawler')
        web_driver.close()
        web_driver.quit()
        
        return None



def parser(html):
    '''
    BeautifulSoup HTML源代码解析
    
    :parameter html: 爬虫目标地址HTML源代码
    :type html: <class 'str'>
    
    :return: soup: 爬虫目标地址HTML源代码解析结果
    :rtype: <class 'bs4.BeautifulSoup'>
    '''
    
    return BeautifulSoup(html, 'lxml')



def get_province_data(url):
    '''
    获取省份数据
    
    :parameter url: 爬虫目标地址
    :type url: <class 'str'>
    
    :returns
    
    :return: province_ids: 省份id字符串列表
    :rtype: <class 'list'>
    
    :return: provinces: 省份字符串列表
    :rtype: <class 'list'>
    
    :exception: exception: 爬虫目标地址HTML源代码解析错误
    :type: <class 'Exception'>
    '''
    
    try:
        # 使用Chrome浏览器进行爬虫
        web_driver = selenium_initialization(CHROME_WEB_DRIVER_PATH, 'Chrome')
        html = crawler(web_driver, url)
        print_log('Parsering...... ')
        # 使用正则表达式解析省份value和省份名
        pattern_province_id = compile('<option value="(A[A-Z]{2})">.+?</option>')
        pattern_province = compile('<option value="A[A-Z]{2}">(.+?)</option>')
        province_ids = pattern_province_id.findall(html)
        provinces = pattern_province.findall(html)
        print_log('Parser Successfully! ')
        
        return province_ids, provinces
    except Exception as exception:
        print_traceback_error(exception, 'Parser')
        
        return None, None



def get_city_data(url):
    '''
    获取城市数据
    
    :parameter url: 爬虫目标地址
    :type url: <class 'str'>
    
    :returns
    
    :return: city_urls: 城市url字符串列表
    :rtype: <class 'list'>
    
    :return: cities: 城市字符串列表
    :rtype: <class 'list'>
    
    :exception: exception: 爬虫目标地址HTML源代码解析错误
    :type: <class 'Exception'>
    '''
    
    try:
        # 使用Chrome浏览器进行爬虫
        web_driver = selenium_initialization(CHROME_WEB_DRIVER_PATH, 'Chrome')
        html = crawler(web_driver, url)
        print_log('Parsering...... ')
        # 使用正则表达式解析城市url和城市名
        pattern_city_url = compile('<option value="[0-9]{5}" url="/publish/forecast/A[A-Z]{2}/(.+?).html">.+?</option>')
        pattern_city = compile('<option value="[0-9]{5}" url="/publish/forecast/A[A-Z]{2}/.+?.html">(.+?)</option>')
        city_urls = pattern_city_url.findall(html)
        cities = pattern_city.findall(html)
        print_log('Parser Successfully! ')
        
        return city_urls, cities
    except Exception as exception:
        print_traceback_error(exception, 'Parser')
        
        return None, None



def get_weather_data(url):
    '''
    获取气象数据

    :parameter url: 爬虫目标地址
    :type url: <class 'str'>

    :returns

    :return: real_time_weather: 实时天气类
    :rtype: <class 'weather.RealTimeWeather'>

    :return: date_weathers: 日期天气类对象列表
    :rtype: <class 'list'>

    :exception: exception: 爬虫目标地址HTML源代码解析错误
    :type: <class 'Exception'>
    '''
    
    try:
        # 使用Chrome浏览器进行爬虫
        web_driver = selenium_initialization(CHROME_WEB_DRIVER_PATH, 'Chrome')
        html = crawler(web_driver, url)
        print_log('Parsering...... ')
        soup = parser(html)
        # 使用BeautifulSoup进行解析
        real_time_publish_time = soup.find(id='realPublishTime').get_text()
        real_time_temperature = soup.find(id='realTemperature').get_text()
        real_time_precipitation = soup.find(id='realRain').get_text()
        real_time_wind_direction = soup.find(id='realWindDirect').get_text()
        real_time_wind_power = soup.find(id='realWindPower').get_text()
        real_time_relative_humidity = soup.find(id='realHumidity').get_text()
        real_time_sensible_temperature = soup.find(id='realFeelst').get_text()
        real_time_aqi = soup.find(id='aqi').get_text().strip()
        real_time_comfort = soup.find(id='realIcomfort').get_text()
        # 创建RealTimeWeather类对象real_time_weather
        real_time_weather = RealTimeWeather(real_time_publish_time, real_time_temperature, real_time_precipitation,
                                            real_time_wind_direction, real_time_wind_power, real_time_relative_humidity,
                                            real_time_sensible_temperature, real_time_aqi, real_time_comfort)
        # 使用BeautifulSoup进行解析
        temperatures = soup.find_all('div', attrs={'class': 'tmp'})
        weather_descriptions = soup.find_all('div', attrs={'class': 'desc'})
        wind_directions = soup.find_all('div', attrs={'class': 'windd'})
        wind_levels = soup.find_all('div', attrs={'class': 'winds'})
        # 创建date_weathers列表
        date_weathers = []
        # 获取当前日期时间
        date = datetime.today()
        
        # 遍历各列表提取HTML标签内文本
        for i in range(7):
            highest_temperature = temperatures[2 * i].get_text().strip()
            lowest_temperature = temperatures[2 * i + 1].get_text().strip()
            weather_description1 = weather_descriptions[2 * i].get_text().strip()
            weather_description2 = weather_descriptions[2 * i + 1].get_text().strip()
            wind_direction1 = wind_directions[2 * i].get_text().strip()
            wind_direction2 = wind_directions[2 * i + 1].get_text().strip()
            wind_level1 = wind_levels[2 * i].get_text().strip()
            wind_level2 = wind_levels[2 * i + 1].get_text().strip()
            # 创建DateWeather类对象并添加进DateWeather类对象列表date_weathers
            date_weathers.append(
                DateWeather(date, highest_temperature, lowest_temperature, weather_description1, weather_description2,
                            wind_direction1, wind_direction2, wind_level1, wind_level2))
            # 当前日期时间值＋1天
            date += timedelta(days=1)
        
        print_log('Parser Successfully! ')
        
        return real_time_weather, date_weathers
    except Exception as exception:
        print_traceback_error(exception, 'Parser')
        
        return None, None



if __name__ == '__main__':
    # get_province_data('http://www.nmc.cn/publish/forecast/ASH/xujiahui.html')
    get_city_data('http://www.nmc.cn/publish/forecast/ASH/xujiahui.html')
    # get_weather_data('http://www.nmc.cn/publish/forecast/ASH/xujiahui.html')
