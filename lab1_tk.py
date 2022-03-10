from tkinter import *  
import threading
import time
from pynput import keyboard


CAPACITY = int(input('Введите размер буфера: '))

buffer = [-1 for i in range(CAPACITY)]
in_index = 0
out_index = 0

mutex = threading.Semaphore()
empty = threading.Semaphore(CAPACITY)
full = threading.Semaphore(0)


window = Tk()  
window.title("Lab1")  
window.geometry('900x715') 

lbl = Label(window, text="Producer1")  
lbl.grid(column=0, row=0)  


lbl = Label(window, text="Consumer1")  
lbl.grid(column=0, row=1)  

lbl = Label(window, text="Consumer2")  
lbl.grid(column=0, row=2)

lbl = Label(window, text="Consumer3")  
lbl.grid(column=0, row=3)  


p1 = Text(window, height=9.5,width=100)
p1.grid(column=1,row=0)

c1 = Text(window, height=9.5,width=100)
c1.grid(column=1,row=1)

c2 = Text(window, height=9.5,width=100)
c2.grid(column=1,row=2)

c3 = Text(window, height=9.5,width=100)
c3.grid(column=1,row=3)


class Producer(threading.Thread): # Producer Thread Class
  def run(self):
    global CAPACITY, buffer, in_index, out_index
    global mutex, empty, full
    is_cheak = False

    def on_press(key):
        global CAPACITY, buffer, in_index, out_index
        global mutex, empty, full
        
        if key == keyboard.Key.esc:
            is_work = False
            return False 
        
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        
        empty.acquire()
        mutex.acquire()


        buffer[in_index] = k
        p1.delete("end")
        p1.insert('end', k)
        
        in_index = (in_index + 1)%CAPACITY
        
        mutex.release()
        full.release()

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join() 


class Consumer(threading.Thread):
  def run(self):
     
    global CAPACITY, buffer, in_index, out_index, counter
    global mutex, empty, full

    while True:
        full.acquire()
        mutex.acquire()
        if buffer[out_index].isalpha():
            
            item = buffer[out_index]
            out_index = (out_index + 1)%CAPACITY

            c1.delete("end")
            c1.insert('end', item)

            mutex.release()
            empty.release()
        else:
            full.release()
            mutex.release()
            time.sleep(0.5)



class Consumer2(threading.Thread):
  def run(self):
     
    global CAPACITY, buffer, in_index, out_index, counter
    global mutex, empty, full
    while True:
        full.acquire()
        mutex.acquire()
        if buffer[out_index].isdigit():
            
            item = buffer[out_index]
            out_index = (out_index + 1)%CAPACITY

            c2.delete("end")
            c2.insert('end', item)

            mutex.release()
            empty.release()
        else:
            full.release()
            mutex.release()
            time.sleep(0.5)



class Consumer3(threading.Thread):
    def run(self):

        global CAPACITY, buffer, in_index, out_index, counter
        global mutex, empty, full

        while True:
            full.acquire()
            mutex.acquire()
            if not buffer[out_index].isalnum() and buffer[out_index] != '':
                item = buffer[out_index]
                out_index = (out_index + 1)%CAPACITY

                c3.delete("end")
                c3.insert('end', item)

                mutex.release()
                empty.release()
            else:
                full.release()
                mutex.release()
                time.sleep(0.5)


producer = Producer()
consumer = Consumer()
consumer2 = Consumer2()
consumer3 = Consumer3()


consumer.start()
consumer2.start()
consumer3.start()
producer.start()

window.mainloop()

producer.join() # Ожидание завершения потоков
consumer.join()
consumer2.join()
consumer3.join()
