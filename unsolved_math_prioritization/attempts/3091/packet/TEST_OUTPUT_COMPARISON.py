#!/usr/bin/env python3
"""Adversarial full-output-comparison tests against authenticated public expectations."""
from pathlib import Path
import argparse,copy,importlib.util,json,subprocess,sys,tempfile

def main():
 ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--worker',action='store_true');a=ap.parse_args();root=a.root.absolute()
 if not a.worker:
  runs=[]
  for name,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
   p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(Path(__file__).resolve()),str(root),'--worker'],capture_output=True,text=True,timeout=30)
   if p.returncode or p.stderr:raise RuntimeError('comparison worker failed: '+p.stderr)
   runs.append({'mode':name,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'result':json.loads(p.stdout)})
  print(json.dumps({'status':'PASS','normalization':'none','runs':runs},sort_keys=True,indent=2));return
 spec=importlib.util.spec_from_file_location('trusted',root/'VERIFY_PUBLICATION.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 f=v.authenticate(root);expected=v.load(f['EXPECTED_OUTPUTS.json']);mode=sys.flags.optimize
 baseline=[expected['native_geometry'][str(mode)],expected['audit_driver'],expected['public_audit_receipt'],expected['cwd_write_probes']]
 v.compare_outputs(*baseline,expected,mode);cases=[]
 def check(name,mutate,error):
  payload=copy.deepcopy(baseline);mutate(payload)
  try:v.compare_outputs(*payload,expected,mode)
  except v.Reject as e:
   if str(e)!=error:raise RuntimeError('wrong rejection: '+name)
   cases.append({'case':name,'status':'REJECT','error':str(e)})
  else:raise RuntimeError('comparison mutant accepted: '+name)
 native='complete native geometry output mismatch';audit='complete audit driver output mismatch';receipt='complete public audit output mismatch';cwd='complete cwd probe output mismatch'
 check('native-extra-key',lambda x:x[0].update(extra=1),native)
 check('native-stdout-byte',lambda x:x[0].update(stdout=x[0]['stdout']+' '),native)
 check('native-stderr',lambda x:x[0].update(stderr='unexpected'),native)
 check('native-exit-type-float',lambda x:x[0].update(exit_code=0.0),native)
 check('native-exit-type-bool',lambda x:x[0].update(exit_code=False),native)
 check('native-python-version',lambda x:x[0]['result'].update(python='3.12.15'),native)
 check('native-count',lambda x:x[0]['result']['counts'].update(grid_subsets_5=4495),native)
 check('native-count-type',lambda x:x[0]['result']['counts'].update(grid_subsets_5=4494.0),native)
 check('driver-stdout-byte',lambda x:x[1].update(stdout=x[1]['stdout']+' '),audit)
 check('driver-extra-key',lambda x:x[1].update(extra=1),audit)
 check('oracle-plausible-count',lambda x:x[2]['runs'][0]['independent_geometry']['result']['counts'].update(grid_subsets_3=561),receipt)
 check('oracle-stdout-byte',lambda x:x[2]['runs'][0]['independent_geometry'].update(stdout=x[2]['runs'][0]['independent_geometry']['stdout']+' '),receipt)
 check('semantic-error',lambda x:x[2]['runs'][0]['semantic_controls'][0]['result'].update(error='different failure'),receipt)
 check('semantic-status',lambda x:x[2]['runs'][0]['semantic_controls'][0]['result'].update(status='PASS'),receipt)
 check('semantic-exit-type',lambda x:x[2]['runs'][0]['semantic_controls'][0].update(exit_code=2.0),receipt)
 check('semantic-extra-key',lambda x:x[2]['runs'][0]['semantic_controls'][0].update(extra=True),receipt)
 check('semantic-stdout-byte',lambda x:x[2]['runs'][0]['semantic_controls'][0].update(stdout=x[2]['runs'][0]['semantic_controls'][0]['stdout']+' '),receipt)
 check('missing-semantic-outcome',lambda x:x[2]['runs'][0]['semantic_controls'].pop(),receipt)
 check('public-inventory-mode',lambda x:x[2]['public_inventory_before']['README.md'].update(mode='0o644'),receipt)
 check('audit-extra-top-key',lambda x:x[2].update(extra=1),receipt)
 check('cwd-probe-order',lambda x:x[3].reverse(),cwd)
 check('cwd-probe-extra-key',lambda x:x[3][0].update(extra=True),cwd)
 print(json.dumps({'status':'PASS','mode':mode,'baseline_passes':1,'precise_comparison_rejections':len(cases),'expected_outputs_sha256':v.sha(f['EXPECTED_OUTPUTS.json']),'results':cases},sort_keys=True,indent=2))
if __name__=='__main__':main()
