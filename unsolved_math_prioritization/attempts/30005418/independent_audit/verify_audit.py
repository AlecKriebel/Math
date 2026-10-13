#!/usr/bin/env python3
"""Strict audit/author binding and independent arithmetic replay."""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import zipfile

if not __debug__:
    raise SystemExit('Assertions must be enabled; do not use python -O.')

AUTHOR_MANIFEST = '86dad4963c8b21ab475b2ef612c09ac499bfe11437d72ef81fbcb583c1b10553'
AUTHOR_ZIP = '6c6762fa475fe36c8c14c81fb9895fe9cee8489794d52cc54b08b6101b54981c'
PAYLOAD = {'AUDIT.md', 'CORRECTIONS.md', 'README.md', 'requirements.txt',
           'independent_math.py', 'independent_sources.py', 'verify_audit.py',
           'INDEPENDENT_MATH_RESULTS.json', 'INDEPENDENT_SOURCE_RESULTS.json',
           'SOURCE_INSPECTION.json', 'PRIOR_ATTEMPT_RECHECK.json', 'INTEGRITY_TEST_RESULTS.json'}

def digest(b):
    return hashlib.sha256(b).hexdigest()

def inventory(root, manifest_name, expected_digest=None, expected_files=None):
    mb = (root/manifest_name).read_bytes()
    if expected_digest is not None:
        assert digest(mb) == expected_digest, 'external manifest digest mismatch'
    m = json.loads(mb)
    names = [e['path'] for e in m['files']]
    assert len(names) == len(set(names)), 'duplicate manifest entry'
    assert all(pathlib.PurePosixPath(n).name == n for n in names), 'unsafe member path'
    if expected_files is not None:
        assert set(names) == expected_files, 'unexpected manifest inventory'
    contents = list(root.iterdir())
    assert all(p.is_file() and not p.is_symlink() for p in contents), 'directory or symlink present'
    assert {p.name for p in contents} == set(names)|{manifest_name}, 'unexpected directory inventory'
    for item in m['files']:
        b = (root/item['path']).read_bytes()
        assert len(b) == item['bytes'] and digest(b) == item['sha256'], item['path']
    return m, digest(mb)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('author_safe', type=pathlib.Path)
    parser.add_argument('--author-zip', type=pathlib.Path)
    parser.add_argument('--expected-manifest')
    args = parser.parse_args()
    here = pathlib.Path(__file__).resolve().parent
    author = args.author_safe.resolve()
    am, mh = inventory(here, 'AUDIT_MANIFEST.json', args.expected_manifest, PAYLOAD)
    assert am['problem_id'] == 30005418 and am['general_outcome'] == 'unsolved'
    assert am['approach_families_used'] == 5 and am['audit_verdict'] == 'PASS_SCOPED_RESULTS'
    original, _ = inventory(author, 'AUTHOR_MANIFEST.json', AUTHOR_MANIFEST)
    assert original['outcome'] == 'unsolved' and original['approach_families_used'] == 5
    zip_status = 'not supplied; author directory and manifest verified'
    if args.author_zip:
        assert digest(args.author_zip.read_bytes()) == AUTHOR_ZIP, 'original ZIP mismatch'
        with zipfile.ZipFile(args.author_zip) as archive:
            names = archive.namelist()
            assert len(names) == len(set(names)), 'duplicate archive member'
            assert set(names) == {p.name for p in author.iterdir()}, 'archive inventory mismatch'
            for name in names:
                assert archive.read(name) == (author/name).read_bytes(), name
        zip_status = 'original bytes and all members verified'
    with tempfile.TemporaryDirectory(prefix='kahler-independent-replay-') as tmp:
        output = pathlib.Path(tmp)/'math.json'
        subprocess.run([sys.executable, '-B', str(author/'verify_packet.py'),
                        '--expected-manifest', AUTHOR_MANIFEST], cwd=tmp,
                       check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, '-B', str(here/'independent_math.py'),
                        str(author), str(output)], cwd=tmp,
                       check=True, stdout=subprocess.DEVNULL)
        assert output.read_bytes() == (here/'INDEPENDENT_MATH_RESULTS.json').read_bytes(), 'independent replay mismatch'
    print(json.dumps({'status': 'PASS', 'problem_id': 30005418, 'general_target': 'UNSOLVED',
                      'audit_manifest_sha256': mh, 'audit_payload_files': len(PAYLOAD),
                      'author_manifest_sha256': AUTHOR_MANIFEST, 'author_zip': zip_status,
                      'author_math_replay': 'byte-identical', 'independent_math_replay': 'byte-identical',
                      'source_scope': 'Historical inspection and full-source hashes recorded; source replay is separate.'}, indent=2))

if __name__ == '__main__':
    main()
