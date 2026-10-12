"""Complete bounded read of private captures, literal replay and typed results."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat
F=Path(__file__).absolute().parent;R=Path('/Users/alec/Documents/Math');A=F.parent
def need(x,n):
    if not x:raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):
    need(not p.is_symlink()and all(not q.is_symlink()for q in p.parents)and stat.S_ISREG(p.stat().st_mode),'regular');return p.read_bytes()
def strict(p):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'duplicate key');d[k]=v
        return d
    def bad(s):raise ValueError(s)
    return json.loads(raw(p),object_pairs_hook=pairs,parse_constant=bad)
def same(a,b):
    need(type(a)is type(b),'recursive type match')
    if type(a)is dict:
        need(a.keys()==b.keys(),'exact keys')
        for k in a:same(a[k],b[k])
    elif type(a)is list:
        need(len(a)==len(b),'list length')
        for x,y in zip(a,b):same(x,y)
    else:need(a==b,'scalar exact')
bindings=strict(F/'SELECTED_INPUT_BINDINGS.json')
for r in bindings['selected_files']:
    p=R/r['path'];b=raw(p);need(type(r['bytes'])is int and len(b)==r['bytes']and sha(b)==r['sha256']and stat.S_IMODE(p.stat().st_mode)==r['full_mode']==292,'literal selected evidence')
caps=[]
for name,pid in [('INDEPENDENT_CONTROLS_ACTUAL_CAPTURE',54290),('LITERAL_AUTHOR_REPLAY_ACTUAL_CAPTURE',54848)]:
    d=F/name;need({p.name for p in d.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','prelaunch_target.py','prelaunch_operator.py','stdout.bin','stderr.bin'},'full own capture6')
    c=strict(d/'CAPTURE.json');pre=strict(d/'PRELAUNCH.json')
    need(c['actual_execution']is True and c['completed']is True and type(c['pid'])is int and c['pid']==pid and type(c['exit_code'])is int and c['exit_code']==0 and c['source_unchanged']is True and c['operator_unchanged']is True and c['stdin_supplied']is False and c['status']=='PASS_ACTUAL_PRIVATE_CHILD','actual child outcome')
    need(dt.datetime.fromisoformat(c['started_utc'])<dt.datetime.fromisoformat(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'actual chronology')
    for k,v in pre.items():
        if k not in ('actual_execution','completed','pid','exit_code','source_unchanged'):same(c[k],v)
    need(pre['actual_execution']is False and pre['completed']is False and pre['pid']is None and pre['exit_code']is None and pre['source_unchanged']is None,'prelaunch not future receipt')
    need(c['argv']==['/usr/bin/python3','-B',str(R/c['source']['path'])]and raw(d/'prelaunch_target.py')==raw(R/c['source']['path'])and sha(raw(d/'prelaunch_target.py'))==c['source']['sha256'],'unchanged target/source/argv')
    need(sha(raw(d/'prelaunch_operator.py'))==c['operator_sha256']==sha(raw(F/'capture_private.py')),'complete captured operator')
    for k in ('stdout','stderr'):
        r=c[k];b=raw(d/r['path']);need(type(r['bytes'])is int and r['path']==k+'.bin'and len(b)==r['bytes']and sha(b)==r['sha256'],'full typed stream')
    need(c['stderr']['bytes']==0,'zero successful stderr');caps.append(c)
controls=strict(F/'CONTROL_RESULT.json');same(controls,strict(F/'INDEPENDENT_CONTROLS_ACTUAL_CAPTURE/stdout.bin'));need(controls['actual_pid']==54290 and controls['assertions']==6155 and controls['edge_cases']==360 and controls['relation_cases']==352 and len(controls['negative_controls'])==8,'independent result counts')
original=strict(A/'original/even_move_verification.json');replay=strict(F/'LITERAL_AUTHOR_REPLAY_ACTUAL_CAPTURE/stdout.bin');same(original,replay)
need(raw(A/'original/verify_even_moves.py')==raw(F/'private_author/verify_even_moves.py')and raw(A/'original/even_move_verification.json')==raw(F/'LITERAL_AUTHOR_REPLAY_ACTUAL_CAPTURE/stdout.bin'),'literal entire helper/result bytes')
result=dict(schema='pr50-classical-private-evidence-validation/v1',status='PASS_COMPLETE_BOUNDED_PRIVATE_EVIDENCE',actual_pid=os.getpid(),created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),complete_captures=caps,literal_replay_byte_and_recursive_type_exact=True,entire_replayed_author_result=replay,independent_control_summary={k:controls[k]for k in ['assertions','edge_cases','coverage','relation_cases','negative_controls']},original_head=bindings['head'],future_acceptance_approved=False)
with(F/'PRIVATE_EVIDENCE_VALIDATION.json').open('xb')as h:h.write((json.dumps(result,indent=2,allow_nan=False)+'\n').encode())
print(json.dumps(dict(status=result['status'],actual_pid=os.getpid(),literal_author_assertions=replay['exact_assertions'],independent_assertions=controls['assertions'],future_acceptance_approved=False)))
