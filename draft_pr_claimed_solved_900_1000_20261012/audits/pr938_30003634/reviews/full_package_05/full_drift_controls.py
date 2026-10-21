"""Actual complete verifier under postauthentication drift; no service work."""
import copy,importlib.util,json,os,shutil,sys,tempfile
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parents[3];rows=[]
def need(v,s):
 if not v:raise RuntimeError(s)
with tempfile.TemporaryDirectory(dir=R/'private',prefix='full_drift_') as td:
 root=Path(td)
 for kind in ['overwrite','symlink','fifo']:
  t=root/kind;shutil.copytree(R/'private/finalizer_complete_v2',t);h=t/'helpers';h.mkdir()
  for n in json.loads((t/'publication/PREPUBLICATION_FREEZE.json').read_text())['future_helpers']:shutil.copyfile(P/n,h/n)
  spec=importlib.util.spec_from_file_location('review05fulldrift',P/'finalize_pr938_and_gate_next.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.P=h;m.A=t;m.D=t/'publication';marker=t/'MUST_NOT_EXECUTE';capture=m.capture_reviewed_helpers;calls=[]
  def captured(accepted):
   frozen,raw=capture(accepted);path=h/'append_pr938_tracker.py';evil=('from pathlib import Path\nPath('+repr(str(marker))+').touch()\n').encode();path.unlink()
   if kind=='overwrite':path.write_bytes(evil)
   elif kind=='symlink':other=t/'evil.py';other.write_bytes(evil);path.symlink_to(other)
   else:os.mkfifo(path)
   return frozen,raw
  def forbid(*a,**k):calls.append(str(a));raise RuntimeError('REAL SERVICE BOUNDARY REACHED')
  m.capture_reviewed_helpers=captured;m.run=forbid;m.blob=forbid;m.save=forbid
  try:m.verify_completed()
  except RuntimeError as e:need('reviewed operational helper changed' in str(e),'unexpected rejection '+str(e));need(not marker.exists() and calls==[],'unreviewed or service execution');rows.append({'case':kind,'actual_complete_verifier_rejected_drift':True,'marker_created':False,'service_or_Git_calls':0})
  else:raise RuntimeError('drift accepted')
print(json.dumps({'status':'PASS','actual_parent_optimization':sys.flags.optimize,'cases':len(rows),'rows':rows,'operational_mains_called':False},indent=2))
