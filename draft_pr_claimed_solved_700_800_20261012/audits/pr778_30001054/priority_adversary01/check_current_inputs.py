#!/usr/bin/env python3
"""Optional sibling input equality, independent of authored packet custody."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-root", type=Path, default=Path(__file__).absolute().parent.parent)
    args = parser.parse_args()
    records = json.loads((Path(__file__).absolute().parent / "CURRENT_INPUT_IDENTITIES.json").read_text())
    checked = []
    for item in records["inputs"]:
        name = item["path_relative_to_audit"]
        pp = PurePosixPath(name)
        if pp.is_absolute() or ".." in pp.parts or str(pp) != name:
            raise ValueError("unsafe input path")
        path = args.audit_root / pp
        if path.is_symlink() or not path.is_file():
            raise ValueError("missing or non-regular input: " + name)
        body = path.read_bytes()
        if len(body) != item["bytes"] or hashlib.sha256(body).hexdigest() != item["sha256"]:
            raise ValueError("changed input: " + name)
        checked.append(name)
    print(json.dumps({"status": "PASS", "checked": checked,
                      "git_access": False, "mtime_prerequisite": False}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}))
        sys.exit(1)
