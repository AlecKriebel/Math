"""Replay the self-contained symbolic checks, without assertion-dependent guards."""
import ast
import hashlib
import importlib.metadata
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def main():
    root = pathlib.Path(__file__).resolve().parent
    script = root / 'verify_curvature_identities.py'
    for name in ('run_checks.py', 'verify_curvature_identities.py', 'verify_manifest.py', 'test_corruption_controls.py'):
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse((root / name).read_text()))),
                'Assertion-dependent checker: ' + name)
    expected = json.loads((root / 'CURVATURE_CHECKS.json').read_text())
    require(expected == json.loads((root / 'CURVATURE_CHECKS_OPTIMIZED.json').read_text()), 'Saved references disagree')
    require(expected['status'] == 'PASS' and len(expected['checks']) == 4, 'Invalid reference structure')
    checks = []
    with tempfile.TemporaryDirectory(prefix='lie-psc-replay-') as tmp:
        work = pathlib.Path(tmp)
        shutil.copyfile(script, work / script.name)
        for optimized in (False, True):
            command = [sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [script.name]
            done = subprocess.run(command, cwd=work, capture_output=True, text=True, timeout=120)
            require(done.returncode == 0, 'Checker failed: ' + done.stderr)
            require(not done.stderr, 'Unexpected checker stderr: ' + done.stderr)
            require(json.loads(done.stdout) == expected, 'Exact symbolic result JSON differs')
            require({p.name for p in work.iterdir()} == {script.name}, 'Checker created unexpected files')
            checks.append({'optimized': optimized, 'exit_code': done.returncode, 'exact_reference_match': True,
                           'stdout_sha256': hashlib.sha256(done.stdout.encode()).hexdigest()})
    print(json.dumps({'status': 'PASS', 'overall_problem_status': 'UNSOLVED',
                      'python_version': sys.version.split()[0], 'sympy_version': importlib.metadata.version('sympy'),
                      'checks': checks, 'assertion_nodes_in_checkers': 0,
                      'claim_limit': 'Symbolic consistency checks only, not formal or complete geometric proof verification.'}, indent=2))


if __name__ == '__main__':
    main()
