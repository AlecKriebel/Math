#!/usr/bin/env python3
"""Fresh finite diagnostics and negative controls, with explicit execution-mode scope."""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess,sys

def require(c,m):
 if not c:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--out-dir',required=True);args=parser.parse_args()
 root=Path(__file__).resolve().parent;out=Path(args.out_dir).resolve();out.mkdir(parents=True,exist_ok=True)
 receipts=[];reports=[]
 def execute(name,script,flags,extra=(),expected=0):
  folder=out/name;folder.mkdir(exist_ok=True)
  argv=[sys.executable,'-I','-B',*flags,str(script),*extra]
  r=subprocess.run(argv,cwd=folder,capture_output=True,text=True)
  (folder/'stdout.txt').write_text(r.stdout);(folder/'stderr.txt').write_text(r.stderr)
  require((r.returncode==0)==(expected==0),'unexpected return code: '+name)
  receipts.append({'name':name,'argv':argv,'returncode':r.returncode,'script_sha256':sha(script),'stderr_bytes':len(r.stderr.encode())})
  if expected==0:
   require(not r.stderr,'successful checker produced stderr')
   return json.loads((folder/'FINITE_CHECKS.json').read_text())
 original=root/'support/history/reviews/entropy_01/finite_checks.py'
 replay=execute('original_normal',original,[])
 baseline=json.loads((root/'support/history/root_reproduction/FINITE_CHECKS.json').read_text())
 project=lambda d:{k:v for k,v in d.items() if k not in ['completed_utc','python','platform']}
 require(project(replay)==project(baseline),'original current replay differs from root baseline')
 for name,flags in [('guard_normal',[]),('guard_optimized',['-O'])]:
  reports.append(execute(name,root/'fresh_guard_checker.py',flags))
 require(project(reports[0])==project(reports[1]),'normal / optimized diagnostics differ')
 faults=['scalar-divergence','unit-endpoint','zero-mass-term','n1-purepower','confuse-KL','drop-sequential-KL','Dong-Jain-half']
 for mode,flags in [('normal',[]),('optimized',['-O'])]:
  for fault in faults:execute(mode+'_'+fault,root/'fresh_guard_checker.py',flags,['--fault',fault],expected=1)
 result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pass':True,'scope':'Exact rational finite combinatorial models and 120-digit Decimal logs, not interval certification, universal proof, historical omitted-script replay or formal verification.','original_entropy_replay':'Unmodified frozen original normal -I -B only; assert validations active. Runtime-only completed_utc, python and platform excluded in baseline projection. No optimized assertion-semantic claim for original.','new_guard_checker':'Explicit raises; same complete finite output normal and -O after declared runtime projection. Seven faults detected in BOTH modes.','matrix_cases':reports[0]['matrix_cases'],'arbitrary_laws':reports[0]['arbitrary_permutation_laws'],'positive_histories':reports[0]['positive_histories_total'],'scalar_pairs':reports[0]['scalar_boundary_pairs'],'negative_controls':faults,'receipts':receipts}
 (out/'CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['pass','matrix_cases','arbitrary_laws','positive_histories','scalar_pairs','negative_controls']},indent=2))
if __name__=='__main__':main()
