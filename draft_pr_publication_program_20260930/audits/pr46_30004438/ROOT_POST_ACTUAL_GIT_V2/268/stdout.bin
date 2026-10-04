#!/usr/bin/env python3
"""Bind exactly the 13 original scientific files, without copying foreign bodies."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
parent=root.parent
manifest=parent/'ORIGINAL_PREPARATION_MANIFEST.json'
raw=manifest.read_bytes()
sha=hashlib.sha256(raw).hexdigest()
assert sha=='da37655e9b3bab420862a0c17c761e67fa9a4bc2028a328d033547249c54ad2e',sha
data=json.loads(raw)
assert data['head']=='a39d178b10f75fb127058b08e0d0002b3ae97f8a'
assert data['files_count']==318
rows=[r for r in data['files'] if r['path'].startswith('source_snapshot/')]
assert len(rows)==13
bindings=[]
for row in rows:
    p=parent/row['path']
    b=p.read_bytes()
    digest=hashlib.sha256(b).hexdigest()
    mode=p.stat().st_mode & 0o7777
    assert digest==row['sha256']
    assert len(b)==row['bytes']
    assert mode==row['full_mode']==0o444
    # Full UTF-8 decoding and JSON parsing are receipt checks, not claims of
    # line-by-line human inspection of every repeated PASS string.
    text=b.decode('utf-8')
    if p.suffix=='.json':json.loads(text)
    bindings.append({'path':str(p),'bytes':len(b),'sha256':digest,'full_mode_octal':oct(mode),'complete_byte_read':True})
out={'schema':'pr46-complex-dynamics-input-bindings/v1','head':data['head'],
 'original_preparation_manifest_sha256':sha,'original_preparation_manifest_bytes':len(raw),
 'original_preparation_files_count':data['files_count'],'original_scientific_files_read':13,
 'original_claim_target':'For each d>=2, Rat_d(R) contains a nonempty Euclidean-open subset with every projective periodic point real.',
 'bindings':bindings,'foreign_raw_pdf_ocr_pixel_cache_bodies_copied':False}
(root/'ORIGINAL_INPUT_BINDINGS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
