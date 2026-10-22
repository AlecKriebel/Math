#!/usr/bin/env python3
"""Read-only, pinned verification of the frozen author packet, plus copy-only attacks."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

assert __debug__, 'Do not run the verifier with assertions disabled'

EXPECTED_MANIFEST_SHA256 = 'e67ac4e9f37d89fce822f00e4e166b20f21d1051c41e5e2acd595a5709cd95c1'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify(root):
    manifest_path = root / 'AUTHOR_MANIFEST.json'
    assert not manifest_path.is_symlink(), 'manifest symlink'
    raw = manifest_path.read_bytes()
    assert digest(raw) == EXPECTED_MANIFEST_SHA256, 'pinned manifest digest mismatch'
    manifest = json.loads(raw)
    expected = {'AUTHOR_MANIFEST.json': {'bytes':len(raw), 'sha256':digest(raw)}}
    for rec in manifest['files']:
        relative = Path(rec['path'])
        assert not relative.is_absolute() and '..' not in relative.parts, 'unsafe path'
        assert rec['path'] not in expected, 'duplicate path'
        expected[rec['path']] = rec
    actual = set()
    for p in root.rglob('*'):
        assert not p.is_symlink(), 'symlink: ' + str(p.relative_to(root))
        if p.is_file():
            actual.add(p.relative_to(root).as_posix())
    assert actual == set(expected), 'file set mismatch'
    files = []
    for name, rec in sorted(expected.items()):
        data = (root / name).read_bytes()
        assert len(data) == rec['bytes'], 'byte count mismatch: ' + name
        assert digest(data) == rec['sha256'], 'digest mismatch: ' + name
        files.append({'path':name, 'bytes':len(data), 'sha256':digest(data)})
    canonical = ''.join(f"{x['path']}\0{x['bytes']}\0{x['sha256']}\n" for x in files).encode()
    return {'status':'PASS', 'manifest_sha256':digest(raw), 'manifest_bytes':len(raw),
            'manifested_payload_files':len(manifest['files']), 'total_bound_files':len(files),
            'tree_hash_encoding':'SHA256 of sorted UTF-8 path NUL decimal_bytes NUL lowercase_sha256 LF records, including root manifest',
            'author_tree_sha256':digest(canonical), 'files':files,
            'target':{'id':2998,'rank':695,'modern_label':'KP-4.122'},
            'full_solution_claimed':manifest['full_solution_claimed'],
            'novelty_claimed':manifest['novelty_claimed']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--author', default=str(Path(__file__).resolve().parent.parent/'author'))
    parser.add_argument('--output')
    parser.add_argument('--negative-controls', action='store_true')
    args = parser.parse_args()
    root = Path(args.author).resolve()
    report = verify(root)
    if args.negative_controls:
        attacks = ['payload_byte_change', 'same_length_payload_change', 'missing_payload', 'unlisted_nested_manifest', 'matching_bytes_symlink', 'manifest_symlink', 'manifest_byte_change']
        outcomes = []
        with tempfile.TemporaryDirectory(prefix='kp2998_integrity_') as temp:
            temp = Path(temp)
            for n, attack in enumerate(attacks):
                target = temp / str(n)
                shutil.copytree(root, target)
                p = target / 'README.md'
                if attack == 'payload_byte_change':
                    p.write_bytes(p.read_bytes() + b'\n')
                elif attack == 'same_length_payload_change':
                    data = p.read_bytes()
                    p.write_bytes(bytes([data[0] ^ 1]) + data[1:])
                elif attack == 'missing_payload':
                    p.unlink()
                elif attack == 'unlisted_nested_manifest':
                    (target/'unlisted').mkdir()
                    (target/'unlisted'/'AUTHOR_MANIFEST.json').write_text('{"unlisted": true}\n')
                elif attack == 'matching_bytes_symlink':
                    external = temp / ('payload_' + str(n))
                    external.write_bytes(p.read_bytes())
                    p.unlink()
                    p.symlink_to(external)
                elif attack == 'manifest_symlink':
                    m = target/'AUTHOR_MANIFEST.json'
                    external = temp / ('manifest_' + str(n))
                    external.write_bytes(m.read_bytes())
                    m.unlink()
                    m.symlink_to(external)
                else:
                    m = target/'AUTHOR_MANIFEST.json'
                    m.write_bytes(m.read_bytes()+b'\n')
                try:
                    verify(target)
                except (AssertionError, FileNotFoundError) as e:
                    outcomes.append({'attack':attack,'status':'REJECTED','reason':str(e)})
                else:
                    raise AssertionError('mutation accepted: '+attack)
        report['negative_controls'] = outcomes
        report['negative_control_count'] = len(outcomes)
        report['frozen_author_unchanged_after_tests'] = verify(root)['author_tree_sha256'] == report['author_tree_sha256']
    result = json.dumps(report, indent=2, sort_keys=True)+'\n'
    if args.output:
        output = Path(args.output).resolve()
        assert output != root and root not in output.parents
        output.write_text(result)
    print(result,end='')


if __name__ == '__main__':
    main()
