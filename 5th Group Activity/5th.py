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

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # leftover elements
    if i < len(left):
        merged += left[i:]
    if j < len(right):
        merged += right[j:]

    return merged

