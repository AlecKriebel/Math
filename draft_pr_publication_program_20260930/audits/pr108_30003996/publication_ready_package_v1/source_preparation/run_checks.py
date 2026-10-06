#!/usr/bin/env python3
"""Run normal/optimized exact diagnostics and mandatory negative controls.

Standard library only. Default execution writes only a temporary directory,
removed on exit. Optional --output is the only retained receipt write.
--include-historical replays copied historical scripts in temporary copies.
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--include-historical', action='store_true')
    args = parser.parse_args()
    records, reports = [], []

    def execute(argv, cwd, expected_exit, expected_error=None):
        start = datetime.datetime.now(datetime.timezone.utc).isoformat()
        proc = subprocess.Popen(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        record = {'argv':argv, 'actual_PID':proc.pid, 'start_UTC':start,
                  'end_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'actual_exit':proc.returncode, 'expected_exit':expected_exit,
                  'stdout_bytes':len(out), 'stderr_bytes':len(err),
                  'stdout_sha256':hashlib.sha256(out).hexdigest(),
                  'stderr_sha256':hashlib.sha256(err).hexdigest()}
        require(proc.returncode == expected_exit,
                'unexpected subprocess exit: '+json.dumps(record)+' '+err.decode(errors='replace'))
        if expected_error:
            require(expected_error.encode() in err, 'negative control must fail for its intended guard')
            record['expected_guard_present'] = True
        records.append(record)
        return out

    with tempfile.TemporaryDirectory(prefix='pr108_exact_checks_') as tmp:
        scratch = Path(tmp)
        for optimized in (False, True):
            prefix = [sys.executable] + (['-O'] if optimized else [])
            out = execute(prefix+[str(ROOT/'verify_exact.py')], scratch, 0)
            report = json.loads(out)
            require(report['all_pass'], 'positive exact verification must pass')
            reports.append(report)
            for control, guard in (('guard','intentional_false_guard'),
                                   ('cost','unrestricted_structural_identity'),
                                   ('proof','exact_research_note_binding')):
                execute(prefix+[str(ROOT/'verify_exact.py'), '--negative-control',control],
                        scratch, 1, guard)
        comparable = lambda r: {k:v for k,v in r.items()
                                 if k not in ('UTC','actual_operator_PID','python_optimization_level')}
        require(comparable(reports[0]) == comparable(reports[1]),
                'normal and optimized runs must have identical mathematical results')
        historical_reports = []
        if args.include_historical:
            for optimized in (False, True):
                run_dir = scratch/('historical_optimized' if optimized else 'historical_normal')
                shutil.copytree(ROOT/'historical', run_dir)
                prefix = [sys.executable] + (['-O'] if optimized else [])
                for script in ('verify.py','independent_review/independent_checks.py'):
                    out = execute(prefix+[str(run_dir/script)], run_dir, 0)
                    historical_reports.append(json.loads(out))
        result = {'schema':'pr108-portable-check-runner/v1',
                  'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'actual_operator_PID':os.getpid(), 'all_pass':True,
                  'normal_and_optimized_counts_identical':True,
                  'intentional_controls_rejected':6, 'actual_subprocesses':records,
                  'verification_reports':reports, 'historical_scratch_replays':historical_reports,
                  'sealed_package_files_mutated':False,
                  'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'scope':'Finite diagnostics, including six actual failing controls. No all-size or priority inference.'}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'all_pass':True, 'checks_per_valid_run':reports[0]['total_checks'],
                      'intentional_controls_rejected':6,
                      'historical_replays':len(historical_reports)}))


if __name__ == '__main__':
    main()
