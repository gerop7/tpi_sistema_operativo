class MemoryManager:
    def __init__(self, num_frames):
        self.frames = [None] * num_frames

    def allocate(self, process):
        free_frames = [i for i, f in enumerate(self.frames) if f is None]
        if len(free_frames) < process.memory_required:
            print(f"[MEMORIA] No hay espacio para P{process.pid}. Queda bloqueado.")
            return False
        for i in free_frames[:process.memory_required]:
            self.frames[i] = process.pid
        print(f"[MEMORIA] P{process.pid} asignado a marcos {free_frames[:process.memory_required]}")
        return True

    def free(self, process):
        for i in range(len(self.frames)):
            if self.frames[i] == process.pid:
                self.frames[i] = None
        print(f"[MEMORIA] P{process.pid} liberó sus marcos.")