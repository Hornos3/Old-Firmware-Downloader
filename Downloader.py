# coding = utf-8
import requests
import re
import os
import Decpfile
from math import *
# 本函数获得的参数是一个含有两个列表的参数，第一个列表为url列表，第二个列表为文件大小列表
def download(data_src, event, counter, mode):
    headers = {"User-Agent": "Microsoft Edge/89.0.774.57 Windows"}
    flag = 0
    filenames = []
    print('***[Thread 2]*** Now downloading begins......')
    if not os.path.isdir('./Firmwares'):
        os.mkdir('./Firmwares')
        flag = 1
    count = 0
    while count < counter:   # data_src[foot][0], data_src[foot][1]
        event.wait()
        datas = data_src.pop(0)
        data = datas[0]
        length = datas[1]
        print('\n***[Thread 2]*** Downloading...')
        response = requests.get(url=data, headers=headers)
        # path = os.path.dirname(os.path.realpath(__file__))
        # with open('D://编程学习//Python PyCharm//FD_byAgCl//' + data, "wb") as d:
        #     for dt in tqdm(response.iter_content(chunk_size=1024)):
        #         d.write(dt)
        print("\n***[Thread 2]*** " + data + ' downloaded' + ', count = %d, size = %.3f MB'
              % (count + 1, length / 0x100000))
        File_Name = './Firmwares/' + re.sub("',\\)", '', re.split('/', str(data))[-1])
        filenames.append(File_Name)
        if (flag == 0 and os.path.isfile(File_Name)):
            continue
        fp = open(File_Name, 'wb')
        fp.write(response.content)
        print("***[Thread 2]*** " + data + ' Saved.')
        count += 1
        if len(data_src) == 0:
            event.clear()
    if mode == "zip" or mode == "Zip":
        choice = input('***[Thread 2]*** zip files have been downloaded.'
                       'Do you want to decompress them? input y or n to give your choice: ')
        if choice == 'y':
            Decpfile.decompress(filenames, 'zip')
    elif mode == "rar" or mode == "RAR":
        choice = input('***[Thread 2]*** rar files have been downloaded.'
                       'Do you want to decompress them? input y or n to give your choice: ')
        if choice == 'y':
            Decpfile.decompress(filenames, 'rar')
    print('***[Thread 2]*** Finished.')
