"""Proposed self-only closer; must be invoked by ROOT in an external actual capture."""
from review_common import *
from datetime import datetime,timezone
import argparse
p=argparse.ArgumentParser();p.add_argument('--expected-report-sha256',required=True);args=p.parse_args()
assert ref(F/'REPORT.md')['sha256']==args.expected_report_sha256
assert not (F/'SELF_MANIFEST.json').exists(),'No replacement or repeat closure'
q=inspect_complete()
ready=load(F/'FINAL_READY_READ_RESULT_V2.json');assert ready['status']=='PASS_READY_WAIT_ROOT' and ready['own_closure_executed'] is False
rc=load(F/'FINAL_READY_READ_V2_ACTUAL_CAPTURE/CAPTURE.json');assert rc['exit_code']==0 and rc['completed'] is True and rc['pid']==ready['actual_pid']
for k in ['stdout','stderr']:body(R/rc[k]['path'],rc[k],False)
assert json.loads((F/'FINAL_READY_READ_V2_ACTUAL_CAPTURE/stdout.bin').read_bytes())['status']=='PASS_READY_WAIT_ROOT'
assert rc['source_unchanged'] is True and rc['operator_unchanged'] is True
body(F/'FINAL_READY_READ_V2_ACTUAL_CAPTURE/PRELAUNCH_SOURCE.py',rc['source'],False)
assert (F/'FINAL_READY_READ_V2_ACTUAL_CAPTURE/PRELAUNCH_COMMON.py').read_bytes()==(F/'review_common.py').read_bytes()
payload=q['owned_files'];assert 'SELF_MANIFEST.json' not in payload
# All checks complete before the first mutation. Only this family is ever chmodded.
for n in payload:(F/n).chmod(0o444)
rows=[]
for n in payload:
    w=ref(F/n);assert w['full_mode']==0o444;rows.append(dict(w,path=n))
_,dirs,dm=topology()
m=dict(schema='pr49-current-whole-adversary-self-only-closure/v2',created_utc=datetime.now(timezone.utc).isoformat(),actual_closing_pid=os.getpid(),self_excluded=1,files_count=len(rows),files=rows,directories=dirs,directory_full_modes=dm,manifest_full_mode=0o444,report_sha256=args.expected_report_sha256,candidate_manifest_sha256='8ca8820e1e1493391224ea8f93dde859bd9b3f6316c41763e86433dc85a1fa47',verdict='PASS_CREDITED_KNOWN_UNRESTRICTED_REFLECTION_CURRENT_PACKET_CUSTODY_REPAIRED',mandatory_corrections=[],external_body_mode_bindings=q['external_rows'],dated_native4=q['dated_native4'],retained_ROOT_failed_closure_fixed_members=q['retained_ROOT_failed_closure_fixed_members'],native4_is_dated_only=True,future_fresh13_ROOT_required=True,retained_actual_caps=q['captures'],future_acceptance_approved=False,ROOT_approval_created=False,production_execution=False,paper=False,DOI=False,tracker=False,external_postexit_ROOT_capture_and_separate_readback_required=True)
dest=F/'SELF_MANIFEST.json'
with dest.open('x') as f:f.write(json.dumps(m,indent=2)+'\n')
dest.chmod(0o444)
print(json.dumps(dict(status='PASS_ROOT_SELF_ONLY_WHOLE_CLOSURE',actual_closing_pid=os.getpid(),manifest_sha256=ref(dest)['sha256'],files_count=len(rows),directories_count=len(dirs),future_acceptance_approved=False)))
