import json
from core.process import Process
from core.scheduler import Scheduler
from core.memory_manager import MemoryManager
from core.io_manager import IOManager
from core.operating_system import OperatingSystem

if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)

    num = config["num_frames"]
    buffer_size = config["io_buffer_size"]

    scheduler = Scheduler()
    memory = MemoryManager(num)
    io_manager = IOManager(scheduler, config["io_buffer_size"])
    os = OperatingSystem(scheduler, memory, io_manager)

    print("[FRAMES] = ",num)
    print("[IO BUFFER SIZE] = ",buffer_size)

    # Crear y cargar procesos
    for p_data in config["processes"]:
        process = Process(**p_data)
        os.load_process(process)

    os.run()