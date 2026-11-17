"""Data-only pause checkpoint, with no mathematical/project-code execution."""
from pathlib import Path
import hashlib,json,stat
from datetime import datetime,timezone
R=Path(__file__).resolve().parent;S=R.parents[1]/'sources'
def pin(p,root):
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode):raise RuntimeError('unexpected file type')
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
for n in ('CHECKPOINT.json','CHECKPOINT_MANIFEST.json'):
    if (R/n).exists():raise RuntimeError('checkpoint exists')
c=json.loads((R/'SOURCE_CUSTODY.json').read_text());sf,sd=inv(S)
if sf!=c['files'] or sd!=c['directories']:raise RuntimeError('source drift')
im=json.loads((R/'INITIAL_MANIFEST.json').read_text())
for p in im['payload_files']:
    if pin(R/p['path'],R)!=p:raise RuntimeError('initial drift')
if pin(R/'INITIAL_SEAL.json',R)['SHA256']!='a6011dfb3d656050816e267ddb27c5a6e037376289772d700f1056655fa6d2db':raise RuntimeError('initial seal drift')
if pin(R/'INITIAL_MANIFEST.json',R)['SHA256']!='2114c6f9c2963e4080ec6ac9790fba6f7af7ea7bb40c1d3858be01991843148d':raise RuntimeError('initial manifest drift')
files,dirs=inv(R);now=datetime.now(timezone.utc).isoformat()
m=dict(UTC=now,payload_files=files,directories=dirs,root_mode=oct(stat.S_IMODE(R.lstat().st_mode)),
       exact_excluded_terminal_controls=['CHECKPOINT_MANIFEST.json','CHECKPOINT.json'],includes_ignored_empty_files_and_modes=True)
with (R/'CHECKPOINT_MANIFEST.json').open('x') as f:f.write(json.dumps(m,indent=2)+'\n')
out=dict(UTC=now,record='23384924',row=176,status='PARTIAL_FROZEN_HOLD_FOR_ROOT_CHECKPOINT',
    manifest=pin(R/'CHECKPOINT_MANIFEST.json',R),initial_seal=pin(R/'INITIAL_SEAL.json',R),
    extent=dict(regular_files=len(files)+2,child_directories=len(dirs)),
    source163files21dirs_and_initial21files1dir_unchanged=True,
    all_handles_terminal=True,all_owned_writes_and_execution_held_after_this_seal=True,
    completion_percent_estimate=60,mathematical_verdict=None,follow_up=None,
    parent_handoff_readiness_pins_extent_only=True,publication_authority=False,self_hash_excluded=True)
with (R/'CHECKPOINT.json').open('x') as f:f.write(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checkpoint=pin(R/'CHECKPOINT.json',R),manifest=pin(R/'CHECKPOINT_MANIFEST.json',R),extent=out['extent']),indent=2))
