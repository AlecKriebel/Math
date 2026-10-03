"""MIT licensed. Unexecuted by preparer; separate ROOT-owned process required."""
import argparse, hashlib, json, pathlib
from ROOT_verify_original import verify
ap=argparse.ArgumentParser()
ap.add_argument("--receipt",required=True); ap.add_argument("--receipt-sha256",required=True)
a=ap.parse_args(); p=pathlib.Path(a.receipt).resolve(); raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()==a.receipt_sha256
r=json.loads(raw); root,obj=verify(r["SOURCE_sha256"])
assert not p.is_relative_to(root)
assert r["packet"]==str(root) and r["bytes_and_modes_read"] is True
assert r["mathematical_approval"] is False and r["new_mathematical_review"] is False
assert r["prepared_files"]==len(obj["files"]) and r["directories"]==len(obj["directories"])
print(json.dumps({"status":"PASS_SEPARATE_PACKET_READBACK_ONLY",
 "receipt_sha256":a.receipt_sha256,"SOURCE_sha256":r["SOURCE_sha256"],
 "mathematical_approval":False,"submission_ready":False},sort_keys=True))


