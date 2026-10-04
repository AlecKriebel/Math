#!/usr/bin/env python3
"""Root-reviewed instrumentation; no execution at import time.

Execute an unchanged private helper with runpy, capture every subprocess.run
(including check_output), and retain complete streams and first-party file
deltas. This is instrumentation, not a reconstruction of historical runs.
"""
import datetime
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys


def main():
    assert not sys.flags.optimize
    target, destination, *arguments = sys.argv[1:]
    target, destination = Path(target).resolve(), Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=False)
    rows = []
    real_run = subprocess.run
    digest = lambda data: hashlib.sha256(data).hexdigest()

    def save():
        (destination/'nested_runs.json').write_text(json.dumps(rows, indent=2)+'\n')

    def inventory(root):
        # Helpers write only first-party artifacts here. Foreign/cache material
        # is never copied. A script inside ignoredtmp is an actual first-party
        # original/mutant case; its own directory is retained independently.
        result = {}
        for path in sorted(root.rglob('*')):
            relative = path.relative_to(root)
            if {'tmp', 'ignoredtmp', '__pycache__'}.intersection(relative.parts):
                continue
            if path.is_symlink():
                # An actual negative-control input may be a symlink. Its
                # definition is separately retained; never follow or copy it.
                continue
            if path.is_file():
                result[relative.as_posix()] = path.read_bytes()
        return result

    def retain_delta(before, after, label):
        result = {'removed': sorted(set(before)-set(after)), 'created_or_changed': []}
        for name, data in after.items():
            if before.get(name) == data:
                continue
            path = destination/label/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            result['created_or_changed'].append({'path': str(path), 'original_relative_path': name,
                                                'size': len(data), 'sha256': digest(data)})
        return result

    def captured_run(argv, *positional, **keywords):
        assert isinstance(argv, (list, tuple)) and not keywords.get('shell')
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        # Preserve inherited-output behavior while retaining full bytes.
        inherit_stdout = not keywords.get('capture_output') and keywords.get('stdout') is None
        inherit_stderr = not keywords.get('capture_output') and keywords.get('stderr') is None
        if inherit_stdout:
            keywords['stdout'] = subprocess.PIPE
        if inherit_stderr:
            keywords['stderr'] = subprocess.PIPE
        assert keywords.get('stderr') != subprocess.STDOUT, 'Separate streams required'
        script = next((Path(str(x)).resolve() for x in argv[1:]
                       if str(x).endswith('.py') and Path(str(x)).is_file()), None)
        before = inventory(script.parent) if script else {}
        failure = None
        try:
            result = real_run(argv, *positional, **keywords)
        except subprocess.CalledProcessError as error:
            result = subprocess.CompletedProcess(argv, error.returncode, error.stdout, error.stderr)
            failure = error
        except subprocess.TimeoutExpired as error:
            result = subprocess.CompletedProcess(argv, None, error.stdout or b'', error.stderr or b'')
            failure = error
        index = len(rows)
        row = {'argv': list(map(str, argv)), 'cwd': str(keywords.get('cwd') or Path.cwd()),
               'started_utc': started, 'exit_code': result.returncode,
               'failure_type': type(failure).__name__ if failure else None}
        if keywords.get('input') is not None:
            content = keywords['input']
            data = content.encode() if isinstance(content, str) else content
            path = destination/('%03d.stdin' % index)
            path.write_bytes(data)
            row['stdin'] = {'path': str(path), 'size': len(data), 'sha256': digest(data)}
        for channel in ['stdout', 'stderr']:
            stream = getattr(result, channel)
            assert stream is not None, 'Every stream must be available'
            data = stream.encode() if isinstance(stream, str) else stream
            path = destination/('%03d.%s' % (index, channel))
            path.write_bytes(data)
            row[channel] = {'path': str(path), 'size': len(data), 'sha256': digest(data)}
            if (channel == 'stdout' and inherit_stdout) or (channel == 'stderr' and inherit_stderr):
                getattr(sys, channel).write(stream if isinstance(stream, str) else stream.decode())
        if script:
            source_copy = destination/('%03d_executed_source.py' % index)
            source_copy.write_bytes(script.read_bytes())
            row['script'] = {'path': str(script), 'size': script.stat().st_size,
                             'sha256': digest(script.read_bytes()), 'retained_full_source': str(source_copy)}
            row['generated_files'] = retain_delta(before, inventory(script.parent), '%03d_generated' % index)
        rows.append(row)
        save()
        if failure:
            raise failure
        return result

    initial = inventory(target.parent)
    subprocess.run = captured_run
    sys.dont_write_bytecode = True
    sys.argv = [str(target), *arguments]
    try:
        runpy.run_path(str(target), run_name='__main__')
    finally:
        save()
        delta = retain_delta(initial, inventory(target.parent), 'outer_generated')
        (destination/'outer_generated_files.json').write_text(json.dumps(delta, indent=2)+'\n')


if __name__ == '__main__':
    main()
