from .i2c_backend import I2CBackend

class I2CBackendMock(I2CBackend):
    def __init__(self, simulator=None, verbose=False):
        self.simulator = simulator
        self.verbose = verbose
        self.registers = {}

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

        if self.simulator:
            self.simulator.update(reg, value)

        if self.verbose:
            print(f"[MOCK] WRITE 0x{reg:02X} ← 0x{value:02X}")