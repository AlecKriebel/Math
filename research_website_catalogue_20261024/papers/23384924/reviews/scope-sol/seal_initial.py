"""Source-only finite initial seal; no scientific or project code import."""
from pathlib import Path
import hashlib,json,stat
from datetime import datetime,timezone
R=Path(__file__).resolve().parent;S=R.parents[1]/'sources'
def pin(p,root):
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode):raise RuntimeError('not regular: '+str(p))
    b=p.read_bytes()
    return dict(path=p.relative_to(root).as_posix(),bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=oct(stat.S_IMODE(st.st_mode)))
def inv(root):
    files=[];dirs=[]
    for p in sorted(root.rglob('*')):
        st=p.lstat()
        if stat.S_ISREG(st.st_mode):files.append(pin(p,root))
        elif stat.S_ISDIR(st.st_mode):dirs.append(dict(path=p.relative_to(root).as_posix(),mode=oct(stat.S_IMODE(st.st_mode))))
        else:raise RuntimeError('unexpected object: '+str(p))
    return files,dirs
for n in ('INITIAL_MANIFEST.json','INITIAL_SEAL.json'):
    if (R/n).exists():raise RuntimeError('already sealed')
custody=json.loads((R/'SOURCE_CUSTODY.json').read_text())
sf,sd=inv(S)
if sf!=custody['files'] or sd!=custody['directories']:raise RuntimeError('source drift')
if oct(stat.S_IMODE(S.lstat().st_mode))!=custody['root_mode']:raise RuntimeError('source root mode drift')
files,dirs=inv(R);now=datetime.now(timezone.utc).isoformat()
manifest=dict(schema='source-first-scope-initial-manifest-v1',UTC=now,payload_files=files,directories=dirs,
    root_mode=oct(stat.S_IMODE(R.lstat().st_mode)),exact_excluded_terminal_controls=['INITIAL_MANIFEST.json','INITIAL_SEAL.json'],includes_ignored_empty_and_all_modes=True)
with (R/'INITIAL_MANIFEST.json').open('x') as f:f.write(json.dumps(manifest,indent=2)+'\n')
seal=dict(schema='source-first-scope-initial-seal-v1',UTC=now,record='23384924',row=176,
    status='SOURCE_ONLY_INITIAL_AND_HAND_RESULTS_FROZEN_BEFORE_SUPPORT_OPINIONS_PRIMARY_BODIES',
    manifest=pin(R/'INITIAL_MANIFEST.json',R),INITIAL=pin(R/'INITIAL.json',R),hand_results=pin(R/'INITIAL_HAND_RESULTS.md',R),
    source_final=pin(S/'SOURCE_FINAL.json',S),all163source_files21dirs_bytes_modes_unchanged=True,
    all293TeX_5PDF_text_pages_and5fresh_pixels_personally_read=True,
    current_root_peer_archived_opinion_support_code_foreign_bodies_opened=False,
    informed_prior_exposure_disclosed=True,scientific_verdict=None,follow_up=None,
    source_gate_percent=100,assigned_family_percent_estimate=40,publication_authority=False,
    finite_extent=dict(regular_files=len(files)+2,child_directories=len(dirs),all_paths=sorted([x['path'] for x in files]+['INITIAL_MANIFEST.json','INITIAL_SEAL.json']),directories=dirs),
    parent_handoff_readiness_pins_extent_only=True,self_hash_excluded=True)
with (R/'INITIAL_SEAL.json').open('x') as f:f.write(json.dumps(seal,indent=2)+'\n')
for p in files:
    if pin(R/p['path'],R)!=p:raise RuntimeError('payload drift during seal')
print(json.dumps(dict(seal=pin(R/'INITIAL_SEAL.json',R),manifest=pin(R/'INITIAL_MANIFEST.json',R),regular_files=len(files)+2,child_directories=len(dirs)),indent=2))
