#!/usr/bin/env python3
"""Pinned all-27 gate; authenticate before isolated copied-code execution.

Trust this file and the embedded pinset hash externally before use. This is
not an operating-system sandbox and is not safe against a concurrent local
attacker replacing directory ancestors or the trusted interpreter.
"""
import argparse, hashlib, json, os, re, stat, subprocess, sys, tempfile
from pathlib import Path
PINSET_SHA='1067526140572bb39644eab14a1887fe13327f9e2450f202bc9eedf05c338807'
AUTHOR='f7b959531c352611c5c9b9d0c2cb57bcb865de9399d65dbd66c4fabef3a88e59'
AUDIT='f8253e86c12c287519a511681d28ec8bcd1206836a3c88b5468c3590db4ea172'
OUTER='a7f24f30d76ca7e53da932dfc1f19deac67f13a675742175274e30ca767832f8'
VERIFIER='07ed9f87820a8cbaa10deec92fbf14b68a61e969e8bf849d8c5484eac4aa5374'
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 out={}
 for k,v in pairs:
  need(k not in out,'Duplicate JSON key');out[k]=v
 return out
def decode(raw):return json.loads(raw,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(RuntimeError('Nonfinite JSON constant')))
def same_schema(value,model):
 need(type(value) is type(model),'Output type mismatch')
 if type(model) is dict:
  need(set(value)==set(model),'Output object keys mismatch')
  for k,v in model.items():same_schema(value[k],v)
 elif type(model) is list:
  need(len(value)==len(model),'Output array length mismatch')
  for x,y in zip(value,model):same_schema(x,y)
def load_pins():
 p=Path(__file__).absolute().parent/'PINNED_SNAPSHOT.json';raw=p.read_bytes();need(sha(raw)==PINSET_SHA,'Independent pinset anchor mismatch');pins=decode(raw)
 need(pins['head']=='704685791ec0053dc0a52590fdef49ed4aae61d9' and type(pins['problem_id']) is int and pins['problem_id']==30002555 and len(pins['files'])==27,'Pinset identity mismatch')
 return pins['files']
def canonical_root(raw):
 need(type(raw) is str and raw.startswith('/') and '\\' not in raw,'Root must be absolute')
 need(all(p not in ('.','..','') for p in raw.split('/')[1:]),'Lexical root path alias')
 need(raw==os.path.realpath(raw),'Root path alias or symlink')
 root=Path(raw)
 for p in [root,*root.parents]:need(stat.S_ISDIR(p.lstat().st_mode),'Symlink/non-directory root ancestor')
 return root
def inventory(raw,pins):
 root=canonical_root(raw);expected_dirs={str(p) for n in pins for p in Path(n).parents if str(p)!='.'};files={};dirs=set()
 for directory,subdirs,names in os.walk(root,followlinks=False):
  for name in subdirs+names:
   p=Path(directory)/name;rel=p.relative_to(root).as_posix();mode=p.lstat().st_mode
   need(not stat.S_ISLNK(mode),'Linked packet member')
   if stat.S_ISDIR(mode):dirs.add(rel)
   else:
    need(stat.S_ISREG(mode),'Special packet member');need(rel in pins,'Unexpected packet file');need(p.stat().st_size==pins[rel]['bytes'],'Pinned size mismatch')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as f:
     before=os.fstat(f.fileno());need(stat.S_ISREG(before.st_mode),'Nonregular opened member');data=f.read(pins[rel]['bytes']+1);after=os.fstat(f.fileno())
    need((before.st_ino,before.st_dev,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_dev,after.st_size,after.st_mtime_ns),'Concurrent member change')
    need(len(data)==pins[rel]['bytes'] and sha(data)==pins[rel]['sha256'],'Pinned bytes mismatch');files[rel]=data
 need(set(files)==set(pins) and dirs==expected_dirs,'Closed packet inventory mismatch')
 # Parse every JSON using duplicate/nonfinite rejection after byte authentication.
 for name,data in files.items():
  if name.endswith('.json'):decode(data)
 return files

def sanitized_env(workspace):
 # Historical reviewers use tempfile; force every mutation underneath this audit.
 env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
 env.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(workspace),TMP=str(workspace),TEMP=str(workspace))
 return env

def execute_checked(root,rel,args,flags,pins,env,timeout=180):
 # Reauthenticate the entire closed copy, including this specific checker, immediately before every execution.
 files=inventory(str(root),pins);need(sha(files[rel])==pins[rel]['sha256'],'Copied checker reauthentication failed')
 result=subprocess.run([sys.executable,'-I','-B',*flags,str(root/rel),*args],cwd=root,env=env,capture_output=True,timeout=timeout)
 need(result.returncode==0,'Authenticated execution failed '+rel+': '+result.stderr.decode(errors='replace'));need(not result.stderr,'Unexpected stderr '+rel)
 parsed=decode(result.stdout);need(type(parsed) is dict and type(parsed.get('status')) is str and parsed['status']=='PASS','Output status/schema mismatch')
 return result.stdout,parsed

