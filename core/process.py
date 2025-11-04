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
        
        #agrego cambios, revisar
        self.remaining_burst = cpu_burst #tiempo que le faltaria ejecutar
        self.io_done = False #bandera para ver si ya hizo una E/S
        self.next_io_at = None # para ver en que segundo de su rafaga restante se interrumpe para E/S
        """sirve para que cada proceso recuerde cuanto CPU le queda, si hizo una E/S y en que momento de su rafaga se interrumpe para E/S"""
        

    def __repr__(self):
        return f"P{self.pid}({self.state.value})"