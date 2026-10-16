from pathlib import Path
import hashlib,json,zipfile,stat,shutil,datetime,subprocess
A=Path(__file__).resolve().parents[2]; W=Path(__file__).resolve().parent; P=A/'publication'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(c,m):
    if not c: raise RuntimeError(m)
f=json.loads((P/'PREPUBLICATION_FREEZE.json').read_text()); fr={}
for n,r in f['files'].items():
    p=P/n; require(p.is_file() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'freeze mismatch '+n); fr[n]=r
z=P/'robinson-tangency-source-verification-v1.0.zip'; dest=W/'tmp/extracted'; dest.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(z) as zz:
    names=zz.namelist(); require(len(names)==len(set(names)),'Duplicate ZIP path')
    for i in zz.infolist():
        require(not Path(i.filename).is_absolute() and '..' not in Path(i.filename).parts,'unsafe path'); require(stat.S_ISREG(i.external_attr>>16),'nonregular ZIP member')
    zz.extractall(dest)
m=dest/'PACKAGE_MANIFEST.json'; require(sha(m)==f['package_manifest_sha256'],'manifest anchor'); data=json.loads(m.read_text()); actual={p.relative_to(dest).as_posix() for p in dest.rglob('*') if p.is_file()}; require(actual==set(data['files'])|{'PACKAGE_MANIFEST.json'},'membership');
for n,r in data['files'].items(): require((dest/n).stat().st_size==r['bytes'] and sha(dest/n)==r['sha256'],'payload mismatch '+n)
for n in ['note.tex','README.md','verify_package.py','requirements.txt']: require((dest/n).read_bytes()==(P/n).read_bytes(),'outer/inner '+n)
orig=A/'original/unsolved_math_prioritization/attempts/30000717'; on={p.relative_to(orig).as_posix():sha(p) for p in orig.rglob('*') if p.is_file()}; en={p.relative_to(dest/'original_packet').as_posix():sha(p) for p in (dest/'original_packet').rglob('*') if p.is_file()}; require(on==en,'original snapshot mismatch')
compile_dir=W/'tmp/compile';compile_dir.mkdir(exist_ok=True);shutil.copy2(P/'note.tex',compile_dir/'note.tex')
output={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen_files':fr,'zip_entries':names,'manifest_sha256':sha(m),'payload_count':len(data['files']),'original_count':len(on),'original_exact_match':True,'outer_inner_equal':True,'source_assets_present':[n for n in names if Path(n).suffix.lower() in ['.pdf','.png','.jpg','.parquet','.csv','.html']], 'zip_regular_unique_relative':True}
(W/'evidence/package_inventory.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ['frozen_files','zip_entries']},indent=2))
