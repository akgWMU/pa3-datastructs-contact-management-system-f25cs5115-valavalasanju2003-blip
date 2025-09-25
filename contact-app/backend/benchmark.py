import random, string, time, tracemalloc
import pandas as pd
import matplotlib.pyplot as plt
from data_structures.contact import Contact
from data_structures.array_store import ArrayStore
from data_structures.linkedlist_store import LinkedListStore
from data_structures.bst_store import BSTStore
from data_structures.hashmap_store import HashMapStore
from data_structures.heap_store import HeapStore
from data_structures.complexities import complexities

stores = {
    "array": ArrayStore,
    "linkedlist": LinkedListStore,
    "bst": BSTStore,
    "hashmap": HashMapStore,
    "heap": HeapStore,
}

def random_contact(i):
    return Contact(f"Name{i}", str(random.randint(1000000000,9999999999)), f"user{i}@mail.com")

def run_benchmarks(n=1000, sizes=[100, 1000, 10000]):
    results = []
    
    for size in sizes:
        for name, cls in stores.items():
            store = cls()
            contacts = [random_contact(i) for i in range(size)]
            
            # Memory tracking
            tracemalloc.start()
            
            # Insert
            start = time.perf_counter()
            for c in contacts:
                store.insert(c)
            insert_time = time.perf_counter() - start

            # Search
            start = time.perf_counter()
            for c in random.sample(contacts, min(50, len(contacts))):
                store.search(c.name)
            search_time = time.perf_counter() - start

            # Delete
            start = time.perf_counter()
            for c in random.sample(contacts, min(50, len(contacts))):
                store.delete(c.name)
            delete_time = time.perf_counter() - start

            # List
            start = time.perf_counter()
            _ = store.list_all()
            list_time = time.perf_counter() - start

            # Memory usage
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            results.append({
                "Data Structure": name,
                "Size": size,
                "Insert Time (s)": insert_time,
                "Search Time (s)": search_time,
                "Delete Time (s)": delete_time,
                "List Time (s)": list_time,
                "Memory (KB)": peak / 1024,
            })
    
    return pd.DataFrame(results)

def plot_benchmarks(df):
    ops = ["Insert Time (s)", "Search Time (s)", "Delete Time (s)", "List Time (s)"]
    for op in ops:
        plt.figure(figsize=(10,6))
        for ds in df["Data Structure"].unique():
            subset = df[df["Data Structure"] == ds]
            plt.plot(subset["Size"], subset[op], marker="o", label=ds)
        plt.title(f"{op} vs Dataset Size")
        plt.xlabel("Dataset Size")
        plt.ylabel(op)
        plt.legend()
        plt.grid(True)
        plt.show()
