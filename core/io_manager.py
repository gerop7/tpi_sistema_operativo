import threading, time
from core.process import ProcessState

class IOManager:
    def __init__(self, scheduler, buffer_size):
        self.buffer = []
        self.MAX_SIZE = buffer_size
        self.mutex = threading.Semaphore(1)
        self.empty = threading.Semaphore(self.MAX_SIZE)
        self.full  = threading.Semaphore(0)
        self.scheduler = scheduler
        self.active = True
        self._worker = threading.Thread(target=self.handle_io, daemon=True)
        self._worker.start()

    def request_io(self, process):
        if len(self.buffer) >= self.MAX_SIZE:
            print(f"[IO] Búfer lleno. P{process.pid} espera a que se libere espacio.")

        self.empty.acquire()                # Espera hasta que haya espacio disponible
        self.mutex.acquire()                # Entra en sección crítica
        self.buffer.append(process)         # Agrega proceso al buffer
        print(f"[IO] P{process.pid} genera petición de E/S.")
        self.mutex.release()                # Sale de la sección crítica
        self.full.release()                 # Avisa al consumidor que hay algo que procesar
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
        return len(self.buffer) > 0

    def stop(self):
        # Cerrar el hilo limpiamente
        self.active = False
        self.full.release()   # despertar al consumidor si está esperando
        self._worker.join(timeout=1)