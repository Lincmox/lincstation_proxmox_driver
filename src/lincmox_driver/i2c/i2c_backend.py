from abc import ABC, abstractmethod


class I2CBackend(ABC):

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def read(self, address, reg):
        pass

    @abstractmethod
    def write(self, address, reg, value):
        pass