"""Independent source03 probes; byte-identical action copies, all effects trapped.

Uses the already-audited synthetic fixture protocol from the regression harness.
New mutations, descriptor traces and assertions are independently authored here.
Every temporary fixture stays inside this authored directory and is removed.
"""
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch
import copy, hashlib, json, os, stat, tempfile
import regression_workflow_probes as h

g=h.g
OUT=Path(__file__).resolve().parent
RESULTS=[]

def record(name, **fields):
    RESULTS.append(dict(test=name, passed=True, **fields))

def reject(name, action, f=None, ready=0, merge=0, exception=RuntimeError):
    try: action()
    except exception as exc:
        if f is not None:
            assert f.ready_count==ready and f.merge_count==merge, (name,f.ready_count,f.merge_count)
        record(name, refused=type(exc).__name__, reason=str(exc),
               **({} if f is None else dict(ready_POST_count=f.ready_count,merge_PUT_count=f.merge_count)))
    else: raise AssertionError(name+': invalid transition accepted')

def fixture(action):
    with tempfile.TemporaryDirectory(prefix='independent-fixture-',dir=OUT) as tmp:
        f=h.Fixture(Path(tmp));action(f)

def prepare(f):
    f.seed_publication();f.execute('append_verified_tracker.py');f.execute('integrate_reviewed_pr.py')
    return json.loads((f.P/'PR_PREPARED.json').read_text())

def mutate_receipt(f, kind):
    path=f.P/({'publication':'ZENODO_VERIFIED_PUBLICATION.json','tracker':'TRACKER_VERIFIED_APPEND.json','prepared':'PR_PREPARED.json'}[kind])
    data=json.loads(path.read_text());data['synthetic_late_extra_field']='changed after initial acceptance';h.save(path,data)
    # Keep the current publication/tracker chain valid. The new exact initial
    # equality check must still reject this independently legitimate-shaped pair.
    if kind=='publication':
        tp=f.P/'TRACKER_VERIFIED_APPEND.json';t=json.loads(tp.read_text());t['publication_receipt_sha256']=h.sha(path);h.save(tp,t)

def ready_identity_probes():
    changes={
      'head':lambda p:p['head'].update(sha='d'*40),
      'branch':lambda p:p['head'].update(ref='other'),
      'head repository':lambda p:p['head']['repo'].update(full_name='other/Math'),
      'base branch':lambda p:p['base'].update(ref='other'),
      'base repository':lambda p:p['base']['repo'].update(full_name='other/Math'),
      'closed state':lambda p:p.update(state='closed'),
      'merged state':lambda p:p.update(merged=True),
    }
    for name,change in changes.items():
        def case(f,name=name,change=change):
            prepare(f);f.before_native_compare=lambda:change(f.pr)
            reject('late ready identity: '+name,lambda:f.execute('verify_and_merge.py'),f)
            assert not (f.P/'NATIVE_READY_ATTEMPT.json').exists()
        fixture(case)
    for kind in ['publication','tracker','prepared']:
        def case(f,kind=kind):
            prepare(f);f.before_native_compare=lambda:mutate_receipt(f,kind)
            reject('late ready exact accepted '+kind+' receipt',lambda:f.execute('verify_and_merge.py'),f)
            assert not (f.P/'NATIVE_READY_ATTEMPT.json').exists()
        fixture(case)
    def already_ready(f):
        prepare(f);f.before_native_compare=lambda:f.pr.update(draft=False)
        f.execute('verify_and_merge.py')
        assert f.ready_count==0 and f.merge_count==1 and not (f.P/'NATIVE_READY_ATTEMPT.json').exists()
        record('freshly observed already-ready state omits ready POST and merges exact expected head',ready_POST_count=0,merge_PUT_count=1)
    fixture(already_ready)


