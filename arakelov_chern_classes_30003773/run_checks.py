"""Replay integrity checks, not mathematical theorem verification."""
import ast
import json
import pathlib
import subprocess
import sys

def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)

def main():
    root = pathlib.Path(__file__).resolve().parent
    for name in ('verify_manifest.py', 'run_checks.py', 'test_corruption_controls.py'):
        require(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse((root/name).read_text()))), 'Assertion-dependent checker')
    checks = []
    for optimized in (False, True):
        done = subprocess.run([sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + ['verify_manifest.py'], cwd=root, capture_output=True, text=True, timeout=60)
        require(done.returncode == 0 and not done.stderr, 'Manifest replay failed: ' + done.stderr)
        result = json.loads(done.stdout)
        require(result['status'] == 'PASS' and result['overall_problem_status'] == 'UNSOLVED', 'Invalid replay result')
        checks.append({'optimized': optimized, 'status': 'PASS'})
    print(json.dumps({'status': 'PASS', 'checks': checks, 'assertion_nodes_in_checkers': 0, 'scope': 'Integrity and metadata replay only; not mathematical proof verification.'}, indent=2))

if __name__ == '__main__':
    main()
