#!/usr/bin/env python3
"""Offline audit replay with optional exact frozen-author binding checks."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent


def require(value, message):
    if not value:
        raise AssertionError(message)


def fingerprint(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def matches(data, entry):
    return fingerprint(data) == {k: entry[k] for k in ('bytes', 'sha256')}


def reject_mutations(data, entry):
    require(bool(data), 'Empty file not expected')
    for mutation in (bytes([data[0] ^ 1]) + data[1:], data[:-1], data + b'!'):
        require(not matches(mutation, entry), 'Integrity negative control failed')
    return 3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-dir', type=Path)
    parser.add_argument('--author-archive', type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    expected = {r['path'] for r in manifest['files']}
    require(len(expected) == len(manifest['files']), 'Duplicate manifest entry')
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    require(actual == expected | {'MANIFEST.json'}, 'Unexpected audit file set')
    negative_count = 0
    for entry in manifest['files']:
        name = entry['path']
        require(Path(name).name == name, 'Nonlocal audit path')
        require(not (ROOT / name).is_symlink(), 'Audit symlink not allowed')
        data = (ROOT / name).read_bytes()
        require(matches(data, entry), 'Audit integrity mismatch: ' + name)
        negative_count += reject_mutations(data, entry)

    output = subprocess.check_output([sys.executable, '-B', str(ROOT / 'independent_checks.py')])
    require(output == (ROOT / 'independent_results.json').read_bytes(), 'Independent replay differs')
    independent = json.loads(output)
    result = json.loads((ROOT / 'RESULT.json').read_text())
    require(result['independent_checks']['assertions'] == independent['assertions'], 'Stale result counter')
    require(result['verdict'] == 'pass' and not result['substantive_defects'], 'Unexpected audit disposition')
    binding = json.loads((ROOT / 'BINDING.json').read_text())
    original_records = {r['path']: r for r in binding['files']}
    require(len(original_records) == 9, 'Wrong bound original file count')
    checked_author = False
    author_report = None
    if args.author_dir is not None:
        actual = {str(p.relative_to(args.author_dir)) for p in args.author_dir.rglob('*') if p.is_file()}
        require(actual == set(original_records), 'Unexpected original file set')
        for name, entry in original_records.items():
            require(Path(name).name == name, 'Nonlocal original path')
            data = (args.author_dir / name).read_bytes()
            require(matches(data, entry), 'Original binding mismatch: ' + name)
            negative_count += reject_mutations(data, entry)
        author_report = json.loads(subprocess.check_output(
            [sys.executable, '-B', str(args.author_dir / 'verify_publication.py')]))
        require(author_report == result['author_replay'], 'Author replay report differs')
        checked_author = True
    checked_archive = False
    if args.author_archive is not None:
        raw = args.author_archive.read_bytes()
        require(matches(raw, binding['frozen_archive']), 'Author archive fingerprint mismatch')
        with zipfile.ZipFile(args.author_archive) as z:
            expected_members = {'4400001/' + n for n in original_records}
            require(len(z.namelist()) == len(expected_members) and set(z.namelist()) == expected_members,
                    'Archive member set differs')
            for name, entry in original_records.items():
                data = z.read('4400001/' + name)
                require(matches(data, entry), 'Archive member mismatch: ' + name)
                if args.author_dir is not None:
                    require(data == (args.author_dir / name).read_bytes(), 'Archive versus directory differs')
        checked_archive = True
    print(json.dumps({
        'status': 'pass', 'audit_files_verified': len(expected),
        'manifest_self_excluded': True, 'independent_replay_byte_identical': True,
        'independent_assertions': independent['assertions'],
        'independent_main_candidate_words': independent['candidate_words_examined'],
        'independent_two_color_control_words': independent['two_color_control_words_examined'],
        'integrity_mutations_rejected': negative_count,
        'author_directory_checked': checked_author, 'author_archive_checked': checked_archive,
        'author_replay': author_report,
        'scope': 'Offline integrity and exact finite controls; source-reading and imported-theorem judgment are not mechanically revalidated.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
