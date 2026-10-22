#!/usr/bin/env python3
"""Read-only packet checks and finite regression replay; not a formal proof."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import subprocess
import sys
import zipfile

HERE=Path(__file__).resolve().parent
ARCHIVES={
 'NEGATIVE_P_ALEKSANDROV_30004953_AUTHOR_SAFE_FREEZE.zip':(24951,'63b3aee3a0e44e17b4ed2fc3d01065708f87dd3dd7e5fee397e85683c1a300e1','author',10),
 'NEGATIVE_P_ALEKSANDROV_30004953_INDEPENDENT_AUDIT.zip':(25293,'231acecc5bfb1ce876d97d8d309e3b17bd14358b82c3e2e4e3c7431fe004d11c','audit',11),
}

def require(ok,msg):
 if not ok: raise RuntimeError(msg)

def metadata(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def inventory():
 result={}
 for p in HERE.rglob('*'):
  if '__pycache__' in p.parts: continue
  require(not p.is_symlink(),'Symbolic link in packet: '+str(p))
  require(p.is_file() or p.is_dir(),'Nonregular entry in packet')
  if p.is_file():result[p.relative_to(HERE).as_posix()]=metadata(p.read_bytes())
 return result

def integrity():
 manifest=json.loads((HERE/'PUBLICATION_MANIFEST.json').read_text())
 require(manifest['problem_id']==30004953 and manifest['full_problem_solved'] is False,'Wrong publication scope')
 expected={'PUBLICATION_MANIFEST.json'}
 for row in manifest['files']:
  name=row['path'];path=PurePosixPath(name)
  require(not path.is_absolute() and '..' not in path.parts and name not in expected,'Unsafe or duplicate manifest path')
  expected.add(name)
  p=HERE/name
  require(p.is_file() and not p.is_symlink(),'Missing or linked manifest member: '+name)
  require(metadata(p.read_bytes())=={'bytes':row['bytes'],'sha256':row['sha256']},'Manifest byte/hash mismatch: '+name)
 actual=inventory();require(set(actual)==expected,'Recursive file inventory mismatch')
 frozen=json.loads((HERE/'FROZEN_INPUTS.json').read_text());pinned={}
 for name,(size,sha,dest,count) in ARCHIVES.items():
  b=(HERE/name).read_bytes();require(metadata(b)==dict(bytes=size,sha256=sha),'Frozen archive mismatch: '+name);pinned[name]=metadata(b)
  with zipfile.ZipFile(HERE/name) as z:
   names=z.namelist();require(len(names)==len(set(names))==count,'Archive inventory mismatch')
   require(all(Path(n).name==n and n not in {'','.','..'} for n in names),'Unsafe archive member')
   fs={p.name for p in (HERE/dest).iterdir() if '__pycache__' not in p.parts}
   require(fs==set(names),'Archive/extracted inventory mismatch')
   for n in names:
    b=z.read(n);require(b==(HERE/dest/n).read_bytes(),'Archive/extracted byte mismatch: '+dest+'/'+n);pinned[dest+'/'+n]=metadata(b)
 require(frozen==pinned,'Frozen input binding mismatch')
 scope=json.loads((HERE/'PUBLICATION.json').read_text())
 require(scope['problem_id']==30004953 and scope['rank']==785,'Wrong target')
 require(scope['status']=='unsolved' and scope['turns']=='5/5','Wrong queue disposition')
 for flag in ['general_problem_solved','mandatory_mathematical_edits','human_peer_review','formal_certificate','interval_certificate','editorial_acceptance','novelty_verified','priority_claim']:
  require(scope[flag] is False,'Overstated scope: '+flag)
 require(scope['independent_audit']=='PASS_SCOPED_PARTIALS','Wrong audit verdict')
 require(scope['independent_controls']==100,'Wrong independent control count')
 require('10.3770/j.issn:2095-2651.2026.03.009' in scope['yang_hu_current_status'],'Missing authenticated source update')
 require('uninspected' in scope['yang_hu_current_status'] and 'unverified' in scope['yang_hu_current_status'],'Missing overlap limitation')
 binding=json.loads((HERE/'SOURCE_BINDING.json').read_text());delta=binding['queue_delta']
 require(binding['problem_id']==30004953 and binding['statement_sha256']==scope['statement_sha256'] and binding['review_sha256']==scope['review_sha256'],'Source identity mismatch')
 require(delta['Status']==['queued','unsolved'] and delta['Turns']==['0/5','5/5'],'Wrong queue patch scope')
 require(all(delta[k] is True for k in ['all_other_bytes_preserved','stale_embedded_header_preserved','Findings_Chat_DOI_unchanged']),'Queue preservation guard failed')
 ir=json.loads((HERE/'audit/INDEPENDENT_RESULTS.json').read_text());require(ir['checks']==100 and ir['full_problem_solved'] is False,'Wrong finite control scope')
 return actual

def run(script,*args,optimized=False):
 cmd=[sys.executable]+(['-O'] if optimized else [])+[str(HERE/script),*map(str,args)]
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
 result=subprocess.run(cmd,cwd=HERE,capture_output=True,text=True,env=env)
 require(result.returncode==0,'Replay failed: '+str(cmd)+'\n'+result.stdout+result.stderr)
 return {'script':script,'mode':'optimized' if optimized else 'normal','exit_code':0}

def main():
 require(sys.argv[1:] in [[],['--integrity-only']],'Usage: test_publication_integrity.py [--integrity-only]')
 before=integrity();runs=[]
 if not sys.argv[1:]:
  for optimized in [False,True]:
   for script in ['author/verify_manifest.py','author/verify_math.py','audit/verify_audit.py','audit/independent_checks.py']:
    runs.append(run(script,optimized=optimized))
   runs.append(run('audit/replay_author.py',HERE/'NEGATIVE_P_ALEKSANDROV_30004953_AUTHOR_SAFE_FREEZE.zip',optimized=optimized))
 require(integrity()==before,'Packet changed during replay')
 print(json.dumps({'status':'PASS','packet_files':len(before),'frozen_files_and_archives':23,'archive_bytes_preserved':True,'recursive_inventory_checked':True,'full_problem_solved':False,'disposition':'UNSOLVED 5/5','independent_high_precision_controls':100,'interval_or_formal_proof_certificate':False,'runs':runs},indent=2,sort_keys=True))

if __name__=='__main__':main()
