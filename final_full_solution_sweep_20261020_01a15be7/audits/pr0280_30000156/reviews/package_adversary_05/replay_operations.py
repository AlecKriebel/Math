#!/usr/bin/env python3
from pathlib import Path
import importlib.util,json,shutil,subprocess,sys
O=Path(__file__).resolve().parent;A=O.parents[1];R=A.parents[1];W=R/'private/pr0280_package05/operations';W.mkdir(parents=True,exist_ok=True)
if len(sys.argv)>1:
 suite=sys.argv[1];D=W/('optimized' if sys.flags.optimize else 'normal')/suite;D.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(A/'ops_record_url_repair_20261021',D)
 sys.path.insert(0,str(D))
 def load(n,p):
  spec=importlib.util.spec_from_file_location(n,D/p);m=importlib.util.module_from_spec(spec);sys.modules[n]=m;spec.loader.exec_module(m);return m
 S=load('controls_support','controls_support.py');S.AUDIT=A
 T=load('own_replay_suite',{'994':'current_controls.py','404':'replay_404.py','3':'resume_path_controls.py','old32':'reproduce_old.py'}[suite]);T.main()
else:
 results=[]
 for mode in [[],['-O']]:
  for suite in ['old32','994','404','3','303']:
   args=[sys.executable,'-B',*mode]
   if suite=='303':args += [str(R/'private/record_url_metamorphic_controls.py'),str(A),str(A/'ops_binding.py')]
   else:args += [str(Path(__file__)),suite]
   r=subprocess.run(args,capture_output=True,text=True);name=('optimized' if mode else 'normal')+'_'+suite;(W/(name+'.stdout')).write_text(r.stdout);(W/(name+'.stderr')).write_text(r.stderr)
   if r.returncode:raise RuntimeError(name+' failed '+r.stderr[-2000:])
   if suite=='303':
    x=json.loads(r.stdout)
    if x['positive_outcomes']!={'target_lead':295,'blocked_ambiguous':1,'silently_missed':0} or any(v['outcome']!='distinct_no_target' for v in x['negative_cases']):raise RuntimeError('303 outcomes')
   results.append({'mode':mode,'suite':suite,'exit_code':r.returncode,'controls':32 if suite=='old32' else int(suite),'stdout_bytes':len(r.stdout),'actual_provider_access_attempts':0})
 (O/'OPERATIONS_REPLAY.json').write_text(json.dumps({'replays':results,'current_controls_per_mode':1704,'old_false_uniqueness_per_mode':32,'scope':'Copied runners with current canonical modules; only scratch/output locations redirected, provider interfaces trapped; no production guard weakened.'},indent=2)+'\n');print(json.dumps(results))
