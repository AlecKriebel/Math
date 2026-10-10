"""Verify pinned audit package before extracting or running its acceptance suite.
Usage: python -I -S [-O] BOOTSTRAP.py ARCHIVE.zip EXTERNAL_MANIFEST.json
This runs finite arithmetic and verification controls, not a universal proof.
"""
import hashlib
import io
import json
import pathlib
import stat
import subprocess
import sys
import tempfile
import zipfile
ARCHIVE_PIN = {'filename': 'BOUNDED_HOUSE_30003245_INDEPENDENT_AUDIT_SAFE.zip', 'bytes': 49443, 'sha256': '06112fbb500494f6cb68da45ccdfb9d78292aa18b72369385b31b91a4ffecda5'}
MANIFEST_PIN = {'filename': 'BOUNDED_HOUSE_30003245_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json', 'bytes': 2875, 'sha256': 'ac5eec2cbd5816c27e869e5c61c71f24fd121eb70c30205bb893cdb2e06dc29b'}
MEMBER_COUNT = 14

def require(ok, label):
    if not ok:
        raise SystemExit("REJECTED BEFORE EXECUTION: " + label)

def read_pinned(path, pin):
    data=pathlib.Path(path).read_bytes()
    require(len(data)==pin["bytes"] and hashlib.sha256(data).hexdigest()==pin["sha256"],pin["filename"])
    return data

require(len(sys.argv)==3,"archive and manifest paths required")
data=read_pinned(sys.argv[1],ARCHIVE_PIN)
mdata=read_pinned(sys.argv[2],MANIFEST_PIN)
m=json.loads(mdata)
require(m["archive"]==ARCHIVE_PIN,"archive binding")
expected={r["name"]:r for r in m["members"]}
require(len(expected)==len(m["members"])==MEMBER_COUNT,"manifest member set")
verified={}
with zipfile.ZipFile(io.BytesIO(data)) as z:
    names=z.namelist()
    require(len(names)==len(set(names))==MEMBER_COUNT and set(names)==set(expected),"archive member set")
    for info in z.infolist():
        require(info.filename==pathlib.PurePosixPath(info.filename).name,"safe flat name")
        require(not stat.S_ISLNK(info.external_attr>>16),"symlink")
        row=expected[info.filename]
        require(info.file_size==row["bytes"],"declared size")
        content=z.read(info)
        require(len(content)==row["bytes"] and hashlib.sha256(content).hexdigest()==row["sha256"],"member hash")
        verified[info.filename]=content
print("AUDIT PINS VERIFIED",flush=True)
with tempfile.TemporaryDirectory(prefix="bounded-house-audit-verified-") as temp:
    folder=pathlib.Path(temp)
    for name,content in verified.items():
        (folder/name).write_bytes(content)
    command=[sys.executable,"-I","-S"]+(["-O"] if sys.flags.optimize else [])+[str(folder/"replay_acceptance.py"),str(folder)]
    run=subprocess.run(command,cwd=folder,timeout=180,check=False)
    raise SystemExit(run.returncode)
