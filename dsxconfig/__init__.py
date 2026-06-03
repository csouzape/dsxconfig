import os
import sys

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "dsxconfig"

from .interface import main
from .detector import SystemDetector
from .generator import RestoreScriptGenerator
from .package_db import PackageAdaptationDB

__all__ = ["SystemDetector", "RestoreScriptGenerator", "PackageAdaptationDB", "main"]

if __name__ == "__main__":
    main()
