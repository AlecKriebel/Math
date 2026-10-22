"""Read-only exact physical membership and SHA verification of this packet."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    name = "CLOSED_DIRECTORY_SEAL.json"
    seal_path = root / name
    seal = json.loads(seal_path.read_text())
    if seal["exclusion_exact_relative_paths"] != [name]:
        raise RuntimeError("Only the exact own seal may be excluded")
    physical = {p.relative_to(root).as_posix():p for p in root.rglob("*") if p.is_file()}
    expected = {m["path"]:m for m in seal["members"]}
    if set(physical)-{name} != set(expected):
        raise RuntimeError("Physical membership differs from the closed seal")
    for rel,m in expected.items():
        p = physical[rel]
        if p.is_symlink():
            raise RuntimeError("Symlink outside closed file format")
        data = p.read_bytes()
        if len(data) != m["bytes"] or hashlib.sha256(data).hexdigest() != m["sha256"]:
            raise RuntimeError("Member bytes differ: "+rel)
    print(json.dumps({"status":"PASS","members":len(expected),
                      "member_bytes":sum(m["bytes"] for m in expected.values()),
                      "seal_sha256":hashlib.sha256(seal_path.read_bytes()).hexdigest()},indent=2))


if __name__ == "__main__":
    main()
