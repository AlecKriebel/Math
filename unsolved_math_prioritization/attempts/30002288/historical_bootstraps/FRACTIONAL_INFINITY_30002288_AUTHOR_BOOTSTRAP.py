"""Trusted external preflight; run only with python -I -S."""
import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit("Use python -I -S for pre-execution inventory")
import hashlib
import json
import pathlib
import stat
import subprocess
import zipfile

PINNED_MANIFEST_SHA256 = "b3a70f59cb89dbc0d7e18ee845cd6ac31db9c3180e1ebc684b94890be418294d"

def reject(message):
    raise SystemExit(message)

def real_path(path, kind):
    for parent in [path]+list(path.parents):
        mode=parent.lstat().st_mode
        if stat.S_ISLNK(mode):
            reject("symlink path forbidden")
    mode=path.lstat().st_mode
    if kind=="file" and not stat.S_ISREG(mode):
        reject("non-regular file forbidden")
    if kind=="directory" and not stat.S_ISDIR(mode):
        reject("root is not a real directory")

if len(sys.argv) not in (4,5) or (len(sys.argv)==5 and sys.argv[4]!="--optimized"):
    reject("usage: bootstrap DIRECTORY ARCHIVE MANIFEST [--optimized]")
root,archive,manifest=(pathlib.Path(s).absolute() for s in sys.argv[1:4])
real_path(root,"directory")
real_path(archive,"file")
real_path(manifest,"file")
if root in archive.parents or root in manifest.parents:
    reject("archive and manifest must be external to extracted root")
raw=manifest.read_bytes()
if hashlib.sha256(raw).hexdigest()!=PINNED_MANIFEST_SHA256:
    reject("pinned manifest mismatch")
data=json.loads(raw)
expected=data["files"]
if set(p.name for p in root.iterdir())!=set(expected):
    reject("strict root inventory mismatch")
for name,record in expected.items():
    if pathlib.PurePosixPath(name).name!=name or name in (".",".."):
        reject("unsafe inventory name")
    p=root/name
    real_path(p,"file")
    b=p.read_bytes()
    if len(b)!=record["bytes"] or hashlib.sha256(b).hexdigest()!=record["sha256"]:
        reject("member digest mismatch: "+name)
b=archive.read_bytes()
if len(b)!=data["archive"]["bytes"] or hashlib.sha256(b).hexdigest()!=data["archive"]["sha256"]:
    reject("archive digest mismatch")
with zipfile.ZipFile(archive) as z:
    names=z.namelist()
    if len(names)!=len(set(names)) or set(names)!=set(expected):
        reject("archive inventory mismatch")
    if z.testzip() is not None:
        reject("archive CRC failure")
    for info in z.infolist():
        mode=(info.external_attr>>16)&0xffff
        if not stat.S_ISREG(mode) or info.is_dir():
            reject("non-regular archive member")
        if z.read(info.filename)!=(root/info.filename).read_bytes():
            reject("archive/root byte mismatch")

command=[sys.executable,"-I","-S"]
if len(sys.argv)==5:
    command.append("-O")
command.append(str(root/"verify_math.py"))
result=subprocess.run(command,cwd=root,capture_output=True,check=False)
if result.returncode!=0 or result.stderr:
    reject("checker process failure")
if result.stdout!=(root/"RESULTS.json").read_bytes():
    reject("checker output mismatch")
sys.stdout.buffer.write(result.stdout)
