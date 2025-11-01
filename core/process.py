from enum import Enum

class ProcessState(Enum):
    NEW = "Nuevo"
    READY = "Listo"
    RUNNING = "Ejecutando"
    BLOCKED = "Bloqueado"
    TERMINATED = "Terminado"

class Process:
    def __init__(self, pid, cpu_burst, memory_required, io_time=0):
        self.pid = pid
        self.cpu_burst = cpu_burst
        self.memory_required = memory_required
        self.io_time = io_time
        self.state = ProcessState.NEW

    def __repr__(self):
        return f"P{self.pid}({self.state.value})"