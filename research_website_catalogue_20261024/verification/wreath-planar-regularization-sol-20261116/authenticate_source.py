"""Opaque custody only; no project/native scientific imports."""
from pathlib import Path
import hashlib,json,stat,datetime
R=Path(__file__).resolve().parent;S=R.parents[1]/'papers/23203143/sources'
def pin(p):
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode):raise RuntimeError('not regular')
    b=p.read_bytes()
    return dict(path=p.relative_to(S).as_posix(),bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=oct(stat.S_IMODE(st.st_mode)))
M=json.loads((S/'SOURCE_MANIFEST.json').read_text());F=json.loads((S/'SOURCE_FINAL.json').read_text())
files=[];dirs=[]
for p in sorted(S.rglob('*')):
    st=p.lstat()
    if stat.S_ISREG(st.st_mode):files.append(pin(p))
    elif stat.S_ISDIR(st.st_mode):dirs.append(dict(path=p.relative_to(S).as_posix(),mode=oct(stat.S_IMODE(st.st_mode))))
    else:raise RuntimeError('unexpected source topology')
if len(files)!=121 or len(dirs)!=20 or dirs!=M['directories']:raise RuntimeError('source extent/dirs mismatch')
if {x['path'] for x in files}!={x['path'] for x in M['files']}|{'SOURCE_MANIFEST.json','SOURCE_FINAL.json'}:raise RuntimeError('source paths mismatch')
for e in M['files']:
    if pin(S/e['path'])!=e:raise RuntimeError('source pin mismatch '+e['path'])
for k in ('SOURCE_MANIFEST','SOURCE_READY'):
    if pin(S/F[k]['path'])!=F[k]:raise RuntimeError('source control mismatch')
pdf=S/'assets/preprint.pdf'
if pdf.read_bytes()!=(S/'published-source/container-001/tree/publication/preprint.pdf').read_bytes():raise RuntimeError('PDF copy mismatch')
record=json.loads((S/'record.response.body').read_text())
for e in record['files']:
    b=(S/'assets'/e['key']).read_bytes()
    if len(b)!=e['size'] or 'md5:'+hashlib.md5(b).hexdigest()!=e['checksum']:raise RuntimeError('native asset identity mismatch')
print(json.dumps(dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_root=str(S),root_mode=oct(stat.S_IMODE(S.lstat().st_mode)),files=files,directories=dirs,
    regular_files=len(files),child_directories=len(dirs),source_controls_and_asset_identities_exact=True,standalone_embedded_PDF_identical=True,
    archived_code_opinion_results_hashed_opaquely=True,scientific_execution=False),indent=2))
