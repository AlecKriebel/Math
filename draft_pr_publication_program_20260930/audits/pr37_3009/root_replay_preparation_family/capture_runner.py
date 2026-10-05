#!/usr/bin/env python3
"""Root-owned instrumentation: run an exact private helper, retain every run stream.

This module deliberately has no import-time execution. The collector invokes it
only after root review. Instrumentation does not edit the target source.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys


def main():
    assert sys.flags.optimize == 0
    target, support, *args = sys.argv[1:]
    target, support = Path(target).resolve(), Path(support).resolve()
    support.mkdir(parents=True, exist_ok=False)
    real_run = subprocess.run
    rows = []

    def captured_run(argv, *pos, **kwargs):
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        # check_output otherwise leaves stderr inherited. Capture it without
        # changing the successful bytes returned to its original caller.
        if kwargs.get('stderr') is None and not kwargs.get('capture_output'):
            kwargs['stderr'] = subprocess.PIPE
        failure = None
        try:
            result = real_run(argv, *pos, **kwargs)
        except subprocess.CalledProcessError as error:
            result = subprocess.CompletedProcess(argv, error.returncode, error.stdout, error.stderr)
            failure = error
        index = len(rows)
        row = {'argv': list(map(str, argv)), 'cwd': str(kwargs.get('cwd') or Path.cwd()),
               'started_utc': started, 'exit_code': result.returncode}
        for channel in ['stdout', 'stderr']:
            stream = getattr(result, channel)
            assert stream is not None, 'All helper subprocess streams must be captured'
            data = stream.encode() if isinstance(stream, str) else stream
            file = support / ('%03d.%s' % (index, channel))
            file.write_bytes(data)
            row[channel] = {'path': str(file), 'size': len(data),
                            'sha256': hashlib.sha256(data).hexdigest()}
        rows.append(row)
        (support / 'nested_runs.json').write_text(json.dumps(rows, indent=2)+'\n')
        if failure is not None:
            raise failure
        return result

    subprocess.run = captured_run
    sys.dont_write_bytecode = True
    sys.argv = [str(target), *args]
    try:
        runpy.run_path(str(target), run_name='__main__')
    finally:
        (support / 'nested_runs.json').write_text(json.dumps(rows, indent=2)+'\n')


if __name__ == '__main__':
    main()
