from collections import deque
from core.process import ProcessState

class Scheduler:
    """
    Clase que representa el planificador de procesos del sistema operativo.
    Administra la cola de listos y aplica el algoritmo de planificación FCFS
    (First Come, First Served) sin expropiación."""
    def __init__(self):
        """
        Inicializa el planificador creando la cola de listos (ready queue).
        Se utiliza una estructura 'deque' (cola doble) para permitir inserciones
        y extracciones eficientes en los extremos."""
        self.ready_queue = deque()


    def add_process(self, process):
        """
        Agrega un proceso a la cola de listos.
        Parámetros:
        process,  Proceso que pasa al estado READY, esperando ser ejecutado por la CPU.

        Efectos:
        Cambia el estado del proceso a READY.
        Inserta el proceso al final de la cola."""
        process.state = ProcessState.READY
        self.ready_queue.append(process)
        print(f"[SCHEDULER] P{process.pid} agregado a cola de listos.\n")


    def dispatch(self):
        """
        Despacha el siguiente proceso de la cola de listos a ejecución.
        Retorna:
        Process | None
            Devuelve el proceso que pasará al estado RUNNING.
            Si la cola está vacía, retorna None.
            
        Efectos:
        - Cambia el estado del proceso a RUNNING.
        - Lo elimina de la cola de listos."""
        if not self.ready_queue:
            return None

        process = self.ready_queue.popleft()
        process.state = ProcessState.RUNNING
        print(f"[SCHEDULER] P{process.pid} pasa a ejecución.")
        return process


    def has_ready_process(self):
        """Verifica si hay procesos disponibles para ejecutar.
        Retorna:
            True si existen procesos en la cola de listos.
            False si la cola está vacía."""
        return len(self.ready_queue) > 0