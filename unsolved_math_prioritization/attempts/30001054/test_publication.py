#!/usr/bin/env python3
"""Relocation and fail-closed checks for the qualified publication wrapper."""
import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def invoke(root, pin, optimized):
    return subprocess.run([sys.executable, '-B'] + (['-O'] if optimized else []) + [str(root / 'verify_publication.py'), '--manifest-sha256', pin], cwd='/', capture_output=True, text=True)

def rewrite(root, name):
    path = root / 'PUBLICATION_MANIFEST.json'
    m = json.loads(path.read_text()); b = (root / name).read_bytes()
    m['files'][name] = {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
    path.write_text(json.dumps(m, sort_keys=True, indent=2) + '\n')

def mutate(root, case):
    if case == 'missing-addendum':
        (root / 'review/PUBLICATION_ADDENDUM.md').unlink()
    elif case == 'changed-addendum-rehashed':
        (root / 'review/PUBLICATION_ADDENDUM.md').write_text('Unqualified acceptance.\n'); rewrite(root, 'review/PUBLICATION_ADDENDUM.md')
    elif case == 'corrupted-archive':
        p = next((root / 'archives').glob('*.zip')); b = p.read_bytes(); p.write_bytes(b[:-1] + bytes([b[-1] ^ 1]))
    elif case == 'changed-extracted-content':
        p = root / 'audit/SCOPE_CORRECTION.md'; p.write_text(p.read_text() + '\nAltered.\n')
    elif case == 'changed-gate-rehashed':
        p = root / 'VERDICT.json'; v = json.loads(p.read_text()); v['effective_gate'] = 'UNQUALIFIED_ACCEPTANCE'; p.write_text(json.dumps(v)); rewrite(root, 'VERDICT.json')
    elif case == 'changed-normalized-scope-rehashed':
        p = root / 'VERDICT.json'; v = json.loads(p.read_text()); v['normalized_polygonal_request'] = 'REFUTED'; p.write_text(json.dumps(v)); rewrite(root, 'VERDICT.json')
    elif case == 'false-author-replay-rehashed':
        p = root / 'VERDICT.json'; v = json.loads(p.read_text()); v['original_author_archive_currently_replayed'] = True; p.write_text(json.dumps(v)); rewrite(root, 'VERDICT.json')
    elif case == 'unexpected-file':
        (root / 'unexpected.txt').write_text('unexpected')
    elif case == 'unexpected-directory':
        (root / 'unexpected').mkdir()
    elif case == 'symlink':
        p = root / 'review/PUBLICATION_ADDENDUM.md'; p.unlink(); p.symlink_to(root / 'README.md')
    elif case == 'malformed-manifest':
        (root / 'PUBLICATION_MANIFEST.json').write_text('{')
    else:
        raise ValueError(case)

def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--manifest-sha256', required=True); args = parser.parse_args()
    tests = []
    cases = ['missing-addendum', 'changed-addendum-rehashed', 'corrupted-archive', 'changed-extracted-content', 'changed-gate-rehashed', 'unexpected-file', 'unexpected-directory', 'symlink', 'malformed-manifest']
    for optimized in (False, True):
        mode = 'optimized' if optimized else 'normal'
        baseline = invoke(ROOT, args.manifest_sha256, optimized)
        require(baseline.returncode == 0, baseline.stderr); tests.append(mode + ':baseline')
        with tempfile.TemporaryDirectory(prefix='double-permutation-publication-') as temp:
            moved = pathlib.Path(temp) / 'relocated package with spaces'; shutil.copytree(ROOT, moved)
            replay = invoke(moved, args.manifest_sha256, optimized)
            require(replay.returncode == 0 and replay.stdout == baseline.stdout, 'relocation failed: ' + replay.stderr)
            tests.append(mode + ':relocation')
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='double-permutation-mutation-') as temp:
                moved = pathlib.Path(temp) / 'package'; shutil.copytree(ROOT, moved); mutate(moved, case)
                got = invoke(moved, args.manifest_sha256, optimized)
                require(got.returncode != 0 and got.stderr.startswith('FAIL:'), 'mutation accepted: ' + case)
                tests.append(mode + ':' + case)
        # With a caller-updated external pin, inner immutable-archive and semantic
        # guards must still reject these changes. This is distinct from testing
        # the historical external pin against a rewritten local manifest.
        for case in ['changed-addendum-rehashed', 'changed-gate-rehashed', 'changed-normalized-scope-rehashed', 'false-author-replay-rehashed']:
            with tempfile.TemporaryDirectory(prefix='double-permutation-inner-guard-') as temp:
                moved = pathlib.Path(temp) / 'package'; shutil.copytree(ROOT, moved); mutate(moved, case)
                new_pin = hashlib.sha256((moved / 'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()
                got = invoke(moved, new_pin, optimized)
                require(got.returncode != 0 and got.stderr.startswith('FAIL:') and 'external manifest pin mismatch' not in got.stderr, 'inner guard not exercised: ' + case)
                tests.append(mode + ':caller-updated-pin:' + case)
        with tempfile.TemporaryDirectory(prefix='double-permutation-root-link-') as temp:
            link = pathlib.Path(temp) / 'linked-root'; link.symlink_to(ROOT, target_is_directory=True)
            got = invoke(link, args.manifest_sha256, optimized)
            require(got.returncode != 0 and got.stderr.startswith('FAIL: invalid root'), 'symlink script root accepted')
            command = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(ROOT / 'verify_publication.py'), str(link), '--manifest-sha256', args.manifest_sha256]
            explicit = subprocess.run(command, cwd='/', capture_output=True, text=True)
            require(explicit.returncode != 0 and explicit.stderr.startswith('FAIL: invalid root'), 'explicit symlink root accepted')
            tests.extend([mode + ':symlink-script-root', mode + ':explicit-symlink-root'])
        wrong = invoke(ROOT, '0' * 64, optimized)
        require(wrong.returncode != 0 and wrong.stderr.startswith('FAIL:'), 'wrong external pin accepted')
        tests.append(mode + ':wrong-external-pin')
    print(json.dumps({'result': 'PASS', 'control_count': len(tests), 'controls': tests}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
