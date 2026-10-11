"""Local preparation archive builder; no publication service calls."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import stat
import sys
import zipfile
sys.dont_write_bytecode = True
base = Path(__file__).resolve().parent.parent
root = base/'publicfiles'
sys.path.insert(0, str(root/'support'))
from safe_output import write_new, json_bytes, exclusive_binary

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

files = []
for p in sorted(root.rglob('*')):
    if p.is_symlink():
        raise ValueError('No symlinks in proposed public payload')
    if p.is_file():
        files.append(dict(path=p.relative_to(root).as_posix(), sha256=sha(p), bytes=p.stat().st_size))
if any(e['path'] == 'MANIFEST.json' for e in files):
    raise ValueError('Never overwrite an already closed portable payload')
manifest = dict(schema='pr97-portable-payload/v1', created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                files=files, closure='Exactly all files except this manifest; ZIP supplied separately',
                publication_authorized=False, package_acceptance=False)
write_new(root/'MANIFEST.json', json_bytes(manifest))
archive = base/'pr97_support.zip'
with exclusive_binary(archive) as stream:
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():
                info = zipfile.ZipInfo(p.relative_to(root).as_posix(), (2026,10,6,0,0,0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, p.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
with zipfile.ZipFile(archive) as z:
    names = z.namelist()
    expected = {e['path'] for e in files} | {'MANIFEST.json'}
    if len(names) != len(set(names)) or set(names) != expected:
        raise ValueError('Archive closure mismatch')
    for name in names:
        if z.read(name) != (root/name).read_bytes():
            raise ValueError('Archive byte mismatch')
receipt = dict(status='PASS', created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
               payload_files=len(files), archive_members=len(names), archive_bytes=archive.stat().st_size,
               payload_manifest_sha256=sha(root/'MANIFEST.json'), zip_sha256=sha(archive),
               exact_archive_byte_equality=True, third_party_bodies_or_pixels_copied=False,
               publication_authorized=False, whole_package_acceptance=False)
write_new(base/'private/ARCHIVE_BUILD_RECEIPT.json', json_bytes(receipt))
print(json.dumps(receipt, indent=2))
