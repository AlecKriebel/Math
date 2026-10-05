#!/usr/bin/env python3
"""Root-reviewed capture revision: persist intended launches before launching.

No execution at import time. OSError is a launch failure, never a child exit.
Timeout partial streams are bytes. Original failures survive retention errors.
"""
import datetime
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import traceback


def main():
    assert not sys.flags.optimize
    target, destination, *arguments = sys.argv[1:]
    target, destination = Path(target).resolve(), Path(destination).resolve()
    rows, retention_errors = [], []
    real_run = subprocess.run
    digest = lambda data: hashlib.sha256(data).hexdigest()
    original_failure = None
    original_traceback = None
    initial = None
    destination_created = False
    invocation = {'target': str(target), 'argv': [str(target), *arguments], 'cwd': str(Path.cwd()),
                  'helper_invocation_started': False, 'helper_invocation_completed': False}

    def failure(error):
        return {'type': type(error).__name__, 'message': str(error), 'traceback': ''.join(traceback.format_exception(type(error), error, error.__traceback__)),
                'errno': getattr(error, 'errno', None), 'filename': str(error.filename) if getattr(error, 'filename', None) else None}

    def data_bytes(value):
        if value is None: return b''
        if isinstance(value, str): return value.encode()
        return bytes(value)

    def write_json(path, value):
        artifact(path, (json.dumps(value, indent=2)+'\n').encode())

    def save():
        write_json(destination/'nested_runs.json', rows)

    def artifact(path, data):
        try:
            path.write_bytes(data)
            actual = path
        except OSError as error:
            retention_errors.append({'stage': 'primary_capture_artifact', 'path': str(path), **failure(error)})
            # The orchestrator supplies only private targets. A failed support
            # write may preserve bytes there, never in a live closed family.
            audit_tmp = Path(__file__).resolve().parent.parent/'tmp'
            assert target.is_relative_to(audit_tmp), 'Private-only retention fallback'
            actual = target.parent/'root_capture_retention_fallback'/destination.name/path.relative_to(destination)
            actual.parent.mkdir(parents=True, exist_ok=True)
            actual.write_bytes(data)
        return {'path': str(actual), 'size': len(data), 'sha256': digest(data)}

    def inventory(root):
        result = {}
        for path in sorted(root.rglob('*')):
            relative = path.relative_to(root)
            if {'tmp', 'ignoredtmp', '__pycache__'}.intersection(relative.parts) or path.is_symlink():
                continue
            if path.is_file(): result[relative.as_posix()] = path.read_bytes()
        return result

    def retain_delta(before, after, label):
        result = {'removed': sorted(set(before)-set(after)), 'created_or_changed': []}
        for name, data in after.items():
            if before.get(name) == data: continue
            path = destination/label/name
            path.parent.mkdir(parents=True, exist_ok=True)
            result['created_or_changed'].append({**artifact(path, data), 'original_relative_path': name})
        return result

    def captured_run(argv, *positional, **keywords):
        assert isinstance(argv, (list, tuple)) and not keywords.get('shell')
        index = len(rows)
        row = {'argv': list(map(str, argv)), 'cwd': str(keywords.get('cwd') or Path.cwd()),
               'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'launch_attempted': False, 'actual_execution': False, 'completed': False,
               'exit_code': None, 'failure_type': None, 'error': None}
        rows.append(row)
        child_failure, child_traceback, result, before, script, popen_called = None, None, None, None, None, False
        partial_available = None
        inherit_stdout = not keywords.get('capture_output') and keywords.get('stdout') is None
        inherit_stderr = not keywords.get('capture_output') and keywords.get('stderr') is None
        try:
            # Every available intended input and source precedes Popen. A
            # prelaunch-retention failure prevents launch and remains explicit.
            if Path(str(argv[0])).name.startswith('python'):
                script = next((Path(str(x)).resolve() for x in argv[1:] if str(x).endswith('.py')), None)
            if script:
                row['script_path'] = str(script)
                row['source_available'] = script.is_file() and not script.is_symlink()
                if row['source_available']:
                    source = script.read_bytes()
                    source_copy = destination/('%03d_prelaunch_source.py' % index)
                    retained_source = artifact(source_copy, source)
                    row['script'] = {'path': str(script), 'size': len(source), 'sha256': digest(source),
                                     'retained_full_source': retained_source['path']}
                    before = inventory(script.parent)
            if keywords.get('input') is not None:
                row['stdin'] = artifact(destination/('%03d.stdin' % index), data_bytes(keywords['input']))
            for channel in ['stdout', 'stderr']:
                row[channel] = artifact(destination/('%03d.%s' % (index, channel)), b'')
            row['stdio_capture'] = {'kind': 'prelaunch_empty_placeholder', 'stdout_available': False, 'stderr_available': False}
            save()
            assert not retention_errors, 'Prelaunch retention failed; do not launch'
            if inherit_stdout: keywords['stdout'] = subprocess.PIPE
            if inherit_stderr: keywords['stderr'] = subprocess.PIPE
            assert keywords.get('stderr') != subprocess.STDOUT, 'Separate streams required'
            row['launch_attempted'] = True
            save()
            assert not retention_errors, 'Prelaunch ledger retention failed; do not launch'
            try:
                popen_called = True
                result = real_run(argv, *positional, **keywords)
                row.update(actual_execution=True, completed=True, exit_code=result.returncode)
            except subprocess.CalledProcessError as error:
                result = subprocess.CompletedProcess(argv, error.returncode, error.stdout, error.stderr)
                row.update(actual_execution=True, completed=True, exit_code=error.returncode)
                child_failure, child_traceback = error, error.__traceback__
            except subprocess.TimeoutExpired as error:
                partial_available = {channel: getattr(error, channel) is not None for channel in ['stdout', 'stderr']}
                result = subprocess.CompletedProcess(argv, None, data_bytes(error.stdout), data_bytes(error.stderr))
                row.update(actual_execution=True, completed=False, exit_code=None)
                child_failure, child_traceback = error, error.__traceback__
            except OSError as error:
                # No CompletedProcess and no fake child exit for an OS launch failure.
                row.update(actual_execution=False, completed=False, exit_code=None)
                child_failure, child_traceback = error, error.__traceback__
            if child_failure:
                row['failure_type'] = type(child_failure).__name__
                row['error'] = failure(child_failure)
            if result is not None:
                row['stdio_capture'] = {'kind': 'partial_timeout' if isinstance(child_failure, subprocess.TimeoutExpired) else 'complete_child_streams',
                                        'stdout_available': partial_available['stdout'] if partial_available else result.stdout is not None,
                                        'stderr_available': partial_available['stderr'] if partial_available else result.stderr is not None}
                for channel in ['stdout', 'stderr']:
                    value = getattr(result, channel)
                    data = data_bytes(value)
                    row[channel] = artifact(destination/('%03d.%s' % (index, channel)), data)
                    if (channel == 'stdout' and inherit_stdout) or (channel == 'stderr' and inherit_stderr):
                        getattr(sys, channel).buffer.write(data)
            else:
                row['stdio_capture'] = {'kind': 'no_child_launched', 'stdout_available': False, 'stderr_available': False}
            save()
        except BaseException as error:
            if not popen_called:
                row['launch_attempted'] = False
                row['failure_stage'] = 'prelaunch_retention'
            if child_failure is None:
                child_failure, child_traceback = error, error.__traceback__
                row['failure_type'], row['error'] = type(error).__name__, failure(error)
            else:
                retention_errors.append({'stage': 'nested_stream_or_ledger_retention', 'index': index, **failure(error)})
        finally:
            try:
                if before is not None:
                    row['generated_files'] = retain_delta(before, inventory(script.parent), '%03d_generated' % index)
                row['ended_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                save()
            except BaseException as error:
                retention_errors.append({'stage': 'nested_final_retention', 'index': index, **failure(error)})
        if child_failure: raise child_failure.with_traceback(child_traceback)
        if retention_errors: raise RuntimeError('Capture retention failed; original outcome and available evidence preserved')
        return result

    try:
        destination.mkdir(parents=True, exist_ok=False)
        destination_created = True
        assert target.is_file() and not target.is_symlink()
        source = target.read_bytes()
        invocation['source'] = artifact(destination/'outer_prelaunch_source.py', source)
        write_json(destination/'outer_helper_attempt.json', invocation)
        save()
        initial = inventory(target.parent)
        assert not retention_errors, 'Outer prelaunch retention failed; do not invoke helper'
        subprocess.run = captured_run
        sys.dont_write_bytecode = True
        sys.argv = [str(target), *arguments]
        invocation['helper_invocation_prepared'] = True
        write_json(destination/'outer_helper_attempt.json', invocation)
        assert not retention_errors, 'Outer invocation ledger retention failed; do not invoke helper'
        invocation['helper_invocation_started'] = True
        runpy.run_path(str(target), run_name='__main__')
        invocation['helper_invocation_completed'] = True
    except BaseException as error:
        original_failure, original_traceback = error, error.__traceback__
        invocation['original_failure'] = failure(error)
    finally:
        if not destination_created:
            # A setup failure must not overwrite a preexisting destination.
            print(json.dumps({'original_failure': invocation.get('original_failure'), 'retention_errors': retention_errors,
                              'destination_created': False}), file=sys.stderr)
            if original_failure: raise original_failure.with_traceback(original_traceback)
        for stage, action in [
            ('nested_ledger_final', save),
            ('outer_attempt_final', lambda: write_json(destination/'outer_helper_attempt.json', invocation)),
            ('outer_generated_final', lambda: write_json(destination/'outer_generated_files.json',
                retain_delta(initial, inventory(target.parent), 'outer_generated') if initial is not None else {'not_run': 'Initial inventory unavailable'}))]:
            try: action()
            except BaseException as error: retention_errors.append({'stage': stage, **failure(error)})
        try:
            write_json(destination/'CAPTURE_STATUS.json', {'status': 'FAIL' if original_failure or retention_errors else 'PASS',
                'original_failure': invocation.get('original_failure'), 'retention_errors': retention_errors,
                'helper_invocation': invocation, 'nested_attempt_count': len(rows)})
        except BaseException as error:
            retention_errors.append({'stage': 'capture_status_final', **failure(error)})
            print(json.dumps({'original_failure': invocation.get('original_failure'), 'retention_errors': retention_errors}), file=sys.stderr)
    if original_failure: raise original_failure.with_traceback(original_traceback)
    if retention_errors: raise RuntimeError('Capture finalization failed; available evidence and original outcome remain retained')


if __name__ == '__main__':
    main()
