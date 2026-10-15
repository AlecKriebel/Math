"""SOURCE-only own review custody utilities, not production rollback code."""
import hashlib
import json
from pathlib import Path
import stat
H=Path(__file__).resolve().parent
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def row(p):
    need(p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'Regular own review member')
    b=p.read_bytes()
    return {'path':p.relative_to(H).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
def topology():
    need(H.is_dir() and not H.is_symlink() and stat.S_IMODE(H.stat().st_mode)==0o755,'Exact review root mode')
    files=[]; dirs=[]
    for p in H.rglob('*'):
        need(not p.is_symlink(),'No review symlink')
        if p.is_file(): files.append(row(p))
        else:
            need(p.is_dir(),'No special review member')
            dirs.append({'path':p.relative_to(H).as_posix(),'full_mode':stat.S_IMODE(p.stat().st_mode)})
    return sorted(files,key=lambda z:z['path']),sorted(dirs,key=lambda z:z['path'])
def validate(frozen=False):
    ready=json.loads((H/'READY.json').read_bytes()); files,dirs=topology()
    names={z['path'] for z in ready['files']}|{'READY.json'}|({'SELF_MANIFEST.json'} if frozen else set())
    need({z['path'] for z in files}==names and dirs==ready['directories'],'Complete exact review topology')
    actual={z['path']:z for z in files}
    for z in ready['files']:
        need(actual[z['path']]=={**z,'full_mode':0o444} if frozen else actual[z['path']]==z,'Whole review body/fullmode')
    need(actual['READY.json']['full_mode']==(0o444 if frozen else 0o644),'READY exact mode')
    need(ready['source_only'] is True and ready['ROOT_execution_approval_claimed'] is False and ready['math_review_credit']==0,'Review authority boundary')
    return ready,files,dirs
