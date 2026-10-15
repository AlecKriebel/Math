"""Final private metadata freeze. ROOT-only closer/reader remain unexecuted SOURCE."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

F=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def bind(q):
    p=Path(q['path']);assert p.is_relative_to(F)
    assert p.stat().st_size==q['bytes'] and sha(p)==q['sha256']


def main():
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    assert F.name=='current_preparation_family'
    for r in ('SELF_MANIFEST.json','FIXED_PAYLOAD_INDEX.json','READY.md'):assert not (F/r).exists()
    cap=F/'captures/whole_readback'
    p=json.loads((cap/'PRELAUNCH.json').read_text());s=json.loads((cap/'STARTED.json').read_text());c=json.loads((cap/'COMPLETE.json').read_text())
    assert p['schema']=='pr51-current-private-command-prelaunch/v1' and c['schema']=='pr51-current-private-command-completed/v1'
    assert p['child_pid'] is None and c['completed'] is True and c['exit_code']==0 and c['child_pid']==s['child_pid']==72414
    assert p['argv']==s['argv']==c['argv'] and p['cwd']==s['cwd']==c['cwd']
    times=[datetime.datetime.fromisoformat(q['utc']) for q in (p,s,c)];assert times==sorted(times)
    bind(p['operator'])
    for q in p['sources']:bind(q['saved']);assert q['original']['sha256']==q['saved']['sha256']
    for k in ('prelaunch','started','stdout','stderr'):bind(c[k])
    assert c['stderr']['bytes']==0 and c['stdout']['bytes']==554
    result=json.loads((cap/'STDOUT.bin').read_text());assert result['checks_actual']==7444 and result['status']=='PASS_CURRENT_SCIENCE_SOURCE_ONLY'
    v=json.loads((F/'VERDICT.json').read_text());assert v['verdict']=='READY_CURRENT_SCIENCE_SOURCE_ONLY' and v['current_family_root_closure_performed'] is False
    with (F/'RESEARCH_LOG.md').open('a') as t:
        t.write('\n'+utc+' — 100% SOURCE preparation estimate: actual readback child has exited and its full capture has now been checked separately. Final fixed index/READY creation and 0444 freeze begin; only final actual stdout confirms success. ROOT closure, native acceptance and publication remain pending, with all authority false.\n')
    rows=[];dirs=['.']
    for p in sorted(F.rglob('*')):
        s=p.lstat();r=p.relative_to(F).as_posix();assert not stat.S_ISLNK(s.st_mode)
        if stat.S_ISDIR(s.st_mode):dirs.append(r)
        else:
            assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
            rows.append({'path':r,'bytes':s.st_size,'sha256':sha(p),'target_storage_mode':'0444'})
    index={'schema':'pr51-current-preparation-fixed-payload-index/v1','utc':utc,'family_path':str(F),
           'files_count':len(rows),'files':rows,'directories':sorted(dirs),'future_authority':False,
           'independent_mathematical_acceptance':None,'designated_exclusions':['FIXED_PAYLOAD_INDEX.json','READY.md','SELF_MANIFEST.json']}
    with (F/'FIXED_PAYLOAD_INDEX.json').open('x') as t:t.write(json.dumps(index,indent=2)+'\n')
    pins={r:sha(F/r) for r in ('REPORT.md','VERDICT.json','CURRENT_SCIENCE_INDEX.json','EXTERNAL_BINDINGS.json','current_science/SOURCE_STATUS.md','close_family.py','verify_closed_family.py','FIXED_PAYLOAD_INDEX.json')}
    ready='''# PR51 current SOURCE preparation READY

Publication-free partial candidate ready for ROOT after preparer exit. The mathematics is the full credited known all-N theorem; this disposition is SOURCE preparation, not a third independent mathematical verdict. All new native/ROOT acceptance/Git/merge/paper/DOI/tracker authority remains false.

Family: `{family}`

Science: 31 files (15 literal original archive, 16 operative), nine operative original bodies retained exactly. Original head `8006dd5f134ad0a2fa930e7278d3cb17945f4201`, eight original JSON documents, original Git mode100644. Global historical qualifications cover every old source/PASS/PDF/model/runtime/pending/readiness claim.

Actual text builder child70580 exit0:2498 preparation evidence checks. Separate actual readback child72414 exit0:7444 evidence checks. Both have complete private copied operator/source prelaunch, literal argv/cwd, actual PID/UTC and full split streams. The completed readback capture was separately checked after child exit. These are not mathematical discovery assertions.

The actual closed original188/eta23/geometry35 schemas and six actual ROOT closure/readback CAP4s are referenced by 273 full external body/mode/path rows, without administrative body copying. New review files are physically0444/directories0555; older0644 receipt fields are historical execution epochs. No future review closure/readback is invented.

Accounting remains original one-object ledger0/5, two source events with no separate response count, new0/audit0; prior_report key/file absent, historical selected SQL report text{{}} versus NULL. Duplicate30000167 shares scope/budget; absent native queue row not created. No native/canonical/Git index/ref/remote or sibling mutation occurred.

Fixed index binds {n} bodies; index and READY add two. Expected directory count including root: {d}. All physical files are0444. SELF_MANIFEST is absent. ROOT-only closer and separate read-only verifier remain unexecuted SOURCE. After this preparer exits, ROOT may inspect and capture an actual self-only closure outside this family, then separately read back only after closer child exit. Exact index/READY pins and full literal argv are supplied in the handoff after this READY exists; no circular self-hash or future manifest is invented.

SHA256 pins:

'''.format(family=F,n=len(rows),d=len(dirs))
    ready+='\n'.join('- `'+r+'`: `'+h+'`' for r,h in pins.items())+'\n'
    with (F/'READY.md').open('x') as t:t.write(ready)
    for p in F.rglob('*'):
        if p.is_file():p.chmod(0o444)
    actual=sorted(p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file())
    assert actual==sorted([q['path'] for q in rows]+['FIXED_PAYLOAD_INDEX.json','READY.md'])
    for q in rows:
        p=F/q['path'];assert p.stat().st_size==q['bytes'] and sha(p)==q['sha256']
    assert all(stat.S_IMODE((F/r).stat().st_mode)==0o444 for r in actual)
    assert not (F/'SELF_MANIFEST.json').exists();pins['READY.md']=sha(F/'READY.md')
    print(json.dumps({'schema':'pr51-current-final-freeze-actual-result/v1','actual_pid':os.getpid(),
        'started_utc':utc,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_sha256':sha(Path(__file__)),'files_frozen_actual':len(actual),'directories_actual':len(dirs),
        'science_files':31,'root_closure_performed':False,'pins':pins},indent=2))


if __name__=='__main__':main()
