import subprocess 
import shutil

def export_flatpak():
    if not shutil.which("flatpak"):
        return []
    cmd = ["flatpak", "list", "--app", "--columns=application"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.splitlines()

    return [line.strip() for line in lines if line.strip()]
