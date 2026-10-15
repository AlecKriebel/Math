#!/usr/bin/env python3
"""Portable exact-byte verifier and deterministic replay for this author packet."""
import argparse,hashlib,json,pathlib,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--author-dir',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent);p.add_argument('--source-dir',type=pathlib.Path);p.add_argument('--allow-unfrozen',action='store_true');a=p.parse_args();root=a.author_dir
bound=0
def verify(entries,folder,key='path'):
 global bound
 for e in entries:
  b=(folder/e[key]).read_bytes();assert len(b)==e['bytes'],e[key];assert hashlib.sha256(b).hexdigest()==e['sha256'],e[key];bound+=1
history=0
for i in range(1,6):
 m=json.loads((root/f'TURN_{i}_MANIFEST.json').read_bytes());verify(m['files'],root);history+=len(m['files'])
 if i>1:assert m['previous_manifest_sha256']==hashlib.sha256((root/f'TURN_{i-1}_MANIFEST.json').read_bytes()).hexdigest()
final=root/'FINAL_AUTHOR_MANIFEST.json'
if final.exists():verify(json.loads(final.read_bytes())['files'],root)
elif not a.allow_unfrozen:raise AssertionError('Final author manifest missing')
outputs=[];total=0
for i in range(1,6):
 out=subprocess.check_output([sys.executable,str(root/f'check_turn_{i}.py')],cwd=root)
 assert out==(root/f'TURN_{i}_CHECKS.json').read_bytes(),f'turn {i} replay bytes'
 d=json.loads(out);n=d.get('exact_assertions',d.get('assertions'));total+=n;outputs.append({'turn':i,'assertions':n,'byte_exact':True})
sources=0
if a.source_dir:
 s=json.loads((root/'SOURCE_MANIFEST.json').read_bytes());verify(s['files'],a.source_dir,'name');sources+=len(s['files'])
 e=json.loads((root/'SOURCE_ADDITION_T4.json').read_bytes())['source'];verify([e],a.source_dir,'local_filename');sources+=1
print(json.dumps({'status':'PASS','historical_file_bindings':history,'all_verified_file_bindings':bound,'source_files_checked':sources,'author_assertions':total,'replays':outputs},indent=2))
