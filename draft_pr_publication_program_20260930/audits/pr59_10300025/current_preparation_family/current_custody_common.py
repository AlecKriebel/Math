"""Exact current SOURCE custody primitives; no mathematical/native authority."""
from pathlib import Path
import hashlib
import json
import stat
import os
import datetime

N=Path(__file__).absolute().parent


def need(ok,message):
    if not ok:raise RuntimeError(message)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def ref(p):
    s=p.lstat();need(not p.is_symlink() and stat.S_ISREG(s.st_mode),'Regular SOURCE body')
    b=p.read_bytes();t=p.lstat()
    need((s.st_ino,s.st_size,s.st_mode,s.st_mtime_ns,s.st_ctime_ns)==(t.st_ino,t.st_size,t.st_mode,t.st_mtime_ns,t.st_ctime_ns),'SOURCE changed while reading')
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'full_mode_07777':format(stat.S_IMODE(s.st_mode),'04o')}
def load(p):return json.loads(p.read_bytes())
def verify_row(z):need(ref(Path(z['path']))==z,'Complete SOURCE body/type/bytes/mode: '+z['path'])
def verify_external():
    x=load(N/'EXTERNAL_BINDINGS.json')
    for z in x['files']:verify_row(z)
    expected={z['path'] for z in x['files']};d={z['path']:z for z in x['directories']}
    for name,z in d.items():
        q=Path(name);need(q.is_dir() and not q.is_symlink() and format(stat.S_IMODE(q.stat().st_mode),'04o')==z['full_mode_07777'],'External directory modes')
        need(all(str(p) in expected or str(p) in d for p in q.iterdir()),'Exact external completed topology')
    return len(x['files'])
def verify_current(closed=False):
    need(__debug__,'No optimized guard execution')
    index=load(N/'INDEX.json');ready=load(N/'READY.json')
    verify_row(ready['INDEX'])
    files=index['files'];expected={z['path'] for z in files}|{str(N/'INDEX.json'),str(N/'READY.json')}
    if closed:expected.add(str(N/'ROOT_MANIFEST.json'))
    need(expected=={str(p) for p in N.rglob('*') if p.is_file()},'Exact current SOURCE full file domain')
    for z in files:verify_row(z)
    dirs=index['directories'];need({z['path'] for z in dirs}=={str(p) for p in [N]+sorted(p for p in N.rglob('*') if p.is_dir())},'Exact current directory domain')
    for z in dirs:
        p=Path(z['path']);need(not p.is_symlink() and format(stat.S_IMODE(p.stat().st_mode),'04o')==z['full_mode_07777'],'Current directory mode')
    need(ref(N/'INDEX.json')['full_mode_07777']=='0444' and ref(N/'READY.json')['full_mode_07777']=='0444','Fixed index/ready modes')
    sci=load(N.parent/'original_preparation_family/SCIENCE_INDEX.json')
    for name,z in sci.items():
        a=ref(N/'original_archive'/name)
        need(a['bytes']==z['bytes'] and a['sha256']==z['sha256'],'Original archive exact23 body join')
    for name in ['KNOWN_RESULT.md','verify.py','verification.json','prior_report.json','source_provenance.json']:
        a=ref(N/'current'/name);b=ref(N/'original_archive'/name)
        need(a['bytes']==b['bytes'] and a['sha256']==b['sha256'],'Current mathematical/history body exact')
    status=load(N/'STATUS.json');need(status['scientific_disposition']=='already_solved' and status['original_substantive_attempt_budget']=='1/5' and status['paper_required'] is False,'Exact qualified disposition')
    turns=load(N/'current/turns.json');need(len(turns)==1 and turns[0]['turn']==1 and turns[0]['discovery_credit'] is False,'No added turn or discovery')
    external=verify_external()
    return {'current_prepared_files':len(expected)-(1 if closed else 0),'external_completed_files':external,'mathematical_review_credit':0,'native_acceptance':False,'paper_or_DOI':False}
def write_new(p,b):
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
    with os.fdopen(fd,'wb') as f:f.write(b);f.flush();os.fchmod(f.fileno(),0o444);os.fsync(f.fileno())
