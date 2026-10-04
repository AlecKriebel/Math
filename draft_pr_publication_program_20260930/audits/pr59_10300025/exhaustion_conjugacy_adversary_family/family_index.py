"""Small readonly index validator for future ROOT closure/readback; no acceptance."""
from pathlib import Path
import hashlib,json,os,stat
ROOT=Path(__file__).resolve().parent
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def validate():
    for name in ('INDEX.json','READY.json'):
        s=(ROOT/name).lstat()
        if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or stat.S_IMODE(s.st_mode)!=0o444: raise RuntimeError('index/readiness mode changed')
    ready=json.loads((ROOT/'READY.json').read_text())
    if sha(ROOT/'INDEX.json')!=ready['index_sha256']: raise RuntimeError('INDEX changed')
    index=json.loads((ROOT/'INDEX.json').read_text())
    expected=set(index['files'])|{'INDEX.json','READY.json'}
    observed=set()
    for p in ROOT.rglob('*'):
        if p.is_symlink(): raise RuntimeError('symlink in family')
        if p.is_file() and p!=ROOT/'SELF_MANIFEST.json': observed.add(p.relative_to(ROOT).as_posix())
    if observed!=expected: raise RuntimeError('file topology changed')
    dirs={'.':ROOT}
    dirs.update({p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('*') if p.is_dir()})
    if set(dirs)!=set(index['directories']): raise RuntimeError('directory topology changed')
    for name,mode in index['directories'].items():
        if stat.S_IMODE(dirs[name].stat().st_mode)!=mode: raise RuntimeError('directory mode changed')
    for name,pin in index['files'].items():
        p=ROOT/name;s=p.stat()
        if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or s.st_size!=pin['bytes'] or stat.S_IMODE(s.st_mode)!=pin['mode_07777'] or sha(p)!=pin['sha256']:
            raise RuntimeError('body/mode changed: '+name)
    if ready['role']!='SOURCE_READY_NOT_ROOT_ACCEPTANCE': raise RuntimeError('unexpected readiness role')
    return ready,index
