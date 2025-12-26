import json
import os
from threading import Lock
from .i2c_backend import I2CBackend

class I2CBackendMock(I2CBackend):
    _lock = Lock()
    _file_path = "/tmp/lincstation_mock_registers.json"  # fichier persistant

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.registers = self._load_registers()

    def _load_registers(self):
        if os.path.exists(self._file_path):
            try:
                with open(self._file_path, "r") as f:
                    return {int(k): v for k, v in json.load(f).items()}
            except Exception:
                return {}
        return {}

    def _save_registers(self):
        with self._lock:
            with open(self._file_path, "w") as f:
                json.dump({str(k): v for k, v in self.registers.items()}, f)

    def open(self, address):
        if self.verbose:
            print(f"[MOCK] open device 0x{address:02X}")

    def close(self):
        if self.verbose:
            print("[MOCK] close device")

    def read(self, address, reg):
        value = self.registers.get(reg, 0x00)
        if self.verbose:
            print(f"[MOCK] READ 0x{reg:02X} → 0x{value:02X}")
        return value

    def write(self, address, reg, value):
        value &= 0xFF
        self.registers[reg] = value
        self._save_registers()  # Sauvegarde persistante
        if self.verbose:
            print(f"[MOCK] WRITE 0x{reg:02X} ← 0x{value:02X}")