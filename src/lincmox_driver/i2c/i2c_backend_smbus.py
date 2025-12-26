import subprocess
from smbus2 import SMBus
from .i2c_backend import I2CBackend


class I2CBackendSMBus(I2CBackend):
    def __init__(self, max_bus=5):
        self.max_bus = max_bus
        self.bus = None
        self.bus_id = None

    def open(self, address):
        if self.bus is None:
            if self.bus_id is None:
                self.bus_id = self._find_bus_id(address)
            self.bus = SMBus(self.bus_id)

    def close(self):
        if self.bus:
            self.bus.close()
            self.bus = None

    def read(self, address, reg):
        return self.bus.read_byte_data(address, reg)

    def write(self, address, reg, value):
        self.bus.write_byte_data(address, reg, value & 0xFF)

    def _find_bus_id(self, address):
        for i in range(self.max_bus):
            try:
                result = subprocess.run(
                    ["i2cdetect", "-y", str(i)],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                if f" {address:02x} " in result.stdout:
                    return i
            except Exception:
                continue

        raise RuntimeError(f"I2C device 0x{address:02X} not found")