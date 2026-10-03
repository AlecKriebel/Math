from pathlib import Path
import argparse,hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--sources');a=ap.parse_args()
checks=0;bindings=0
for t in range(1,6):
 got=subprocess.check_output([sys.executable,str(p/f'check_turn_{t}.py')],cwd=p)
 assert got==(p/f'TURN_{t}_CHECKS.json').read_bytes(),t
 checks+=json.loads(got)['assertions']
 m=json.loads((p/f'TURN_{t}_MANIFEST.json').read_text())
 if t>1:assert m['previous_manifest_sha256']==hashlib.sha256((p/f'TURN_{t-1}_MANIFEST.json').read_bytes()).hexdigest()
 for f in m['files']:
  b=(p/f['path']).read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'];bindings+=1
final=p/'FINAL_AUTHOR_MANIFEST.json'
if final.exists():
 for f in json.loads(final.read_text())['files']:
  b=(p/f['path']).read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'];bindings+=1
sources=0
if a.sources:
 for f in json.loads((p/'SOURCE_MANIFEST.json').read_text())['files']:
  b=(Path(a.sources)/Path(f['path']).name).read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'];sources+=1
print(json.dumps({'author_assertions':checks,'verified_bindings':bindings,'optional_source_files':sources,'all_five_receipts_exact':True},indent=2,sort_keys=True))
