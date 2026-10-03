"""Portable exact controls and immutable bindings; Python standard library only."""
import argparse,hashlib,json,pathlib,subprocess,sys
p=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--sources',type=pathlib.Path);a=ap.parse_args();entries=0
for m in [*sorted(p.glob('TURN_*_MANIFEST.json')),*sorted(p.glob('FINAL_FROZEN_MANIFEST.json'))]:
 for e in json.loads(m.read_text()).get('files',[]):
  b=(p/e['path']).read_bytes();assert len(b)==e['bytes'];assert hashlib.sha256(b).hexdigest()==e['sha256'],(m.name,e['path']);entries+=1
counts=[]
for n in range(1,6):
 b=subprocess.check_output([sys.executable,str(p/f'verify_turn{n}.py')],cwd=p);assert b==(p/f'TURN_{n}_CHECKS.json').read_bytes(),n;counts.append(json.loads(b)['assertions'])
sources=0
if a.sources:
 for m in ['SOURCE_MANIFEST.json','TURN_5_SOURCE_MANIFEST.json']:
  for e in json.loads((p/m).read_text())['primary_sources']:
   b=(a.sources/e['file']).read_bytes();assert len(b)==e['bytes'];assert hashlib.sha256(b).hexdigest()==e['sha256'];sources+=1
print(json.dumps(dict(author_assertions=sum(counts),per_turn=counts,manifest_entries_verified=entries,primary_source_pdfs_verified=sources,scope='Five-turn scoped reductions; original abstract CB-versus-MB separation remains unresolved.'),indent=2,sort_keys=True))
