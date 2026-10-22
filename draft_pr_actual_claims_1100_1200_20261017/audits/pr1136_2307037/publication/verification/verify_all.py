#!/usr/bin/env python3
"""Pinned mathematical diagnostics; Python3.10+ stdlib. Never publish.
Optional source retrieval and all executions use a disposable audit mirror.
"""
from pathlib import Path
import argparse,ast,hashlib,json,math,shutil,subprocess,sys,tempfile,urllib.request
HERE=Path(__file__).resolve().parents[1]
def fail(s):raise RuntimeError(s)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def check(p,w):
 if pin(p)!=w:fail('Fingerprint mismatch: '+str(p))
def select(v,keys):
 for k in keys:v=v[k]
 return v
def compare(g,w,s='result'):
 # Compare every mathematical field. Only floating diagnostic roundoff is allowed;
 # each original program separately enforces its own mathematical thresholds.
 if isinstance(g,bool) or isinstance(w,bool):
  if type(g)!=type(w) or g!=w:fail('Boolean mismatch '+s)
 elif isinstance(g,float) or isinstance(w,float):
  if not isinstance(g,(int,float)) or not isinstance(w,(int,float)) or not math.isfinite(g) or not math.isfinite(w) or not math.isclose(g,w,rel_tol=1e-12,abs_tol=1e-12):fail('Numeric mismatch '+s)
 elif isinstance(w,dict):
  if not isinstance(g,dict) or set(g)!=set(w):fail('Keys mismatch '+s)
  for k in w:compare(g[k],w[k],s+'.'+k)
 elif isinstance(w,list):
  if not isinstance(g,list) or len(g)!=len(w):fail('Length mismatch '+s)
  for i,(x,y) in enumerate(zip(g,w)):compare(x,y,s+'['+str(i)+']')
 elif type(g)!=type(w) or g!=w:fail('Exact mismatch '+s)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--with-target-source',action='store_true');ap.add_argument('--target-source-file',type=Path);args=ap.parse_args()
 plan=json.loads((HERE/'verification/CONTROL_PLAN.json').read_text());members=json.loads((HERE/'verification/AUDIT_MEMBERS.json').read_text())
 audit=HERE/plan['source_prefix'] if (HERE/plan['source_prefix']).is_dir() else HERE.parent
 for n,w in members.items():check(audit/n,w)
 if pin(audit/'inputs/PROOF.md')['sha256']!=plan['source_proof_sha256']:fail('Source proof changed')
 if (HERE/'SOURCE_MANIFEST.json').exists():
  for n,w in json.loads((HERE/'SOURCE_MANIFEST.json').read_text()).items():check(HERE/n,w)
 runs=[];guards=[]
 with tempfile.TemporaryDirectory(prefix='fixed-area-controls-') as t:
  mirror=Path(t)/plan['source_prefix']
  for n in members:
   dest=mirror/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(audit/n,dest)
  target=args.with_target_source or args.target_source_file is not None
  if target:
   source=plan['target_source'];dest=mirror/source['path'];dest.parent.mkdir(parents=True,exist_ok=True)
   if args.target_source_file:shutil.copyfile(args.target_source_file,dest)
   else:
    request=urllib.request.Request(source['url'],headers={'User-Agent':'fixed-area-verification/1.0'})
    with urllib.request.urlopen(request,timeout=60) as response:dest.write_bytes(response.read())
   check(dest,{'bytes':source['bytes'],'sha256':source['sha256']})
  for row in plan['controls']:
   if row['optional_target_source'] and not target:continue
   script=mirror/row['program']
   if any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(script.read_text()))):fail('Optimizable assert '+row['program'])
   expected=select(json.loads((mirror/row['expected']).read_text()),row['selector'])
   for optimized in [False,True]:
    cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(script)]
    r=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=90)
    if r.returncode or r.stderr:fail('Control failed '+row['program']+' '+r.stderr[-1000:])
    actual=json.loads(r.stdout);wanted=json.loads(json.dumps(expected))
    if row['program'].endswith('check_quadrature.py'):
     wanted['python_optimization']=int(optimized);wanted['python_version']=sys.version
    compare(actual,wanted)
    runs.append({'program':row['program'],'optimized':optimized,'complete_output_compared':True,'result':actual})
    tests=[(row['guard'],row['diagnostic'])] if row['guard'] else []
    if row['optional_target_source']:tests += [(['--mutant',m],m) for m in ['missing_pi','spurious_R2','radius_lambda']]
    for extra,diagnostic in tests:
     bad=subprocess.run(cmd+extra,cwd='/',capture_output=True,text=True,timeout=90)
     if bad.returncode==0 or diagnostic not in bad.stdout+bad.stderr:fail('Failure guard inactive '+row['program']+str(extra))
     guards.append({'program':row['program'],'optimized':optimized,'arguments':extra,'returncode':bad.returncode,'expected_diagnostic_present':True})
 for n,w in members.items():check(audit/n,w)
 print(json.dumps({'status':'PASS','authored_audit_members_checked':len(members),'source_inputs_checked':len(plan['inputs']),'runs':runs,'actual_failure_guards':guards,'target_source_control':'run with hash-pinned primary PDF in temporary mirror' if target else 'not run; use --with-target-source or --target-source-file PATH','floating_comparison':plan['floating_comparison'],'scope':'Supplementary diagnostics; universal written proof and imported source interfaces required.'},indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
