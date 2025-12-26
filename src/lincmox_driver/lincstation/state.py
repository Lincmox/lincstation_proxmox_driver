import json
import os
import tempfile
from typing import Any, Dict

_DEFAULT_PATH = "/var/lib/lincmox/state.json"

_DEFAULT_STATE = {
    "POWER": {"on": False, "blink": False, "color": "none"},
    "SATA_1": {"on": False, "blink": False, "color": "none"},
    "SATA_2": {"on": False, "blink": False, "color": "none"},
    "NETWORK": {"on": False, "blink": False, "color": "none"},
    "NVME_1": {"on": False, "blink": False, "color": "none"},
    "NVME_2": {"on": False, "blink": False, "color": "none"},
    "NVME_3": {"on": False, "blink": False, "color": "none"},
    "NVME_4": {"on": False, "blink": False, "color": "none"},
    "STRIP": {
        "animation": "off",
        "brightness": 0,
        "color": {"r": 0, "g": 0, "b": 0},
        "first_loop_color": {"r": 0, "g": 0, "b": 0},
        "second_loop_color": {"r": 0, "g": 0, "b": 0},
    },
}

class LincStationState:
    def __init__(self, path: str = ""):
        self.path = path if path else _DEFAULT_PATH
        self.state: Dict[str, Any] = {}

        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._load()

    def _load(self) -> None:
        """Charge l'état depuis le disque ou crée le fichier par défaut."""
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self.state = json.load(f)
        else:
            self.state = _DEFAULT_STATE
            self._save()

    def _save(self) -> None:
        """Sauvegarde atomique sur disque."""
        directory = os.path.dirname(self.path)

        with tempfile.NamedTemporaryFile(
            "w", dir=directory, delete=False, encoding="utf-8"
        ) as tmp:
            json.dump(self.state, tmp, indent=4)
            tmp.flush()
            os.fsync(tmp.fileno())
            temp_name = tmp.name

        os.replace(temp_name, self.path)

    # ---------- API publique ----------

    def get(self, key: str) -> Any:
        return self.state.get(key)

    def set(self, key: str, value: Any) -> None:
        self.state[key] = value
        self._save()

    def update(self, key: str, subkey: str, value: Any) -> None:
        if key not in self.state:
            raise KeyError(f"{key} n'existe pas")
        self.state[key][subkey] = value
        self._save()

    def get_sub(self, key: str, subkey: str) -> Any:
        return self.state[key][subkey]

    def as_dict(self) -> Dict[str, Any]:
        return self.state.copy()