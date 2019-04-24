# coding=utf-8
import threading
import time


class myThread(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.i = i

    def run(self):
        time.sleep(2)
        print('Thread {} is running.'.format(self.i))
        time.sleep(2)
        return


if __name__ == '__main__':
    print "进入一页"
    threads = []
    for i in range(1, 6):

        t = myThread(i)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    print '进入下一页'