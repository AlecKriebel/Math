"""Read-only validation of the exact whole publication payload; stdlib only."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import hashlib,json,zipfile,stat
A=Path(__file__).resolve().parent.parent
P=A/'publication_package_v2'
EXPECT='89bbfc82c0ae2b80fca046671681f94cef28f130d01df4a3b52036efd7a95ad5'
checks=[]
def need(c,m):
    if not c:raise RuntimeError(m)
    checks.append(m)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def safe(rel):
    p=PurePosixPath(rel)
    return not p.is_absolute() and '..' not in p.parts and '\\' not in rel
sealbytes=(P/'PACKAGE_SEAL.json').read_bytes()
need(len(sealbytes)==90105 and hashlib.sha256(sealbytes).hexdigest()==EXPECT,'exact seal size/SHA256')
s=json.loads(sealbytes)
actual={str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()}
need(actual==set(s['package_safe_files'])|{'PACKAGE_SEAL.json'},'exhaustive outer package file set')
for rel,pn in s['package_safe_files'].items():
    f=P/rel;need(safe(rel) and not f.is_symlink() and pin(f.read_bytes())==pn,'sealed file '+rel)
for rel,pn in s['upload_files'].items():need(pin((P/rel).read_bytes())==pn,'upload file '+rel)
mat=P/'materials';m=json.loads((mat/'MANIFEST.json').read_bytes())
files={str(f.relative_to(mat)) for f in mat.rglob('*') if f.is_file()}
need(files==set(m['files'])|{'MANIFEST.json'},'exhaustive materials manifest')
for rel,pn in m['files'].items():need(safe(rel) and pin((mat/rel).read_bytes())==pn,'manifest '+rel)
with zipfile.ZipFile(P/'verification-package.zip') as z:
    names=z.namelist();need(len(names)==len(set(names))==233,'ZIP exactly 233 unique entries')
    need(z.testzip() is None,'ZIP CRC all entries')
    need(set(names)==files==set(s['zip_entries']),'ZIP/extracted/seal exact file sets')
    for rel in names:
        info=z.getinfo(rel);need(safe(rel) and not info.is_dir(),'safe regular ZIP name '+rel)
        need(stat.S_IFMT(info.external_attr>>16)!=stat.S_IFLNK,'ZIP not symlink '+rel)
        b=z.read(rel);need(pin(b)==s['zip_entries'][rel] and b==(mat/rel).read_bytes(),'ZIP exact bytes '+rel)
metadata=json.loads((mat/'metadata.json').read_bytes());deposit=json.loads((P/'zenodo-deposit.json').read_bytes())
need(s['metadata_exact']==metadata==deposit['metadata'],'exact metadata equality')
need([x['path'] for x in deposit['files']]==list(s['upload_files']),'exact three upload names/order')
need((P/'outer_pedal_flag.tex').read_bytes()==(mat/'outer_pedal_flag.tex').read_bytes(),'standalone/archive source equality')
c=json.loads((mat/'audit/ORIGINAL_SUBMISSION_CUSTODY.json').read_bytes());orig=mat/'audit/original_submitted_head'
orig_files={str(f.relative_to(orig)) for f in orig.rglob('*') if f.is_file()}
need(orig_files==set(c['files']) and len(orig_files)==c['file_count']==24,'complete original 24 file set')
for rel,pn in c['files'].items():
    b=(orig/rel).read_bytes();need(pin(b)=={k:pn[k] for k in ('bytes','sha256')},'original SHA/size '+rel)
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    need(blob==pn['git_blob'],'original native Git blob '+rel)
need(sum((orig/f).stat().st_size for f in orig_files)==c['total_native_bytes']==54661,'original total bytes')
# Archival suffix scan is deliberately content-independent: no prior verdict is read.
for rel in files:
    need(Path(rel).suffix.lower() not in {'.pdf','.jpg','.jpeg','.png','.whl','.so','.dylib','.zip','.html'},'no fulltext/dependency/browser binary '+rel)
need(not s['theorem_novelty_firstness_independence_certified'],'seal no novelty/firstness/independence certification')
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','seal':pin(sealbytes),'outer_files_excluding_seal':len(s['package_safe_files']),'materials_files':len(files),'manifest_pins':len(m['files']),'zip_entries':len(s['zip_entries']),'original_files':len(orig_files),'checks':len(checks),'checks_details':checks},indent=2))
