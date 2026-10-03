"""Actual final source-only review read; never call own closer or production/helper."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat
F=Path(__file__).absolute().parent;R=Path('/Users/alec/Documents/Math');S=F.parent/'current_preparation_family'
def need(x,n):
    if not x:raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'regular nonsymlink');return p.read_bytes()
def bind(p):
    b=raw(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def main():
    need(not (F/'MANIFEST.json').exists(),'own closure absent, ROOT only');need(not (F.parent/'reviewed_candidate').exists(),'candidate absent');v=json.loads(raw(F/'VERDICT.json'));need(v['mandatory_corrections']==[] and v['closure_state']=='READY_WAIT_ROOT_NOT_CLOSED' and v['future_acceptance_approved'] is False and v['report']['sha256']==sha(raw(F/'REPORT.md')),'bounded complete verdict/report')
    fixed=json.loads(raw(F/'FIXED_READ_RESULT.json'))
    for r in fixed['checked_body_mode_rows']:
        p=R/r['path'];need(bind(p)==r,'complete external fixed unchanged')
    expected={'FIXED_INPUT_INSPECTION_ACTUAL_CAPTURE':1,'FIXED_INPUT_INSPECTION_V2_ACTUAL_CAPTURE':0,'PRIVATE_GUARD_CONTROLS_ACTUAL_CAPTURE':1,'PRIVATE_GUARD_CONTROLS_V2_ACTUAL_CAPTURE':1,'PRIVATE_GUARD_CONTROLS_V3_ACTUAL_CAPTURE':1,'PRIVATE_GUARD_CONTROLS_V4_ACTUAL_CAPTURE':0,'SCOPE_AND_LIMITS_ACTUAL_CAPTURE':0};captures=[]
    for n,exitcode in sorted(expected.items()):
        p=F/n;c=json.loads(raw(p/'CAPTURE.json'));pre=json.loads(raw(p/'PRELAUNCH.json'));need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==exitcode and c['operator_unchanged'] is True and c['target_unchanged'] is True,'real retained actual outcome');need(pre['actual_execution'] is False and pre['completed'] is False and pre['pid'] is None and pre['exit_code'] is None,'genuine prelaunch');need(sha(raw(p/'prelaunch_operator.py'))==c['operator_sha256'] and sha(raw(p/'prelaunch_target.py'))==c['target_source']['sha256']==sha(raw(Path(c['target_source']['path']))),'unchanged prelaunch sources')
        for k in ('stdout','stderr'):r=c[k];b=raw(p/r['path']);need(type(r['bytes']) is int and len(b)==r['bytes'] and sha(b)==r['sha256'],'full actual split streams')
        captures.append(dict(capture=bind(p/'CAPTURE.json'),actual_pid=c['pid'],exit_code=exitcode))
    names=['REPORT.md','VERDICT.json','close_current_source_adversary.py','verify_current_source_adversary_readonly.py','capture_actual_command.py'];source_rows=[bind(F/n) for n in names]
    # Full TEXT reads and exact ROOT entrypoint arguments, never import or compile them.
    closer=raw(F/'close_current_source_adversary.py').decode();verifier=raw(F/'verify_current_source_adversary_readonly.py').decode();need('pr49-current-source-adversary-self-only-closure/v1' in closer and 'files_count=len(members)' in closer and 'files=members' in closer and 'self_excluded=[SELF]' in closer and '--expected-report-sha256' in closer and '--expected-manifest-sha256' in verifier and 'FINAL_REVIEW_READ_ACTUAL_CAPTURE' in closer,'actual required closure interface')
    need(sha(raw(S/'PREPARATION_MANIFEST.json'))==v['source_manifest']['sha256'] and sha(raw(S/'prepare_current_packet.py'))==v['builder']['sha256'] and sha(raw(S/'capture_root_builder_operation.py'))==v['operator']['sha256'],'reviewed production bodies unchanged; text-only')
    result=dict(schema='pr49-current-source-adversary-final-source-read/v1',status='PASS_FINAL_SOURCE_ONLY_REVIEW_READ',actual_pid=os.getpid(),created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),external_fixed_body_mode_rows_reread=len(fixed['checked_body_mode_rows']),complete_retained_actual_captures=captures,full_report_verdict_closer_verifier_operator_bindings=source_rows,production_imported_compiled_executed=False,own_closer_or_verifier_executed=False,helpers_executed=False,own_closure_absent=True,reviewed_candidate_absent=True,future_acceptance_approved=False,new_whole_current_review_gate='PENDING')
    with (F/'FINAL_SOURCE_READ_RESULT.json').open('xb') as h:h.write((json.dumps(result,indent=2,allow_nan=False)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('complete_retained_actual_captures','full_report_verdict_closer_verifier_operator_bindings')},sort_keys=True))
if __name__=='__main__':main()
