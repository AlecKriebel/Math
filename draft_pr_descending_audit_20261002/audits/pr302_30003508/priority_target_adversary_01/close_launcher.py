"""Observe native private-audit closure, retaining real streams/PID/exit and final modes."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parent
EXPECTED = Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr302_30003508/priority_target_adversary_01')
assert BASE == EXPECTED


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def pin(path):
    p = Path(path)
    raw = p.read_bytes()
    return {'path': str(p), 'resolved_path': str(p.resolve()), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest(),
            'mode_observed': oct(p.stat().st_mode & 0o7777)}


def main():
    out = BASE / 'closure_capture'
    out.mkdir()
    retained = out / 'launcher_source.py'
    retained.write_bytes(Path(__file__).read_bytes())
    retained.chmod(0o444)
    payload = BASE / 'close_payload.py'
    python = Path(sys.executable).resolve()
    argv = [str(python), '-E', '-B', str(payload)]
    record = {'kind': 'actual_native_private_audit_closure', 'launcher_pid': os.getpid(),
              'launcher_argv': sys.argv, 'launcher_cwd': os.getcwd(),
              'launcher_source': pin(Path(__file__).resolve()),
              'retained_launcher_source': pin(retained), 'child_source': pin(payload),
              'launcher_and_child_python': pin(python),
              'runtime': {'sys_version': sys.version, 'optimization': sys.flags.optimize,
                          'selected_stdlib_whole_pins': [pin(m.__file__) for m in
                                                        (datetime, hashlib, json, shutil, subprocess)
                                                        if getattr(m, '__file__', None)],
                          'limit': 'Named whole source/executable/stdlib pins, not full OS/dynamic/import closure.'},
              'argv': argv, 'cwd': str(BASE), 'started_utc': now()}
    with (out / 'stdout.bin').open('wb') as so, (out / 'stderr.bin').open('wb') as se:
        child = subprocess.Popen(argv, cwd=BASE, stdout=so, stderr=se)
        record['actual_child_pid'] = child.pid
        record['observed_exit_code'] = child.wait()
    record['child_completed_utc'] = now()
    record['stdout'] = pin(out / 'stdout.bin')
    record['stderr'] = pin(out / 'stderr.bin')
    receipt = out / 'execution.json'
    if record['observed_exit_code'] != 0:
        receipt.write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
        print(json.dumps({'closure_failed': True, 'actual_child_pid': child.pid,
                          'observed_exit': child.returncode, 'receipt': str(receipt)}))
        return 1
    record['output_inventory'] = pin(BASE / 'OUTPUT_INVENTORY.json')
    record['input_inventory'] = pin(BASE / 'INPUT_INVENTORY.json')
    record['control_check'] = pin(BASE / 'CONTROL_CHECK.json')
    mode_changes = []
    # Receipt is opened before mode sealing; its observed process record is written
    # through this existing descriptor after chmod, rather than inventing its exit.
    with receipt.open('w') as f:
        paths = sorted(p for p in BASE.rglob('*') if p.is_file())
        for p in paths:
            before = oct(p.stat().st_mode & 0o7777)
            p.chmod(0o444)
            mode_changes.append({'path': str(p), 'before': before, 'after_observed': oct(p.stat().st_mode & 0o7777)})
        dirs = [BASE, *[p for p in BASE.rglob('*') if p.is_dir()]]
        for p in sorted(dirs, key=lambda d: len(d.parts), reverse=True):
            before = oct(p.stat().st_mode & 0o7777)
            p.chmod(0o555)
            mode_changes.append({'path': str(p), 'before': before, 'after_observed': oct(p.stat().st_mode & 0o7777)})
        file_modes = [{'path': str(p), 'mode_observed': oct(p.stat().st_mode & 0o7777)} for p in paths]
        dir_modes = [{'path': str(p), 'mode_observed': oct(p.stat().st_mode & 0o7777)} for p in dirs]
        assert all(x['mode_observed'] == '0o444' for x in file_modes)
        assert all(x['mode_observed'] == '0o555' for x in dir_modes)
        record['final_mode_verification'] = {'verified_utc': now(), 'files_count': len(paths),
                                           'directories_count': len(dirs), 'files': file_modes,
                                           'directories': dir_modes, 'observed_mode_changes': mode_changes,
                                           'all_files0444_dirs0555': True}
        record['stdout_final'] = pin(out / 'stdout.bin')
        record['stderr_final'] = pin(out / 'stderr.bin')
        record['completed_utc'] = now()
        record['noncircular_exclusions'] = ['OUTPUT_INVENTORY.json', 'closure_capture/stdout.bin',
                                         'closure_capture/stderr.bin', 'closure_capture/execution.json']
        record['historical_records_unchanged'] = True
        f.write(json.dumps(record, sort_keys=True, indent=2) + '\n')
        f.flush()
        os.fsync(f.fileno())
    print(json.dumps({'closure_completed': True, 'actual_child_pid': child.pid,
                      'observed_child_exit': child.returncode, 'completed_utc': now(),
                      'whole_pins': {name: pin(BASE / name) for name in
                                     ['REPORT.md', 'VERDICT.json', 'INPUT_INVENTORY.json',
                                      'OUTPUT_INVENTORY.json', 'CONTROL_CHECK.json',
                                      'closure_capture/execution.json']},
                      'files0444': len(paths), 'directories0555': len(dirs)}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
