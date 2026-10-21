"""Prepare-only Root completion100 source freeze. Import is inert.
Run only after actual accepted merge95, exact local-five sync and genuine PR merge.
GET-only native API; writes only new owned sources, manifest and freeze journal.
No existing view, QUEUE, ref, PR, publication, tracker or Git mutation route.
"""
import argparse, copy, datetime, hashlib, importlib.util, json, os, re, stat, sys
from pathlib import Path

D=Path(__file__).absolute().parent
A=D.parent
B=A/'native_integration_preparation_01'
P=A.parents[1]
C=P.parent
CASE='draft_pr_publication_program_20260930/audits/pr207_5100044/'
HELPER_PIN={'bytes':31634,'sha256':'e850bb9adcb40db4d9949251c103677e37651f3ec3daad16219227729f7e1efc'}
M95_PIN={'bytes':159432,'sha256':'d636727bdb719b0d9acbc76e5ef7e7040a3d2e92e55f7f539601845c45d47861'}
CANDIDATE95='cd33621f1fa67d272e64ce4186bb4ccff4d4c1af'
TREE95='4e5a94115fcd1e974c7e8f9e4a3490cd726d048d'
INPUT_ACCEPT_PIN={'bytes':1846,'sha256':'668a09b14bfbed5807ab82377a8b3a34b5b5c781eb8282222f77c2edfd1cdd2e'}
FOLLOW_MANIFEST_PIN={'bytes':1062,'sha256':'51e48c0fa366ad6a6b5c83000e2b39c0149da3e5d5614eae1341ec3836ec2327'}
FOLLOW_SEAL_PIN={'bytes':935,'sha256':'23df3d20a6e00e2a71cef214ef36e55fb403a4b80f25441cef51f7fcc87f4d60'}
PATHS={
 'acceptance':'native_integration_preparation_01/ROOT_MERGE95_ACCEPTANCE_01.json',
 'pointer':'native_integration_preparation_01/ROOT_ACTUAL_MERGE95_POINTER.json',
 'sync':'native_integration_preparation_01/root_merge95_local_sync_01/LOCAL_GLOBAL_FIVE_SYNC.json',
 'original_PR_merge':'ROOT_ACTUAL_ORIGINAL_PR_MERGE_01.json',
 'plan':'root_native_integration_execution_01/MERGE95_PLAN.stdout.json',
 'verification':'native_integration_preparation_01/root_merge95_independent_verify_01/VERIFIED.json',
 'cas_intent':'root_native_integration_execution_01/MERGE95_CAS_INTENT.json',
 'cas_result':'root_native_integration_execution_01/MERGE95_CAS_TOOL_RESULT.json',
 'ref_readback':'root_native_integration_execution_01/MERGE95_REF_READBACK.json',
}

def need(ok,msg):
 if type(ok) is not bool or not ok:raise RuntimeError(msg)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def enc(value):return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def initial_read(path,wanted):
 """Only used before loading the unchanged independently accepted helper."""
 need(path.is_absolute() and path.resolve()==path,'Canonical pinned path required')
 need(type(wanted) is dict and set(wanted)=={'bytes','sha256'} and type(wanted['bytes']) is int and 0<=wanted['bytes']<=8000000 and type(wanted['sha256']) is str and re.fullmatch('[0-9a-f]{64}',wanted['sha256']) is not None,'Strict bounded pin required')
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 try:
  before=os.fstat(fd);need(stat.S_ISREG(before.st_mode) and before.st_size==wanted['bytes'],'Pinned ordinary file required')
  with os.fdopen(fd,'rb',closefd=False) as stream:raw=stream.read(8000001)
  after=os.fstat(fd);entry=path.lstat()
  need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns) and (entry.st_dev,entry.st_ino)==(after.st_dev,after.st_ino) and stat.S_ISREG(entry.st_mode),'Pinned file changed during read')
 finally:os.close(fd)
 need(pin(raw)==wanted,'Pinned file bytes changed');return raw
def load_helper():
 path=B/'native207_v2.py';initial_read(path,HELPER_PIN);need(stat.S_IMODE(path.stat().st_mode)==0o444,'Accepted helper must remain sealed')
 spec=importlib.util.spec_from_file_location('unchanged_accepted_pr207_v2',path);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h);return h
