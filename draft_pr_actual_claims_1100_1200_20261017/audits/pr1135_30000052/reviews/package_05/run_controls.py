#!/usr/bin/env python3
"""Capture four final independent runs and actual portable-runner mutations."""
from pathlib import Path
import copy,datetime,hashlib,json,os,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def require(v,label):
 if not v:raise RuntimeError(label)
def encoded(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def main():
 source=HERE/'independent_control.py';codepin=pin(source.read_bytes());rows=[];normal=None
 for optimize in (False,True):
  for forced in (False,True):
   command=[sys.executable,'-B']+(['-O'] if optimize else [])+[str(source)]+(['--force-wrong-identity'] if forced else [])
   p=subprocess.run(command,capture_output=True,text=True)
   require(pin(source.read_bytes())==codepin,'control changed during execution')
   label=('optimized' if optimize else 'normal')+('.forced' if forced else '')
   (HERE/'tmp'/('control.'+label+'.stdout')).write_text(p.stdout)
   (HERE/'tmp'/('control.'+label+'.stderr')).write_text(p.stderr)
   if forced:
    require(p.returncode!=0 and '19/1620 != 4/405' in p.stderr,'wrong identity was not actually rejected')
   else:
    require(p.returncode==0,'independent positive run failed')
    result=json.loads(p.stdout);require(result['status']=='PASS','independent result status')
    (HERE/('RESULTS.'+label+'.json')).write_bytes(p.stdout.encode())
    if normal is None:normal=p.stdout
    else:require(normal==p.stdout,'ordinary/optimized differ')
   rows.append({'optimized':optimize,'forced_wrong_identity':forced,'exit':p.returncode,'stdout':pin(p.stdout.encode()),'stderr':pin(p.stderr.encode()),'diagnostic':'computed n3 lattice 19/1620 rejected wrong iid expected 4/405' if forced else '78 named checks and 6 deliberately false identities rejected'})
 base=HERE/'tmp/extracted';plan=json.loads((base/'verification/CONTROL_PLAN.json').read_text());guardrows=[]
 for mutation in ('wrong_expected_value','input_corruption','checker_corruption','optimization_assertion'):
  mirror=HERE/'tmp'/('guard_'+mutation);shutil.copytree(base,mirror)
  localplan=copy.deepcopy(plan);spec=localplan['controls'][0]
  if mutation=='wrong_expected_value':
   target=mirror/'audit'/spec['expected'];expected=json.loads(target.read_text());expected['lattice_fourth_moment']='4/405';target.write_bytes(encoded(expected));spec['expected_pin']=pin(target.read_bytes())
  elif mutation=='input_corruption':
   target=mirror/'audit/inputs/PROOF.md';target.write_bytes(target.read_bytes()+b'\nmutation\n')
  elif mutation=='checker_corruption':
   target=mirror/'audit'/spec['file'];target.write_bytes(target.read_bytes()+b'\n# mutation\n')
  elif mutation=='optimization_assertion':
   target=mirror/'audit'/spec['file'];target.write_bytes(target.read_bytes()+b'\nassert True\n');spec['pin']=pin(target.read_bytes())
  # Isolate the first pinned program, preserving all input and result checks.
  localplan['controls']=[spec];(mirror/'verification/CONTROL_PLAN.json').write_bytes(encoded(localplan))
  for mode in ('ordinary','optimized'):
   command=[sys.executable,'-B',str(mirror/'verification/verify_all.py'),'--mode',mode]
   p=subprocess.run(command,capture_output=True,text=True,env=os.environ|{'TMPDIR':str(HERE/'tmp')})
   marker={'wrong_expected_value':'Result mismatch','input_corruption':'Fingerprint mismatch','checker_corruption':'Fingerprint mismatch','optimization_assertion':'Optimization-sensitive assertion'}[mutation]
   require(p.returncode!=0 and marker in p.stderr,'runner failed to reject '+mutation+' '+mode)
   (HERE/'tmp'/('runner.'+mutation+'.'+mode+'.stderr')).write_text(p.stderr)
   guardrows.append({'mutation':mutation,'mode':mode,'exit':p.returncode,'diagnostic_contains':marker,'stderr':pin(p.stderr.encode()),'expected_pin_updated':mutation=='wrong_expected_value','checker_pin_updated':mutation=='optimization_assertion'})
 receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'executable':sys.executable,'sealed_control':codepin,'independent_runs':rows,'ordinary_optimized_byte_identical':True,'successful_result':json.loads(normal),'runner_adverse_runs':guardrows,'live_package_mutated':False}
 (HERE/'CONTROL_REPLAY.json').write_bytes(encoded(receipt));print(json.dumps({'independent_runs':rows,'portable_runner_adverse_runs':guardrows},indent=2))
if __name__=='__main__':main()
