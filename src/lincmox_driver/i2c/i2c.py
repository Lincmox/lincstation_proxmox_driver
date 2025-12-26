from threading import Lock
from .i2c_backend import I2CBackend

class I2C:
    def __init__(self, address, backend: I2CBackend):
        self.address = address
        self.backend = backend
        self._lock = Lock()
        self._refcount = 0

    def __enter__(self):
        with self._lock:
            if self._refcount == 0:
                self.backend.open(self.address)
            self._refcount += 1
        return self

    def __exit__(self, exc_type, exc, tb):
        with self._lock:
            self._refcount -= 1
            if self._refcount == 0:
                self.backend.close()
        return False

    def read(self, reg):
        return self.backend.read(self.address, reg)

    def write(self, reg, value):
        self.backend.write(self.address, reg, value)