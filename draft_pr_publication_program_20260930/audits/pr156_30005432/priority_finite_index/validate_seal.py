from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
seal=json.loads((root/'SEAL.json').read_text())
manifest=root/'INPUT_OUTPUT_BYTEHASH_MANIFEST.json'
if hashlib.sha256(manifest.read_bytes()).hexdigest()!=seal['manifest_sha256']:raise RuntimeError('Manifest seal mismatch')
x=json.loads(manifest.read_text());n=0
for group in ['inputs','outputs']:
 for row in x[group]:
  f=Path(row['path']) if group=='inputs' else root/row['path']
  b=f.read_bytes()
  if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:raise RuntimeError('Mismatch '+str(f))
  n+=1
for key,file in [('review_sha256','REVIEW.md'),('result_sha256','RESULT.json'),('derivation_sha256','DERIVED_PRIOR_IMPLICATION.md')]:
 if hashlib.sha256((root/file).read_bytes()).hexdigest()!=seal[key]:raise RuntimeError('Core seal mismatch '+file)
print(json.dumps({'status':'PASS','authenticated_records':n,'seal_UTC':seal['UTC']},indent=2))
