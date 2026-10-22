"""Read-only custody verification; this is not a mathematical test."""
from pathlib import Path
import hashlib
import json

base = Path(__file__).resolve().parent
receipt = json.loads((base / 'RECEIPT.json').read_text())
allowed_external = {'../../inputs/COUNTEREXAMPLE.md', '../../REVIEWED_PROOF.md'}
count = 0
for group in ('artifacts', 'inputs', 'private_sources_and_history'):
    for item in receipt[group]:
        rel = item['path']
        if Path(rel).is_absolute() or ('..' in Path(rel).parts and rel not in allowed_external):
            raise SystemExit('Unexpected custody path')
        path = base / rel
        if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != Path('/')):
            raise SystemExit('Symlink rejected: ' + rel)
        data = path.read_bytes()
        if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise SystemExit('Custody mismatch: ' + rel)
        count += 1
print(json.dumps({'status': 'PASS', 'pinned_files_checked': count,
                  'purpose': 'read-only custody, not mathematical verification'}, sort_keys=True))
