#!/usr/bin/env python3
"""Explicit metadata-only preparation/sealing; inert default.

Writes only three exact root controls in this new owned namespace. --seal
runs only the fully read new offline custody helper; no native/science route.
Actual stdout/stderr/exits are retained even when a preseal check fails.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import stat
import subprocess
import sys

A = Path(__file__).resolve().parent
TERMINALS = ['CLOSURE.json', 'FINAL_MANIFEST.json', 'FINAL_SEAL.json']


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def pin(p, relative=False):
    b = p.read_bytes()
    return {'path': p.relative_to(A).as_posix() if relative else str(p),
            'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()}


def save(name, obj):
    (A / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def inventory():
    files, dirs = [], []
    for base, names, leaves in os.walk(A, followlinks=False):
        names.sort()
        leaves.sort()
        for n in names:
            p = Path(base) / n
            if not stat.S_ISDIR(p.lstat().st_mode):
                raise ValueError('nonordinary directory')
            dirs.append(p.relative_to(A).as_posix())
        for n in leaves:
            p = Path(base) / n
            if not stat.S_ISREG(p.lstat().st_mode):
                raise ValueError('nonordinary file')
            if p.relative_to(A).as_posix() not in TERMINALS:
                files.append(pin(p, True))
    return sorted(files, key=lambda r: r['path']), sorted(dirs)


def main():
    if sys.argv[1:] not in (['--prepare'], ['--seal']):
        print('Inert default; explicit --prepare or --seal required.')
        return
    if sys.argv[1:] == ['--prepare']:
        if any((A / n).exists() for n in TERMINALS):
            raise ValueError('refuse overwriting any terminal preparation')
        files, dirs = inventory()
        save('CLOSURE.json', {'status': 'PREPARED_NOT_EXECUTED', 'attempts': []})
        save('FINAL_SEAL.json', {'status': 'UNFINALIZED_PRESEAL_PLACEHOLDER'})
        save('FINAL_MANIFEST.json', {'schema': 'row143-scope-exact-finite-manifest-v1',
                                   'UTC': utc(), 'owned_root': str(A),
                                   'files': files, 'directories': dirs,
                                   'exact_root_terminals': TERMINALS,
                                   'all_exact_root_terminals_now_ordinary': True,
                                   'future_or_basename_exclusions': False})
        print(json.dumps({'status': 'PREPARED', 'payloads': len(files),
                          'actual_files': len(files) + 3, 'directories': len(dirs)}))
        return
    seal = json.loads((A / 'FINAL_SEAL.json').read_text())
    if seal.get('status') != 'UNFINALIZED_PRESEAL_PLACEHOLDER':
        raise ValueError('refuse writing a finalized seal')
    closure = json.loads((A / 'CLOSURE.json').read_text())
    attempts = closure['attempts']
    for optimize in [False, True]:
        command = [sys.executable, '-B'] + (['-O'] if optimize else []) + [str(A / 'verify_custody.py'), '--preseal']
        start = utc()
        r = subprocess.run(command, capture_output=True)
        record = {'started_UTC': start, 'completed_UTC': utc(), 'argv': command,
                  'exit': r.returncode, 'stdout': r.stdout.decode('utf-8'),
                  'stderr': r.stderr.decode('utf-8'), 'optimized': optimize,
                  'explicit_preseal_not_final_default': True}
        attempts.append(record)
        save('CLOSURE.json', {'schema': 'row143-scope-literal-preseal-closure-v1',
                              'status': 'PRESEAL_FAILED' if r.returncode else 'PRESEAL_CHECK_RECORDED',
                              'attempts': attempts,
                              'all_prior_attempts_retained': True,
                              'current_helper': pin(A / 'verify_custody.py'),
                              'final_default_receipts_not_falsely_claimed': True})
        if r.returncode:
            print(json.dumps({'status': 'PRESEAL_FAILED', 'exit': r.returncode,
                              'whole_streams_retained': 'CLOSURE.json'}))
            raise SystemExit(r.returncode)
    manifest = json.loads((A / 'FINAL_MANIFEST.json').read_text())
    save('FINAL_SEAL.json', {'schema': 'row143-independent-scope-final-seal-v1',
                           'UTC': utc(), 'status': 'INDEPENDENT_SCOPE_FINAL_SEALED',
                           'record_id': 22982894, 'sheet_row': 143,
                           'manifest': pin(A / 'FINAL_MANIFEST.json'),
                           'closure': pin(A / 'CLOSURE.json'),
                           'current_pure_helper': pin(A / 'verify_custody.py'),
                           'full_helper_read_receipt': pin(A / 'CONTROL_READ_RECEIPT.json'),
                           'payload_count': len(manifest['files']),
                           'actual_file_count': len(manifest['files']) + 3,
                           'directory_count': len(manifest['directories']),
                           'exact_root_terminals': TERMINALS,
                           'all_files_and_directories_closed': True,
                           'no_future_or_basename_carveouts': True,
                           'source_files': 108, 'source_directories': 14,
                           'source_ZIP_regular_occurrences': 48,
                           'complete_PDF_pages': 3, 'controlling_TeX_lines': 192,
                           'source_seal_SHA256': '24e7b08bda1c3561d9db2040745b2b1b8eb5b2e1f8c37be60426e831511cfb11',
                           'INITIAL_seal_SHA256': '34ee9916ed52e047272becb1f571883dc4efce486e30717bd57a383c0edc50e9',
                           'own_results_seal_SHA256': '87923ccd3c29a1efdd4616e1822632464d5011065fdd0929cfb4eed371b74135',
                           'qualified_core': '17 originals plus sole authorized405b checkpoint helper',
                           'scientific_findings_disclosed': False,
                           'root143_gate_at_seal': 'CLOSED',
                           'publication_authority': False, 'canonical_url': None, 'AA': None,
                           'followup': None, 'completion_percent': 100,
                           'actual_preseal_normal_O_streams_in_closure': True,
                           'final_defaults_will_be_issued_after_seal_without_packet_writes': True,
                           'immutable_after_seal': True})
    print(json.dumps({'status': 'FINAL_SEALED', 'seal': pin(A / 'FINAL_SEAL.json'),
                      'manifest': pin(A / 'FINAL_MANIFEST.json'),
                      'closure': pin(A / 'CLOSURE.json')}))


if __name__ == '__main__':
    main()
