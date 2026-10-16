"""New actual candidate06 deterministic closing-read controls. Only Git/services are fake."""
import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use -I -B')
from pathlib import Path
import hashlib,json,copy,types,contextlib,io,shutil
from datetime import datetime,timezone
O=Path(__file__).resolve().parent;R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';root=O/'private/current07_context';p=root/P.name;a=p/'audits/pr946_6000001';d=a/'preprint';w=a/'reviews/full_package_07'
b=(P/'accept_pr946.py').read_bytes();assert hashlib.sha256(b).hexdigest()=='8e1a0d7b3ca6e5d72e76415541b393fbfbe52e307368bc86b9e7982d5be27cd7';N={'__name__':'_actual06_closure_','__file__':str(P/'accept_pr946.py')};exec(compile(b,N['__file__'],'exec'),N);N.update(ROOT=root,P=p,A=a,D=d);N['freeze_check'].__defaults__=(d,False);N['archive_check'].__defaults__=(d,)
F=json.loads((d/'FREEZE.json').read_bytes());FP=hashlib.sha256((d/'FREEZE.json').read_bytes()).hexdigest();assert FP=='9af8f2570af53b6a6658a7998ac08927829c8747be7c764a8d2c392dc6c6afe1';ctx=N['capture_inventory'](F['operations_inventory_sha256']);accepted=json.loads((a/'ACCEPTANCE.json').read_text());oldacc=(a/'ACCEPTANCE.json').read_bytes();specs=[f"{q['round']:02d}:"+q['manifest_sha256'] for q in accepted['full_package_reviews']];originals=json.loads((O/'AUTHENTICATION_START.json').read_text())['originals'];queue=json.loads((A/'reviews/full_package_05/AUTHENTICATION_START.json').read_text())['immutable_queue_row'].encode();assert hashlib.sha256(queue.rstrip(b'\n')).hexdigest()=='11fbd85ea991520337b918a2caa719737acff2d202c796aa93e3343c61403895';catalog=json.dumps([x for x in json.loads((R/N['CATALOG']).read_text()) if str(x.get('id'))=='6000001']).encode()
def blob(ref,name):
 if name in originals:return(a/'original'/name).read_bytes()
 return {N['QUEUE']:queue,N['CATALOG']:catalog,N['RELATED']:b'{"groups":[]}'}[name]
def run(argv,**kwargs):
 if argv[:2]==['git','ls-tree']:return '100644 blob '+originals[argv[-1]]['git_blob']+'\t'+argv[-1]+'\n'
 if argv[:2]==['git','fetch']:return ''
 if argv[:2]==['git','merge-base']:return 'a'*40+'\n'
 if argv[:2]==['gh','api']:return '\n'.join([*originals,N['QUEUE']])+'\n'
 raise RuntimeError('Unexpected fake transport '+repr(argv))
N.update(blob=blob,run=run,remote_main=lambda:'a'*40,subprocess=types.SimpleNamespace(run=lambda *x,**k:(_ for _ in()).throw(RuntimeError('Forbidden external dispatch'))));N['pr_view']=lambda:{'number':946,'state':'OPEN','isDraft':True,'baseRefName':'main','headRefOid':N['HEAD'],'body':(d/'ORIGINAL_PR_DESCRIPTION.md').read_text()}
targets={'tex':d/'research_note.tex','freeze':d/'FREEZE.json','inventory':a/'OPERATIONS_INVENTORY.json','core':p/'accept_pr946.py','evidence':root/next(iter(F['evidence_files'])),'review_payload':w/'FULL_AUDIT.md','review_seal':w/'MANIFEST.json','historical_payload':d/'reviewed_candidates/candidate01/research_note.tex','historical_dependency':d/'reviewed_candidates/candidate01/operations/zenodo_deposit_tool/zenodo.py'};original={k:q.read_bytes() for k,q in targets.items()};extra=a/'reviews/full_package_08';records=[]
def inject(k):
 if k in ['pending','adverse']:
  extra.mkdir()
  if k=='adverse':(extra/'RESULT.json').write_text('{"required_issues":[{"id":"SYNTHETIC_ADVERSE"}]}')
 else:targets[k].write_bytes(original[k]+b'\n')
def restore():
 for k,q in targets.items():q.write_bytes(original[k])
 if extra.exists():shutil.rmtree(extra)
 (a/'ACCEPTANCE.json').write_bytes(oldacc)
def call(fn):
 with contextlib.redirect_stdout(io.StringIO()):return fn()
def reject(label,fn):
 try:call(fn)
 except (RuntimeError,OSError,ValueError,KeyError) as e:
  assert 'Unexpected fake' not in str(e) and 'Forbidden external' not in str(e);records.append({'case':label,'rejected':True,'reason':str(e)[:600]});return
 raise RuntimeError('INVALID ACCEPTED '+label)
real_source=N['source_gate'];real_read=N['read_regular'];kinds=[*targets,'pending','adverse']
for kind in kinds:
 restore();(a/'ACCEPTANCE.json').unlink();hits=[0]
 def source(parent):
  value=real_source(parent);hits[0]+=1
  if hits[0]==2:inject(kind)
  return value
 N['source_gate']=source;reject('initial_accept_final_actual_source_'+kind,lambda:N['accept'](types.SimpleNamespace(freeze=FP,review=specs),ctx));assert hits[0]==2 and not(a/'ACCEPTANCE.json').exists();restore()
N['source_gate']=real_source
for kind in ['review_payload','review_seal','historical_payload','historical_dependency','pending','adverse']:
 hits=[0];fired=[False]
 def read(path,*args,**kw):
  value=real_read(path,*args,**kw)
  if Path(path)==d/'FREEZE.json':
   hits[0]+=1
   if hits[0]==2:inject(kind);fired[0]=True
  return value
 N['read_regular']=read;reject('shared_guard_during_second_current_FREEZE_'+kind,lambda:N['accepted_review_check'](accepted,F,ctx));assert fired[0];N['read_regular']=real_read;restore()
# Positive initial approval uses actual premerge/source/original/archive/review/closing functions.
(a/'ACCEPTANCE.json').unlink();call(lambda:N['accept'](types.SimpleNamespace(freeze=FP,review=specs),ctx));fresh=N['load'](a/'ACCEPTANCE.json');assert fresh['accepted'] and fresh['original_declared_turns']=='4/5' and fresh['author_native_history_authenticated'] is False and fresh['proof_search_turns_added_by_audit']==0;call(lambda:N['accepted_package'](ctx));records.append({'case':'positive_actual_initial_accept_and_complete_readback','pass':True,'review_rounds':7,'originals':33,'audit_proof_turns':0});restore()
call(lambda:N['accepted_package'](ctx));records.append({'case':'positive_restored_actual_current06_complete_chain','pass':True})
(O/'CLOSURE07_CONTROLS.json').write_text(json.dumps({'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'candidate_revision':6,'actual_current06_context':True,'all_six_prior_sealed_rounds':True,'terminal07_explicitly_synthetic':True,'subject_core_sha256':hashlib.sha256(b).hexdigest(),'actual_guards_unstubbed':['premerge_gate','source_gate','original_check','archive_check','capture_inventory','freeze_check','review_check','candidate_state_check','review_state_check','accepted_state_check','accepted_review_check','accept','accepted_package'],'fake_only':['Git object transport','PR metadata transport','remote main transport'],'cases':records,'case_count':len(records),'actual_external_mutations':0,'no_hostile_OS_atomicity_contract':True},indent=2)+'\n');print(json.dumps({'status':'PASS','new_closure_cases':len(records),'external_mutations':0}))
