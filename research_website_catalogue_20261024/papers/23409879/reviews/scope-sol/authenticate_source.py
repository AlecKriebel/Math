#!/usr/bin/env python3
"""Opaque source authentication only; no manuscript/support-code interpretation."""
import datetime, hashlib, json, stat
from pathlib import Path
S=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23409879/sources')
def need(x,label):
    if not x: raise ValueError(label)
def raw(p):
    need(p.is_absolute() and all(not x.is_symlink() for x in [p,*p.parents]),'ordinary source path')
    a=p.lstat(); need(stat.S_ISREG(a.st_mode),'regular source file'); b=p.read_bytes(); z=p.lstat()
    need((a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns),'stable opaque source read'); return b
def pin(p):
    b=raw(p); return dict(path=p.relative_to(S).as_posix(),bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=oct(stat.S_IMODE(p.lstat().st_mode)))
final=pin(S/'SOURCE_FINAL.json'); manifest_pin=pin(S/'SOURCE_MANIFEST.json')
need((final['bytes'],final['SHA256'])==(909,'a9ba3a7a10423aeda0e4af4d0395b408592f9b8d05209e37dbdb56ee04ea7e17'),'actual SOURCE_FINAL')
need((manifest_pin['bytes'],manifest_pin['SHA256'])==(20071,'741015d090043331f6707051111c4c37f4a0d7e44141f9d663e140fabe12db06'),'actual SOURCE_MANIFEST')
manifest=json.loads(raw(S/'SOURCE_MANIFEST.json'))
files=[]; directories=[]
for p in sorted(S.rglob('*')):
    kind=p.lstat().st_mode; need(not p.is_symlink(),'no source symlink')
    if stat.S_ISREG(kind): files.append(pin(p))
    elif stat.S_ISDIR(kind): directories.append(dict(path=p.relative_to(S).as_posix(),mode=oct(stat.S_IMODE(kind))))
    else: raise ValueError('special source entry')
need(len(files)==77 and len(directories)==10 and directories==manifest['directories'],'complete77/10 source namespace')
expected={r['path']:r for r in manifest['files']}; expected.update(SOURCE_FINAL=final)
expected.pop('SOURCE_FINAL')
expected['SOURCE_FINAL.json']=final; expected['SOURCE_MANIFEST.json']=manifest_pin
need({r['path']:r for r in files}==expected,'every actual source byte and mode')
need(sorted(expected)==manifest['actual_file_paths_including_controls'] and oct(stat.S_IMODE(S.lstat().st_mode))==manifest['root_mode'],'complete finite names/root mode')
native=S/'assets/outer_focal_period.tex'
embedded=S/'published-source/container-001/tree/outer_focal_period.tex'
need(raw(native)==raw(embedded),'standalone and controlling extracted TeX identical')
need(pin(native)['bytes']==16515 and pin(native)['SHA256']=='5df48a79187c73fe0ceba5ae34970906588b3b9a4401655a15f5c7c792ad5589','actual controlling TeX')
pdf=pin(S/'assets/outer_focal_period.pdf')
need(pdf['bytes']==78866 and pdf['SHA256']=='846e4d9b67d240b60499fb0eab52c345d4a74b3279f869717deff47230b0392f','actual native PDF')
print(json.dumps(dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='WHOLE77_SOURCE_BYTES_MODES10_DIRS_AUTHENTICATED_BEFORE_MANUSCRIPT_READING',source_root=str(S),root_mode=manifest['root_mode'],files=files,directories=directories,regular_files=77,child_directories=10,standalone_and_embedded_TeX_identical=True,closed_support_bodies_opaque_hashes_only=True,source_or_scientific_execution=False),indent=2))
