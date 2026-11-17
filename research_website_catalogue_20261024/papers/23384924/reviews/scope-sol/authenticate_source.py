"""Opaque source byte/mode custody only; project code is never imported."""
from pathlib import Path
import stat, hashlib, json
from datetime import datetime, timezone
R=Path(__file__).resolve().parent
S=R.parents[1]/'sources'
def pin(p):
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode): raise RuntimeError('not regular: '+str(p))
    b=p.read_bytes()
    return dict(path=p.relative_to(S).as_posix(),bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=oct(stat.S_IMODE(st.st_mode)))
M=json.loads((S/'SOURCE_MANIFEST.json').read_text())
F=json.loads((S/'SOURCE_FINAL.json').read_text())
files=[]; dirs=[]
for p in sorted(S.rglob('*')):
    st=p.lstat()
    if stat.S_ISREG(st.st_mode): files.append(pin(p))
    elif stat.S_ISDIR(st.st_mode): dirs.append(dict(path=p.relative_to(S).as_posix(),mode=oct(stat.S_IMODE(st.st_mode))))
    else: raise RuntimeError('unexpected object: '+str(p))
if len(files)!=163 or len(dirs)!=21: raise RuntimeError('source extent mismatch')
if dirs!=M['directories']: raise RuntimeError('directory mismatch')
if sorted(x['path'] for x in files)!=M['actual_file_paths_including_controls']: raise RuntimeError('source path mismatch')
for e in M['files']:
    if pin(S/e['path'])!=e: raise RuntimeError('source file mismatch: '+e['path'])
if pin(S/'SOURCE_MANIFEST.json')!=F['SOURCE_MANIFEST']: raise RuntimeError('manifest binding mismatch')
if pin(S/'SOURCE_READY.json')!=F['SOURCE_READY']: raise RuntimeError('ready binding mismatch')
if oct(stat.S_IMODE(S.lstat().st_mode))!=M['root_mode']: raise RuntimeError('root mode mismatch')
pdf=S/'assets/real_schlicht_preschwarzian.pdf'
embedded=S/'published-source/container-001/tree/real_schlicht_preschwarzian.pdf'
if pdf.read_bytes()!=embedded.read_bytes(): raise RuntimeError('PDF copy mismatch')
record=json.loads((S/'record.response.body').read_text())
for e in record['files']:
    p=S/'assets'/e['key']; b=p.read_bytes()
    if len(b)!=e['size'] or 'md5:'+hashlib.md5(b).hexdigest()!=e['checksum']: raise RuntimeError('native asset identity mismatch')
out=dict(UTC=datetime.now(timezone.utc).isoformat(),source_root=str(S),root_mode=M['root_mode'],files=files,directories=dirs,
    regular_files=len(files),child_directories=len(dirs),all_frozen_manifest_byte_modes_exact=True,
    standalone_embedded_PDF_identical=True,native_asset_order=[x['key'] for x in record['files']],
    source_bodies_hashed_opaquely=True,project_or_scientific_execution=False)
print(json.dumps(out,indent=2))
