#!/usr/bin/env python3
"""Offline R7 captured-dependency controls. Synthetic local fixtures only."""
import ast,copy,hashlib,importlib.util,json,os,shutil,sys,tempfile
from pathlib import Path
P=Path(__file__).resolve().parent;A=P/'audits/pr938_30003634';D=A/'publication'
HELPERS=['accept_pr938.py','merge_pr938.py','run_pr938_zenodo.py','append_pr938_tracker.py','update_pr938_publication_ledger.py','finalize_pr938_and_gate_next.py'];DEPENDENCY='append_pr938_tracker.py';HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
def need(ok,label):
 if not ok:raise RuntimeError(label)
def fp(path):
 raw=path.read_bytes();return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def load(path):return json.loads(path.read_text())
def save(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n')
def module():
 spec=importlib.util.spec_from_file_location('captured_finalizer_regression',P/'finalize_pr938_and_gate_next.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
rows=[]
def main():
 m0=module();need(callable(getattr(m0,'capture_reviewed_helpers',None)) and callable(getattr(m0,'load_reviewed_receipt_checker',None)),'R7 production capture/loader not implemented yet')
 tree=ast.parse((P/'finalize_pr938_and_gate_next.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='verify_completed');prefix=[]
 for node in fn.body:
  if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Attribute) and isinstance(node.value.func.value,ast.Name) and node.value.func.value.id=='m' and node.value.func.attr=='verify_receipt_links':break
  prefix.append(node)
 else:raise RuntimeError('Actual dependency-execution boundary missing')
 code=compile(ast.fix_missing_locations(ast.Module(body=prefix,type_ignores=[])),'actual_finalizer_pre_receipt_prefix','exec')
 scratch=A/'private/review04_repairs';scratch.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(dir=scratch) as td:
  root=Path(td);counter=[0]
  def fixture():
   counter[0]+=1;base=root/f'case{counter[0]:02d}';h=base/'helpers';q=base/'audit/publication';h.mkdir(parents=True);q.mkdir(parents=True)
   for name in HELPERS:shutil.copyfile(P/name,h/name)
   freeze=copy.deepcopy(load(D/'PREPUBLICATION_FREEZE.json'));freeze['future_helpers']={n:fp(h/n) for n in HELPERS}
   acc={'accepted':True,'pr':938,'problem_id':'30003634','original_pr_head':HEAD,'full_package_reviews':[{},{}],'future_helpers':freeze['future_helpers'],'files':freeze['files']}
   def bind():
    save(q/'PREPUBLICATION_FREEZE.json',freeze);acc['freeze_sha256']=fp(q/'PREPUBLICATION_FREEZE.json')['sha256'];save(base/'audit/ACCEPTANCE.json',acc)
   bind()
   for path in [q/'ZENODO_PUBLISH.json',base/'audit/PR_MERGE_RECEIPT.json',base/'audit/TRACKER_RECEIPT.json',base/'audit/NATIVE_PUBLICATION_RECEIPT.json']:save(path,{})
   m=module();m.P=h;m.A=base/'audit';m.D=q;marker=base/'MUST_NOT_EXECUTE';return m,base,h,q,freeze,acc,bind,marker
  def invoke_prefix(m):
   ns=dict(m.__dict__);exec(code,ns);return ns['m']
  def expect_reject(label,m,marker):
   try:invoke_prefix(m)
   except (RuntimeError,OSError,ValueError,KeyError) as error:
    need(not marker.exists(),label+' executed altered dependency before rejection');rows.append({'case':label,'rejected_before_dependency_execution':True,'marker_created':False,'reason':str(error)});return
   raise RuntimeError(label+' accepted adverse dependency/inventory')
  m,b,h,q,f,a,bind,marker=fixture();checker=invoke_prefix(m);need(checker.__file__==str(h/DEPENDENCY) and callable(checker.verify_receipt_links) and checker.valid_tracker_range("'Math Puzzles'!A10:D10"),'Valid captured checker not loaded');rows.append({'case':'actual_finalizer_prefix_valid_complete_inventory','passed':True,'module_source':'authenticated captured bytes'})
  for name in HELPERS:
   m,b,h,q,f,a,bind,marker=fixture();evil=('from pathlib import Path\nPath('+repr(str(marker))+').write_text("UNREVIEWED_EXECUTION")\n').encode();(h/name).write_bytes(evil+(h/name).read_bytes());expect_reject('changed_'+name,m,marker)
  m,b,h,q,f,a,bind,marker=fixture();path=h/DEPENDENCY;old=path.read_bytes();evil=('from pathlib import Path\nPath('+repr(str(marker))+').write_text("SAME_SIZE_UNREVIEWED")\n').encode();need(len(evil)<len(old),'Same-size fixture budget');path.write_bytes(evil+b'#'*(len(old)-len(evil)));expect_reject('same_size_changed_dependency_hash',m,marker)
  for kind in ['missing','symlink','directory','fifo']:
   m,b,h,q,f,a,bind,marker=fixture();path=h/DEPENDENCY;old=path.read_bytes();path.unlink()
   if kind=='symlink':outside=b/'same_expected_dependency.py';outside.write_bytes(old);path.symlink_to(outside)
   elif kind=='directory':path.mkdir()
   elif kind=='fifo':os.mkfifo(path)
   expect_reject('nonregular_or_missing_'+kind,m,marker)
  for kind in ['missing_helper','extra_helper','accepted_map_disagrees','stale_freeze','not_accepted','wrong_frozen_target','boolean_helper_size']:
   m,b,h,q,f,a,bind,marker=fixture()
   if kind=='missing_helper':f['future_helpers']=dict(f['future_helpers']);f['future_helpers'].pop('merge_pr938.py');a['future_helpers']=copy.deepcopy(f['future_helpers']);bind()
   elif kind=='extra_helper':f['future_helpers']=dict(f['future_helpers']);f['future_helpers']['../outside.py']=fp(h/DEPENDENCY);a['future_helpers']=copy.deepcopy(f['future_helpers']);bind()
   elif kind=='accepted_map_disagrees':a['future_helpers']=copy.deepcopy(a['future_helpers']);a['future_helpers'][DEPENDENCY]['sha256']='0'*64;save(b/'audit/ACCEPTANCE.json',a)
   elif kind=='stale_freeze':a['freeze_sha256']='0'*64;save(b/'audit/ACCEPTANCE.json',a)
   elif kind=='wrong_frozen_target':f['pr']=939;bind()
   elif kind=='boolean_helper_size':f['future_helpers'][DEPENDENCY]['bytes']=True;a['future_helpers']=copy.deepcopy(f['future_helpers']);bind()
   else:a['accepted']=False;save(b/'audit/ACCEPTANCE.json',a)
   expect_reject(kind,m,marker)
  for kind in ['overwrite','replace_symlink','replace_fifo']:
   m,b,h,q,f,a,bind,marker=fixture();capture=m.capture_reviewed_helpers
   def after_auth(accepted,capture=capture,kind=kind,h=h,b=b,marker=marker):
    frozen,verified=capture(accepted);path=h/DEPENDENCY;evil=('from pathlib import Path\nPath('+repr(str(marker))+').write_text("POST_AUTH_DRIFT_EXECUTED")\n').encode()
    if kind=='overwrite':path.write_bytes(evil)
    else:
     path.unlink()
     if kind=='replace_symlink':outside=b/'unreviewed_after_auth.py';outside.write_bytes(evil);path.symlink_to(outside)
     else:os.mkfifo(path)
    return frozen,verified
   m.capture_reviewed_helpers=after_auth;checker=invoke_prefix(m);need(not marker.exists() and callable(checker.verify_receipt_links) and checker.__file__==str(h/DEPENDENCY),kind+' loaded path again after auth');rows.append({'case':'post_auth_'+kind,'captured_original_bytes_executed_only':True,'marker_created':False})
  m,b,h,q,f,a,bind,marker=fixture();path=h/DEPENDENCY;path.write_bytes(path.read_bytes()+b'\nR7_CAPTURED_DEBUG=__debug__\n');f['future_helpers'][DEPENDENCY]=fp(path);a['future_helpers']=copy.deepcopy(f['future_helpers']);bind();checker=invoke_prefix(m);need(checker.R7_CAPTURED_DEBUG is True,'Captured dependency inherited optimized execution');rows.append({'case':'captured_dependency_compiled_without_optimization','passed':True})
 print(json.dumps({'status':'PASS','actual_parent_optimization':sys.flags.optimize,'cases':len(rows),'rows':rows,'actual_verify_completed_prefix_executed_before_first_receipt_call':True,'synthetic_local_receipts_only':True,'real_service_Git_or_operational_main_actions':False,'new_proof_search_responses':0},indent=2))
if __name__=='__main__':main()
