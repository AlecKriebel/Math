"""Offline read-only full-body DIFF control; not a continuation execution."""
import sys, pathlib, types, json, time, resource, hashlib, os
D=pathlib.Path(__file__).parent;A=D.parent
old=A/'native_post_assess_carryforward_v2_20261006'
def module(n,p):
    m=types.ModuleType(n);m.__file__=str(p);sys.modules[n]=m;exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
a=module('readonly_diff_phase',old/'native_acceptance_actions_v3.py')
d=module('readonly_linear_diff',D/'linear_full_diff.py')
p=a.loads(a.read(A/'native_actual_input_preparation_20261006/root_fresh_native_preflight_20261006/EXECUTION_INPUTS.json'))
i=a.loads(a.read(A/'current_main_carryforward_input_20261006/CURRENT_INTEGRATION_INPUTS.json'))
cap=a.Capture(D/'controls'/('actual_diff_before_'+str(os.getpid())),whole_seconds=60)
before={}
for n,s in i['native_baseline'].items():
    if 'unsolved_math_prioritization/'+n in a.DERIVED:
        b=a.git(cap,p['runtime'],'show',i['main_parent']+':'+s['path']);a.need(a.pin(b)=={k:s[k] for k in ['bytes','sha256']},'Actual baseline full body');before[n]=b
W=old/'workspaces/candidate_d9eb646c1dd70e89'
# Source offer order is the immutable packet order, then native scope, then the
# seven generated members in the sealed continuation source order.
source_names=list(p['attempt_offer_sources'])
scoped_names=['assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','QUEUE.md']
generated=['IMPORT_BASELINE.json','HISTORICAL_DESK_ASSESSMENT.json','assessment.json','PUBLICATION_EVIDENCE.json','ACCEPTANCE_EVIDENCE.json','README.md','RESEARCH_LOG.md']
paths=source_names+['unsolved_math_prioritization/'+n for n in scoped_names]+[a.PREFIX+n for n in generated]
actual={str(x.relative_to(W/'offer')) for x in (W/'offer').rglob('*') if x.is_file()}
a.need(len(paths)==84 and len(set(paths))==84 and set(paths)==actual,'Exactly all84 stopped offers')
offers={n:a.read(W/'offer'/n,32*1024*1024) for n in paths}
begin=time.monotonic();u0=resource.getrusage(resource.RUSAGE_SELF);diff=d.full_diff(before,offers,a.PREFIX);u1=resource.getrusage(resource.RUSAGE_SELF)
elapsed=time.monotonic()-begin
r={'schema':'pr110-offline-actual84-linear-diff-control/v1','UTC':a.now(),'actual_control_PID':os.getpid(),'offline_pure_control':True,'actual_continuation_executed':False,'native_assess_calls':0,'live_export_executed':False,'helper_pin':{'path':str((D/'linear_full_diff.py').relative_to(A)),**a.pin(a.read(D/'linear_full_diff.py'))},'actual_stop_workspace':str(W),'before_pins':{n:a.pin(b) for n,b in before.items()},'offer_pins':{n:a.pin(b) for n,b in offers.items()},'all84_offers_included':True,'all_eight_globals_included':True,'DIFF_pin':a.pin(diff),'elapsed_monotonic_seconds':elapsed,'user_CPU_seconds':u1.ru_utime-u0.ru_utime,'system_CPU_seconds':u1.ru_stime-u0.ru_stime,'actual_readonly_Git_children':len(cap.records),'complete_readonly_Git_custody_folder':str(cap.root),'cap_bytes':1024*1024}
a.atomic(D/'controls/ACTUAL84_LINEAR_DIFF_CORRECTED.txt',diff);a.save(D/'ACTUAL84_LINEAR_DIFF_CONTROL.json',r)
print(json.dumps({k:r[k] for k in ['actual_control_PID','elapsed_monotonic_seconds','user_CPU_seconds','system_CPU_seconds','DIFF_pin','actual_readonly_Git_children']}))
