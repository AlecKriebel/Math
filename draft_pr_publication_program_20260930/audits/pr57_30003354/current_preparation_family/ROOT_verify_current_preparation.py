"""MIT licensed. Source-only helper, not executed by preparer.
Verify full packet bytes and full 07777 modes; no mathematical certification.
Invoke under a ROOT-owned capture with python3 -B and --source-sha256.
"""
import argparse, hashlib, json, pathlib, stat
def digest(data): return hashlib.sha256(data).hexdigest()
def verify(expected):
    root=pathlib.Path(__file__).resolve().parent
    source=root/"SOURCE.json"; raw=source.read_bytes()
    assert digest(raw)==expected, "SOURCE changed"
    obj=json.loads(raw)
    assert obj["self_indexed"] is False
    assert stat.S_IMODE(root.stat().st_mode)==0o755
    actual_files=set(); actual_dirs={"."}
    for p in root.rglob("*"):
        assert not p.is_symlink(), str(p)
        rel=p.relative_to(root).as_posix()
        if p.is_dir(): actual_dirs.add(rel)
        elif p.is_file(): actual_files.add(rel)
        else: raise AssertionError("special object: "+rel)
    indexed={e["path"] for e in obj["files"]}
    assert "SOURCE.json" not in indexed
    assert actual_files==indexed|{"SOURCE.json"}, "file topology changed"
    assert actual_dirs=={e["path"] for e in obj["directories"]}, "directory topology changed"
    for e in obj["files"]:
        p=root/e["path"]; body=p.read_bytes()
        assert len(body)==e["bytes"] and digest(body)==e["sha256"], e["path"]
        assert stat.S_IMODE(p.stat().st_mode)==int(e["full_mode_07777"],8)==0o444
    for e in obj["directories"]:
        assert stat.S_IMODE((root/e["path"]).stat().st_mode)==int(e["full_mode_07777"],8)==0o755
    assert stat.S_IMODE(source.stat().st_mode)==0o444
    return root, obj
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--source-sha256",required=True)
    a=ap.parse_args(); root,obj=verify(a.source_sha256)
    print(json.dumps({"status":"PASS_PACKET_BYTES_MODES_ONLY","prepared_files":len(obj["files"]),
        "directories":len(obj["directories"]),"source_sha256":a.source_sha256,
        "scientific_approval":False,"compiler_or_new_preprint_review":False},sort_keys=True))
