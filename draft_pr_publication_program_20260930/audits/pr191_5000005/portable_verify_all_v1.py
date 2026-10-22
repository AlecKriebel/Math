"""Portable stdlib verification; copies executable inputs into owned temporary folders."""
from pathlib import Path
import ast,hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(data):return hashlib.sha256(data).hexdigest()
def scientific(obj):
 obj=dict(obj);obj.pop('utc',None);obj.pop('script_sha256',None);return obj
def integrity():
 manifest=json.loads((ROOT/'MANIFEST.json').read_text());expected=set()
 for x in manifest['files']:
  name=x['path'];require(not Path(name).is_absolute() and '..' not in Path(name).parts,'Unsafe manifest path');p=ROOT/name;require(p.is_file() and not p.is_symlink(),'Missing or nonregular input '+name);b=p.read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Input identity drift '+name);expected.add(name)
 actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()};require(actual==expected|{'MANIFEST.json'},'Unexpected or missing payload');return len(expected)
JOBS=[
 ('author','original_submission/files/unsolved_math_prioritization/attempts/5000005/verify.py','check',3276822),
 ('original_reviewer','original_submission/files/unsolved_math_prioritization/attempts/5000005/review/check_independent.py','require',441920),
 ('literal_hardened','checks/literal_type_hardened.py',None,None),
 ('physical_346','checks/reflection_geometry.py','require',646),
 ('physical_5','checks/pentagon_geometry.py','require',172),
 ('physical_8','checks/octagon_geometry.py','require',462),
 ('geometry_sanity','checks/geometry_checker.py','require',None)]
def run(job,optimize,base,mutate=False):
 name,rel,guard,expected=job;source=(ROOT/rel).read_text();tree=ast.parse(source);require(not any(isinstance(x,ast.Assert) for x in ast.walk(tree)),'Optimization-removable assertion in executable input '+rel)
 d=base/(name+('_optimized' if optimize else '_ordinary')+('_false' if mutate else ''));d.mkdir();target=d/Path(rel).name
 if mutate:
  if guard:
   pos=next((i for i,x in enumerate(tree.body) if isinstance(x,ast.FunctionDef) and x.name==guard),None);require(pos is not None,'Missing actual guard '+name);tree.body.insert(pos+1,ast.Expr(ast.Call(func=ast.Name(id=guard,ctx=ast.Load()),args=[ast.Constant(False),ast.Constant('PACKET_FALSE_GUARD_CONTROL')],keywords=[])))
  else:
   node=next((x for x in ast.walk(tree) if isinstance(x,ast.If) and isinstance(x.test,ast.UnaryOp) and isinstance(x.test.op,ast.Not) and any(isinstance(z,ast.Raise) and isinstance(z.exc,ast.Call) and isinstance(z.exc.func,ast.Name) and z.exc.func.id=='AssertionError' for z in x.body)),None);require(node is not None,'Missing hardened assertion guard');node.test=ast.Constant(True);node.body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[ast.Constant('PACKET_FALSE_GUARD_CONTROL')],keywords=[]),cause=None)]
  source=ast.unparse(ast.fix_missing_locations(tree))+'\n'
 target.write_text(source)
 if name=='original_reviewer':shutil.copyfile(ROOT/'original_submission/files/unsolved_math_prioritization/attempts/5000005/review/CANDIDATE_FROZEN.md',d/'CANDIDATE_FROZEN.md')
 args=[sys.executable,'-E','-S','-B','-P']+(['-O'] if optimize else [])+[str(target)];p=subprocess.run(args,cwd=d,capture_output=True,text=True,timeout=180)
 row={'job':name,'optimized':optimize,'false_condition_injected':mutate,'exit':p.returncode,'source_sha256':sha(source.encode()),'stdout_sha256':sha(p.stdout.encode()),'stderr_sha256':sha(p.stderr.encode())}
 if mutate:
  require(p.returncode!=0 and 'PACKET_FALSE_GUARD_CONTROL' in p.stderr,'False condition failed to fail '+name);return row,None
 require(p.returncode==0,'Verification failed '+name+': '+p.stderr[-1500:]);obj=json.loads(p.stdout)
 if name in ['author','original_reviewer']:require(obj['status']=='PASS' and obj['assertions']==expected,'Original check count drift')
 elif name.startswith('physical_'):require(obj['status']=='PASS' and obj['pair_count']==expected,'Physical first-hit comparison count drift')
 elif name=='literal_hardened':require(scientific(obj)==scientific(json.loads((ROOT/'reference_results/literal_original_ordinary.json').read_text())),'Hardened semantics differ from authenticated ordinary baseline')
 else:require(obj['status']=='PASS' and obj['counts']['exact_canonical_chords']==1398012,'Geometry sanity drift')
 clean=scientific(obj);row['scientific_sha256']=sha(json.dumps(clean,sort_keys=True,separators=(',',':')).encode());row['counts']=obj.get('counts',obj.get('assertions'));row['pair_count']=obj.get('pair_count');return row,row['scientific_sha256']
def main():
 count=integrity();positive=[];negative=[]
 with tempfile.TemporaryDirectory(prefix='math-pr191-verification-') as raw:
  base=Path(raw)
  for job in JOBS:
   modes=[]
   for opt in [False,True]:
    row,digest=run(job,opt,base);positive.append(row);modes.append(digest)
   require(modes[0]==modes[1],'Ordinary/optimized scientific discrepancy '+job[0])
  for job in JOBS[:6]:
   for opt in [False,True]:row,_=run(job,opt,base,True);negative.append(row)
 require(integrity()==count,'Payload changed during execution')
 print(json.dumps({'status':'PASS','payload_files_checked':count,'positive_executions':positive,'expected_failure_executions':negative,'expected_failure_count':len(negative),'physical_transformed_pairs':1280,'terminated_trace_invocations_including_repetitions':1628,'scope':'Finite corroboration and optimization-safe failure enforcement only. Universal theorem is analytic; literal imported conjunction is false; qualified credited rederivation, no novelty or historical-priority certification.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
