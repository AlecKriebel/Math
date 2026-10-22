"""Verify byte-exact portable evidence; does not replace mathematical replay."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
checks=0
for manifest_name in ('FROZEN_MANIFEST.json','independent_review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json'):
    path=root/manifest_name
    data=json.loads(path.read_text())
    for entry in data['files']:
        b=(path.parent/entry['path']).read_bytes()
        assert len(b)==entry['bytes'],entry['path']
        assert hashlib.sha256(b).hexdigest()==entry['sha256'],entry['path']
        checks+=1
assert hashlib.sha256((root/'FROZEN_MANIFEST.json').read_bytes()).hexdigest()=='4941008f76b72a5dae9d853531b9c4c12267a19ced6ab7dbb3b205c19e671aea'
assert hashlib.sha256((root/'independent_review/REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='5ea069458ba3abaaae67458e92b006e87431d775b45339fb75f0b596566b1f46'
print(json.dumps({'status':'PASS_PORTABLE_MANIFESTS','file_digest_checks':checks,'original_status':'unsolved','turns':5},sort_keys=True))
