#!/usr/bin/env python3
"""Portable exact binding and replay. This checks artifacts, not the infinite theorem."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parent
PINS={
 'author/release/MANIFEST.json':'4396be5d06045d5f619dbded61846c83008b2ea6d578a2d913273f136f691c22',
 'author/AUTHOR_RELEASE.zip':'1cc570a6030395b0e4e3677d9c492cd8f0ab11402479f51053f0438d50b879eb',
 'independent_audit/AUDIT_MANIFEST.json':'727f564c65b203cf0361a75ee3b2fb520fe95a7f1e6164a32b4ccc21bf905410',
 'independent_audit/AUDIT_REPORT.md':'c2995207dd1e13238f7e9e565719737573e7190498ab98fa68d534d5b053ffaa',
 'INDEPENDENT_AUDIT.zip':'14a9fc064e9c2bc6927d5df36fbb14feaf7f5028d86fd40858b6b92b9f104131',
}
def require(ok,message):
 if not ok:raise RuntimeError(message)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def regular(p):return stat.S_ISREG(p.lstat().st_mode)
def inventory(root,expected):
 mp=root/'PUBLICATION_MANIFEST.json'
 require(regular(mp),'Nonregular publication manifest')
 raw=mp.read_bytes();require(digest(raw)==expected,'Publication manifest binding mismatch')
 obj=json.loads(raw);rows=obj['files'];records={r['path']:r for r in rows}
 require(obj['problem_id']=='30002129' and obj['queue_status']=='unsolved' and obj['turns']=='5/5','Wrong manifest scope')
 require(len(rows)==len(records)==32,'Wrong or duplicate inventory')
 for name in records:
  p=PurePosixPath(name)
  require(not p.is_absolute() and '..' not in p.parts and str(p)==name and '\\' not in name,'Unsafe inventory path')
 for p in root.rglob('*'):
  require(not p.is_symlink(),'Symlink forbidden')
  require(p.is_dir() or regular(p),'Special file forbidden')
 actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
 dirs={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
 require(actual==set(records)|{'PUBLICATION_MANIFEST.json'},'Nonexact publication file inventory')
 require(dirs=={'author','author/release','independent_audit'},'Nonexact publication directory inventory')
 payload={}
 for name,row in records.items():
  body=(root/name).read_bytes()
  require(len(body)==row['bytes'] and digest(body)==row['sha256'],'Publication member mismatch: '+name)
  payload[name]=body
 for name,pin in PINS.items():require(digest(payload[name])==pin,'Frozen pin mismatch: '+name)
 for directory,manifest in [('author/release','MANIFEST.json'),('independent_audit','AUDIT_MANIFEST.json')]:
  entries=json.loads(payload[directory+'/'+manifest])['files']
  require(len({r['path'] for r in entries})==len(entries),'Duplicate inner inventory')
  require({p.name for p in (root/directory).iterdir()}=={r['path'] for r in entries}|{manifest},'Nonexact inner inventory')
  for row in entries:
   body=payload[directory+'/'+row['path']]
   require(len(body)==row['bytes'] and digest(body)==row['sha256'],'Frozen member mismatch')
 for archive,directory in [('author/AUTHOR_RELEASE.zip','author/release'),('INDEPENDENT_AUDIT.zip','independent_audit')]:
  require(len(payload[archive])=={'author/AUTHOR_RELEASE.zip':19090,'INDEPENDENT_AUDIT.zip':26853}[archive],'Wrong archive size')
  with zipfile.ZipFile(root/archive) as z:
   infos=z.infolist();names=[i.filename for i in infos]
   require(len(names)==len(set(names)),'Duplicate ZIP member')
   require(set(names)=={p.name for p in (root/directory).iterdir()},'Nonexact ZIP inventory')
   for info in infos:
    mode=(info.external_attr>>16)&0xffff
    require(not info.is_dir() and '/' not in info.filename and '\\' not in info.filename,'Unsafe ZIP member')
    require(not mode or stat.S_ISREG(mode),'Nonregular ZIP member')
    require(z.read(info)==payload[directory+'/'+info.filename],'ZIP member bytes differ')
 status=json.loads(payload['PUBLICATION_STATUS.json']);audit=json.loads(payload['independent_audit/AUDIT_RESULTS.json'])
 require(status['queue_status']=='unsolved' and status['turns']=='5/5','Wrong queue gate')
 require(audit['verdict']=='PASS_SCOPED_UNSOLVED_INVESTIGATION' and audit['required_corrections']==[],'Wrong audit verdict')
 require(not status['full_resolution'] and not status['novelty_certified'] and not status['global_current_openness_certified'],'Unsupported scope promotion')
 require(not status['finite_computations_are_theorem_proof'] and not status['human_peer_review'] and not status['formal_verification'],'Unsupported evidence promotion')
 return payload,raw

def corruption_tests(root,expected):
 names=['changed_author_file','missing_audit_file','extra_file','extra_directory','symlink','changed_manifest','changed_archive','changed_wrapper']
 for name in names:
  with tempfile.TemporaryDirectory(prefix='rotation-publication-corruption-') as td:
   dst=Path(td)/'packet';shutil.copytree(root,dst)
   if name=='changed_author_file':p=dst/'author/release/RESULT.md';p.write_bytes(p.read_bytes()+b'corruption')
   elif name=='missing_audit_file':(dst/'independent_audit/AUDIT_REPORT.md').unlink()
   elif name=='extra_file':(dst/'unknown.txt').write_bytes(b'extra')
   elif name=='extra_directory':(dst/'unknown').mkdir()
   elif name=='symlink':p=dst/'README.md';p.unlink();p.symlink_to(dst/'RESEARCH_LOG.md')
   elif name=='changed_manifest':p=dst/'PUBLICATION_MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
   elif name=='changed_archive':p=dst/'INDEPENDENT_AUDIT.zip';p.write_bytes(p.read_bytes()+b'corruption')
   elif name=='changed_wrapper':p=dst/'verify_publication.py';p.write_bytes(p.read_bytes()+b'\n# changed\n')
   try:inventory(dst,expected)
   except (RuntimeError,FileNotFoundError,KeyError,ValueError,zipfile.BadZipFile):continue
   raise RuntimeError('Accepted corruption: '+name)
 return names

def replay(payload):
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
 env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
 jobs=[
  ('author_math','author/release/verify_math.py',[],'author/release/MATH_CHECKS.json'),
  ('author_bundle','author/release/verify_bundle.py',['--expected-manifest',PINS['author/release/MANIFEST.json'],'--replay','--self-test'],'independent_audit/AUTHOR_NORMAL_REPLAY.json'),
  ('independent_math','independent_audit/independent_controls.py',[],'independent_audit/INDEPENDENT_CONTROLS.json'),
  ('oracle_comparison','independent_audit/compare_oracles.py',[str(ROOT/'author/release')],'independent_audit/ORACLE_COMPARISON.json'),
  ('independent_binding','independent_audit/audit_binding.py',[str(ROOT/'author')],'independent_audit/EXACT_BINDING.json'),
 ]
 out=[]
 for optimized in (False,True):
  for name,script,args,expected in jobs:
   cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(ROOT/script)]+args
   actual=subprocess.check_output(cmd,cwd=tempfile.gettempdir(),env=env)
   require(actual==payload[expected],'Replay mismatch: '+name+(' -O' if optimized else ''))
   out.append({'name':name,'direct_optimized':optimized,'byte_exact':True})
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest',required=True);ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
 require(sys.version_info>=(3,10),'Python 3.10+ required')
 payload,raw=inventory(ROOT,args.expected_manifest)
 replays=replay(payload)
 mutations=corruption_tests(ROOT,args.expected_manifest) if args.self_test else []
 after,after_manifest=inventory(ROOT,args.expected_manifest)
 require(after==payload and after_manifest==raw,'Replay changed original bytes')
 print(json.dumps({'status':'PASS_PUBLICATION_REPLAY','problem_id':'30002129','queue_status':'unsolved','turns':'5/5','packet_files':33,'frozen_files_preserved':28,'publication_manifest_sha256':args.expected_manifest,'replays':replays,'rejected_publication_corruptions':mutations,'originals_preserved':True,'full_resolution':False,'finite_controls_are_theorem_proof':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
