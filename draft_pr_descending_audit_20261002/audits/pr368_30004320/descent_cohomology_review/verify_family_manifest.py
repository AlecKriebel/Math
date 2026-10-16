from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
m=json.loads((P/'PUBLIC_MANIFEST.json').read_bytes())
expected={r['path'] for r in m['files']}
actual={str(f.relative_to(P)) for f in P.iterdir() if f.is_file() and f.name!='PUBLIC_MANIFEST.json'}
assert expected==actual,(expected^actual)
for row in m['files']:
 b=(P/row['path']).read_bytes();assert len(b)==row['bytes'];assert hashlib.sha256(b).hexdigest()==row['sha256']
for name in ['SOURCE_FIRST_SEAL.json','MATHEMATICAL_SEAL.json']:
 for row in json.loads((P/name).read_bytes())['files']:
  b=(P/row['path']).read_bytes();assert len(b)==row['bytes'];assert hashlib.sha256(b).hexdigest()==row['sha256']
print(json.dumps({'status':'PASS','family_public_files':len(expected),'immutable_source_and_math_seals':True},sort_keys=True))