def put_new(h,path,raw):
 need(path.is_relative_to(B/'phase_completion100_sources_01') or path in (B/'COMPLETION100_INPUTS_01.json',D/'COMPLETION100_SOURCE_FREEZE_01.json'),'Source-freeze write boundary')
 missing=[];parent=path.parent
 while not parent.exists():missing.append(parent);parent=parent.parent
 need(parent.resolve()==parent and parent.is_dir(),'Canonical output ancestor')
 for directory in reversed(missing):directory.mkdir(mode=0o700);h.durable_dir(directory);h.durable_dir(directory.parent)
 need(path.parent.resolve()==path.parent,'Canonical output parent')
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
 try:
  with os.fdopen(fd,'wb',closefd=False) as stream:need(stream.write(raw)==len(raw),'Short frozen source write');stream.flush();os.fchmod(fd,0o444);os.fsync(fd)
 finally:os.close(fd)
 h.durable_dir(path.parent)

def receipts(h,control,m95):
 need(type(control['pins']) is dict and set(control['pins'])==set(PATHS),'Exactly nine named actual/operational receipt pins')
 raw={role:initial_read(A/name,h.bytepin(control['pins'][role])) for role,name in PATHS.items()}
 objects={role:h.decode(body) for role,body in raw.items()}
 a=h.acceptance(m95,M95_PIN,A/PATHS['acceptance'],control['pins']['acceptance'])
 need(a['candidate']==CANDIDATE95 and a['tree']==TREE95,'Exact actual95 candidate/tree required')
 facts=h.phase_facts('merge95')
 h.matches(objects['sync'],{'schema':'pr207-native-integration-five-sync-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'phase':'merge95','facts':facts,'candidate':CANDIDATE95,'tree':TREE95,'acceptance_pin':control['pins']['acceptance'],'manifest_pin':M95_PIN,'all_five_local_files_match_actual_checkpoint':True},'Actual95 sync receipt')
 h.matches(objects['pointer'],{'schema':'pr207-native-integration-actual-pointer-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'phase':'merge95','facts':facts,'candidate':CANDIDATE95,'tree':TREE95,'acceptance_pin':control['pins']['acceptance'],'manifest_pin':M95_PIN,'sync_path':str(A/PATHS['sync']),'sync_pin':control['pins']['sync'],'recorded_only_after_actual_ref_readback_and_exact_all_five_files':True},'Actual95 pointer')
 for obj in (objects['sync'],objects['pointer']):
  need(type(obj['facts']) is dict and set(obj['facts'])==set(facts),'Actual95 receipt fact fields');h.matches(obj['facts'],facts,'Actual95 receipt fact types')
 h.matches(objects['original_PR_merge'],{'schema':'pr207-root-actual-original-pr-merge-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'accepted':True,'original_head':h.HEAD,'original_head_tree':h.HEAD_TREE,'actual_original_PR_head':h.HEAD,'actual_original_PR_state':'closed','actual_original_PR_is_draft':False,'actual_original_PR_merged':True,'merge95_candidate':CANDIDATE95,'merge95_tree':TREE95,'actual_MAIN_observed':CANDIDATE95},'Genuine actual original PR merge proof')
 need(h.hexid(objects['original_PR_merge'].get('actual_original_PR_merge_commit')),'Actual original PR merge commit required')
 h.matches(objects['plan'],{'schema':'pr207-native-integration-plan-v1','status':'GET_ONLY_PLAN','phase':'merge95','facts':facts,'parent':m95['expected_parent'],'parents':[m95['expected_parent'],h.HEAD],'tree':TREE95,'ref_actions_performed':False},'Actual reviewed95 plan')
 h.matches(objects['verification'],{'schema':'pr207-native-integration-verification-v1','phase':'merge95','facts':facts,'parent':m95['expected_parent'],'parents':[m95['expected_parent'],h.HEAD],'candidate':CANDIDATE95,'tree':TREE95,'full_scope_verified':True,'all_selected_native_bodies_verified':True,'ref_actions_performed':False},'Actual independent95 verification')
 h.matches(objects['ref_readback'],{'schema':'pr207-root-native-ref-readback-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'phase':'merge95','expected_parent':m95['expected_parent'],'candidate':CANDIDATE95,'tree':TREE95,'parents':[m95['expected_parent'],h.HEAD],'actual_MAIN_observed':CANDIDATE95,'accepted':True},'Actual95 native ref readback')
 for role in ('cas_intent','cas_result'):need(type(objects[role]) is dict and len(raw[role])<=50000,'Narrow pinned CAS event required')
 return raw,objects,a

def current_views(h,old,objects):
 rows=objects['sync']['files'];need(type(rows) is list and len(rows)==5 and {x['path'] for x in rows}==set(h.VIEWS),'Exact five actual95 sync paths')
 for row in rows:
  need(type(row) is dict and set(row)=={'path','postimage'} and h.bytepin(row['postimage'])==pin(old[row['path']]),'Actual95 synced source byte identity')
  need(h.sealed(C/row['path'],row['postimage'])==old[row['path']],'Current local five must remain exact accepted95 postimages')

def documentary_views(h,old,proof_path,proof_pin,now):
 facts=h.phase_facts('completion100');status=h.decode(old[h.VIEWS[0]]);oldtime=status['UTC'];progress=h.decode(old[h.VIEWS[2]])
 prior_completed=progress['fully_completed_eligible_PRs'];prior_published=progress['published_PRs']
 need(len(prior_completed)==len(set(prior_completed))==49 and all(type(x) is int for x in prior_completed) and prior_completed[-1]==206 and 207 not in prior_completed,'Exact prior49 completion list')
 need(len(prior_published)==len(set(prior_published))==34 and all(type(x) is int for x in prior_published) and prior_published[-1]==207,'Exact prior34 publication list')
 changed={}
 documentary={'UTC':now,'updated_UTC':now,'current_PR':207,'current_case_percent':100,'current_publication_ready':True,'current_status':'completed_published_tracked_original_PR_merged','status':'completed_published_tracked_original_PR_merged','checkpoint_semantics':'Completion100 checkpoint records actual accepted merge95, exact merge95 local-five sync and genuine original-HEAD PR merge, alongside verified publication/tracker. The separate Root actual completion100 receipt and pointer certify this checkpoint’s native installation and exact local-five sync. No next-case intake was performed by its source freeze.','next_step':'After actual completion100 terminal checkpoint acceptance and exact locked local-five sync, numeric intake may proceed at PR208. This source freeze performs no next-case intake.','actual_original_PR_merged':True,'actual_original_PR_merge_receipt':{'path':proof_path,**proof_pin}}
 for path,obj in ((h.VIEWS[0],status),(h.VIEWS[2],progress)):
  before=copy.deepcopy(obj);obj.update(facts);obj.update(documentary)
  for alias in ('workflow_percent','case_percent'):
   if alias in obj:obj[alias]=100
  if path==h.VIEWS[2]:
   obj['fully_completed_eligible_PRs']=prior_completed+[207];obj['published_PRs']=list(prior_published);obj['fully_completed_fraction_percent']=100*50/99;obj['last_completed_DOI']='10.5281/zenodo.23428090';obj['denominator_semantics']='Dated October3 census99;50/99 is workflow completion, not novelty/discovery or current-openness certification.'
  allowed=set(facts)|set(documentary)|{'workflow_percent','case_percent'}
  if path==h.VIEWS[2]:allowed|={'fully_completed_eligible_PRs','published_PRs','fully_completed_fraction_percent','last_completed_DOI','denominator_semantics'}
  need(all(obj[k]==v for k,v in before.items() if k not in allowed),'Scientific/source/readiness/known-priority field changed')
  changed[path]=enc(obj)
 need(progress['fully_completed_eligible_PRs'][:-1]==prior_completed and progress['fully_completed_eligible_PRs'][-1]==207 and progress['published_PRs']==prior_published,'Only207 completion added; all published IDs exact')
 entry=(now+' — PR207 completion100 source freeze: actual accepted merge95 candidate '+CANDIDATE95+' and exact local-five sync verified; native original-HEAD PR207 closed/merged. Publication DOI10.5281/zenodo.23428090 and trackerA134:D134 remain verified.50completed/34published,last207,cursor208,advanceTrue,goalFalse. Completion100 terminal CAS/acceptance/local sync remains pending; no next-case intake performed. Scientific claims, known-priority attribution, native22/archive20 and whole QUEUE are unchanged.').encode()
 oldmarker=h.marker(h.phase_facts('merge95'));newmarker=h.marker(facts)
 for path in (h.VIEWS[1],h.VIEWS[3],h.VIEWS[4]):
  lines=old[path].splitlines(keepends=True);need(sum(x.rstrip(b'\r\n')==oldmarker for x in lines)==1 and old[path].count(b'<!-- PR207_NATIVE_PHASE_FACTS ')==1,'Exactly one old current95 marker')
  body=b''.join(x for x in lines if x.rstrip(b'\r\n')!=oldmarker)
  if path==h.VIEWS[3]:
   replacements={('Frozen '+oldtime+': **PR207 at95%**').encode():('Frozen '+now+': **PR207 at100%**').encode(),b'49completed/34published,last206,cursor207. Case completion and next intake remain pending. Dated workflow census99:49.49%.':b'50completed/34published,last207,cursor208. Completion100 checkpoint; native installation and exact local-five sync are certified by the separate Root actual completion100 receipt/pointer. No next-case intake performed at freeze. Dated workflow census99:50.51%.',b'Native merge and completion require actual Root receipts.':b'Actual merge95/native original-PR merge and exact local-five sync are recorded. Native completion100 installation and exact local-five sync are certified by the separate Root actual completion100 receipt/pointer.'}
   for before,after in replacements.items():need(body.count(before)==1,'Exact documentary progress phrase required');body=body.replace(before,after)
  changed[path]=body+b'\n\n'+entry+b'\n\n'+newmarker+b'\n'
 return changed,prior_completed,prior_published

def main():
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Ordinary Python -E -S -B -P required')
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--control',type=Path,required=True);ap.add_argument('--control-bytes',type=int,required=True);ap.add_argument('--control-sha256',required=True);args=ap.parse_args()
 h=load_helper();control_path=args.control.absolute();need(control_path.is_relative_to(D),'Owned separately pinned Root control required');control_pin=h.bytepin({'bytes':args.control_bytes,'sha256':args.control_sha256});control=h.decode(initial_read(control_path,control_pin))
 h.matches(control,{'schema':'pr207-root-completion100-freeze-control-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'accepted':True,'prepare_sources_only':True,'no_ref_or_existing_view_write':True,'candidate95':CANDIDATE95,'tree95':TREE95,'builder_pin':pin(h.sealed(Path(__file__).absolute()))},'Explicit Root source-freeze control')
 c,m95,old,oldpre,oldpins=h.inputs(B/'MERGE95_INPUTS_01.json',M95_PIN);need(m95['phase']=='merge95' and len(old)==311 and sum(map(len,old.values()))==2594743,'Exact311 prior selected source packet')
 raw,objects,a=receipts(h,control,m95);current_views(h,old,objects)
 for path in (B/'phase_completion100_sources_01',B/'COMPLETION100_INPUTS_01.json',D/'COMPLETION100_SOURCE_FREEZE_01.json'):need(not path.exists() and not path.is_symlink(),'Exclusive unused completion source output required')
 selected=dict(old)
 def add(target,body):
  h.rel(target);need(target.startswith(CASE),'New additions only in own native case')
  if target in selected:need(selected[target]==body,'Existing selected artifact cannot change');return
  selected[target]=body
 for role,name in PATHS.items():add(CASE+name,raw[role])
 add(CASE+'native_integration_preparation_01/MERGE95_INPUTS_01.json',initial_read(B/'MERGE95_INPUTS_01.json',M95_PIN))
 inputraw=initial_read(A/'ROOT_MERGE95_INPUTS_ACCEPTANCE_01.json',INPUT_ACCEPT_PIN);inputaccept=h.decode(inputraw);h.matches(inputaccept,{'schema':'pr207-root-merge95-source-inputs-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'accepted':True,'manifest_pin':M95_PIN,'required_repairs':[]},'Root source-input acceptance');add(CASE+'ROOT_MERGE95_INPUTS_ACCEPTANCE_01.json',inputraw)
 follow=A/'native_integration_adversary_01/merge95_manifest_followup_01';fmraw=initial_read(follow/'PUBLIC_ARTIFACT_MANIFEST.json',FOLLOW_MANIFEST_PIN);fm=h.decode(fmraw);need(fm.get('public_explicit_allowlist') is True and fm.get('no_input_or_fixture_copies_included') is True and fm.get('reviewed_operational_manifest_pin')==M95_PIN and type(fm.get('files')) is list and len(fm['files'])==4,'Exact small followup public allowlist')
 for row in fm['files']:add(CASE+'native_integration_adversary_01/merge95_manifest_followup_01/'+h.rel(row['path']),initial_read(follow/h.rel(row['path']),h.bytepin({k:row[k] for k in ('bytes','sha256')})))
 add(CASE+'native_integration_adversary_01/merge95_manifest_followup_01/PUBLIC_ARTIFACT_MANIFEST.json',fmraw);add(CASE+'native_integration_adversary_01/merge95_manifest_followup_01/FINAL_SEAL.json',initial_read(follow/'FINAL_SEAL.json',FOLLOW_SEAL_PIN))
 prepraw=initial_read(D/'PREPARATION_MANIFEST_V2.json',h.bytepin(control['preparation_manifest_pin']));prep=h.decode(prepraw);need(prep.get('public_explicit_allowlist') is True and type(prep.get('files')) is list and len(prep['files'])==4,'Exact tiny builder preparation allowlist')
 for row in prep['files']:add(CASE+D.name+'/'+h.rel(row['path']),initial_read(D/h.rel(row['path']),h.bytepin({k:row[k] for k in ('bytes','sha256')})))
 add(CASE+D.name+'/PREPARATION_MANIFEST_V2.json',prepraw);add(CASE+D.name+'/PREPARATION_SEAL_V2.json',initial_read(D/'PREPARATION_SEAL_V2.json',h.bytepin(control['preparation_seal_pin'])))
 # Only after all local actual authority/evidence sources exist do GET operations start.
 api=h.API(h.journal_new('root_completion100_freeze_get_01'),mutate=False)
 need(api('GET','git/ref/heads/main')['object']['sha']==CANDIDATE95,'Fresh MAIN must still be actual accepted95 candidate')
 commit=api('GET','git/commits/'+CANDIDATE95);need(commit.get('sha')==CANDIDATE95 and commit['tree']['sha']==TREE95 and [x['sha'] for x in commit['parents']]==[m95['expected_parent'],h.HEAD] and commit.get('message')==m95['commit_message'],'Actual95 native commit association')
 pr=h.original_pr(api,'completion100');need(objects['original_PR_merge']['actual_original_PR_merge_commit']==pr['merge_commit_sha'],'Root original-PR proof/native merge commit differs')
 h.matches(objects['ref_readback']['actual_PR'],{'state':'closed','draft':False,'merged':True,'head':h.HEAD,'merge_commit_sha':pr['merge_commit_sha']},'Native ref readback original PR facts')
 compare=api('GET','compare/'+h.HEAD+'...'+CANDIDATE95);need(compare.get('status')=='ahead' and compare['merge_base_commit']['sha']==h.HEAD,'Merged original HEAD must be actual95 ancestor')
 trees=c.NativeTrees(api)
 for path,body in old.items():need(trees.lookup(TREE95,path)==('100644','blob',c.native('blob',body)),'Every prior311 native preimage must remain exact: '+path)
 for path in h.VIEWS+(h.QUEUE,):need(h.read_blob(c,api,c.native('blob',old[path]))==old[path],'Actual95 native five/QUEUE body differs')
 h.queue_change(old[h.QUEUE],old[h.QUEUE],'completion100')
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();proofpath=CASE+PATHS['original_PR_merge'];views,priorcompleted,priorpublished=documentary_views(h,old,proofpath,control['pins']['original_PR_merge'],now);selected.update(views)
 gate95=h.decode(old[m95['gate_receipt']]);roles=copy.deepcopy(gate95['receipts']);roles['ready_PR_merge']={'path':proofpath,**control['pins']['original_PR_merge']}
 facts=h.phase_facts('completion100');gate={'schema':'pr207-root-native-phase-gates-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','UTC':now,'PR':207,'phase':'completion100','accepted':True,'original_head':h.HEAD,'facts':facts,'scientific_accepted':True,'whole_package_accepted':True,'actual_publication_verified':True,'actual_tracker_verified':True,'ready_for_merge':True,'receipts':roles,'actual_merge95_acceptance':{'path':CASE+PATHS['acceptance'],**control['pins']['acceptance']},'actual_merge95_sync':{'path':CASE+PATHS['sync'],**control['pins']['sync']},'completion100_terminal_native_acceptance_and_local_sync_pending':True,'next_case_intake_performed':False}
 gatepath=CASE+'ROOT_NATIVE_COMPLETION100_GATES_01.json';add(gatepath,enc(gate))
 need(len(selected)-len(old)<=30 and all(selected[path]==body for path,body in old.items() if path not in h.VIEWS),'Only five prior311 bodies may change; small additions only')
 rows=[]
 for path,body in sorted(selected.items()):
  pre=trees.lookup(TREE95,path)
  if path not in h.VIEWS:need(pre is None or pre==('100644','blob',c.native('blob',body)),'New artifact collides with native existing body')
  rows.append({'path':path,'source':'phase_completion100_sources_01/'+path,**pin(body),'git_blob':c.native('blob',body),'preimage':None if pre is None else dict(zip(('mode','type','sha'),pre))})
 current_views(h,old,objects);need(api('GET','git/ref/heads/main')['object']['sha']==CANDIDATE95,'MAIN changed before source freeze')
 for row in rows:put_new(h,B/row['source'],selected[row['path']])
 m={'schema':'pr207-native-integration-inputs-v1','PR':207,'phase':'completion100','anchor':h.ANCHOR,'original_head':h.HEAD,'original_head_tree':h.HEAD_TREE,'expected_parent':CANDIDATE95,'helper_pin':HELPER_PIN,'core_pin':h.CORE_PIN,'facts':facts,'files':rows,'total_files':len(rows),'total_bytes':sum(x['bytes'] for x in rows),'local_views':[{'path':path,'preimage':pin(old[path])} for path in h.VIEWS],'gate_receipt':gatepath,'commit_message':'Complete PR207 after verified publication, tracker and original submission merge'}
 manifest=B/'COMPLETION100_INPUTS_01.json';put_new(h,manifest,enc(m));h.inputs(manifest,pin(enc(m)))
 need(api('GET','git/ref/heads/main')['object']['sha']==CANDIDATE95,'MAIN changed before completion source receipt');current_views(h,old,objects)
 summary={'schema':'pr207-root-completion100-source-freeze-v1','evidence_scope':'SOURCE_FREEZE_ONLY_NOT_ACTUAL_COMPLETION_ACCEPTANCE','UTC':now,'PR':207,'parent':CANDIDATE95,'parent_tree':TREE95,'manifest_pin':pin(enc(m)),'previous_manifest_pin':M95_PIN,'control_pin':control_pin,'builder_pin':pin(h.sealed(Path(__file__).absolute())),'selected_files':len(rows),'selected_bytes':m['total_bytes'],'previous_selected_files':311,'changed_previous_paths':list(h.VIEWS),'all_other_previous_selected_bytes_unchanged':True,'prior49_completed_IDs':priorcompleted,'only_added_completed_ID':207,'published34_IDs_unchanged':priorpublished,'native22_archive20_QUEUE_unchanged':True,'all_native_preimages_checked':True,'actual95_native_and_local_receipts_verified':True,'actual_original_HEAD_PR_merged_verified':True,'completion100_terminal_acceptance_and_sync_pending':True,'no_next_case_intake_performed':True,'no_ref_or_existing_view_write':True,'facts':facts}
 put_new(h,D/'COMPLETION100_SOURCE_FREEZE_01.json',enc(summary));print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
