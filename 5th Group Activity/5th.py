import random
import time
from multiprocessing import Process, Queue

# Dataset 
def make_data(n):
    data = []
    for _ in range(n):
        data.append(random.randint(1, 100000)) # Medium dataset
    return data


# Sequential Sort
def merge_sort(arr):
    if len(arr) < 2:
        return arr

    # Split the list into two halves
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])  
    right = merge_sort(arr[mid:]) 

    merged = []  # This will store the merged sort result
    i = 0       
    j = 0       

    # Merge the two sorted halves by comparing elements
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])  
            i += 1
        else:
            merged.append(right[j]) 
            j += 1

    if i < len(left):
        merged += left[i:]

    if j < len(right):
        merged += right[j:]

    return merged


# Sequential Search
def linear_search(arr, target):
    idx = -1
    for i in range(len(arr)):
        if arr[i] == target:
            idx = i
            break
    return idx


# Parallel Sort
def parallel_merge_sort(data):
    # split into 4 parts
    size = len(data)
    step = size // 4

    chunks = []
    start = 0
    for i in range(4):
        if i == 3:
            chunks.append(data[start:])  # last part gets the extra items
        else:
            chunks.append(data[start:start + step])
        start += step

    q = Queue()

    def worker(sub):
        sorted_part = merge_sort(sub)
        q.put(sorted_part)

    procs = []
    for c in chunks:
        p = Process(target=worker, args=(c,))
        procs.append(p)
        p.start()

    results = []
    for _ in procs:
        results.append(q.get())

    for p in procs:
        p.join()

    # merge the sorted parts together
    result = results[0]
    for r in results[1:]:
        result = merge(result, r)

    return result


def merge(a, b):
    res = []
    i = j = 0

    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            res.append(a[i]); i += 1
        else:
            res.append(b[j]); j += 1

    if i < len(a):
        res.extend(a[i:])
    if j < len(b):
        res.extend(b[j:])

    return res

# Parallel Search
def parallel_search(data, target):
    size = len(data)
    step = size // 4
    q = Queue()

    def worker(sub, offset):
        for i, v in enumerate(sub):
            if v == target:
                q.put(i + offset)
                return
        q.put(-1)

    procs = []
    for i in range(4):
        start = i * step
        if i == 3:
            sub = data[start:]
        else:
            sub = data[start:start + step]

        p = Process(target=worker, args=(sub, start))
        procs.append(p)
        p.start()

    found = -1
    for _ in procs:
        res = q.get()
        if res != -1:
            found = res  # last one wins 

    for p in procs:
        p.join()

    return found
 
# Timing
def time_sort(data, use_parallel):
    t0 = time.time()

    if use_parallel:
        parallel_merge_sort(data)
    else:
        merge_sort(data)

    return time.time() - t0


def time_search(data, target, use_parallel):
    t0 = time.time()

    if use_parallel:
        parallel_search(data, target)
    else:
        linear_search(data, target)

    return time.time() - t0