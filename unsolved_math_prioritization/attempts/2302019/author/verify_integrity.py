#!/usr/bin/env python3
"""Verify this exact frozen author inventory. Authenticate its hash separately."""
import hashlib
import json
from pathlib import Path


def main():
    if not __debug__:
        raise SystemExit("Run without Python optimization: assertions are required.")
    root=Path(__file__).resolve().parent
    manifest=root/"AUTHOR_MANIFEST.json"
    data=json.loads(manifest.read_text())
    assert set(data)=={"schema","packet_id","files"}, "manifest schema"
    assert data["schema"]==1, "manifest schema version"
    assert data["packet_id"]=="2302019-reconstruction-20261005-v1", "packet id"
    entries=data["files"]
    paths=[entry["path"] for entry in entries]
    assert paths==sorted(set(paths)), "file order or duplicate path"
    assert "verify_integrity.py" in paths and "PROOFS.md" in paths, "required files"
    actual=[]
    for p in root.rglob("*"):
        assert not p.is_symlink(), "symlink in author packet"
        if p.is_file():
            actual.append(p.relative_to(root).as_posix())
    assert sorted(actual)==sorted(paths+["AUTHOR_MANIFEST.json"]), "unexpected or missing file"
    for entry in entries:
        assert set(entry)=={"path","bytes","sha256"}, "entry schema"
        relative=Path(entry["path"])
        assert not relative.is_absolute() and ".." not in relative.parts, "unsafe path"
        content=(root/relative).read_bytes()
        assert len(content)==entry["bytes"], "byte count: "+str(relative)
        assert hashlib.sha256(content).hexdigest()==entry["sha256"], "digest: "+str(relative)
    print(json.dumps({"packet_id":data["packet_id"],"verified_files":len(entries),
                      "manifest_sha256":hashlib.sha256(manifest.read_bytes()).hexdigest()},
                     indent=2,sort_keys=True))


if __name__=="__main__":
    main()
