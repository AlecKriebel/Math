#!/usr/bin/env python3
"""Explicit self-excluding seal creation; run only before final family closure."""
from pathlib import Path
import datetime,hashlib,json
from verify_first_party import rows
root=Path(__file__).resolve().parent
files=rows(root)
manifest={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'schema':'strict_recursive_self_excluding_first_party_v1','self_excluded':['FIRST_PARTY_MANIFEST.json'],'foreign_excluded_prefixes':['primary/'],'bytecode_excluded_component':'__pycache__','files_count':len(files),'files':files,'scope':'Every retained first-party authored/revision/stream/receipt file recursively bound. Imported PDFs/text excluded as foreign. V1 inner receipt/streams explicitly not retained and not reconstructed.'}
p=root/'FIRST_PARTY_MANIFEST.json';p.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'members':len(files),'manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
