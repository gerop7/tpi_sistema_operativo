class MemoryManager:
    """
    Clase que gestiona la memoria principal del sistema simulando un esquema de
    paginación simple. Administra la asignación y liberación de marcos (frames)
    para los procesos cargados en ejecución.
    """

    def __init__(self, num_frames):
        """
        Inicializa la memoria principal con una cantidad fija de marcos vacíos.

        Parámetros:
        ------------
        num_frames : int
            Número total de marcos disponibles en la memoria.
        """
        self.frames = [None] * num_frames  # Cada posición representa un marco de memoria libre u ocupado


    def allocate(self, process, noisy=True):
        """
        Intenta asignar marcos de memoria al proceso indicado.

        Parámetros:
        ------------
        process : Process
            Proceso que solicita ocupar memoria.
        noisy : bool, opcional
            Si es True, muestra mensajes en consola. Usado para modo “verbose”.

        Retorna:
        --------
        bool
            True si el proceso pudo ser cargado en memoria.
            False si no hay suficientes marcos disponibles (queda bloqueado).
        """
        # Busca índices de marcos libres
        free_frames = [i for i, f in enumerate(self.frames) if f is None]

        # Si no hay suficientes marcos, el proceso se bloquea
        if len(free_frames) < process.memory_required:
            if noisy:
                print(f"[MEMORIA] No hay espacio para P{process.pid}. Queda bloqueado.")
            return False

        # Asigna los marcos libres necesarios al proceso
        for i in free_frames[:process.memory_required]:
            self.frames[i] = process.pid

        print(f"[MEMORIA] P{process.pid} asignado a marcos {free_frames[:process.memory_required]}")
        return True


    def free(self, process):
        """
        Libera los marcos ocupados por el proceso cuando finaliza su ejecución.

        Parámetros:
        ------------
        process : Process
            Proceso finalizado que libera la memoria.
        """
        # Recorre la memoria y libera los marcos pertenecientes al proceso
        for i in range(len(self.frames)):
            if self.frames[i] == process.pid:
                self.frames[i] = None

        print(f"\n[MEMORIA] P{process.pid} liberó sus marcos.")