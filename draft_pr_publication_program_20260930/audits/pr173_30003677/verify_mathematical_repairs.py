"""Check repaired actual checker bytes in both Python modes and false variants."""
from pathlib import Path
import datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parent;D=A/'repaired_candidate_v1';OUT=A/'root_reproduction/repaired_checkers'
PY='/opt/homebrew/opt/python@3.14/bin/python3.14'
def require(c,m):
 if not c:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run(name,code,opt):
 p=OUT/name;p.mkdir(parents=True,exist_ok=False);(p/'author_replay').mkdir()
 (p/'CANDIDATE.md').write_bytes((D/'CANDIDATE.md').read_bytes());(p/'author_replay/CANDIDATE.md').write_bytes((D/'CANDIDATE.md').read_bytes());(p/'checker.py').write_text(code)
 r=subprocess.run([PY,'-E','-S','-B','-P']+(['-O'] if opt else [])+[str(p/'checker.py')],capture_output=True,text=True,cwd=p,timeout=120)
 (p/'stdout.txt').write_text(r.stdout);(p/'stderr.txt').write_text(r.stderr)
 return r,{'checker':pin(p/'checker.py'),'stdout':pin(p/'stdout.txt'),'stderr':pin(p/'stderr.txt'),'exit_code':r.returncode}
def main():
 require(not OUT.exists(),'Previous repair replay needs reconciliation')
 prep=json.loads((A/'MATHEMATICAL_REPAIR_PREPARATION.json').read_text())
 for n,v in prep['files'].items():require(pin(D/n)==v,'Repair bytes changed')
 codes={'author':(D/'verify.py').read_text(),'independent':(D/'review/independent_checks.py').read_text()}
 variants={'author':[('protected_colour','colour[v]==1 and times[v]<=length','colour[v]==2 and times[v]<=length'),('time_budget','F(R)/(lam*T)==F(1,j*j)','F(R)/(lam*T)==F(2,j*j)'),('fast_ball',"ds[v]<=times[v],'fast unopposed domination'","ds[v]>times[v],'fast unopposed domination'")], 'independent':[('protected_colour','colors[v]==1 and times[v]<=T','colors[v]==2 and times[v]<=T'),('size_bias','F(2*j)*F(1,2**j)/4==F(j,2**(j+1))','F(2*j)*F(1,2**j)/8==F(j,2**(j+1))'),('parity_cost',"0<=inc<=degrees[i]+1,'parity_seed_mass_bound'","0<=inc<=0,'parity_seed_mass_bound'")]}
 baseline=[];negative=[]
 for f,code in codes.items():
  values=[]
  for opt in [False,True]:
   r,v=run(f+'_baseline_'+str(opt),code,opt);require(r.returncode==0,'Repair baseline failed');j=json.loads(r.stdout);values.append(j)
   require(j['artifact_sha256']==pin(D/'CANDIDATE.md')['sha256'],'Repair receipt bound to wrong proof')
   require(j['assertions']==(11561 if f=='author' else 62001),'Reproduction count differs')
   baseline.append({'family':f,'optimized':opt,'identities':v,'receipt':j})
  require(values[0]==values[1],'Repaired baseline differs with optimization')
  for n,old,new in variants[f]:
   require(code.count(old)==1,'Mutation anchor changed');bad=code.replace(old,new)
   for opt in [False,True]:
    r,v=run(f+'_'+n+'_'+str(opt),bad,opt);require(r.returncode!=0,'False repair variant passed')
    negative.append({'family':f,'variant':n,'optimized':opt,'identities':v,'rejected':True})
 require(not any(p.name=='independent_results.json' for p in OUT.rglob('*')),'Checker wrote beside source')
 j={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'REPAIRED_EXPLICIT_FAILURE_CHECKERS_REPRODUCED_WITH_ALL_FALSE_VARIANTS_REJECTED','repair_preparation':pin(A/'MATHEMATICAL_REPAIR_PREPARATION.json'),'candidate_files':prep['files'],'baseline_runs':baseline,'negative_runs':negative,'false_variants':6,'false_variant_rejections_across_modes':12,'baseline_receipts_identical_across_modes':True,'combined_finite_checks_per_baseline':73562,'source_side_writes':False,'universal_stochastic_theorem_certified_by_computation':False}
 (A/'ROOT_REPAIRED_CHECKERS_REPRODUCTION.json').write_text(json.dumps(j,indent=2)+'\n')
 for p in D.rglob('*'):
  if p.is_file():p.chmod(0o444)
 (A/'MATHEMATICAL_REPAIR_PREPARATION.json').chmod(0o444)
 print(json.dumps({k:j[k] for k in ['status','false_variants','false_variant_rejections_across_modes','combined_finite_checks_per_baseline','baseline_receipts_identical_across_modes']}))
if __name__=='__main__':main()
