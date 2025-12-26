from lincmox_driver.i2c import I2C, I2CBackendSMBus, I2CBackendMock
from .simulator import LincStationSimulator
from .target import LincStationTarget

class LincStationController:
    _I2C_ADDRESS = 0x26
    
    def __init__(self, simulation: bool = False):
        if simulation:
            self.simulator = LincStationSimulator()
            i2c_backend = I2CBackendMock(simulator=self.simulator, verbose=True)
        else:
            i2c_backend = I2CBackendSMBus()
        self.i2c = I2C(self._I2C_ADDRESS, i2c_backend)
        self.simulation = simulation

    def _switch_on_led(self, reg, color_mask):
        with self.i2c:
            current_value = self.i2c.read(reg)
            new_value = current_value | color_mask
            self.i2c.write(reg, new_value)

    def _switch_off_led(self, reg, color_mask):
        with self.i2c:
            current_value = self.i2c.read(reg)
            new_value = current_value & (~color_mask)
            self.i2c.write(reg, new_value)

    def _set_led(self, target, action, color):
        color_mask = target.value.mask_color.get(color)
        if color_mask is None:
            raise ValueError(f"Invalid color for {target.name} LED")
        if action == "on":
            self._switch_on_led(target.value.reg_on, color_mask)
        elif action == "off":
            self._switch_off_led(target.value.reg_off, color_mask)
        else:
            raise ValueError("Invalid action (use 'on' or 'off')")
    
    def set_power_led(self, action, color):
        self._set_led(LincStationTarget.POWER, action, color)
    
    def set_sata_led(self, ssd_num, action, color):
        if ssd_num == 1:
            self._set_led(LincStationTarget.SATA_1, action, color)
        elif ssd_num == 2:
            self._set_led(LincStationTarget.SATA_2, action, color)
        else:
            raise ValueError("Invalid SSD number (1-2)")

    def set_network_led(self, action, color):
        self._set_led(LincStationTarget.NETWORK, action, color)

    def set_nvme_led(self, nvme_num, action, color):
        if nvme_num == 1:
            self._set_led(LincStationTarget.NVME_1, action, color)
        elif nvme_num == 2:
            self._set_led(LincStationTarget.NVME_2, action, color)
        elif nvme_num == 3:
            self._set_led(LincStationTarget.NVME_3, action, color)
        elif nvme_num == 4:
            self._set_led(LincStationTarget.NVME_4, action, color)
        else:
            raise ValueError("Invalid NVMe number (1-4)")

    def set_strip_animation(self, animation):
        with self.i2c:
            self.i2c.write(LincStationTarget.STRIP.value.reg_animation, LincStationTarget.STRIP.value.mask_animation[animation])

    def set_strip_brightness(self, value):
        with self.i2c:
            self.i2c.write(LincStationTarget.STRIP.value.reg_brightness, value)
    
    def set_strip_color(self, r, g, b):
        with self.i2c:
            self.i2c.write(LincStationTarget.STRIP.value.reg_red, r)
            self.i2c.write(LincStationTarget.STRIP.value.reg_green, g)
            self.i2c.write(LincStationTarget.STRIP.value.reg_blue, b)

    def set_strip_first_loop_color(self, r, g, b):
        with self.i2c:
            self.i2c.write(LincStationTarget.STRIP.value.reg_first_loop_red, r)
            self.i2c.write(LincStationTarget.STRIP.value.reg_first_loop_green, g)
            self.i2c.write(LincStationTarget.STRIP.value.reg_first_loop_blue, b)

    def set_strip_second_loop_color(self, r, g, b):
        with self.i2c:
            self.i2c.write(LincStationTarget.STRIP.value.reg_second_loop_red, r)
            self.i2c.write(LincStationTarget.STRIP.value.reg_second_loop_green, g)
            self.i2c.write(LincStationTarget.STRIP.value.reg_second_loop_blue, b)

    def __str__(self):
        if self.simulation:
            return str(self.simulator)
        else:
            return "Lincmox is running in real mode."