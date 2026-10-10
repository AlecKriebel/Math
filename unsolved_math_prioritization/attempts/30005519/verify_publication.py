#!/usr/bin/env python3
"""Verify the complete safe publication, with optional replay and queue checks."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile


def require(test, message):
    if not test:
        raise RuntimeError(message)


def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def safe_relative(name):
    p = PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and str(p) == name,
            'Unsafe relative path: ' + name)
    return p


def verify(root):
    manifest = json.loads((root / 'PUBLICATION_MANIFEST.json').read_text())
    entries = manifest['files']
    names = [x['path'] for x in entries]
    require(len(names) == len(set(names)), 'Duplicate manifest entry')
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'Symlink in payload')
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    require(actual == set(names) | {'PUBLICATION_MANIFEST.json'},
            'Publication file inventory mismatch')
    for item in entries:
        p = safe_relative(item['path'])
        b = (root / str(p)).read_bytes()
        require(identity(b) == {k: item[k] for k in ('bytes', 'sha256')},
                'Publication file hash mismatch: ' + item['path'])
    provenance = json.loads((root / 'PUBLICATION_PROVENANCE.json').read_text())
    archive_members = 0
    for item in provenance['archives']:
        p = root / str(safe_relative(item['path']))
        require(identity(p.read_bytes()) == {k: item[k] for k in ('bytes', 'sha256')},
                'Archive identity mismatch')
        with zipfile.ZipFile(p) as z:
            require(z.testzip() is None, 'Archive CRC failure')
            members = z.namelist()
            require(len(members) == len(set(members)) == item['member_count'],
                    'Archive count or duplicate member failure')
            target = root / str(safe_relative(item['extracted_directory']))
            expected = {item['archive_prefix'] + '/' + str(q.relative_to(target))
                        for q in target.rglob('*') if q.is_file()}
            require(set(members) == expected, 'Archive exact inventory mismatch')
            for name in members:
                rel = safe_relative(name)
                require(rel.parts[0] == item['archive_prefix'], 'Archive prefix mismatch')
                dest = target / Path(*rel.parts[1:])
                require(z.read(name) == dest.read_bytes(), 'Extracted byte mismatch')
            archive_members += len(members)
    for directory in ('author', 'audit'):
        for flags in ([], ['-O']):
            completed = subprocess.run([sys.executable, *flags, str(root / directory / 'verify_manifest.py')],
                                       check=True, capture_output=True)
            require(json.loads(completed.stdout)['status'] == 'PASS', 'Frozen manifest failure')
    return {'status': 'PASS', 'payload_files': len(actual),
            'manifested_files': len(entries), 'archive_members': archive_members,
            'frozen_manifest_normal_and_optimized': 'PASS'}


def verify_queue(root, base_path, updated_path):
    d = json.loads((root / 'QUEUE_DELTA.json').read_text())
    base, updated = base_path.read_bytes(), updated_path.read_bytes()
    require(identity(base) == d['base'], 'Base queue identity mismatch')
    require(identity(updated) == d['updated'], 'Updated queue identity mismatch')
    before, after = base.splitlines(keepends=True), updated.splitlines(keepends=True)
    require(len(before) == len(after), 'Queue line count mismatch')
    positions = [i for i, b in enumerate(before) if b'| 30005519 / OWR-13750332-001 |' in b]
    require(len(positions) == 1, 'Queue target not unique')
    i = positions[0]
    require(i + 1 == d['row_line_1_based'], 'Queue row position mismatch')
    require(before[:i] == after[:i] and before[i+1:] == after[i+1:], 'Unrelated queue byte change')
    x, y = before[i].split(b'|'), after[i].split(b'|')
    require(len(x) == len(y), 'Queue cell count mismatch')
    require([j for j in range(len(x)) if x[j] != y[j]] == [8, 9, 11], 'Unexpected changed cells')
    for j, change in zip((8, 9, 11), d['changes']):
        require(x[j].decode().strip() == change['old'] and y[j].decode().strip() == change['new'],
                'Queue cell value mismatch')
    require(y[8].strip() == b'already_solved' and y[9].strip() == b'1/5', 'Disposition mismatch')
    return {'status': 'PASS', 'changed_cells': ['Status', 'Turns', 'Findings'],
            'all_other_bytes_preserved': True, 'stale_header_preserved': True}


def replay(root):
    out = {}
    for label, script, result, expected in (
        ('author', 'author/verify.py', 'author/RESULTS.json', 710862),
        ('independent', 'audit/independent_verify.py', 'audit/INDEPENDENT_RESULTS.json', 391846)):
        modes = []
        for flags in ([], ['-O']):
            run = subprocess.run([sys.executable, *flags, str(root / script)],
                                 check=True, capture_output=True)
            require(run.stdout == (root / result).read_bytes(), label + ' replay bytes differ')
            parsed = json.loads(run.stdout)
            require(parsed['status'] == 'PASS' and parsed['total_checks'] == expected,
                    label + ' replay check count mismatch')
            modes.append('optimized' if flags else 'normal')
        out[label] = {'checks_each_mode': expected, 'modes': modes, 'exact_result_bytes': True}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--replay', action='store_true')
    ap.add_argument('--queue-base', type=Path)
    ap.add_argument('--queue-updated', type=Path)
    args = ap.parse_args()
    require(bool(args.queue_base) == bool(args.queue_updated), 'Supply both queue paths')
    root = Path(__file__).resolve().parent
    output = verify(root)
    if args.queue_base:
        output['queue'] = verify_queue(root, args.queue_base, args.queue_updated)
    if args.replay:
        output['replay'] = replay(root)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
