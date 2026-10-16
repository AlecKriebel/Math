import sys, subprocess, json, os
from pathlib import Path
HERE=Path.cwd(); PKG=HERE.parent/'publication_package_v2'/'materials'
RUNTIME=HERE.parent/'math_algebra_family_01'/'runtime_packages'
PY='/opt/homebrew/opt/python@3.14/bin/python3.14'
rows=[]
for optimized in (False,True):
 mode='optimized' if optimized else 'normal'
 for filename in ('exact_certificates.py','parity_controls.py'):
  source=PKG/'verification'/filename
  base=[PY,'-E','-S','-B','-P']+(['-O'] if optimized else [])
  setup='import sys,runpy;sys.path.insert(0,'+repr(str(RUNTIME))+');'
  outdir=HERE/('replay-'+mode)
  code=setup+'sys.argv=['+repr(str(source))+',"--output-dir",'+repr(str(outdir))+'];runpy.run_path('+repr(str(source))+',run_name="__main__")'
  with (HERE/(filename+'.'+mode+'.log')).open('w') as log:
   proc=subprocess.run(base+['-c',code],stdout=log,stderr=subprocess.STDOUT)
  if proc.returncode: raise RuntimeError('portable replay failed '+mode+' '+filename)
  expected=PKG/'expected'/filename.replace('.py','.json')
  if filename=='parity_controls.py':expected=PKG/'expected'/'parity_controls_results.json'
  actual=outdir/expected.name
  if json.loads(actual.read_text())!=json.loads(expected.read_text()):raise RuntimeError('semantic mismatch '+mode+' '+filename)
  selfcode=code.replace('];runpy.run_path',',"--self-test-failure"];runpy.run_path')
  selfproc=subprocess.run(base+['-c',selfcode],capture_output=True,text=True)
  if selfproc.returncode==0 or 'deliberate explicit-guard failure' not in selfproc.stderr:raise RuntimeError('self failure bypass')
  prefix=setup+'from pathlib import Path;sys.argv=["guard-probe","--output-dir",'+repr(str(outdir))+'];text=Path('+repr(str(source))+').read_text();'
  if filename=='exact_certificates.py':
   mutation='text=text.replace("s.cancel(H-fact)==0","s.cancel(H-fact-1)==0");exec(compile(text,"substantive-false-identity","exec"),{"__name__":"guard_probe"})'
   signal='physical paired focal-distance factorization'
  else:
   mutation='text=text.replace("(U * U - kappa * V * V * S)","(U * U + kappa * V * V * S)");ns={"__name__":"guard_probe"};exec(compile(text,"substantive-false-identity","exec"),ns);ns["exact_checks"]()'
   signal='parity check failed at source-audit line 20'
  probe=subprocess.run(base+['-c',prefix+mutation],capture_output=True,text=True)
  if probe.returncode==0 or signal not in probe.stderr:raise RuntimeError('substantive false identity bypass')
  rows.append({'mode':mode,'checker':filename,'portable_exit':proc.returncode,'semantic_expected_match':True,'self_test_exit':selfproc.returncode,'substantive_false_identity_exit':probe.returncode,'substantive_rejection':signal})
  (HERE/(filename+'.'+mode+'.negative-tests.log')).write_text(selfproc.stderr+'\n'+probe.stderr)
report={'status':'PASS','interpreter':PY,'isolation_flags':['-E','-S','-B','-P'],'third_party_root':str(RUNTIME),'results':rows}
(HERE/'REPLAY_GUARDS_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
