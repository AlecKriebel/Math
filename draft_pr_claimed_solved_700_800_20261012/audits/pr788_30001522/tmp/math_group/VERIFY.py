#!/usr/bin/env python3
"""Strict authored inventory and bound-input replay. MANIFEST.json requires external authentication."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys

def fail(message): raise ValueError(message)
def require(ok,message):
    if not ok: fail(message)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--input-root");ap.add_argument("--intake-root");ap.add_argument("--source-root")
    args=ap.parse_args();b=Path(__file__).resolve().parent
    mp=b/"MANIFEST.json"
    require(mp.is_file() and not mp.is_symlink(),"manifest missing or symlink")
    m=json.loads(mp.read_text())
    expected=set(m["files"])|{"MANIFEST.json"}
    require({p.name for p in b.iterdir()}==expected,"exact authored inventory mismatch")
    for name,row in m["files"].items():
        require(Path(name).name==name and name not in (".",".."),"non-flat manifest name")
        p=b/name
        require(p.is_file() and not p.is_symlink(),"authored file missing/nonfile/symlink: "+name)
        require(p.stat().st_size==row["bytes"],"authored length mismatch: "+name)
        require(digest(p)==row["sha256"],"authored digest mismatch: "+name)
    bind=json.loads((b/"INPUT_BINDINGS.json").read_text())
    intake=Path(args.intake_root or bind["intake_root"])
    root=Path(args.input_root or bind["original_root"])
    for name,row in bind["intake_files"].items():
        p=intake/name
        require(p.is_file() and not p.is_symlink(),"bound intake absent/symlink")
        require(p.stat().st_size==row["bytes"] and digest(p)==row["sha256"],"intake binding mismatch: "+name)
    identity=json.loads((intake/"ROOT_SOURCE_IDENTITY.json").read_text())
    require(identity["reviewed_head"]==bind["reviewed_head"],"head binding mismatch")
    inventory={r["path"]:r for r in identity["original_files"]}
    for row in bind["original_files"]:
        inv=inventory[row["path"]]
        require(inv["sha256"]==row["sha256"] and inv["bytes"]==row["bytes"],"source inventory disagreement")
        p=root/row["path"]
        require(p.is_file() and not p.is_symlink(),"original input absent/symlink")
        require(p.stat().st_size==row["bytes"] and digest(p)==row["sha256"],"original input mismatch")
    sources=json.loads((b/"SOURCE_RECEIPTS.json").read_text())
    source_root=Path(args.source_root or sources["default_source_root"])
    for source in sources["sources"]:
        p=source_root/source["scratch_basename"]
        require(Path(source["scratch_basename"]).name==source["scratch_basename"],"unsafe source basename")
        require(p.is_file() and not p.is_symlink(),"source body absent/symlink")
        require(p.stat().st_size==source["bytes"] and digest(p)==source["sha256"],"source body binding mismatch")
        require(bool(source["url"]) and bool(source["read_scope"]),"source scope metadata missing")
    # Only after the CHECKS bytes and all bound inputs pass is authored code executed.
    got=subprocess.run([sys.executable,"-B",str(b/"CHECKS.py")],capture_output=True,text=True)
    require(got.returncode==0,"diagnostics failed: "+got.stderr)
    require(json.loads(got.stdout)==json.loads((b/"RESULTS.json").read_text()),"diagnostic result mismatch")
    freeze=json.loads((b/"INITIAL_FREEZE.json").read_text())
    require(digest(b/"INITIAL_POSITION.md")==freeze["initial_position_sha256"],"initial position changed")
    require(freeze["before_author_or_audits_or_peer_math"] is True,"independence flag absent")
    print(json.dumps({"status":"PASS","authored_files":len(m["files"]),"original_bound_files":len(bind["original_files"]),"reviewed_head":bind["reviewed_head"],"scope":"integrity and exact diagnostic replay; mathematical proof in REVIEW.md"},sort_keys=True))
if __name__=="__main__":
    try: main()
    except Exception as e:
        print("VERIFY FAIL: "+str(e),file=sys.stderr);sys.exit(1)
