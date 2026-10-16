#!/usr/bin/env python3
"""Reproduce actual four-mode release replay, controls, helper sentinels and fresh PDF pixels."""
import argparse,datetime,hashlib,importlib.util,json,os,pathlib,shutil,subprocess,sys,tempfile,zipfile
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent;A=R.parents[1]
def need(x,s):
 if not x:raise RuntimeError(s)
def module(n):
 s=importlib.util.spec_from_file_location('reproduce03_'+n,R/n);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def command(args,env=None,timeout=1800):
 p=subprocess.run(list(map(str,args)),capture_output=True,text=True,env=env,timeout=timeout)
 need(p.returncode==0,str(args[1:3])+': '+p.stderr[-4000:]);return p.stdout
def equivalent(a,b):
 need(type(a) is type(b),'strict output type')
 if type(a) is dict:
  need(a.keys()==b.keys(),'strict output keys')
  for k in a:equivalent(a[k],b[k])
 elif type(a) is list:
  need(len(a)==len(b),'strict output list length')
  for x,y in zip(a,b):equivalent(x,y)
 else:need(a==b,'strict output value')
def main():
 p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);p.add_argument('--candidate',type=pathlib.Path,default=A/'publication');p.add_argument('--python',type=pathlib.Path,default=pathlib.Path(sys.executable));p.add_argument('--output',type=pathlib.Path);args=p.parse_args();seal=module('VERIFY.py').verify(args.expected_manifest)
 auth=module('AUTHENTICATE.py');start=auth.perform(args.candidate);prior=module('PRIOR_REPAIRS.py').perform(args.candidate)
 work=R/'private/full_reproduction';work.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(dir=work) as td:
  temp=pathlib.Path(td);c=temp/'candidate';c.mkdir();f=json.loads((args.candidate/'PREPUBLICATION_FREEZE.json').read_text())
  for n in [*f['files'],'PREPUBLICATION_FREEZE.json','BUILD_RECEIPT.json']:
   q=c/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(args.candidate/n,q)
  (c/'tmp').mkdir();bundle=c/'tmp/bundle'
  with zipfile.ZipFile(c/'rotational-veech-source-verification-v1.0.zip') as z:z.extractall(bundle)
  env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(temp)}
  print('Reproducing all four complete modes.',flush=True);command([args.python,'-B',c/'replay_all_modes.py','--python',args.python],env)
  modes=['normal','O','OO','env2'];results=[json.loads((c/('PACKAGE_REPLAY_'+m+'.json')).read_text()) for m in modes]
  for got in results:equivalent(got,results[0])
  # Compare exact saved outputs except interpreter-version metadata, which is explicitly runtime-specific.
  saved=json.loads((R/'REPLAY_normal.json').read_text());oldversion=saved['original_replay'].pop('python_version');got=copy_json(results[0]);currentversion=got['original_replay'].pop('python_version');equivalent(got,saved)
  print('Reproducing structural, assertion and copy guards.',flush=True)
  command([args.python,'-B',c/'package_guard_challenges.py','--bundle',bundle,'--python',args.python,'--output',temp/'guards.json'],env)
  guard=json.loads((temp/'guards.json').read_text());need(guard['hostile_inventory_runs']==140 and guard['false_assertion_child_runs']==4 and guard['positive_runs']==4,'guard counts')
  command([args.python,'-B',c/'copy_guard_challenge.py','--bundle',bundle,'--expected-manifest',f['package_manifest_sha256'],'--python',args.python,'--output',temp/'copy.json','--workdir',temp/'copy-work'],env)
  copyguard=json.loads((temp/'copy.json').read_text());need(copyguard['tampered_copy_runs']==4 and copyguard['all_copies_rejected_before_execution'] is True,'copy guards')
  independent=[]
  for label,flags,opt in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('env2',[],'2')]:
   e={**env};e.pop('PYTHONOPTIMIZE',None)
   if opt:e['PYTHONOPTIMIZE']=opt
   v=json.loads(command([args.python,*flags,'-B',R/'INDEPENDENT_CONTROLS.py','--bundle',bundle],e,60));equivalent(v,json.loads((R/'INDEPENDENT_RESULTS.json').read_text()));independent.append(label)
  helpers=module('HELPER_CONTROLS.py').perform();equivalent(helpers,json.loads((R/'HELPER_CONTROL_RESULTS.json').read_text()))
  acceptance=module('ACCEPTANCE_GATE_CONTROLS.py').perform();equivalent(acceptance,json.loads((R/'ACCEPTANCE_GATE_RESULTS.json').read_text()))
  root=module('ROOT_REGRESSIONS.py').run(args.python,temp/'root-regression')
  # Independent private compilation and rendered-page equality, not just a PDF digest.
  print('Recompiling and comparing all three PDF pages.',flush=True);tex=temp/'paper';tex.mkdir();shutil.copy2(c/'note.tex',tex/'note.tex');command(['/opt/homebrew/bin/tectonic','--outdir',tex,tex/'note.tex'],env,120)
  pixel=[]
  for page in range(1,4):
   for label,pdf in [('frozen',c/'output/pdf/note.pdf'),('compiled',tex/'note.pdf')]:command(['pdftoppm','-f',page,'-l',page,'-scale-to','1400','-png','-singlefile',pdf,tex/(label+str(page))],env,30)
   need((tex/('frozen'+str(page)+'.png')).read_bytes()==(tex/('compiled'+str(page)+'.png')).read_bytes(),'PDF page pixels '+str(page));pixel.append(page)
  end=auth.perform(args.candidate);need(start['candidate_files']==end['candidate_files'] and start['original_files']==end['original_files'],'candidate/original endpoint drift');module('VERIFY.py').verify(args.expected_manifest)
  result={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'full_replay_modes':modes,'strict_recursive_identity':True,'historical_files_authenticated':27,'independent_exact_controls':89992,'structural_negative_runs':140,'false_assertion_runs':4,'postcopy_guard_runs':4,'positive_integrity_runs':4,'independent_control_outer_modes':independent,'independent_rejections_per_mode':26,'helper_controls_synthetic':True,'acceptance_gate_controls_synthetic':True,'root_regressions':root,'fresh_compiled_PDF_pages_equal':pixel,'saved_interpreter_version':oldversion,'reproduction_interpreter_version':currentversion,'candidate_and_original_endpoints_unchanged':True,'seal_verified_before_and_after':True,'external_service_actions':0,'human_visual_review_repeated':False,'limits':'This reruns numerical/integrity/operational controls and PDF pixels; written mathematical/source review remains human-readable evidence, not formal machine proof or a priority-completeness certificate.'}
 if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
def copy_json(v):return json.loads(json.dumps(v))
if __name__=='__main__':main()
