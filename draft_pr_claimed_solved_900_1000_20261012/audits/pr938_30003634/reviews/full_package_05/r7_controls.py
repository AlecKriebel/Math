"""Independent reviewer05 captured-code boundary tests; own synthetic files only."""
import ast,copy,hashlib,importlib.util,json,os,shutil,sys,tempfile
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parents[3];A=R.parents[1];D=A/'publication';rows=[]
def need(v,s):
 if not v:raise RuntimeError(s)
def fingerprint(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def imported():
 spec=importlib.util.spec_from_file_location('independent05final',P/'finalize_pr938_and_gate_next.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m0=imported();names=m0.HELPERS;freeze0=json.loads((D/'PREPUBLICATION_FREEZE.json').read_bytes())
fn=next(n for n in ast.parse((P/'finalize_pr938_and_gate_next.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='verify_completed');prefix=[]
for n in fn.body:
 if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='verify_receipt_links':break
 prefix.append(n)
code=compile(ast.fix_missing_locations(ast.Module(body=prefix,type_ignores=[])),'actual05pre_execution_boundary','exec')
with tempfile.TemporaryDirectory(dir=R/'private',prefix='r7_') as td:
 root=Path(td);number=0
 def fixture():
  global number
  number+=1;t=root/str(number);h=t/'helpers';q=t/'audit/publication';h.mkdir(parents=True);q.mkdir(parents=True)
  for n in names:shutil.copyfile(P/n,h/n)
  f=copy.deepcopy(freeze0);a={'accepted':True,'pr':938,'problem_id':'30003634','original_pr_head':m0.HEAD}
  def bind():
   f['future_helpers']={n:fingerprint(h/n) for n in names};write(q/'PREPUBLICATION_FREEZE.json',f);a['future_helpers']=copy.deepcopy(f['future_helpers']);a['freeze_sha256']=fingerprint(q/'PREPUBLICATION_FREEZE.json')['sha256'];write(t/'audit/ACCEPTANCE.json',a)
  bind()
  for p in [q/'ZENODO_PUBLISH.json',t/'audit/PR_MERGE_RECEIPT.json',t/'audit/TRACKER_RECEIPT.json',t/'audit/NATIVE_PUBLICATION_RECEIPT.json']:write(p,{})
  m=imported();m.P=h;m.A=t/'audit';m.D=q;return m,t,h,q,f,a,bind,t/'unreviewed_execution_marker'
 def invoke(m):
  ns=dict(m.__dict__);exec(code,ns);return ns['m'],ns['freeze']
 def bad(label,change):
  m,t,h,q,f,a,bind,marker=fixture();change(m,t,h,q,f,a,bind,marker)
  try:invoke(m)
  except (RuntimeError,OSError,ValueError,KeyError) as e:need(not marker.exists(),'unreviewed execution '+label);rows.append({'case':label,'rejected_before_unreviewed_execution':True,'reason':str(e)});return
  raise RuntimeError('Adverse case accepted '+label)
 m,t,h,q,f,a,bind,marker=fixture();checker,frozen=invoke(m);need(callable(checker.verify_receipt_links) and checker.valid_tracker_range("'Math Puzzles'!A2:D2") and frozen==f,'positive');rows.append({'case':'all_six_exact_and_actual_prefix_positive','passed':True})
 for name in names:
  def change(m,t,h,q,f,a,bind,marker,name=name):
   raw=(h/name).read_bytes();evil=('from pathlib import Path\nPath('+repr(str(marker))+').touch()\n').encode();(h/name).write_bytes(evil+b'#'*(len(raw)-len(evil)))
  bad('same_size_hash_change_'+name,change)
 for kind in ['missing','symlink','directory','fifo']:
  def change(m,t,h,q,f,a,bind,marker,kind=kind):
   path=h/'append_pr938_tracker.py';raw=path.read_bytes();path.unlink()
   if kind=='symlink':other=t/'same_bytes.py';other.write_bytes(raw);path.symlink_to(other)
   elif kind=='directory':path.mkdir()
   elif kind=='fifo':os.mkfifo(path)
  bad(kind,change)
 for key,val in [('accepted',False),('pr',True),('pr',939),('problem_id','wrong'),('original_pr_head','0'*40),('freeze_sha256','0'*64)]:
  bad('accepted_'+key+'_'+str(val),lambda m,t,h,q,f,a,bind,marker,key=key,val=val:(a.update({key:val}),write(t/'audit/ACCEPTANCE.json',a)))
 for kind in ['missing','extra','disagree','boolsize','frozen_target']:
  def change(m,t,h,q,f,a,bind,marker,kind=kind):
   if kind=='missing':f['future_helpers'].pop(names[-1])
   elif kind=='extra':f['future_helpers']['outside.py']=f['future_helpers'][names[0]]
   elif kind=='boolsize':f['future_helpers'][names[0]]['bytes']=True
   elif kind=='frozen_target':f['problem_id']='wrong'
   if kind!='disagree':a['future_helpers']=copy.deepcopy(f['future_helpers'])
   else:a['future_helpers'][names[0]]['sha256']='0'*64
   write(q/'PREPUBLICATION_FREEZE.json',f);a['freeze_sha256']=fingerprint(q/'PREPUBLICATION_FREEZE.json')['sha256'];write(t/'audit/ACCEPTANCE.json',a)
  bad('inventory_'+kind,change)
 for kind in ['overwrite','symlink','fifo']:
  m,t,h,q,f,a,bind,marker=fixture();capture=m.capture_reviewed_helpers
  def drift(a,capture=capture,kind=kind,h=h,t=t,marker=marker):
   frozen,raw=capture(a);path=h/'append_pr938_tracker.py';evil=('from pathlib import Path\nPath('+repr(str(marker))+').touch()\n').encode();path.unlink()
   if kind=='overwrite':path.write_bytes(evil)
   elif kind=='symlink':other=t/'evil.py';other.write_bytes(evil);path.symlink_to(other)
   else:os.mkfifo(path)
   return frozen,raw
  m.capture_reviewed_helpers=drift;checker,_=invoke(m);need(not marker.exists() and callable(checker.verify_receipt_links),'postauth load reopened '+kind);rows.append({'case':'postauth_'+kind,'only_captured_original_executed':True,'marker_created':False})
 m,t,h,q,f,a,bind,marker=fixture();path=h/'append_pr938_tracker.py';path.write_bytes(path.read_bytes()+b'\nCAPTURE_DEBUG=__debug__\n');bind();checker,_=invoke(m);need(checker.CAPTURE_DEBUG is True,'compiled optimized');rows.append({'case':'explicit_compile0_in_actual_outer','passed':True})
print(json.dumps({'status':'PASS','actual_parent_optimization':sys.flags.optimize,'cases':len(rows),'rows':rows,'actual_finalizer_prefix':True,'operational_mains_called':False,'real_external_calls':0},indent=2))
