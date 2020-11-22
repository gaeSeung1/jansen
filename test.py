import threading
 
from queue import Queue
 
 
def creator(q):
    while True:
        evt = threading.Event()
        data = 1
        q.put((data, evt))

 
def consumer(q):

    while True:
        data, evt = q.get()
        print(data)
        evt.set()
        q.task_done()
 
 
q = Queue()

thread_one = threading.Thread(target=creator, args=(q,))
thread_two = threading.Thread(target=consumer, args=(q,))
thread_one.start()
thread_two.start()
 
q.join()
