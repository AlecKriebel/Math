#!/usr/bin/env python3
"""Validate this audit's public bindings and two immutable independence seals."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'PUBLIC_MANIFEST.json').read_text())
for entry in manifest['files']:
 rel=Path(entry['path'])
 assert not rel.is_absolute() and '..' not in rel.parts
 assert rel.name!='PUBLIC_MANIFEST.json' and rel.parts[0]!='private'
 body=(root/rel).read_bytes()
 assert len(body)==entry['bytes'],rel
 assert hashlib.sha256(body).hexdigest()==entry['sha256'],rel
for seal_name in ['SOURCE_BASELINE_SEAL.json','MATH_VERDICT_SEAL.json']:
 seal=json.loads((root/seal_name).read_text())
 assert hashlib.sha256((root/seal['file']).read_bytes()).hexdigest()==seal['sha256'],seal_name
print(json.dumps({'status':'PASS','public_bound_files':len(manifest['files']),'source_first_seal_unchanged':True,'pre_program_math_seal_unchanged':True,'mandatory_fixes':manifest['mandatory_fixes'],'raw_sources_excluded':True},indent=2))
