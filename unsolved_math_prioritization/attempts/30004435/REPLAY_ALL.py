"""Portable standard-library replay and frozen-byte integrity checks."""
import argparse,hashlib,json,pathlib,subprocess,sys
p=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--sources',type=pathlib.Path);args=ap.parse_args()
entries=0
for manifest in [*sorted(p.glob('TURN_*_MANIFEST.json')), *sorted(p.glob('FINAL_FROZEN_MANIFEST.json'))]:
 for item in json.loads(manifest.read_text())['files']:
  b=(p/item['path']).read_bytes();assert len(b)==item['bytes'];assert hashlib.sha256(b).hexdigest()==item['sha256'],(manifest.name,item['path']);entries+=1
counts=[]
for turn in range(1,6):
 output=subprocess.check_output([sys.executable,str(p/f'verify_turn{turn}.py')],cwd=p)
 expected=(p/f'TURN_{turn}_CHECKS.json').read_bytes();assert output==expected,f'turn {turn} replay mismatch';counts.append(json.loads(output)['assertions'])
source_count=0
if args.sources:
 items=json.loads((p/'SOURCE_MANIFEST.json').read_text())['primary_pdfs'];extra=json.loads((p/'TURN_3_SOURCE.json').read_text());items.append(dict(file=extra['local_source'],bytes=extra['bytes'],sha256=extra['sha256']))
 for item in items:
  b=(args.sources/item['file']).read_bytes();assert len(b)==item['bytes'];assert hashlib.sha256(b).hexdigest()==item['sha256'];source_count+=1
print(json.dumps(dict(author_assertions=sum(counts),per_turn=counts,manifest_entries_verified=entries,source_pdfs_verified=source_count,scope='Five-turn partial packet; unrestricted probability-only tail equality remains unresolved.'),indent=2,sort_keys=True))
