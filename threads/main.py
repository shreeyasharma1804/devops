import threading
import time

def worker(thread_id):
    """Worker function that runs in a while loop"""
    iteration = 0
    while True:
        iteration += 1
        print(f"Thread {thread_id}: Iteration {iteration}")
        time.sleep(1)
    print(f"Thread {thread_id}: Stopping")

def main():
    
    threads = []
    print("Starting 10 threads...")
    
    for i in range(10):
        thread = threading.Thread(target=worker, args=(i,))
        thread.start()
        threads.append(thread)
    
    print("All threads started. Press Ctrl+C to stop.\n")
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()