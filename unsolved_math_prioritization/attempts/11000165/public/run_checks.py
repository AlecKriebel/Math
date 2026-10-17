#!/usr/bin/env python3
"""Replay exact public mathematical checkers in isolated disposable copies."""
import ast,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MODES=[('normal',[]),('optimized',['-O']),('double_optimized',['-OO'])]
CHECKS=[
 ('pass1_exact_validation/verify_exact_formulas.py','pass1_exact_validation/PUBLIC_EXACT_CHECKS.json',False),
 ('pass1_genus_two/verify_homology.py','pass1_genus_two/ALGEBRA_CHECKS.json',False),
 ('pass1_constructive/verify_lattice.py','pass1_constructive/VERIFICATION.json',False),
 ('pass1_johnson_obstruction/verify_free_group.py','pass1_johnson_obstruction/FREE_GROUP_CHECK.json',True),
 ('pass1_audit/check_integral_lattice.py','pass1_audit/INTEGRAL_LATTICE_CHECK.json',False),
 ('pass1_audit/check_outer_commutator.py','pass1_audit/OUTER_COMMUTATOR_CHECK.json',False),
 ('pass1_closed_transfer/verify_integral_quotient.py','pass1_closed_transfer/INTEGRAL_QUOTIENT_CHECK.json',False)]
MUTANTS=[
 ('commutator_sign','w = (3, -2, -3, 2)','w = (3, 2, -3, -2)','commutator x1'),
 ('balanced_exponent_sign','padd(pq, pscale(q2, -1)), pscale(pq, -1)]','padd(pq, pscale(q2, -1)), pscale(pq, 1)]','universal balanced exponent identity'),
 ('exceptional_aab_sign','return escale(difference_action(disk_twist(g, i), B(j, i, j)), -1)','return escale(difference_action(disk_twist(g, i), B(j, i, j)), 1)','AAB realization'),
 ('quotient_reduction_sign','out = eadd(out, escale(relation, -coefficient))','out = eadd(out, escale(relation, coefficient))','relations vanish in normal form')]
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def digest(data):return hashlib.sha256(data).hexdigest()
def snapshot():return {p.relative_to(ROOT).as_posix():digest(p.read_bytes()) for p in ROOT.rglob('*') if p.is_file()}
def invoke(args,cwd):
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None)
 return subprocess.run([sys.executable,'-I','-B',*args],cwd=cwd,env=env,capture_output=True,timeout=180)
class ForceGuard(ast.NodeTransformer):
 def __init__(self):self.done=False
 def visit_If(self,node):
  if not self.done and node.body and isinstance(node.body[0],ast.Raise):
   self.done=True
   node.test=ast.Constant(True)
   node.body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError',ctx=ast.Load()),args=[ast.Constant('intentional public guard probe')],keywords=[]))]
   return node
  return self.generic_visit(node)
def main():
 cp=invoke([str(ROOT/'verify_package.py')],ROOT)
 require(cp.returncode==0 and not cp.stderr,'Integrity failed before replay')
 before=snapshot();records=[];guards=[];mutants=[]
 principal=CHECKS[0][0]
 historical=json.loads((ROOT/'pass1_exact_validation/EXACT_CHECKS.json').read_bytes())
 public=json.loads((ROOT/CHECKS[0][1]).read_bytes())
 for item in [historical,public]:
  item.pop('input_sha256');item.pop('checker_sha256')
 require(historical==public and public['exact_checks']==62840,'Principal mathematical output differs from accepted historical result')
 with tempfile.TemporaryDirectory(prefix='handlebody-exact-replay-') as temp:
  for script,baseline,from_file in CHECKS:
   source=(ROOT/script).read_text();tree=ast.parse(source)
   require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'Optimization-sensitive assertion: '+script)
   transform=ForceGuard();negative=transform.visit(ast.parse(source));ast.fix_missing_locations(negative)
   require(transform.done,'No runtime guard found: '+script)
   for mode,flags in MODES:
    work=Path(temp)/(script.replace('/','_')+'_'+mode);shutil.copytree(ROOT,work)
    for p in work.rglob('*'):
     if p.is_file():p.chmod(0o644)
    cp=invoke([*flags,str(work/script)],work)
    require(cp.returncode==0 and cp.stderr==b'','Checker failed: '+script+' '+mode+' '+cp.stderr.decode())
    output=(work/baseline).read_bytes() if from_file else cp.stdout
    require(output==(ROOT/baseline).read_bytes(),'Baseline differs: '+script+' '+mode)
    if from_file:require(json.loads(cp.stdout)=={'all_checks_passed':True,'ranks':[3,12],'powers':[-12,12],'output':'FREE_GROUP_CHECK.json'},'Free-check status differs')
    records.append({'script':script,'mode':mode,'script_sha256':digest((ROOT/script).read_bytes()),'output_bytes':len(output),'output_sha256':digest(output),'exact_baseline_match':True})
    (work/script).write_text(ast.unparse(negative)+'\n')
    cp=invoke([*flags,str(work/script)],work)
    require(cp.returncode!=0 and b'RuntimeError: intentional public guard probe' in cp.stderr,'Intentional failed guard accepted: '+script+' '+mode)
    guards.append({'script':script,'mode':mode,'rejected':True})
  for name,old,new,label in MUTANTS:
   original=(ROOT/principal).read_text();require(original.count(old)==1,'Mutant target not unique: '+name)
   work=Path(temp)/name;shutil.copytree(ROOT,work)
   for p in work.rglob('*'):
    if p.is_file():p.chmod(0o644)
   (work/principal).write_text(original.replace(old,new))
   for mode,flags in MODES:
    cp=invoke([*flags,str(work/principal)],work)
    require(cp.returncode!=0 and ('RuntimeError: '+label).encode() in cp.stderr,'Formula mutant accepted/wrong failure: '+name+' '+mode)
    mutants.append({'case':name,'mode':mode,'expected_failure':label,'rejected':True})
 require(snapshot()==before,'Replay modified public source tree')
 print(json.dumps({'status':'PASS','finite_script_count':len(CHECKS),'finite_executions':len(records),'principal_checks_per_execution':62840,'principal_mathematical_result_matches_historical_acceptance':True,'all_finite_outputs_byte_identical_to_baselines':True,'optimization_sensitive_assertions':False,'guard_rejections':len(guards),'formula_mutant_cases':len(MUTANTS),'formula_mutant_rejections':len(mutants),'modes':[m for m,_ in MODES],'source_tree_modified':False,'scope':'Exact algebraic replay; uniform proofs and cited topology justify unbounded and group-generation claims.','checks':records,'negative_guards':guards,'formula_mutants':mutants},indent=2,sort_keys=True))
if __name__=='__main__':main()
