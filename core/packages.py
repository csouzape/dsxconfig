import subprocess

EXCLUDE_PREFIXES = (
    "kernel", "grub2", "systemd", "glibc", "dracut",
    "plymouth", "shim", "selinux", "firmware", "microcode"
)

def _filter_packages(packages):
    return [p for p in packages
            if not any(p.startswith(prefix) for prefix in EXCLUDE_PREFIXES)]

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
        packages = [line.split()[0] for line in lines if line.strip()]
    else:
        packages = [line.strip() for line in lines if line.strip()]

    return _filter_packages(packages)