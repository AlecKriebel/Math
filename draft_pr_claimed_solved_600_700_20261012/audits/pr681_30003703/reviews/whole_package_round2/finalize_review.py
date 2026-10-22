"""Final independent pins, toy-tree inspection, evidence consistency and freeze."""
import datetime as dt,hashlib,json,os,stat,subprocess,sys
from pathlib import Path
R=Path(__file__).absolute().parent;A=R.parent.parent;repo=A.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(v,label):
 if not v:raise RuntimeError(label)
def write(name,value):
 (R/name).write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')
now=lambda:dt.datetime.now(dt.timezone.utc).isoformat()
checks={}
for stem in ['PACKAGE_REPLAY','MATH_CONTROLS','CAPSULE_CONTROLS','OPERATIONS_CONTROLS','KIT_CONTROLS']:
 a=json.loads((R/(stem+'.normal.json')).read_bytes());b=json.loads((R/(stem+'.optimized.json')).read_bytes())
 need(a['status']==b['status']=='PASS',stem)
 if stem in ['PACKAGE_REPLAY','MATH_CONTROLS','CAPSULE_CONTROLS']:need(a==b,stem+' mode equality')
 else:need(a['checks']==b['checks'],stem+' case/outcome equality')
 checks[stem]={'status':'PASS','checks_per_mode':a.get('count'),'case_inventory_mode_equality':True}
need(json.loads((R/'OPERATIONS_CONTROLS.normal.json').read_bytes())['count']==72,'operations count')
need(json.loads((R/'KIT_CONTROLS.normal.json').read_bytes())['count']==17,'kit count')
# Independently inspect every retained proposed tree from both fresh operation runs.
qa=[]
for mode in ['NORMAL','OPT']:
 for p in sorted((R/'tmp'/('FAKE_FIXTURE_'+mode)).glob('f*/toyrepo/program/audits/pr681_30003703/INTEGRATION_PREPARED_RECEIPT.json')):
  record=json.loads(p.read_bytes());toy=p.parents[3]
  need(toy.name=='toyrepo'and toy.is_relative_to(R/'tmp'),'toy path')
  env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_OBJECT_DIRECTORY=record['object_directory'],GIT_ALTERNATE_OBJECT_DIRECTORIES=str(toy/'.git/objects'))
  def git(*args):return subprocess.check_output(['git',*args],cwd=toy,env=env,stderr=subprocess.PIPE)
  def entries(tree):
   result={}
   for line in git('ls-tree','-r','-z',tree).split(b'\0'):
    if line:
     details,name=line.split(b'\t',1);result[name.decode()]=details.decode()
   return result
  before,after=entries(record['main_base']),entries(record['tree'])
  for name,entry in before.items():
   if name!='unsolved_math_prioritization/QUEUE.md':need(after[name]==entry,'unrelated tree entry changed')
  for n,h in record['attempt_sha256'].items():
   path='unsolved_math_prioritization/attempts/30003703/'+n
   need(after[path].startswith('100644 blob ')and sha(git('show',record['tree']+':'+path))==h,'native proposed-tree pin')
  for n,h in record['publication_sha256'].items():
   path='unsolved_math_prioritization/publications/30003703/'+n
   need(after[path].startswith('100644 blob ')and sha(git('show',record['tree']+':'+path))==h,'publication proposed-tree pin')
  qa.append({'mode':mode,'fixture':str(p.relative_to(R)),'tree':record['tree'],'native_files':len(record['attempt_sha256']),'publication_files':len(record['publication_sha256']),'unrelated_base_entries_preserved':len(before)-1,'scope_and_all_modes_hashes_verified':True})
