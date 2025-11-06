import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

class ThreadPoolMonitor:
    def __init__(self, max_workers=5):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_tasks = 0
        self.completed_tasks = 0
        self.lock = threading.Lock()
    
    def get_available_threads(self):
        """Calculate available threads in the pool"""
        return self.max_workers - self.active_tasks
    
    def get_pool_status(self):
        """Get current status of thread pool"""
        available = self.get_available_threads()
        return {
            'total_threads': self.max_workers,
            'active_threads': self.active_tasks,
            'available_threads': available,
            'completed_tasks': self.completed_tasks,
            'utilization': f"{(self.active_tasks / self.max_workers) * 100:.1f}%"
        }
    
    def print_status(self):
        """Print formatted pool status"""
        status = self.get_pool_status()
        print(f"\n{'='*60}")
        print(f"Thread Pool Status:")
        print(f"  Total Threads: {status['total_threads']}")
        print(f"  Active: {status['active_threads']} | Available: {status['available_threads']}")
        print(f"  Utilization: {status['utilization']}")
        print(f"  Completed Tasks: {status['completed_tasks']}")
        print(f"{'='*60}\n")
    
    def io_operation(self, task_id):
        """Simulate an I/O operation (file read, API call, database query, etc.)"""
        with self.lock:
            self.active_tasks += 1
        
        try:
            # Simulate I/O delay (2-5 seconds)
            duration = random.uniform(2, 5)
            print(f"[Task {task_id}] Started - Available threads: {self.get_available_threads()}")
            
            # Simulate I/O operation
            time.sleep(duration)
            
            result = f"Task {task_id} completed in {duration:.2f}s"
            print(f"[Task {task_id}] Completed")
            
            return result
            
        finally:
            with self.lock:
                self.active_tasks -= 1
                self.completed_tasks += 1
    
    def submit_task(self, task_id):
        """Submit a task to the thread pool with availability check"""
        available = self.get_available_threads()
        
        if available > 0:
            print(f"✓ Submitting Task {task_id} (Available threads: {available})")
            future = self.executor.submit(self.io_operation, task_id)
            return future
        else:
            print(f"✗ Pool full! Task {task_id} waiting... (Available threads: {available})")
            # Still submit, but it will queue
            future = self.executor.submit(self.io_operation, task_id)
            return future
    
    def shutdown(self):
        """Shutdown the thread pool"""
        print("\nShutting down thread pool...")
        self.executor.shutdown(wait=True)
        print("All tasks completed. Thread pool shut down.")


def main():
    # Create thread pool with 5 workers
    pool = ThreadPoolMonitor(max_workers=5)
    
    print("Thread Pool I/O Operation Monitor")
    print("Creating pool with 5 threads...\n")
    
    # Initial status
    pool.print_status()
    
    # Submit 15 tasks to demonstrate pool behavior
    futures = []
    for i in range(15):
        future = pool.submit_task(i + 1)
        futures.append(future)
        
        # Show status every 3 tasks
        if (i + 1) % 3 == 0:
            pool.print_status()
            time.sleep(0.5)  # Small delay between batches
    
    # Monitor completion
    print("\n" + "="*60)
    print("Monitoring task completion...")
    print("="*60)
    
    for future in as_completed(futures):
        result = future.result()
        pool.print_status()
    
    # Final status
    print("\n" + "="*60)
    print("All tasks submitted and completed!")
    pool.print_status()
    
    # Cleanup
    pool.shutdown()


if __name__ == "__main__":
    main()