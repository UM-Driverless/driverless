"""
FSDS module loader

Usage:
    from driverless.utils.fsds_loader import load_fsds
    fsds = load_fsds()
    client = fsds.client.FSDSClient()
    client.confirmConnection()  # Example method to confirm connection
"""

import sys
from pathlib import Path
from types import ModuleType

_FSDS_PATH = Path(__file__).resolve().parents[4] / "Formula-Student-Driverless-Simulator" / "python"
_fsds_module: ModuleType | None = None

def load_fsds() -> ModuleType:
    """Dynamically import the fsds module with path injection, only once."""
    global _fsds_module
    if _fsds_module is None:
        if str(_FSDS_PATH) not in sys.path:
            sys.path.insert(0, str(_FSDS_PATH))
        import fsds  # noqa: E402
        _fsds_module = fsds
    return _fsds_module

if __name__ == "__main__":
    # For testing purposes
    fsds = load_fsds()
    client = fsds.client.FSDSClient()
    client.confirmConnection()
    print("FSDS module loaded and simulator connection confirmed.")