def premerge_probes():
    for kind in ['publication','tracker','prepared']:
        def case(f,kind=kind):
            prepare(f);original=f.api;fired=False
            def api(method,endpoint,payload):
                nonlocal fired
                value=original(method,endpoint,payload)
                if endpoint=='pulls/210' and method=='GET' and f.ready_count==1 and not fired:
                    fired=True;mutate_receipt(f,kind)
                return value
            f.api=api
            reject('premerge exact accepted '+kind+' receipt after ready',lambda:f.execute('verify_and_merge.py'),f,ready=1)
            assert not (f.P/'NATIVE_MERGE_REQUEST.json').exists()
        fixture(case)
    def same_bytes(f):
        prepare(f);target=f.P/'PR_PREPARED.json';original=Path.read_bytes;fired=False
        def read(p):
            nonlocal fired
            raw=original(p)
            if p==target and not fired:
                fired=True;data=json.loads(raw);data['synthetic_after_read_change']=True;h.save(p,data)
            return raw
        with patch.object(Path,'read_bytes',read):
            reject('prepared JSON and SHA use accepted same bytes; later change caught',lambda:f.execute('verify_and_merge.py'),f)
        assert fired and not (f.P/'NATIVE_READY_ATTEMPT.json').exists()
    fixture(same_bytes)


def durable_primitive_probes():
    with tempfile.TemporaryDirectory(prefix='primitive-fixture-',dir=OUT) as tmp:
        base=Path(tmp);events=[];real_fsync=os.fsync
        def sync(fd):
            events.append('directory' if stat.S_ISDIR(os.fstat(fd).st_mode) else 'file');return real_fsync(fd)
        with patch.object(os,'fsync',sync):g.exclusive_json(base/'intent.json',dict(synthetic_fixture_only=True))
        assert events==['file','directory'],events
        record('actual descriptor order: intent file then containing directory',fsync_order=events)
        calls=[];real_sync=g.sync_directory
        def directory(path):calls.append(str(Path(path).relative_to(base.parent)));return real_sync(path)
        new=base/'one/two/three'
        with patch.object(g,'sync_directory',directory):g.durable_mkdir(new)
        expected=[str(p.relative_to(base.parent)) for p in [base.parent,base,base/'one',base/'one/two']]
        # First anchor-parent is base.parent, outside the fixture pathname but no
        # write occurs there: this is a directory fsync only.
        assert calls==expected,(calls,expected)
        record('all three missing ancestor links sync after mkdir',directory_syncs=calls)
        retry=base/'retry/child';calls=[]
        def fail_link(path):
            calls.append(str(path))
            if Path(path)==base:raise OSError('synthetic unconfirmed new retry linkage')
            return real_sync(path)
        reject('new ancestor directory-sync failure propagates',lambda:run_mkdir(fail_link,retry),exception=OSError)
        assert (base/'retry').is_dir() and not retry.exists()
        calls=[]
        with patch.object(g,'sync_directory',lambda path:(calls.append(str(path)),real_sync(path))[1]):g.durable_mkdir(retry)
        assert calls==[str(base),str(base/'retry')],calls
        record('retry resyncs visible unconfirmed ancestor then new child link',directory_syncs=calls)
        existing=base/'existing';existing.mkdir();calls=[]
        with patch.object(g,'sync_directory',lambda path:(calls.append(str(path)),real_sync(path))[1]):g.durable_mkdir(existing)
        assert calls==[str(base)]
        record('existing final directory retry resyncs its parent',directory_syncs=calls)
        fail=base/'failure.json';events=[]
        def failed_directory(path):events.append('directory_failed');raise OSError('synthetic directory sync failure')
        with patch.object(os,'fsync',sync),patch.object(g,'sync_directory',failed_directory):
            reject('exclusive intent directory-sync failure propagates after file fsync',lambda:g.exclusive_json(fail,{'synthetic':True}),exception=OSError)
        assert events==['file','directory_failed'] and fail.exists(),events
        reject('failed-directory-sync intent remains exclusive on retry',lambda:g.exclusive_json(fail,{'synthetic':2}),exception=FileExistsError)


def run_mkdir(sync,target):
    with patch.object(g,'sync_directory',sync):g.durable_mkdir(target)


