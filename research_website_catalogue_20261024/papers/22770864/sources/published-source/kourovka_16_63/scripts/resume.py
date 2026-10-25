#!/usr/bin/env python3
"""Reproduce the independent exact verification, with no network access.
Default: Python standard library plus GCC/Clang C++17 with __int128.
--full additionally regenerates Python data using NumPy and SymPy.
Does not install dependencies or execute any remote service.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true', help='Regenerate all Python coefficients and Smith data first')
    parser.add_argument('--compiler', help='C++ compiler name or executable path')
    args = parser.parse_args()
    build, logs = ROOT / 'build', ROOT / 'logs'
    build.mkdir(exist_ok=True)
    logs.mkdir(exist_ok=True)
    names = [args.compiler] if args.compiler else ['c++', 'g++', 'clang++']
    compiler = next((shutil.which(name) for name in names if name and shutil.which(name)), None)
    if compiler is None:
        raise RuntimeError('A local GCC or Clang C++17 compiler supporting __int128 is required. Use --compiler /path/to/compiler to select one. No compiler was installed by this script.')
    log_path = logs / 'resume_verify.log'
    commands: list[list[str]] = []
    with log_path.open('w') as logfile:
        def run(command: list[str]) -> str:
            commands.append(command)
            header = '$ ' + ' '.join(command) + '\n'
            print(header, end='', flush=True)
            logfile.write(header)
            logfile.flush()
            process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            output = process.stdout + process.stderr
            print(output, end='', flush=True)
            logfile.write(output)
            logfile.flush()
            if process.returncode:
                raise RuntimeError(f'Command failed with exit code {process.returncode}; see {log_path}')
            return output

        compiler_version = run([compiler, '--version']).splitlines()[0]
        if args.full:
            # Verify availability; never install or fetch a dependency.
            run([sys.executable, '-c', 'import numpy, sympy; print("numpy", numpy.__version__, "sympy", sympy.__version__)'])
            for script, options in [
                ('lie31.py', []),
                ('exact_linear.py', []),
                ('smith_local.py', ['--precision', '12']),
                ('smith_local.py', ['--verify-plan', '--precision', '6']),
                ('export_presentation.py', [])
            ]:
                run([sys.executable, 'scripts/' + script] + options)
        control_output = run([sys.executable, 'scripts/sanity_groups.py'])
        (logs / 'resume_sanity_groups.json').write_text(control_output)
        executable = build / 'independent_verify'
        if executable.exists():
            executable.unlink()  # A failed build must never leave a stale runnable verifier.
        flags = ['-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror']
        run([compiler] + flags + ['-o', str(executable), 'scripts/independent_verify.cpp'])
        output = run([str(executable), 'data/smith_pivot_plan.txt'])
        required = [
            'original_integer_jacobi_checks=4495',
            'adapted_integer_jacobi_checks=4495',
            'unscaled_derivation_rank_mod_p=931 derivation_dimension=30',
            'smith_valuation=0 multiplicity=87',
            'smith_valuation=1 multiplicity=55',
            'smith_valuation=2 multiplicity=758',
            'smith_valuation=3 multiplicity=6',
            'smith_valuation=4 multiplicity=25',
            'sum_smith_valuations=1689',
            'candidate_group_order_exponent=52359',
            'predicted_aut_order_exponent=52359',
            'ALL_CHECKS_PASSED'
        ]
        for fragment in required:
            if fragment not in output:
                raise RuntimeError(f'Missing expected verification output: {fragment}')
        (logs / 'resume_cpp_verify.log').write_text(output)

        lines = (ROOT / 'data/smith_pivot_plan.txt').read_text().splitlines()
        first = lines[1].split()
        if first[2] != '0':
            raise RuntimeError('Unexpected first pivot valuation')
        first[2] = '5'
        lines[1] = ' '.join(first)
        with tempfile.TemporaryDirectory(prefix='negative_certificate_', dir=build) as temporary:
            bad = Path(temporary) / 'bad_plan.txt'
            bad.write_text('\n'.join(lines) + '\n')
            process = subprocess.run([str(executable), str(bad)], cwd=ROOT, capture_output=True, text=True)
            rejected = process.returncode != 0 and 'pivot valuation mismatch' in process.stderr
            negative = {'changed_record': 0, 'original_valuation': 0, 'corrupted_valuation': 5,
                        'exit_code': process.returncode, 'stderr': process.stderr.strip(),
                        'corrupted_certificate_rejected': rejected}
            (logs / 'resume_negative_test.json').write_text(json.dumps(negative, indent=2) + '\n')
            logfile.write(json.dumps(negative, indent=2) + '\n')
            print(json.dumps(negative, indent=2), flush=True)
            if not rejected:
                raise RuntimeError('The corrupted-certificate test did not reject as expected')
    record = {
        'completed_at_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'ALL_CHECKS_PASSED',
        'full_python_regeneration': args.full,
        'python': sys.version,
        'platform': platform.platform(),
        'compiler': compiler_version,
        'compiler_flags': flags,
        'input_sha256': {str(path.relative_to(ROOT)): sha256(path) for path in
                         [ROOT / 'scripts/independent_verify.cpp', ROOT / 'data/smith_pivot_plan.txt']},
        'commands': commands,
        'network_access': False,
        'randomized_mathematical_steps': False,
        'external_peer_review_claimed': False,
        'group_order_exponent': 52359,
        'full_automorphism_order_exponent': 52359,
        'proof_dependency': 'The report proves the full-stabilizer, lifting, logarithm/exponential, and Lazard steps. This command independently verifies their exact finite linear-algebra inputs.'
    }
    (logs / 'resume_run.json').write_text(json.dumps(record, indent=2) + '\n')
    print('\nREPRODUCTION_PASSED: exact certificate checks and corrupted-certificate rejection.')
    print('The mathematical proof is in report/kourovka_16_63.pdf.')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError) as exc:
        print(f'REPRODUCTION_FAILED: {exc}', file=sys.stderr)
        raise SystemExit(1)
