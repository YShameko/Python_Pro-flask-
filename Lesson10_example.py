# import os
#
# # Кількість потоків (логічних процесорів)
# logical_processors = os.cpu_count()
# print(f"Кількість потоків (логічних процесорів): {logical_processors}")
# print("--------------------------------------------------------------------------")
# import psutil
#
# # Кількість фізичних ядер
# physical_cores = psutil.cpu_count(logical=False)
# # Кількість потоків (логічних процесорів)
# logical_processors = psutil.cpu_count(logical=True)
#
# print(f"Кількість фізичних ядер: {physical_cores}")
# print(f"Кількість потоків (логічних процесорів): {logical_processors}")
from datetime import datetime
# from multiprocessing import Process
# import os
#
# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())
#
# def f(name):
#     info('function f')
#     print('hello', name)
#
# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()
# ------------------------------------------------------------------------------
from multiprocessing import Process, Queue
from threading import Thread

def is_lucky(ticket_number):
    half1 = ticket_number[:len(ticket_number) // 2]
    half2 = ticket_number[len(ticket_number) // 2:]
    sum_half1 = sum(map(int, half1))
    sum_half2 = sum(map(int, half2))
    return sum_half1 == sum_half2

def partial_count(number_from, number_to, queue_object):
    lucky_numbers_qty = 0
    for i in range(number_from, number_to):
        if is_lucky(str(i).rjust(8, "0")):
            lucky_numbers_qty += 1
    queue_object.put(lucky_numbers_qty)

def counting_with_threads():
    lucky_ticket_numbers = Queue()
    # t1 = Thread(target=partial_count, args=(0, 100000000, lucky_ticket_numbers))
    t1 = Thread(target=partial_count, args=(0, 25000000, lucky_ticket_numbers))
    t2 = Thread(target=partial_count, args=(25000000, 50000000, lucky_ticket_numbers))
    t3 = Thread(target=partial_count, args=(50000000, 75000000, lucky_ticket_numbers))
    t4 = Thread(target=partial_count, args=(75000000, 100000000, lucky_ticket_numbers))
    print("Counting lucky numbers with threads, please wait...")
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    total = 0
    while not lucky_ticket_numbers.empty():
        lucky_tickets_qty = lucky_ticket_numbers.get()
        print(lucky_tickets_qty)
        total += lucky_tickets_qty
    print("Total:",total)

def counting_with_processes():
    lucky_ticket_numbers = Queue()
    t1 = Process(target=partial_count, args=(0, 25000000, lucky_ticket_numbers))
    t2 = Process(target=partial_count, args=(25000000, 50000000, lucky_ticket_numbers))
    t3 = Process(target=partial_count, args=(50000000, 75000000, lucky_ticket_numbers))
    t4 = Process(target=partial_count, args=(75000000, 100000000, lucky_ticket_numbers))
    print("Counting lucky numbers with processes, please wait...")
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    total = 0
    while not lucky_ticket_numbers.empty():
        lucky_tickets_qty = lucky_ticket_numbers.get()
        print(lucky_tickets_qty)
        total += lucky_tickets_qty
    print("Total:",total)

if __name__ == '__main__':
    start_time = datetime.now()
    counting_with_threads()
    end_time = datetime.now()
    print(f"Time taken (with 4 threads): {end_time - start_time}")
    print("---------------------------------------------------------------------")

    start_time = datetime.now()
    counting_with_processes()
    end_time = datetime.now()
    print(f"Time taken (with 4 processes): {end_time - start_time}")
