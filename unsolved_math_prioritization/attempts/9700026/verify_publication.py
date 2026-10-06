#!/usr/bin/env python3
"""Fail-closed publication replay. Use the manifest SHA-256 from outside this tree."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
PINS = {
    'CITY_STABILITY_9700026_AUTHOR_SAFE_FREEZE.zip': (11844, 'adc58ab6c2b52963f303582261ee603470dbf2728eee8b4546c04ba7cf9b201d'),
    'CITY_STABILITY_9700026_AUTHOR_EXTERNAL_MANIFEST.json': (1878, '1e2c8f73e3d7d0bb127773a089901d11d70f3f44445f08f128c399ee71c68fe9'),
    'CITY_STABILITY_9700026_INDEPENDENT_AUDIT_SAFE.zip': (43131, 'c4cab38294bbc44310811056fcfe6c2f83ad8b5ab8690ff45438184d368f64fc'),
    'CITY_STABILITY_9700026_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': (4568, '2b67f74197fe8fa032dcf70f5375c8e9f7a958c386c978469aa358738bca4712'),
    'review_b/MANIFEST_B.json': (826, '83ab158511fc5a8fe4a3550cd04e79dc91779e90759144409ca1d1151675d213'),
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def pin(data):
    return len(data), hashlib.sha256(data).hexdigest()

def safe_path(name):
    p = PurePosixPath(name)
    require(type(name) is str and not p.is_absolute() and '..' not in p.parts
            and name == p.as_posix() and name not in ('', '.'), 'Unsafe member path')
    return ROOT.joinpath(*p.parts)

def manifest_check(manifest_name, expected_sha):
    raw = (ROOT / manifest_name).read_bytes()
    require(len(expected_sha) == 64 and hashlib.sha256(raw).hexdigest() == expected_sha,
            'Externally pinned publication manifest mismatch')
    m = json.loads(raw)
    require(m['schema'] == 'city-ode-publication-manifest-v1' and m['problem_id'] == '9700026',
            'Publication manifest identity mismatch')
    rows = m['files']
    names = [r['path'] for r in rows]
    require(len(names) == len(set(names)) and manifest_name not in names,
            'Duplicate or circular publication member')
    all_paths = list(ROOT.rglob('*'))
    require(not any(p.is_symlink() for p in all_paths), 'Symlinks forbidden')
    actual = {p.relative_to(ROOT).as_posix() for p in all_paths if p.is_file()}
    require(actual == set(names) | {manifest_name}, 'Exact publication inventory mismatch')
    for r in rows:
        require(pin(safe_path(r['path']).read_bytes()) == (r['bytes'], r['sha256']),
                'Publication member mismatch: ' + r['path'])
    return len(rows), hashlib.sha256(raw).hexdigest()

def archive_check(archive, manifest, expansion):
    m = json.loads((ROOT / manifest).read_bytes())
    rows = m['files']
    names = [r['path'] for r in rows]
    require(len(names) == len(set(names)), 'Duplicate archive manifest entry')
    count = 0
    with zipfile.ZipFile(io.BytesIO((ROOT / archive).read_bytes())) as z:
        require(len(z.namelist()) == len(names) and set(z.namelist()) == set(names),
                'Exact ZIP inventory mismatch')
        require(z.testzip() is None, 'ZIP CRC mismatch')
        for r in rows:
            data = z.read(r['path'])
            require(pin(data) == (r['bytes'], r['sha256']), 'ZIP member pin mismatch')
            require(safe_path(expansion + '/' + r['path']).read_bytes() == data,
                    'ZIP expansion differs')
            count += 1
    return count

def run(path, *args):
    flags = ['-I', '-B'] + (['-O'] if sys.flags.optimize else [])
    p = subprocess.run([sys.executable, *flags, str(ROOT / path), *map(str, args)],
                       cwd=ROOT, capture_output=True, text=True, timeout=90)
    require(p.returncode == 0, 'Checker failed: ' + path + ': ' + p.stderr[:500])
    result = json.loads(p.stdout)
    require(result.get('status') == 'PASS', 'Checker did not report PASS: ' + path)
    return result

def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--manifest-sha256', required=True)
    a.add_argument('--corpus', type=Path)
    a.add_argument('--sources', type=Path)
    args = a.parse_args()
    require((args.corpus is None) == (args.sources is None), 'Supply both corpus and sources')
    count, digest = manifest_check('PUBLICATION_MANIFEST.json', args.manifest_sha256)
    for name, expected in PINS.items():
        require(pin((ROOT / name).read_bytes()) == expected, 'Frozen input mismatch: ' + name)
    archives = {}
    for prefix, folder in [('AUTHOR', 'author'), ('INDEPENDENT_AUDIT', 'audit_a')]:
        archives[prefix] = archive_check('CITY_STABILITY_9700026_' + prefix + '_SAFE' +
            ('_FREEZE' if prefix == 'AUTHOR' else '') + '.zip',
            'CITY_STABILITY_9700026_' + prefix + '_EXTERNAL_MANIFEST.json', folder)
    b = json.loads((ROOT / 'review_b/MANIFEST_B.json').read_bytes())
    require(len(b['files']) == 4 and len({r['path'] for r in b['files']}) == 4,
            'Review B inventory mismatch')
    for row in b['files']:
        require(pin(safe_path('review_b/' + row['path']).read_bytes()) ==
                (row['bytes'], row['sha256']), 'Review B member mismatch')
    acceptance_a = json.loads((ROOT / 'audit_a/ACCEPTANCE.json').read_bytes())
    acceptance_b = json.loads((ROOT / 'review_b/ACCEPTANCE_B.json').read_bytes())
    require(acceptance_a['verdict'] == 'ACCEPT_LITERAL_COUNTEREXAMPLE_UNCHANGED'
            and acceptance_a['repairs_required'] is False, 'Audit A acceptance mismatch')
    require(acceptance_b['verdict'] == 'ACCEPT_FULL_LITERAL_NEGATIVE_WITH_EXPLICIT_SCOPE'
            and acceptance_b['author_changes_required'] is False, 'Review B acceptance mismatch')
    checkers = {
        'author': run('author/verify.py'),
        'author_self_test': run('author/verify.py', '--self-test'),
        'audit_a': run('audit_a/verify_audit.py'),
        'audit_a_self_test': run('audit_a/verify_audit.py', '--self-test'),
    }
    source = {'status': 'NOT_RUN', 'reason': 'External complete corpus and PDFs not supplied.'}
    if args.corpus is not None:
        source = run('audit_a/verify_sources.py', args.corpus.resolve(), args.sources.resolve())
    print(json.dumps({
        'status': 'PASS', 'problem_id': '9700026', 'manifest_sha256': digest,
        'pinned_publication_members': count, 'archive_members_verified': archives,
        'review_b_members_verified': 4, 'unchanged_author_accepted_by_two_independent_reviews': True,
        'checkers': checkers, 'external_inputs': source,
        'proof_status': 'Literal 2007/catalog counterexample accepted; restricted dynamics unresolved.',
        'formal_proof_assistant': False, 'human_peer_review': False, 'novelty_claim': False,
    }, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
