#!/usr/bin/env python3
"""Build an allowlisted, uncompressed canonical ZIP. No archive recursion."""
from pathlib import Path
import argparse
import json
import stat
import zipfile
def build(root, target):
    allow = json.loads((root/'ALLOWLIST.json').read_text())['files']
    if sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()) != allow:
        raise RuntimeError('actual file set differs from explicit allowlist')
    if target.exists():
        raise RuntimeError('refusing to replace an existing archive')
    with zipfile.ZipFile(target,'x') as z:
        for name in allow:
            if (root/name).is_symlink():
                raise RuntimeError('symlink')
            i=zipfile.ZipInfo(name,(2026,10,16,0,0,0))
            i.create_system=3
            i.external_attr=(stat.S_IFREG|0o644)<<16
            i.compress_type=zipfile.ZIP_STORED
            z.writestr(i,(root/name).read_bytes())
if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('target',type=Path)
    a=p.parse_args()
    build(Path(__file__).resolve().parents[1],a.target)
