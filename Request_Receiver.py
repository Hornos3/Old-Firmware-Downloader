# coding = utf-8
import re, os
import Decpfile
# Questions()
# @func 本函数实现用户需求的输入，用户可选择下载固件的扩展名和下载数量
# @return 本函数返回一个字典，mode对应扩展名，num对应下载数量
def Questions():
    choice = input('Do you want to download files or just extract and sort files? 1 / 2: ')
    if choice == '1':
        mode_list = ['zip', 'ZIP', 'bin', 'trx', 'rar']
        required_mode = input('Please select file mode you want to download from zip, bin, trx and rar: ')
        while required_mode not in mode_list:
            required_mode = input('Mode error! Please choose one from zip, bin, trx and rar: ')
        required_num = input('Then please input number of files you want to download: ')
        while int(required_num) <= 0 or re.match('\\.', required_num) or required_num == '':
            required_num = input('Input error! Please input again: ')
        required_num = int(required_num)
        ret_dict = {'mode': required_mode, 'num': required_num}
        choice_kw = input('Do you want to download with key words? input Y or N to choose: ')
        if choice_kw == "Y" or choice_kw == 'y':
            required_keyword = input('Please input key word included in the file:')
            ret_dict.update(kw=required_keyword)
            return ret_dict
        elif choice_kw == "N" or choice_kw == 'n':
            pass
        else:
            print("You've input neither a 'Y' or a 'N', we regarded it as N")
        return ret_dict
    elif choice == '2':
        filelist = []
        if not os.path.isdir('./Firmwares'):
            print('Sorry, no file to extract!')
            exit(1)
        else:
            for dirname, folders, filenames in list(os.walk('./Firmwares')):
                if dirname == './Firmwares':
                    filelist = filenames
            for file in filelist:
                Decpfile.ext('./Firmwares/' + file, './Firmwares/' + file, re.split('\\.', file)[-1])
        filelist.append('./Firmwares/Decompressed')
        Decpfile.order(filelist)
        exit(0)
    else:
        print('Input Error!')
        exit(1)