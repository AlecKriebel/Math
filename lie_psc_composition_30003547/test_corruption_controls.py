"""Fail-closed controls in disposable copies. Does not alter package files."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def run(directory, script, optimized):
    args = [sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [script]
    return subprocess.run(args, cwd=directory, capture_output=True, text=True, timeout=180)


def main():
    root = pathlib.Path(__file__).resolve().parent
    results = []
    mutations = ('same_size_manuscript', 'missing_file', 'extra_file', 'wrong_reference', 'wrong_symbolic_coefficient')
    for optimized in (False, True):
        baseline = run(root, 'verify_manifest.py', optimized)
        require(baseline.returncode == 0 and not baseline.stderr, 'Baseline manifest must pass before corruption controls: ' + baseline.stderr)
        for mutation in mutations:
            with tempfile.TemporaryDirectory(prefix='lie-psc-corruption-') as tmp:
                work = pathlib.Path(tmp) / 'package'
                shutil.copytree(root, work)
                target = 'verify_manifest.py'
                diagnostic = ''
                if mutation == 'same_size_manuscript':
                    p = work / 'FIVE_AVENUE_REPORT.md'
                    data = p.read_bytes(); p.write_bytes(bytes([data[0] ^ 1]) + data[1:])
                    diagnostic = 'SHA-256 mismatch'
                elif mutation == 'missing_file':
                    (work / 'SOURCE_CHECKS.json').unlink(); diagnostic = 'Inventory mismatch'
                elif mutation == 'extra_file':
                    (work / 'EXTRA.txt').write_text('unexpected'); diagnostic = 'Inventory mismatch'
                elif mutation == 'wrong_reference':
                    for name in ('CURVATURE_CHECKS.json', 'CURVATURE_CHECKS_OPTIMIZED.json'):
                        p = work / name; obj = json.loads(p.read_text()); obj['checks'][0] = 'corrupted reference'; p.write_text(json.dumps(obj))
                    target = 'run_checks.py'; diagnostic = 'Exact symbolic result JSON differs'
                else:
                    p = work / 'verify_curvature_identities.py'; text = p.read_text()
                    old = 'expected=-2*s.diff(f,x,2)/f-f**2*s.diff(a,x)**2/2'
                    require(text.count(old) == 1, 'Mutation target changed')
                    p.write_text(text.replace(old, 'expected=-3*s.diff(f,x,2)/f-f**2*s.diff(a,x)**2/2'))
                    target = 'run_checks.py'; diagnostic = 'Kaluza-Klein identity failed'
                done = run(work, target, optimized)
                require(done.returncode != 0 and diagnostic in done.stderr,
                        'Corruption not rejected as expected: ' + mutation + '\n' + done.stdout + done.stderr)
                results.append({'mutation': mutation, 'optimized': optimized, 'rejected': True, 'diagnostic': diagnostic})
    print(json.dumps({'status': 'PASS', 'controls': results,
                      'scope': 'Detection of selected accidental tampering and invalid symbolic/reference results, not authentication.'}, indent=2))


if __name__ == '__main__':
    main()
