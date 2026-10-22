#!/usr/bin/env python3
"""Read-only structural coverage of the resumable sweep; never proof/priority clearance."""
import collections
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parent
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
SHEET_GID = 1254632077
# Only this exact, already independently verified historical receipt predates
# separate public-file receipts. Modern publications cannot opt into its schema.
LEGACY_RECEIPT = ('PR0292_PUBLICATION_VERIFICATION.json',
                  'ad5cad544399809004b1007a2758444fbc43891ad28a4745fffa805f46987cf2')


def evidence_json(name):
    if not isinstance(name, str):
        raise RuntimeError('Evidence path must be an exact relative filename')
    relative = PurePosixPath(name)
    if (relative.is_absolute() or '..' in relative.parts or relative.as_posix() != name
            or any(ROOT.joinpath(*relative.parts[:i]).is_symlink()
                   for i in range(1, len(relative.parts)+1))):
        raise RuntimeError('Unsafe evidence path')
    path = ROOT/name
    if not path.is_file() or not path.resolve().is_relative_to(ROOT.resolve()):
        raise RuntimeError('Missing evidence file')
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise RuntimeError('Evidence must be a JSON object')
    return value


def public_files(value):
    files = value.get('files')
    if not isinstance(files, list) or len(files) < 2:
        raise RuntimeError('Published PDF and supporting archive evidence is required')
    result = {}
    for entry in files:
        name = entry.get('name')
        if (not isinstance(name, str) or PurePosixPath(name).name != name
                or name in {'.', '..'} or name in result):
            raise RuntimeError('Unsafe or duplicate public filename')
        digest = entry.get('sha256')
        size = entry.get('bytes', entry.get('size'))
        if type(size) is not int or size <= 0 or not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest):
            raise RuntimeError('Missing public file size or SHA256')
        legacy = 'download_verified' in entry
        if legacy:
            if any(k in entry for k in ('downloaded_and_matches_reviewed', 'http_status', 'bytes', 'md5')):
                raise RuntimeError('Mixed or contradictory public download schemas')
            md5 = entry.get('checksum', '')
            if entry.get('download_verified') is not True or not re.fullmatch('md5:[0-9a-f]{32}', md5):
                raise RuntimeError('Legacy public download is not verified')
            md5 = md5[4:]
        else:
            md5 = entry.get('md5', '')
            if (entry.get('downloaded_and_matches_reviewed') is not True
                    or type(entry.get('http_status')) is not int or entry['http_status'] != 200
                    or not re.fullmatch('[0-9a-f]{32}', md5)):
                raise RuntimeError('Public download is not verified')
        if name.endswith('.zip'):
            members = entry.get('members')
            if legacy:
                if (entry.get('zip_crc_ok') is not True or not isinstance(members, list)
                        or len(members) < 2 or len(members) != len(set(members))
                        or any(not isinstance(m, str) or PurePosixPath(m).is_absolute()
                               or '..' in PurePosixPath(m).parts for m in members)):
                    raise RuntimeError('Legacy supporting archive evidence is incomplete')
            elif (entry.get('zip_crc_safe_unique_pass') is not True
                  or type(members) is not int or members < 2
                  or type(entry.get('all_manifest_payloads_verified')) is not int
                  or entry['all_manifest_payloads_verified'] != members-1):
                raise RuntimeError('Supporting archive manifest evidence is incomplete')
        archive_evidence = ((tuple(sorted(members)) if legacy else
                             (members, entry['all_manifest_payloads_verified']))
                            if name.endswith('.zip') else None)
        result[name] = (size, digest, md5, archive_evidence)
    if not any(n.endswith('.pdf') for n in result) or not any(n.endswith('.zip') for n in result):
        raise RuntimeError('Published PDF or supporting archive absent')
    return result