need(len(qa)==10,'ten retained proposed trees expected')
write('PROPOSED_TREES_QA.json',{'status':'PASS','trees':qa,'count':len(qa),'all_transports_mocked':True})
initial=json.loads((R/'INPUT_PINS.json').read_bytes());rechecked={}
for name,pin in initial['files'].items():
 p=Path(name);need(p.is_file()and not p.is_symlink(),'regular final input '+name);b=p.read_bytes();actual={'bytes':len(b),'sha256':sha(b)}
 need(actual['bytes']==pin['bytes']and actual['sha256']==pin['sha256'],'input drift '+name)
 if 'git_blob'in pin:
  actual['git_blob']=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();actual['mode']='100644'
  need(actual['git_blob']==pin['git_blob']and stat.S_IMODE(p.stat().st_mode)==0o644,'native final mode/blob')
 rechecked[name]=actual
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
g=lambda*a:subprocess.check_output(['git',*a],cwd=repo,env=env).decode().strip()
index=repo/g('rev-parse','--git-path','index');state={'head':g('rev-parse','HEAD'),'branch':g('symbolic-ref','HEAD'),'refs':g('show-ref'),'index_sha256':sha(index.read_bytes())}
need(all(state[k]==initial['shared_git_state'][k]for k in ('head','branch','index_sha256')),'shared checkout/HEAD/index changed')
ref_drift=state['refs']!=initial['shared_git_state']['refs']
freeze_bytes=(A/'WHOLE_PACKAGE_REVIEW_INPUTS.json').read_bytes();need(sha(freeze_bytes)=='5c8ce364581641c7259f8a1bd3c3999002ea60b1e0c82b499cee0177f32632f8','input freeze changed');freeze=json.loads(freeze_bytes)
previous=(A/'reviews/whole_package_round1/VERDICT.json').read_bytes();need(sha(previous)=='4ad090e428a90fd531258bd8b5212d457fe880247feedd3f167097b80d9372c7','previous report changed')
started='2026-10-15T06:45:23+00:00';need(dt.datetime.fromisoformat(json.loads(previous)['completed_utc'])<=dt.datetime.fromisoformat(started),'not sequential')
# No fake acceptance/publication/tracker/push artifact may exist at live audit root.
pending_names=['ACCEPTED_PUBLICATION_INPUTS.json','PUBLICATION_FINAL_ACCEPTANCE.json','ZENODO_PUBLICATION_RECEIPT.json','ZENODO_POST_PUBLICATION_INSPECTION.json','TRACKER_RECEIPT.json','TRACKER_UNCONFIRMED.json','INTEGRATION_PUSH_INTENT.json','INTEGRATION_PUSHED_RECEIPT.json','FINAL_INTEGRATION_GATE.json','FINAL_TRACKER_GATE.json']
live={n:(A/n).exists()or(A/n).is_symlink()for n in pending_names}
need(not any(live.values()),'live future-action artifact unexpectedly exists; reconcile')
# Ensure all107 extracted members retain exact initial hashes/modes/inventory.
rows=json.loads((R/'ARCHIVE_INVENTORY.json').read_bytes());packet=R/'tmp/packet'
actual_names={p.relative_to(packet).as_posix()for p in packet.rglob('*')if p.is_file()}
need(actual_names=={r['path']for r in rows},'extracted inventory drift')
for row in rows:
 p=packet/row['path'];need(sha(p.read_bytes())==row['sha256']and stat.S_IMODE(p.stat().st_mode)==0o644,'extracted member drift')
write('FINAL_INPUT_RECHECK.json',{'schema':'pr681-round2-final-input-recheck-v1','status':'PASS','checked_utc':now(),'files':rechecked,'files_count':len(rechecked),'shared_checkout_HEAD_index_unchanged':True,'shared_refs_unchanged':not ref_drift,'shared_remote_tracking_drift_observed':ref_drift,'shared_Git_state':state,'parent_checkpoint_cause_record':'SHARED_GIT_DRIFT_OBSERVATION.json','native23_bytes_blob_modes_preserved':True,'extracted107_unchanged':True,'actual_future_action_artifacts_present_at_live_root':live,'input_freeze_sha256':sha(freeze_bytes),'previous_report_sha256':sha(previous)})
write('REPRODUCTION.json',{'schema':'pr681-round2-reproduction-v1','status':'PASS','python_executable':sys.executable,'python_version':sys.version,'checks':checks,'capsule_replay_each_outer_run':'native5/12; matrix21; freegroup20/489 paths; classical12; scope8;30 hostile cases in each internal mode','deterministic_ZIP_sha256':freeze['publication_files']['satoh_filtration_verification.zip']['sha256'],'all_actual_network_or_cloud_writes':0,'all_review_writes_confined_to':str(R),'fixtures_not_production_evidence':True})
completed=now()
with (R/'RESEARCH_LOG.md').open('a')as f:
 f.write('\n'+completed+' — Completed scientific reconstruction, primary statement/attribution checks, all107-member source/data/manifest/freeze validation and both complete capsule replays; rebuilt exact ZIP. The new mixed-characteristic probes supplement the universal proof. Completion estimate:80% of the scoped review; final operational evidence/pins then closed below.\n')
 f.write('\n'+completed+' — All72 new operational cases,17 fake-client repository-kit cases,10 fresh capsule probes and7 independent math families pass in both modes. Ten proposed Git trees independently checked. Final39 input bindings, native23, extracted107, predecessor hash and shared main/head/index rechecked unchanged. Shared origin tracking refs moved during a parent-authorized concurrent checkpoint, documented separately; this reviewer issued no shared-ref mutation. No required/optional correction; no waived finding. Completion estimate:100% of this scoped whole-package review;0% of actual publication/tracker/push/merge execution performed by this reviewer. Missing final-journal access and all future cloud facts remain limitations.\n')
