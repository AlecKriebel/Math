"""Trusted pre-execution inventory gate. Run only with Python -I -S -B."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: -I -S -B required')
import hashlib
import json
import os
from pathlib import Path
import stat
import zipfile

def reject(message):
    raise SystemExit('REJECT: ' + message)

def exact_path(value, kind):
    p = Path(value)
    if not p.is_absolute() or str(p.resolve()) != str(p):
        reject(kind + ' must be canonical absolute path')
    for part in [p] + list(p.parents):
        if part.is_symlink():
            reject(kind + ' symlink')
    return p

if len(sys.argv) != 4:
    reject('arguments: archive root external_manifest')
archive = exact_path(sys.argv[1], 'archive')
root = exact_path(sys.argv[2], 'root')
manifest_path = exact_path(sys.argv[3], 'manifest')
if not root.is_dir():
    reject('root not directory')
if not archive.is_file() or not manifest_path.is_file():
    reject('missing external input')
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
expected = {'REPORT.md', 'STATUS.json', 'VERIFICATION_METADATA.json', 'validate.py'}
if set(manifest.get('files', {})) != expected or manifest.get('entrypoint') != 'validate.py':
    reject('manifest inventory or entrypoint')
if set(p.name for p in root.iterdir()) != expected:
    reject('unexpected or missing root entry, including caches')
checked = {}
for name in sorted(expected):
    p = root / name
    if not stat.S_ISREG(p.lstat().st_mode) or p.is_symlink():
        reject('nonregular inventory member')
    blob = p.read_bytes()
    record = manifest['files'][name]
    if len(blob) != record['bytes'] or hashlib.sha256(blob).hexdigest() != record['sha256']:
        reject('member integrity: ' + name)
    checked[name] = blob
ab = archive.read_bytes()
if len(ab) != manifest['archive']['bytes'] or hashlib.sha256(ab).hexdigest() != manifest['archive']['sha256']:
    reject('archive integrity')
with zipfile.ZipFile(archive) as z:
    if len(z.infolist()) != len(expected) or set(z.namelist()) != expected:
        reject('archive inventory')
    for name in expected:
        zi = z.getinfo(name)
        if zi.is_dir() or zi.flag_bits & 1 or stat.S_ISLNK(zi.external_attr >> 16):
            reject('archive entry type')
        if z.read(name) != checked[name]:
            reject('archive and root mismatch')
# Isolated startup excludes cwd, PYTHONPATH, user-site and script directory.
# Reject any later path insertion of package or current directory.
for value in sys.path:
    if not value or Path(value).resolve() in {root, Path.cwd().resolve()}:
        reject('unsafe import search path')
entry = root / 'validate.py'
sys.argv = [str(entry)]
namespace = {'__name__':'__main__','__file__':str(entry),'__package__':None,'__cached__':None}
# Execute exactly the verified in-memory bytes; never reread a package entrypoint.
exec(compile(checked['validate.py'],str(entry),'exec'),namespace)
