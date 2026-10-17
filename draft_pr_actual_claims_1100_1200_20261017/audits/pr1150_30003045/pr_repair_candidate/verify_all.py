#!/usr/bin/env python3
"""Read-only exact diagnostics and member integrity; not a cohomology oracle."""
from pathlib import Path
import hashlib,json,subprocess,sys
D=Path(__file__).absolute().parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
def main():
 need(not D.is_symlink(),'symlink edition directory');need(all(not p.is_symlink() and p.is_file() for p in D.iterdir()),'unexpected non-file or symlink entry');m=json.loads((D/'MANIFEST.json').read_text());need(m['self_hash_excluded']=='MANIFEST.json','manifest rule');names=m['members'];need(len(names)==len(set(names)),'duplicate members')
 actual={p.name for p in D.iterdir()};need(actual==set(names),'unexpected or missing file inventory')
 for n in names:
  p=D/n;need(not Path(n).is_absolute() and len(Path(n).parts)==1 and not p.is_symlink() and p.is_file(),'unsafe member '+n)
 for n,want in m['entries'].items():
  raw=(D/n).read_bytes();need(len(raw)==want['bytes'] and hashlib.sha256(raw).hexdigest()==want['sha256'],'pin mismatch '+n)
 need(set(m['entries'])==set(names)-{'MANIFEST.json'},'manifest coverage')
 runs=[];failures=[]
 modes=['differentiate_square','wrong_h_frobenius','wrong_s_power','omit_exact_correction','gamma_kills_dz','a_belongs_R','wrong_quotient_derivative','slot_z_preserves_dz','invalid_exponent_one_base_dlog']
 for flags in [[],['-O']]:
  for prog,baseline in [('verify_symbols.py','symbols_expected.json'),('diagnose_norm.py','norm_expected.json')]:
   r=subprocess.run([sys.executable,'-B',*flags,str(D/prog)],capture_output=True);need(r.returncode==0 and not r.stderr and r.stdout==(D/baseline).read_bytes(),'complete diagnostic mismatch '+prog);runs.append({'program':prog,'flags':flags,'output_sha256':hashlib.sha256(r.stdout).hexdigest()})
  for mode in modes:
   r=subprocess.run([sys.executable,'-B',*flags,str(D/'verify_symbols.py'),'--wrong',mode],capture_output=True);last=r.stderr.decode().splitlines()[-1] if r.stderr else '';need(r.returncode!=0 and last.startswith('ValueError: CHECK FAILED:') and 'unexpectedly passed' not in last,'wrong-result control failed '+mode);failures.append({'mode':mode,'flags':flags,'exit':r.returncode,'diagnostic':last})
 print(json.dumps({'status':'PASS','member_count':len(names),'runs':runs,'actual_wrong_result_failures':failures,'finite_diagnostics_only':True},sort_keys=True,indent=2))
if __name__=='__main__':main()
