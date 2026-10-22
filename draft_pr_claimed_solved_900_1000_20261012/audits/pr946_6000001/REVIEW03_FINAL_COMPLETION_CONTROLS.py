"""Root independent final-completion review-history controls; all external boundaries mocked."""
import sys
if not sys.flags.safe_path: raise RuntimeError('Use -I or -P')
from pathlib import Path
import argparse, copy, datetime, hashlib, json, shutil, tempfile, contextlib, io, types
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';W=A/'reviews/full_package_01'
parser=argparse.ArgumentParser();parser.add_argument('--core',required=True);parser.add_argument('--output',required=True);parser.add_argument('--expect-defect',action='store_true');args=parser.parse_args()
source=Path(args.core);b=source.read_bytes();N={'__name__':'_offline_guard_repair_','__file__':str(P/'accept_pr946.py')};exec(compile(b,str(source),'exec'),N)
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
 # The actual shared guard/accepted_package remain active. Only services/Git/transport are fixtures.
 effort=fix/'effort';effort.mkdir();N['P']=effort
 for path in [effort/'README.md',effort/'RESEARCH_LOG.md',fix/'RESEARCH_LOG.md']:path.write_text('Synthetic fixture only.\n')
 oldbody=(A/'PR_DESCRIPTION_ANCHOR.md').read_text();assert hashlib.sha256(oldbody.encode()).hexdigest()==F['pr_description_sha256']
 pub={'id':12,'doi':'10.5281/zenodo.12','record_url':'https://zenodo.org/records/12'};merge={'number':946,'state':'MERGED','baseRefName':'main','headRefOid':N['HEAD'],'mergeCommit':{'oid':'a'*40}};tracker={'updated_range':"'Math Puzzles'!A2:D2",'row':['p','','https://doi.org/10.5281/zenodo.12','note']};native={'commit':'b'*40};published=[904,905,906,908,909,919,938]
 base_state={'active_pr':946,'active_problem_id':'6000001','eligible_prs':published+[946,947],'completed_prs':published,'completed_results':[{'pr':n,'outcome':'accepted_merged_preprint_published'} for n in published],'publication':'old_summary','portable_release_tooling':'old946tool'}
 base_load=N['load'];N['merged_gate']=lambda *a:{};N['publication_links']=lambda *a:(pub,merge);N['native_verify']=lambda *a:{'status':'PASS','synthetic':True};N['gws']=lambda *a:{'range':tracker['updated_range'],'values':[tracker['row']]}
 oldrun=N['subprocess'].run
 payload_path=fix/'reviews/full_package_01/FULL_AUDIT.md';manifest_path=fix/'reviews/full_package_01/MANIFEST.json';payload_raw=payload_path.read_bytes();manifest_raw=manifest_path.read_bytes()
 for case in ['valid_completion','valid_already_finalized','adverse_during_next_status_reads','pending_during_next_status_reads','adverse_during_already_finalized_state_read','pending_during_already_finalized_state_read','payload_drift_during_next_status_reads','manifest_drift_during_next_status_reads','payload_drift_during_already_finalized_state_read','manifest_drift_during_already_finalized_state_read']:
  payload_path.write_bytes(payload_raw);manifest_path.write_bytes(manifest_raw)
  if third.exists():
   if holding.exists():third.rmdir()
   else:third.rename(holding)
  state=copy.deepcopy(base_state);saved={};views=[0];commands=[];stdout=io.StringIO()
  if case=='valid_already_finalized' or case.endswith('already_finalized_state_read'):
   state.update(active_pr=947,active_problem_id='synthetic_next',completed_prs=published+[946],completed_results=state['completed_results']+[{'pr':946,'outcome':'accepted_merged_preprint_published'}],published_prs=published+[946],publication='_'.join('PR'+str(n) for n in published+[946])+'_published_tracker_native_ledgers_verified')
   state.pop('portable_release_tooling',None)
  def inject():
   if case.startswith('pending'):third.mkdir()
   elif case.startswith('payload_drift'):payload_path.write_bytes(bytes([(payload_raw[0]+1)%256])+payload_raw[1:])
   elif case.startswith('manifest_drift'):manifest_path.write_bytes(manifest_raw+b'\n')
   else:holding.rename(third)
  def load(path):
   if path==fix/'TRACKER_RECEIPT.json':return copy.deepcopy(tracker)
   if path==fix/'NATIVE_PUBLICATION_RECEIPT.json':return copy.deepcopy(native)
   if path==effort/'CURRENT_STATE.json':
    if case.endswith('already_finalized_state_read'):
     inject()
    return copy.deepcopy(state)
   if path==effort/'inventory.json':return [{'number':946},{'number':947}]
   return base_load(path)
  N['load']=load;N['save']=lambda path,value,**k:saved.__setitem__(path,copy.deepcopy(value))
  def next_gate(*a):
   if case.endswith('next_status_reads'):
    inject()
   return [],{'number':947,'problem_id':'synthetic_next','headRefOid':'c'*40}
  N['gate_next']=next_gate
  def view():
   views[0]+=1
   recovering=case=='valid_already_finalized' or case.endswith('already_finalized_state_read')
   return {**merge,'body':oldbody if views[0]==1 and not recovering else (fix/'PR_PUBLISHED_BODY.md').read_text(),'title':'old' if views[0]==1 and not recovering else '6000001: accepted global Hessian construction and published preprint'}
  N['pr_view']=view;N['subprocess'].run=lambda argv,**kwargs:commands.append(argv) or types.SimpleNamespace(returncode=0,stdout='fake',stderr='')
  error=None
  try:
   with contextlib.redirect_stdout(stdout):N['finalize'](types.SimpleNamespace(),context)
  except RuntimeError as caught:error=str(caught)
  completion_written=effort/'CURRENT_STATE.json' in saved
  if case=='valid_completion':
   assert error is None and completion_written and saved[effort/'CURRENT_STATE.json']['active_pr']==947
   cases.append({'case':case,'accepted':True,'fresh_complete_history':True})
  elif case=='valid_already_finalized':
   assert error is None and not completion_written and 'already_finalized' in stdout.getvalue() and commands==[]
   cases.append({'case':case,'accepted':True,'completion_written':False,'external_dispatches':0})
  elif args.expect_defect:
   assert error is None
   if case.endswith('next_status_reads'):assert completion_written and 946 in saved[effort/'CURRENT_STATE.json']['completed_prs']
   else:assert 'already_finalized' in stdout.getvalue()
   # Actual shared check rejects the same filesystem immediately afterward.
   try:N['accepted_review_check'](accepted,F,context)
   except RuntimeError as caught:assert any(reason in str(caught) for reason in ('supplied reviews must account','file fingerprint changed','external review seal'))
   else:raise RuntimeError('Fixture did not create an adverse omitted round')
   cases.append({'case':case,'defect_reproduced':True,'completion_written':completion_written,'early_return_reported':'already_finalized' in stdout.getvalue(),'shared_guard_rejects_afterward':True})
  else:
   assert error is not None and any(reason in error for reason in ('supplied reviews must account','file fingerprint changed','external review seal')) and not completion_written
   assert effort/'inventory.json' not in saved and 'already_finalized' not in stdout.getvalue()
   cases.append({'case':case,'rejected':True,'completion_written':False,'inventory_written':False,'false_early_return':False,'reason':error})
 N['subprocess'].run=oldrun
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'DEFECT_REPRODUCED' if args.expect_defect else 'PASS','core_sha256':hashlib.sha256(b).hexdigest(),'controls':len(cases),'cases':cases,'actual_complete_sealed_directory_and_shared_guard_and_accepted_package_and_finalize':True,'Git_source_transport_and_services_mocked':True,'external_actions':0,'synthetic_proof_verdicts_only':True,'new_proof_responses':0};Path(args.output).write_bytes(encode(report));print(json.dumps({'status':report['status'],'controls':len(cases),'core_sha256':report['core_sha256'],'external_actions':0}))
