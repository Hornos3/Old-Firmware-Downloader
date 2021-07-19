# coding = utf-8
import psycopg2, re, Request_Receiver, os, requests, sys, time, threading
def inst(data_src, event, Need_dict):

    # 如果存有url的txt文件不存在，则新建txt文件并写入url数据
    if not os.path.isfile('./url_src.txt'):
        print('***[Thread 1]*** It seems that you don\'t have the resource of urls, they will be downloaded soon.')
        conn = psycopg2.connect(database='firmware', user='root', password='root', host='118.126.65.110', port='5432')
        cursor = conn.cursor()
        print('***[Thread 1]*** Database connection completed, directing cursor...')
        sql = '***[Thread 1]*** SELECT url FROM public.product'
        cursor.execute(sql)
        print('***[Thread 1]*** Cursor direction completed.')
        all_url = cursor.fetchall()
        file = open('url_src.txt', 'w', encoding='utf-8')
        for url in all_url:
            file.write(url[0] + '\n')
        print('***[Thread 1]*** URL data downloaded.')
        file.close()
    # 如果已经存在txt文件，则将直接从该文件中读取url数据
    else:
        print('***[Thread 1]*** You have the resource of URLs in the database, '
              'so you don\'t have to connect to it again.')

    if len(data_src) == 0:
        event.clear()
    src = open('./url_src.txt', 'r', encoding='utf-8')
    # 读取文件中的内容，以换行作为分隔符以获得url和对应文件大小的字符串，两者用空格隔开
    all_url = src.read().split('\n')
    num = 0
    url_foot = 0
    src.close()
    print('***[Thread 1]*** Now searching begins......')
    while num < Need_dict['num']:
        src = open('./url_src.txt', 'r', encoding='utf-8')

        # 全部查询完毕
        if url_foot >= len(all_url):
            print('\n***[Thread 1]*** All searched.')
            break

        # 获取一个字符串其中的url，如果已经存在文件大小，则读取文件大小
        temp_data_url = re.split(' ', all_url[url_foot])[0]

        sys.stdout.write('\b' * 70 + '***[Thread 1]*** Database searching process: %d / %d URLs' %
                         (url_foot + 1, len(all_url)))

        # 暂不支持ftp，跳过
        if re.findall('^ftp', temp_data_url):
            url_foot += 1
            src.close()
            continue

        # 如果用户没有填写查询关键字
        if Need_dict.get('kw') is None:
            if re.findall('\\.' + Need_dict['mode'], temp_data_url):
                # 如果文件已经存在，则不再重复下载
                if os.path.isfile('./Firmwares/' + re.sub("',\\)", '', re.split('/', temp_data_url)[-1])):
                    print('\n***[Thread 1]*** This file ' + temp_data_url + ' was already downloaded.')
                else:
                    num = size_inst(temp_data_url, src, num, Need_dict, all_url, url_foot, data_src)
                    event.set()

        # 如果用户填写了关键字
        else:
            if re.findall(Need_dict['kw'], temp_data_url, re.I) and re.findall('\\.' + Need_dict['mode'], temp_data_url):
                # 如果文件已经存在，则不再重复下载
                if os.path.isfile('./Firmwares/' + re.sub("',\\)", '', re.split('/', temp_data_url)[-1])):
                    print('\n***[Thread 1]*** This file ' + temp_data_url + ' was already downloaded.')
                else:
                    num = size_inst(temp_data_url, src, num, Need_dict, all_url, url_foot, data_src)
                    event.set()
        url_foot += 1
        src.close()
    print("***[Thread 1]*** Searching process completed.")
def delete_line(file, string):
    file_bcp = open('url_src_bcp.txt', 'w', encoding='utf-8')
    line_list = file.readlines()
    line_list.remove(string + '\n')
    file.close()
    os.remove(file.name)
    for line in line_list:
        file_bcp.write(line)
    file_bcp.close()
    os.rename('url_src_bcp.txt', 'url_src.txt')
def size_inst(temp_data_url, src, num, Need_dict, all_url, url_foot, data_src):
    if len(re.split(' ', all_url[url_foot])) == 2:
        temp_data_length = float(re.split(' ', all_url[url_foot])[1])
        data_src.append((temp_data_url, temp_data_length))
        num += 1
        print('\n***[Thread 1]*** Valid url found, url searching process: %d / %d URLs' % (num, Need_dict['num']))
    else:
        length = int(requests.get(temp_data_url).headers['Content-Length'])
        if length < 10240:
            print("\n***[Thread 1]*** Length of ", temp_data_url, 'is too small(' + str(length) + ' B), abandoned.')
            delete_line(src, temp_data_url)
            print('***[Thread 1]*** This invalid url was removed from the resource file.')
        else:
            data_src.append((temp_data_url, length))
            add_size(src, temp_data_url, length)
            num += 1
            print('\n***[Thread 1]*** Valid url found, url searching process: %d / %d URLs' % (num, Need_dict['num']))
    return num
def add_size(file, string, length):
    file_bcp = open('url_src_bcp.txt', 'w', encoding='utf-8')
    line_list = file.readlines()
    file.close()
    index = line_list.index(string + '\n')
    line_list[index] = string + ' ' + str(length) + '\n'
    os.remove(file.name)
    for line in line_list:
        file_bcp.write(line)
    file_bcp.close()
    os.rename('url_src_bcp.txt', 'url_src.txt')