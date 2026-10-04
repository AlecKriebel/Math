"""MIT licensed. Unexecuted by preparer; invoke with ROOT-owned full capture.
Records custody only; output must lie outside the fixed packet.
"""
import argparse, datetime, hashlib, json, os, pathlib
from ROOT_verify_current_preparation import verify
ap=argparse.ArgumentParser()
ap.add_argument("--source-sha256",required=True); ap.add_argument("--output",required=True)
a=ap.parse_args(); root,obj=verify(a.source_sha256)
out=pathlib.Path(a.output).resolve()
assert not out.is_relative_to(root), "receipt must be outside packet"
receipt={"schema":"pr61-current-preparation-root-custody/v1",
    "utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"pid":os.getpid(),
    "packet":str(root),"SOURCE_sha256":a.source_sha256,
    "prepared_files":len(obj["files"]),"directories":len(obj["directories"]),
    "bytes_and_modes_read":True,"mathematical_approval":False,
    "new_paper_created":False,"published":False}
body=(json.dumps(receipt,sort_keys=True,indent=2)+"\n").encode()
with out.open("xb") as f: f.write(body)
print(json.dumps({"receipt":str(out),"sha256":hashlib.sha256(body).hexdigest(),
    "status":"CUSTODY_ONLY"},sort_keys=True))
