#!/usr/bin/env python3
"""Authenticate this audit with an external digest, then reproduce into own tmp.
The entry program/interpreter must themselves be trusted before execution.
"""
import argparse,hashlib,json,os,re,stat,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).absolute().parent

def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'Duplicate JSON key');d[k]=v
 return d
def decode(b):return json.loads(b,object_pairs_hook=unique)
def run(args,env=None):
 p=subprocess.run([sys.executable,'-I','-B',*args],capture_output=True,env=env,timeout=600);need(p.returncode==0,p.stderr.decode(errors='replace'));return p.stdout

def main():
 p=argparse.ArgumentParser();p.add_argument('--expected-audit-manifest',required=True);a=p.parse_args();need(re.fullmatch('[0-9a-f]{64}',a.expected_audit_manifest) is not None,'Invalid external digest')
 path=HERE/'MANIFEST.json';need(stat.S_ISREG(path.lstat().st_mode),'Nonregular audit manifest');raw=path.read_bytes();need(sha(raw)==a.expected_audit_manifest,'Audit manifest anchor mismatch');m=decode(raw);need(m['schema']=='pr919-computation-family-public-v1' and m['problem_id']==30002555 and type(m['problem_id']) is int,'Wrong audit identity')
 expected={'MANIFEST.json'}
 for x in m['files']:
  need(set(x)=={'path','bytes','sha256'} and type(x['path']) is str and re.fullmatch('[A-Za-z0-9_.-]+',x['path']) is not None and x['path'] not in ('.','..') and x['path'] not in expected,'Unsafe audit member');expected.add(x['path']);q=HERE/x['path'];need(stat.S_ISREG(q.lstat().st_mode),'Nonregular audit member');b=q.read_bytes();need(type(x['bytes']) is int and len(b)==x['bytes'] and sha(b)==x['sha256'],'Audit member binding mismatch')
 need({q.name for q in HERE.iterdir()}-{'tmp','raw'}==expected,'Audit root inventory mismatch')
 for n in ('tmp','raw'):
  if (HERE/n).exists() or (HERE/n).is_symlink():need(stat.S_ISDIR((HERE/n).lstat().st_mode),'Ignored workspace is not a real directory')
 sys.path.insert(0,str(HERE));import HARDENED_VERIFY as H
 packet=HERE.parents[1]/'original/unsolved_math_prioritization/attempts/30002555';pins=H.load_pins();H.inventory(str(packet),pins);summary={'status':'PASS','audit_manifest_sha256':a.expected_audit_manifest,'source_files':27}
 with tempfile.TemporaryDirectory(prefix='reproduction-',dir=HERE/'tmp') as td:
  workspace=Path(td);env=H.sanitized_env(workspace);env['PYTHONOPTIMIZE']='2'
  authbase=[str(HERE/'AUTHENTICATE_GIT.py'),'--repo',str(HERE.parents[4]),'--packet',str(packet),'--snapshot',str(HERE.parents[1]/'ORIGINAL_SNAPSHOT.json'),'--pinset',str(HERE/'PINNED_SNAPSHOT.json')]
  run([*authbase,'--phase','end','--output',str(workspace/'git-start.json')],env)
  replay=decode(run([str(HERE/'HARDENED_VERIFY.py'),'--packet',str(packet),'--workspace',str(workspace)],env));need(replay['runs']==decode((HERE/'HISTORICAL_REPLAY.json').read_bytes())['runs'],'Historical replay changed');summary['historical_replays']=len(replay['runs']);summary['historical_mutation_rejections']=replay['historical_mutation_suite']['rejections']
  for filename,receipt,args in [('INDEPENDENT_CONTROLS.py','INDEPENDENT_RESULTS.json',[]),('HOSTILE_CASES.py','HOSTILE_RESULTS.json',[str(packet)])]:
   for flags in ([],['-O'],['-OO']):need(run([*flags,str(HERE/filename),*args],env)==(HERE/receipt).read_bytes(),'Receipt changed: '+filename)
  run([*authbase,'--phase','end','--output',str(workspace/'git-end.json')],env)
 summary.update(independent_controls=decode((HERE/'INDEPENDENT_RESULTS.json').read_bytes())['total_controls'],independent_hostile_rejections_per_mode=decode((HERE/'HOSTILE_RESULTS.json').read_bytes())['rejections'],source_unchanged=True)
 print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=='__main__':main()
