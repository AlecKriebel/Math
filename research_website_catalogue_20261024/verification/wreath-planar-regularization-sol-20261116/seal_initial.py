"""Data-only informed-source initial seal; no project/native/foreign mathematical execution."""
from pathlib import Path
import hashlib,json,stat,datetime
R=Path(__file__).resolve().parent;S=R.parents[1]/'papers/23203143/sources'
def pin(p,root):
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode):raise RuntimeError('not regular')
    b=p.read_bytes()
    return dict(path=p.relative_to(root).as_posix(),bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=oct(stat.S_IMODE(st.st_mode)))
def inv(root):
    fs=[];ds=[]
    for p in sorted(root.rglob('*')):
        st=p.lstat()
        if stat.S_ISREG(st.st_mode):fs.append(pin(p,root))
        elif stat.S_ISDIR(st.st_mode):ds.append(dict(path=p.relative_to(root).as_posix(),mode=oct(stat.S_IMODE(st.st_mode))))
        else:raise RuntimeError('unexpected object')
    return fs,ds
for n in ('INITIAL_MANIFEST.json','INITIAL_SEAL.json'):
    if (R/n).exists():raise RuntimeError('already sealed')
c=json.loads((R/'SOURCE_CUSTODY.json').read_text());sf,sd=inv(S)
if sf!=c['files'] or sd!=c['directories'] or oct(stat.S_IMODE(S.lstat().st_mode))!=c['root_mode']:raise RuntimeError('source drift')
for n in ('SOURCE_AUTH.stderr.txt','PDFINFO.stderr.txt','PDFTEXT.stderr.txt','RASTER.stdout.txt','RASTER.stderr.txt'):
    if (R/n).read_bytes()!=b'':raise RuntimeError('nonempty source tool stream '+n)
fs,ds=inv(R);now=datetime.datetime.now(datetime.timezone.utc).isoformat()
m=dict(schema='informed-source-interface-initial-manifest-v1',UTC=now,payload_files=fs,directories=ds,
    root_mode=oct(stat.S_IMODE(R.lstat().st_mode)),exact_excluded_terminal_controls=['INITIAL_MANIFEST.json','INITIAL_SEAL.json'],all_ignored_empty_modes_included=True)
with (R/'INITIAL_MANIFEST.json').open('x') as f:f.write(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
seal=dict(schema='informed-source-interface-initial-seal-v1',UTC=now,record='23203143',row=164,
    status='SOURCE_PROGRAM_AND_HAND_CHECKS_FROZEN_BEFORE_CURRENT_OPINIONS_OR_FOREIGN_PROOFS',
    INITIAL=pin(R/'INITIAL.json',R),hand_checks=pin(R/'INITIAL_HAND_CHECKS.md',R),manifest=pin(R/'INITIAL_MANIFEST.json',R),
    source_final=pin(S/'SOURCE_FINAL.json',S),source121files20dirs_bytes_modes_unchanged=True,
    full212TeX_all8PDFtext_pages_and8fresh_source_pixels_personally_read=True,
    previous164scope_and_related_exposure_disclosed=True,current_or_old_local_opinions_and_foreign_bodies_opened_for_this_audit=False,
    scientific_disposition=None,full_paper_certification=False,focused_percent_estimate=40,follow_up=None,publication_authority=False,
    extent=dict(regular_files=len(fs)+2,child_directories=len(ds),all_paths=sorted([x['path'] for x in fs]+['INITIAL_MANIFEST.json','INITIAL_SEAL.json']),directories=ds),self_hash_excluded=True)
with (R/'INITIAL_SEAL.json').open('x') as f:f.write(json.dumps(seal,ensure_ascii=False,indent=2)+'\n')
for x in fs:
    if pin(R/x['path'],R)!=x:raise RuntimeError('payload drift during seal')
print(json.dumps(dict(INITIAL_SEAL=pin(R/'INITIAL_SEAL.json',R),INITIAL_MANIFEST=pin(R/'INITIAL_MANIFEST.json',R),regular_files=len(fs)+2,child_directories=len(ds)),indent=2))
