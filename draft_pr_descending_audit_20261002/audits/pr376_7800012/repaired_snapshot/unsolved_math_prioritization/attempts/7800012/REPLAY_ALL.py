"""Portable standard-library replay for the frozen five-turn flux packet."""
import argparse,hashlib,json,pathlib,subprocess,sys
p=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--sources',type=pathlib.Path);args=ap.parse_args()
entries=0
for manifest in [*sorted(p.glob('TURN_*_MANIFEST.json')),*sorted(p.glob('FINAL_FROZEN_MANIFEST.json'))]:
 for item in json.loads(manifest.read_text())['files']:
  b=(p/item['path']).read_bytes();assert len(b)==item['bytes'];assert hashlib.sha256(b).hexdigest()==item['sha256'],(manifest.name,item['path']);entries+=1
counts=[]
for turn in range(1,6):
 output=subprocess.check_output([sys.executable,str(p/f'verify_turn{turn}.py')],cwd=p)
 assert output==(p/f'TURN_{turn}_CHECKS.json').read_bytes(),f'turn {turn} mismatch';counts.append(json.loads(output)['assertions'])
source_count=0
if args.sources:
 for item in json.loads((p/'SOURCE_MANIFEST.json').read_text())['primary_sources']:
  b=(args.sources/item['file']).read_bytes();assert len(b)==item['bytes'];assert hashlib.sha256(b).hexdigest()==item['sha256'];source_count+=1
print(json.dumps(dict(author_assertions=sum(counts),per_turn=counts,manifest_entries_verified=entries,primary_source_files_verified=source_count,scope='Five-turn scoped partials; unrestricted quarter-filled optimal flux remains unresolved.'),indent=2,sort_keys=True))
