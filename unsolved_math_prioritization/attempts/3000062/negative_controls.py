"""Exact mathematical, whole-module hardening and fail-closed inventory controls."""
import ast,hashlib,importlib.util,json,os,stat,tempfile
from fractions import Fraction as Q
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).parent
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
class Harden(ast.NodeTransformer):
 def visit_Assert(self,node):
  return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[node.msg or ast.Constant(value='verification failed')],keywords=[]),cause=None)],orelse=[]),node)
def definitions(name):
 tree=ast.parse((ROOT/name).read_text());tree.body=[x for x in tree.body if isinstance(x,(ast.Import,ast.ImportFrom,ast.FunctionDef))];ns={};exec(compile(tree,name,'exec'),ns);return ns
def main():
 checks=[];guards=0
 for name in ['check_algorithms.py','check_robust_rounding.py']:
  old=(ROOT/'originals'/name).read_text();new=(ROOT/name).read_text();p=json.loads((ROOT/'provenance'/(name+'.json')).read_text())
  for label,text in [('original',old),('hardened',new)]:
   require(hashlib.sha256(text.encode()).hexdigest()==p[label+'_sha256'],label+' digest')
   require(ast.dump(ast.parse(text),include_attributes=True)==p[label+'_full_ast'],label+' whole-module AST')
  require(ast.unparse(ast.fix_missing_locations(Harden().visit(ast.parse(old))))+'\n'==new,'non-assert change')
  require(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(new))),'assert remains')
  for node in ast.walk(ast.parse(old)):
   if not isinstance(node,ast.Assert):continue
   for truth in [True,False]:
    guard=Harden().visit(ast.Assert(test=ast.Constant(value=truth),msg=None));m=ast.fix_missing_locations(ast.Module(body=[guard],type_ignores=[]))
    try:exec(compile(m,'<guard-control>','exec'),{})
    except AssertionError:require(not truth,'true guard rejected')
    else:require(truth,'false guard accepted')
   guards+=1
 checks.append({'test':'whole_module_AST_and_true_false_guard_controls','guards':guards,'passed':True})
 actual_guards=0
 for name in ['check_algorithms.py','check_robust_rounding.py']:
  ns=definitions(name)
  for node in ast.walk(ast.parse((ROOT/'originals'/name).read_text())):
   if not isinstance(node,ast.Assert):continue
   expression=ast.unparse(node.test)
   env=dict(ns)
   if name=='check_algorithms.py':
    if 'F(u, A)' in expression:
     env.update(A=[(1,0,2),(1,2,4),(2,1,4)],u=(2,4,4),l=(0,0,0),m=(1,2,2))
    elif 'opts' in expression:env.update(A=[(0,1,2),(0,2,2)],opts=[(2,0,0)])
    elif 'W - t' in expression:env.update(W=4,t=Q(3,2))
    else:env.update(A=[(0,1,2),(1,0,2)],x=(Q(1,2),Q(3,2)))
   else:
    env.update(A=[(0,1,2),(1,0,2)],x=(Q(501,1000),Q(1501,1000)),eta=Q(1,1000),z=(1,1))
   require(eval(compile(ast.Expression(body=node.test),'<original-predicate>','eval'),env),'original predicate positive fixture')
   for invert in [False,True]:
    import copy
    pred=copy.deepcopy(node.test)
    if invert:pred=ast.UnaryOp(op=ast.Not(),operand=pred)
    guard=Harden().visit(ast.Assert(test=pred,msg=node.msg));module=ast.fix_missing_locations(ast.Module(body=[guard],type_ignores=[]))
    try:exec(compile(module,'<actual-guard>','exec'),env)
    except AssertionError:require(invert,'valid mathematical guard failed')
    else:require(not invert,'negated mathematical predicate survived')
   actual_guards+=1
 checks.append({'test':'every_actual_source_predicate_positive_and_negated_control','guards':actual_guards,'passed':True})
 a=definitions('check_algorithms.py');b=definitions('check_robust_rounding.py');F=a['F'];good=a['good'];R=a['R'];rounded=b['rounded']
 def check(name,ok):require(ok,name);checks.append({'test':name,'passed':True})
 check('positive_source_wrong_LP_output_rejected',not good((2,0,0),[(0,1,2),(0,2,2)]) and good((0,2,2),[(0,1,2),(0,2,2)]))
 arcs=[(1,0,2),(1,2,4),(2,1,4)];check('two_cycle_midpoint_rejected',F(F((0,0,0),arcs),arcs)==(0,0,0) and not good((1,2,2),arcs))
 arcs=[(0,1,4),(1,0,4),(0,2,2),(1,2,4)];check('nonconvexity_counterexample',good((0,4,2),arcs) and good((2,2,2),arcs) and not good((1,3,2),arcs))
 arcs=[(0,1,2),(1,0,2)];x=(Q(501,1000),Q(1501,1000));check('fixed_nearest_rounding_small_residual_failure',max(abs(u-v) for u,v in zip(x,F(x,arcs)))==Q(1,500) and not good(tuple(map(R,x)),arcs))
 t=Q(1,4);check('adjustable_threshold_recovers_exact',good(tuple(rounded(z,t) for z in x),arcs))
 check('odd_weight_reflection_negative_control',R(1-Q(1,2))!=1-R(Q(1,2)))
 for K in [1,2,17]:
  arcs=[(1,0,2*K+2),(0,1,2*K)];x=(0,0)
  for j in range(K+2):
   require(x==(2*j,0),'iteration lower bound');x=F(F(x,arcs),arcs)
 check('binary_weight_iteration_lower_bound',True)
 check('loop_and_source_edges',good((2,),[(0,0,4)]) and good((0,),[]) and not good((1,),[(0,0,4)]))
 # Mutating the max to min destroys both a cover and rounding controls.
 code=(ROOT/'check_algorithms.py').read_text();tree=ast.parse(code);tree.body=[x for x in tree.body if isinstance(x,(ast.Import,ast.ImportFrom,ast.FunctionDef))]
 class Mutate(ast.NodeTransformer):
  def visit_Name(self,node):return ast.copy_location(ast.Name(id='min',ctx=node.ctx),node) if node.id=='max' else node
 mutant={};exec(compile(ast.fix_missing_locations(Mutate().visit(tree)),'<min-mutant>','exec'),mutant)
 check('min_recurrence_mutant_detected',mutant['F']((0,0),[(0,1,2)])!=(0,2))
 spec=importlib.util.spec_from_file_location('inventory',ROOT/'verify_inventory.py');inv=importlib.util.module_from_spec(spec);spec.loader.exec_module(inv)
 with tempfile.TemporaryDirectory() as td:
  td=Path(td);root=td/'root';root.mkdir();(root/'nested').mkdir()
  def reject(path):
   with patch.object(Path,'read_text',side_effect=RuntimeError('premature read')),patch.object(Path,'read_bytes',side_effect=RuntimeError('premature read')):
    try:inv.verify(path)
    except ValueError:return True
   raise RuntimeError('unsafe path accepted')
  link=td/'link';link.symlink_to(root,target_is_directory=True);check('root_symlink_before_reads',reject(link))
  for name in ['MANIFEST.json','nested/unsafe']:
   path=root/name;path.symlink_to(root);check(name+'_symlink_before_reads',reject(root));path.unlink()
   os.mkfifo(path);check(name+'_FIFO_before_reads',reject(root));check(name+'_as_root_FIFO_before_reads',reject(path));path.unlink()
  class Entry:
   name='synthetic';path=str(root/'synthetic')
   def stat(self,follow_symlinks=False):return type('Mode',(),{'st_mode':mode})()
  for mode in [stat.S_IFSOCK,stat.S_IFCHR,stat.S_IFBLK]:
   with patch.object(inv.os,'scandir',return_value=[Entry()]):require(reject(root),'special mode')
  check('synthetic_socket_device_modes_no_socket_created',True)
  (root/'MANIFEST.json').write_text(json.dumps({'files':{}}));(root/'unexpected').write_text('x')
  try:inv.verify(root)
  except ValueError:check('unexpected_regular_file_rejected',True)
  else:raise RuntimeError('extra accepted')
  (root/'MANIFEST.json').write_text(json.dumps({'files':{'unexpected':{'bytes':1,'sha256':'0'*64}}}))
  try:inv.verify(root)
  except ValueError:check('digest_tamper_rejected',True)
  else:raise RuntimeError('tamper accepted')
 print(json.dumps({'mode':'normal' if __debug__ else 'optimized','all_passed':True,'controls':checks},indent=2))
if __name__=='__main__':main()
