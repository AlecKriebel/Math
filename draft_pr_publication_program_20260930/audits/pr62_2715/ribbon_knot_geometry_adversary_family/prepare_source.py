#!/usr/bin/env python3
"""Pin this SOURCE-only family and check existing preserved original bodies."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,stat

BASE=Path(__file__).resolve().parent
AUTH=BASE.parent/'original_preparation_family'/'ORIGINAL_AUTHENTICATION.json'
def pin(p):
    s=p.lstat()
    if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1:
        raise RuntimeError('nonregular or multiply linked file: '+str(p))
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'full_mode_07777':format(s.st_mode&0o7777,'04o'),'nlink':s.st_nlink}

auth=json.loads(AUTH.read_text())
if auth['head']!='98cc2821e9376507caf2d2c57414f7c7e7719c1b' or auth['science_count']!=17:
    raise RuntimeError('unexpected original authentication scope')
external=[]
for expected in auth['scientific_files']:
    p=Path(expected['path']);actual=pin(p);b=p.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    if any(actual[k]!=expected[k] for k in ('bytes','sha256','full_mode_07777','nlink')) or blob!=expected['git_blob_sha1']:
        raise RuntimeError('original body pin mismatch: '+str(p))
    external.append({**actual,'repository_path':expected['repository_path'],'git_blob_sha1':blob,'source_role':'external authenticated original-head body; reviewed content scope in REPORT.md'})

captures=[]
for p in sorted((BASE/'captures').glob('*/CAPTURE.json')):
    c=json.loads(p.read_text())
    for key in ('prelaunch','stdout','stderr'):
        current=pin(Path(c[key]['path']))
        if any(current[k]!=c[key][k] for k in ('bytes','sha256','full_mode_07777','nlink')):
            raise RuntimeError('capture pin mismatch: '+key)
    if not all(c['inputs_unchanged']):
        raise RuntimeError('input changed during capture')
    captures.append({'capture':pin(p),'actual_controller_pid':c['actual_controller_pid'],'actual_child_pid':c['actual_child_pid'],'started_utc':c['started_utc'],'ended_utc':c['ended_utc'],'exit_code':c['exit_code']})

sub=(BASE/'captures/submitted_default/stdout.bin').read_bytes()
if sub!=(BASE.parent/'original_preparation_family/original/verification.json').read_bytes():
    raise RuntimeError('submitted output does not reproduce original')
ind=json.loads((BASE/'captures/independent_default/stdout.bin').read_text())
if ind['total_checks']!=3273:
    raise RuntimeError('unexpected independent count')

items=[];directories=[]
for p in [BASE]+sorted(BASE.rglob('*')):
    s=p.lstat()
    if stat.S_ISDIR(s.st_mode):
        directories.append({'path':str(p),'relative_path':str(p.relative_to(BASE)),'full_mode_07777':format(s.st_mode&0o7777,'04o')})
    elif p.name!='SOURCE.json':
        items.append({**pin(p),'relative_path':str(p.relative_to(BASE))})
result={
 'schema':'pr62-geometry-priority-source-only/v1',
 'prepared_utc':datetime.now(timezone.utc).isoformat(),
 'actual_preparer_pid':os.getpid(),
 'family':'ribbon_knot_geometry_adversary_family',
 'root':str(BASE),
 'ROOT_custody_or_scientific_approval':False,
 'publication_or_remote_authorization':False,
 'original_api_retrieval_claimed_by_this_family':False,
 'original_authentication_index':pin(AUTH),
 'external_original_body_pins':external,
 'actual_captures':captures,
 'files':items,
 'directories':directories,
 'scope_note':'All current meaningful family files and exact directory topology. SOURCE.json excludes itself to avoid recursive hashing. Read-only external bodies are pinned but not copied; body pin checking does not assert all historical review content was read. No READY or ROOT closure is produced by this SOURCE-only family.'
}
out=BASE/'SOURCE.json'
with out.open('x') as f:f.write(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'SOURCE':pin(out),'actual_preparer_pid':os.getpid(),'files':len(items),'directories':len(directories),'external_original_bodies_checked':len(external),'captures_checked':len(captures),'ROOT_approval':False},indent=2,sort_keys=True))
