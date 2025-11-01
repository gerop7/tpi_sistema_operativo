# core/io_manager.py
import threading, time
from core.process import ProcessState

class IOManager:
    def __init__(self, scheduler):
        self.buffer = []
        self.MAX_SIZE = 3
        self.mutex = threading.Semaphore(1)
        self.empty = threading.Semaphore(self.MAX_SIZE)
        self.full  = threading.Semaphore(0)
        self.scheduler = scheduler
        self.active = True
        self._worker = threading.Thread(target=self.handle_io, daemon=True)
        self._worker.start()

    def request_io(self, process):
        self.empty.acquire()
        self.mutex.acquire()
        self.buffer.append(process)
        print(f"[IO] P{process.pid} genera petición de E/S.")
        self.mutex.release()
        self.full.release()
        process.state = ProcessState.BLOCKED

    def handle_io(self):
        while True:
            self.full.acquire()
            if not self.active and not self.buffer:
                break
            self.mutex.acquire()
            proc = self.buffer.pop(0) if self.buffer else None
            self.mutex.release()
            self.empty.release()
            if proc is None:
                continue
            print(f"[IO] Procesando E/S de P{proc.pid} ({proc.io_time}s)")
            time.sleep(proc.io_time)
            proc.state = ProcessState.READY
            self.scheduler.add_process(proc)
            print(f"[IO] E/S de P{proc.pid} completada, vuelve a listos.")

    def has_pending(self):
        # ¿Queda trabajo de E/S por hacer?
        return len(self.buffer) > 0

    def stop(self):
        # Cerrar el hilo limpiamente
        self.active = False
        self.full.release()   # despertar al consumidor si está esperando
        self._worker.join(timeout=1)