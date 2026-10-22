#!/usr/bin/env python3
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import datetime,hashlib,json,zipfile,re
HERE=Path(__file__).resolve().parent
PACKAGE=HERE.parent/'publication_package_v1'
def h(b): return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();s=p.stat()
 return dict(bytes=len(b),sha256=h(b),mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
files={str(p.relative_to(PACKAGE)):pin(p) for p in sorted(PACKAGE.rglob('*')) if p.is_file()}
(HERE/'package_before.json').write_text(json.dumps(files,indent=2)+'\n')
seal=json.loads((PACKAGE/'PACKAGE_SEAL.json').read_bytes())
errors=[]
for n,v in seal['files'].items():
 if n not in files or any(files[n][k]!=v[k] for k in ('bytes','sha256')): errors.append('seal pin '+n)
if set(files)-{'PACKAGE_SEAL.json'}!=set(seal['files']): errors.append('seal exact file set')
manifest=json.loads((PACKAGE/'PUBLIC_MATERIALS_MANIFEST.json').read_bytes())
for n,v in manifest['files'].items():
 if n not in files or any(files[n][k]!=v[k] for k in ('bytes','sha256')): errors.append('public pin '+n)
z=zipfile.ZipFile(PACKAGE/'verification-package.zip'); names=z.namelist(); zbad=z.testzip()
if zbad: errors.append('CRC '+zbad)
if len(names)!=len(set(names)): errors.append('duplicate ZIP names')
for n in names:
 if n.startswith('/') or '..' in Path(n).parts or n.endswith('/'): errors.append('ZIP path '+n)
 if n not in files or h(z.read(n))!=files[n]['sha256']: errors.append('ZIP byte mismatch '+n)
expected=set(manifest['files'])|{'PUBLIC_MATERIALS_MANIFEST.json'}
if set(names)!=expected: errors.append('ZIP public allowlist')
suspects=[]
for n in files:
 if re.search(r'(?i)(\.pdf$|\.py[co]$|__pycache__|node_modules|runtime_packages|\.env|credentials|token|screenshot|\.DS_Store)',n): suspects.append(n)
inventory={n:files[n] for n in files}
out=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),outer_count=len(files),seal_count=len(seal['files']),ZIP_count=len(names),ZIP_CRC_failure=zbad,ZIP_compressed_bytes=sum(x.compress_size for x in z.infolist()),public_manifest_count=len(manifest['files']),outer_only=sorted(set(files)-set(names)),suspect_paths=suspects,errors=errors)
(HERE/'package_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
print('RELATIVE INVENTORY')
for n in files: print(n)

