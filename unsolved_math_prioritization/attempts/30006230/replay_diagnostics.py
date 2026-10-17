#!/usr/bin/env python3
"""Replay the unchanged accepted diagnostics and active-failure controls.

This is an integrity/reproducibility tool, not a new mathematical proof or audit.
Runs every accepted checker in normal, -O, and -OO modes, in isolated temporary
copies. Nothing in the sealed reader package is modified. Numerical checks are
finite diagnostics only. The mathematical conclusions rest on the manuscripts.
"""
import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    'pass1_hardy/check_hardy_identities.py',
    'pass1_hardy/check_nonnegative_rellich_identities.py',
    'pass1_hardy/check_independent_function_identities.py',
    'pass1_rellich/check_rellich_counterexample.py',
    'pass1_rellich/historical_q3/check_historical_q3.py',
    'pass1_audit/check_audit.py',
    'pass1_spectral_audit/check_spectral_algebra.py',
    'pass1_spectral_audit/check_historical_q3_algebra.py',
]
MODES = [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]
MARKER = 'EXPECTED_NEGATIVE_CONTROL_REJECTION'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def normalize(report):
    return {key: value for key, value in report.items()
            if key not in {'checked_at_utc', 'optimization_flag'}}


def negative_control(source, relative):
    """Alter only the check-enforcement input in an isolated copy."""
    tree = ast.parse(source)
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
            f'Optimization-removable assert found: {relative}')
    if relative.startswith('pass1_hardy/'):
        found = False
        for index, node in enumerate(tree.body):
            if isinstance(node, ast.Raise):
                assignment = ast.parse('report["all_checks_pass"] = False').body[0]
                tree.body.insert(index, assignment)
                found = True
                break
        require(found, f'Missing terminal failure enforcement: {relative}')
        kind = 'force final all_checks_pass false before SystemExit'
    else:
        class ForceFailure(ast.NodeTransformer):
            changed = False
            def visit_Call(self, node):
                if (not self.changed and isinstance(node.func, ast.Name)
                        and node.func.id == 'require'):
                    self.changed = True
                    condition_index = 1 if relative == 'pass1_audit/check_audit.py' else 0
                    label_index = 1 - condition_index
                    node.args[condition_index] = ast.Constant(False)
                    node.args[label_index] = ast.Constant(MARKER)
                    return node
                return self.generic_visit(node)
        transform = ForceFailure()
        tree = transform.visit(tree)
        require(transform.changed, f'No runtime require call: {relative}')
        kind = 'force first runtime require condition false with known rejection marker'
    ast.fix_missing_locations(tree)
    return ast.unparse(tree) + '\n', kind


def run_one(relative):
    original = ROOT / 'accepted' / relative
    source = original.read_text()
    mutant, mutation = negative_control(source, relative)
    original_bytes = original.read_bytes()
    modes = []
    normalized = []
    for mode, flags in MODES:
        with tempfile.TemporaryDirectory(prefix='grushin_replay_') as directory:
            temporary = Path(directory)
            checker = temporary / original.name
            shutil.copyfile(original, checker)
            require(checker.read_bytes() == original_bytes, 'Copy changed original checker')
            command = [sys.executable, *flags, str(checker)]
            run = subprocess.run(command, cwd=temporary, capture_output=True, text=True, timeout=180)
            require(run.returncode == 0, f'Checker failed: {relative}, {mode}: {run.stderr}')
            require(not run.stderr.strip(), f'Unexpected checker stderr: {relative}, {mode}')
            report = json.loads(run.stdout)
            if 'all_checks_pass' in report:
                require(report['all_checks_pass'] is True, 'False success flag')
            if 'status' in report:
                require(report['status'] == 'PASS', 'Non-PASS status')
            checks = report.get('checks', {})
            if isinstance(checks, dict):
                require(all(value is True for value in checks.values()), 'Failed declared check')
            elif isinstance(checks, list):
                require(all(value.get('passed') is True for value in checks), 'Failed check record')
            mutants = report.get('deliberately_incorrect_formula_rejections', {})
            require(all(value is True for value in mutants.values()), 'Formula rejection failed')
            if 'optimization_flag' in report:
                require(report['optimization_flag'] == len(flags[0]) - 1 if flags else report['optimization_flag'] == 0,
                        'Reported optimization flag differs from invocation')
            normalized.append(normalize(report))
            probe = temporary / ('negative_control_' + original.name)
            probe.write_text(mutant)
            failure = subprocess.run([sys.executable, *flags, str(probe)], cwd=temporary,
                                     capture_output=True, text=True, timeout=180)
            if relative.startswith('pass1_hardy/'):
                require(failure.returncode == 1, 'Expected final-flag rejection did not occur')
                require(json.loads(failure.stdout)['all_checks_pass'] is True,
                        'Negative control unexpectedly altered the formula checks')
                require(not failure.stderr.strip(), 'Unexpected negative-control error')
                # The final flag is changed after the original report is printed.
            else:
                require(failure.returncode != 0 and MARKER in failure.stderr,
                        'Expected runtime require rejection did not occur')
            modes.append({
                'mode': mode, 'python_flags': flags, 'exit_code': run.returncode,
                'stdout_sha256': digest(run.stdout.encode()),
                'stderr_empty': not bool(run.stderr.strip()), 'report': report,
                'negative_control': {'mutation': mutation, 'mutated_source_sha256': digest(mutant.encode()),
                                     'expected_failure_observed': True, 'exit_code': failure.returncode},
            })
    require(all(item == normalized[0] for item in normalized), f'Mode results differ: {relative}')
    return {'reader_path': 'accepted/' + relative, 'bytes': len(original_bytes),
            'sha256': digest(original_bytes), 'assert_nodes': 0,
            'normalized_results_identical_across_modes': True, 'runs': modes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional JSON path outside the sealed reader directory')
    args = parser.parse_args()
    if args.output:
        target = args.output.resolve()
        require(target != ROOT and ROOT not in target.parents, 'Output must be outside the sealed reader directory')
    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(run_one, SCRIPTS))
    report = {
        'status': 'PASS', 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(), 'checker_count': len(SCRIPTS),
        'successful_checker_runs': len(SCRIPTS) * len(MODES),
        'successful_active_failure_controls': len(SCRIPTS) * len(MODES),
        'source_originals_modified': False,
        'normalization_ignores_only': ['checked_at_utc', 'optimization_flag'],
        'scope': 'Reproduction and active runtime enforcement only; no new mathematical proof or pass.',
        'limitations': [
            'No checker certifies the universal analytical conclusions.',
            'Finite numerical eigenvalues never define the exact variational parameters.',
            'An active failure control verifies a checker enforcement path, not every conceivable software fault.',
        ],
        'checkers': records,
    }
    payload = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
        print(json.dumps({'status': 'PASS', 'checker_runs': 24, 'active_failure_controls': 24}))
    else:
        print(payload, end='')


if __name__ == '__main__':
    main()