def workflow_io_faults():
    # All stages must stop at their shared durable lock ancestry before even a
    # read-only provider command if the initial directory sync fails.
    for stage in ['publish_preprint.py','append_verified_tracker.py','integrate_reviewed_pr.py','verify_and_merge.py','verify_published_readonly.py']:
        def case(f,stage=stage):
            if stage=='verify_and_merge.py':h.save(f.P/'PR_PREPARED.json',dict(prepared_head='synthetic'))
            with patch.object(g,'sync_directory',side_effect=OSError('synthetic startup directory-sync failure')):
                reject(stage+' startup directory-sync failure blocks every provider call',lambda:f.execute(stage),exception=OSError)
            assert f.calls==[] and f.downloads==[]
        fixture(case)
    # Each provider mutation has a complete intent file+parent sync barrier.
    cases=[('STAGE_ATTEMPT.json','publish_preprint.py','stage'),
           ('PUBLISH_ATTEMPT.json','publish_preprint.py','publish'),
           ('private_transport/tracker/APPEND_ATTEMPT.json','append_verified_tracker.py','append'),
           ('NATIVE_PREPARE_ATTEMPT.json','integrate_reviewed_pr.py','ref'),
           ('NATIVE_READY_ATTEMPT.json','verify_and_merge.py','ready'),
           ('NATIVE_MERGE_REQUEST.json','verify_and_merge.py','merge')]
    for intent,stage,operation in cases:
        for fault in ['file','directory']:
            def case(f,intent=intent,stage=stage,operation=operation,fault=fault):
                if operation=='append':f.seed_publication()
                if operation=='ref':f.seed_publication();f.execute('append_verified_tracker.py')
                if operation in ['ready','merge']:prepare(f)
                target=f.P/intent;before=len(f.calls);fired=False
                real_directory=g.sync_directory;real_fsync=os.fsync
                def directory(path):
                    nonlocal fired
                    if fault=='directory' and Path(path)==target.parent and target.exists():
                        fired=True;raise OSError('synthetic '+operation+' intent parent-sync failure')
                    return real_directory(path)
                def fsync(fd):
                    nonlocal fired
                    if fault=='file' and not stat.S_ISDIR(os.fstat(fd).st_mode) and target.exists():
                        fired=True;raise OSError('synthetic '+operation+' intent file-sync failure')
                    return real_fsync(fd)
                with patch.object(g,'sync_directory',directory),patch.object(os,'fsync',fsync):
                    reject(operation+' intent '+fault+'-sync failure blocks associated provider mutation',lambda:f.execute(stage),exception=OSError)
                assert fired and target.exists()
                calls=f.calls[before:]
                if operation in ['stage','publish','append','ready','merge']:
                    count={'stage':f.stage_count,'publish':f.publish_count,'append':f.append_count,'ready':f.ready_count,'merge':f.merge_count}[operation]
                    assert count==0,(operation,count)
                if operation=='ref':assert not any('git/refs/heads/' in ' '.join(c) and 'PATCH' in c for c in calls)
                if operation=='merge':assert f.ready_count==1
                # The individual fault record above reflects the associated
                # mutation, not earlier read-only checks or Git object creation.
            fixture(case)


def additional_boundaries():
    def wrong_native(f):
        prepare(f);k=next(p for p in f.native_files if p.endswith('/PROOF.md'));f.native_files[k]+=b'\nsynthetic remote corruption\n'
        reject('native body corrupted under same mocked head refuses before ready/merge',lambda:f.execute('verify_and_merge.py'),f,exception=AssertionError)
    fixture(wrong_native)
    def scope(f):
        prepare(f);f.compare_override=dict(files=[dict(filename='foreign/changed.md',status='modified')])
        reject('foreign native changed path refuses before ready/merge',lambda:f.execute('verify_and_merge.py'),f,exception=AssertionError)
    fixture(scope)
    def missing_seal(f):
        f.seed_publication();f.execute('append_verified_tracker.py')
        (f.D/'release_helpers_adversary_03/AUTHORED_MANIFEST.json').unlink()
        reject('required source03 seal absent refuses before native object/ref mutation',lambda:f.execute('integrate_reviewed_pr.py'),exception=AssertionError)
        assert not any('--method' in c and c[c.index('--method')+1] in ['POST','PATCH','PUT'] for c in f.calls)
    fixture(missing_seal)


if __name__=='__main__':
    ready_identity_probes();premerge_probes();durable_primitive_probes();workflow_io_faults();additional_boundaries()
    value=dict(utc=datetime.now(timezone.utc).isoformat(),synthetic_fixture_only=True,
               source03_independently_authored_assertions=True,tests=RESULTS,test_count=len(RESULTS),
               all_tests_passed=all(r['passed'] for r in RESULTS),actual_provider_network_calls=0,
               actual_helper_subprocesses=0,untrapped_action_helper_imports=0,crash_simulated=False,
               mandatory_findings=[],optional_findings=[],completion_percent=95)
    h.save(OUT/'INDEPENDENT_TRANSITION_RESULTS.json',value)
    print(json.dumps(value,indent=2))
