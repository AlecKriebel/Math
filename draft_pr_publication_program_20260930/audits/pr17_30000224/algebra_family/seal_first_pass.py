#!/usr/bin/env python3
"""Seal the independent pass before any conclusions from other families."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
HERE=Path(__file__).resolve().parent
paths=['FIRST_PASS.md','exact_probes.py','evidence/exact_probe_results.json',
       'reproduce_author.py','evidence/author_reproduction.json',
       'fetch_sources.py','evidence/primary_source_receipts.json']
manifest={p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in paths}
source=HERE.parent/'source_snapshot'
sourcehash=hashlib.sha256((source/'PARTIAL_RESULTS.md').read_bytes()).hexdigest()
assert sourcehash=='8d6995c10f48640f33afc5a437766eaccead99808e7b3c7f770bb52a8e900444'
out={'sealed_at_utc':datetime.now(timezone.utc).isoformat(),
     'frozen_head':'dae2b77074945443e1b91c92f641ff9feff12235',
     'target':'30000224 / OWR-824-008','PARTIAL_RESULTS_sha256':sourcehash,
     'unread_before_seal':['historical REVIEW','historical review_summary','sibling conclusions','root conclusions'],
     'hashes':manifest,'verdict':'algebra partial results pass; geometry-specific conclusions conditional'}
seal=HERE/'evidence'/'first_pass_seal.json'
if seal.exists():
    raise RuntimeError('First-pass seal already exists; never overwrite it')
seal.write_text(json.dumps(out,indent=2)+'\n')
print(out['sealed_at_utc'])
