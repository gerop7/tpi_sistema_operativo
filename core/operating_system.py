
import time
from core.process import ProcessState
import random #nuevo

class OperatingSystem:
    def __init__(self, scheduler, memory, io_manager):
        self.scheduler = scheduler
        self.memory = memory
        self.io = io_manager
        self.blocked_for_memory = []
        self.finished = []
        self.total_processes = 0

    def load_process(self, process):
        self.total_processes += 1
        if self.memory.allocate(process, noisy=True):
            self.scheduler.add_process(process)
        else:
            process.state = ProcessState.BLOCKED
            self.blocked_for_memory.append(process)
            print(f"[OS] P{process.pid} bloqueado por falta de memoria.\n")

    def _retry_memory(self):
        for p in self.blocked_for_memory[:]:
            if self.memory.allocate(p, noisy=False):
                self.scheduler.add_process(p)
                self.blocked_for_memory.remove(p)

    def run(self):
        print("\n========== INICIO DE LA SIMULACIÓN ==========\n")

        while len(self.finished) < self.total_processes:
            if self.scheduler.has_ready_process():
                time.sleep(0.05)
                proc = self.scheduler.dispatch()

                # Si tiene E/S pendiente por hacer, elige el segundo aleatorio
                if proc.io_time > 0 and not getattr(proc, "io_done", False):
                    if proc.remaining_burst > 1:
                        proc.next_io_at = random.randint(1, proc.remaining_burst - 1)
                        print(f"[CPU] P{proc.pid} tendrá E/S en t={proc.next_io_at}s de su ráfaga actual.")

                # Si hay E/S planificada
                if proc.next_io_at is not None:
                    print(f"[CPU] Ejecutando P{proc.pid} (Ráfaga = {proc.remaining_burst})")
                    time.sleep(proc.next_io_at)
                    proc.remaining_burst -= proc.next_io_at

                    # Lanzar operación de E/S
                    self.io.request_io(proc)
                    proc.io_done = True
                    proc.next_io_at = None
                    print(f"[CPU] P{proc.pid} bloqueado por E/S.\n")
                    continue  # salta a la siguiente iteración, CPU queda libre

                # Si no hay E/S pendiente o ya volvió del I/O
                if proc.remaining_burst > 0:
                    print(f"[CPU] Ejecutando P{proc.pid} (Ráfaga = {proc.remaining_burst})")
                    time.sleep(proc.remaining_burst)
                    proc.remaining_burst = 0

                # Proceso terminado
                proc.state = ProcessState.TERMINATED
                self.memory.free(proc)
                self.finished.append(proc)
                print(f"[CPU] P{proc.pid} finalizado.\n")

                self._retry_memory()
            else:
                self._retry_memory()

        self.io.stop()
        print("\n========== SIMULACIÓN FINALIZADA ==========\n")
        self.show_summary()

    def show_summary(self):
        print("Procesos finalizados:", [f"P{p.pid}" for p in self.finished])
        print("Estado de la memoria:", self.memory.frames)