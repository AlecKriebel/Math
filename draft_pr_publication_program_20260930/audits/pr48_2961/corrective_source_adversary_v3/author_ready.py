"""Own readiness authorship only; never invokes proposed closers or production."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,stat
F=Path(__file__).absolute().parent
def ref(n):
    q=F/n;b=q.read_bytes();return dict(path=n,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
assert not (F/'READY.json').exists() and not (F/'SELF_MANIFEST.json').exists()
names=sorted(q.relative_to(F).as_posix() for q in F.rglob('*') if q.is_file());dirs=sorted(['.']+[q.relative_to(F).as_posix() for q in F.rglob('*') if q.is_dir()])
assert all(not q.is_symlink() and (q.is_file() or q.is_dir()) for q in F.rglob('*'))
assert all(stat.S_IMODE((F/n).stat().st_mode)==0o644 for n in names)
assert all(stat.S_IMODE((F/d).stat().st_mode)==0o755 for d in dirs)
assert set(dirs)=={'.'}|{a.as_posix() for n in names for a in PurePosixPath(n).parents}
v=json.loads((F/'VERDICT.json').read_bytes());assert v['status']=='REPAIR_REQUIRED_SOURCE' and [z['id'] for z in v['mandatory_findings']]==['M3']
capture=json.loads((F/'private_actual_capture_v2/CAPTURE.json').read_bytes());assert capture['status']=='PASS' and capture['pid']==92858
for z in json.loads((F/'FIXED_INPUT_BINDINGS.json').read_bytes())['fixed_rows']:
    q=Path('/Users/alec/Documents/Math')/z['path'];b=q.read_bytes();assert len(b)==z['bytes'] and hashlib.sha256(b).hexdigest()==z['sha256'] and stat.S_IMODE(q.stat().st_mode)==z['full_mode']
ready=dict(schema='pr48-corrective-v3-adverse-readiness/v1',utc=dt.datetime.now(dt.timezone.utc).isoformat(),status='READY_FOR_ROOT_ADVERSE_EVIDENCE_READING_AND_CLOSURE_ONLY',source_only=True,production_executed=False,future_acceptance_approved=False,candidate_source_ready_sha256=v['source_ready_sha256'],candidate_SOURCE_manifest_at_review=None,candidate_closure_required=False,qualification='Bound rejected V3 and preceding V2 remain unclosed full0644; this freezes adverse review evidence only. Same reviewer corrective continuity, no independent blind math claim.',closure_payload_files=sorted(names+['READY.json']),closure_directory_names=dirs,fixed_own_files=[ref(n) for n in names],ROOT_closer_argv=['/usr/bin/python3','-B',str(F/'close_adverse_family.py'),'--execute','--personally-read-complete-source','--ready-sha256','ACTUAL_READY_SHA'],ROOT_reader_argv=['/usr/bin/python3','-B',str(F/'verify_closed_adverse_family.py'),'--self-manifest-sha256','ACTUAL_ROOT_CLOSED_SELF_SHA'],own_closer_and_reader_executed=False,no_self_manifest_authored=True,mandatory_findings=['M3'],source_review_completion_percent=100,actual_recovery_percent=0,mathematical_credit=0,actual_private_capture=ref('private_actual_capture_v2/CAPTURE.json'),original_failed_prelaunch=ref('PRIVATE_PREPARATION_FAILURE.json'))
with (F/'READY.json').open('xb') as f:f.write((json.dumps(ready,indent=2,allow_nan=False)+'\n').encode())
print(json.dumps(dict(status=ready['status'],actual_author_pid=os.getpid(),utc=ready['utc'],payload_count=len(ready['closure_payload_files']),relative_directories=len(dirs)-1,READY=ref('READY.json'),REPORT=ref('REPORT.md'),VERDICT=ref('VERDICT.json'),closer=ref('close_adverse_family.py'),reader=ref('verify_closed_adverse_family.py'),common=ref('closure_common.py'),actual_capture=ref('private_actual_capture_v2/CAPTURE.json')),indent=2))
