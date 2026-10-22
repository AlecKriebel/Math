#!/usr/bin/env python3
"""Portable offline integrity, replay, and fail-closed mutation checks."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def run(script, *arguments):
    return subprocess.run([sys.executable, str(script), *map(str, arguments)],
                          cwd=tempfile.gettempdir(), capture_output=True,
                          text=True, timeout=120)


def main():
    root = Path(__file__).resolve().parent
    publication = json.loads((root / 'PUBLICATION.json').read_text())
    rows = publication['files']
    names = [r['path'] for r in rows]
    require(len(names) == len(set(names)), 'Duplicate manifest paths')
    require(set(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file())
            == set(names) | {'PUBLICATION.json'}, 'Publication file set differs')
    for row in rows:
        path = root / row['path']
        require(root in path.resolve().parents, 'Unsafe manifest path')
        data = path.read_bytes()
        require(len(data) == row['bytes'], 'Size mismatch: ' + row['path'])
        require(hashlib.sha256(data).hexdigest() == row['sha256'],
                'Hash mismatch: ' + row['path'])
    for archive_name, folder, manifest in (
        ('AUTHOR_PACKET.zip', 'packet', root / 'FREEZE_MANIFEST.json'),
        ('audit/AUDIT_PACKET.zip', 'audit', root / 'audit/AUDIT_FREEZE.json')):
        frozen = json.loads(manifest.read_text())
        expected = {r['path'] for r in frozen['files']} if folder == 'packet' else set(frozen['included_files'])
        with zipfile.ZipFile(root / archive_name) as archive:
            require(len(archive.namelist()) == len(expected), 'Unexpected archive entries')
            require(set(archive.namelist()) == expected, 'Archive file set changed')
            for name in expected:
                require(archive.read(name) == (root / folder / name).read_bytes(),
                        'Archive and expanded bytes differ: ' + name)
    author = run(root / 'packet/verify.py')
    require(author.returncode == 0, 'Author replay failed: ' + author.stderr)
    author_result = json.loads(author.stdout)
    require(author_result == json.loads((root / 'packet/controls.json').read_text()),
            'Author replay differs from frozen controls')
    require(author_result == json.loads((root / 'packet/result.json').read_text())['controls'],
            'Author replay differs from frozen result')
    audit_script = root / 'audit/replay_audit.py'
    audit = run(audit_script, root / 'AUTHOR_PACKET.zip')
    require(audit.returncode == 0, 'Audit replay failed: ' + audit.stderr)
    require(audit.stdout.encode() == (root / 'audit/replay_results.json').read_bytes(),
            'Audit replay differs from frozen output')
    controls = []
    original = (root / 'AUTHOR_PACKET.zip').read_bytes()
    with tempfile.TemporaryDirectory(prefix='time-one-negative-controls-') as temp:
        mutated = bytearray(original)
        mutated[len(mutated) // 2] ^= 1
        for name, payload, message in (
            ('one-bit.zip', mutated, 'Archive hash changed'),
            ('truncated.zip', original[:-1], 'Archive byte count changed')):
            target = Path(temp) / name
            target.write_bytes(payload)
            result = run(audit_script, target)
            require(result.returncode != 0 and message in result.stderr,
                    'Mutation was not rejected for the expected reason: ' + name)
            controls.append({'case': name, 'correctly_rejected': True})
    print(json.dumps({'all_passed': True, 'manifest_files_checked': len(rows),
                      'author_assertions': author_result['assertions'],
                      'audit_assertions': json.loads(audit.stdout)['independent_controls']['assertions'],
                      'audit_replay_byte_identical': True,
                      'negative_controls': controls}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
