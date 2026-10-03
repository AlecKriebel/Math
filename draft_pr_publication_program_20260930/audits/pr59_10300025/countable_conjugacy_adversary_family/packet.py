"""Read only exact family body/domain/mode pins. Never execute mathematical code."""
import hashlib,json,pathlib,stat
ROOT=pathlib.Path(__file__).resolve().parent
SELF='ROOT_MANIFEST.json'
def descriptor(p):
    s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and s.st_mode&0o7777==0o444
    return {'path':p.relative_to(ROOT).as_posix(),'bytes':s.st_size,
            'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode_07777':'0444'}
def validate(closed=False):
    idx=json.loads((ROOT/'INDEX.json').read_bytes());ready=json.loads((ROOT/'READY.json').read_bytes())
    paths=set(idx['domain'])|{'INDEX.json','READY.json'}|({SELF} if closed else set())
    found=set();dirs={'.'}
    for p in ROOT.rglob('*'):
        s=p.lstat()
        if stat.S_ISDIR(s.st_mode):
            assert s.st_mode&0o7777==0o755;dirs.add(p.relative_to(ROOT).as_posix())
        else:descriptor(p);found.add(p.relative_to(ROOT).as_posix())
    assert ROOT.lstat().st_mode&0o7777==0o755
    assert found==paths and dirs==set(idx['directories']) and set(idx['entries'])==set(idx['domain'])
    for n,e in idx['entries'].items():assert descriptor(ROOT/n)==e
    assert set(ready['bindings'])=={'INDEX.json','REPORT.md','VERDICT.json','UNIVERSAL_PROOF.md'}
    for n,e in ready['bindings'].items():assert descriptor(ROOT/n)==e
    assert ready['status']=='PASS_LITERAL_READY_FOR_ROOT' and ready['ROOT_executed'] is False
    return [descriptor(ROOT/n) for n in sorted(paths-({SELF} if closed else set()))]
