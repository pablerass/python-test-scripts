#!/usr/bin/env python3

import sys
import time
import threading

def main(argv=None):
    # Create queue
    num_threads = 3
    queue = list(range(1, 100))
    results = []

    # Start threads
    thread_list = []
    num_threads = min(num_threads, len(queue))
    print('Starting {i} threads'.format(i=num_threads))
    for thread_number in range(1, num_threads + 1):
        thread = threading.Thread(target=worker,
                                  args=(queue, results, thread_number)),
        thread_list.append(thread)
        thread[0].start()

    # Wait until finished
    for thread in thread_list:
        thread[0].join()
    print('All threads finished')

    # Print result
    print(results)

def worker(queue, results, thread_number=0):
    while queue:
        try:
            value = queue.pop()
            print("Worker {thread} gets {value}".format(thread=thread_number,
                                                        value=value))
            results.append(command(value, thread_number))
        except IndexError:
            continue

def command(value, worker):
    # Take into account that due to Python GIL (global interpreter lock), in
    # current Python 3 versions all threads are executed in the same processor.
    # To avoid this, subprocess module can be used to run external commands and
    # use Python only to manage workers execution and parse results.
    time.sleep(1)
    return { "worker": worker, "value": value }

# Main execution
if (__name__ == "__main__"):
    sys.exit(main())

