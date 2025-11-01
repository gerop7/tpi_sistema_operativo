
import time
from core.process import ProcessState

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

        # Correr hasta que todos terminen
        while len(self.finished) < self.total_processes:
            if self.scheduler.has_ready_process():
                time.sleep(0.05)  # pequeña pausa para dejar mostrar E/S completada
                proc = self.scheduler.dispatch()

                # Si el proceso todavía no ejecutó y requiere E/S inicial
                if getattr(proc, "io_done", False) is False and proc.io_time > 0:
                    self.io.request_io(proc)
                    proc.io_done = True  # marcar que ya se hizo la E/S una vez
                    print(f"[CPU] P{proc.pid} bloqueado por E/S inicial.\n")
                    continue

                # Ejecutar CPU completo (no expropiativo)
                print(f"[CPU] Ejecutando P{proc.pid} (ráfaga total: {proc.cpu_burst})")
                time.sleep(proc.cpu_burst)
                proc.cpu_burst = 0

                # Al terminar CPU, liberar memoria
                proc.state = ProcessState.TERMINATED
                self.memory.free(proc)
                self.finished.append(proc)
                print(f"[CPU] P{proc.pid} finalizado.\n")

                # Al liberar memoria, intentar cargar los que estaban bloqueados
                self._retry_memory()

            else:
                # CPU ociosa → verificar si hay procesos bloqueados por memoria
                self._retry_memory()

        # Fin de simulación
        self.io.stop()
        print("\n========== SIMULACIÓN FINALIZADA ==========\n")
        self.show_summary()

    def show_summary(self):
        print("Procesos finalizados:", [f"P{p.pid}" for p in self.finished])
        print("Estado de la memoria:", self.memory.frames)