"""Bounded original and exception-guarded replay with semantic negative controls."""
from pathlib import Path
import datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parent
O=A/'original_submission/files/unsolved_math_prioritization/attempts/30003677'
PY='/opt/homebrew/opt/python@3.14/bin/python3.14'
D=A/'root_reproduction';D.mkdir(exist_ok=True)
def require(c,m):
 if not c:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run(folder,code,optimized):
 folder.mkdir(parents=True,exist_ok=False)
 (folder/'checker.py').write_text(code)
 (folder/'CANDIDATE.md').write_bytes((O/'CANDIDATE.md').read_bytes())
 (folder/'author_replay').mkdir()
 (folder/'author_replay/CANDIDATE.md').write_bytes((O/'CANDIDATE.md').read_bytes())
 command=[PY,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(folder/'checker.py')]
 r=subprocess.run(command,cwd=folder,capture_output=True,text=True,timeout=120)
 (folder/'stdout.txt').write_text(r.stdout);(folder/'stderr.txt').write_text(r.stderr)
 return {'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'checker':pin(folder/'checker.py'),'stdout_identity':pin(folder/'stdout.txt'),'stderr_identity':pin(folder/'stderr.txt')}
def main():
 originals={'author':(O/'verify.py').read_text(),'independent':(O/'review/independent_checks.py').read_text()}
 guards={'author':('    assert v,label','    if not v: raise RuntimeError(label)'), 'independent':('    assert value,category','    if not value: raise RuntimeError(category)')}
 variants={'author':[
  ('false_protected_colour','colour[v]==1 and times[v]<=length','colour[v]==2 and times[v]<=length'),
  ('false_time_budget','F(R)/(lam*T)==F(1,j*j)','F(R)/(lam*T)==F(2,j*j)'),
  ('false_fast_domination',"ds[v]<=times[v],'fast unopposed domination'","ds[v]>times[v],'fast unopposed domination'")],
 'independent':[
  ('false_protected_colour','colors[v]==1 and times[v]<=T','colors[v]==2 and times[v]<=T'),
  ('false_size_bias','F(2*j)*F(1,2**j)/4==F(j,2**(j+1))','F(2*j)*F(1,2**j)/8==F(j,2**(j+1))'),
  ('false_repair_cost',"0<=inc<=degrees[i]+1,'parity_seed_mass_bound'","0<=inc<=0,'parity_seed_mass_bound'")]}
 runs=[];baseline=[]
 for family,source in originals.items():
  old,new=guards[family];require(source.count(old)==1,'Check guard changed')
  versions={'original':source,'exception_guarded':source.replace(old,new)}
  for version,code in versions.items():
   values=[]
   for opt in [False,True]:
    key=family+'_'+version+'_baseline_'+('optimized' if opt else 'ordinary');r=run(D/key,code,opt)
    require(r['exit_code']==0,'Baseline failed '+key)
    value=json.loads(r['stdout']);values.append(value)
    baseline.append({'run':key,'checker':r['checker'],'receipt':value,'stdout_identity':r['stdout_identity']})
   require(values[0]==values[1],'Baseline differs with optimization')
   for name,old,new in variants[family]:
    require(code.count(old)==1,'Mutation anchor changed '+name)
    bad=code.replace(old,new)
    for opt in [False,True]:
     key=family+'_'+version+'_'+name+'_'+('optimized' if opt else 'ordinary');r=run(D/key,bad,opt)
     expected=r['exit_code']!=0 if version=='exception_guarded' or not opt else r['exit_code']==0
     require(expected,'Unexpected false-variant behavior '+key)
     runs.append({'run':key,'checker':r['checker'],'exit_code':r['exit_code'],'false_variant_rejected':r['exit_code']!=0,'stdout_identity':r['stdout_identity'],'stderr_identity':r['stderr_identity']})
 receipt={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'ORIGINAL_CHECKS_REPRODUCED_AND_ASSERT_OPTIMIZATION_GAP_DEMONSTRATED','scientific_inputs':{str(O/n):pin(O/n) for n in ['CANDIDATE.md','verify.py','review/independent_checks.py']},'baseline_runs':baseline,'semantic_false_variant_runs':runs,'total_runs':len(baseline)+len(runs),'original_ordinary_false_variants_rejected':6,'original_optimized_false_variants_incorrectly_accepted':6,'exception_guarded_ordinary_and_optimized_false_variants_rejected':12,'originals_unchanged':True,'limits':'Finite deterministic controls support path/resource arithmetic only. Universal probabilistic/local/diagonal theorem requires the written proof. Replacing assert by explicit exceptions is necessary for reliable optimized verification; fingerprints alone do not prove mathematical claims.'}
 for n,v in receipt['scientific_inputs'].items():require(pin(Path(n))==v,'Original changed')
 p=D/'REPRODUCTION.json';require(not p.exists(),'Replay already recorded');p.write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({k:receipt[k] for k in ['status','total_runs','original_ordinary_false_variants_rejected','original_optimized_false_variants_incorrectly_accepted','exception_guarded_ordinary_and_optimized_false_variants_rejected']}))
if __name__=='__main__':main()