def verify_resolution(value, record, doi):
    if not isinstance(value, dict):
        raise RuntimeError('DOI resolution must be an object')
    status = value.get('http_status') if value.get('status') == 'resolved' else value.get('status')
    target = 'https://zenodo.org/records/'+str(record)
    if (type(status) is not int or status != 200 or value.get('resolved_url') != target
            or ('http_status' in value and (type(value['http_status']) is not int or value['http_status'] != 200))
            or ('url' in value and value['url'] != 'https://doi.org/'+doi)
            or ('expected_record' in value and (type(value['expected_record']) is not int or value['expected_record'] != record))
            or ('exact_expected_record_destination_verified' in value
                and value['exact_expected_record_destination_verified'] is not True)):
        raise RuntimeError('Exact canonical DOI destination evidence absent or contradictory')
    if 'destination_verified' in value:
        bound = value['destination_verified']
        if (not isinstance(bound, dict) or type(bound.get('record')) is not int or bound['record'] != record
                or type(bound.get('status')) is not int or bound['status'] != 200 or bound.get('resolved_url') != target):
            raise RuntimeError('Nested DOI destination proof contradicts its record')


def verify_completed_publications(own, effective, reopened):
    expected = {n: e for n, e in effective.items() if e['disposition'] == 'published_verified_full_solution'}
    identities = [set() for _ in range(5)]
    for item in own:
        number, record, row = item.get('pr'), item.get('record'), item.get('ledger_row')
        problem, doi = item.get('problem_id'), item.get('doi')
        if (any(type(v) is not int or v <= 0 for v in [number, record, row]) or row < 2
                or not isinstance(problem, str) or not re.fullmatch('[1-9][0-9]*', problem)
                or doi != '10.5281/zenodo.'+str(record) or number not in expected):
            raise RuntimeError('Malformed or unbound completed publication identity')
        for seen, identity in zip(identities, [number, record, row, problem, doi]):
            if identity in seen:
                raise RuntimeError('Completed publication repeats a PR, record, row, problem or DOI')
            seen.add(identity)
        entry = expected[number]
        name = f'PR{number:04d}_'+('REOPENED_' if number in reopened else '')+'PUBLICATION_VERIFICATION.json'
        if item.get('verification') != name or entry.get('publication_evidence') != name:
            raise RuntimeError('Completed entry and effective disposition name different canonical evidence')
        proof = evidence_json(name)
        merge = item.get('merge_commit')
        if (type(entry.get('pr')) is not int or entry['pr'] != number
                or type(proof.get('pr')) is not int or proof['pr'] != number
                or proof.get('record') != record or type(proof.get('record')) is not int
                or proof.get('doi') != doi or entry.get('doi') != doi
                or proof.get('problem_ids') != [problem] or entry.get('problem_ids') != [problem]
                or proof.get('ledger_row') != row or type(proof.get('ledger_row')) is not int
                or entry.get('ledger_row') != row or type(entry.get('ledger_row')) is not int
                or not isinstance(merge, str) or not re.fullmatch('[0-9a-f]{40}', merge)
                or proof.get('merge_commit') != merge or entry.get('merge_commit', merge) != merge
                or entry.get('new_publication') is not True or proof.get('published') is not True
                or proof.get('ledger_read_back_exact') is not True or proof.get('unique_target_and_DOI') is not True
                or proof.get('doi_url') != 'https://doi.org/'+doi
                or proof.get('record_url') != 'https://zenodo.org/records/'+str(record)):
            raise RuntimeError('Completed publication cross-artifact identities disagree')
        verify_resolution(proof.get('doi_resolution'), record, doi)
        files = public_files(proof)
        evidence = proof.get('evidence', {})
        prefix = f'audits/pr{number:04d}_{problem}/'
        if evidence.get('ledger') != prefix+'LEDGER_PUBLICATION_VERIFICATION.json':
            raise RuntimeError('Ledger receipt is outside the corresponding publication')
        ledger = evidence_json(evidence['ledger'])
        values = ledger.get('values')
        if (type(ledger.get('pr')) is not int or ledger['pr'] != number or ledger.get('doi') != doi
                or type(ledger.get('row_number')) is not int or ledger['row_number'] != row
                or ledger.get('status') != 'verified' or ledger.get('read_back_exact') is not True
                or ledger.get('unique_target_and_DOI') is not True
                or ledger.get('spreadsheet_id') != SHEET or type(ledger.get('sheet_gid')) is not int
                or ledger['sheet_gid'] != SHEET_GID or not isinstance(values, list) or len(values) != 4
                or any(not isinstance(v, str) for v in values) or values[2] not in {doi, 'https://doi.org/'+doi}
                or not re.search(r'(?<![0-9])'+re.escape(problem)+r'(?![0-9])', values[0])
                or not re.search(r'https://github\.com/AlecKriebel/Math/pull/'+str(number)+r'(?![0-9])', ' '.join(values))):
            raise RuntimeError('Bound ledger receipt disagrees with publication')
        if 'public_files' in evidence:
            if evidence['public_files'] != prefix+'ZENODO_PUBLIC_FILE_VERIFICATION.json':
                raise RuntimeError('Public file receipt is outside the corresponding publication')
            payload = evidence_json(evidence['public_files'])
            verify_resolution(payload.get('doi_resolution'), record, doi)
            metadata_flags = [payload[k] for k in (
                'all_intended_authenticated_and_public_metadata_verified',
                'all_intended_metadata_verified_by_existing_tool') if k in payload]
            if (type(payload.get('pr')) is not int or payload['pr'] != number
                    or type(payload.get('record')) is not int or payload['record'] != record
                    or payload.get('doi') != doi or public_files(payload) != files
                    or payload.get('doi_url') != 'https://doi.org/'+doi
                    or type(payload.get('record_http_status')) is not int or payload['record_http_status'] != 200
                    or payload.get('title') != proof.get('title')
                    or ('version' in proof and payload.get('version') != proof['version'])
                    or payload.get('all_public_file_bytes_match_reviewed') is not True
                    or not metadata_flags or any(v is not True for v in metadata_flags)):
                raise RuntimeError('Bound public file receipt disagrees with publication')
        else:
            # The first released receipt uses the documented legacy download
            # schema and separately records its reviewed PDF/archive SHA pins.
            if (name != LEGACY_RECEIPT[0] or number != 292
                    or hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != LEGACY_RECEIPT[1]):
                raise RuntimeError('Only the exact pinned historical receipt may use legacy compatibility')
            pins = proof.get('reviewed_hashes', {})
            for extension, key in [('.pdf', 'pdf'), ('.zip', 'zip')]:
                if {v[1] for n, v in files.items() if n.endswith(extension)} != {pins.get(key)}:
                    raise RuntimeError('Legacy material differs from its reviewed SHA pins')
    if identities[0] != set(expected):
        raise RuntimeError('Completed list is not one-to-one with effective publication dispositions')


