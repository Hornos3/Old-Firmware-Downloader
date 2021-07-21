# coding = utf-8
import zipfile, os, re, shutil, rarfile
def ext(file, dir, suffix):
    if suffix == 'zip':
        file_to_dezip = zipfile.ZipFile(file, 'r')
        print('Start extracting file %s' % file)
        for f in file_to_dezip.namelist():
            file_to_dezip.extract(f, './Firmwares/Decompressed/' + dir[2:])
            print('File %s extracted.' % f)
            if re.match(".+\\.zip$", f):
                ext('./Firmwares/Decompressed/' + dir[2:] + '/' + f, './Firmwares/Decompressed/' + dir[2:] + '/' + f,
                    'zip')
    elif suffix == 'rar':
        israr = True
        try:
            file_to_derar = rarfile.RarFile(file, 'r')
            print('Start extracting file %s' % file)
        except rarfile.NotRarFile:
            israr = False
            try:
                ext(file, dir, 'zip')
            except zipfile.error:
                print('This file is neither a zip file nor a rar file!')
        finally:
            if israr:
                for f in file_to_derar.namelist():
                    try:
                        file_to_derar.extract(f, './Firmwares/Decompressed/' + dir[2:])
                        print('File %s extracted.' % f)
                    except rarfile.BadRarFile:
                        print('Uh oh, This file was damaged!')
                    finally:
                        if re.match(".+\\.rar$", f):
                            ext('./Firmwares/Decompressed/' + dir[2:] + '/' + f,
                                './Firmwares/Decompressed/' + dir[2:] + '/' + f,
                                'rar')

def copyfile(dirname, folder):
    for dirname, folders, filenames in list(os.walk(dirname + '/' + folder)):
        for filename in filenames:
            if not os.path.isdir('./Firmwares/Ordered/' + re.split('\\.', filename)[-1]):
                os.mkdir('./Firmwares/Ordered/' + re.split('\\.', filename)[-1])
            shutil.copy(dirname + '/' + filename, './Firmwares/Ordered/' + re.split('\\.', filename)[-1] +
                        '/' + filename)
            print(filename + " ordered.")
        for folder in folders:
            copyfile(dirname, folder)

def order(filenames):
    if not os.path.isdir('./Firmwares/Ordered'):
        os.mkdir('./Firmwares/Ordered')
    for folder in filenames:
        for dirname, folders, filenames in list(os.walk(folder)):
            if re.match('.+\\.\\w+$', dirname):
                for filename in filenames:
                    if not os.path.isdir('./Firmwares/Ordered/' + re.split('\\.', filename)[-1]):
                        os.mkdir('./Firmwares/Ordered/' + re.split('\\.', filename)[-1])
                    shutil.copy(dirname + '/' + filename, './Firmwares/Ordered/' + re.split('\\.', filename)[-1] +
                                '/' + filename)
                    print(filename + " ordered.")
                for folder in folders:
                    copyfile(dirname, folder)

def decompress(filenames, suffix):
    if not os.path.isdir('./Firmwares/Decompressed'):
        os.mkdir('./Firmwares/Decompressed')
    for file in filenames:
        ext(file, file, suffix)
    IsOrder = input('Do you want to order those decompressed file into different suffixes? Y / N ')
    if IsOrder == 'y' or IsOrder == 'Y':
        filenames.append('./Firmwares/Decompressed')
        order(filenames)
