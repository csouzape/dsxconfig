from .detector import SystemDetector
from .generator import RestoreScriptGenerator
from .package_db import PackageAdaptationDB

__all__ = ["SystemDetector", "RestoreScriptGenerator", "PackageAdaptationDB"]


def main():
    detector = SystemDetector()
    state = detector.detect_installed_apps()
    generator = RestoreScriptGenerator()
    path = generator.generate_restore_script(state)
    print(f"Generated restore script: {path}")
    print("Use: bash ~/dsxconfig_restore.sh")
