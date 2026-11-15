"""Default held-data checks only. --live requires a later real root install receipt."""
import sys
sys.dont_write_bytecode = True
import argparse
import json
from pathlib import Path
import exact11_lib as L


def held_contract():
    # Revision default deliberately does not reopen any upstream packet/source descriptor.
    contract = L.obj(L.O / 'HELD_BASELINE_CONTRACT.json')
    rows = L.overlay_rows(L.obj(L.O / 'inputs/stage-OVERLAY_MANIFEST.json')['files'],
                          L.obj(L.O / 'inputs/stage-INSTALLATION_PLAN.json'))
    raw = L.read(L.O / 'private/retained-approved-index')
    index = L.parse_index(raw, {('public/' + r['path']).encode() for r in rows})
    L.need(L.sha(raw) == contract['Git']['index_SHA256']
           and index['count'] == 58554 and index['protected_record_count'] == 58552
           and index['protected_raw_records_SHA256'] == contract['Git']['protected_raw_records_SHA256'],
           'retained whole native index and new-scope protection')
    L.need(contract['source_data_only'] is True
           and contract['current_live_website_dot_git_or_remote_requeried_by_preparation'] is False,
           'original held observation remains literal, no new live scan')
    return contract


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit-contract', action='store_true')
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--adoption-sha256')
    args = parser.parse_args()
    L.need(not (args.emit_contract and args.live), 'distinct held/live phases')
    contract = held_contract()
    if args.emit_contract:
        print(json.dumps(contract, indent=2))
        return
    L.need(contract == L.obj(L.O / 'HELD_BASELINE_CONTRACT.json'), 'whole reproducible held contract')
    if args.live:
        adoption = L.root_adoption(args.adoption_sha256)
        rows, summary = L.stage_fences('baseline')
        raw, index, state = L.website_git_state(rows)
        L.need(raw == L.read(L.O / 'private/retained-approved-index'), 'future actual raw index matches held buffer')
        for key in ['HEAD', 'master', 'branch', 'HEAD_file_SHA256', 'master_file_SHA256',
                    'local_git_config_SHA256', 'index_SHA256', 'protected_raw_records_SHA256',
                    'protected_stage_tuple_SHA256', 'origin_push_URL_SHA256', 'remote_master']:
            L.need(state[key] == contract['Git'][key], 'future actual unchanged fence: ' + key)
        result = {'status': 'PASS_LATER_ROOT_AUTHORIZED_LIVE_PREFLIGHT', 'actual_Git': state,
                  'stage_and_website': summary, 'root_install_receipt_SHA256': args.adoption_sha256,
                  'mutations': False}
    else:
        L.need(L.LIVE_AUTHORIZED is False, 'default remains source-only')
        result = {'status': 'PASS_SOURCE_ONLY_HELD_PREFLIGHT', 'held_contract_SHA256': L.sha(L.read(L.O / 'HELD_BASELINE_CONTRACT.json')),
                  'held_baseline': [614, 92, 93], 'proposal': [623, 94, 95],
                  'retained_index_records': 58554, 'protected_native_records': 58552,
                  'website_dot_git_or_remote_access': False, 'Git_commands': 0,
                  'installation_or_publication_authority': False}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
