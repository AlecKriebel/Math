#!/usr/bin/env python3
"""Build metadata-only final inventory after receipt capture completes."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRIVATE = Path('/Users/alec/.cache/pr66_exact_target_priority_20261004')

def record(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}

public = [record(p) for p in sorted(ROOT.rglob('*')) if p.is_file()
          and p.name != 'MANIFEST.json']
private = [record(p) for p in sorted(PRIVATE.rglob('*')) if p.is_file()]
manifest = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'generator_pid': os.getpid(),
    'verdict': 'prior_full_solution',
    'verdict_scope': 'Original universal Ohtsuki Conjecture2.11, after exact vt3=4v3 normalization and integrality; separate even refinement and mechanism novelty not adjudicated',
    'public_root': str(ROOT),
    'private_cache': str(PRIVATE),
    'copyright_custody': 'Publication bodies, extracted text, pixels, raw web/API results and raw streams are private; only metadata/code/reports/receipts in repository',
    'input_custody_record': str(ROOT / 'INPUT_CUSTODY.json'),
    'first_conclusion_seal': str(ROOT / 'FIRST_CONCLUSION_SEAL.json'),
    'receipt_count': len(list((ROOT / 'receipts').glob('*.json'))),
    'public_files': public,
    'private_files_metadata_only': private,
    'inventory_excludes': ['MANIFEST.json itself to avoid self-reference'],
    'historical_limit': 'No immutable pre2026 author-PDF byte-history or identical2000printed-body access asserted'
}
target = ROOT / 'MANIFEST.json'
target.write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'manifest': record(target), 'generator_pid': os.getpid(),
                  'public_file_count': len(public), 'private_file_count': len(private),
                  'receipt_count': manifest['receipt_count']}, indent=2))
