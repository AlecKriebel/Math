from pathlib import Path
import sys,os,subprocess,importlib.util,json,tempfile,datetime,traceback,shutil,copy,inspect
F=Path(__file__).resolve().parent;A=F.parent.parent;P=A/'publication';scratch=F/'_local/workflow_tooling';scratch.mkdir(parents=True,exist_ok=True)
os.chdir(F)
sys.dont_write_bytecode=True;os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(scratch));tempfile.tempdir=str(scratch)
def under(raw):
 if isinstance(raw,int):return True
 try:return Path(raw).absolute().is_relative_to(F)
 except TypeError:return False
def audit(event,args):
 if event in ['socket.connect','socket.connect_ex','socket.bind','socket.getaddrinfo']:raise RuntimeError('REVIEW BLOCKED NETWORK '+event)
 if event=='subprocess.Popen':
  exe,argv=args[0],args[1]
  if Path(exe).resolve()!=Path(sys.executable).resolve() and not under(exe):raise RuntimeError('REVIEW BLOCKED SERVICE/GIT SUBPROCESS '+repr(argv))
  if Path(exe).resolve()==Path(sys.executable).resolve():
   scripts=[a for a in argv[1:] if isinstance(a,str) and a.endswith('.py')]
   if not scripts or not all(under(a) for a in scripts):raise RuntimeError('REVIEW BLOCKED PYTHON OUTSIDE F '+repr(argv))
 if event=='open':
  path,mode,flags=args
  if (isinstance(mode,str) and any(m in mode for m in 'wax+')) or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
   if not under(path):raise RuntimeError('REVIEW BLOCKED OUTSIDE WRITE '+str(path))
 if event in ['os.mkdir','os.remove','os.rmdir','os.chmod','os.symlink'] and not under(args[0] if event!='os.symlink' else args[1]):raise RuntimeError('REVIEW BLOCKED OUTSIDE MUTATION '+event+' '+str(args))
 if event in ['os.rename','os.replace'] and (not under(args[0]) or not under(args[1])):raise RuntimeError('REVIEW BLOCKED OUTSIDE RENAME')
sys.addaudithook(audit)
spec=importlib.util.spec_from_file_location('round2_current_workflow',P/'workflow_regression.py');w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w);w.REPORT_ROOT=F
results=[]
def run(label,fn):
 root=scratch/label
 try:
  f=w.fixture(root);out=fn(f);results.append({'label':label,'status':'PASS','result':out})
 except BaseException:
  results.append({'label':label,'status':'FAIL','traceback':traceback.format_exc()});raise
 finally:
  if root.exists():shutil.rmtree(root)
def ready(f):
 pub,tracker,public=w.publication_and_tracker_controls(f);update=w.update_controls(f,pub,tracker);pre=w.preimport_controls(f);r=w.ready_controls(f)
 return {'public_tracker':public,'update':update,'preimport':pre,'ready':r}
def coordinator(f,case):return w.coordinator_case(f,case)
try:
 group=sys.argv[1]
 if group=='ready':run('ready_OO',ready)
 elif group=='coordinator':
  for case in ['successful_publish','uncertain_stage_known_id_recovery','normalization_between_inspect_and_POST','wrong_id_first_fresh_inspection','wrong_id_second_fresh_inspection','uncertain_then_published_recovery']+['server_field_'+k for k in ['title','upload_type','publication_type','description','creators','access_right','license','version','publication_date','keywords','related_identifiers']]:run('coordinator_'+case,lambda f,case=case:coordinator(f,case))
 elif group=='postmerge':
  selected=['baseline','doi_fallback_valid','wrong_gid_same_title','duplicate_designated_gid','wrong_cell_1','range_wrong','merge_parent_wrong','live_base_wrong','live_base_missing','public_id_wrong','doi_wrong_status','state_eligible_count_wrong','state_completed_duplicate','state_publications_duplicate','merged_blob_12','duplicate_aliasMixed_1','unrelated_nearTrailingLetter_1']
  helper=inspect.getsource(w.postmerge_controls)
  marker='    for case in cases:'
  if helper.count(marker)!=1:raise RuntimeError('ambiguous harness loop')
  helper=helper.replace(marker,'    cases='+repr(selected)+'\n'+marker)
  exec(compile(helper,'<round2_selected_postmerge_harness>','exec'),w.__dict__)
  def selected_postmerge(f):
   pub,tracker,_=w.publication_and_tracker_controls(f);w.update_controls(f,pub,tracker)
   out=w.postmerge_controls(f)
   if len(out['cases'])!=len(selected):raise RuntimeError('selected count differs')
   return {'selected_cases':selected,'actual_complete_postmerge_main':out,'only_harness_case_list_selected_in_memory':True}
  run('postmerge_OO_selected17',selected_postmerge)
 elif group=='schemas':
  run('schema',lambda f:{'explicit_current_correction':w.correction_controls(f),'source_and_portable':w.context_and_portable_controls(f),'review_gate':w.review_controls(f),'document_assurance':w.document_controls(f)})
 else:raise ValueError('unknown group')
finally:
 print(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimization':sys.flags.optimize,'results':results,'scope':'Fresh serial, isolated targeted fixture runs on exact deployed code; actual source loaded, in-memory REPORT_ROOT overridden to F. Real socket activity and outside writes, direct Git/gh/gws subprocesses blocked. Synthetic compiler/pdfinfo/service/client/Git responses only. Fixtures deleted after each group. No actual production action.'},indent=2))
