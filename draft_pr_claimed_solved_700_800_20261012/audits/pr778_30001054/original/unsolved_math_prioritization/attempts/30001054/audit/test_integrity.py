#!/usr/bin/env python3
"""Package controls independent of the literal-word verifier tests."""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent


def require(c, message):
    if not c:
        raise RuntimeError(message)


def run(root, optimized, extra=()):
    return subprocess.run([sys.executable, '-B'] + (['-O'] if optimized else []) +
                          [str(root / 'verify_audit.py')] + list(extra),
                          cwd='/', text=True, capture_output=True)


def rehash(root, name):
    p = root / 'MANIFEST.json'; m = json.loads(p.read_text()); data = (root / name).read_bytes()
    m['files'][name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    p.write_text(json.dumps(m))


def mutate(root, name):
    if name == 'missing-member':
        (root / 'README.md').unlink()
    elif name == 'unexpected-member':
        (root / 'extra.txt').write_text('unexpected')
    elif name == 'symlink-member':
        (root / 'README.md').unlink(); (root / 'README.md').symlink_to(root / 'AUDIT_REPORT.md')
    elif name == 'changed-witness':
        p = root / 'WITNESS.json'; p.write_text('{}')
    elif name == 'duplicate-manifest-key':
        p = root / 'MANIFEST.json'; p.write_text(p.read_text().replace('"schema": 1', '"schema": 1, "schema": 1'))
    elif name == 'boolean-manifest-schema':
        p = root / 'MANIFEST.json'; m = json.loads(p.read_text()); m['schema'] = True; p.write_text(json.dumps(m))
    elif name == 'unqualified-gate-rehashed':
        p = root / 'AUDIT_CERTIFICATE.json'; c = json.loads(p.read_text()); c['audit_gate'] = 'ACCEPTED'; p.write_text(json.dumps(c)); rehash(root, p.name)
    elif name == 'removed-correction-rehashed':
        p = root / 'SCOPE_CORRECTION.md'; p.write_text('All allowable sequences are solved.\n'); rehash(root, p.name)
    elif name == 'wrong-source':
        p = root / 'SOURCES.json'; s = json.loads(p.read_text()); s['sources'][0]['sha256'] = '0' * 64; p.write_text(json.dumps(s)); rehash(root, p.name)
    else:
        raise ValueError(name)


def main():
    checks = []
    cases = ['missing-member', 'unexpected-member', 'symlink-member', 'changed-witness',
             'duplicate-manifest-key', 'boolean-manifest-schema', 'unqualified-gate-rehashed',
             'removed-correction-rehashed', 'wrong-source']
    for optimized in (False, True):
        mode = 'optimized' if optimized else 'normal'
        require(run(ROOT, optimized).returncode == 0, mode + ' baseline')
        checks.append(mode + ':baseline')
        with tempfile.TemporaryDirectory(prefix='double-permutation-package-') as tmp:
            moved = pathlib.Path(tmp) / 'relocated package'; shutil.copytree(ROOT, moved)
            require(run(moved, optimized).returncode == 0, 'Relocation failed')
            checks.append(mode + ':relocation')
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='double-permutation-corrupt-') as tmp:
                moved = pathlib.Path(tmp) / 'package'; shutil.copytree(ROOT, moved); mutate(moved, case)
                result = run(moved, optimized)
                require(result.returncode != 0 and result.stderr.startswith('FAIL:'), 'Mutation accepted: ' + case)
                checks.append(mode + ':' + case)
        with tempfile.TemporaryDirectory(prefix='double-permutation-wrong-archive-') as tmp:
            wrong = pathlib.Path(tmp) / 'wrong.zip'; wrong.write_bytes(b'not the author freeze')
            require(run(ROOT, optimized, ['--author-zip', str(wrong)]).returncode != 0, 'Wrong author archive accepted')
            checks.append(mode + ':wrong-author-archive')
    print(json.dumps({'result': 'PASS', 'count': len(checks), 'checks': checks}, indent=2))


if __name__ == '__main__':
    main()
