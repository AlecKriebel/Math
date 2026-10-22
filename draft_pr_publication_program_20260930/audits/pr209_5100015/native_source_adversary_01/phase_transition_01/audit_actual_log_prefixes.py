"""Read-only pre-phase95 local-prefix replay; bodies remain in memory only."""
from pathlib import Path
import os,stat,types,json,hashlib,tempfile
from datetime import datetime,timezone
BASE=Path(__file__).absolute().parent
q=BASE/'audit_phase_transition.py';test=types.ModuleType('actual_prefix_fixture');test.__file__=str(q)
exec(compile(q.read_bytes(),str(q),'exec'),test.__dict__)
def read_exact(path):
    if path.resolve()!=path:raise RuntimeError('Canonical log required')
    handles=[];fd=None
    try:
        current=Path('/');parent=os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);handles.append((current,parent,os.fstat(parent)))
        for part in path.parent.parts[1:]:
            current=current/part;parent=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent);handles.append((current,parent,os.fstat(parent)))
        fd=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent);a=os.fstat(fd)
        if not(stat.S_ISREG(a.st_mode) and a.st_size<=4000000):raise RuntimeError('Bounded regular log required')
        with os.fdopen(fd,'rb',closefd=False) as stream:raw=stream.read(4000001)
        b,e=os.fstat(fd),path.lstat();attrs=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
        if not(attrs(a)==attrs(b)==attrs(e) and len(raw)==b.st_size):raise RuntimeError('Log changed')
        for path,d,old in handles:
            now,entry=os.fstat(d),path.lstat()
            if not(stat.S_ISDIR(entry.st_mode) and (old.st_dev,old.st_ino)==(now.st_dev,now.st_ino)==(entry.st_dev,entry.st_ino)):raise RuntimeError('Ancestor changed')
        return raw
    finally:
        if fd is not None:os.close(fd)
        for _,d,_ in reversed(handles):os.close(d)
case=BASE.parents[1];paths=[case/'RESEARCH_LOG.md',case.parents[1]/'RESEARCH_LOG.md'];seeds=[read_exact(p) for p in paths];rows=[]
for phase in ('merge95','completion100'):
    result=test.fixture('repaired',phase,seeds=seeds)
    if not(result['accepted'] and result['logs_keep_local_prefix'] and result['logs_keep_native_prefix']):raise RuntimeError('Pre-phase95 snapshot no longer valid or transition failed: '+str(result))
    rows.append({'phase':phase,'result':result})
output={'schema':'pr209-independent-actual-local-log-prefix-structure-replay-v1','UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS_SOURCE_ONLY_CONDITIONAL','actual_local_log_preimages':[{'path':str(p),**test.pin(raw),'raw_body_exported':False} for p,raw in zip(paths,seeds)],'results':rows,'external_calls':0,'production_mutations':0,'actual_manifest_or_gate_created':False}
fd,name=tempfile.mkstemp(prefix='REPLAY_ACTUAL_LOCAL_LOG_PREFIX_',suffix='.json',dir=BASE)
with os.fdopen(fd,'wb') as stream:stream.write(test.enc(output))
print(json.dumps({'status':output['status'],'checks':2},sort_keys=True))
