# coding = utf-8
import DBConnection
import Downloader
import threading
import Request_Receiver
global data_src, counter
def push_data_src(event):
    global data_src, counter
    DBConnection.inst(data_src, event, Need_dict)
def pop_data_src(event):
    global data_src, counter
    Downloader.download(data_src, event, counter, Need_dict['mode'])
if __name__ == '__main__':
    data_src = []
    Need_dict = Request_Receiver.Questions()
    counter = Need_dict['num']
    list_is_not_empty = threading.Event()
    list_is_not_empty.clear()
    thread_1 = threading.Thread(target=push_data_src, args=(list_is_not_empty, ))
    thread_2 = threading.Thread(target=pop_data_src, args=(list_is_not_empty, ))
    thread_1.start()
    thread_2.start()