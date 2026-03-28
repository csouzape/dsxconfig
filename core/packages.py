import subprocess

def export_packages(distro):
    if distro == "arch":
        cmd = ["pacman", "-Qn"]
    elif distro == "debian":
        cmd = ["apt-mark", "showmanual"]
    elif distro == "fedora":
        cmd = ["dnf", "repoquery", "--userinstalled", "--queryformat", "%{name}\n"]
    else:
        return []

    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.splitlines()

    if distro == "arch":
        return [line.split()[0] for line in lines if line.strip()]
    else:
        return [line.strip() for line in lines if line.strip()]