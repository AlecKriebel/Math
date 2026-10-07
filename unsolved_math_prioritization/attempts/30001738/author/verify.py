"""Trusted isolated verifier; caller must separately pin this file and manifest."""
import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit("Use python -I -S -B verify.py EXPECTED_MANIFEST_SHA256 [PACKET]")
from pathlib import Path
import contextlib
import hashlib
import io
import json

def fail(message):
    raise SystemExit("REJECTED: " + message)
if len(sys.argv) not in (2,3):
    fail("Expected manifest pin and optional packet directory")
pin = sys.argv[1]
if len(pin) != 64 or any(c not in "0123456789abcdef" for c in pin):
    fail("Malformed manifest pin")
root = Path(sys.argv[2]).resolve() if len(sys.argv)==3 else Path(__file__).resolve().parent
manifest_path = root/"MANIFEST.json"
if manifest_path.is_symlink() or not manifest_path.is_file():
    fail("Missing or linked manifest")
raw = manifest_path.read_bytes()
if hashlib.sha256(raw).hexdigest() != pin:
    fail("Manifest hash mismatch")
manifest = json.loads(raw)
entries = manifest["files"]
if not isinstance(entries,list):
    fail("Invalid entries")
names = [r["path"] for r in entries]
if len(set(names))!=len(names) or any("/" in n or "\\" in n or n in ("",".","..","MANIFEST.json") for n in names):
    fail("Invalid flat inventory")
actual = set()
for path in root.iterdir():
    if path.is_symlink() or not path.is_file():
        fail("Symlink, directory or nonregular entry")
    actual.add(path.name)
if actual != set(names)|{"MANIFEST.json"}:
    fail("Inventory mismatch")
snapshot = {}
for row in entries:
    b=(root/row["path"]).read_bytes()
    if len(b)!=row["bytes"] or hashlib.sha256(b).hexdigest()!=row["sha256"]:
        fail("Payload mismatch: "+row["path"])
    snapshot[row["path"]] = b
capture = io.StringIO()
with contextlib.redirect_stdout(capture):
    exec(compile(snapshot["controls.py"],"<verified-controls>","exec"),
         {"__name__":"__main__"})
expected_receipt = json.loads(snapshot["CONTROL_RECEIPT.json"])
receipt = json.loads(capture.getvalue())
if receipt != expected_receipt or receipt["status"]!="pass":
    fail("Control receipt mismatch")
print(json.dumps({"status":"pass","verified_files":len(entries),
                  "manifest_sha256":pin,"controls":receipt},sort_keys=True,indent=2))
