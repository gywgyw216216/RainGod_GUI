#!usr/bin/env python
# -*- coding: utf-8 -*-

'''
main.py
Rain God System Application Execution Entry.
'''

from tkinter import Tk
from base64 import b64decode
from os import remove, listdir, rmdir, makedirs
import os.path

from gui import RainGod
from tools import print_log, print_traceback_error
from resources import *



def build_resources(resource_data, folder_name, resource_name):
    '''
    生成资源文件
    
    :parameter resource_data: 资源文件base64加密字符串
    :type resource_data: <class 'str'>
    
    :parameter folder_name: 当前项目下的目标文件夹名
    :type folder_name: <class 'str'>
    
    :parameter resource_name: 资源文件名
    :type resource_name: <class 'str'>
    '''
    
    # 判断当前项目下的目标文件夹是否存在，不存在则创建文件夹
    if not os.path.exists('./' + folder_name):
        print_log('Folder ./' + folder_name + ' Not Exists. ')
        makedirs('./' + folder_name)
        print_log('Create Folder ./' + folder_name)
    else:
        print_log('Folder ./' + folder_name + ' Exists. ')
    
    # 在目标文件夹下生成资源文件
    with open(folder_name + '/' + resource_name, 'wb') as file:
        file.write(b64decode(resource_data))  # 对资源文件进行base64解密
    
    file.close()
    print_log('Build Resource ./' + folder_name + '/' + resource_name + ' Successfully! ')



def delete_resources(src_path):
    '''
    移除该目录下的所有文件和目录
    
    :param src_path: 源路径
    :type src_path: <class 'str'>
    
    :exception: exception: 移除文件/文件夹类型错误
    :type: <class 'Exception'>
    '''
    
    # 判断源路径是否为文件
    if os.path.isfile(src_path):
        try:
            remove(src_path)
            print_log('Resource ' + src_path + ' Removed Successfully! ')
        except Exception as exception:
            print_traceback_error(exception, 'Remove File')
    # 判断源路径是否为目录
    elif os.path.isdir(src_path):
        # 遍历该目录下的所有项目
        for item in listdir(src_path):
            delete_resources(os.path.join(src_path, item))  # 递归移除
            
            # 移除目录
            try:
                rmdir(src_path)
                print_log('Folder ' + src_path + ' Removed Successfully! ')
            except Exception as exception:
                print_traceback_error(exception, 'Remove Directory')



def main():
    print_log('Building Resources......')
    # 生成Rain God运行所需资源文件
    build_resources(chromedriver, 'resources', 'chromedriver.exe')
    build_resources(ICO, 'resources', 'RainGod256x256.ico')
    build_resources(RAIN_GOD, 'resources', 'RainGod256x256.png')
    build_resources(BACKGROUND, 'resources', 'background.png')
    build_resources(AQI, 'resources', 'AQI256x256.png')
    build_resources(COMFORT, 'resources', 'Comfort256x256.png')
    build_resources(PRECIPITATION, 'resources', 'Precipitation256x256.png')
    build_resources(RELATIVE_HUMIDITY, 'resources', 'RelativeHumidity256x256.png')
    build_resources(SENSIBLE_TEMPERATURE, 'resources', 'SensibleTemperature256x256.png')
    build_resources(WIND, 'resources', 'Wind256x256.png')
    print_log('Build Resources Successfully! ')
    print_log('Running Rain God......')
    # 运行GUI界面程序
    root = Tk()
    RainGod(root)
    root.mainloop()
    print_log('Exit Rain God Successfully! ')
    print_log('Removing Resources......')
    delete_resources('./resources')  # 移除文件夹./resources
    print_log('Remove Resources Successfully! ')



main()
