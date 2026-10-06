#!/usr/bin/env python3
"""Stage unchanged PR97 diagnostic sources and record actual subprocess runs."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
sys.dont_write_bytecode = True
from safe_output import fresh_output, copy_new, write_new, Journal

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    package = source.parent
    output = fresh_output(args.output_dir, package)
    journal = []
    custody = Journal(output/'PROCESS_RECEIPTS.json')
    for family, script in [('author', source/'verify.py'),
                           ('independent', source/'review/independent_checks.py')]:
        for mode in ('normal', 'optimized', 'false_check_optimized'):
            case = family + '_' + mode
            with tempfile.TemporaryDirectory(prefix=case+'_', dir=output) as temp:
                stage = Path(temp)
                code = stage/script.name
                copy_new(script, code)
                candidate = source/'CANDIDATE.md'
                if family == 'author':
                    copy_new(candidate, stage/'CANDIDATE.md')
                else:
                    (stage/'author_replay').mkdir()
                    copy_new(candidate, stage/'author_replay/CANDIDATE.md')
                command = [sys.executable, '-E', '-B']
                if mode != 'normal':
                    command.append('-O')
                if mode == 'false_check_optimized':
                    command += ['-c',
                        'import runpy,sys; s=runpy.run_path(sys.argv[1]); '
                        's["ck"]("deliberately_false_package_control", False)', str(code)]
                else:
                    command.append(str(code))
                started = dt.datetime.now(dt.timezone.utc).isoformat()
                tick = time.monotonic()
                proc = subprocess.Popen(command, cwd=stage,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
                write_new(output/(case+'.stdout.json'), stdout)
                write_new(output/(case+'.stderr.txt'), stderr)
                expected = 1 if mode == 'false_check_optimized' else 0
                record = dict(family=family, mode=mode, command=command,
                              cwd=str(stage), pid=proc.pid, started_utc=started,
                              finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                              wall_seconds=time.monotonic()-tick, exit_code=proc.returncode,
                              expected_exit_code=expected, accepted=None,
                              input_script_sha256=sha(script), candidate_sha256=sha(candidate),
                              stdout_sha256=hashlib.sha256(stdout).hexdigest(),
                              stderr_sha256=hashlib.sha256(stderr).hexdigest())
                journal.append(record)
                # Persist raw custody before parsing or rejecting any child output.
                custody.save(journal)
                if mode == 'false_check_optimized':
                    accepted = (proc.returncode == expected and
                                b'AssertionError: deliberately_false_package_control' in stderr)
                    if not accepted:
                        record['rejection_reason'] = 'False-check control was not rejected as expected'
                elif proc.returncode != expected:
                    accepted = False
                    record['rejection_reason'] = 'Unexpected child exit code'
                else:
                    try:
                        parsed = json.loads(stdout)
                        accepted = isinstance(parsed, dict) and parsed.get('status') == 'PASS'
                        if not accepted:
                            record['rejection_reason'] = 'Child output lacks a PASS object'
                        else:
                            record['diagnostic_assertions'] = parsed.get('assertions')
                            record['sympy_version'] = parsed.get('sympy_version')
                    except (ValueError, TypeError) as error:
                        accepted = False
                        record['parse_error'] = type(error).__name__ + ': ' + str(error)
                        record['rejection_reason'] = 'Malformed child output'
                record['accepted'] = accepted
                custody.save(journal)
                if not accepted:
                    raise RuntimeError('Diagnostic run failed: '+case)
    print(json.dumps(dict(status='PASS', runs=len(journal),
                         python_version=sys.version,
                         new_central_proof_search_turns=0,
                         publication_authorized=False,
                         scope='Finite local algebra/margin diagnostics and active false-check guards; '
                               'not ET/Gray proofs or a priority certificate.'), indent=2))

if __name__ == '__main__':
    main()
