import time
from core.process import ProcessState

class OperatingSystem:
    def __init__(self, scheduler, memory, io_manager):
        self.scheduler = scheduler
        self.memory = memory
        self.io = io_manager
        self.blocked_for_memory = []
        self.finished = []

    def load_process(self, process):
        if self.memory.allocate(process):
            self.scheduler.add_process(process)
        else:
            process.state = ProcessState.BLOCKED
            self.blocked_for_memory.append(process)
            print(f"[OS] P{process.pid} bloqueado por falta de memoria.")

    def run(self):
        print("\n========== INICIO DE LA SIMULACIÓN ==========\n")
        while self.scheduler.has_ready_process():
            process = self.scheduler.dispatch()
            print(f"[CPU] Ejecutando P{process.pid} (rafaga restante: {process.cpu_burst})")

            time.sleep(1)  # Simula ejecución CPU
            process.cpu_burst -= 1

            if process.cpu_burst == 0:
                process.state = ProcessState.TERMINATED
                self.memory.free(process)
                self.finished.append(process)
                print(f"[CPU] P{process.pid} finalizado.")
            else:
                # Cada proceso hace una operación de E/S entre ráfagas
                self.io.request_io(process)

            # Intentar cargar procesos bloqueados por memoria
            for p in self.blocked_for_memory[:]:
                if self.memory.allocate(p):
                    self.scheduler.add_process(p)
                    self.blocked_for_memory.remove(p)
        print("\n========== SIMULACIÓN FINALIZADA ==========\n")
        self.show_summary()

    def show_summary(self):
        print("Procesos finalizados:", [f"P{p.pid}" for p in self.finished])
        print("Estado de la memoria:", self.memory.frames)