"""Final first-party preparation freeze only. Does not execute either ROOT closure helper."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

F=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def identity(q):
    p=Path(q['path']);b=p.read_bytes()
    assert p.is_relative_to(F) and len(b)==q['bytes'] and hashlib.sha256(b).hexdigest()==q['sha256']


def main():
    begin=datetime.datetime.now(datetime.timezone.utc).isoformat()
    assert F.name=='original_preparation_family' and F.parent.name=='pr51_30000166'
    for name in ('FIXED_PAYLOAD_INDEX.json','READY.md','SELF_MANIFEST.json'):assert not (F/name).exists()
    cap=F/'captures/final_preparation_checks'
    pre=json.loads((cap/'PRELAUNCH.json').read_text());started=json.loads((cap/'STARTED.json').read_text());done=json.loads((cap/'COMPLETE.json').read_text())
    assert pre['schema']=='pr51-private-command-prelaunch/v1'
    assert started['schema']=='pr51-private-command-started/v1' and done['schema']=='pr51-private-command-completed/v1'
    assert done['child_pid']==started['child_pid']==14482 and done['completed'] is True and done['exit_code']==0
    assert pre['child_pid'] is None and pre['completed'] is False
    assert pre['argv']==started['argv']==done['argv'] and pre['cwd']==started['cwd']==done['cwd']
    times=[datetime.datetime.fromisoformat(q['utc']) for q in (pre,started,done)]
    assert times==sorted(times) and all(q.tzinfo is not None for q in times)
    identity(pre['operator'])
    for q in pre['sources']:
        identity(q['saved']);assert q['original']['sha256']==q['saved']['sha256'] and q['original']['bytes']==q['saved']['bytes']
    for k in ('prelaunch','started','stdout','stderr'):identity(done[k])
    assert done['stdout']['bytes']==6414 and done['stderr']['bytes']==0
    report=json.loads((cap/'STDOUT.bin').read_text())
    assert report['checks_actual']==1800 and report['status']=='PASS_PREPARATION_EVIDENCE_ONLY'
    assert report['completed_capture_count']==22 and report['future_authority'] is False
    log=F/'RESEARCH_LOG.md'
    with log.open('a') as t:
        t.write('\n'+begin+' — 100% preparation handoff estimate: final check child completion read back separately, full split streams and chronology verified. Final fixed index/READY construction and 0444 freeze begin immediately; success is confirmed only by the actual final stdout after its inventory/body/mode checks. Mathematical acceptance, publication and ROOT closure remain pending; no future approval is supplied. This is a preparation estimate, not discovery progress.\n')
    files=[];dirs=['.']
    for p in sorted(F.rglob('*')):
        s=p.lstat();r=p.relative_to(F).as_posix()
        assert not stat.S_ISLNK(s.st_mode),r
        if stat.S_ISDIR(s.st_mode):dirs.append(r)
        else:
            assert stat.S_ISREG(s.st_mode) and s.st_nlink==1,r
            files.append({'path':r,'bytes':s.st_size,'sha256':sha(p),'target_storage_mode':'0444'})
    index={'schema':'pr51-original-preparation-fixed-payload-index/v1',
           'utc':begin,'family_path':str(F),'original_head':'8006dd5f134ad0a2fa930e7278d3cb17945f4201',
           'files_count':len(files),'files':files,'directories':sorted(dirs),
           'designated_exclusions':['FIXED_PAYLOAD_INDEX.json','READY.md','SELF_MANIFEST.json'],
           'future_authority':False,'independent_mathematical_acceptance':None}
    p=F/'FIXED_PAYLOAD_INDEX.json'
    with p.open('x') as t:t.write(json.dumps(index,indent=2)+'\n')
    pins={k:sha(F/k) for k in ('REPORT.md','PRIMARY_SCOPE_CHECK.md','PREPARATION_STATUS.json','close_family.py','verify_closed_family.py','FIXED_PAYLOAD_INDEX.json')}
    ready='''# PR51 original preparation READY

Preparation is complete and files are frozen for ROOT after this preparer exits. Independent mathematical acceptance is pending. No closer or readback has run; no future ROOT result, native authority or publication approval is supplied.

Family: `{family}`

Original head: `8006dd5f134ad0a2fa930e7278d3cb17945f4201`. Fifteen literal science files, 53,495 bytes, eight JSON documents, original Git modes 100644. Full 16-path diff SHA256: `cd347fdfcf118cf10d59151d3a5c75e14edfab10add0ef2e93ef8525271aa951`.

Actual unchanged helper outputs match all bytes and recursive JSON keys/types/values: author 2,837 assertions, historical checker 35,980. The latter is a replay, not a fresh independent family. Actual final preparation check child 14482 exited 0 with 1,800 evidence checks. Its own completed capture was separately verified after exit. Twenty-three completed capture chains are retained, including missing-local-object exit 128; one earlier failed launch has only genuine prelaunch evidence, and one shell failure never launched a capture. Both are explicitly qualified.

Native observations remain historical: target queued 0/5, duplicate queue row absent; both selected catalog payloads match the original records, prior_report keys absent, SQL report literal text{{}} rather than NULL. Original ledger has one object, two events, zero proof attempts, budget 5 and no separate source-response count. New and audit proof attempts remain zero. No PDF download/hash/pixels or full imported proof certificate is claimed.

Fixed payload index binds {count} bodies; index and READY add two designated bodies. ROOT's self-only manifest will exclude only itself. Expected relative directory count including the family root: {dirs}. All retained files are 0444; no foreign raw paper/cache/header/full SQL ledger is retained.

ROOT must run the unexecuted SOURCE-only closer after receiving this preparer's completed/exit notification, capture actual child launch/completion outside this family, then run the separate unexecuted read-only verifier only after the closer child exits. Both require the exact index and READY SHA256 pins. The READY SHA256 and full literal argv are supplied in the handoff after this file exists; no circular self-hash is invented here. The verifier can additionally bind the actual manifest SHA256 after closure. Neither helper authorizes production/native/Git/remote changes or supplies a mathematical verdict.

Body SHA256 pins:

'''.format(family=F,count=len(files),dirs=len(dirs))
    ready+='\n'.join('- `'+k+'`: `'+v+'`' for k,v in pins.items())+'\n'
    with (F/'READY.md').open('x') as t:t.write(ready)
    for p in F.rglob('*'):
        if p.is_file():p.chmod(0o444)
    expected=sorted([q['path'] for q in files]+['FIXED_PAYLOAD_INDEX.json','READY.md'])
    actual=sorted(p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file())
    assert actual==expected
    for q in files:
        p=F/q['path'];assert p.stat().st_size==q['bytes'] and sha(p)==q['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
    assert all(stat.S_IMODE((F/r).stat().st_mode)==0o444 for r in actual)
    assert not (F/'SELF_MANIFEST.json').exists()
    pins['READY.md']=sha(F/'READY.md')
    print(json.dumps({'schema':'pr51-final-freeze-actual-result/v1','actual_pid':os.getpid(),
          'utc_begin':begin,'utc_complete':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'source_sha256':sha(Path(__file__)),'files_frozen_actual':len(actual),
          'directories_actual':len(dirs),'completed_captures_actual':23,
          'ready':True,'root_closure_performed':False,'pins':pins},indent=2))


if __name__=='__main__':main()
