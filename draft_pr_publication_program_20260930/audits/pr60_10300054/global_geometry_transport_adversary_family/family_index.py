"""Readonly exact SOURCE validator; no mathematical/native acceptance."""
from pathlib import Path
import hashlib,json,stat
ROOT=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def validate():
    for name in ('INDEX.json','READY.json'):
        s=(ROOT/name).lstat()
        if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or stat.S_IMODE(s.st_mode)!=0o444: raise RuntimeError('index/readiness modes')
    ready=json.loads((ROOT/'READY.json').read_text());index=json.loads((ROOT/'INDEX.json').read_text())
    if ready['role']!='SOURCE_READY_NOT_ROOT_ACCEPTANCE' or sha(ROOT/'INDEX.json')!=ready['index_sha256']: raise RuntimeError('readiness/index changed')
    observed=set();dirs={'.':ROOT}
    for p in ROOT.rglob('*'):
        if p.is_symlink(): raise RuntimeError('symlink in family')
        if p.is_dir(): dirs[p.relative_to(ROOT).as_posix()]=p
        elif p.is_file() and p!=ROOT/'SELF_MANIFEST.json': observed.add(p.relative_to(ROOT).as_posix())
    if observed!=set(index['files'])|{'INDEX.json','READY.json'} or set(dirs)!=set(index['directories']): raise RuntimeError('topology changed')
    for name,mode in index['directories'].items():
        if stat.S_IMODE(dirs[name].stat().st_mode)!=mode: raise RuntimeError('directory mode changed')
    def check(p,pin):
        s=p.lstat()
        if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or s.st_size!=pin['bytes'] or stat.S_IMODE(s.st_mode)!=pin['mode_07777'] or sha(p)!=pin['sha256']: raise RuntimeError('body/mode changed: '+str(p))
    for name,pin in index['files'].items(): check(ROOT/name,pin)
    for pin in json.loads((ROOT/'source_reference_pins.json').read_text())['references']: check(Path(pin['path']),pin)
    return ready,index
