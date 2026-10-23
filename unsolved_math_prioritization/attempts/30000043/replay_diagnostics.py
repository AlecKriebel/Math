#!/usr/bin/env python3
"""Replay the reader's scalar diagnostic in normal, -O and -OO Python.

Each successful run is paired with an active runtime-failure control in an
isolated temporary copy. Original files are never changed. This tests arithmetic
and check enforcement, not the infinite-dimensional mathematical claims.
"""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
DIAGNOSTIC = 'diagnostics/check_stated_constants.py'
MODES = [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]
MARKER = 'EXPECTED_NEGATIVE_CONTROL_REJECTION'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def make_mutant(source):
    tree = ast.parse(source)
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
            'Optimization-removable assertion found')

    class ForceFailure(ast.NodeTransformer):
        changed = False

        def visit_Call(self, node):
            if not self.changed and isinstance(node.func, ast.Name) and node.func.id == 'require':
                self.changed = True
                node.args = [ast.Constant(False), ast.Constant(MARKER)]
                return node
            return self.generic_visit(node)

    mutation = ForceFailure()
    tree = mutation.visit(tree)
    require(mutation.changed, 'No active check was found')
    ast.fix_missing_locations(tree)
    return ast.unparse(tree) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output:
        target = args.output.resolve()
        require(target != ROOT and ROOT not in target.parents,
                'Replay output must be outside the sealed reader')
    original = (ROOT / DIAGNOSTIC).read_bytes()
    mutant = make_mutant(original.decode('utf-8')).encode('utf-8')
    runs = []
    normalized = []
    for mode, flags in MODES:
        with tempfile.TemporaryDirectory(prefix='wavelet_scalar_replay_') as temporary:
            directory = Path(temporary)
            checker = directory / 'check_stated_constants.py'
            checker.write_bytes(original)
            command = [sys.executable, *flags, str(checker)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            require(result.returncode == 0 and not result.stderr.strip(), 'Diagnostic failed: ' + mode)
            report = json.loads(result.stdout)
            require(report['status'] == 'PASS' and all(value is True for value in report['checks'].values()),
                    'Diagnostic reported a failing check')
            require(report['optimization_flag'] == len(flags[0]) - 1 if flags else report['optimization_flag'] == 0,
                    'Unexpected optimization flag')
            normalized.append({key: value for key, value in report.items() if key != 'optimization_flag'})
            checker.write_bytes(mutant)
            negative = subprocess.run(command, capture_output=True, text=True, timeout=30)
            require(negative.returncode != 0 and MARKER in negative.stderr,
                    'Runtime-failure control did not reject: ' + mode)
            runs.append({'mode': mode, 'exit_code': result.returncode, 'stderr_empty': True,
                         'stdout_sha256': digest(result.stdout.encode()), 'report': report,
                         'negative_control': {'kind': 'force first active runtime condition false',
                                              'mutated_source_sha256': digest(mutant),
                                              'exit_code': negative.returncode,
                                              'expected_rejection_observed': True}})
    require(normalized[0] == normalized[1] == normalized[2], 'Optimization changed diagnostic results')
    report = {'status': 'PASS', 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'python_version': platform.python_version(), 'diagnostic': DIAGNOSTIC,
              'bytes': len(original), 'sha256': digest(original), 'assert_nodes': 0,
              'successful_runs': 3, 'active_runtime_failure_controls': 3,
              'normalized_results_identical_across_modes': True,
              'source_originals_modified': False,
              'scope': 'Exact scalar arithmetic and active runtime enforcement only; not a mathematical proof or a new mathematical pass.',
              'runs': runs}
    payload = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
        print(json.dumps({'status': 'PASS', 'successful_runs': 3, 'active_runtime_failure_controls': 3}))
    else:
        print(payload, end='')


if __name__ == '__main__':
    main()
