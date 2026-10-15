#!/usr/bin/env python3
"""Fail-closed byte validation and isolated exact replay of the frozen release."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def validate(root, expected):
    root = Path(root).resolve()
    raw = (root / 'PUBLIC_MANIFEST.json').read_bytes()
    require(len(expected) == 64 and sha(raw) == expected, 'Public manifest anchor mismatch')
    m = json.loads(raw)
    require(m['problem_id'] == 30000717 and m['status'] == 'claimed_solved' and m['turns'] == '1/5', 'Release scope mismatch')
    files = m['files']
    require(isinstance(files, dict) and files, 'Empty file manifest')
    actual = set()
    for f in root.rglob('*'):
        require(not f.is_symlink(), 'Symlinks are forbidden')
        if f.is_file():
            actual.add(f.relative_to(root).as_posix())
    require(actual == set(files) | {'PUBLIC_MANIFEST.json'}, 'File set mismatch')
    for name, record in files.items():
        q = PurePosixPath(name)
        require(not q.is_absolute() and all(x not in ('', '.', '..') for x in q.parts) and q.as_posix() == name, 'Unsafe file path')
        b = (root / name).read_bytes()
        require(len(b) == record['bytes'] and sha(b) == record['sha256'], 'Byte mismatch: ' + name)
    anchors = {
        'author/PROOF.md': 'a2e2109d45f7776103fc43cff554c7f49de1b9290b92dc62b3d3db5ad23050c1',
        'author/MANIFEST.json': '0256537fe98d411ca8911c22b341785d029e1f4b51f3a20207e056789bc8e380',
        'audit_a/AUDIT_MANIFEST.json': '8f2276ab950aa2593e4e69902d7679f429c49cf480ba444c666cba61b8cc5a9f',
        'audit_b/AUDIT_REPORT.md': '41a53e6b00bd7036cc7d3d510c4f3b442e667f53442c0aedeff733eb7f9cb256',
    }
    for name, digest in anchors.items():
        require(sha((root / name).read_bytes()) == digest, 'Frozen acceptance mismatch: ' + name)
    for folder, mn, key in [('author', 'MANIFEST.json', 'files'), ('audit_a', 'AUDIT_MANIFEST.json', 'files'), ('audit_b', 'AUDIT_MANIFEST.json', 'audit_artifacts')]:
        frozen = json.loads((root / folder / mn).read_bytes())
        for item in frozen[key]:
            name = folder + '/' + item['path']
            require(files.get(name) == {'bytes': item['bytes'], 'sha256': item['sha256']}, 'Nested manifest mismatch: ' + name)
    return m

def replay(root, expected):
    m = validate(root, expected)
    import sympy
    require(sympy.__version__ == '1.14.0', 'Requires SymPy 1.14.0')
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    with tempfile.TemporaryDirectory(prefix='robinson-release-') as td:
        r = Path(td) / 'packet'
        shutil.copytree(root, r)
        def run(relative):
            process = subprocess.run([sys.executable, '-I', '-B', str(r / relative)], cwd=td, env=env, capture_output=True, timeout=120)
            require(process.returncode == 0, 'Replay failed: ' + relative + '\n' + process.stderr.decode(errors='replace'))
            return process.stdout
        author = run('author/verify.py')
        require(author == (r / 'author/checks.json').read_bytes(), 'Author output mismatch')
        require(json.loads(author)['assertions'] == 185, 'Author assertion count mismatch')
        run('audit_a/checks/verify_robinson_obstruction_independent.py')
        require((r / 'audit_a/results/independent_exact_checks.json').read_bytes() == (Path(root) / 'audit_a/results/independent_exact_checks.json').read_bytes(), 'Audit A output mismatch')
        second = run('audit_b/checks/independent_verify.py')
        require(second == (r / 'audit_b/checks/independent_results.json').read_bytes(), 'Audit B output mismatch')
        require(json.loads(second)['check_count'] == 51, 'Audit B assertion count mismatch')
        for name in ['audit_a/results/candidate_verifier_rerun.json', 'audit_a/results/candidate_v2_verifier_rerun.json', 'audit_b/checks/author_checks_replayed.json']:
            require(author == (r / name).read_bytes(), 'Saved author replay mismatch: ' + name)
        validate(r, expected)
    validate(root, expected)
    return {'verdict': 'PASS', 'problem_id': 30000717, 'author_assertions': 185, 'audit_a_replay': 'byte-identical', 'audit_b_assertions': 51, 'all_frozen_files_unchanged': True, 'manifest_sha256': expected, 'file_count': len(m['files']) + 1, 'scope': 'Exact finite algebra controls and artifact integrity; not formal proof certification.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-manifest', required=True, help='Trusted SHA256 published in the PR description')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    if args.check_only:
        validate(root, args.expected_manifest)
        print(json.dumps({'verdict': 'PASS_INTEGRITY'}))
    else:
        print(json.dumps(replay(root, args.expected_manifest), indent=2, sort_keys=True))
