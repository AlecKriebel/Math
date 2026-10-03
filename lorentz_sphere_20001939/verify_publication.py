"""Verify preserved author bytes and reproduce the exact algebra checks."""
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUTHOR_MANIFEST.json').read_text())
for entry in manifest['files']:
    data=(root/entry['path']).read_bytes()
    if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
        raise SystemExit('Author-file mismatch: '+entry['path'])
result=subprocess.run([sys.executable,str(root/'verify_identities.py')],capture_output=True,check=True)
if result.stdout!=(root/'verification.json').read_bytes():
    raise SystemExit('Exact checker output differs from verification.json')
print('PASS: 10 author files match; all 4 identity checks reproduced byte-for-byte.')
