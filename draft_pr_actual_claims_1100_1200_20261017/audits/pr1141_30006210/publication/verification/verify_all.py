#!/usr/bin/env python3
"""Offline exact mathematical diagnostics. Python3.10+ stdlib; never publish."""
from pathlib import Path
import ast,copy,hashlib,json,platform,shutil,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parents[1]
def need(c,s):
 if not c:raise RuntimeError(s)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def compare(g,w,path='result'):
 need(type(g) is type(w),'Type mismatch '+path)
 if isinstance(w,dict):
  need(set(g)==set(w),'Keys mismatch '+path)
  for k in w:compare(g[k],w[k],path+'.'+k)
 elif isinstance(w,list):
  need(len(g)==len(w),'Length mismatch '+path)
  for i,(a,b) in enumerate(zip(g,w)):compare(a,b,path+'['+str(i)+']')
 else:need(g==w,'Value mismatch '+path)
def check_member(root,n,w):
 q=Path(n);need(not q.is_absolute() and '..' not in q.parts,'Unsafe member '+n)
 f=root/q;need(not f.is_symlink() and pin(f)==w,'Fingerprint mismatch '+n)
def normalize(value,row,optimized):
 v=copy.deepcopy(value)
 if row['runtime_kind']=='separator':
  need(v['runtime']['python']==sys.version,'Unexpected separator interpreter')
  need(v['runtime']['optimization']==int(optimized),'Unexpected separator mode')
 if row['runtime_kind']=='target':
  need(v['python_version']==platform.python_version(),'Unexpected target interpreter')
  need(v['optimized'] is optimized,'Unexpected target mode')
 for path in row['drop_paths']:
  node=v
  for k in path[:-1]:node=node[k]
  del node[path[-1]]
 return v
def expected_semantics(value,row):
 v=copy.deepcopy(value)
 for path in row['drop_paths']:
  node=v
  for k in path[:-1]:node=node[k]
  del node[path[-1]]
 return v
def main():
 plan=json.loads((HERE/'verification/CONTROL_PLAN.json').read_text());members=json.loads((HERE/'verification/AUDIT_MEMBERS.json').read_text())
 audit=HERE/plan['source_prefix'] if (HERE/plan['source_prefix']).is_dir() else HERE.parent
 for n,w in members.items():check_member(audit,n,w)
 need(pin(audit/'inputs/PROOF.md')['sha256']==plan['source_proof_sha256'],'Source proof changed')
 if (HERE/'SOURCE_MANIFEST.json').exists():
  for n,w in json.loads((HERE/'SOURCE_MANIFEST.json').read_text()).items():check_member(HERE,n,w)
 runs=[];guards=[]
 with tempfile.TemporaryDirectory(prefix='boolean-compatibility-controls-') as temp:
  mirror=Path(temp)/plan['source_prefix']
  for n in members:
   target=mirror/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(audit/n,target)
  for row in plan['controls']:
   script=mirror/row['program'];need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(script.read_text()))),'Optimizable assert in '+row['program'])
   expected=json.loads((mirror/row['expected']).read_text());semantic=expected_semantics(expected,row)
   for optimized in (False,True):
    cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(script)]
    if row['output_argument']:cmd+=['--output',str(Path(temp)/'last-output.json')]
    r=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=180)
    need(r.returncode==0 and not r.stderr,'Control failed '+row['program']+' '+r.stderr[-1500:])
    actual=json.loads(r.stdout);compare(normalize(actual,row,optimized),semantic)
    runs.append({'program':row['program'],'optimized':optimized,'all_mathematical_fields_exactly_equal':True,'result':actual})
    for mutant in row['mutants']:
     if 'code' in mutant:
      code="import importlib.util; s=importlib.util.spec_from_file_location('m',"+repr(str(script))+"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "+mutant['code']
      badcmd=[sys.executable,'-B']+(['-O'] if optimized else [])+['-c',code]
     else:badcmd=cmd+mutant['args']
     bad=subprocess.run(badcmd,cwd='/',capture_output=True,text=True,timeout=30)
     need(bad.returncode!=0 and mutant['diagnostic'] in bad.stdout+bad.stderr,'Incorrect-result guard inactive '+row['program']+' '+mutant['name'])
     guards.append({'program':row['program'],'optimized':optimized,'mutant':mutant['name'],'exit_code':bad.returncode,'expected_diagnostic_present':True})
 for n,w in members.items():check_member(audit,n,w)
 need(len(runs)==8 and len(guards)==40,'Incomplete execution plan')
 print(json.dumps({'status':'PASS','authored_audit_members_checked':len(members),'source_inputs_checked':plan['source_input_count'],'runs':runs,'actual_failure_guards':guards,'comparison':'All mathematical fields exact; only explicitly listed and validated process/runtime fields excluded.','scope':'Finite exact diagnostics supplement the universal written proof and primary source interfaces; no arbitrary-dimensional or formal proof certificate.'},indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
