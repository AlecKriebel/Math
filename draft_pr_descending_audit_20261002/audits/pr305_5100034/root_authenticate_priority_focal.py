"""Authenticate a closed read-only focal-priority corpus and its native history."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
A=Path(__file__).resolve().parent;D=A/'priority_focal_20261004'
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
    assert p.is_file() and not p.is_symlink(),p
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b),'mode':oct(stat.S_IMODE(p.stat().st_mode))}
seal=D/'FINAL_SEAL.json'
assert pin(seal)['sha256']=='843f846574bf433ad64d6178490d69c0d2ab055556a3750a6f2484ff1c12c92e'
j=json.loads(seal.read_bytes());expected={}
for e in j['files']:
    p=Path(e['path']);assert not p.is_absolute() and '..' not in p.parts and str(p) not in expected
    assert pin(D/p)=={k:e[k] for k in ['bytes','sha256','mode']},p
    assert e['mode']=='0o444';expected[str(p)]=e
assert {str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()}==set(expected)|{'FINAL_SEAL.json'}
assert all(not p.is_symlink() for p in D.rglob('*'))
directories={'.':oct(stat.S_IMODE(D.stat().st_mode))}
directories.update({str(p.relative_to(D)):oct(stat.S_IMODE(p.stat().st_mode)) for p in D.rglob('*') if p.is_dir()})
assert all(v=='0o555' for v in directories.values()) and pin(seal)['mode']=='0o444'
c=json.loads((D/'SOURCE_CUSTODY.json').read_bytes())
assert c['criteria_freeze']['before_reading'] and c['criteria_freeze']['sha256']=='0d336c3309131121bad29cb2ed05238da2b59e3dceb23e5b49d027cd39927d90'
assert pin(D/'FROZEN_ACCEPTANCE_CRITERIA.md')['sha256']==c['criteria_freeze']['sha256']
assert len(c['sources'])==23 and len(c['all_private_evidence_files'])==65
for e in c['all_private_evidence_files']:
    assert {k:pin(D/e['path'])[k] for k in ['bytes','sha256']}=={k:e[k] for k in ['bytes','sha256']}
records=[];bindings=0;archived=[];failed=[]
for p in sorted((D/'receipts').glob('*.json')):
    r=json.loads(p.read_bytes());assert r['cwd']==str(D)
    assert datetime.fromisoformat(r['UTC_start'])<=datetime.fromisoformat(r['UTC_finish'])
    for k in ['stdout','stderr']:
        q=Path(r[k+'_file']);assert q.is_relative_to(D) and pin(q)['sha256']==r[k+'_sha256']
    for e in r['artifacts']:
        bindings+=1;q=Path(e['path']);assert q.is_relative_to(D)
        if {k:pin(q)[k] for k in ['bytes','sha256']}!={k:e[k] for k in ['bytes','sha256']}:
            assert p.name=='classical_boundary_control.json' and q.name=='classical_boundary_control.py'
            q=D/'classical_boundary_control_initial.py'
            assert {k:pin(q)[k] for k in ['bytes','sha256']}=={k:e[k] for k in ['bytes','sha256']}
            archived.append({'receipt':p.name,'retained_initial_program':q.name})
    if r['exit_code']:
        failed.append({'receipt':p.name,'exit_code':r['exit_code'],'argv':r['native_argv'],
                       'stderr':Path(r['stderr_file']).read_text(errors='replace')})
    records.append(r)
closure=json.loads((D/'CLOSURE.json').read_bytes())
assert closure['bounded_audit_completed'] and closure['no_more_writes_after_final_seal_is_written']
assert not closure['authorization_to_merge_or_publish']
assert pin(D/'FOCAL_PRIORITY_COMPARISON.md')['sha256']=='d52b3846f8fe89f1c217fd7431aa77cf813ca9dc875457d964bc34d51c300823'
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_CLOSED_FOCAL_PRIORITY_CORPUS_CUSTODY',
     'payload_files':len(expected),'seal':pin(seal),'directory_modes':directories,
     'source_entries':23,'private_evidence_files':65,'native_receipts':len(records),'artifact_bindings':bindings,
     'archived_historical_program_resolution':archived,'retained_failed_operations':failed,
     'all_bytes_full_streams_and_final_modes_authenticated':True,
     'failed_acquisitions_qualification':'Authenticates history, including explicitly disclosed unavailable editions and historical initial verifier failure; does not assert all acquisitions succeeded.',
     'root_full_reports_read':['FOCAL_PRIORITY_COMPARISON.md','SEARCH_TRAIL.md','FINAL_SELF_CHECK.md'],
     'integrated_priority_adjudication':False,'publishing_clearance':False}
(A/'ROOT_PRIORITY_FOCAL_CUSTODY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
