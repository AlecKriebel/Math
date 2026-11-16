#!/usr/bin/env python3
"""Only successor routing checks: two owned config includes and one RAM drift."""
from pathlib import Path
import ast,hashlib,json,os,subprocess,tempfile
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');O=P/'verification/next-three-production-audit-sol-20261116';N=P/'verification/next-three-production-release-sol-20261116';W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
source=(N/'release_next_three.py').read_bytes();expected='568c442fab8055c659113f3c9bdb453481f1bc106031e684bd04d104f8092010';assert hashlib.sha256(source).hexdigest()==expected
p=json.loads((N/'PLAN.json').read_bytes());mod=ast.parse(source);funcs=[n for n in mod.body if isinstance(n,ast.FunctionDef)and n.name in {'need','sha','pin','routing'}];assert len(funcs)==4
options=ast.literal_eval(next(n.value for n in mod.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='GIT_OPTIONS'for t in n.targets)))
ns={'hashlib':hashlib};exec(compile(ast.Module(body=funcs,type_ignores=[]),'<fully-read successor routing functions>','exec'),ns)
env={k:v for k,v in os.environ.items()if not k.startswith('GIT_')};env.update(GIT_OPTIONAL_LOCKS='0',GIT_INDEX_VERSION='2',GIT_TERMINAL_PROMPT='0')
include=None
calls=[]
def git(*args,opaque=False):
 cmd=['git','--no-optional-locks',*options]
 if include is not None:cmd+=['-c','include.path='+str(include)]
 cmd+=list(args);r=subprocess.run(cmd,cwd=W,env=env,capture_output=True,check=True);calls.append({'operation':list(args[:2]),'exit':r.returncode,'opaque':opaque});return r.stdout
ns['git']=git
baseline=ns['routing'](p);results=[{'case':'actual current effective singleton routing matches default','pass':baseline==json.loads((O/'V2_DEFAULT.stdout.json').read_bytes())['routing']}];assert results[0]['pass']
def reject(name,expected_state=None):
 try:ns['routing'](p,expected_state)
 except ValueError as e:results.append({'case':name,'rejected':True,'reason':str(e)})
 else:raise AssertionError('Routing case survived: '+name)
with tempfile.TemporaryDirectory(prefix='routing-fixtures-',dir=O)as d:
 include=Path(d)/'wrong-push.ini';include.write_text('[remote "origin"]\n\tpushurl = https://example.invalid/unapproved.git\n');reject('v1 ambient wrong-pushurl witness now fails closed')
 include=Path(d)/'duplicate-push.ini';include.write_text('[remote "origin"]\n\tpushurl = '+p['origin']+'\n\tpushurl = '+p['origin']+'\n');reject('duplicate effective push endpoints rejected')
 include=Path(d)/'new-benign-rule.ini';include.write_text('[url "https://unused.invalid/destination/"]\n\tpushInsteadOf = https://unused.invalid/source/\n');reject('changed relevant configuration fails old authorization despite same effective URLs',baseline)
include=None;normal_git=ns['git'];config_calls=0
def drift_git(*args,opaque=False):
 global config_calls
 result=normal_git(*args,opaque=opaque)
 if args[0]=='config':
  config_calls+=1
  if config_calls==2:result+=b'RAM-only simulated route-config drift'
 return result
ns['git']=drift_git;reject('configuration drift between before/after snapshots rejected')
print(json.dumps({'helper_SHA256':expected,'baseline_opaque_routing_pin':baseline,'cases':results,'all_cases_pass':True,'read_only_Git_subprocess_calls':len(calls),'remote_calls':0,'release_modes_executed':[],'global_config_or_W_or_Math_mutations':False,'scope':'Only actual read-only route queries with owned temporary includes, plus one RAM-only change to returned config bytes. No credential contents printed.'},indent=2))
