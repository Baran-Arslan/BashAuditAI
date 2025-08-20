import os
from typing import List

def list_shell_scripts(root: str) -> List[str]:
    out = []
    for base, dirs, files in os.walk(root):
        for fn in files:
            if fn.lower().endswith(".sh"):
                out.append(os.path.join(base, fn))
    return sorted(out)

def path_exists(p: str) -> bool:
    return os.path.exists(p)
