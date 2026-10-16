"""Close only this new authored family; no native/Git/remote or prior code execution."""
from pathlib import Path,PurePosixPath
import os,sys,stat,json,hashlib,datetime

if sys.flags.optimize or not __debug__ or os.environ.get('PYTHONOPTIMIZE','')not in ('','0'):
 raise RuntimeError('Nonoptimized actual own closure required')
P=Path(__file__).resolve().parent;A=P.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,m):
 if not ok:raise RuntimeError(m)
def raw(p):
 require(not p.is_symlink()and all(not q.is_symlink()for q in p.parents),'symlink ancestry')
 require(stat.S_ISREG(p.stat().st_mode),'regular owned file')
 return p.read_bytes()
def read(p):return json.loads(raw(p))
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def ref(p):
 b=raw(p);return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
require(P.name=='whole_current_source_first_family'and A.name=='pr45_9900007','own anchor')
require(not(P/'MANIFEST.json').exists(),'never replace own manifest')
v=read(P/'VERDICT.json');require(v['verdict']=='PASS_WHOLE_CURRENT_SCOPED_NO_MANDATORY_CORRECTION'and v['mandatory_corrections']==[]and v['future_native_acceptance_approved']is False,'scoped verdict')
require(v['reviewed_candidate_manifest_sha256']==sha(raw(A/'reviewed_candidate/MANIFEST.json'))=='d136815406dc35265a828deece080813c716c69c2bb915192e606acafdcdd4c5','same reviewed whole candidate')
captures=[]
expected={'handwritten_controls':0,'complete_whole_inspection':1,'complete_whole_inspection_v2':0,'complete_whole_inspection_v3':0,'hostile_original_controls':0,'math_falsifier_indices':0,'independent_inspection_falsifier':0,'inspection_falsifier_failed_guard_replay':1}
for label,code in expected.items():
 d=P/'actual_runs'/label;cap=read(d/'CAPTURE.json')
 require(cap['exit_code']==code and type(cap['exit_code'])is int,'own actual outcome')
 require(type(cap['child_pid'])is int and cap['child_pid']>0 and type(cap['operator_pid'])is int,'own PIDs')
 require(cap['source_unchanged']is True and cap['operator_unchanged']is True,'own sources unchanged')
 require(sha(raw(d/'prelaunch_source.py'))==cap['source_sha256']and sha(raw(d/'prelaunch_operator.py'))==cap['operator_sha256'],'own prelaunch source hashes')
 for channel in ['stdout','stderr']:
  z=cap[channel];b=raw(Path(z['path']));require(len(b)==z['bytes']and sha(b)==z['sha256'],'whole own stream')
 require(datetime.datetime.fromisoformat(cap['start_utc'])<=datetime.datetime.fromisoformat(cap['end_utc']),'own actual clocks')
 captures.append({'label':label,**ref(d/'CAPTURE.json'),'child_pid':cap['child_pid'],'operator_pid':cap['operator_pid'],'exit_code':code})
gitcaps=[]
for d in sorted(q for q in(P/'actual_git').rglob('*')if q.is_dir()and(q/'CAPTURE.json').exists()):
 cap=read(d/'CAPTURE.json');require(cap['exit_code']==0 and cap['argv'][0]=='git','actual read-only query')
 require(cap['argv'][1]in{'show','ls-tree','diff','branch','rev-parse','merge-base'},'read-only Git role')
 require(cap['source_unchanged']is cap['operator_unchanged']is True,'Git snapshot unchanged')
 for channel in ['stdout','stderr']:
  z=cap[channel];b=raw(Path(z['path']));require(len(b)==z['bytes']and sha(b)==z['sha256'],'complete Git streams')
 require(cap['stderr']['bytes']==0,'Git stderr')
 gitcaps.append({'capture':ref(d/'CAPTURE.json'),'child_pid':cap['child_pid'],'argv':cap['argv']})
require(len(gitcaps)==137,'all genuine first/second/third Git queries retained')
for z in read(P/'inspection_falsifier/INDEPENDENT_REPORT_BINDINGS.json')['files']:
 b=raw(P/'inspection_falsifier'/z['path']);require(len(b)==z['bytes']and sha(b)==z['sha256'],'independent supplement report binding')