report={'schema':'pr681-whole-package-review-verdict-v1','verdict':'PASS','reviewer_id':'/root/pr681_whole_package_adversary_round2','pr':681,'problem_id':'30003703','original_head':'e92320ea5979c812089780a982fbd88136a26522','started_utc':started,'completed_utc':completed,'previous_report_sha256':'4ad090e428a90fd531258bd8b5212d457fe880247feedd3f167097b80d9372c7','publication_files':freeze['publication_files'],'helper_sha256':freeze['helper_sha256'],'gate_bindings':freeze['gate_bindings'],'mandatory_findings':0,'optional_findings':0,'findings':[],'findings_waived':False,'human_peer_review':False,'AI_tools_used_extensively':True,'input_freeze_sha256':sha(freeze_bytes),'zenodo_kit':freeze['zenodo_kit'],'scientific_conclusion':'Exact two explicit counterexample families supported; no broader rank/degree/algebra or priority claim.','evidence':{'package_members':107,'strict_JSON_members':70,'capsule_Python_sources':11,'immutable_root_family_pins':28,'native_files':23,'operations_controls_each_mode':72,'operations_accepted_each_mode':12,'operations_rejections_each_mode':60,'repository_kit_controls_each_mode':17,'fresh_capsule_controls_each_mode':10,'independent_math_families_each_mode':7,'retained_proposed_trees_independently_checked':10,'deterministic_ZIP_reproduced':True,'all_final_inputs_unchanged':True,'shared_main_head_index_unchanged':True,'shared_remote_tracking_ref_drift_observed':ref_drift,'reviewer_shared_ref_mutations':0,'real_network_cloud_GitHub_tracker_writes':0},'limitations':['No independent human peer review or formal proof certificate.','Shared origin tracking refs moved during a concurrent user-authorized parent checkpoint; local main/HEAD/index and exact reviewed inputs stayed unchanged. No shared-ref mutation was issued by this reviewer.','No historical firstness, exhaustive novelty or current-openness certificate; final2017/2021 and related2025/2026 journal full-text gaps remain.','No actual staged/public metadata, DOI, binary readback, tracker append, integration push or merge has occurred in this review.','Benign repository-kit metadata normalization still requires explicit reconciliation against current exact metadata gate before actual publication.','Round1 source-pinned fixture plumbing was reused only after independent complete source/proof analysis; all new hostile cases and math probes are explicit.'],'publication_allowed_by_this_verdict_alone':False}
write('VERDICT.json',report)
files={}
for p in sorted(R.iterdir()):
 if p.is_file()and p.name!='FINAL_FREEZE.json':
  b=p.read_bytes();files[p.name]={'bytes':len(b),'sha256':sha(b)}
write('FINAL_FREEZE.json',{'schema':'pr681-round2-final-freeze-v1','completed_utc':completed,'reviewer_id':report['reviewer_id'],'files':files,'tmp_excluded':True,'mandatory_findings':0,'optional_findings':0,'findings_waived':False})
print(json.dumps({'status':'PASS','completed_utc':completed,'verdict_sha256':sha((R/'VERDICT.json').read_bytes()),'freeze_sha256':sha((R/'FINAL_FREEZE.json').read_bytes()),'frozen_files':len(files)}))
