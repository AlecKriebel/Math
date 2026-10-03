#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--author-dir',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent);ap.add_argument('--source-dir',type=pathlib.Path);ap.add_argument('--allow-unfrozen',action='store_true');a=ap.parse_args();p=a.author_dir
bindings=history=0
def check(es,folder,key='path'):
 global bindings
 for e in es:
  b=(folder/e[key]).read_bytes();assert len(b)==e['bytes'];assert hashlib.sha256(b).hexdigest()==e['sha256'],e[key];bindings+=1
for i in range(1,6):
 m=json.loads((p/f'TURN_{i}_MANIFEST.json').read_bytes());check(m['files'],p);history+=len(m['files'])
 if i>1:assert m['previous_manifest_sha256']==hashlib.sha256((p/f'TURN_{i-1}_MANIFEST.json').read_bytes()).hexdigest()
if (p/'FINAL_AUTHOR_MANIFEST.json').exists():check(json.loads((p/'FINAL_AUTHOR_MANIFEST.json').read_bytes())['files'],p)
elif not a.allow_unfrozen:raise AssertionError('Missing final manifest')
rows=[];total=0
for i in range(1,6):
 b=subprocess.check_output([sys.executable,str(p/f'check_turn_{i}.py')],cwd=p);assert b==(p/f'TURN_{i}_CHECKS.json').read_bytes();v=json.loads(b)['exact_assertions'];total+=v;rows.append({'turn':i,'assertions':v,'byte_exact':True})
source_count=0
if a.source_dir:
 es=json.loads((p/'SOURCE_MANIFEST.json').read_bytes())['files'];check(es,a.source_dir,'name');source_count=len(es)
print(json.dumps({'status':'PASS','historical_file_bindings':history,'all_file_bindings':bindings,'source_pdfs_checked':source_count,'exact_author_assertions':total,'replays':rows},indent=2))
