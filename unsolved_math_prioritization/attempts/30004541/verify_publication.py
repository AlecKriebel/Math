#!/usr/bin/env python3
"""Offline portable packet verification. Finite controls are not a proof checker."""
from pathlib import Path
import base64
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent

def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def run(path, *args):
    return json.loads(subprocess.check_output([sys.executable, str(path), *map(str, args)], text=True))

def verify():
    manifest = json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_text())
    expected = set(manifest['files']) | {'PUBLICATION_MANIFEST.json'}
    found = set()
    dirs = set()
    for path in ROOT.rglob('*'):
        assert not path.is_symlink(), f'Symlink: {path.name}'
        name = path.relative_to(ROOT).as_posix()
        if path.is_dir():
            dirs.add(name)
        else:
            assert path.is_file(), f'Non-file: {name}'
            found.add(name)
    assert found == expected, {'missing': sorted(expected-found), 'unexpected': sorted(found-expected)}
    expected_dirs = {str(parent) for name in expected for parent in Path(name).parents if str(parent) != '.'}
    assert dirs == expected_dirs, 'Unexpected/missing directory'
    for name, want in manifest['files'].items():
        assert meta((ROOT/name).read_bytes()) == want, f'Bytes changed: {name}'
    specs = [
        ('DERRIDA_30004541_AUTHOR_SAFE_FREEZE.zip', 'author', 'derrida_30004541',
         {'bytes': 24145, 'sha256': '87523ba565a385498b3f779924373a20e3fc0b6c75d596e8d1aa91f4de33b750'}),
        ('DERRIDA_30004541_INDEPENDENT_AUDIT_SAFE.zip', 'audit', 'derrida_30004541_independent_audit',
         {'bytes': 20059, 'sha256': '8856e9a4e4333a83ea080bfb38d8fdbb0bfbcb8237ab904ae9060cf4c7d15c67'})
    ]
    with tempfile.TemporaryDirectory(prefix='derrida-publication-') as temporary:
        tmp = Path(temporary)
        for name, folder, prefix, want in specs:
            encoded = (ROOT/'frozen_archives'/f'{name}.b64').read_bytes()
            data = base64.b64decode(encoded.strip(), validate=True)
            assert base64.b64encode(data)+b'\n' == encoded, 'Noncanonical base64'
            assert meta(data) == want, f'Freeze changed: {name}'
            archive = tmp/name
            archive.write_bytes(data)
            with zipfile.ZipFile(archive) as z:
                files = {p.name for p in (ROOT/folder).iterdir()}
                assert len(z.namelist()) == len(files), 'Duplicate archive member'
                assert set(z.namelist()) == {prefix+'/'+n for n in files}, 'Archive member set'
                for member in z.namelist():
                    assert z.read(member) == (ROOT/folder/Path(member).name).read_bytes(), member
        author_manifest = run(ROOT/'author/verify_manifest.py')
        audit_manifest = run(ROOT/'audit/verify_audit_manifest.py')
        author = run(ROOT/'author/verify_controls.py')
        assert author == json.loads((ROOT/'author/EXACT_CHECKS.json').read_text())
        independent = run(ROOT/'audit/verify_independent.py', '--author-dir', ROOT/'author',
                          '--archive', tmp/specs[0][0])
        assert independent == json.loads((ROOT/'audit/INDEPENDENT_CHECKS.json').read_text())
        assert author_manifest['status'] == audit_manifest['status'] == author['status'] == independent['status'] == 'PASS'
    binding = json.loads((ROOT/'SOURCE_BINDING.json').read_text())
    result = json.loads((ROOT/'audit/AUDIT_RESULT.json').read_text())
    readiness = json.loads((ROOT/'author/readiness.json').read_text())
    assert binding['problem_id'] == result['problem_id'] == readiness['problem_id'] == 30004541
    assert binding['review_hash'] == result['review_hash'] == readiness['review_hash']
    assert result['full_resolution_proved'] is False and result['novelty_certified'] is False
    assert result['approaches'] == 5 and result['required_corrections'] == []
    return {'status': 'PASS', 'packet_files': len(expected), 'author_controls': author['check_count'],
            'independent_named_checks': independent['named_check_count'],
            'rational_tree_cases': independent['rational_tree_cases'],
            'stationary_negative_controls': len(independent['stationary_negative_controls']),
            'both_freezes_verified': True, 'analytic_proof_certified_by_code': False,
            'hosted_ci_pass_claimed': False}

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
