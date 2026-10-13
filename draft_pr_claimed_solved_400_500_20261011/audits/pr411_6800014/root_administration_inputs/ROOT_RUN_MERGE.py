#!/usr/bin/env python3
"""Execute exact accepted administration bytes; preserve actual CLI output privately.

This wrapper grants no phase approval. The reviewed helper requires actual
native bindings, a separately approved concrete plan and one durable journal.
"""
import argparse
import base64
import contextlib
import datetime as dt
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import sys

sys.dont_write_bytecode = True
CASE = Path(__file__).resolve().parent.parent
HELPER = CASE / 'merge_preparation/pr411_admin.py'
HELPER_SHA = '1a3963efbab49cf96ea75326cc77b9c3c7455a6c87140a382fc294e739afa131'
ACCEPTANCE_SHA = 'be27b7714db15aae89a9ac81bd017f0148e1d00a10d29a512ce327a33112dc73'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-name', required=True)
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    a = parser.parse_args()
    if not a.run_name.replace('_', '').isalnum():
        raise ValueError('unsafe root run name')
    fd = os.open(HELPER, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as source:
        if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
            raise ValueError('nonregular accepted helper')
        raw = source.read()
    if sha(raw) != HELPER_SHA:
        raise ValueError('accepted source drift')
    spec = importlib.util.spec_from_file_location('root_merge_admin', HELPER)
    m = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(HELPER), 'exec'), m.__dict__)
    acceptance = m.read_local(CASE, 'ROOT_MERGE_FINAL_COMPONENT_ACCEPTANCE.json', ACCEPTANCE_SHA)
    m.need(json.loads(acceptance)['result'] == 'PASS_MERGE_ADMINISTRATION_COMPONENT', 'component acceptance differs')
    arguments = a.arguments[1:] if a.arguments[:1] == ['--'] else a.arguments
    m.need(arguments and arguments[0] in ('plan', 'apply', 'recover', 'reconcile'), 'positive operation required')
    private = CASE / 'private_sources/root_merge_runs' / a.run_name
    private.mkdir(parents=True, exist_ok=False)
    sys.argv = [str(HELPER), *arguments]
    out, err, result, code = io.StringIO(), io.StringIO(), None, 0
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            m.main()
        result = json.loads(out.getvalue())
    except Exception as exc:
        code = 2
        err.write('STOP: ' + (str(exc) if isinstance(exc, m.Stop) else type(exc).__name__) + '\n')
    native = {'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'argv': sys.argv,
              'helper_sha256': HELPER_SHA, 'root_component_acceptance_sha256': ACCEPTANCE_SHA,
              'returncode': code, 'stdout_base64': base64.b64encode(out.getvalue().encode()).decode(),
              'stderr_base64': base64.b64encode(err.getvalue().encode()).decode(),
              'evidence_kind': 'actual_root_in_process_python_CLI_capture', 'no_retry': True}
    for name, obj in [('ROOT_CLI_NATIVE.json', native), ('RESULT.json', result)]:
        if obj is not None:
            fd = os.open(private / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            with os.fdopen(fd, 'wb') as file:
                file.write(json.dumps(obj, sort_keys=True, indent=2).encode() + b'\n'); file.flush(); os.fsync(file.fileno())
    summary = {'returncode': code, 'custody': str(private.relative_to(CASE))}
    if result is not None:
        summary.update({k: result[k] for k in ('result', 'phase', 'canonical_plan_sha256', 'native_write') if k in result})
        if 'plan' in result:
            summary['head'] = result['plan']['expected_head']
            summary['main_anchor'] = result['plan']['main_head']
            summary['integrated_head'] = result['plan']['integrated_head']
            summary['native_observations'] = result['plan'].get('native_observations')
    else:
        summary['safe_error'] = err.getvalue()
    print(json.dumps(summary, sort_keys=True))
    return code

if __name__ == '__main__':
    sys.exit(main())
