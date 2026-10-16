#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import argparse
import json
import zipfile
from common import KIT, inventory, fresh_output

def main():
    p = argparse.ArgumentParser(description="Build deterministic stored ZIP to a fresh path outside protected trees")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    inventory()
    names = sorted(q.relative_to(KIT).as_posix() for q in KIT.rglob("*") if q.is_file())
    with fresh_output(args.out) as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
            for name in names:
                info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, (KIT / name).read_bytes())
    print(json.dumps({"status": "PASS", "members": len(names)}, sort_keys=True))

if __name__ == "__main__":
    main()
