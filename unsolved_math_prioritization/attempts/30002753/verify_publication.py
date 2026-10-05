#!/usr/bin/env python3
"""Fail-closed, portable replay of a frozen partial-result publication."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile

PINS = {
    'safe_release/MANIFEST.json': 'dbc674b5e74de6e98a077b3eb5fd6a5b38e6566a89c6b629f54d7d8c0db9b31e',
    'audit_release/MANIFEST.json': 'df64fe4b0063fc56ac0cff182f4282c471fa64bbc4f3bd6dd781fdd9a7401c49',
    'transpositions_30002753_safe.tar.gz': '051c82bb55cc5cd3a967b128db8c560065000ec5db81753cdb78016ef2e3755c',
    'transpositions_30002753_independent_audit.tar.gz': 'e2250e618e1fb986f2670b84fffc8ddd6f4f88130a0560d9dffa8802657445e3',
}

def need(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def regular(path):
    need(path.is_file() and not path.is_symlink(), 'nonregular file: ' + str(path))
    return path.read_bytes()

def bind(root, expected):
    need(re.fullmatch('[0-9a-f]{64}', expected) is not None, 'invalid external pin')
    raw = regular(root / 'MANIFEST.json')
    need(sha(raw) == expected, 'external publication manifest mismatch')
    manifest = json.loads(raw)
    need(manifest['schema'] == 'transpositions-publication-manifest-v1', 'manifest schema')
    names = set()
    for item in manifest['files']:
        need(set(item) == {'path', 'bytes', 'sha256'}, 'record schema')
        name = item['path']
        need(isinstance(name, str) and name not in names and name != 'MANIFEST.json', 'duplicate/self path')
        p = Path(name)
        need(not p.is_absolute() and '..' not in p.parts and str(p) == name, 'unsafe path')
        need(type(item['bytes']) is int and item['bytes'] >= 0, 'invalid byte count')
        need(isinstance(item['sha256'], str) and re.fullmatch('[0-9a-f]{64}', item['sha256']) is not None, 'invalid digest')
        data = regular(root / name)
        need(len(data) == item['bytes'] and sha(data) == item['sha256'], 'file mismatch: ' + name)
        names.add(name)
    entries = list(root.rglob('*'))
    need(not any(p.is_symlink() for p in entries), 'symlink in packet')
    need({p.relative_to(root).as_posix() for p in entries if p.is_file()} == names | {'MANIFEST.json'}, 'unexpected or missing file')
    expected_dirs = {str(p) for name in names for p in Path(name).parents if str(p) != '.'}
    need({p.relative_to(root).as_posix() for p in entries if p.is_dir()} == expected_dirs, 'unexpected directory')
    for name, pin in PINS.items():
        need(sha(regular(root / name)) == pin, 'frozen pin mismatch: ' + name)
    for folder, archive, count, size in [
        ('safe_release', 'transpositions_30002753_safe.tar.gz', 10, 18329),
        ('audit_release', 'transpositions_30002753_independent_audit.tar.gz', 15, 25174),
    ]:
        need(len(regular(root / archive)) == size, 'archive size mismatch')
        inner = json.loads(regular(root / folder / 'MANIFEST.json'))
        inner_names = ['MANIFEST.json'] + [r['path'] for r in inner['files']]
        need(len(inner_names) == count and len(set(inner_names)) == count, 'inner manifest inventory')
        need(set(inner_names) == {p.name for p in (root / folder).iterdir()}, 'inner inventory mismatch')
        for row in inner['files']:
            need(Path(row['path']).name == row['path'], 'unsafe inner path')
            data = regular(root / folder / row['path'])
            need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'inner manifest binding')
        with tarfile.open(root / archive, 'r:gz') as stream:
            members = stream.getmembers()
            need(len(members) == count, 'archive member count')
            need({m.name for m in members} == {folder + '/' + x for x in inner_names}, 'archive member set')
            for member in members:
                need(member.isfile() and not member.issym() and not member.islnk(), 'nonregular archive member')
                need(stream.extractfile(member).read() == regular(root / member.name), 'archive member mismatch')
    return len(names) + 1

def probe(path, function, arguments):
    spec = importlib.util.spec_from_file_location('publication_probe_' + path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        getattr(module, function)(*arguments)
    except AssertionError:
        return True
    raise ValueError('assertion failure probe did not fail: ' + str(path))

def replay(script, arguments, cwd):
    environment = dict(os.environ)
    environment.pop('PYTHONOPTIMIZE', None)
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    result = subprocess.run([sys.executable, '-B', str(script)] + list(map(str, arguments)), cwd=cwd, env=environment, capture_output=True, text=True)
    need(result.returncode == 0, 'replay failed: ' + str(script) + '\n' + result.stderr)
    return json.loads(result.stdout)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-manifest', required=True)
    parser.add_argument('--queue', type=Path)
    args = parser.parse_args()
    need(__debug__ and sys.flags.optimize == 0, 'Python optimization is forbidden; assertions must remain active')
    sys.dont_write_bytecode = True
    root = Path(__file__).resolve().parent
    count = bind(root, args.expected_manifest)
    probes = {
        'author': probe(root / 'safe_release/verify.py', 'check', (False, 'false-input guard')),
        'independent': probe(root / 'audit_release/independent_controls.py', 'require', (False, 'false-input guard')),
        'symbolic': probe(root / 'audit_release/symbolic_controls.py', 'identity', (0, 1, 'false identity guard')),
    }
    with tempfile.TemporaryDirectory(prefix='transpositions-replay-') as temporary:
        author = replay(root / 'safe_release/verify.py', [], temporary)
        independent = replay(root / 'audit_release/independent_controls.py', [], temporary)
        symbolic = replay(root / 'audit_release/symbolic_controls.py', [], temporary)
        binding = replay(root / 'audit_release/verify_binding.py', [root], temporary)
        exploration = replay(root / 'audit_release/check_exploration.py', [root / 'safe_release/EXPLORATORY_RESULTS.json'], temporary)
    for actual, saved in [(author, 'AUTHOR_REPLAY.json'), (independent, 'INDEPENDENT_RESULTS.json'),
                          (symbolic, 'SYMBOLIC_RESULTS.json'), (binding, 'BINDING.json'),
                          (exploration, 'EXPLORATORY_RECHECK.json')]:
        need(actual == json.loads(regular(root / 'audit_release' / saved)), 'saved result differs: ' + saved)
    need(author['arithmetic_assertions'] == 113 and author['permutation_states_enumerated'] == 872, 'author counts')
    need(independent['exact_assertions'] == 187 and len(independent['negative_controls']) == 9, 'independent counts')
    need(symbolic['symbolic_assertions'] == 19 and len(binding['negative_controls']) == 4, 'symbolic/binding counts')
    need(exploration['results'][0]['agreement_with_reported_within_1e-9'] is False, 'exploratory precision qualification lost')
    queue_verified = False
    if args.queue is not None:
        data = regular(args.queue)
        metadata = json.loads(regular(root / 'PUBLICATION.json'))['queue']
        need(len(data) == metadata['updated_bytes'] and sha(data) == metadata['updated_sha256'], 'queue bytes mismatch')
        need(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == metadata['updated_git_blob_sha1'], 'queue Git blob mismatch')
        queue_verified = True
    need(bind(root, args.expected_manifest) == count, 'packet changed during replay')
    print(json.dumps({'outcome': 'PASS_RETAINED_PARTIALS_WITH_EXPLORATORY_PRECISION_QUALIFICATION',
        'status': 'unsolved', 'turns': '5/5', 'publication_files': count,
        'external_manifest_sha256': args.expected_manifest, 'assertion_failure_probes': probes,
        'author_assertions': 113, 'author_states': 872, 'independent_assertions': 187,
        'symbolic_assertions': 19, 'mathematical_negative_controls': 9, 'binding_negative_controls': 4,
        'all_five_saved_results_match': True, 'both_archives_match_original_directories': True,
        'exploratory_n3_1e_minus_9_reproducibility': False, 'exact_witness_qualification_unaffected': True,
        'queue_verified': queue_verified, 'all_n_order_solved': False}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
