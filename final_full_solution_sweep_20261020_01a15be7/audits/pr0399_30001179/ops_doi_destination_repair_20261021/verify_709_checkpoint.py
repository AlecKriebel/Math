#!/usr/bin/env python3
"""Reconstruct the pre-label-correction709 checkpoint using its exact report copy."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent;A=H.parent;C=H/'checkpoint_709';data=(C/'MANIFEST.json').read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
expected='5814e8fe7c80b35a7b87fc563ddc03879d503fd915cc3673f2fb5d78a3f74a5b'
if sha(data)!=expected or (C/'MANIFEST.sha256').read_text()!=expected+'  MANIFEST.json\n':raise RuntimeError('709 seal changed')
value=json.loads(data)
for e in value['files']+value['immutable_inputs']:
 p=C/'REPORT.md' if e['path']=='ops_doi_destination_repair_20261021/REPORT.md' else A/e['path'];body=p.read_bytes()
 if len(body)!=e['bytes'] or sha(body)!=e['sha256']:raise RuntimeError('709 reconstruction changed '+e['path'])
print(json.dumps({'verified':True,'artifacts':len(value['files']),'immutable_inputs':len(value['immutable_inputs']),'manifest_sha256':expected,'only_override':'Exact preserved report before UTF8 byte-count label correction','production_helpers_and_controls_unchanged':True}))
