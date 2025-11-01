from collections import deque
from core.process import ProcessState

class Scheduler:
    def __init__(self):
        self.ready_queue = deque()

    def add_process(self, process):
        process.state = ProcessState.READY
        self.ready_queue.append(process)
        print(f"[SCHEDULER] P{process.pid} agregado a cola de listos.")

    def dispatch(self):
        if not self.ready_queue:
            return None
        process = self.ready_queue.popleft()
        process.state = ProcessState.RUNNING
        print(f"[SCHEDULER] P{process.pid} pasa a ejecución.")
        return process

    def has_ready_process(self):
        return len(self.ready_queue) > 0