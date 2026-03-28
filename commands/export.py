from core.detect import detect_distro, detect_shell, detect_terminals, detect_fetch
from core.packages import export_packages
from core.flatpak import export_flatpak
from core.configs import detect_configs
from core.generator import generate_script
from tui.fzf import fzf_select
import os

def run_export():
    print("Detecting system...")
    
    distro = detect_distro()
    shell = detect_shell()
    terminals = detect_terminals()
    
    print(f"  distro:    {distro}")
    print(f"  shell:     {shell}")
    print(f"  terminals: {', '.join(terminals) if terminals else 'none'}")
    print()

    options = ["Packages", "Flatpak", "Configs"]
    selected = fzf_select(options, prompt="Select what to export > ", multi=True)

    packages = []
    flatpaks = []
    configs = {}

    if "Packages" in selected:
        print("Collecting packages...")
        packages = export_packages(distro)
        print(f"  Found {len(packages)} packages")

    if "Flatpak" in selected:
        print("Collecting Flatpak apps...")
        flatpaks = export_flatpak()
        print(f"  Found {len(flatpaks)} apps")

    if "Configs" in selected:
        print("Detecting configs...")
        configs = detect_configs(terminals, shell)
        print(f"  Found {len(configs)} config paths")

    print("\nGenerating script...")
    script = generate_script(packages, flatpaks, configs, distro, shell)

    home = os.path.expanduser("~")
    from datetime import datetime
    filename = f"dsxconfig-{datetime.now().strftime('%Y-%m-%d')}.sh"
    output_path = os.path.join(home, filename)

    with open(output_path, "w") as f:
        f.write(script)

    os.chmod(output_path, 0o755)

    print(f"\n  ✓ Script saved: {output_path}")
    print(f"  ✓ {len(packages)} packages  ·  {len(flatpaks)} flatpak  ·  {len(configs)} configs")