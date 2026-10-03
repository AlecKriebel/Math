"""Recheck this family's completed records and individually excluded inputs."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat
D=Path(__file__).resolve().parent;A=D.parent;R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,label):
    if not ok:raise ValueError(label)
def read(p):
    need(p.is_file() and not p.is_symlink(),'Regular body '+str(p))
    for parent in p.parents:need(not parent.is_symlink(),'Symlink ancestor')
    return p.read_bytes()
def load(p):return json.loads(read(p))
result=load(D/'INPUT_READING_RESULT.json');rows=result['all_individual_inputs']
historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
external={}
for z in rows:
    name=z['path'];p=Path(name)
    need(p.is_absolute() and R in p.parents and D not in p.parents,'Outside family input')
    if p.relative_to(R).as_posix() in historical:
        matches=[g for g in result['historical_Git_captures'] if g['argv']==['git','show','c61dc0cb572de281b871264819c8b80d647d0373:'+p.relative_to(R).as_posix()]]
        need(len(matches)==1,'One genuine dated full Git body');raw=read(Path(matches[0]['stdout']['path']))
        classification='Dated immutable native project body; actual retained Git stdout; never current authority'
    else:raw=read(p);classification='Foreign individually bound input, not copied into authored closure'
    need(len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Full unchanged individually bound input '+name)
    ref={'path':name,'bytes':len(raw),'sha256':sha(raw),'individual_exclusion':True,'classification':classification}
    need(name not in external or external[name]==ref,'Consistent repeated literal input');external[name]=ref
for name in ['INPUT_READING_ACTUAL_CAPTURE','INDEPENDENT_CONTROLS_ACTUAL_CAPTURE','SUPPLEMENTAL_CONTROLS_ACTUAL_CAPTURE','OWN_REFINEMENT_AUTHOR_ACTUAL_CAPTURE','INDEPENDENT_CONTROLS_V2_ACTUAL_CAPTURE','SUPPLEMENTAL_CONTROLS_V2_ACTUAL_CAPTURE']:
    base=D/name;cap=load(base/'CAPTURE.json');need(type(cap['actual_child_pid']) is int and cap['actual_child_pid']>0 and cap['actual_execution'] is True and cap['completed_after_child_exit'] is True and cap['exit_code']==0 and cap['source_unchanged'] is True,'Genuine completed own capture')
    need(dt.datetime.fromisoformat(cap['started_utc'])<=dt.datetime.fromisoformat(cap['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Complete actual own clocks')
    need(sha(read(base/'PRELAUNCH_SOURCE.py'))==cap['prelaunch_source_sha256'] and sha(read(base/'PRELAUNCH_OPERATOR.py'))==cap['prelaunch_operator_sha256'],'Entire genuine own prelaunch source/operator')
    for channel in ['stdout','stderr']:
        ref=cap[channel];raw=read(base/ref['path']);need(len(raw)==ref['bytes'] and sha(raw)==ref['sha256'],'Complete own actual stream')
    need({p.name for p in base.iterdir()}=={'CAPTURE.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Exact complete five-member own capture')
final=load(D/'INDEPENDENT_CONTROL_RESULT_V2.json');supp=load(D/'SUPPLEMENTAL_CONTROL_RESULT_V2.json');verdict=load(D/'VERDICT.json')
need(type(supp['AST_all_guard_exports_checked']) is dict and len(supp['AST_all_guard_exports_checked'])==4,'Corrected actual AST export map retained')
need(final['predicates']+supp['predicates']==verdict['final_positive_control_predicates']==4151 and final['negative_control_count']+supp['negative_control_count']==verdict['final_negative_controls']==84,'Exact final genuine control counts')
need(verdict['mandatory_defects']==[] and verdict['future_ROOT_approval_certified'] is False and verdict['future_actual_PR42_predecessor_certified'] is False,'Scope not future authority')
output={'schema':'PR43_V2_SOURCE_ADVERSARY_PRE_CLOSURE_CHECK_v1','actual_pid':os.getpid(),'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS','external_individual_input_count':len(external),'external_individually_excluded_inputs':sorted(external.values(),key=lambda z:z['path']),'all_six_complete_actual_captures_checked':True,'future_ROOT_or_PR42_approval_certified':False}
(D/'CLOSURE_CONTROL_RESULT.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:v for k,v in output.items() if k!='external_individually_excluded_inputs'},indent=2))
