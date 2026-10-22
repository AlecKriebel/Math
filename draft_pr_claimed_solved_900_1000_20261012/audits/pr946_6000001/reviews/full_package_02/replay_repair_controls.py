"""Offline controls for all operational FP01 findings; no external boundaries."""
import sys
if not sys.flags.safe_path: raise RuntimeError('Use -I or -P')
from pathlib import Path
import argparse, copy, datetime, hashlib, json, shutil, tempfile, contextlib, io, types
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';W=A/'reviews/full_package_01'
parser=argparse.ArgumentParser();parser.add_argument('--core',required=True);parser.add_argument('--output',required=True);args=parser.parse_args()
source=Path(args.core);b=source.read_bytes();N={'__name__':'_offline_guard_repair_','__file__':str(P/'accept_pr946.py')};exec(compile(b,str(source),'exec'),N)
def forbidden(*a,**k):raise RuntimeError('Forbidden external boundary')
N['run']=forbidden;N['blob']=forbidden;N['remote_main']=forbidden
D=A/'preprint/reviewed_candidates/candidate01';N['D']=D
F=json.loads((D/'FREEZE.json').read_text());FP=hashlib.sha256((D/'FREEZE.json').read_bytes()).hexdigest();AUTH=json.loads((W/'AUTHENTICATION_START.json').read_text());COLD=json.loads((W/'COLD_REPLAY.json').read_text());expected={k:{x:v for x,v in p.items() if x not in ['archive_mode','disk_and_archive_match']} for k,p in AUTH['originals'].items()}
N['archive_check']=lambda *a,**k:{'payload_files':219,'zip_members':220}
def encode(j):return (json.dumps(j,indent=2)+'\n').encode()
def fp(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
cases=[]
with tempfile.TemporaryDirectory(prefix='root_guard_',dir=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001/reviews/full_package_02/private')) as temp:
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
 def reject(label, supplied):
  try:N['review_check'](supplied,F,FP,{},expected)
  except (RuntimeError,KeyError,TypeError,ValueError,OSError) as error:cases.append({'case':label,'rejected':True,'reason':str(error)[:170]})
  else:raise RuntimeError('Invalid case accepted: '+label)
 reject('omitted_sealed_adverse_round03',specs[:2]);reject('all_three_adverse_rounds',specs)
 third=fix/'reviews/full_package_03';holding=fix/'held03';third.rename(holding)
 valid=N['review_check'](specs[:2],F,FP,{},expected);assert len(valid[0])==2
 cases.append({'case':'complete_clean_two_round_history','accepted':True})
 for name,kind in [('full_package_03','unfinished'),('full_package_bad','malformed'),('FULL_PACKAGE_03','mixedcase'),('full_package_00','zero'),('full_package_001','extra_digit'),('full_package_04','gap'),('full_package_03','symlink')]:
  entry=fix/'reviews'/name
  if kind=='symlink':entry.symlink_to(holding,target_is_directory=True)
  else:entry.mkdir()
  reject('extra_'+kind+'_round',specs[:2])
  if entry.is_symlink():entry.unlink()
  else:entry.rmdir()
 folder=fix/'reviews/full_package_02'
 for name in ['RESULT.json','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json']:
  original=(folder/name).read_bytes();obj=json.loads(original)
  keys={'RESULT.json':list(N['result_schema'].__code__.co_consts),'other':[]}
  documented={'RESULT.json':['pr','problem_id','original_pr_head','reviewer_agent_id','clean_context','full_reproducer_completed','started_utc','completed_utc','candidate_revision','candidate_pins','inspected_helper_hashes','required_issues','optional_issues','clean_for_preprint','mathematical_remaining_gap_for_stated_theorem','strongest_verified_theorem','prior_issue_resolution'],'AUTHENTICATION_START.json':['status','utc','original_pr_head','freeze_sha256','package_manifest_sha256','future_helpers','candidate_files','payloads','archive_members','originals'],'AUTHENTICATION_END.json':['status','utc','original_pr_head','freeze_sha256','package_manifest_sha256','future_helpers','candidate_files','payloads','archive_members','originals'],'COLD_REPLAY.json':['status','utc','cold_extraction','typed_float_policy_verified','historical_strict_failure_preserved','package_manifest_sha256','externally_pinned_verifier_sha256','normalized_fields_ignored','modes']}[name]
  for key in documented:
   changed=copy.deepcopy(obj);changed.pop(key);(folder/name).write_bytes(encode(changed));changed_specs=[specs[0],reseal(2)];reject(name+'_missing_'+key,changed_specs)
  mutations=[]
  if name=='RESULT.json':mutations=[('revision999',lambda j:j.update(candidate_revision=999)),('revision_bool',lambda j:j.update(candidate_revision=True)),('revision0',lambda j:j.update(candidate_revision=0)),('clean_flag_string',lambda j:j.update(clean_for_preprint='true')),('resolution_list',lambda j:j.update(prior_issue_resolution=[])),('theorem_empty',lambda j:j.update(strongest_verified_theorem=' '))]
  if name=='COLD_REPLAY.json':mutations=[('normalization_none',lambda j:j.update(normalized_fields_ignored=None)),('normalization_nonempty',lambda j:j.update(normalized_fields_ignored=['invented'])),('mode_optimization_bool',lambda j:j['modes'][0].update(observed_outer_optimization=False)),('mode_receipt_missing',lambda j:j['modes'][0].pop('receipt'))]
  for label,mutate in mutations:
   changed=copy.deepcopy(obj);mutate(changed);(folder/name).write_bytes(encode(changed));reject(name+'_'+label,[specs[0],reseal(2)])
  (folder/name).write_bytes(original);specs[1]=reseal(2)
 holding.rename(third)
 result=json.loads((third/'RESULT.json').read_text());result.update(required_issues=[],clean_for_preprint=True);(third/'RESULT.json').write_bytes(encode(result));specs[2]=reseal(3)
 assert len(N['review_check'](specs,F,FP,{},expected)[0])==3;cases.append({'case':'complete_clean_three_round_history','accepted':True})
 # Full finalization with all service/Git/native boundaries mocked, own temporary files only.
 effort=fix/'effort';audit=effort/'audits/pr946_6000001';audit.mkdir(parents=True);N['P']=effort;N['A']=audit;N['D']=audit/'preprint'
 for path in [effort/'README.md',effort/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']:path.write_text('Synthetic fixture only.\n')
 oldbody='reviewed original synthetic body';pub={'id':12,'doi':'10.5281/zenodo.12','record_url':'https://zenodo.org/records/12'};merge={'number':946,'state':'MERGED','baseRefName':'main','headRefOid':N['HEAD'],'mergeCommit':{'oid':'a'*40}};tracker={'updated_range':"'Math Puzzles'!A2:D2",'row':['p','','https://doi.org/10.5281/zenodo.12','note']};native={'commit':'b'*40};accepted={'exact_claim':'Synthetic theorem fixture.','full_package_reviews':[{'manifest_sha256':'1'*64},{'manifest_sha256':'2'*64}]};freeze={'pr_description_sha256':hashlib.sha256(oldbody.encode()).hexdigest(),'revision_candidate':1};published=[904,905,906,908,909,919,938]
 state={'active_pr':946,'active_problem_id':'6000001','eligible_prs':published+[946,947],'completed_prs':published,'completed_results':[{'pr':n,'outcome':'accepted_merged_preprint_published'} for n in published],'publication':'old_summary','portable_release_tooling':'old946tool','review_families':['pr946_jet'],'active_original_head':N['HEAD']};saved={};calls=[]
 N['accepted_package']=lambda c:(accepted,freeze);N['merged_gate']=lambda a,f:{};N['publication_links']=lambda *a:(pub,merge);N['native_verify']=lambda *a:{'status':'PASS','synthetic':True};N['gws']=lambda args:{'range':tracker['updated_range'],'values':[tracker['row']]}
 def load(path):
  table={audit/'TRACKER_RECEIPT.json':tracker,audit/'NATIVE_PUBLICATION_RECEIPT.json':native,effort/'CURRENT_STATE.json':state,effort/'inventory.json':[{'number':946},{'number':947}]}
  return copy.deepcopy(table[path])
 N['load']=load;N['save']=lambda path,value,**k:saved.__setitem__(path,copy.deepcopy(value));N['gate_next']=lambda inventory,st:([],{'number':947,'problem_id':'synthetic_next','headRefOid':'c'*40});counter=[0]
 def view():
  counter[0]+=1
  return {**merge,'body':oldbody if counter[0]==1 else (audit/'PR_PUBLISHED_BODY.md').read_text(),'title':'old' if counter[0]==1 else '6000001: accepted global Hessian construction and published preprint'}
 N['pr_view']=view;oldrun=N['subprocess'].run;N['subprocess'].run=lambda argv,**kwargs:calls.append(argv) or types.SimpleNamespace(returncode=0,stdout='mock',stderr='')
 try:
  with contextlib.redirect_stdout(io.StringIO()):N['finalize'](types.SimpleNamespace(),{})
 finally:N['subprocess'].run=oldrun
 out=saved[effort/'CURRENT_STATE.json'];assert out['active_pr']==947 and 946 in out['published_prs'] and 'portable_release_tooling' not in out and out['publication']=='_'.join('PR'+str(n) for n in published+[946])+'_published_tracker_native_ledgers_verified';cases.append({'case':'full_finalize_refreshes_summary_clears_prior_tooling_and_selects_next','accepted':True})
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','core_sha256':hashlib.sha256(b).hexdigest(),'cases':cases,'controls':len(cases),'required_and_optional_operational_findings':['FP01-OPS-001','FP01-OPS-002','FP01-OPS-003'],'external_actions':0,'synthetic_proof_verdicts_only':True,'new_proof_responses':0};Path(args.output).write_bytes(encode(report));print(json.dumps({'status':'PASS','controls':len(cases),'core_sha256':report['core_sha256'],'external_actions':0}))
