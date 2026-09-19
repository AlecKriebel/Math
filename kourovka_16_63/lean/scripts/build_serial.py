#!/usr/bin/env python3
"""Compile the selected project import closure serially, always from project source.

Pinned upstream dependency objects must already be available. They are not
rebuilt here. Use check.py for dependency-pin and axiom auditing; this helper
only compiles project source. All selected project objects are invalidated before compilation;
no failed or skipped module retains a stale object. This does not prove the
missing final group theorem.
"""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

from audit_support import AuditError, inventory, closure

ROOT = Path(__file__).resolve().parents[1]


def run_process(command, *, cwd, timeout, stdout=subprocess.PIPE):
    """Return (exit, text, timed_out); terminate the whole child group on failure.

    A new POSIX session includes Lake and the Lean process it spawns. Killing
    only the immediate Lake process can otherwise leave a compiler running.
    """
    if timeout <= 0:
        raise ValueError('timeout must be positive')
    proc = subprocess.Popen(command, cwd=cwd, stdout=stdout,
                            stderr=subprocess.STDOUT, text=True,
                            start_new_session=True)

    def kill_group(sig):
        try:
            os.killpg(proc.pid, sig)
        except ProcessLookupError:
            pass

    try:
        output, _ = proc.communicate(timeout=timeout)
        return proc.returncode, output or '', False
    except subprocess.TimeoutExpired:
        kill_group(signal.SIGTERM)
        try:
            output, _ = proc.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            kill_group(signal.SIGKILL)
            output, _ = proc.communicate()
        finally:
            # A child may ignore TERM even if the immediate parent has exited.
            kill_group(signal.SIGKILL)
        return proc.returncode or -signal.SIGKILL, output or '', True
    except BaseException:
        kill_group(signal.SIGKILL)
        proc.communicate()
        raise


def build(root: Path, module: str, timeout: int, *, execute=run_process):
    """Build exactly the selected local closure and preserve per-module evidence."""
    if timeout <= 0:
        raise AuditError('timeout must be positive')
    inv = inventory(root)
    selected = closure(inv, module)
    ordered = [mod for mod in inv['topological_order'] if mod in selected]
    if not ordered or set(ordered) != selected:
        raise AuditError('invalid or incomplete selected import closure')
    source_hashes = inv['source_hashes']
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    logs = root / 'logs' / 'serial_builds' / stamp
    logs.mkdir(parents=True, exist_ok=False)
    results = {}
    outputs = {}
    pending = {'status': 'RUNNING', 'selected_module': module,
               'complete_formalization': False, 'all_selected_modules_passed': False,
               'log_directory': str(logs.relative_to(root))}
    (root / 'logs' / 'latest_serial_build.json').write_text(json.dumps(pending, indent=2) + '\n')
    for mod in ordered:
        relative = Path(*mod.split('.'))
        output = root / '.lake' / 'build' / 'lib' / 'lean' / relative.with_suffix('.olean')
        if not output.resolve().is_relative_to(root.resolve()):
            raise AuditError('refusing external build output: ' + str(output))
        output.parent.mkdir(parents=True, exist_ok=True)
        outputs[mod] = output
        # Invalidate the ENTIRE closure first, including modules later skipped.
        output.unlink(missing_ok=True)
        output.with_suffix('.ilean').unlink(missing_ok=True)
    try:
        for mod in ordered:
            relative = Path(*mod.split('.'))
            output = outputs[mod]
            failed = [dep for dep in inv['imports'][mod]
                      if results[dep]['status'] != 'passed']
            if failed:
                results[mod] = {'status': 'blocked_by_failed_import', 'imports': failed}
            else:
                command = ['lake', 'env', 'lean', '-j1', '-s65536',
                           '-o', str(output), str(relative.with_suffix('.lean'))]
                start = time.monotonic()
                with (logs / (mod + '.log')).open('w') as log:
                    log.write('$ ' + ' '.join(command) + '\n')
                    log.flush()
                    try:
                        code, _, timed_out = execute(command, cwd=root, stdout=log, timeout=timeout)
                        status = 'timeout' if timed_out else ('passed' if code == 0 else 'failed')
                        if status == 'passed' and not output.is_file():
                            status = 'missing_output'
                            log.write('\nCompiler exited zero without producing the required object.\n')
                    except OSError as ex:
                        status, code = 'execution_error', None
                        log.write(str(ex) + '\n')
                    if status != 'passed':
                        output.unlink(missing_ok=True)
                    results[mod] = {'status': status, 'exit': code,
                                    'seconds': round(time.monotonic() - start, 3),
                                    'command': command}
                    if status == 'passed':
                        results[mod]['olean_sha256'] = hashlib.sha256(output.read_bytes()).hexdigest()
                print(mod + ': ' + status, flush=True)
            (logs / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
        after = inventory(root)
        if after['source_hashes'] != source_hashes:
            raise AuditError('project sources changed during serial compilation')
    except BaseException as ex:
        pending.update(status='ABORTED', error=str(ex))
        (logs / 'summary.json').write_text(json.dumps(pending, indent=2) + '\n')
        (root / 'logs' / 'latest_serial_build.json').write_text(json.dumps(pending, indent=2) + '\n')
        # A partially completed interrupted run cannot supply reusable proof objects.
        for output in outputs.values():
            output.unlink(missing_ok=True)
        raise
    summary = {'selected_module': module, 'selected_modules': ordered,
               'complete_formalization': False,
               'dependencies_rebuilt_from_source': False,
               'all_selected_modules_passed':
                   set(results) == selected and all(x['status'] == 'passed' for x in results.values()),
               'source_hashes': source_hashes, 'results': results,
               'log_directory': str(logs.relative_to(root))}
    summary['status'] = 'PASSED_CURRENT_SOURCE_ONLY' if summary['all_selected_modules_passed'] else 'FAILED'
    (logs / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    (root / 'logs' / 'latest_serial_build.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in {'results', 'source_hashes'}}, indent=2))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--module', default='Kourovka')
    parser.add_argument('--timeout', type=int, default=1800, help='maximum seconds per module')
    args = parser.parse_args()
    try:
        result = build(ROOT, args.module, args.timeout)
        return 0 if result['all_selected_modules_passed'] else 2
    except (AuditError, OSError, ValueError) as ex:
        print('Serial build failed: ' + str(ex), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
