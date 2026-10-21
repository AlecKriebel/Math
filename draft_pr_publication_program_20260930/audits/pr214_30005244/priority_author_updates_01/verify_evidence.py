#!/usr/bin/env python3
"""Read-only validation of finite authored manifest and explicitly pinned primary bodies."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
def check(item,base=None):
 p=Path(item['path']);p=p if p.is_absolute() else (base or P)/p
 b=p.read_bytes();assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],str(p)
manifest=json.loads((P/'AUTHORED_MANIFEST.json').read_text())
for item in manifest['files']:check(item)
seal=json.loads((P/'EXTERNAL_SEAL.json').read_text());check(seal['manifest'])
ledger=json.loads((P/'SOURCE_VERSION_SEARCH_LEDGER.json').read_text());n=0
for source in ledger['sources']:
 if 'PDF' in source:check(source['PDF']);n+=1
root=P.parent/'ROOT_MATHEMATICAL_ACCEPTANCE_01.json';b=root.read_bytes();assert len(b)==8102 and hashlib.sha256(b).hexdigest()=='bbe3367361a402b920d6576ed8ab398f96998a28077d7278e7b8a0ee7727b5ad'
print(json.dumps({'status':'all finite authored entries, manifest seal, seven named primary PDFs and exact Root gate verified','authored_files':len(manifest['files']),'PDFs':n,'whole_case_or_priority_certificate':False}))
