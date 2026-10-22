#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
D=Path(__file__).absolute().parent
def need(c,m):
 if not c:raise ValueError(m)
def safe(p):
 q=Path(p.anchor)
 for t in p.parts[1:]:
  q=q/t;need(not q.is_symlink(),'symlink '+str(q))
 return p
def main():
 safe(D);m=json.loads(safe(D/'MANIFEST.json').read_text());names=m['members'];need(len(names)==13 and len(set(names))==len(names),'manifest membership');need(all(Path(n).name==n and n not in {'.','..'} for n in names),'unsafe name');need({p.name for p in D.iterdir()}==set(names),'flat release mismatch')
 for e in m['entries']:
  p=safe(D/e['file']);need(p.is_file(),'file type');b=p.read_bytes();need(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'hash '+e['file'])
 need({e['file'] for e in m['entries']}==set(names)-{'MANIFEST.json'},'manifest entry set')
 baseline=safe(D/'EXPECTED_FINITE_SIGNS.json').read_bytes();runs=[];failures=[]
 errors={'omit_deletion':'explicit inverse failure','keep_minimum':'rotation collision','append_plus':'rotation collision','omit_scaling':'bottom source generator does not map to target unit'}
 for mode in [[],['-O']]:
  r=subprocess.run([sys.executable,'-B']+mode+[str(D/'verify_finite_signs.py')],capture_output=True);need(r.returncode==0 and not r.stderr and r.stdout==baseline,'complete positive output');runs.append({'mode':'optimized' if mode else 'normal','stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest()})
  for mutation,message in errors.items():
   r=subprocess.run([sys.executable,'-B']+mode+[str(D/'verify_finite_signs.py'),'--mutation',mutation],capture_output=True);need(r.returncode!=0 and not r.stdout and ('ValueError: '+message) in r.stderr.decode(),'computed mutation failure '+mutation);failures.append({'mode':'optimized' if mode else 'normal','mutation':mutation,'failure':message})
 print(json.dumps({'status':'PASS','member_count':len(names),'runs':runs,'actual_wrong_result_failures':failures,'finite_diagnostics_only':True},sort_keys=True,indent=2))
if __name__=='__main__':main()
