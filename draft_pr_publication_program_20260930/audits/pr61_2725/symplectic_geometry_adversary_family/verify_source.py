"""Read-only byte/mode/topology checks; no mathematical or ROOT-authority proof."""
import hashlib, json, pathlib, stat
BASE = pathlib.Path(__file__).resolve().parent
MANIFEST = "ROOT_SOURCE_CLOSURE.json"
def sha(b):
    return hashlib.sha256(b).hexdigest()
def verify(expected_index, closed=False):
    index_bytes = (BASE/"INDEX.json").read_bytes()
    assert sha(index_bytes) == expected_index
    idx = json.loads(index_bytes)
    allowed = {r["path"] for r in idx["files"]} | {"INDEX.json","READY.json"}
    if closed:
        allowed.add(MANIFEST)
    nodes = list(BASE.rglob("*"))
    assert {str(p.relative_to(BASE)) for p in nodes if p.is_file()} == allowed
    assert {"."} | {str(p.relative_to(BASE)) for p in nodes if p.is_dir()} == set(idx["directories"])
    for p in [BASE]+nodes:
        s = p.lstat()
        assert not p.is_symlink()
        assert stat.S_ISREG(s.st_mode) or stat.S_ISDIR(s.st_mode)
        assert (s.st_mode&0o7777) == (0o755 if p.is_dir() else 0o444)
        if p.is_file():
            assert s.st_nlink == 1
    total = 0
    for r in idx["files"]:
        rel = pathlib.PurePosixPath(r["path"])
        assert not rel.is_absolute() and ".." not in rel.parts
        b = (BASE/r["path"]).read_bytes()
        assert len(b) == r["bytes"] and sha(b) == r["sha256"]
        total += len(b)
    ready_bytes = (BASE/"READY.json").read_bytes()
    ready = json.loads(ready_bytes)
    assert ready["index_sha256"] == expected_index
    assert ready["source_only"] is True and ready["ROOT_custody_claimed"] is False
    for r in json.loads((BASE/"ORIGINAL_INPUT_PINS.json").read_text())["original_science"]:
        p = pathlib.Path(r["path"])
        s = p.lstat()
        assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
        assert (s.st_mode&0o7777) == int(r["full_mode"],8)
        b = p.read_bytes()
        assert len(b) == r["bytes"] and sha(b) == r["sha256"]
    return {"index_sha256":expected_index,"ready_sha256":sha(ready_bytes),
            "source_file_count":len(idx["files"])+2,
            "source_logical_bytes":total+len(index_bytes)+len(ready_bytes),
            "directory_count":len(idx["directories"]),
            "external_original_bodies_checked":10,
            "scope":"full listed bodies/modes/topology; original local byte pins; no remote, mathematical, human-review or authority certification"}
