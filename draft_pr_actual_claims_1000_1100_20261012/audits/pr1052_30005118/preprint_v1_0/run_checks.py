#!/usr/bin/env python3
"""Run exact authored historical checkers in isolation plus new checks."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', default='_runs/fresh.json')
    args = ap.parse_args()
    out = ROOT / args.output
    out.resolve().relative_to(ROOT)
    out.parent.mkdir(parents=True, exist_ok=True)
    results = {'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'python': sys.version, 'scope': 'Fresh runs of copied authored checkers; no omitted historical executable replay, no finite-check proof of universal theorem.', 'runs': []}
    history = ROOT/'support/history/reviews'
    with tempfile.TemporaryDirectory(prefix='checks-', dir=out.parent) as temp:
        work = Path(temp)
        for family, source, optimized in [('cyclic_transfer_01', history/'cyclic_transfer_01/sources/fresh_checks.py', False), ('cyclic_transfer_01', history/'cyclic_transfer_01/sources/fresh_checks.py', True), ('primary_encoding_01', history/'primary_encoding_01/independent_checks.py', False), ('new_claim', ROOT/'verification/check_claim.py', False), ('new_claim', ROOT/'verification/check_claim.py', True)]:
            # Retain the cyclic checker's relative layout, without changing frozen outputs.
            dest = work/family/'sources'/source.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
            argv = [sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [str(dest)]
            started = time.monotonic()
            proc = subprocess.run(argv, cwd=work, capture_output=True, timeout=600)
            require(proc.returncode == 0 and not proc.stderr, family+' execution failure: '+proc.stderr.decode(errors='replace'))
            if family == 'cyclic_transfer_01':
                name = 'FRESH_CHECKS_OPTIMIZED.json' if optimized else 'FRESH_CHECKS.json'
                actual = json.loads((dest.parent.parent/name).read_text())
                expected = json.loads((history/family/name).read_text())
                for key in ['started_utc', 'completed_utc']:
                    actual.pop(key, None); expected.pop(key, None)
                require(actual == expected, 'cyclic historical substantive results changed')
            else:
                actual = json.loads(proc.stdout)
                if family == 'primary_encoding_01':
                    require(actual == json.loads((history/family/'INDEPENDENT_CHECKS.json').read_text()), 'primary historical results changed')
            results['runs'].append({'family': family, 'optimization': int(optimized), 'source_sha256': digest(source), 'exit_code': proc.returncode, 'stderr_bytes': len(proc.stderr), 'stdout_sha256': hashlib.sha256(proc.stdout).hexdigest(), 'elapsed_seconds': round(time.monotonic()-started, 3), 'results': actual})
    require(results['runs'][-1]['results'] == results['runs'][-2]['results'], 'new checks differ under optimization')
    results['completed_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    results['all_checks_passed'] = True
    out.write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps({'all_checks_passed': True, 'runs': len(results['runs']), 'output': str(out.relative_to(ROOT))}))

if __name__ == '__main__':
    main()
