#!/usr/bin/env python3
"""Portable artifact binding and finite replay; not an analytic proof certificate."""
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

ROOT=Path(__file__).resolve().parent
PINS={
 'author/MANIFEST.json':'e9b0934c31eb18e76e4c99f3bdca5c362ce5519f4ecc4efe551eeef6ea4b6019',
 'independent_audit/MANIFEST.json':'757a97f78d0926e6706b3c5b939ef500712896fb0320e06cfa90cf845ec5c924',
 'independent_audit/AUDIT.md':'eb7b4200801453f7199179c4faf5651269d4336b3861f258330e18bf50a3b2e1',
}
def require(ok,message):
 if not ok:raise RuntimeError(message)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def regular(p):return stat.S_ISREG(p.lstat().st_mode)
def safe_name(name):
 p=PurePosixPath(name)
 return bool(name) and not p.is_absolute() and '..' not in p.parts and str(p)==name and '\\' not in name

def inventory(root,expected):
 mp=root/'PUBLICATION_MANIFEST.json'
 require(regular(mp),'Nonregular publication manifest')
 raw=mp.read_bytes();require(digest(raw)==expected,'Publication manifest binding mismatch')
 obj=json.loads(raw);rows=obj['files'];records={r['path']:r for r in rows}
 require(obj['problem_id']=='30002180' and obj['queue_status']=='unsolved' and obj['turns']=='5/5','Wrong publication scope')
 require(len(rows)==len(records)==33,'Wrong or duplicate inventory')
 require(all(safe_name(name) for name in records),'Unsafe inventory path')
 for p in root.rglob('*'):
  require(not p.is_symlink(),'Symlink forbidden')
  require(p.is_dir() or regular(p),'Special file forbidden')
 actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
 dirs={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
 require(actual==set(records)|{'PUBLICATION_MANIFEST.json'},'Nonexact publication file inventory')
 require(dirs=={'author','independent_audit'},'Nonexact publication directory inventory')
 payload={}
 for name,row in records.items():
  body=(root/name).read_bytes()
  require(len(body)==row['bytes'] and digest(body)==row['sha256'],'Publication member mismatch: '+name)
  payload[name]=body
 for name,pin in PINS.items():require(digest(payload[name])==pin,'Frozen pin mismatch: '+name)
 for directory,count in [('author',16),('independent_audit',11)]:
  entries=json.loads(payload[directory+'/MANIFEST.json'])['files']
  require(len(entries)==len({r['path'] for r in entries})==count,'Wrong inner inventory')
  require(all(safe_name(r['path']) and '/' not in r['path'] for r in entries),'Unsafe inner path')
  require({p.name for p in (root/directory).iterdir()}=={r['path'] for r in entries}|{'MANIFEST.json'},'Nonexact inner inventory')
  for row in entries:
   body=payload[directory+'/'+row['path']]
   require(len(body)==row['bytes'] and digest(body)==row['sha256'],'Frozen member mismatch')
 binding=json.loads(payload['independent_audit/PACKET_BINDING.json'])['packets']['safe_packet_v2']
 require(binding['manifest_sha256']==PINS['author/MANIFEST.json'],'Wrong audit target')
 require(binding['manifest_bytes']==len(payload['author/MANIFEST.json']),'Wrong audited manifest size')
 require(binding['files']==json.loads(payload['author/MANIFEST.json'])['files'],'Audit binding differs')
 status=json.loads(payload['PUBLICATION_STATUS.json']);audit=json.loads(payload['independent_audit/RESULTS.json'])
 require(status['queue_status']=='unsolved' and status['turns']=='5/5','Wrong queue gate')
 require(audit['verdict']=='PASS_SCOPED_UNSOLVED_5_OF_5' and audit['mandatory_corrections']==[],'Wrong audit verdict')
 require(audit['target_manifest_sha256']==PINS['author/MANIFEST.json'],'Wrong audit target pin')
 require(audit['author_assertions_passed']==3274 and audit['independent_assertions_passed']==8705,'Wrong check counts')
 for key in ['full_resolution','novelty_certified','global_current_openness_certified','finite_computations_are_theorem_proof','human_peer_review','formal_verification']:
  require(status[key] is False,'Unsupported evidence promotion: '+key)
 return payload,raw

def corruption_tests(root,expected):
 names=['changed_author_file','missing_audit_file','extra_file','extra_directory','symlink','changed_manifest','changed_inner_manifest','changed_wrapper','changed_audit_report']
 for name in names:
  with tempfile.TemporaryDirectory(prefix='jet-curvature-corruption-') as td:
   dst=Path(td)/'packet';shutil.copytree(root,dst)
   if name=='changed_author_file':p=dst/'author/STATEMENT.md';p.write_bytes(p.read_bytes()+b'corruption')
   elif name=='missing_audit_file':(dst/'independent_audit/RESULTS.json').unlink()
   elif name=='extra_file':(dst/'unknown.txt').write_bytes(b'extra')
   elif name=='extra_directory':(dst/'unknown').mkdir()
   elif name=='symlink':p=dst/'README.md';p.unlink();p.symlink_to(dst/'RESEARCH_LOG.md')
   elif name=='changed_manifest':p=dst/'PUBLICATION_MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
   elif name=='changed_inner_manifest':p=dst/'author/MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
   elif name=='changed_wrapper':p=dst/'verify_publication.py';p.write_bytes(p.read_bytes()+b'\n# changed\n')
   elif name=='changed_audit_report':p=dst/'independent_audit/AUDIT.md';p.write_bytes(p.read_bytes()+b'corruption')
   try:inventory(dst,expected)
   except (RuntimeError,FileNotFoundError,KeyError,ValueError):continue
   raise RuntimeError('Accepted corruption: '+name)
 return names

def replay(payload):
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
 env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
 jobs=[
  ('author_exact','author/verify_exact.py','author/EXACT_RESULTS.json'),
  ('independent_exact','independent_audit/independent_controls.py','independent_audit/INDEPENDENT_RESULTS.json'),
  ('author_manifest','author/verify_manifest.py',None),
  ('audit_manifest','independent_audit/verify_audit.py',None),
 ]
 out=[]
 for name,script,expected in jobs:
  actual=subprocess.check_output([sys.executable,'-B',str(ROOT/script)],cwd=tempfile.gettempdir(),env=env)
  parsed=json.loads(actual)
  if expected:
   require(actual==payload[expected],'Byte-exact replay mismatch: '+name)
  elif name=='author_manifest':
   require(parsed=={'files_verified':16,'manifest_verified':True,'original_problem_solved':False},'Author manifest replay mismatch')
  else:
   require(parsed=={'audit_manifest_verified':True,'files_verified':11,'independent_controls_reproduced':True,'original_problem_solved':False},'Audit manifest replay mismatch')
  out.append({'name':name,'optimization_disabled':True,'passed':True,'output_byte_exact':bool(expected)})
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest',required=True);ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
 require(sys.version_info>=(3,10),'Python 3.10+ required')
 payload,raw=inventory(ROOT,args.expected_manifest)
 replays=replay(payload)
 mutations=corruption_tests(ROOT,args.expected_manifest) if args.self_test else []
 after,after_manifest=inventory(ROOT,args.expected_manifest)
 require(after==payload and after_manifest==raw,'Replay changed original bytes')
 print(json.dumps({'status':'PASS_PUBLICATION_REPLAY','problem_id':'30002180','queue_status':'unsolved','turns':'5/5','packet_files':34,'frozen_files_preserved':29,'publication_manifest_sha256':args.expected_manifest,'replays':replays,'author_assertions':3274,'independent_assertions':8705,'rejected_publication_corruptions':mutations,'originals_preserved':True,'full_resolution':False,'finite_controls_are_theorem_proof':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
