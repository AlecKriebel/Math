"""Actual finalizer verifier and status gate with fully mocked reads, own fixtures."""
import ast,copy,hashlib,importlib.util,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parents[3];A=R.parents[1];T=R/'private/finalizer_complete_v2';T.mkdir(parents=True,exist_ok=False);Q=T/'publication';Q.mkdir();sys.dont_write_bytecode=True
HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b';MERGE='b'*40;PARENT='c'*40;NATIVE='d'*40;REMOTE='e'*40;KEY='30003634';QUEUE='unsolved_math_prioritization/QUEUE.md';STATE='unsolved_math_prioritization/state.json';HISTORY='unsolved_math_prioritization/history.jsonl';rows=[]
def need(v,s):
 if not v:raise RuntimeError(s)
def load(p):return json.loads(p.read_bytes())
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
spec=importlib.util.spec_from_file_location('review05_finalizer_complete',P/'finalize_pr938_and_gate_next.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.A=T;m.D=Q
# Use authentic complete receipt links, with entirely synthetic DOI and commit IDs.
B=R/'private/controls_0_normal_final'
for name in ['ZENODO_PUBLISH_INTENT.json','ZENODO_STAGE.json','ZENODO_INSPECT.json','ZENODO_PUBLISH.json','PREPUBLICATION_FREEZE.json','zenodo-deposit.json','deep-derived-pure-braids-source-verification-v1.0.zip','output/pdf/note.pdf']:
 p=Q/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((B/'publication'/name).read_bytes())
acc=load(B/'ACCEPTANCE.json');save(T/'ACCEPTANCE.json',acc)
merge=load(B/'PR_MERGE_RECEIPT.json');tracker=load(B/'TRACKER_RECEIPT.json');save(T/'PR_MERGE_RECEIPT.json',merge);save(T/'TRACKER_RECEIPT.json',tracker);save(T/'TRACKER_READBACK.json',load(B/'TRACKER_READBACK.json'));snapshot=load(A/'ORIGINAL_SNAPSHOT.json');save(T/'ORIGINAL_SNAPSHOT.json',snapshot)
pub=load(Q/'ZENODO_PUBLISH.json');doi=pub['doi'];event={'id':KEY,'pr':938,'doi':doi,'original_pr_head':HEAD,'accepted_freeze_sha256':acc['freeze_sha256'],'merged_commit':MERGE,'merged_base':'main','zenodo_record_id':123,'evidence':{'tracker_range':tracker['updated_range']},'status':'preprint_published','turns_used':2,'candidate_turn':2,'turn_limit':5,'verified_candidate_approaches':2,'original_total_attempt_count_known':False,'proof_search_turns_added_by_audit':1,'turn_count_status':'original_observed_one_plus_one_genuinely_recorded_strengthening'}
native={'push_confirmed':True,'published_event':event,'commit':NATIVE,'parent':PARENT,'paths':[QUEUE,STATE,HISTORY]};save(T/'NATIVE_PUBLICATION_RECEIPT.json',native)
oldrow=(A/'GATED_QUEUE_ROW.md').read_text();cells=oldrow.rstrip('\n').split('|');cells[8]=' preprint_published ';cells[9]=' 2/5 ';cells[12]=' '+doi+' ';newrow='|'.join(cells)+'\n';other=b'opaque unrelated queue bytes\r\n';oldstate=b'{ "other" : {"opaque":[1,true]}, "30003634" : {"turns_used":1} }\n';newstate=('{ "other" : {"opaque":[1,true]}, "30003634" : '+json.dumps(event)+' }\n').encode();oldhistory=b'{"id":"unrelated","opaque":"retained"}\n';newhistory=oldhistory+(json.dumps(event)+'\n').encode()
base_blobs={(PARENT,QUEUE):other+oldrow.encode(),(NATIVE,QUEUE):other+newrow.encode(),(PARENT,STATE):oldstate,(NATIVE,STATE):newstate,(PARENT,HISTORY):oldhistory,(NATIVE,HISTORY):newhistory,(HEAD,QUEUE):oldrow.encode()}
for name in snapshot['files']:base_blobs[(MERGE,name)]=(A/'original'/name).read_bytes()
base_live=copy.deepcopy(merge);base_rb=load(T/'TRACKER_READBACK.json');captured=[]
def exercise(label,mutator=None,expected_fragment=None):
 blobs=copy.deepcopy(base_blobs);live=copy.deepcopy(base_live);rb=copy.deepcopy(base_rb);settings={'parent':PARENT,'paths':native['paths'],'fail_ancestry':None};n=copy.deepcopy(native)
 if mutator:mutator(blobs,live,rb,settings,n)
 save(T/'NATIVE_PUBLICATION_RECEIPT.json',n);calls=[]
 def read(args):
  calls.append(args)
  if args[:3]==['gh','pr','view']:return json.dumps(live)
  if args[0]=='gws':return json.dumps(rb)
  if args[:2]==['git','fetch']:return ''
  if args[:2]==['git','ls-remote']:return REMOTE+' refs/heads/main'
  if args[:2]==['git','merge-base']:
   if settings['fail_ancestry']==args[3]:raise RuntimeError('Controlled ancestry failure')
   return ''
  if args[:2]==['git','show']:return settings['parent']+'\n'
  if args[:2]==['git','diff']:return '\n'.join(settings['paths'])
  raise RuntimeError('Unmocked external operation '+repr(args))
 m.run=read;m.blob=lambda ref,name:blobs[(ref,name)];m.save=lambda path,value:captured.append({'path':str(path),'value':value})
 try:result=m.verify_completed()
 except RuntimeError as e:
  need(mutator is not None and (expected_fragment is None or expected_fragment in str(e)),label+' unrelated rejection '+str(e));rows.append({'case':label,'rejected':True,'reason':str(e)});return
 need(mutator is None,label+' adverse fixture passed');need(any(c[:2]==['git','merge-base'] and c[3]==MERGE for c in calls),'merge/native ancestry absent');rows.append({'case':label,'passed':True,'all_service_Git_reads_mocked':True})
exercise('actual_complete_finalizer_positive')
for field,val in [('baseRefName','other'),('headRefOid','0'*40),('state','OPEN'),('mergeCommit',{'oid':'0'*40})]:exercise('fresh_PR_'+field,lambda b,l,r,s,n,f=field,v=val:l.update({f:v}),'Fresh actual merged head differs')
exercise('fresh_tracker_range',lambda b,l,r,s,n:r.update(range="'Math Puzzles'!A11:D11"),'tracker row differs')
exercise('fresh_tracker_values',lambda b,l,r,s,n:r.update(values=[['changed']]),'tracker row differs')
for c in [NATIVE,MERGE]:exercise('ancestry_'+c[0],lambda b,l,r,s,n,c=c:s.update(fail_ancestry=c),'ancestry failure')
exercise('native_wrong_parent',lambda b,l,r,s,n:s.update(parent='0'*40),'parent differs')
exercise('native_unrelated_path',lambda b,l,r,s,n:s.update(paths=[QUEUE,STATE,HISTORY,'unrelated']),'path')
exercise('other_queue_bytes',lambda b,l,r,s,n:b.update({(NATIVE,QUEUE):b'CHANGED\n'+newrow.encode()}),'other queue bytes')
exercise('native_wrong_target_turns',lambda b,l,r,s,n:b.update({(NATIVE,QUEUE):other+newrow.replace(' 2/5 ',' 3/5 ').encode()}),'other queue bytes')
exercise('other_state_literal_change',lambda b,l,r,s,n:b.update({(NATIVE,STATE):newstate.replace(b'"other" :',b'"other":')}),'Other state members changed')
exercise('state_event_mismatch',lambda b,l,r,s,n:b.update({(NATIVE,STATE):newstate.replace(b'"turns_used": 2',b'"turns_used": 3')}),'state differs')
exercise('history_prefix_change',lambda b,l,r,s,n:b.update({(NATIVE,HISTORY):b'changed\n'+newhistory}),'history bytes changed')
exercise('history_duplicate_event',lambda b,l,r,s,n:b.update({(NATIVE,HISTORY):newhistory+(json.dumps(event)+'\n').encode()}),'append exactly')
exercise('original_observed_turns_change',lambda b,l,r,s,n:b.update({(HEAD,QUEUE):oldrow.replace(' 1/5 ',' 2/5 ').encode()}),'Original observed accounting')
name=next(iter(snapshot['files']));exercise('merged_original_file_change',lambda b,l,r,s,n:b.update({(MERGE,name):b'changed'}),'Merged original bytes changed')
# Status-only next-target loop extracted verbatim: fake IDs/rows, no other problem's source.
fn=next(n for n in ast.parse((P/'finalize_pr938_and_gate_next.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='main');loop=next(n for n in fn.body if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='old');loopcode=compile(ast.fix_missing_locations(ast.Module(body=[loop],type_ignores=[])),'review05_actual_status_only_next_loop','exec')
for state_,draft,status in [('CLOSED',True,'claimed_solved'),('OPEN',False,'claimed_solved'),('OPEN',True,'queued'),('OPEN',True,'exhausted'),('OPEN',True,'claimed_solved_extra')]:
 calls=[];synthetic_inventory=[{'number':939,'entries':[{'id':'synthetic-only'}]}];state={'eligible_prs':[939],'completed_prs':[]};skipped=[]
 def next_read(args):
  calls.append(args)
  if args[:3]==['gh','pr','view']:return json.dumps({'number':939,'state':state_,'isDraft':draft,'headRefOid':'f'*40,'baseRefName':'main'})
  if args[:2]==['gh','api']:return '| 1 | synthetic-only / fixture | t | 0 | 0 | 0 | 0 | '+status+' | 1/5 | | | |\n'
  raise RuntimeError('Status-only gate tried source/operational read '+repr(args))
 ns=dict(m.__dict__,P=T,inventory=synthetic_inventory,state=state,skipped=skipped,run=next_read);exec(loopcode,ns);need(len(skipped)==1 and skipped[0]['math_source_read'] is False and not any(a[0]=='git' for a in calls),'Noneligible gate leaked source');rows.append({'case':'actual_status_only_skip_'+state_+'_'+str(draft)+'_'+status,'passed':True,'math_source_read':False})
# Main-base drift for an otherwise eligible synthetic next target fails before snapshot/source.
state={'eligible_prs':[939],'completed_prs':[]};calls=[]
def wrongbase_read(args):
 calls.append(args)
 if args[:3]==['gh','pr','view']:return json.dumps({'number':939,'state':'OPEN','isDraft':True,'headRefOid':'f'*40,'baseRefName':'other'})
 if args[:2]==['gh','api']:return '| 1 | synthetic-only / fixture | t | 0 | 0 | 0 | 0 | claimed_solved | 1/5 | | | |\n'
 raise RuntimeError('Unexpected next-target read')
ns=dict(m.__dict__,P=T,inventory=[{'number':939,'entries':[{'id':'synthetic-only'}]}],state=state,skipped=[],run=wrongbase_read)
try:exec(loopcode,ns)
except RuntimeError as e:need('base changed' in str(e),'unrelated next gate rejection');rows.append({'case':'actual_next_eligible_wrongbase','rejected':True})
else:raise RuntimeError('Wrongbase target passed')
# Literal parser and already-finished early-return logic; no external metadata/main action.
need(m.raw_json_values(b'{"x" : {"nested":[1,{"brace":"}"}]}, "30003634":{}}')['x']=='"x" : {"nested":[1,{"brace":"}"}]}','literal parser');rows.append({'case':'literal_nested_state_parser','passed':True})
result={'status':'PASS','cases':len(rows),'rows':rows,'operational_mains_called':False,'real_external_calls':0,'synthetic_fixtures_only':True,'finalizer_R7_checked_separately':True}
(R/'FINALIZER_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','cases':len(rows)}))
