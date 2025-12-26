from enum import Enum
from dataclasses import dataclass

# --- LED REGISTERS ---
_REG_LED = {
    "on": {
        1: 0xA0,
        2: 0xA1,
    },
    "off": {
        1: 0xB0,
        2: 0xB1,
    }
}

# --- LED MASKS ---
_MASK_LED_BLINK = {
    "on": 0x01,
    "off": 0x00
}

@dataclass(frozen=True)
class LincStationLedConfig:
    label: str
    reg_on: int
    reg_off: int
    reg_blink: int
    mask_color: dict[str, int]

@dataclass(frozen=True)
class LincStationStripConfig:
    label: str
    reg_animation: int
    reg_brightness: int
    reg_red: int
    reg_green: int
    reg_blue: int
    reg_first_loop_red: int
    reg_first_loop_green: int
    reg_first_loop_blue: int
    reg_second_loop_red: int
    reg_second_loop_green: int
    reg_second_loop_blue: int
    mask_animation: dict[str, int]

class LincStationTarget(Enum):
    POWER = LincStationLedConfig(
        label="Power",
        reg_on=_REG_LED["on"][1],
        reg_off=_REG_LED["off"][1],
        reg_blink=0x50,
        mask_color={
            "white": 0x01,
            "red": 0x02,
            "orange": 0x03,
        }
    )

    SATA_1 = LincStationLedConfig(
        label="SATA 1",
        reg_on=_REG_LED["on"][1],
        reg_off=_REG_LED["off"][1],
        reg_blink=0x52,
        mask_color={
            "white": 0x04,
            "red": 0x08,
            "orange": 0x0C,
        }
    )

    SATA_2 = LincStationLedConfig(
        label="SATA 2",
        reg_on=_REG_LED["on"][1],
        reg_off=_REG_LED["off"][1],
        reg_blink=0x54,
        mask_color={
            "white": 0x10,
            "red": 0x20,
            "orange": 0x30,
        }
    )

    NETWORK = LincStationLedConfig(
        label="Network",
        reg_on=_REG_LED["on"][1],
        reg_off=_REG_LED["off"][1],
        reg_blink=0x56,
        mask_color={
            "white": 0x40,
            "red": 0x80,
            "orange": 0xC0,
        }
    )

    NVME_1 = LincStationLedConfig(
        label="NVMe 1",
        reg_on=_REG_LED["on"][2],
        reg_off=_REG_LED["off"][2],
        reg_blink=0x58,
        mask_color={
            "white": 0x01,
            "red": 0x02,
            "orange": 0x03,
        }
    )

    NVME_2 = LincStationLedConfig(
        label="NVMe 2",
        reg_on=_REG_LED["on"][2],
        reg_off=_REG_LED["off"][2],
        reg_blink=0x5A,
        mask_color={
            "white": 0x04,
            "red": 0x08,
            "orange": 0x0C,
        }
    )

    NVME_3 = LincStationLedConfig(
        label="NVMe 3",
        reg_on=_REG_LED["on"][2],
        reg_off=_REG_LED["off"][2],
        reg_blink=0x5C,
        mask_color={
            "white": 0x10,
            "red": 0x20,
            "orange": 0x30,
        }
    )

    NVME_4 = LincStationLedConfig(
        label="NVMe 4",
        reg_on=_REG_LED["on"][2],
        reg_off=_REG_LED["off"][2],
        reg_blink=0x5E,
        mask_color={
            "white": 0x40,
            "red": 0x80,
            "orange": 0xC0,
        }
    )

    STRIP = LincStationStripConfig(
        label="Strip",
        reg_animation=0x90,
        reg_brightness=0x91,
        reg_red=0x92,
        reg_green=0x93,
        reg_blue=0x94,
        reg_first_loop_red=0x95,
        reg_first_loop_green=0x96,
        reg_first_loop_blue=0x97,
        reg_second_loop_red=0x98,
        reg_second_loop_green=0x99,
        reg_second_loop_blue=0x9A,
        mask_animation={
            "off": 0x00,
            "breath": 0x01,
            "loop": 0x02,
        }
    )
