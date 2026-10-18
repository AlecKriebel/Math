#!/usr/bin/env python3
"""Serial isolated current-source workflow challenges, no production services."""
from pathlib import Path
import datetime,importlib.util,inspect,json,os,socket,subprocess,sys,tempfile,time
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;A=R.parent.parent
spec=importlib.util.spec_from_file_location('round1_targeted_frozen_workflow',A/'publication/workflow_regression.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.REPORT_ROOT=R/'_local/workflow_tooling';scratch=m.REPORT_ROOT/'_local';scratch.mkdir(parents=True,exist_ok=True);os.environ['TMPDIR']=str(scratch);tempfile.tempdir=str(scratch)
def blocked_socket(*args,**kwargs):raise RuntimeError('External sockets forbidden in package review')
socket.socket.connect=blocked_socket
oldrun=subprocess.run;oldoutput=subprocess.check_output
def check(args):
 if isinstance(args,(list,tuple)) and args and Path(str(args[0])).name in {'gh','gws','git'}:raise RuntimeError('Unmocked external service/Git command forbidden: '+str(args[0]))
def run(args,*a,**kw):check(args);return oldrun(args,*a,**kw)
def output(args,*a,**kw):check(args);return oldoutput(args,*a,**kw)
subprocess.run=run;subprocess.check_output=output
out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':sys.flags.optimize,'runtime_override':'Only REPORT_ROOT redirected in memory to reviewer scratch; source unmodified.','external_socket_and_direct_service_subprocess_guards':True,'groups':{}}
def save(): (R/('TARGETED_WORKFLOW_'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(out,indent=2)+'\n')
with tempfile.TemporaryDirectory(prefix='serial-ready-',dir=scratch) as tmp:
 f=m.fixture(Path(tmp)/'main');out['groups']['preimport']=m.preimport_controls(f);p,t,pub=m.publication_and_tracker_controls(f);out['groups']['tracker_and_public']=pub;out['groups']['updater']=m.update_controls(f,p,t);out['groups']['ready']=m.ready_controls(f);save()
if '--postmerge' in sys.argv:
 with tempfile.TemporaryDirectory(prefix='serial-postmerge-',dir=scratch) as tmp:
  f=m.fixture(Path(tmp)/'main');p,t,pub=m.publication_and_tracker_controls(f);m.update_controls(f,p,t);selected={'baseline','doi_fallback_valid','wrong_gid_same_title','missing_gid','duplicate_designated_gid','wrong_title','bad_headers','missing_row','range_wrong','checkout_wrong','merge_parent_wrong','merge_single_parent','merge_three_parents','live_base_wrong','live_base_missing','public_false','public_identity_false','public_id_wrong','public_doi_wrong','doi_unresolved','doi_wrong_status','state_current_wrong','state_eligible_count_wrong','state_completed_duplicate','state_publications_duplicate'}|{'wrong_cell_'+str(i) for i in range(4)}|{'merged_blob_'+str(i) for i in range(13)}|{'duplicate_aliasHyphen_'+str(i) for i in range(4)};source=inspect.getsource(m.postmerge_controls);source=source.replace('for case in cases:', 'for case in [case for case in cases if case in ROUND1_SELECTED_CASES]:');namespace=dict(m.__dict__,ROUND1_SELECTED_CASES=selected);exec(compile(source, str(R/'run_targeted_workflow.py')+':selected_postmerge', 'exec'),namespace);out['groups']['postmerge']=namespace['postmerge_controls'](f);out['groups']['postmerge']['subset_selection_only']=sorted(selected);save()
if '--coordinator' in sys.argv:
 cases=['successful_publish','uncertain_stage_known_id_recovery','normalization_between_inspect_and_POST','wrong_id_first_fresh_inspection','wrong_id_second_fresh_inspection','uncertain_then_published_recovery']+['server_field_'+name for name in sorted(f['context']['metadata'])]
 out['groups']['coordinator']=[]
 for case in cases:
  with tempfile.TemporaryDirectory(prefix='serial-coordinator-',dir=scratch) as tmp:
   f=m.fixture(Path(tmp)/'main');out['groups']['coordinator'].append(m.coordinator_case(f,case));save()
out['status']='PASS';out['completed_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save();print('PASS mode',sys.flags.optimize, 'groups',list(out['groups']))
