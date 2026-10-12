"""Small fixed-domain byte checker for this family only. No external writes."""
import datetime,hashlib,json,os,stat
from pathlib import Path

B=Path(__file__).resolve().parent
H='465d771ec1ddc91877e8d9db51ed59aea1b0d97d'
I='INDEX.json'; R='READY.json'; M='SELF_MANIFEST.json'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def d(p):
    s=p.lstat(); assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
    data=p.read_bytes()
    return {'name':p.name,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'full_st_mode':oct(s.st_mode),'mode_07777':format(s.st_mode&0o7777,'04o'),'links':1}
def read(name): return json.loads((B/name).read_text())
def write_once(name,body):
    data=(json.dumps(body,indent=2,sort_keys=True)+'\n').encode()
    fd=os.open(B/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
    try:
        os.fchmod(fd,0o444); off=0
        while off<len(data): off+=os.write(fd,data[off:])
        os.fsync(fd)
    finally: os.close(fd)
def verify(closed=False):
    index=read(I); ready=read(R)
    assert index['schema']=='pr58-transform-fixed-index/v1'
    assert ready['schema']=='pr58-transform-ready/v1'
    assert index['reserved']==[I,R,M]
    assert index['head']==H==ready['head']
    names=[x['name'] for x in index['bodies']]
    assert names==sorted(set(names)) and not set(names)&{I,R,M}
    assert index['directory']=={'path':str(B),'mode_07777':'0755','full_st_mode':oct(B.lstat().st_mode)}
    assert stat.S_ISDIR(B.lstat().st_mode) and not B.is_symlink()
    assert B.lstat().st_mode&0o7777==0o755
    assert {p.name for p in B.iterdir()}==set(names+[I,R]+([M] if closed else []))
    assert index['bodies']==[d(B/n) for n in names]
    assert all(d(p)['mode_07777']=='0444' for p in B.iterdir())
    assert ready['bindings']==[d(B/n) for n in [I,'REPORT.md','VERDICT.json']]
    assert ready['ROOT_helpers_unexecuted_at_handoff'] is True
    assert ready['SELF_manifest_absent_at_handoff'] is True
    assert ready['ROOT_or_math_acceptance'] is False
    return index,ready
