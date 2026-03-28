import subprocess
import tempfile
import os

def fzf_select(items, prompt="", multi=False):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp_in:
        tmp_in.write("\n".join(items))
        tmp_in_path = tmp_in.name
    cmd = ["fzf", "--prompt=" + prompt, "--height=40%", "--layout=reverse", "--border=rounded"]
    if multi:
        cmd.append("-m")

    with open(tmp_in_path) as f:
        result = subprocess.run(cmd, stdin=f, capture_output=True, text=True)

    os.unlink(tmp_in_path)

    if multi:
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    else:
        return result.stdout.strip()