with(P/'RESEARCH_LOG.md').open('a')as log:
 log.write('\n'+stamp()+' — 100% assigned-audit closure checkpoint, discovery0%. Actual closure child'+str(os.getpid())+' verified all eight own control captures and137 read-only Git captures, both independent challenges and exact report bindings. Preparing sole-self manifest and full0444 normalization; final success remains the actual exit/capture outcome. No future native acceptance.\n')
files=[];dirs=[]
for q in sorted(P.rglob('*')):
 require(not q.is_symlink(),'no owned symlink')
 if q.is_dir():dirs.append({'path':q.relative_to(P).as_posix(),'mode':format(stat.S_IMODE(q.stat().st_mode),'04o')})
 else:
  b=raw(q);q.chmod(0o444);require(stat.S_IMODE(q.stat().st_mode)==0o444,'full0444')
  files.append({'path':q.relative_to(P).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':'0444'})
names={z['path']for z in files};expected_dirs={p.as_posix()for n in names for p in PurePosixPath(n).parents if p.as_posix()!='.'}
require({z['path']for z in dirs}==expected_dirs,'exact directories, no extra/empty dirs')
inventory=read(P/'EXTERNAL_INPUT_INVENTORY.json')
require(len(inventory['native_four_separately_enumerated_actual_Git_capture_records'])==4,'native4 explicit nonempty captures')
outer=A/'whole_current_source_first_closure_actual_capture';pre=read(outer/'PRELAUNCH.json')
require(pre['child_argv'][1]==str(P/'close_family.py')and pre['source_sha256']==sha(raw(P/'close_family.py'))and pre['operator_pid']==os.getppid(),'genuine own closure parent/prelaunch')
m={'schema':'pr45-whole-current-source-first-family-self-only-closure/v1','created_utc':stamp(),'actual_closure_child_pid':os.getpid(),'actual_closure_parent_pid':os.getppid(),'self_excluded':['MANIFEST.json'],'files_count':len(files),'files':files,'directories':dirs,'root_mode':format(stat.S_IMODE(P.stat().st_mode),'04o'),'full_file_mode':'0444','no_symlinks_or_nonregular_members':True,'no_extra_or_empty_directories':True,'verdict_sha256':sha(raw(P/'VERDICT.json')),'report_sha256':sha(raw(P/'REPORT.md')),'reviewed_candidate_manifest_sha256':v['reviewed_candidate_manifest_sha256'],'current_dependency_manifest_sha256':v['current_dependency_manifest_sha256'],'actual_own_controls':captures,'actual_read_only_Git_captures':gitcaps,'external_input_inventory_sha256':sha(raw(P/'EXTERNAL_INPUT_INVENTORY.json')),'foreign_inputs_semantics':inventory['foreign_inputs_semantics'],'foreign_primary_access_OCR_cache_SQL_body_copies':False,'native_four_Git_full_stream_first_party_exception':True,'external_closure_capture_path':str(outer),'completed_external_capture_claimed_prelaunch':False,'Git_full_permission_bits_preserved':False,'Git_empty_directories_preserved':False,'local_full0444_restoration_required_after_checkout':True,'audit_completion_percent':100,'full_target_discovery_completion_percent':0,'future_native_acceptance_approved':False,'original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'novelty_certified':False,'paper_new_DOI_tracker_created':False}
body=(json.dumps(m,indent=2,ensure_ascii=False)+'\n').encode();(P/'MANIFEST.json').write_bytes(body);(P/'MANIFEST.json').chmod(0o444)
for z in files:
 q=P/z['path'];b=raw(q);require(len(b)==z['bytes']and sha(b)==z['sha256']and stat.S_IMODE(q.stat().st_mode)==0o444,'final own bytes/full modes')
require({q.relative_to(P).as_posix()for q in P.rglob('*')if q.is_file()}==names|{'MANIFEST.json'},'exact final own topology')
print(json.dumps({'schema':'pr45-whole-family-actual-closure-result/v1','status':'PASS_EXACT_SELF_ONLY_OWN_CLOSURE','actual_child_pid':os.getpid(),'actual_parent_pid':os.getppid(),'utc':stamp(),'manifest':ref(P/'MANIFEST.json'),'files_count':len(files),'actual_control_captures':len(captures),'actual_Git_captures':len(gitcaps),'full0444':True,'audit_completion_percent':100,'discovery_completion_percent':0,'future_native_acceptance_approved':False},indent=2))
