from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: float
    popularity: int
    rating: float
    original_index: int


import random

def generate_products(n):
    products = []
    for i in range(n):
        price = round(random.uniform(10, 500), 2)
        popularity = random.randint(1, 10000)
        rating = round(random.uniform(1.0, 5.0), 1)
        products.append(Product(i, f"Product{i}", price, popularity, rating, i))
    return products


def bubble_sort(products, key=lambda x: x.price):
    arr = products[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if key(arr[j]) > key(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def merge_sort(products, key=lambda x: x.price):
    if len(products) <= 1:
        return products
    mid = len(products) // 2
    left = merge_sort(products[:mid], key)
    right = merge_sort(products[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        # <= ensures stability (left item first if equal)
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
def is_sorted(arr, key=lambda x: x.price):
    return all(key(arr[i]) <= key(arr[i+1]) for i in range(len(arr)-1))

def is_stable(original, sorted_list, key=lambda x: x.price):
    from collections import defaultdict
    # map price to queue of indices
    order_map = defaultdict(list)
    for p in original:
        order_map[key(p)].append(p.original_index)

    for p in sorted_list:
        expected = order_map[key(p)].pop(0)
        if expected != p.original_index:
            return False
    return True

import time

def benchmark():
    small_sizes = [10, 50]
    large_sizes = [10000]

    for n in small_sizes:
        print(f"\n=== SMALL DATASET (n={n}) ===")
        data = generate_products(n)

        for name, func in [("BubbleSort", bubble_sort), ("MergeSort", merge_sort)]:
            copy = data[:]  # fresh copy
            start = time.time()
            sorted_data = func(copy, key=lambda x: x.price)
            elapsed = time.time() - start
            print(f"{name}: {elapsed*1000:.3f} ms, Sorted={is_sorted(sorted_data)}, Stable={is_stable(data, sorted_data)}")

    for n in large_sizes:
        print(f"\n=== LARGE DATASET (n={n}) ===")
        data = generate_products(n)

        # Skip bubble sort (too slow)
        start = time.time()
        sorted_data = merge_sort(data, key=lambda x: x.price)
        elapsed = time.time() - start
        print(f"MergeSort: {elapsed:.3f} s, Sorted={is_sorted(sorted_data)}, Stable={is_stable(data, sorted_data)}")

if __name__ == "__main__":
    benchmark()
