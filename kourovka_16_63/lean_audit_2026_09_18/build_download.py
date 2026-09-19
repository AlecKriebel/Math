#!/usr/bin/env python3
"""Package the Lean sources and scoped local audit; never include build caches."""
from pathlib import Path
import hashlib
import json
import zipfile

AUDIT = Path(__file__).resolve().parent
PROBLEM = AUDIT.parent
REPO = PROBLEM.parent
DEST = REPO / 'docs/papers/kourovka-16-63/lean-source-and-audit.zip'
PREFIX = 'kourovka_16_63_lean_review_2026-09-18/'
EXCLUDED = {'.lake', '.tools', '.runtime', '__pycache__', '.git', 'post_deployment'}

def files():
    for folder, prefix in [(PROBLEM / 'lean', 'lean'), (AUDIT, 'audit')]:
        for p in sorted(folder.rglob('*')):
            if not p.is_file() or p.is_symlink():
                continue
            rel = p.relative_to(folder)
            if any(part in EXCLUDED for part in rel.parts):
                continue
            if p.suffix in {'.olean', '.ilean', '.pyc'}:
                continue
            yield prefix + '/' + rel.as_posix(), p.read_bytes()

def main():
    evidence = json.loads((AUDIT / 'latest_accepted_object_audit.json').read_text())
    assert evidence['status'] == 'ACCEPTED_OBJECT_QUERIES_PASSED_NOT_FULL_FORMALIZATION'
    assert 'pending final assembly' not in (AUDIT / 'VERIFICATION_REPORT.md').read_text()
    progress = json.loads((PROBLEM / 'lean/progress.json').read_text())
    assert progress['successful_lean_compilation'] and not progress['complete_formalization']
    for record in evidence['snapshot_after']['modules'].values():
        source = PROBLEM / 'lean' / record['source']
        assert hashlib.sha256(source.read_bytes()).hexdigest() == record['source_sha256']
    for line in (PROBLEM / 'lean/SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert hashlib.sha256((PROBLEM / 'lean' / name).read_bytes()).hexdigest() == digest
    entries = list(files())
    entries.append(('README.md', (
        '# Kourovka 16.63 — partial Lean source and local audit\n\n'
        'Start with `lean/README.md` and `audit/VERIFICATION_REPORT.md`.\n'
        'The complete finite-group theorem is not formalized in this package.\n'
        'The audit distinguishes accepted source from missing proof obligations.\n\n'
        'The source project is in `lean/`; enter that directory before running '
        'the documented build commands. No compiler or dependency caches are included.\n'
    ).encode()))
    manifest = ''.join(hashlib.sha256(data).hexdigest() + '  ' + name + '\n'
                       for name, data in entries)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DEST, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in entries + [('SHA256SUMS', manifest.encode())]:
            info = zipfile.ZipInfo(PREFIX + name, date_time=(2026, 9, 18, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    with zipfile.ZipFile(DEST) as z:
        assert z.testzip() is None
        for line in z.read(PREFIX + 'SHA256SUMS').decode().splitlines():
            digest, name = line.split('  ', 1)
            assert hashlib.sha256(z.read(PREFIX + name)).hexdigest() == digest
    print(f'{DEST}\n{hashlib.sha256(DEST.read_bytes()).hexdigest()}  {DEST.name}')

if __name__ == '__main__':
    main()
