"""Additional independent exact queue/preimage/publication controls, owned only."""
from pathlib import Path
import ast,copy,ctypes,datetime as dt,hashlib,json,os,stat
D=Path(__file__).resolve().parent;A=D.parent;R=A.parents[2];V=A/'acceptance_preparation_family_v2'
checks=[];negatives=[]
def need(ok,label):
    if not ok:raise ValueError(label)
    checks.append(label)
def reject(label,fn):
    try:fn()
    except (ValueError,TypeError,OSError,KeyError):negatives.append(label)
    else:raise ValueError('Accepted mutant '+label)
def eq(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
    return a==b
def load(p):return json.loads(p.read_bytes())
guard=ast.parse((V/'pr43_guards.py').read_bytes())
exports={n.name for n in guard.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
for n in guard.body:
    if isinstance(n,ast.Assign):
        for target in n.targets:
            exports|={v.id for v in ast.walk(target) if isinstance(v,ast.Name)}
used={}
for name in ['seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']:
    tree=ast.parse((V/name).read_bytes());attrs={n.attr for n in ast.walk(tree) if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='g'}
    need(attrs<=exports,'Every literal g export exists '+name);used[name]=sorted(attrs)
# Whole queue preservation at the actual source row, read-only.
raw=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes()
header='| Rank | ID / code | Problem | EV | Impact (/10) | Difficulty | Proposed | Status | Turns | Chat | Findings | DOI |'
lines=raw.decode().splitlines(keepends=True);need(sum(s.startswith('| Rank | ID / code |') for s in lines)==1,'One actual queue header')
rows=[s for s in lines if len(s.split('|'))==14 and s.split('|')[2].strip()=='30004386 / OWR-17469-011'];need(len(rows)==1,'One actual target row')
row=rows[0];cells=row.split('|');need(cells[8].strip()=='queued' and cells[9].strip()=='0/5','Actual source row queued0/5')
new=cells.copy();new[8]=' already_solved ';new[11]=' [Accepted qualified scoped partial](attempts/30004386/ACCEPTANCE.md) ';newrow='|'.join(new)
after=raw.replace(row.encode(),newrow.encode(),1)
def validqueue(body):
    if body!=after or body.replace(newrow.encode(),row.encode(),1)!=raw:raise ValueError('Exact entire queue inverse')
validqueue(after);need({i for i in range(len(cells)) if cells[i]!=new[i]}=={8,11},'Only Status Findings change')
need(new[9]==cells[9] and new[10]==cells[10] and new[12]==cells[12],'Actual Turns Chat DOI exact')
reject('queue_other_byte',lambda:validqueue(after+b'\n'));reject('queue_budget_change',lambda:validqueue(after.replace(b'0/5',b'1/5',1)))
def ledger(raw,used,limit):
    if raw!=b'' or type(used) is not int or used!=0 or type(limit) is not int or limit!=5:raise ValueError('Literal empty0/5')
ledger(b'',0,5)
for label,body,used,limit in [('nonempty',b'x',0,5),('whitespace',b'\n',0,5),('invented_JSONL',b'{"turn":1}\n',0,5),('bool_used',b'',False,5),('float_used',b'',0.0,5),('str_used',b'','0',5),('wrong_used',b'',1,5),('bool_limit',b'',0,True),('wrong_limit',b'',0,4)]:
    reject('ledger_'+label,lambda body=body,used=used,limit=limit:ledger(body,used,limit))
dated=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json');now=dt.datetime.now(dt.timezone.utc)
paths={z['path'] for z in dated['files']};need(len(paths)==13,'Dated13 names only, not fresh authority')
fresh={'schema':'pr43-root-fresh-acceptance-input-preimages/v1','approved_by_root':True,'created_utc':now.isoformat(),'reason_date_utc':now.date().isoformat(),'reason':'Synthetic test reason protecting current native state after independent completed review.','current_head':'a'*40,'files':[{**z,'worktree_mode':0o644} for z in dated['files']]}
def validfresh(o):
    if type(o) is not dict or set(o)!=set(fresh):raise ValueError('Exact fresh schema')
    if o['approved_by_root'] is not True or o['schema']!=fresh['schema']:raise ValueError('Real approval required')
    stamp=dt.datetime.fromisoformat(o['created_utc'])
    if stamp.tzinfo is None or stamp.utcoffset()!=dt.timedelta(0) or stamp>dt.datetime.now(dt.timezone.utc) or o['reason_date_utc']!=stamp.date().isoformat():raise ValueError('Actual UTC reason date')
    reason=o['reason']
    if type(reason) is not str or reason!=reason.strip() or len(reason)<40 or len(reason.split())<6:raise ValueError('Substantive reason')
    if type(o['files']) is not list or len(o['files'])!=13 or {z['path'] for z in o['files']}!=paths:raise ValueError('Exact13names')
    for z in o['files']:
        if type(z) is not dict or set(z)!={'path','bytes','sha256','worktree_mode'} or type(z['bytes']) is not int or type(z['worktree_mode']) is not int or not 0<=z['worktree_mode']<=0o7777:raise ValueError('Complete typed fresh row')
validfresh(fresh);need(True,'Explicitly synthetic fresh13 valid')
for label,key,value in [('bool_approval','approved_by_root',1),('empty_reason','reason','yes'),('wrong_date','reason_date_utc','2026-01-01'),('naive_time','created_utc','2026-10-03T02:00:00'),('future_time','created_utc',(now+dt.timedelta(days=1)).isoformat())]:
    mutant=copy.deepcopy(fresh);mutant[key]=value;reject('fresh_'+label,lambda mutant=mutant:validfresh(mutant))
for label,key,value in [('bool_mode','worktree_mode',False),('negative_mode','worktree_mode',-1),('overflow_mode','worktree_mode',0o10000),('float_size','bytes',1.0)]:
    mutant=copy.deepcopy(fresh);mutant['files'][0][key]=value;reject('fresh_'+label,lambda mutant=mutant:validfresh(mutant))
mutant=copy.deepcopy(fresh);mutant['files'].pop();reject('fresh_missing_path',lambda:validfresh(mutant))
mutant=copy.deepcopy(fresh);mutant['files'][0]['extension']=True;reject('fresh_unknown_row_field',lambda:validfresh(mutant))
# Actual absent-only complete-file and macOS complete-directory publication.
private=D/'PRIVATE_PUBLICATION_FIXTURES';private.mkdir();tmp=private/'complete_temp';tmp.write_bytes(b'Own complete bytes.\n');existing=private/'existing_target';existing.write_bytes(b'Existing bytes must survive.\n')
before=existing.read_bytes();reject('atomic_existing_file',lambda:os.link(tmp,existing,follow_symlinks=False));need(existing.read_bytes()==before and tmp.read_bytes()==b'Own complete bytes.\n','Existing target and temp preserved')
newtarget=private/'new_target';os.link(tmp,newtarget,follow_symlinks=False);need(newtarget.read_bytes()==tmp.read_bytes(),'Absent-only file publication succeeds')
stage=private/'stage_for_existing';stage.mkdir();(stage/'own_marker').write_bytes(b'Own failed-stage marker.\n')
target=private/'existing_directory';target.mkdir();(target/'own_marker').write_bytes(b'Own existing directory marker.\n')
libc=ctypes.CDLL(None,use_errno=True);rename=libc.renamex_np;rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
code=rename(os.fsencode(stage),os.fsencode(target),4);need(code!=0 and stage.is_dir() and (target/'own_marker').read_bytes()==b'Own existing directory marker.\n','Actual RENAME_EXCL rejects existing directory')
errno=ctypes.get_errno();negatives.append('atomic_existing_directory')
second=private/'stage_for_absent';second.mkdir();(second/'own_marker').write_bytes(b'Own published directory marker.\n');absent=private/'new_directory'
need(rename(os.fsencode(second),os.fsencode(absent),4)==0 and not second.exists() and (absent/'own_marker').read_bytes()==b'Own published directory marker.\n','Actual RENAME_EXCL absent directory succeeds')
result={'schema':'PR43_V2_SOURCE_ADVERSARY_SUPPLEMENTAL_CONTROLS_v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'predicates':len(checks),'negative_controls':negatives,'negative_control_count':len(negatives),'actual_queue_bytes_read':len(raw),'actual_queue_sha256':hashlib.sha256(raw).hexdigest(),'queue_modified':False,'AST_all_guard_exports_checked':used,'actual_RENAME_EXCL_rejection_errno':errno,'fresh13_test_is_synthetic_not_ROOT_approval':True,'no_future_PR42_receipt_or_ROOT_gate_certified':True,'production_native_candidate_scripts_imported_compiled_executed':False}
(D/'SUPPLEMENTAL_CONTROL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
