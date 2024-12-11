from datetime import datetime
from multiprocessing import Process, Queue, cpu_count
from concurrent.futures import ProcessPoolExecutor

def split_range(start, end, parts):
    step = (end - start + 1) // parts
    ranges = []

    for i in range(parts):
        range_start = start + i * step
        range_end = start + (i + 1) * step - 1 if i < parts - 1 else end
        ranges.append((range_start, range_end))

    return ranges

def is_odd(number):
    return number % 2 != 0

def recurs_calc_wrapper(from_number, to_number):
    for i in range(from_number, to_number + 1):
        recursive_calculation(i)

''' Якщо число парне, то ділимо його на 2, а якщо непарне, то множимо на 3 і додаємо 1 (отримуємо 3n + 1). 
    Над отриманим числом виконуємо ті ж самі дії, і так далі. '''
def recursive_calculation(number):
    # Calculation in the recursive way
    if number == 1:
        # print('We have reached 1. The theorem works!')
        return # 'OK, confirmed'
    if is_odd(number):
        number = int(number * 3 + 1)
    else:
        number = int(number / 2)
    return recursive_calculation(number)

def nonrecurs_calc_wrapper(from_number, to_number):
    for i in range(from_number, to_number + 1):
        non_recursive_calculation(i)

def non_recursive_calculation(number):
    while number != 1:
        if is_odd(number):
            number = int(number * 3 + 1)
        else:
            number = int(number / 2)


def variant1(number, calculation_function):
    physical_cores = cpu_count()
    range_for_counting = split_range(1, number, physical_cores)
    processes = []
    for i in range_for_counting:
        process = Process(target=calculation_function, args=(i[0], i[1]))
        processes.append(process)
        process.start()
        if len(processes) >= physical_cores:
            for p in processes:
                p.join()
            processes = []

    for p in processes:
        p.join()

    return


def variant2(number, calculation_function):
    # with PoolExecutor
    physical_cores = cpu_count()
    range_for_counting = split_range(1, number, physical_cores)
    with ProcessPoolExecutor(max_workers=physical_cores) as executor:
        for i in range_for_counting:
            executor.map(calculation_function, range(i[0], i[1]))
    return

#-------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    number = 1000000 # 1000000000

    # Please feel free to comment/uncomment the necessary parts of code below
    # calculation with 1 process, recursive  --------------------------------------
    start_time = datetime.now()
    recurs_calc_wrapper(1, number + 1)
    end_time = datetime.now()
    print(f"Time taken (1 process, recursive version): {end_time - start_time}")
    print("---------------------------------------------------------------------")

    # # calculation with 1 process, non-recursive  -----------------------------------
    start_time = datetime.now()
    nonrecurs_calc_wrapper(1, number + 1)
    end_time = datetime.now()
    print(f"Time taken (1 process, non-recursive version): {end_time - start_time}")
    print("---------------------------------------------------------------------")

    # calculation with many process, recursive  --------------------------------
    start_time = datetime.now()
    variant1(number, recurs_calc_wrapper)
    end_time = datetime.now()
    print(f"Time taken ({cpu_count()} processes, recursive version): {end_time - start_time}")
    print("---------------------------------------------------------------------")

    # calculation with many process, non-recursive  --------------------------------
    start_time = datetime.now()
    variant1(number, nonrecurs_calc_wrapper)
    end_time = datetime.now()
    print(f"Time taken ({cpu_count()} processes, non-recursive version): {end_time - start_time}")
    print("---------------------------------------------------------------------")

    # calculation with many process, with PoolExecutor, recursive  -------------------
    start_time = datetime.now()
    variant1(number, recurs_calc_wrapper)
    end_time = datetime.now()
    print(f"Time taken ({cpu_count()} processes, with PoolExecutor, recursive version): {end_time - start_time}")
    print("---------------------------------------------------------------------")

    # calculation with many process, with PoolExecutor, non-recursive  --------------
    start_time = datetime.now()
    variant1(number, nonrecurs_calc_wrapper)
    end_time = datetime.now()
    print(f"Time taken ({cpu_count()} processes, with PoolExecutor, non-recursive version): {end_time - start_time}")
    print("---------------------------------------------------------------------")
