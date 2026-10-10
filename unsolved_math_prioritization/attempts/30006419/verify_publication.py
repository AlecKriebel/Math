#!/usr/bin/env python3
"""Authenticate the complete source-free packet, then replay in temporary copies."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, math, os, shutil, subprocess, sys, tempfile

PINS = {
    'author/MANIFEST.json': '9cb1f5c242224d4f04a34b1d28e660a29fb2f63d47215d16257f5d4073c001cb',
    'author/PROOF.md': '2634e714b9a06a1770ae39b0201031c7d2a7ce6e97f3330f8745d0e2453d4fef',
    'author/KOREVAAR_SCHOEN.md': '4bac91a7e34b266391051d48ae2ef10adc60d10b6ed0d57d1c5cb8395e2a6abe',
    'audit_a/AUDIT_MANIFEST.json': 'dd4962a906e248bd347b1ce4296a4817bcc5ce2ac9a0ef417344faf9883fe052',
    'audit_b/AUDIT_MANIFEST.json': '0c7e1f517f62b27734e5e91a7a7209585ecc2b853bdc1d460b4cee7f4013f5dc',
}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def validate(root, expected):
    root = Path(root).resolve()
    manifest = root / 'PUBLIC_MANIFEST.json'
    require(not manifest.is_symlink() and manifest.is_file(), 'Invalid public manifest path')
    raw = manifest.read_bytes()
    require(len(expected) == 64 and sha(raw) == expected, 'External manifest anchor mismatch')
    m = json.loads(raw)
    require(m['problem_id'] == 30006419 and m['status'] == 'claimed_solved' and m['turns'] == '2/5', 'Wrong release scope')
    records = m['files']
    require(isinstance(records, dict) and records, 'Empty manifest')
    directories = set()
    for name, record in records.items():
        q = PurePosixPath(name)
        require(not q.is_absolute() and q.as_posix() == name and all(p not in ('', '.', '..') for p in q.parts), 'Unsafe path')
        for parent in q.parents:
            if parent.as_posix() != '.':
                directories.add(parent.as_posix())
    actual_files, actual_dirs = set(), set()
    for f in root.rglob('*'):
        require(not f.is_symlink(), 'Symlinks forbidden')
        name = f.relative_to(root).as_posix()
        if f.is_file():
            actual_files.add(name)
        elif f.is_dir():
            actual_dirs.add(name)
        else:
            raise RuntimeError('Nonregular path: ' + name)
    require(actual_files == set(records) | {'PUBLIC_MANIFEST.json'}, 'File inventory mismatch')
    require(actual_dirs == directories, 'Directory inventory mismatch')
    for name, record in records.items():
        data = (root / name).read_bytes()
        require(len(data) == record['bytes'] and sha(data) == record['sha256'], 'Byte mismatch: ' + name)
    for name, digest in PINS.items():
        require(sha((root / name).read_bytes()) == digest, 'Frozen acceptance anchor mismatch: ' + name)
    for folder, filename in [('author', 'MANIFEST.json'), ('audit_a', 'AUDIT_MANIFEST.json'), ('audit_b', 'AUDIT_MANIFEST.json')]:
        frozen = json.loads((root / folder / filename).read_bytes())
        require(frozen['problem_id'] == 30006419, 'Wrong nested problem identity')
        require({x.name for x in (root / folder).iterdir()} == set(frozen['files']) | {filename}, 'Frozen inventory mismatch')
        for name, record in frozen['files'].items():
            require(records.get(folder + '/' + name) == record, 'Nested manifest mismatch')
    status = json.loads((root / 'PUBLICATION_STATUS.json').read_bytes())
    require(status['status'] == 'claimed_solved' and status['turns'] == '2/5' and status['frozen_files_preserved'] == 22, 'Disposition mismatch')
    return m

def equivalent(actual, expected, path='root'):
    if isinstance(expected, bool):
        require(type(actual) is bool and actual == expected, 'Boolean mismatch: ' + path)
    elif isinstance(expected, float):
        require(isinstance(actual, (float, int)) and math.isfinite(actual) and math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-10), 'Numerical replay mismatch: ' + path)
    elif isinstance(expected, dict):
        require(isinstance(actual, dict) and actual.keys() == expected.keys(), 'Key mismatch: ' + path)
        for k in expected:
            equivalent(actual[k], expected[k], path + '/' + k)
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(actual) == len(expected), 'List mismatch: ' + path)
        for i, e in enumerate(expected):
            equivalent(actual[i], e, path + '/' + str(i))
    else:
        require(type(actual) is type(expected) and actual == expected, 'Exact replay mismatch: ' + path)

def replay(root, expected, sources=None):
    root = Path(root).resolve()
    manifest = validate(root, expected)
    import numpy, scipy, sympy
    versions = {'numpy': numpy.__version__, 'scipy': scipy.__version__, 'sympy': sympy.__version__}
    require(versions == {'numpy': '2.3.5', 'scipy': '1.17.0', 'sympy': '1.14.0'}, 'Use versions in requirements.txt')
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    flags = ['-I', '-B'] + (['-O'] if sys.flags.optimize else [])
    with tempfile.TemporaryDirectory(prefix='harmonic-sphere-replay-') as tmp:
        r = Path(tmp) / 'packet'
        shutil.copytree(root, r)
        def run(relative, *args):
            p = subprocess.run([sys.executable, *flags, str(r / relative), *map(str, args)], cwd=tmp, env=env, capture_output=True, timeout=180)
            require(p.returncode == 0, 'Control failed: ' + relative + '\n' + p.stderr.decode(errors='replace'))
            return p.stdout
        run('author/verify_manifest.py', '--expected-manifest-sha256', PINS['author/MANIFEST.json'])
        author = run('author/checks.py')
        require(author == (root / 'author/CHECK_RESULTS.json').read_bytes(), 'Author exact output mismatch')
        require(json.loads(author)['total'] == 257, 'Author control count mismatch')
        require(author == (root / 'audit_a/AUTHOR_CONTROL_REPLAY.json').read_bytes(), 'Saved author replay mismatch')
        audit_a = run('audit_a/independent_controls.py')
        saved_a = (root / 'audit_a/INDEPENDENT_CONTROL_RESULTS.json').read_bytes()
        equivalent(json.loads(audit_a), json.loads(saved_a))
        result_path = Path(tmp) / 'audit_b_replayed.json'
        if sources is None:
            run('source_free_audit_b.py', '--manuscript', r / 'author', '--output', result_path)
        else:
            run('audit_b/independent_checks.py', '--manuscript', r / 'author', '--sources', Path(sources).resolve(), '--output', result_path)
        b = json.loads(result_path.read_bytes())
        count = 673 if sources is None else 675
        require(b['status'] == 'PASS' and b['failed'] == 0 and b['checks'] == count and len(b['results']) == count, 'Audit B count or outcome mismatch')
        require(all(item['passed'] is True for item in b['results']), 'Failed Audit B record')
        saved_b = json.loads((root / 'audit_b/CHECK_SUMMARY.json').read_bytes())
        equivalent(b['c'], saved_b['c'])
        equivalent(b['ks_stress_errors'], saved_b['ks_stress_errors'])
        for item in saved_b['selected_results']:
            matches = [q for q in b['results'] if q['name'] == item['name']]
            require(len(matches) == 1, 'Missing selected control')
            equivalent(matches[0], item)
        # Audit A writes only in the disposable copy. Restore its historical
        # output before validating that every other frozen byte stayed intact.
        (r / 'audit_a/INDEPENDENT_CONTROL_RESULTS.json').write_bytes(saved_a)
        validate(r, expected)
    validate(root, expected)
    return {'status': 'PASS', 'problem_id': 30006419, 'manifest_sha256': expected, 'packet_files': len(manifest['files']) + 1, 'frozen_files_preserved': 22, 'author_exact_controls': 257, 'author_output_byte_identical': True, 'audit_a_mixed_controls': 'PASS', 'audit_a_output_byte_identical': audit_a == saved_a, 'audit_b_executed_mixed_checks': count, 'audit_b_historical_full_checks': 675, 'source_identity_checks_omitted': 2 if sources is None else 0, 'source_retrieval_or_inspection_performed': False, 'optimized_children': bool(sys.flags.optimize), 'dependencies': versions, 'scope': 'Finite exact/symbolic and numerical controls plus byte integrity; not formal verification of the analytic theorems.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-manifest', required=True)
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--sources', type=Path, help='Optional local directory of the two public source PDFs; never fetched by this script')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    if args.check_only:
        m = validate(root, args.expected_manifest)
        print(json.dumps({'status': 'PASS_INTEGRITY', 'files': len(m['files']) + 1}))
    else:
        print(json.dumps(replay(root, args.expected_manifest, args.sources), indent=2, sort_keys=True))
