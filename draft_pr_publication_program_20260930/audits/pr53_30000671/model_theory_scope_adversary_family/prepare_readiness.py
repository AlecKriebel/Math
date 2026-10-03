"""Write a lean SOURCE readiness index; do not execute the ROOT-only closer."""
import datetime as dt
import json
from closed_scope_common import F, EXCLUDED, digest, file_row, inventory, prepared_check

def main():
    assert not any((F / name).exists() for name in EXCLUDED)
    files, dirs = inventory()
    index = {'schema': 'pr53-model-theory-prepared-payload-index/v1',
             'files': [file_row(F / name) for name in sorted(files)],
             'directories': sorted(dirs), 'root_approval': False}
    with (F / 'PAYLOAD_INDEX.json').open('x') as stream:
        stream.write(json.dumps(index, indent=2) + '\n')
    keys = ['REPORT.md', 'VERDICT.json', 'INVERSE_SYSTEM_PROOF.md',
            'FIXED_EXTERNAL_INPUTS.json', 'closed_scope_common.py',
            'close_for_ROOT.py', 'verify_closed_readonly.py']
    ready = {'schema': 'pr53-model-theory-adversary-ready/v1',
             'status': 'READY_FOR_ROOT_CUSTODY_ONLY',
             'prepared_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
             'prepared_payload_files': len(files) + 2,
             'payload_index_sha256': digest(F / 'PAYLOAD_INDEX.json'),
             'key_sha256': {name: digest(F / name) for name in keys},
             'mandatory_repairs': [], 'root_approval': False,
             'root_closer_executed': False, 'manifest_present': False,
             'root_closer_argv': ['/usr/bin/python3', '-B', str(F / 'close_for_ROOT.py')],
             'separate_reader_argv_template': ['/usr/bin/python3', '-B',
                 str(F / 'verify_closed_readonly.py'), 'ACTUAL_ROOT_CLOSED_MANIFEST_SHA256'],
             'no_native_git_remote_publication_writes': True}
    with (F / 'READY.json').open('x') as stream:
        stream.write(json.dumps(ready, indent=2) + '\n')
    checked_files, checked_dirs, refs, captures = prepared_check()
    print(json.dumps({'status': 'PASS_PREPARED_READINESS_ONLY',
                      'prepared_payload_files': len(checked_files),
                      'directories': len(checked_dirs),
                      'external_fixed_references': refs, 'actual_capture_objects': captures,
                      'manifest_present': False, 'root_closer_executed': False,
                      'ready_sha256': digest(F / 'READY.json'),
                      'report_sha256': digest(F / 'REPORT.md'),
                      'verdict_sha256': digest(F / 'VERDICT.json'),
                      'proof_sha256': digest(F / 'INVERSE_SYSTEM_PROOF.md'),
                      'root_approval': False}, indent=2))

if __name__ == '__main__':
    main()
