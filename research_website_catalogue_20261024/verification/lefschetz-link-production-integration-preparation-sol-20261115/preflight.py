"""Read-only website/Git/remote fences. --capture writes only this new preparation."""
import sys
sys.dont_write_bytecode = True
import argparse
import json
from pathlib import Path
from exact11_lib import (O, W, S, BASE, STAGE_SEAL, AUDIT_SEAL, ADOPTION, COMMIT_APPROVAL,
                         need, now, sha, read, obj, stage_fences, website_git_state, git)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--capture', action='store_true')
    args = parser.parse_args()
    rows, summary = stage_fences('baseline')
    raw, index, state = website_git_state(rows)
    result = {'UTC': now(), 'status': 'PASS_READ_ONLY_EXACT11_PREFLIGHT',
              'baseline_HEAD': BASE, 'stage_final_seal_SHA256': STAGE_SEAL,
              'audit_final_seal_SHA256': AUDIT_SEAL, 'stage_and_website': summary, 'Git': state,
              'website_Git_or_remote_mutations': False, 'stage_or_audit_code_executed': False,
              'current_pair_root_adopted': False, 'production_install_authorized': False}
    if args.capture:
        need(not (O / 'PREFLIGHT_CAPTURE.json').exists(), 'capture is write-once')
        need(not ADOPTION.exists() and not COMMIT_APPROVAL.exists(), 'no current root install/commit authority')
        protected = b'\0'.join(p + b'\t' + r.hex().encode() for p, r in index['protected']) + b'\0'
        deletions = git('diff', '--cached', '--name-only', '--diff-filter=D', '-z', BASE)
        (O / 'private/shared-index.before').write_bytes(raw)
        (O / 'private/protected-index.raw-records').write_bytes(protected)
        (O / 'private/staged-deletions.z').write_bytes(deletions)
        need(sha(protected) == state['protected_raw_records_SHA256'], 'whole protected raw records')
        need(read(W / '.git/index') == raw, 'shared index unchanged during capture')
        result['staged_deletions'] = {'count': len([x for x in deletions.split(b'\0') if x]),
                                      'bytes': len(deletions), 'SHA256': sha(deletions),
                                      'path': 'private/staged-deletions.z'}
        result['whole_original_index_snapshot'] = 'private/shared-index.before'
        result['whole_protected_native_records'] = 'private/protected-index.raw-records'
        result['current_root_authority_paths_observed_absent'] = [str(ADOPTION), str(COMMIT_APPROVAL)]
        (O / 'PREFLIGHT_CAPTURE.json').write_text(json.dumps(result, indent=2) + '\n')
    else:
        capture = obj(O / 'PREFLIGHT_CAPTURE.json')
        for key in ['HEAD', 'master', 'branch', 'HEAD_file_SHA256', 'master_file_SHA256',
                    'local_git_config_SHA256', 'index_SHA256', 'protected_raw_records_SHA256',
                    'protected_stage_tuple_SHA256', 'origin_push_URL_SHA256', 'remote_master']:
            need(state[key] == capture['Git'][key], 'fresh unchanged control fence: ' + key)
        need(raw == read(O / 'private/shared-index.before'), 'whole fresh raw shared index remains equal')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
