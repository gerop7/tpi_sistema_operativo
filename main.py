import json
from core.process import Process
from core.scheduler import Scheduler
from core.memory_manager import MemoryManager
from core.io_manager import IOManager
from core.operating_system import OperatingSystem

if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)

    scheduler = Scheduler()
    memory = MemoryManager(config["num_frames"])
    io_manager = IOManager(scheduler)
    os = OperatingSystem(scheduler, memory, io_manager)

    # Crear y cargar procesos
    for p_data in config["processes"]:
        process = Process(**p_data)
        os.load_process(process)

    os.run()