def snapshot():
    state = json.loads((ROOT/'STATE.json').read_text())
    inventory = json.loads((ROOT/'rest_inventory.json').read_text())
    journal = [json.loads(line) for line in (ROOT/'dispositions.jsonl').read_text().splitlines() if line.strip()]
    if any(type(entry.get('pr')) is not int for entry in journal):
        raise RuntimeError('Historical journal PR identities must be exact integers')
    numbers = [entry['pr'] for entry in journal]
    if numbers != list(range(state['start_pr'], state['next_pr'])):
        raise RuntimeError('Ordered journal is not the exact numerical prefix ending before next_pr')
    if state['last_completely_processed_pr'] != state['next_pr']-1 or state['completed_pr_count'] != len(numbers):
        raise RuntimeError('Cursor/count disagrees with ordered journal')
    inventory_numbers = [entry['number'] for entry in inventory['pull_requests']]
    if (any(type(n) is not int or n < state['start_pr'] for n in inventory_numbers)
            or len(inventory_numbers) != len(set(inventory_numbers))):
        raise RuntimeError('Inventory PR identities must be unique exact integers')
    known = set(inventory_numbers)
    if len(known) != inventory['in_scope_pr_count'] or max(known) != inventory['highest_pr']:
        raise RuntimeError('Inventory total/maximum mismatch')
    gaps = set(inventory['numeric_gaps'])
    if known | gaps != set(range(state['start_pr'], inventory['highest_pr']+1)) or known & gaps:
        raise RuntimeError('Inventory numbers/gap partition incomplete')
    if any(number not in known for number in numbers):
        raise RuntimeError('Journal contains a number absent from the actual PR inventory')
    for entry in journal:
        saved = json.loads((ROOT/('PR%04d_DISPOSITION.json' % entry['pr'])).read_text())
        if saved != entry:
            raise RuntimeError('Per-PR disposition differs from journal: '+str(entry['pr']))
    own = state.get('completed_publications', [])
    if not isinstance(own, list) or any(not isinstance(e, dict) for e in own):
        raise RuntimeError('Completed publications must be a list of objects')
    own_dois = [entry['doi'].removeprefix('https://doi.org/') for entry in own]
    if len(set(own_dois)) != len(own_dois):
        raise RuntimeError('Own completed publication list repeats a DOI')
    for entry in own:
        evidence = ROOT/entry['verification']
        if not evidence.is_file():
            raise RuntimeError('Own completed publication lacks its verification artifact')
    # Reopened work supersedes an old disposition without rewriting the ordered
    # journal. Bind each override to its exact historical artifact and its actual
    # completed-publication evidence before using it for effective accounting.
    effective = {entry['pr']: entry for entry in journal}
    overrides = state.get('reopened_disposition_overrides', [])
    seen_overrides = set()
    for item in overrides:
        number = item['pr']
        if number in seen_overrides or number not in effective:
            raise RuntimeError('Duplicate or out-of-prefix reopened override')
        seen_overrides.add(number)
        original_path = ROOT/f'PR{number:04d}_DISPOSITION.json'
        if hashlib.sha256(original_path.read_bytes()).hexdigest() != item['historical_disposition_sha256']:
            raise RuntimeError('Reopened override no longer binds its historical disposition')
        if item['replacement_disposition'] != f'PR{number:04d}_REOPENED_DISPOSITION.json':
            raise RuntimeError('Reopened replacement path is not canonical')
        replacement = evidence_json(item['replacement_disposition'])
        publication = evidence_json(replacement['publication_evidence'])
        completed = [v for v in own if v['pr'] == number]
        if (type(replacement['pr']) is not int or replacement['pr'] != number
                or replacement['disposition'] != 'published_verified_full_solution'
                or replacement.get('historical_disposition_sha256') != item['historical_disposition_sha256']
                or len(completed) != 1 or completed[0]['doi'] != replacement['doi']
                or publication.get('published') is not True or publication['doi'] != replacement['doi']
                or publication['ledger_row'] != completed[0]['ledger_row']
                or publication.get('ledger_read_back_exact') is not True
                or publication.get('unique_target_and_DOI') is not True):
            raise RuntimeError('Reopened publication override is not fully verified')
        effective[number] = replacement
    verify_completed_publications(own, effective, seen_overrides)
    raw_counts = dict(collections.Counter(entry['disposition'] for entry in journal))
    counts = dict(collections.Counter(entry['disposition'] for entry in effective.values()))
    doi_prs = collections.defaultdict(list)
    for entry in effective.values():
        if entry.get('doi'):
            doi_prs[entry['doi'].removeprefix('https://doi.org/')].append(entry['pr'])
    pending = sorted(known-set(numbers))
    return {
        'timestamp_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'scope': 'Structural progress only. No new mathematical, priority, live publication, sheet or final-reconciliation certification.',
        'inventory_timestamp': inventory['completed_at'],
        'highest_pr': inventory['highest_pr'],
        'in_scope_pr_count': len(known),
        'numeric_issue_gaps': sorted(gaps),
        'contiguous_completed_prefix': {'from': state['start_pr'], 'through': state['last_completely_processed_pr'], 'count': len(numbers)},
        'next_pr': state['next_pr'], 'pending_pr_count': len(pending),
        'first_pending_pr': pending[0] if pending else None,
        'last_pending_pr': pending[-1] if pending else None,
        'disposition_counts': counts,
        'historical_journal_disposition_counts': raw_counts,
        'verified_reopened_disposition_overrides': overrides,
        'own_completed_publications': own,
        'own_completed_dois_unique': True,
        'same_record_referenced_by_multiple_processed_PRs': {doi:prs for doi,prs in sorted(doi_prs.items()) if len(prs)>1},
        'reopened_candidates_requiring_final_override': state.get('reopened_candidates', []),
        'all_inventory_PRs_considered': not pending,
        'final_reconciliation_complete': False,
        'journal_sha256': hashlib.sha256((ROOT/'dispositions.jsonl').read_bytes()).hexdigest(),
        'completion_estimate_percent': state['completion_estimate_percent'],
    }

if __name__ == '__main__':
    print(json.dumps(snapshot(), indent=2))
