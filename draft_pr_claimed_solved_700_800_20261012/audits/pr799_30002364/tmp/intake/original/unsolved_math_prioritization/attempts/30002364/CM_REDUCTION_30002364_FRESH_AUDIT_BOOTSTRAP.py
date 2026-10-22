import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit("Use python -I -S for trusted pre-execution inventory")
import hashlib
import json
import pathlib
import stat
import subprocess
PINNED_MANIFEST_SHA256 = '94411439254901040896f6f6222c980f0d7a2f9e9674a900dac623e4c0cff9ff'
if len(sys.argv) not in (3,4) or (len(sys.argv)==4 and sys.argv[3]!="--optimized"):
    raise SystemExit("usage: bootstrap DIRECTORY MANIFEST [--optimized]")
root=pathlib.Path(sys.argv[1]).absolute()
manifest=pathlib.Path(sys.argv[2]).absolute()
if root.resolve()!=root or not stat.S_ISDIR(root.lstat().st_mode):
    raise SystemExit("root is not a real canonical directory")
if manifest.resolve()!=manifest or not stat.S_ISREG(manifest.lstat().st_mode):
    raise SystemExit("manifest is not a regular canonical file")
if root in manifest.parents:
    raise SystemExit("manifest must be external to packet root")
raw=manifest.read_bytes()
if hashlib.sha256(raw).hexdigest()!=PINNED_MANIFEST_SHA256:
    raise SystemExit("manifest digest mismatch")
expected=json.loads(raw)["files"]
actual={p.name for p in root.iterdir()}
if actual!=set(expected):
    raise SystemExit("strict inventory mismatch")
for name,record in expected.items():
    if pathlib.PurePosixPath(name).name!=name or name in (".",".."):
        raise SystemExit("unsafe inventory name")
    p=root/name
    if not stat.S_ISREG(p.lstat().st_mode):
        raise SystemExit("non-regular inventory member")
    payload=p.read_bytes()
    if len(payload)!=record["bytes"] or hashlib.sha256(payload).hexdigest()!=record["sha256"]:
        raise SystemExit("file digest mismatch: "+name)
command=[sys.executable,"-I","-S"]
if len(sys.argv)==4:
    command.append("-O")
command.append(str(root/"independent_exact.py"))
result=subprocess.run(command,cwd=root,check=False)
raise SystemExit(result.returncode)
