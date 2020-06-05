from concurrent.futures import ThreadPoolExecutor

def task():
    print("Executing our Task")
    result = 0
    i = 0
    for i in range(10000000):
        result = result + i
    print("I: {}".format(result))

def main():
    executor = ThreadPoolExecutor(max_workers=100)
    task1 = executor.submit(task)
    task2 = executor.submit(task)


if __name__ == '__main__':
    main()