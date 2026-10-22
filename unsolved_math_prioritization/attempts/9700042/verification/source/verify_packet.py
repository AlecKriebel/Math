#!/usr/bin/env python3
"""Authenticate the packet, replay patches, and rerun finite diagnostics.

Uses only the Python standard library and the system's patch utility. The
mathematical proof and its external inputs are not established by these tests.
Frozen checker bytes are compiled with optimize=0 even under Python -O.
All generated checker outputs live in temporary directories, never this packet.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MODES = [[], ['-O'], ['-I'], ['-I', '-O']]
CHECKERS = [
    ('verify_resume_turn1.py', 'TURN_C1_CHECKS.json'),
    ('verify_resume_turn4.py', 'TURN_C4_CHECKS.json'),
    ('audit_c1/check_independent.py', 'audit_c1/INDEPENDENT_CHECKS.json'),
    ('audit_a/check_independent_c4.py', 'audit_a/INDEPENDENT_CHECKS.json'),
    ('audit_b/independent_checks.py', 'audit_b/INDEPENDENT_CHECKS.json'),
]
PATCHES = [
    ('TURN_C1_MARKED_DEFECT_BOUND.md', 'audit_c1/C1_CLARIFICATION.patch', 'audit_c1/TURN_C1_CLARIFIED.md'),
    ('TURN_C4_BK_POISSON_CANDIDATE.md', 'C4_CLARIFICATION.patch', 'TURN_C4_BK_POISSON_REVISED.md'),
]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def authenticate(root):
    manifest = json.loads((root / 'PACKET_MANIFEST.json').read_text())
    expected = {x['path'] for x in manifest['files']} | {'PACKET_MANIFEST.json'}
    actual = {str(x.relative_to(root)) for x in root.rglob('*') if x.is_file()}
    require(actual == expected, 'Unexpected or missing packet paths')
    for record in manifest['files']:
        path = root / record['path']
        require(not path.is_symlink(), 'Symbolic link is not a packet file')
        data = path.read_bytes()
        require((len(data), sha256(data), git_blob(data)) ==
                (record['bytes'], record['sha256'], record['git_blob']),
                'Authentication failed: ' + record['path'])
    return len(manifest['files'])


# The script hash is checked in the new subprocess before parsing or execution.
# optimize=0 retains all frozen assert statements in each interpreter mode.
BOOTSTRAP = r'''
import ast, hashlib, pathlib, sys
p = pathlib.Path(sys.argv[1]); expected = sys.argv[2]; negative = sys.argv[3] == 'negative'
b = p.read_bytes()
if hashlib.sha256(b).hexdigest() != expected:
    raise RuntimeError('Checker hash mismatch before execution')
t = ast.parse(b, filename=str(p))
if negative:
    # A forced assertion exercises the assertion-preservation execution gate.
    idx = 1 if t.body and isinstance(t.body[0], ast.Expr) and isinstance(t.body[0].value, ast.Constant) and isinstance(t.body[0].value.value, str) else 0
    t.body.insert(idx, ast.Assert(test=ast.Constant(value=False), msg=ast.Constant(value='NEGATIVE_CONTROL_ASSERTION')))
    ast.fix_missing_locations(t)
ns = {'__name__': '__main__', '__file__': str(p)}
exec(compile(t, str(p), 'exec', optimize=0), ns)
'''


def run_checkers():
    results = []
    for script_name, output_name in CHECKERS:
        script = (ROOT / script_name).read_bytes()
        expected_output = (ROOT / output_name).read_bytes()
        modes = []
        for mode in MODES:
            with tempfile.TemporaryDirectory(prefix='oriented-flow-check-') as td:
                p = Path(td) / Path(script_name).name
                p.write_bytes(script)
                cmd = [sys.executable, *mode, '-c', BOOTSTRAP, str(p), sha256(script)]
                run = subprocess.run(cmd + ['positive'], cwd=td, capture_output=True, timeout=600)
                require(run.returncode == 0, 'Checker failed: ' + script_name + ': ' + run.stderr.decode())
                actual = p.with_name(Path(output_name).name).read_bytes()
                require(actual == expected_output, 'Output bytes differ: ' + script_name)
                # This tests that -O cannot erase failure assertions in the wrapper.
                neg = subprocess.run(cmd + ['negative'], cwd=td, capture_output=True, timeout=30)
                require(neg.returncode != 0 and b'NEGATIVE_CONTROL_ASSERTION' in neg.stderr,
                        'Assertion negative control was not rejected')
                # Corrupting authenticated source bytes must fail before execution.
                p.write_bytes(script + b'\n# intentional corruption\n')
                corrupt = subprocess.run(cmd + ['positive'], cwd=td, capture_output=True, timeout=30)
                require(corrupt.returncode != 0 and b'Checker hash mismatch before execution' in corrupt.stderr,
                        'Hash negative control was not rejected')
                modes.append({'flags': mode, 'exit_code': run.returncode,
                              'output_bytes': len(actual), 'output_sha256': sha256(actual),
                              'matches_frozen_output': True,
                              'forced_assertion_rejected': True, 'corrupt_checker_rejected': True})
        results.append({'checker': script_name, 'checker_sha256': sha256(script),
                        'assertions_compiled_with_optimize': 0, 'modes': modes})
    return results


def replay_patches():
    require(shutil.which('patch') is not None, 'The system patch utility is required')
    results = []
    for original, patch_name, revised in PATCHES:
        with tempfile.TemporaryDirectory(prefix='oriented-flow-patch-') as td:
            p = Path(td) / Path(original).name
            p.write_bytes((ROOT / original).read_bytes())
            command = ['patch', '--batch', '--fuzz=0', str(p)]
            run = subprocess.run(command, input=(ROOT / patch_name).read_bytes(), cwd=td, capture_output=True)
            require(run.returncode == 0, 'Patch application failed: ' + patch_name)
            expected = (ROOT / revised).read_bytes()
            require(p.read_bytes() == expected, 'Patch result differs: ' + revised)
            # Destroy a required context line and reject the real patch with no fuzz.
            data = (ROOT / original).read_bytes()
            patch_lines = (ROOT / patch_name).read_text().splitlines(keepends=True)
            context = next(x[1:].encode() for x in patch_lines if x.startswith(' ') and x[1:].strip())
            require(context in data, 'No patch context available for negative control')
            p.write_bytes(data.replace(context, b'INTENTIONALLY_CHANGED_PATCH_CONTEXT\n', 1))
            negative = subprocess.run(command, input=(ROOT / patch_name).read_bytes(), cwd=td, capture_output=True)
            require(negative.returncode != 0, 'Damaged patch context was not rejected')
            results.append({'original': original, 'patch': patch_name, 'revised': revised,
                            'revised_bytes': len(expected), 'revised_sha256': sha256(expected),
                            'actual_patch_replay_matches': True, 'damaged_context_rejected': True})
    return results


def integrity_negative_controls():
    with tempfile.TemporaryDirectory(prefix='oriented-flow-integrity-') as td:
        p = Path(td) / 'packet'
        shutil.copytree(ROOT, p)
        target = p / 'TURN_C4_BK_POISSON_REVISED.md'
        original = target.read_bytes()
        target.write_bytes(original + b'\n')
        try:
            authenticate(p)
        except RuntimeError:
            pass
        else:
            raise RuntimeError('Corrupt proof accepted')
        target.write_bytes(original)
        (p / 'UNEXPECTED.txt').write_text('unexpected')
        try:
            authenticate(p)
        except RuntimeError:
            pass
        else:
            raise RuntimeError('Unexpected file accepted')
    return {'corrupt_proof_rejected': True, 'unexpected_file_rejected': True}


def main():
    count = authenticate(ROOT)
    if sys.argv[1:] == ['--integrity-only']:
        print(json.dumps({'authenticated_files': count, 'exact_path_set': True}, indent=2))
        return
    require(not sys.argv[1:], 'Usage: python verify_packet.py [--integrity-only]')
    out = {'schema': 'oriented-flow-publication-replay-v1',
           'python': sys.version.split()[0], 'authenticated_before_execution': True,
           'checks_are_finite_diagnostics_only': True,
           'patch_replays': replay_patches(),
           'checkers': run_checkers(),
           'packet_negative_controls': integrity_negative_controls(),
           'all_passed': True}
    authenticate(ROOT)
    print(json.dumps(out, indent=2) + '\n', end='')


if __name__ == '__main__':
    main()
