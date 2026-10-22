#!/usr/bin/env python3
"""Deterministic stored ZIP from the explicit allowlist; never silently reseal."""
import argparse
import json
import zipfile
from pathlib import Path
import importlib.util
import sys
sys.dont_write_bytecode = True

_spec = importlib.util.spec_from_file_location("pr1080_kit_verify", Path(__file__).resolve().with_name("verify.py"))
verify = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(verify)


def build(destination):
    output = verify.fresh_output(destination)
    verify.verify()
    names = json.loads((verify.ROOT / "ALLOWLIST.json").read_text())["members"]
    # Exclusive creation never truncates an existing output or inode alias.
    with output.open("xb") as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as z:
            for name in names:
                record = zipfile.ZipInfo("verification_kit/" + name, (2026, 10, 14, 0, 0, 0))
                record.create_system = 3
                record.external_attr = 0o100644 << 16
                record.compress_type = zipfile.ZIP_STORED
                record.flag_bits = 0
                z.writestr(record, (verify.ROOT / name).read_bytes())
    return {"status": "PASS", "archive": str(output), "bytes": output.stat().st_size,
            "sha256": verify.digest(output), "members": len(names), "method": "stored; fixed date, mode and sorted order"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    print(json.dumps(build(a.output), indent=2))


if __name__ == "__main__":
    main()
