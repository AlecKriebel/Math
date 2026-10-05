#!/usr/bin/env python3
"""SOURCE ONLY: ROOT's future real prelaunch administrative builder capture.

This operator may be run by ROOT only after the closed source package has been
read and a new different source adversary has reviewed it. It accepts four real
ROOT prerequisite SHA pins. It never fabricates child completion or erases a
failure. No candidate/family mathematical helper is run by this operator.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import traceback


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def regular(path):
    require(not path.is_symlink() and all(not p.is_symlink() for p in path.parents)
            and stat.S_ISREG(path.stat().st_mode), 'Regular nonsymlink source required')
    return path.read_bytes()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def dump(obj):
    return (json.dumps(obj, indent=2, allow_nan=False) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--expected-builder-sha256', required=True)
    for name in ['root-scope-certificate', 'root-read-ledger', 'root-science-card', 'root-current-input-manifest']:
        parser.add_argument('--' + name + '-sha256', required=True)
    args = parser.parse_args()
    require(args.execute and all(type(value) is str and re.fullmatch('[0-9a-f]{64}', value)
            for key, value in vars(args).items() if key.endswith('sha256')), 'Explicit ROOT execution and SHA pins required')
    require(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0'), 'No optimized checks')
    script = Path(__file__).absolute()
    family, audit = script.parent, script.parent.parent
    repo = audit.parents[2]
    require(family.name == 'current_preparation_family' and audit.name == 'pr43_30004386' and
            repo == Path('/Users/alec/Documents/Math'), 'Exact PR43 ROOT audit anchor required')
    builder = family / 'prepare_current_packet.py'
    source, operator = regular(builder), regular(script)
    require(digest(source) == args.expected_builder_sha256, 'Reviewed builder changed before launch')
    require(not (audit / 'reviewed_candidate').exists() and not (audit / 'reviewed_candidate').is_symlink(),
            'Never launch over an existing candidate')
    (audit / 'tmp').mkdir(exist_ok=True)
    require(not (audit / 'tmp').is_symlink(), 'Regular tmp required')
    capture = audit / 'tmp' / ('root_pr43_current_outer_' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'))
    capture.mkdir(exist_ok=False)
    (capture / 'PRELAUNCH_BUILDER_SOURCE.py').write_bytes(source)
    (capture / 'PRELAUNCH_OPERATOR.py').write_bytes(operator)
    argv = ['/usr/bin/python3', '-B', str(builder), '--execute']
    for name in ['root_scope_certificate', 'root_read_ledger', 'root_science_card', 'root_current_input_manifest']:
        argv.extend(['--' + name.replace('_', '-') + '-sha256', getattr(args, name + '_sha256')])
    prelaunch = {'schema': 'PR43_ROOT_BUILDER_PRELAUNCH_v1', 'operator_pid': os.getpid(),
                 'started_utc': stamp(), 'argv': argv, 'cwd': str(repo),
                 'builder_sha256': digest(source), 'operator_sha256': digest(operator),
                 'administrative_only': True, 'scientific_helpers_run': False}
    (capture / 'OPERATION_PRELAUNCH.json').write_bytes(dump(prelaunch))
    record = dict(prelaunch, schema='PR43_ROOT_ACTUAL_BUILDER_OPERATION_v1',
                  actual_execution=False, completed=False, pid=None, exit_code=None, stdin_supplied=False)
    child = None
    try:
        with (capture / 'stdout.bin').open('xb') as out, (capture / 'stderr.bin').open('xb') as err:
            child = subprocess.Popen(argv, cwd=repo, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                env=dict(os.environ, PR43_ROOT_OUTER_CAPTURE=capture.relative_to(audit).as_posix(),
                         GIT_OPTIONAL_LOCKS='0'))
            record.update(actual_execution=True, pid=child.pid)
            try:
                record['exit_code'] = child.wait(timeout=600)
                record['completed'] = True
            except BaseException:
                child.kill()
                record['exit_code'] = child.wait()
                raise
    except BaseException:
        record['operator_failure'] = traceback.format_exc()
    finally:
        record['finished_utc'] = stamp()
        for channel in ['stdout', 'stderr']:
            path = capture / (channel + '.bin')
            if path.exists():
                raw = regular(path)
                record[channel] = {'path': path.name, 'bytes': len(raw), 'sha256': digest(raw)}
        for key, path, prior in [('builder_unchanged_after_child', builder, source),
                                 ('operator_unchanged_after_child', script, operator)]:
            try:
                record[key] = regular(path) == prior
            except BaseException:
                record[key] = False
                record[key + '_read_failure'] = traceback.format_exc()
        record['new_whole_current_gate'] = 'PENDING'
        record['current_whole_verdict'] = None
        record['capture_requires_ROOT_full_read_before_promotion'] = True
        # Keep each truth value explicit; zero return alone is insufficient.
        ok = (record['actual_execution'] is True and record['completed'] is True and
              type(record['exit_code']) is int and record['exit_code'] == 0 and
              record['builder_unchanged_after_child'] is True and record['operator_unchanged_after_child'] is True and
              'operator_failure' not in record)
        record['status'] = 'ACTUAL_ADMINISTRATIVE_CAPTURE_COMPLETE_WHOLE_REVIEW_PENDING' if ok else 'FAILED_ACTUAL_OPERATION_PRESERVED'
        (capture / 'CAPTURE.json').write_bytes(dump(record))
    print(json.dumps({'status': record['status'], 'audit_relative_capture': capture.relative_to(audit).as_posix(),
                      'pid': record['pid'], 'exit_code': record['exit_code'],
                      'capture_sha256': digest(regular(capture / 'CAPTURE.json')),
                      'new_whole_current_gate': 'PENDING'}, indent=2))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
