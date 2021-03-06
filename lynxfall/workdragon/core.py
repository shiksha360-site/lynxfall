"""
Work in progress worker management for lynxfall
Note: This will only handle startup/shutdown and other tasks, not micromanaging individual workers. 
Stats and error handling is a maybe that will be implemented after core functionality
Worker-specific tasks are another maybe unless that task is done via redis PUBSUB or other as rabbit is round-robin so not all workers get every task
Workdragon will have a redis pubsub protocol for external management
Support for windows/mac is not planned as of right now.
"""
import os
import subprocess
import threading

class Worker():
    """Represents a worker"""
    def __init__(self, worker_num, process, thread):
        self.process = process
        self.worker_num = worker_num
        self.thread = thread
    
class WorkDragon():
    """WorkDragon main class"""
    def __init__(self, launcher):
        self.workers = []
        self.launcher = launcher
        self.log_workers = True
        self.workers_to_log = []
    
    def worker_log(self, wnum):
        """Returns worker log function"""
        def _log(proc):
            for line in iter(proc.stdout.readline, b''):
                line = line.decode('utf-8')
                if int(wnum) in self.workers_to_log and self.log_workers:
                    print(f"{wnum}: {line}", end='')
        return _log
    
    def new_worker(self): 
        """Creates a new worker"""
        wnum = len(self.workers) + 1
        proc = subprocess.Popen(['python3', '-u', self.launcher],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=dict(os.environ, LYNXFALL_WORKER_NUM=str(wnum))
        )
        t = threading.Thread(target=self.worker_log(wnum), args=(proc,))
        self.workers_to_log.append(wnum)
        t.start()
        self.workers.append(Worker(wnum, proc, t))
