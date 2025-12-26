class LincStationSimulator:
    def __init__(self):
        self.power = False
        self.network = False
        # self.sata = {1: False, 2: False}

    def update(self, reg, value):
        if reg == 0x50:
            self.power = bool(value)
        elif reg == 0x56:
            self.network = bool(value)

    def __str__(self):
        lines = []

        lines.append(f"Power LED   : {'ON' if self.power else 'OFF'}")
        lines.append(f"Network LED : {'ON' if self.network else 'OFF'}")

        # for i in self.sata:
        #     lines.append(f"SSD {i} LED   : {'ON' if self.sata[i] else 'OFF'}")

        # for i in self.nvme_blink:
        #     blink = "BLINK" if self.nvme_blink[i] else "OFF"
        #     color = self.nvme_color[i] or "none"
        #     lines.append(f"NVMe {i}     : {blink}, color={color}")

        # lines.append("Strip:")
        # lines.append(f"  animation : {self.strip['animation']}")
        # lines.append(f"  brightness: {self.strip['brightness']}")
        # lines.append(f"  color     : {self.strip['color']}")
        # lines.append(f"  loop1     : {self.strip['loop1']}")
        # lines.append(f"  loop2     : {self.strip['loop2']}")

        return "\n".join(lines)