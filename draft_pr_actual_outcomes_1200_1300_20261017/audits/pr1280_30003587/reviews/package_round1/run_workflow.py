from pathlib import Path
import importlib.util,json,datetime,sys,os,shutil
H=Path(__file__).resolve().parent; A=H.parent.parent
p=A/'publication/workflow_regression.py'; s=importlib.util.spec_from_file_location('actual_frozen_workflow',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.REPORT_ROOT=H
# Resource-only lifecycle wrapper: release only finished, owned fixture trees.
# It preserves every actual frozen function and all test predicates/results.
cleanup_records=[]
def release(path):
 resolved=path.resolve();relative=resolved.relative_to((H/'_local').resolve())
 if not relative.parts or not relative.parts[0].startswith('synthetic-offline-'):
  raise RuntimeError('Refuse cleanup outside this run own disposable fixtures')
 shutil.rmtree(resolved);cleanup_records.append(relative.as_posix())
identity_original=m.identity_matrix
def identity_owned(folder):
 result=identity_original(folder);release(folder);return result
m.identity_matrix=identity_owned
coordinator_original=m.coordinator_case
def coordinator_owned(f,case):
 result=coordinator_original(f,case);release(f['audit'].parents[2]);return result
m.coordinator_case=coordinator_owned

start=datetime.datetime.now(datetime.timezone.utc).isoformat();result=m.worker();out={'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimization':sys.flags.optimize,'actual_frozen_program':str(p),'result':result,'fixture_lifecycle_cleanup':cleanup_records}
(H/('_local/WORKFLOW_'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps({'status':result['status'],'optimization':sys.flags.optimize,'completed_utc':out['completed_utc']}))
