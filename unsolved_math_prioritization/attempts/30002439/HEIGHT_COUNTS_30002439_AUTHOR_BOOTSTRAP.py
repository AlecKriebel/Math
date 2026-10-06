"""External trust root: verify every bundle byte before executing bundle code."""
import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit('Use python -I -S; optimized mode is also supported')
import contextlib
import hashlib
import io
import json
import pathlib
import stat
import zipfile
PINNED_MANIFEST_SHA256 = '3527edc41af60fc640160c63416aacccc212d99d04f6f9a0c54cd7e477b4cfec'

def reject(message):
    raise SystemExit(message)

def real_path(path, kind):
    for part in [path]+list(path.parents):
        if stat.S_ISLNK(part.lstat().st_mode):
            reject('symlink path forbidden')
    mode=path.lstat().st_mode
    if kind=='file' and not stat.S_ISREG(mode):
        reject('expected regular file')
    if kind=='directory' and not stat.S_ISDIR(mode):
        reject('expected real root directory')

if len(sys.argv)!=4:
    reject('usage: bootstrap EXTRACTED_ROOT ARCHIVE EXTERNAL_MANIFEST')
root,archive,manifest=(pathlib.Path(s).absolute() for s in sys.argv[1:])
real_path(root,'directory');real_path(archive,'file');real_path(manifest,'file')
if root in archive.parents or root in manifest.parents:
    reject('archive and manifest must be external')
raw=manifest.read_bytes()
if hashlib.sha256(raw).hexdigest()!=PINNED_MANIFEST_SHA256:
    reject('pinned external manifest mismatch')
data=json.loads(raw);expected=data['files']
if {p.name for p in root.iterdir()}!=set(expected):
    reject('strict root inventory mismatch')
payloads={}
for name,record in expected.items():
    if pathlib.PurePosixPath(name).name!=name or name in ('.','..'):
        reject('unsafe inventory name')
    p=root/name;real_path(p,'file');b=p.read_bytes()
    if len(b)!=record['bytes'] or hashlib.sha256(b).hexdigest()!=record['sha256']:
        reject('member digest mismatch: '+name)
    payloads[name]=b
b=archive.read_bytes()
if len(b)!=data['archive']['bytes'] or hashlib.sha256(b).hexdigest()!=data['archive']['sha256']:
    reject('archive digest mismatch')
with zipfile.ZipFile(io.BytesIO(b)) as z:
    names=z.namelist()
    if len(names)!=len(set(names)) or set(names)!=set(expected):
        reject('archive inventory mismatch')
    if z.testzip() is not None:
        reject('archive CRC failure')
    for item in z.infolist():
        if item.is_dir() or not stat.S_ISREG((item.external_attr>>16)&0xffff):
            reject('non-regular archive member')
        if z.read(item)!=payloads[item.filename]:
            reject('archive and extracted bytes differ')
# Only now may any repository-owned code run. Execute the checked bytes rather
# than reopening a mutable pathname. No repository module is imported.
scope={'__name__':'__main__','__file__':str(root/'verify_math.py'),'_BUNDLE_VERIFIED':'height-counts-30002439-v1'}
output=io.StringIO()
with contextlib.redirect_stdout(output):
    exec(compile(payloads['verify_math.py'],str(root/'verify_math.py'),'exec'),scope)
result=output.getvalue().encode()
if result!=payloads['RESULTS.json']:
    reject('checker output mismatch')
sys.stdout.buffer.write(result)
