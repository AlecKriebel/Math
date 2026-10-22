"""Selected portable replays and enforcement falsifiers, without package writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys, time

HERE = Path(__file__).resolve().parent
P = HERE.parent / 'publication_package_v1/materials'
DEP = HERE.parent.parent / 'pr200_5100007/math_algebra_family_01/runtime_packages'

def require(c, message):
    if not c:
        raise RuntimeError(message)

def clean(x):
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items() if k not in ('UTC', 'elapsed_seconds', 'optimization')}
    if isinstance(x, list):
        return [clean(v) for v in x]
    return x

def main():
    env = dict(os.environ, PYTHONPATH=str(DEP), PYTHONDONTWRITEBYTECODE='1')
    jobs = [
        ('optimized_source', ['-O'], 'verification/source_area_checks.py', [], 'source_normal.txt'),
        ('optimized_classical', ['-O'], 'verification/exact_classical_controls.py', [], 'classical_exact.json'),
        ('normal_guard_false', [], 'verification/run_checks.py', ['--guard-false'], None),
        ('optimized_guard_false', ['-O'], 'verification/run_checks.py', ['--guard-false'], None),
        ('normal_false_mathematical_identity', [], 'audit/root_reproduction_01/DELIBERATELY_FALSE_source_product.py', [], None),
        ('optimized_false_mathematical_identity', ['-O'], 'audit/root_reproduction_01/DELIBERATELY_FALSE_source_product.py', [], None),
    ]
    result = []
    for name, flags, script, args, expected in jobs:
        started = time.monotonic()
        run = subprocess.run([sys.executable, '-B'] + flags + [str(P/script)] + args, env=env, capture_output=True, text=True)
        if expected:
            require(run.returncode == 0, name + ': ' + run.stderr)
            want = (P/'verification/expected'/expected).read_text()
            if expected.endswith('.json'):
                require(clean(json.loads(run.stdout)) == clean(json.loads(want)), name + ': output mismatch')
            else:
                require(run.stdout == want, name + ': output mismatch')
            status = 'PASS: retained expected output agrees'
        else:
            require(run.returncode != 0, name + ': deliberate falsehood passed')
            expected_error = 'DELIBERATE FALSE CONDITION' if 'guard' in name else 'six-period direct product'
            require(expected_error in run.stderr, name + ': failed for wrong reason')
            status = 'PASS: deliberate falsehood rejected for intended reason'
        result.append({'name': name, 'UTC': datetime.now(timezone.utc).isoformat(), 'returncode': run.returncode,
                       'status': status, 'elapsed_seconds': round(time.monotonic()-started, 3),
                       'stdout_sha256': hashlib.sha256(run.stdout.encode()).hexdigest(),
                       'stdout_bytes': len(run.stdout.encode()),
                       'enforcement_error': None if expected else expected_error})
    receipt = {'UTC': datetime.now(timezone.utc).isoformat(), 'python': sys.version,
               'dependencies_used_read_only': str(DEP), 'jobs': result,
               'scope': 'Normal portable runner separately replayed all five exact jobs; only selected optimized jobs and both-mode false controls replayed here. No full historical physical suite repeated.'}
    (HERE/'SELECTED_REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
