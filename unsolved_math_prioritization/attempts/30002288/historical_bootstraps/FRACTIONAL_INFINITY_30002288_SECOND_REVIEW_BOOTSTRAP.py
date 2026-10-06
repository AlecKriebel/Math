"""Pinned external strict-inventory bootstrap for the independent review."""
import sys
if not (sys.flags.isolated and sys.flags.no_site):
    raise SystemExit('Use python -I -S')
import hashlib
import json
import pathlib
import stat
import subprocess
import zipfile
PIN = '82014e876476df1118a4defc7e6c24271932fe2be805490810a4711f54322be8'
def need(test, message):
    if not test:
        raise SystemExit(message)
def regular(path, directory=False):
    for p in [path]+list(path.parents):
        need(not stat.S_ISLNK(p.lstat().st_mode), 'symlink path forbidden')
    mode=path.lstat().st_mode
    need(stat.S_ISDIR(mode) if directory else stat.S_ISREG(mode), 'non-regular input or root type')
need(len(sys.argv) in (4,5), 'usage: bootstrap ROOT ARCHIVE MANIFEST [--optimized]')
need(len(sys.argv)==4 or sys.argv[4]=='--optimized', 'invalid optimization option')
root,archive,manifest=(pathlib.Path(x).absolute() for x in sys.argv[1:4])
regular(root,True);regular(archive);regular(manifest)
need(root not in archive.parents and root not in manifest.parents, 'external metadata required')
m=manifest.read_bytes();need(hashlib.sha256(m).hexdigest()==PIN,'pinned manifest mismatch')
data=json.loads(m);files=data['files']
need(set(p.name for p in root.iterdir())==set(files),'strict inventory mismatch')
for name,r in files.items():
    need(pathlib.PurePosixPath(name).name==name and name not in ('.','..'),'unsafe member name')
    f=root/name;regular(f);b=f.read_bytes()
    need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'member digest mismatch: '+name)
b=archive.read_bytes();r=data['archive']
need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'archive digest mismatch')
with zipfile.ZipFile(archive) as z:
    names=z.namelist()
    need(len(names)==len(set(names)) and set(names)==set(files),'archive inventory mismatch')
    need(z.testzip() is None,'archive CRC failure')
    for i in z.infolist():
        need(stat.S_ISREG((i.external_attr>>16)&0xffff) and not i.is_dir(),'nonregular archive member')
        need(z.read(i.filename)==(root/i.filename).read_bytes(),'archive/root mismatch')
command=[sys.executable,'-I','-S']
if len(sys.argv)==5:command+=['-O']
command+=[str(root/data['checker'])]
r=subprocess.run(command,cwd=root,capture_output=True)
need(r.returncode==0 and not r.stderr,'checker failure')
need(r.stdout==(root/data['expected_output']).read_bytes(),'checker output mismatch')
sys.stdout.buffer.write(r.stdout)
