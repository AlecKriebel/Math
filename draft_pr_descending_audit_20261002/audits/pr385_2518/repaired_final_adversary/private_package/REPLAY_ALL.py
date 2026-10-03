#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--source-dir',type=Path);args=ap.parse_args()
def verify(e,path):
 b=path.read_bytes();assert len(b)==e['bytes'],str(path)
 assert hashlib.sha256(b).hexdigest()==e['sha256'],str(path)
 if 'git_blob_sha' in e:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha'],str(path)
bound=0
for t in range(1,6):
 m=json.loads((p/f'TURN_{t}_MANIFEST.json').read_text())
 if t>1:assert m['previous_manifest_sha256']==hashlib.sha256((p/f'TURN_{t-1}_MANIFEST.json').read_bytes()).hexdigest()
 for e in m['files']:verify(e,p/e['path']);bound+=1
f=p/'FINAL_AUTHOR_MANIFEST.json'
if f.exists():
 for e in json.loads(f.read_text())['files']:verify(e,p/e['path'])
counts=[]
for t in range(1,6):
 r=subprocess.run([sys.executable,str(p/f'verify_turn{t}.py')],cwd=p,capture_output=True,check=True)
 expected=(p/f'TURN_{t}_CHECKS.json').read_bytes();assert r.stdout==expected,t
 counts.append(json.loads(r.stdout)['assertions'])
source_count=0
if args.source_dir:
 for n in ['SOURCE_MANIFEST.json','TURN_2_SOURCES.json','TURN_4_SOURCES.json']:
  for e in json.loads((p/n).read_text())['files']:
   verify(e,args.source_dir/Path(e['path']).name);source_count+=1
print(json.dumps({'author_assertions':sum(counts),'turn_assertions':counts,'historical_bindings':bound,'local_source_bindings':source_count,'source_files_published':False},sort_keys=True,indent=2))
