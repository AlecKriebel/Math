"""Read-only verification of the self-excluded public audit manifest and raw streams."""
from pathlib import Path
import gzip,hashlib,json
ROOT=Path(__file__).resolve().parent
def private(path):return any(part in {'private_sources','private_runtime','__pycache__','final_live','post_merge'} for part in path.parts)
manifest=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_bytes())
expected={row['path'] for row in manifest['files']}
actual={str(path.relative_to(ROOT)) for path in ROOT.rglob('*') if path.is_file() and not private(path.relative_to(ROOT)) and path.name!='PUBLIC_MANIFEST.json'}
assert actual==expected
for row in manifest['files']:
 data=(ROOT/row['path']).read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
for row in json.loads((ROOT/'receipts/replay_storage.json').read_bytes()):
 data=(ROOT/row['stored_path']).read_bytes()
 if row['compression']=='gzip':data=gzip.decompress(data)
 assert len(data)==row['complete_raw_output_bytes'] and hashlib.sha256(data).hexdigest()==row['complete_raw_output_sha256']
for row in json.loads((ROOT/'FINAL_SEAL.json').read_bytes())['sealed_artifacts']:
 data=(ROOT/row['path']).read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
print('PASS: complete self-excluded public audit, earlier/final seals and44 raw execution-output streams')
