#!/usr/bin/env python3
"""Postseal cross-check integrity/replay; mathematical arguments are in CROSSCHECK.md."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
def need(ok,msg):
 if not ok:raise ValueError(msg)
def row(p):return {"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--manifest-sha256",required=True);a=ap.parse_args()
 b=Path(__file__).resolve().parent
 need(row(b/"MANIFEST.json")["sha256"]==a.manifest_sha256,"manifest pin mismatch")
 m=json.loads((b/"MANIFEST.json").read_text())
 need({p.name for p in b.iterdir()}==set(m["files"])|{"MANIFEST.json"},"inventory mismatch")
 for name,r in m["files"].items():
  p=b/name;need(p.is_file() and not p.is_symlink() and row(p)==r,"authored integrity failure: "+name)
 bindings=json.loads((b/"INPUT_BINDINGS.json").read_text())
 for r in bindings["inputs"]:
  p=Path(r["path"]);need(p.is_file() and not p.is_symlink(),"input missing/symlink")
  need(row(p)=={"bytes":r["bytes"],"sha256":r["sha256"]},"bound input changed: "+r["role"])
 sealed=Path(bindings["sealed_packet"])
 r=subprocess.run([sys.executable,"-B",str(sealed/"VERIFY.py")],capture_output=True,text=True)
 need(r.returncode==0,"sealed packet replay failed: "+r.stderr)
 got={"status":"PASS","blocking_mathematical_issues":0,"sealed_packet_unchanged":True,"peer_report_sha256":bindings["peer_report_sha256"],"sealed_replay":json.loads(r.stdout),"limitation":"Integrity/replay checks do not machine-prove the adversarial arguments."}
 need(got==json.loads((b/"RESULTS.json").read_text()),"recorded result differs")
 print(json.dumps(got,sort_keys=True))
if __name__=="__main__":
 try:main()
 except Exception as e:print("CROSSCHECK FAIL: "+str(e),file=sys.stderr);sys.exit(1)
