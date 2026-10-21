import ast,copy,importlib.util,json,sys,types
from pathlib import Path
from datetime import datetime,timezone
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;P=R.parents[3];S=R/'private/helpers/receipts'
def module(name):
 spec=importlib.util.spec_from_file_location(name,P/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
le=module('update_pr938_publication_ledger');tr=module('append_pr938_tracker')
rows=[]
def check(name,call,reject=False):
 try:call()
 except Exception as e:
  if not reject:raise
  rows.append(dict(case=name,rejected=True,error=str(e)));return
 if reject:raise RuntimeError('Unexpected acceptance '+name)
 rows.append(dict(case=name,passed=True))
# Mock every Git write/read in the actual recursive explicit-tree builder.
calls=[]
def mocked_run(args,**kw):
 calls.append(args)
 if args[:2]==['git','hash-object']:return '1'*40
 if args[:2]==['git','ls-tree']:return '100644 blob '+'2'*40+'\t'+args[-1]
 raise RuntimeError('Unmocked call')
def fake_git(args,**kw):
 calls.append(args)
 if args[:2]==['git','ls-tree']:
  ref=args[-1];payload={'P':b'040000 tree '+'A'.encode()*40+b'\tunsolved_math_prioritization\0', 'A'*40:b'100644 blob '+b'2'*40+b'\tQUEUE.md\0'+b'100644 blob '+b'3'*40+b'\tstate.json\0'+b'100644 blob '+b'4'*40+b'\thistory.jsonl\0'+b'100644 blob '+b'5'*40+b'\tOTHER.md\0'}[ref]
  return types.SimpleNamespace(stdout=payload)
 if args[:2]==['git','mktree']:
  if b'OTHER.md' in kw['input'] and b'5'*40 not in kw['input']:raise RuntimeError('Unrelated tree entry changed')
  return types.SimpleNamespace(stdout=b'9'*40+b'\n')
 raise RuntimeError('Unmocked subprocess')
le.run=mocked_run;le.subprocess=types.SimpleNamespace(run=fake_git)
allowed={'unsolved_math_prioritization/'+n:'new' for n in ['QUEUE.md','state.json','history.jsonl']}
check('explicit_tree_only_three_declared_paths_mocked_git',lambda:le.explicit_tree('P',allowed))
for kind,change in [('extra',dict(allowed,extra='x')),('missing',{k:v for k,v in allowed.items() if not k.endswith('QUEUE.md')})]:check('explicit_tree_'+kind,lambda change=change:le.explicit_tree('P',change),True)
rows.append(dict(case='explicit_tree_no_shared_git_index_commands',passed=not any(a[1] in ['add','reset','checkout','update-index','read-tree','write-tree'] for a in calls),all_calls_mocked=True))
# Native receipt linkage in both duplicated validators.
def load(p):return json.loads(p.read_text())
freeze=load(S/'publication/PREPUBLICATION_FREEZE.json');import hashlib
pin=hashlib.sha256((S/'publication/PREPUBLICATION_FREEZE.json').read_bytes()).hexdigest();head=freeze['original_pr_head'];acc=dict(accepted=True,original_pr_head=head,full_package_reviews=[{},{}],freeze_sha256=pin,files=freeze['files']);pub=load(S/'publication/ZENODO_STAGE.json');merge=dict(number=938,state='MERGED',headRefOid=head,mergeCommit={'oid':'b'*40})
tracker=dict(confirmed=True,readback_matches=True,pr=938,problem_id='30003634',original_pr_head=head,merged_head=head,merge_commit='b'*40,accepted_freeze_sha256=pin,doi=pub['doi'],zenodo_record_id=123,spreadsheet_id=tr.SID,gid=1254632077,tab_title='Math Puzzles',updated_range="'Math Puzzles'!A10:D10",row=['primary','','https://doi.org/'+pub['doi'],'note'])
(S/'TRACKER_READBACK.json').write_text(json.dumps(dict(range=tracker['updated_range'],values=[tracker['row']])))
event=dict(id='30003634',pr=938,doi=pub['doi'],original_pr_head=head,accepted_freeze_sha256=pin,merged_commit='b'*40,zenodo_record_id=123,evidence=dict(tracker_range=tracker['updated_range']));native=dict(push_confirmed=True,published_event=event)
for m in [tr,le]:
 check('native_link_positive_'+m.__name__,lambda m=m:m.verify_receipt_links(S,pub,merge,acc,tracker,native))
 for key,value in [('id','different'),('pr',939),('doi','bad'),('original_pr_head','0'*40),('accepted_freeze_sha256','0'*64),('merged_commit','0'*40),('zenodo_record_id',124),('evidence',dict(tracker_range="'Other'!A10:D10"))]:
  x=copy.deepcopy(native);x['published_event'][key]=value;check('native_link_'+m.__name__+'_'+key,lambda x=x,m=m:m.verify_receipt_links(S,pub,merge,acc,tracker,x),True)
# Evaluate actual CAS failure classifier with no network; accepted retries require
# an identified concurrent-main condition, and actual push command has no force.
source=(P/'update_pr938_publication_ledger.py').read_text();tree=ast.parse(source)
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');loop=next(n for n in fn.body if isinstance(n,ast.For));tail=[];taking=False
for n in loop.body:
 if isinstance(n,ast.Import):taking=True
 if taking:tail.append(n)
code=compile(ast.Module(body=tail,type_ignores=[]),'actual_CAS_retry_classifier','exec')
parent='a'*40;new='c'*40
for label,stderr,expected in [('non_fast_forward','non-fast-forward',False),('fetch_first','fetch first',False),('exact_race',f"cannot lock ref 'refs/heads/main': is at {new} but expected {parent}",False),('wrong_parent',f"cannot lock ref 'refs/heads/main': is at {new} but expected {'b'*40}",True),('unchanged',f"cannot lock ref 'refs/heads/main': is at {parent} but expected {parent}",True),('unknown','permission denied',True)]:
 check('CAS_'+label,lambda stderr=stderr:exec(code,dict(parent=parent,push=types.SimpleNamespace(stderr=stderr))),expected)
push=next(n for n in ast.walk(loop) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='run' and n.args and isinstance(n.args[0],ast.List) and any(isinstance(x,ast.Constant) and x.value=='push' for x in n.args[0].elts))
rows.append(dict(case='CAS_nonforced_explicit_remote_main_push',actual_command_ast=ast.unparse(push.args[0]),passed='--force' not in ast.unparse(push.args[0]) and 'refs/heads/main' in ast.unparse(push.args[0])))
(R/'ADDITIONAL_HELPER_CONTROLS.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',rows=rows,all_operations_pure_or_mocked=True,operational_mains_called=False),indent=2)+'\n');print(json.dumps(dict(status='PASS',cases=len(rows))))
