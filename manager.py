from multiprocessing import Process, Queue
from scraper import BookScraper
import time

class ScraperProcess(Process):
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        scraper = BookScraper()
        while not self.task_queue.empty():
            try:
                url = self.task_queue.get_nowait()
                data = scraper.scrape_book(url)
                self.result_queue.put(data)
            except Exception as e:
                print(f"Error in process {self.pid}: {e}")
                break
        scraper.close()

class ProcessManager:
    def __init__(self, urls, num_processes=3):
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.processes = []
        self.num_processes = num_processes

        for url in urls:
            self.task_queue.put(url)

    def start_processes(self):
        for _ in range(self.num_processes):
            p = ScraperProcess(self.task_queue, self.result_queue)
            p.start()
            self.processes.append(p)

    def monitor_processes(self):
        while not self.task_queue.empty():
            for i, p in enumerate(self.processes):
                if not p.is_alive():
                    print(f"Process {p.pid} died. Restarting...")
                    new_p = ScraperProcess(self.task_queue, self.result_queue)
                    new_p.start()
                    self.processes[i] = new_p
            time.sleep(2)

    def gather_results(self):
        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get())
        return results

    def run(self):
        self.start_processes()
        self.monitor_processes()
        for p in self.processes:
            p.join()
        return self.gather_results()