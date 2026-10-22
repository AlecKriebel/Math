"""Offline controls for all operational FP01 findings; no external boundaries."""
import sys
if not sys.flags.safe_path: raise RuntimeError('Use -I or -P')
from pathlib import Path
import argparse, copy, datetime, hashlib, json, shutil, tempfile, contextlib, io, types
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';W=A/'reviews/full_package_01'
parser=argparse.ArgumentParser();parser.add_argument('--core',required=True);parser.add_argument('--output',required=True);parser.add_argument('--expect-defect',action='store_true');args=parser.parse_args()
source=Path(args.core);b=source.read_bytes();N={'__name__':'_offline_guard_repair_','__file__':str(P/'accept_pr946.py')};exec(compile(b,str(source),'exec'),N)
# Legacy minimal transport fixtures; new full-current capture tested separately.
N['accepted_state_check']=lambda *args,**kwargs:None
def forbidden(*a,**k):raise RuntimeError('Forbidden external boundary')
N['run']=forbidden;N['blob']=forbidden;N['remote_main']=forbidden
D=A/'preprint/reviewed_candidates/candidate01';N['D']=D
F=json.loads((D/'FREEZE.json').read_text());FP=hashlib.sha256((D/'FREEZE.json').read_bytes()).hexdigest();AUTH=json.loads((W/'AUTHENTICATION_START.json').read_text());COLD=json.loads((W/'COLD_REPLAY.json').read_text());expected={k:{x:v for x,v in p.items() if x not in ['archive_mode','disk_and_archive_match']} for k,p in AUTH['originals'].items()}
N['archive_check']=lambda *a,**k:{'payload_files':219,'zip_members':220}
def encode(j):return (json.dumps(j,indent=2)+'\n').encode()
def fp(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
cases=[]
with tempfile.TemporaryDirectory(prefix='root_guard_',dir=A/'private') as temp:
 fix=Path(temp);N['A']=fix;(fix/'reviews').mkdir()
 def reseal(number):
  folder=fix/'reviews'/f'full_package_{number:02d}'
  data={p.name:p.read_bytes() for p in folder.iterdir() if p.name!='MANIFEST.json'}
  raw=encode({'files':{k:fp(v) for k,v in data.items()},'explicit_public_allowlist':sorted(data)});(folder/'MANIFEST.json').write_bytes(raw)
  return f'{number:02d}:'+hashlib.sha256(raw).hexdigest()
 specs=[]
 for number in range(1,4):
  folder=fix/'reviews'/f'full_package_{number:02d}';folder.mkdir();ts=[f'2026-10-15T0{number}:00:0{i}+00:00' for i in range(5)]
  auth=copy.deepcopy(AUTH);auth['utc']=ts[1];endauth=copy.deepcopy(AUTH);endauth['utc']=ts[3];cold=copy.deepcopy(COLD);cold['utc']=ts[2]
  result={'pr':946,'problem_id':'6000001','original_pr_head':N['HEAD'],'reviewer_agent_id':'synthetic_'+str(number),'clean_context':True,'full_reproducer_completed':True,'started_utc':ts[0],'completed_utc':ts[4],'candidate_revision':1,'candidate_pins':{'freeze':FP,'manifest':F['package_manifest_sha256'],'pdf':F['files']['research_note.pdf']['sha256']},'inspected_helper_hashes':F['future_helpers'],'required_issues':[] if number<3 else [{'id':'LATER-REQUIRED','summary':'Synthetic unresolved issue'}],'optional_issues':[],'clean_for_preprint':number<3,'mathematical_remaining_gap_for_stated_theorem':None,'strongest_verified_theorem':'Synthetic guard fixture, not a real theorem verdict.','prior_issue_resolution':{}}
  for name,j in [('RESULT.json',result),('AUTHENTICATION_START.json',auth),('AUTHENTICATION_END.json',endauth),('COLD_REPLAY.json',cold)]: (folder/name).write_bytes(encode(j))
  (folder/'FULL_AUDIT.md').write_text('Synthetic audit only.\n');(folder/'RESEARCH_LOG.md').write_text('Synthetic log only.\n');specs.append(reseal(number))
 # Use actual canonical-directory fixtures and external review seals; transport and Git/service boundaries mocked.
 third=fix/'reviews/full_package_03';holding=fix/'held03';third.rename(holding)
 checked,latest=N['review_check'](specs[:2],F,FP,{},expected)
 accepted={'accepted':True,'pr':946,'problem_id':'6000001','original_pr_head':N['HEAD'],
  'operations_inventory_sha256':F['operations_inventory_sha256'],'full_package_reviews':checked,
  'all_prior_required_and_optional_findings_resolved':True,'proof_gap':None,'freeze_sha256':FP,
  'files':F['files'],'future_helpers':F['future_helpers'],'exact_claim':latest['strongest_verified_theorem']}
 (fix/'ACCEPTANCE.json').write_bytes(encode(accepted));context={'inventory_sha256':F['operations_inventory_sha256']}
 N['original_check']=lambda *a:(None,expected);N['disposition_check']=lambda:{}
 N['freeze_check']=lambda *a,**k:F
 assert N['accepted_package'](context)==(accepted,F);cases.append({'case':'complete_accepted_two_round_history','accepted':True})
 def reject(label, call):
  try:call()
  except RuntimeError as error:
   if not any(text in str(error) for text in ['supplied reviews must account','file fingerprint changed','nonregular or oversized file','external review seal','accepted review records/theorem differ']):raise
   cases.append({'case':label,'rejected':True,'reason':str(error)})
  else:raise RuntimeError('Invalid case accepted: '+label)
 holding.rename(third)
 if args.expect_defect:
  assert N['accepted_package'](context)==(accepted,F)
  cases.append({'case':'DEFECT_accepted_package_accepts_later_sealed_adverse_review','defect_reproduced':True})
 else:
  for action in ['merge','tracker_append','native_write','finalize']:
   reject('later_adverse_round_blocks_'+action,lambda action=action:N[action](types.SimpleNamespace(),context))
  for action in ['stage','publish','inspect']:
   reject('later_adverse_round_blocks_kit_'+action,lambda action=action:N['zenodo'](types.SimpleNamespace(action=action),context))
  reject('later_adverse_round_blocks_accepted_package',lambda:N['accepted_package'](context))
 third.rename(holding)
 if not args.expect_defect:
  for name in ['full_package_03','full_package_bad','FULL_PACKAGE_03']:
   entry=fix/'reviews'/name;entry.mkdir();reject('post_acceptance_pending_or_malformed_'+name,lambda:N['accepted_package'](context));entry.rmdir()
  resultpath=fix/'reviews/full_package_02/RESULT.json';original=resultpath.read_bytes();resultpath.write_bytes(original+b' ');reject('previously_sealed_packet_payload_drift',lambda:N['accepted_package'](context));resultpath.write_bytes(original)
  previous=copy.deepcopy(accepted);bad=copy.deepcopy(accepted);bad['full_package_reviews'][1]['completed_utc']='2026-10-15T09:00:00+00:00';(fix/'ACCEPTANCE.json').write_bytes(encode(bad));reject('accepted_chain_record_drift',lambda:N['accepted_package'](context));(fix/'ACCEPTANCE.json').write_bytes(encode(previous))
 # Fresh real merge control: a fake ready mutation creates actual adverse03.
 # All external calls are intercepted; exact fake actual-state readback supports old code's full merge path.
 current=[{'number':946,'state':'OPEN','isDraft':True,'baseRefName':'main','headRefOid':N['HEAD'],'body':'synthetic','mergeCommit':None}];calls=[]
 N['pr_view']=lambda:copy.deepcopy(current[0]);N['premerge_gate']=lambda *a,**k:(copy.deepcopy(current[0]),'a'*40,{},expected);N['merged_gate']=lambda *a:{}
 oldrun=N['subprocess'].run
 def fake(argv,**kwargs):
  if argv[:3]==['gh','pr','ready']:
   calls.append('ready');holding.rename(third);current[0]['isDraft']=False
  elif argv[:3]==['gh','pr','merge']:
   calls.append('merge');current[0].update(state='MERGED',mergeCommit={'oid':'b'*40})
  else:raise RuntimeError('Forbidden actual command '+repr(argv))
  return types.SimpleNamespace(returncode=0,stdout='mock',stderr='')
 N['subprocess'].run=fake
 try:
  if args.expect_defect:
   with contextlib.redirect_stdout(io.StringIO()):N['merge'](types.SimpleNamespace(),context)
   assert calls==['ready','merge'];cases.append({'case':'DEFECT_post_ready_new_adverse_round_still_dispatches_merge','defect_reproduced':True,'mocked_external_dispatches':calls})
  else:
   reject('post_ready_new_adverse_round_blocks_merge_dispatch',lambda:N['merge'](types.SimpleNamespace(),context))
   assert calls==['ready'];cases.append({'case':'post_ready_merge_dispatch_count','ready':1,'merge':0})
 finally:N['subprocess'].run=oldrun
 if not args.expect_defect:
  # Structural coverage of each immediate external mutation boundary, in addition
  # to real shared-guard and post-ready behavior above. This is not a service test.
  import ast
  tree=ast.parse(b);boundaries=[]
  for node in ast.walk(tree):
   for field,value in ast.iter_fields(node):
    if type(value) is not list:continue
    for index,stmt in enumerate(value):
     if not isinstance(stmt,ast.Assign) or not isinstance(stmt.value,ast.Call):continue
     call=stmt.value;func=call.func
     if not call.args or not isinstance(call.args[0],ast.List):continue
     literals=[x.value if isinstance(x,ast.Constant) else None for x in call.args[0].elts]
     relevant=(isinstance(func,ast.Attribute) and func.attr=='run' and
       (literals[:3] in [['gh','pr','ready'],['gh','pr','merge'],['gh','pr','edit']] or literals[:2]==['git','push'] or '*kit_args' in ast.unparse(call))) or (isinstance(func,ast.Name) and func.id=='gws' and literals[:4]==['sheets','spreadsheets','values','append'])
     if relevant:
      prior=value[index-1] if index else None
      assert isinstance(prior,ast.Expr) and isinstance(prior.value,ast.Call) and isinstance(prior.value.func,ast.Name) and prior.value.func.id=='accepted_review_check',ast.unparse(stmt)
      boundaries.append(ast.unparse(call)[:180])
  assert len(boundaries)==6,boundaries;cases.append({'case':'immediate_mutation_guard_AST_coverage','guarded_dispatches':6,'boundaries':boundaries})
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'DEFECT_REPRODUCED' if args.expect_defect else 'PASS','core_sha256':hashlib.sha256(b).hexdigest(),'controls':len(cases),'cases':cases,'external_actions':0,'transport_Git_source_and_services_mocked':True,'review_directory_inventory_and_sealed_packets_real':True,'synthetic_review_verdicts_only':True,'new_proof_responses':0};Path(args.output).write_bytes(encode(report));print(json.dumps({'status':report['status'],'controls':len(cases),'core_sha256':report['core_sha256'],'external_actions':0}))
