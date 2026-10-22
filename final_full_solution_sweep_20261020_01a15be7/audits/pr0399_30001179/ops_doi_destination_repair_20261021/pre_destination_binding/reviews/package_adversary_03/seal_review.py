#!/usr/bin/env python3
"""Seal only reviewer03 authored files; never alter canonical research/helpers."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parent
S = R.parents[3] / 'private/pr0399_package03'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entries(root, excludes=()):
    result = []
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise RuntimeError('Symlink in review custody: '+str(path))
        if path.is_file() and path.relative_to(root).as_posix() not in excludes:
            result.append({'path': path.relative_to(root).as_posix(),
                           'bytes': path.stat().st_size, 'sha256': sha(path)})
    return result


def main():
    now = datetime.now(timezone.utc).isoformat()
    custody = {'schema': 1, 'sealed_utc': now, 'root': str(S),
               'scope': 'Ignored reviewer-owned scratch, supplied copies, downloads, raw public GET bodies and renders; no third-party body is copied into the public review directory.',
               'files': entries(S)}
    (R/'PRIVATE_CUSTODY_MANIFEST.json').write_text(json.dumps(custody, indent=2)+'\n')
    excludes = {'AUTHORED_FILE_MANIFEST.json', 'AUTHORED_FILE_MANIFEST.sha256'}
    manifest = {'schema': 1, 'sealed_utc': now, 'pr': 399, 'problem_id': '30001179',
                'reviewer': 'package_adversary_03', 'verdict': 'REPAIR_REQUIRED',
                'completion_estimate_percent': 100, 'publication_ready': False,
                'self_exclusions': sorted(excludes), 'files': entries(R, excludes)}
    p = R/'AUTHORED_FILE_MANIFEST.json'
    p.write_text(json.dumps(manifest, indent=2)+'\n')
    checksum = sha(p)
    (R/'AUTHORED_FILE_MANIFEST.sha256').write_text(checksum+'  AUTHORED_FILE_MANIFEST.json\n')
    for entry in manifest['files']:
        path = R/entry['path']
        if path.stat().st_size != entry['bytes'] or sha(path) != entry['sha256']:
            raise RuntimeError('Review seal check failed')
    print(json.dumps({'authored_files': len(manifest['files']), 'manifest_sha256': checksum,
                      'report_bytes': (R/'REPORT.md').stat().st_size,
                      'report_sha256': sha(R/'REPORT.md'),
                      'private_files': len(custody['files']), 'all_verified': True}, indent=2))


if __name__ == '__main__':
    main()
