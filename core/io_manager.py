import threading, time
from core.process import ProcessState

class IOManager:
    def __init__(self, scheduler):
        self.buffer = []                  # Cola de E/S
        self.MAX_SIZE = 3
        self.mutex = threading.Semaphore(1)
        self.empty = threading.Semaphore(self.MAX_SIZE)
        self.full = threading.Semaphore(0)
        self.scheduler = scheduler
        self.active = True

        # Inicia hilo del consumidor (simulación de dispositivo)
        t = threading.Thread(target=self.handle_io)
        t.daemon = True
        t.start()

    def request_io(self, process):
        """Proceso (productor) solicita E/S"""
        self.empty.acquire()
        self.mutex.acquire()
        self.buffer.append(process)
        print(f"[IO] P{process.pid} genera petición de E/S.")
        self.mutex.release()
        self.full.release()
        process.state = ProcessState.BLOCKED

    def handle_io(self):
        """Consumidor que procesa las peticiones"""
        while self.active:
            self.full.acquire()
            self.mutex.acquire()
            if not self.buffer:
                self.mutex.release()
                continue
            process = self.buffer.pop(0)
            print(f"[IO] Procesando E/S de P{process.pid} ({process.io_time}s)")
            self.mutex.release()
            self.empty.release()

            time.sleep(process.io_time)
            process.state = ProcessState.READY
            self.scheduler.add_process(process)
            print(f"[IO] E/S de P{process.pid} completada, vuelve a listos.")