def replay(root,pins,env):
 specs=[('public/CHECKS.py',[],'public/CHECK_RESULTS.json','total_exact_checks',1996),('audit_rotational_independent/public/INDEPENDENT_CHECKS.py',[str(root/'public')],'audit_rotational_independent/public/INDEPENDENT_RESULTS.json','total_controls',4160),('reviewer_b/public/INDEPENDENT_CHECKS.py',[],'reviewer_b/public/INDEPENDENT_RESULTS.json','independent_exact_checks',3055),('public/VERIFY.py',[AUTHOR],None,'total_exact_checks_per_mode',1996),('audit_rotational_independent/public/VERIFY_AUDIT.py',[AUDIT,str(root/'public')],None,'independent_controls_per_mode',4160)]
 runs=[]
 for mode,flags in [('ordinary',[]),('optimized',['-O']),('double_optimized',['-OO'])]:
  for rel,args,receipt,key,count in specs:
   raw,parsed=execute_checked(root,rel,args,flags,pins,env)
   need(type(parsed.get(key)) is int and parsed[key]==count,'Wrong exact count')
   if receipt:
    model=decode((root/receipt).read_bytes());same_schema(parsed,model);need(raw==(root/receipt).read_bytes(),'Historical receipt mismatch')
   elif rel=='public/VERIFY.py':
    same_schema(parsed,{'status':'','manifest_sha256':'','verified_member_count':0,'replay_modes':['',''],'total_exact_checks_per_mode':0});need(parsed['manifest_sha256']==AUTHOR and parsed['verified_member_count']==8 and parsed['replay_modes']==['ordinary','optimized'],'Author verifier output mismatch')
   else:
    same_schema(parsed,{'status':'','audit_manifest_sha256':'','author_manifest_sha256':'','verified_member_count':0,'independent_controls_per_mode':0,'replay_modes':['','']});need(parsed['audit_manifest_sha256']==AUDIT and parsed['author_manifest_sha256']==AUTHOR and parsed['verified_member_count']==5,'Audit wrapper output mismatch')
   runs.append({'script':rel,'mode':mode,'stdout_sha256':sha(raw),'receipt_byte_match':receipt is not None,'exact_count':count})
 child_receipts=[{k:v for k,v in r.items() if k!='exact_count'} for r in runs]
 # Outer wrapper independently repeats its own entire 15-child sequence under all three top-level modes.
 for mode,flags in [('ordinary',[]),('optimized',['-O']),('double_optimized',['-OO'])]:
  raw,p=execute_checked(root,'VERIFY_PUBLICATION.py',['--packet',str(root),'--expected-manifest',OUTER],flags,pins,env)
  model={'status':'','problem_id':0,'publication_manifest_sha256':'','bound_files':0,'check_only':False,'replays':[{'script':'','mode':'','stdout_sha256':'','receipt_byte_match':False} for _ in range(15)],'limits':''};same_schema(p,model)
  need(p['problem_id']==30002555 and p['bound_files']==26 and p['check_only'] is False and p['publication_manifest_sha256']==OUTER,'Outer wrapper output identity mismatch')
  need(p['replays']==child_receipts,'Outer child receipts disagree')
  runs.append({'script':'VERIFY_PUBLICATION.py','mode':mode,'stdout_sha256':sha(raw),'internal_replays':15})
 raw,p=execute_checked(root,'TEST_MUTATIONS.py',['--packet',str(root),'--expected-manifest',OUTER,'--expected-verifier',VERIFIER],[],pins,env)
 model=decode((root/'MUTATION_RESULTS.json').read_bytes());same_schema(p,model);need(raw==(root/'MUTATION_RESULTS.json').read_bytes(),'Mutation suite receipt mismatch')
 return {'runs':runs,'historical_mutation_suite':{'mutation_classes':p['mutation_classes'],'rejections':p['rejections'],'stdout_sha256':sha(raw),'receipt_byte_match':True}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--packet',required=True);p.add_argument('--workspace',required=True);p.add_argument('--check-only',action='store_true');p.add_argument('--output');a=p.parse_args();pins=load_pins();files=inventory(a.packet,pins);result={'status':'PASS','pinned_files':len(files),'pinset_sha256':PINSET_SHA,'check_only':a.check_only,'incoming_PYTHONOPTIMIZE':os.environ.get('PYTHONOPTIMIZE'),'python_version':sys.version,'parent_optimize':sys.flags.optimize}
 if not a.check_only:
  workspace=canonical_root(a.workspace)
  with tempfile.TemporaryDirectory(prefix='replay-',dir=workspace) as td:
   root=Path(td)/'packet';root.mkdir()
   for rel,data in files.items():
    q=root/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
   need(inventory(str(root),pins)==files,'Isolated copy reauthentication failed');env=sanitized_env(workspace);poisoned=dict(env,PYTHONOPTIMIZE='2')
   c=subprocess.run([sys.executable,'-I','-B','-c','import sys; print(sys.flags.optimize); assert False, "sentinel assertion must remain active"'],env=poisoned,capture_output=True)
   need(c.returncode!=0 and c.stdout==b'0\n' and b'AssertionError: sentinel assertion must remain active' in c.stderr,'Nonoptimized assert-False sentinel failed')
   result['inherited_optimize_2_assert_false_child']={'optimize':0,'assertion_active':True};result.update(replay(root,pins,env));need(inventory(str(root),pins)==files,'Copied packet changed after execution')
 need(inventory(a.packet,pins)==files,'Original packet changed after execution')
 out=json.dumps(result,indent=2,sort_keys=True)+'\n'
 if a.output:Path(a.output).write_text(out)
 print(out,end='')
if __name__=='__main__':main()
