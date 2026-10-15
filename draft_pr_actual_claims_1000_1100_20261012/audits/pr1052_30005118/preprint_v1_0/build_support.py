#!/usr/bin/env python3
"""Rebuild the exact deterministic allowlisted archive using Python stdlib."""
import argparse
import hashlib
import importlib.util
from pathlib import Path
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('verify_support', ROOT/'verify_support.py')
_verify = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_verify)
verify_payload = _verify.verify_payload

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', default='pr1052_support_v1_0.zip')
    args = ap.parse_args()
    out = ROOT / args.output
    out.resolve().relative_to(ROOT)
    members = verify_payload()
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_STORED) as z:
        for name in sorted(members):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 14, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_STORED
            z.writestr(info, (ROOT/name).read_bytes())
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    Path(str(out)+'.sha256').write_text(sha+'  '+out.name+'\n')
    print(sha+'  '+str(out.relative_to(ROOT)))

if __name__ == '__main__':
    main()
