"""Create or read-only verify the exact self-excluding first-party closure manifest."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

TASK_DIR = Path(__file__).resolve().parent
EXCLUDED_DIRS = {'sources', 'tmp', '__pycache__'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def members():
    return sorted(p for p in TASK_DIR.rglob('*') if p.is_file()
                  and p.name != 'MANIFEST.json'
                  and not any(part in EXCLUDED_DIRS for part in p.relative_to(TASK_DIR).parts))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    manifest = TASK_DIR / 'MANIFEST.json'
    if args.verify:
        doc = json.loads(manifest.read_text())
        actual = {p.relative_to(TASK_DIR).as_posix(): p for p in members()}
        recorded = {row['path']: row for row in doc['files']}
        errors = []
        if actual.keys() != recorded.keys():
            errors.append({'membership_mismatch': sorted(actual.keys() ^ recorded.keys())})
        for name in actual.keys() & recorded.keys():
            path, row = actual[name], recorded[name]
            if path.stat().st_size != row['size'] or sha(path) != row['sha256']:
                errors.append({'content_mismatch': name})
        print(json.dumps({'manifest_sha256': sha(manifest), 'members': len(recorded), 'self_excluding': True,
                          'errors': errors, 'pass': not errors}, indent=2))
        raise SystemExit(bool(errors))
    if manifest.exists():
        raise SystemExit('Closed manifest already exists; use --verify. Do not reseal this family.')
    doc = {'created_utc': datetime.now(timezone.utc).isoformat(), 'status': 'CLOSED',
           'family': 'pr32_6800007 priority_flag_family', 'self_excluding': True,
           'excluded': ['MANIFEST.json', 'sources/ foreign reference bytes and derivatives', 'tmp/', '__pycache__/'],
           'early_seal_sha256': sha(TASK_DIR / 'EARLY_PRIORITY_SEAL.md'),
           'meaning': 'First-party audit/program/receipt/output integrity; not universal mathematics, exhaustive priority or novelty proof.',
           'files': [{'path': p.relative_to(TASK_DIR).as_posix(), 'size': p.stat().st_size, 'sha256': sha(p)} for p in members()]}
    manifest.write_text(json.dumps(doc, indent=2) + '\n')
    print(json.dumps({'manifest_sha256': sha(manifest), 'members': len(doc['files']), 'status': 'CLOSED'}, indent=2))
