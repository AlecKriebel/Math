#!/usr/bin/env python3
"""Supplementary instrumentation; canonical replays are separate and unmodified.

Records each predicate's evaluation count and caught exception type/args.
Only diagnostic fixtures compile inserted probes; frozen files are never edited.
"""
import argparse
import ast
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from explicit_checks import ExplicitAssertions
from replay import PROGRAMS, GENERATED, CONTROLS, replace_once, sha


def worker(program, output, repair):
    counts = {}
    predicates = {}

    class ProbeAssertions(ast.NodeTransformer):
        def visit_Assert(self, node):
            number = len(counts)
            counts[number] = 0
            predicates[number] = {'line': node.lineno,
                                  'predicate': ast.unparse(node.test)}
            node.test = ast.copy_location(ast.Call(
                func=ast.Name(id='__certificate_probe__', ctx=ast.Load()),
                args=[ast.Constant(number), node.test], keywords=[]), node.test)
            return node

    def probe(number, value):
        counts[number] += 1
        return value

    tree = ProbeAssertions().visit(ast.parse(program.read_text()))
    if repair:
        tree = ExplicitAssertions().visit(tree)
    code = compile(ast.fix_missing_locations(tree), str(program), 'exec',
                   optimize=sys.flags.optimize)
    exception = None
    try:
        exec(code, {'__name__': '__main__', '__file__': str(program),
                    '__package__': None, '__certificate_probe__': probe})
    except BaseException as exc:
        exception = {'type': type(exc).__module__ + '.' + type(exc).__qualname__,
                     'args_repr': repr(exc.args)}
    result = {'program': str(program), 'repair': repair,
              'optimization': sys.flags.optimize, 'exception': exception,
              'predicate_evaluations': [dict(number=n, evaluations=c, **predicates[n])
                                        for n, c in counts.items()]}
    output.write_text(json.dumps(result, indent=2) + '\n')
    return 1 if exception else 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=Path)
    parser.add_argument('--worker-program', type=Path)
    parser.add_argument('--worker-output', type=Path)
    parser.add_argument('--repair', action='store_true')
    args = parser.parse_args()
    if args.worker_program:
        sys.exit(worker(args.worker_program, args.worker_output, args.repair))
    case = args.case.resolve()
    public = case / 'reviews' / 'reproduction_adversary'
    private = case / 'private_sources' / 'reproduction_adversary' / 'instrumented'
    source = case / 'source_snapshot' / 'unsolved_math_prioritization' / 'attempts' / '20001515'
    tasks = [(f'baseline_{Path(p).stem}', p, None, repair, optimized)
             for p in PROGRAMS for repair in (False, True) for optimized in (False, True)]
    tasks += [(name, values[0], name, repair, optimized)
              for name, values in CONTROLS.items()
              for repair, optimized in [(False, False), (True, False), (True, True)]]
    records = []
    for label, program, mutation, repair, optimized in tasks:
        fixture = private / f'{label}__{"repair" if repair else "frozen"}__{"optimized" if optimized else "normal"}'
        if fixture.exists():
            shutil.rmtree(fixture)
        shutil.copytree(source, fixture)
        for name in GENERATED:
            (fixture / name).unlink(missing_ok=True)
        if mutation == 'proof_byte':
            p = fixture / 'ATTEMPT_1.md'
            p.write_bytes(p.read_bytes() + b'\n')
        elif mutation:
            target, old, new, _ = CONTROLS[mutation]
            replace_once(fixture / target, old, new)
        report = fixture / 'PROBE_RESULT.json'
        argv = [sys.executable] + (['-O'] if optimized else []) + [
            str(Path(__file__).resolve()), '--worker-program', str(fixture / program),
            '--worker-output', str(report)] + (['--repair'] if repair else [])
        start = time.perf_counter()
        proc = subprocess.run(argv, cwd=fixture, capture_output=True, timeout=60)
        elapsed = time.perf_counter() - start
        result = json.loads(report.read_text())
        (fixture / 'PROBE.stdout').write_bytes(proc.stdout)
        (fixture / 'PROBE.stderr').write_bytes(proc.stderr)
        records.append({'label': label, 'program': program, 'mutation': mutation,
                        'repair': repair, 'optimized': optimized, 'argv': argv,
                        'duration_seconds': elapsed, 'exit_code': proc.returncode,
                        'stdout_sha256': sha(proc.stdout), 'stderr_sha256': sha(proc.stderr),
                        'result_sha256': sha(report.read_bytes()), 'result': result})
    public_result = {'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
                     'diagnostic_only': True,
                     'limitation': 'Predicates are instrumented, so these runs supplement rather than replace exact canonical-source replays.',
                     'runs': records}
    (public / 'EXECUTION_PROBES.json').write_text(json.dumps(public_result, indent=2) + '\n')
    print(json.dumps({'runs': len(records), 'baseline_probe_evaluations': [
        [r['program'], r['repair'], r['optimized'],
         sum(p['evaluations'] for p in r['result']['predicate_evaluations']),
         sum(p['evaluations'] > 0 for p in r['result']['predicate_evaluations'])]
        for r in records if r['mutation'] is None]}, indent=2))


if __name__ == '__main__':
    main()
