"""Verify this authored packet and the two immutable initial packets."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_members(root, manifest):
    members = manifest["authored_files"]
    names = [entry["path"] for entry in members]
    assert len(names) == len(set(names)), "duplicate authored paths"
    for entry in members:
        rel = Path(entry["path"])
        assert not rel.is_absolute() and ".." not in rel.parts
        assert rel.parts[0] != "_local" and rel.name != "MANIFEST.json"
        path = root / rel
        assert path.stat().st_size == entry["bytes"], path
        assert digest(path) == entry["sha256"], path
    return len(members)


current = json.loads((HERE / "MANIFEST.json").read_text())
count = verify_members(HERE, current)
for folder, expected in [
    ("primary_lineage", "a329d5fe51b943bade54f4cf6235e9e4def6862578003d191e8ca6d37dac2d3e"),
    ("endpoint_witnesses", "5d9a42f759bafd3b2b9b86643d155ae9b0323fce5d8292d8e27d08b955f8beeb"),
]:
    root = HERE.parent / folder
    path = root / "MANIFEST.json"
    assert digest(path) == expected, path
    verify_members(root, json.loads(path.read_text()))
assert not json.loads((HERE / "VERDICT.json").read_text())["priority_clearance"]
print(f"PASS: {count} explicit authored outputs; both initial seals unchanged; raw evidence excluded.")
