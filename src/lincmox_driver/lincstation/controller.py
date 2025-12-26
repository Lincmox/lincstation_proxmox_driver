from lincmox_driver.i2c import I2C, I2CBackendSMBus, I2CBackendMock
from .config import LincStationConfig, LincStationLedConfig, LincStationStripConfig, MASK_LED_BLINK
from .state import LincStationState

class LincStationController:
    _I2C_ADDRESS = 0x26
    
    def __init__(self, simulation: bool = False):
        # self.state = LincStationState()
        if simulation:
            i2c_backend = I2CBackendMock(verbose=True)
        else:
            i2c_backend = I2CBackendSMBus()
        self.i2c = I2C(self._I2C_ADDRESS, i2c_backend)
        self.simulation = simulation

    def _toggle_led(self, target, action):
        with self.i2c:
            self.i2c.write(target.value.reg_blink, MASK_LED_BLINK[action])

    def _switch_on_led(self, target, color):
        with self.i2c:
            self.i2c.write(target.value.reg_on, target.value.mask_color.get(color))
        # self.state.update(target.name, "on", True)
        # current_color = self.state.get_sub(target.name, "color")
        # new_color = color if current_color == "none" else "orange"
        # self.state.update(target.name, "color", new_color)

    def _switch_off_led(self, target, color):
        with self.i2c:
            self.i2c.write(target.value.reg_off, target.value.mask_color.get(color))
        # self.state.update(target.name, "on", False)
        # current_color = self.state.get_sub(target.name, "color")
        # if current_color == "orange" and color == "red":
        #     new_color = "white"
        # elif current_color == "orange" and color == "white":
        #     new_color = "red"
        # elif current_color != "orange":
        #     new_color = "none"
        # self.state.update(target.name, "color", new_color)

    def _set_led(self, target, action, color):
        color_mask = target.value.mask_color.get(color)
        if color_mask is None:
            raise ValueError(f"Invalid color for {target.name} LED")
        if action == "on":
            self._switch_on_led(target, color)
        elif action == "off":
            self._switch_off_led(target, color)
        else:
            raise ValueError("Invalid action (use 'on' or 'off')")

    def toggle_power_led(self, action):
        self._toggle_led(LincStationConfig.POWER, action)
    
    def set_power_led(self, action, color):
        self._set_led(LincStationConfig.POWER, action, color)

    def toggle_sata_led(self, ssd_num, action):
        if ssd_num == 1:
            self._toggle_led(LincStationConfig.SATA_1, action)
        elif ssd_num == 2:
            self._toggle_led(LincStationConfig.SATA_2, action)
        else:
            raise ValueError("Invalid SSD number (1-2)")
    
    def set_sata_led(self, ssd_num, action, color):
        if ssd_num == 1:
            self._set_led(LincStationConfig.SATA_1, action, color)
        elif ssd_num == 2:
            self._set_led(LincStationConfig.SATA_2, action, color)
        else:
            raise ValueError("Invalid SSD number (1-2)")

    def toggle_network_led(self, action):
        self._toggle_led(LincStationConfig.NETWORK, action)

    def set_network_led(self, action, color):
        self._set_led(LincStationConfig.NETWORK, action, color)

    def toggle_nvme_led(self, nvme_num, action):
        if nvme_num == 1:
            self._toggle_led(LincStationConfig.NVME_1, action)
        elif nvme_num == 2:
            self._toggle_led(LincStationConfig.NVME_2, action)
        elif nvme_num == 3:
            self._toggle_led(LincStationConfig.NVME_3, action)
        elif nvme_num == 4:
            self._toggle_led(LincStationConfig.NVME_4, action)
        else:
            raise ValueError("Invalid NVMe number (1-4)")

    def set_nvme_led(self, nvme_num, action, color):
        if nvme_num == 1:
            self._set_led(LincStationConfig.NVME_1, action, color)
        elif nvme_num == 2:
            self._set_led(LincStationConfig.NVME_2, action, color)
        elif nvme_num == 3:
            self._set_led(LincStationConfig.NVME_3, action, color)
        elif nvme_num == 4:
            self._set_led(LincStationConfig.NVME_4, action, color)
        else:
            raise ValueError("Invalid NVMe number (1-4)")

    def set_strip_animation(self, animation):
        with self.i2c:
            self.i2c.write(LincStationConfig.STRIP.value.reg_animation, LincStationConfig.STRIP.value.mask_animation[animation])
        # self.state.update(LincStationConfig.STRIP.name, "animation", animation)

    def set_strip_brightness(self, value):
        with self.i2c:
            self.i2c.write(LincStationConfig.STRIP.value.reg_brightness, value)
        # self.state.update(LincStationConfig.STRIP.name, "brightness", value)
    
    def set_strip_color(self, r, g, b):
        with self.i2c:
            self.i2c.write(LincStationConfig.STRIP.value.reg_red, r)
            self.i2c.write(LincStationConfig.STRIP.value.reg_green, g)
            self.i2c.write(LincStationConfig.STRIP.value.reg_blue, b)

    def set_strip_first_loop_color(self, r, g, b):
        with self.i2c:
            self.i2c.write(LincStationConfig.STRIP.value.reg_first_loop_red, r)
            self.i2c.write(LincStationConfig.STRIP.value.reg_first_loop_green, g)
            self.i2c.write(LincStationConfig.STRIP.value.reg_first_loop_blue, b)

    def set_strip_second_loop_color(self, r, g, b):
        with self.i2c:
            self.i2c.write(LincStationConfig.STRIP.value.reg_second_loop_red, r)
            self.i2c.write(LincStationConfig.STRIP.value.reg_second_loop_green, g)
            self.i2c.write(LincStationConfig.STRIP.value.reg_second_loop_blue, b)

    def reset_leds(self):
        with self.i2c:
            self.set_power_led("off", "white")
            self.set_power_led("off", "red")
            self.set_network_led("off", "white")
            self.set_network_led("off", "red")
            for i in range(1, 3):
                self.set_sata_led(i, "off", "white")
                self.set_sata_led(i, "off", "red")
            for i in range(1, 5):
                self.set_nvme_led(i, "off", "white")
                self.set_nvme_led(i, "off", "red")

    def reset_strip(self):
        with self.i2c:
            self.set_strip_animation("off")
            self.set_strip_brightness(0)
            self.set_strip_color(0, 0, 0)
            self.set_strip_first_loop_color(0, 0, 0)
            self.set_strip_second_loop_color(0, 0, 0)

    def reset(self):
        self.reset_leds()
        self.reset_strip()

    def __str__(self):
        with self.i2c:
            lines = [f"[I2C Device 0x{self._I2C_ADDRESS:02X}]"]

            # for target in LincStationConfig:
            #     cfg = target.value
            #     if isinstance(cfg, LincStationLedConfig):
            #         try:
            #             val_on = self.i2c.read(cfg.reg_on)
            #             val_off = self.i2c.read(cfg.reg_off)
            #             val_blink = self.i2c.read(cfg.reg_blink)

            #             colors_state = []
            #             for name, mask in cfg.mask_color.items():
            #                 if val_off & mask:
            #                     state = "OFF"
            #                 elif val_on & mask:
            #                     state = "ON"
            #                 else:
            #                     state = "OFF"
            #                 colors_state.append(f"{name}={state}")

            #             blink = " BLINK" if val_blink else ""
            #             lines.append(f"{cfg.label:10}: {', '.join(colors_state)}{blink}")

            #         except Exception:
            #             lines.append(f"{cfg.label:10}: registre(s) illisible(s)")

            #     elif isinstance(cfg, LincStationStripConfig):
            #         try:
            #             val_anim = self.i2c.read(cfg.reg_animation)
            #             val_bright = self.i2c.read(cfg.reg_brightness)
            #             val_r = self.i2c.read(cfg.reg_red)
            #             val_g = self.i2c.read(cfg.reg_green)
            #             val_b = self.i2c.read(cfg.reg_blue)

            #             anim_name = next(
            #                 (name for name, mask in cfg.mask_animation.items() if val_anim & mask),
            #                 "unknown"
            #             )

            #             lines.append(
            #                 f"{cfg.label:10}: Animation={anim_name:6}, Brightness={val_bright:3}, "
            #                 f"RGB=({val_r:3},{val_g:3},{val_b:3})"
            #             )
            #         except Exception:
            #             lines.append(f"{cfg.label:10}: registre(s) illisible(s)")

            return "\n".join(lines)