"""Inventory retained reference bytes and receipt bindings without changing sources.

This checks identity and format, not novelty or theorem correctness. Network replay
is a separate explicit program. All foreign content stays in ignored sources/.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

TASK_DIR = Path(__file__).resolve().parent

def utc():
    return datetime.now(timezone.utc).isoformat()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def receipts():
    rows = []
    for path in sorted(TASK_DIR.glob('*RECEIPTS.json')):
        value = json.loads(path.read_text())
        entries = value if isinstance(value, list) else value.get('receipts', [])
        for entry in entries:
            rows.append({'receipt_file': path.name, **entry})
    return rows

if __name__ == '__main__':
    rows = receipts()
    catalog = []
    pdfs = []
    for path in sorted((TASK_DIR / 'sources').rglob('*')):
        if not path.is_file():
            continue
        data = path.read_bytes()
        matches = [row for row in rows if row.get('name') in (path.name, path.stem)]
        entry = {'path': path.relative_to(TASK_DIR).as_posix(), 'bytes': len(data),
                 'sha256': digest(path), 'is_pdf': data.startswith(b'%PDF-'),
                 'receipt_files': sorted(set(row['receipt_file'] for row in matches))}
        if entry['is_pdf']:
            info = subprocess.run(['/opt/homebrew/bin/pdfinfo', str(path)],
                                  capture_output=True, text=True)
            page_lines = [line for line in info.stdout.splitlines() if line.startswith('Pages:')]
            entry['pages'] = int(page_lines[0].split(':')[1]) if page_lines else None
            entry['pdfinfo_exit'] = info.returncode
            pdfs.append(entry)
        catalog.append(entry)
    bindings = []
    for row in rows:
        name = row.get('name')
        if not name:
            continue
        path = TASK_DIR / 'sources' / name
        if not path.is_file() and path.suffix == '':
            alternatives = [p for p in (TASK_DIR / 'sources').iterdir() if p.is_file() and p.stem == name]
            if len(alternatives) == 1:
                path = alternatives[0]
        if path.is_file():
            bindings.append({'receipt_file': row['receipt_file'], 'name': name,
                             'actual_bytes': path.stat().st_size,
                             'actual_sha256': digest(path),
                             'receipt_hash_present': 'sha256' in row,
                             'hash_matches_when_present': digest(path) == row['sha256'] if 'sha256' in row else None,
                             'requested_url': row.get('requested_url', row.get('url'))})
    (TASK_DIR / 'SOURCE_BYTE_CATALOG.json').write_text(json.dumps({
        'generated_utc': utc(), 'scope': 'Retained ignored reference bytes, including errors and derived extraction/conversion files.',
        'files': catalog, 'receipt_bindings': bindings,
        'limitations': ['A missing receipt hash is supplemented by this catalog, not retroactively claimed as contemporaneously recorded.',
                        'PDF magic and matching SHA establish format/identity only, not publication-version identity or mathematical validity.']}, indent=2) + '\n')
    (TASK_DIR / 'PDF_INVENTORY.json').write_text(json.dumps({'generated_utc': utc(), 'files': pdfs}, indent=2) + '\n')
    print(json.dumps({'source_files': len(catalog), 'pdf_files': len(pdfs),
                      'hash_mismatches': [x for x in bindings if x['hash_matches_when_present'] is False]}, indent=2))
