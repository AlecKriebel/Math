"""Default held-data checks only. --live requires a later real root install receipt."""
import sys
sys.dont_write_bytecode = True
import argparse
import json
from pathlib import Path
import exact11_lib as L


def held_contract():
    rows, summary = L.stage_fences('held')
    observation = L.obj(L.A / 'FRESH_GIT_OBSERVATIONS.json')
    raw = L.pin(L.O / 'private/retained-approved-index', observation['actual_raw_index_file_observation'])
    targets = {('public/' + row['path']).encode() for row in rows}
    index = L.parse_index(raw, targets)
    tuples = [('%06o' % mode).encode() + b' ' + oid.encode() + b' 0\t' + path
              for path, record, mode, oid in index['entries']]
    whole_tuples = b'\0'.join(tuples) + b'\0'
    L.need(whole_tuples == L.pin(Path(observation['raw_index_records']['path']), observation['raw_index_records']),
           'whole retained binary agrees with independently observed actual stage tuples')
    protected = [value for value in tuples if value.split(b'\t', 1)[1] not in targets]
    protected_tuples = b'\0'.join(protected) + b'\0'
    L.need(protected_tuples == L.pin(Path(observation['fresh_protected_raw_records']['path']),
                                   observation['fresh_protected_raw_records']), 'whole58552 independent protected tuples')
    existing = {path for path, record, mode, oid in index['entries'] if path in targets}
    L.need(existing == {('public/' + path).encode() for path in L.AGGREGATES},
           'only two existing index targets; all nine new leaves absent')
    L.need(index['count'] == observation['all_index_record_count'] == 58554
           and index['protected_record_count'] == observation['fresh_protected_index_record_count'] == 58552,
           'current-scope held index counts, never prior58543 count')
    prior = L.obj(L.O / 'inputs/prior-PREFLIGHT_CAPTURE.json')['Git']
    prepublication = L.obj(L.O / 'inputs/prior-PRE_PUBLICATION.json')
    publication = L.obj(L.O / 'inputs/prior-PUBLICATION.json')
    L.need(L.sha(raw) == prepublication['approved_index_SHA256']
           and prepublication['commit'] == publication['commit'] == observation['website_HEAD'] == L.BASE,
           'same retained approved buffer, prior publication and independent actual observation')
    state = {'HEAD': L.BASE, 'master': L.BASE, 'branch': 'master',
             'HEAD_file_SHA256': L.sha(b'ref: refs/heads/master\n'),
             'master_file_SHA256': L.sha((L.BASE + '\n').encode()),
             'local_git_config_SHA256': prior['local_git_config_SHA256'],
             'index_SHA256': L.sha(raw), 'index_record_count': index['count'],
             'protected_record_count': index['protected_record_count'],
             'protected_raw_records_SHA256': index['protected_raw_records_SHA256'],
             'protected_stage_tuple_SHA256': L.sha(protected_tuples),
             'origin_push_URL_SHA256': prior['origin_push_URL_SHA256'],
             'remote_master': L.BASE, 'fresh_remote_read_by_this_preparation': False}
    return {'schema': 'held_expected_before_exact11_contract_no_live_access_v1',
            'independent_observation_UTC': observation['UTC'], 'Git': state,
            'stage_and_held_baseline': summary, 'source_data_only': True,
            'retained_index_buffer': 'private/retained-approved-index',
            'expected_HEAD_master_file_bytes_derived_from_checked_BASE': True,
            'Git_config_and_push_URL_pins_retained_from_prior_approved_preflight': True,
            'future_live_byte_identity_and_actual_remote_advertisement_required': True,
            'current_live_website_dot_git_or_remote_requeried_by_preparation': False,
            'installation_or_publication_authority': False}


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
