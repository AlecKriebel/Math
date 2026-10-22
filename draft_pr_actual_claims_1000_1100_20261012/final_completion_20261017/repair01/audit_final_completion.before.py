"""Verify the full finite-range goal against current records and remote reads.

No remote write is made. Full-sheet responses stay in memory; only this
program's exact rows enter the saved completion evidence.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import json
import re
import subprocess
import sys
import time

D = Path(__file__).resolve().parent.parent
REPO = D.parent
O_BASE = D / 'final_completion_20261017'
O = O_BASE
GWS = '/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077
sys.path.insert(0, str(REPO / 'zenodo_deposit_tool'))
import zenodo as z


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def read(path):
    return json.loads(path.read_text())


def ident(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def save(name, value):
    path = O / name
    need(not path.exists(), 'Preserve existing final evidence: ' + str(path))
    path.write_text(json.dumps(value, indent=2) + '\n')


def command(argv, label):
    attempts = []
    for attempt in range(3):
        try:
            result = subprocess.run(argv, cwd=REPO, capture_output=True, text=True, timeout=60)
            attempts.append({'attempt': attempt + 1, 'exit': result.returncode,
                             'stdout_sha256': hashlib.sha256(result.stdout.encode()).hexdigest(),
                             'stderr_sha256': hashlib.sha256(result.stderr.encode()).hexdigest()})
            if result.returncode == 0:
                return json.loads(result.stdout), {'label': label, 'argv': argv, 'attempts': attempts}
        except subprocess.TimeoutExpired:
            attempts.append({'attempt': attempt + 1, 'outcome': 'READ_ONLY_TIMEOUT'})
        time.sleep(attempt + 1)
    raise RuntimeError('Read-only request failed after bounded retries: ' + label)


def main():
    global O
    O_BASE.mkdir(exist_ok=True)
    for attempt in range(1, 100):
        O = O_BASE / ('attempt_' + str(attempt).zfill(2))
        try:
            O.mkdir()
            break
        except FileExistsError:
            continue
    else:
        raise RuntimeError('Preserve all previous final-audit attempts')
    print(json.dumps({'final_audit_attempt': str(O)}), flush=True)
    state = read(D / 'STATE.json')
    registry = read(D / 'CLAIM_REGISTRY.json')['records']
    candidates = state['candidate_full_claim_prs']
    excluded = state['skipped_as_partial_or_prior_prs']
    need(len(registry) == 101 and {r['pr'] for r in registry} == set(range(1000, 1101)), 'Full intake range')
    need(set(candidates).isdisjoint(excluded) and set(candidates) | set(excluded) == set(range(1000, 1101)), 'Scope partition')
    need(sorted(state['completed_prs']) == sorted(candidates) and state['next_pr'] is None, 'Every eligible workflow must finish')
    need(not state['scope_reconciliation_pending'], 'Unresolved intake ambiguity')
    accepted = {r['pr']: r for r in state['accepted_results']}
    need(len(accepted) == len(candidates), 'Exactly one accepted record per eligible PR')
    evidence_checked = 0
    for row in registry:
        for evidence in row.get('evidence', []):
            if isinstance(evidence, dict) and 'repository_path' in evidence:
                pins = read(D / f'intake/pr{row["pr"]}/PINS.json')
                matches = [p for p in pins['artifacts'] if p['repository_path'] == evidence['repository_path']]
                need(len(matches) == 1, 'Repository evidence lacks unique pinned intake copy')
                pin = matches[0]
                need(ident(D / pin['local_relative_path']) == {'bytes': pin['size'], 'sha256': pin['sha256']}, 'Pinned intake evidence drift')
                evidence_checked += 1
                continue
            reference = evidence if isinstance(evidence, str) else evidence.get('path')
            need(reference is not None, 'Unrecognized intake evidence reference')
            filename = reference.split('#', 1)[0]
            path = Path(filename)
            if not path.is_absolute():
                path = (REPO if path.parts[0] == D.name else D) / path
            need(path.exists(), 'Missing intake evidence: ' + reference)
            evidence_checked += 1

    # One fresh read covers all 101 current assertions and all accepted merges.
    fields = 'number state isDraft headRefOid title body mergedAt baseRefName baseRepository{nameWithOwner} mergeCommit{oid parents(first:10){nodes{oid}}}'
    selection = ' '.join(f'p{n}:pullRequest(number:{n}){{{fields}}}' for n in range(1000, 1101))
    query = 'query { repository(owner:"AlecKriebel",name:"Math") {' + selection + '} }'
    github, gh_receipt = command(['/opt/homebrew/bin/gh', 'api', 'graphql', '--raw-field', 'query=' + query], 'LIVE_ALL101_PR_SCOPE_AND_MERGES')
    need(not github.get('errors'), 'GraphQL returned errors')
    live = github['data']['repository']
    changed = []
    exclusion_pins = []
    for n in excluded:
        old = read(D / f'intake/pr{n}/pr.json')
        current = live['p' + str(n)]
        need(current is not None, 'Current excluded PR unavailable: ' + str(n))
        same = (current['headRefOid'] == old['headRefOid'] and current['title'] == old['title'] and current['body'] == old['body'])
        exclusion_pins.append({'pr': n, 'head': current['headRefOid'], 'current_state': current['state'],
                               'assertion_unchanged': same, 'body_sha256': hashlib.sha256(current['body'].encode()).hexdigest()})
        if not same:
            changed.append({'pr': n, 'original': old, 'current': current})
    save('EXCLUDED_CURRENT_SOURCE_CHECK.json', {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'records': exclusion_pins, 'changed_count': len(changed)})
    if changed:
        save('EXCLUDED_CHANGED_REQUIRES_RECLASSIFICATION.json', changed)
    need(not changed, 'Excluded assertions changed; inspect and reconcile before declaring completion')

    old_review_counts = {1001: 3, 1024: 2, 1025: 2, 1031: 4}
    entries = []
    for n in candidates:
        record = accepted[n]
        need(record['published'] and record['merged'] and record['tracker_exact_readback'], 'Incomplete accepted record')
        a = next((D / 'audits').glob('pr' + str(n) + '_*'))
        cfg_path = D / 'service_resume_20261016' / f'PR{n}_SERVICE_CONFIG.json'
        if cfg_path.exists():
            cfg = read(cfg_path)
            manifest = D / cfg['manifest']
            need(ident(manifest) == cfg['manifest_identity'] and ident(D / cfg['final_seal']) == cfg['final_seal_identity'], 'Final publication binding drift')
            authority = read(D / cfg['final_seal'])
            need(authority.get('publication_ready', authority.get('immutable_ready')) is True, 'Current ROOT readiness')
            issues = authority.get('actionable_issues')
            if n == 1098:
                need(authority['all_actionable_findings_resolved'], '1098 resolution gate')
                issues = read(a / 'ROOT_WHOLE_PACKAGE_REVIEW_02.json')['actionable_P0_P1_P2_P3']
            need(issues == 0 or issues == [] or issues == dict.fromkeys(('P0', 'P1', 'P2', 'P3'), 0), 'Current zero-actionable authority')
            count = cfg['fresh_complete_reviews']
            need(read(a / 'service_receipts_20261016/COMPLETION_RECONCILED.json')['state_saved_last'], 'Completion reconciliation absent')
            tracker_expected = read(a / 'service_receipts_20261016/TRACKER_VERIFIED.json')['values']
            for file in cfg['files']:
                need(ident(D / file['path']) == {key: file[key] for key in ('bytes', 'sha256')}, 'Reviewed binary drift')
        else:
            need(n in old_review_counts, 'Missing current service configuration')
            manifest = a / 'publication/zenodo-deposit.json'
            count = old_review_counts[n]
            tracker_expected = read(a / 'receipts/TRACKER_VERIFICATION.json')['values']
            if n == 1001:
                verdict = read(a / 'reviews/package_03/VERDICT.json')
                need(not verdict['actionable_concerns'] and verdict['status'].startswith('ACCEPT'), 'Original whole03 concerns')
                seal = read(a / 'receipts/FINAL_SEAL.json')
                need(seal['mechanical_additions_only_after_review'], 'Original finalization boundary')
            else:
                seal = read(a / 'FINAL_SEAL.json')
                need(seal['immutable_ready'] and seal['no_actionable_concerns'], 'Original final seal')
                count = seal.get('new_whole_package_reviews', seal.get('fresh_whole_package_reviews'))
        need(count >= 2, 'Minimum two complete reviews')
        metadata, files = z.load_manifest(manifest.resolve())
        disclosures = metadata.get('description', '') + metadata.get('notes', '')
        need('unrefereed' in disclosures.lower(), 'Unrefereed disclosure')
        need(re.search(r'\bAI\b|artificial intelligence', disclosures, re.I), 'Visible AI disclosure')
        need(any(c.get('orcid') == '0009-0001-9320-500X' for c in metadata['creators']), 'Author ORCID')
        pr = live['p' + str(n)]
        need(pr['state'] == 'MERGED' and pr['headRefOid'] == record['audited_and_merged_head'], 'Live exact-head PR acceptance')
        need(pr['baseRefName'] == 'main' and pr['baseRepository']['nameWithOwner'].casefold() == 'aleckriebel/math', 'Live merge base')
        need(pr['mergeCommit']['oid'] == record['merge_commit'] and record['audited_and_merged_head'] in [p['oid'] for p in pr['mergeCommit']['parents']['nodes']], 'Live exact audited head parent')
        need(record['doi'] in pr['body'], 'Published result absent from current PR acceptance')
        entries.append({'pr': n, 'manifest': manifest.resolve(), 'metadata': metadata, 'files': files,
                        'record': record, 'tracker_expected': tracker_expected, 'whole_reviews': count,
                        'live_merge': {'merge_commit': pr['mergeCommit']['oid'], 'merged_at': pr['mergedAt'], 'head': pr['headRefOid']}})

    token = z.token_for('production')

    def verify_publication(entry):
        manifest = entry['manifest']
        _, local = z.local_state(manifest, 'production')
        need(local is not None, 'Missing saved native state')
        deposit = z.ZenodoClient('production', token).get(local['id'])
        z.validate_record(deposit, local['id'])
        need(deposit['submitted'], 'Record is not published')
        normalizations = z.verify(deposit, entry['metadata'], entry['files'])
        doi = deposit.get('doi') or deposit.get('metadata', {}).get('doi')
        need(doi == entry['record']['doi'], 'Live DOI differs')
        resolution = z.doi_status(doi)
        need(resolution['status'] == 'resolved', 'DOI did not resolve in final audit')
        result = {'pr': entry['pr'], 'id': local['id'], 'doi': doi, 'state': 'published',
                  'title': entry['metadata']['title'], 'whole_reviews': entry['whole_reviews'],
                  'metadata_normalizations': normalizations, 'doi_resolution': resolution,
                  'files': [{'name': f['name'], 'bytes': f['size'], 'sha256': f['sha256']} for f in entry['files']],
                  'live_merge': entry['live_merge']}
        save('NATIVE_AND_MERGE_PR' + str(entry['pr']) + '.json', result)
        print(json.dumps({'final_verified_publication': entry['pr'], 'doi': doi}), flush=True)
        return result

    with ThreadPoolExecutor(max_workers=3) as pool:
        publications = list(pool.map(verify_publication, entries))
    save('LIVE_PUBLICATIONS_AND_EXACT_HEAD_MERGES.json', {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'records': publications, 'github_read': gh_receipt})
    tabs, tab_receipt = command([GWS, 'sheets', 'spreadsheets', 'get', '--params', json.dumps({'spreadsheetId': SHEET, 'fields': 'spreadsheetId,sheets.properties'})], 'FINAL_TRACKER_GID')
    tab = [s['properties'] for s in tabs['sheets'] if s['properties']['sheetId'] == GID]
    need(len(tab) == 1, 'Requested tracker tab missing')
    title = tab[0]['title']
    values, values_receipt = command([GWS, 'sheets', 'spreadsheets', 'values', 'get', '--params', json.dumps({'spreadsheetId': SHEET, 'range': "'" + title.replace("'", "''") + "'!A:D"})], 'FINAL_TRACKER_VALUES')
    rows = values.get('values', [])
    need(rows and rows[0] == ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes'], 'Tracker header drift')
    own = []
    for entry in entries:
        doi = entry['record']['doi']
        matches = [(i + 1, row) for i, row in enumerate(rows) if len(row) > 2 and row[2].removeprefix('https://doi.org/') == doi]
        need(len(matches) == 1 and matches[0][1] == entry['tracker_expected'], 'Final exact unique tracker row: ' + str(entry['pr']))
        own.append({'pr': entry['pr'], 'doi': doi, 'sheet_row': matches[0][0], 'values': matches[0][1], 'exact_unique_row': True})
    save('FINAL_TRACKER_OWN_ROWS_ONLY.json', {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'spreadsheet_id': SHEET, 'gid': GID, 'sheet_title': title, 'own_rows': own, 'read_receipts': [tab_receipt, values_receipt], 'unrelated_rows_not_saved': True})
    audit = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'PASS_FULL_CURRENT_RANGE_COMPLETION_AUDIT',
             'screened_assertions': 101, 'accepted_scoped_results': len(entries), 'excluded_partial_prior': len(excluded),
             'intake_evidence_references_checked': evidence_checked,
             'excluded_current_assertions_unchanged': True, 'all_live_zenodo_metadata_files_dois_verified': True,
             'all_live_exact_head_merge_parents_verified': True, 'all_tracker_rows_unique_and_exact': True,
             'all_minimum_two_complete_reviews_latest_no_actionables': True,
             'priority_novelty_worldwide_openness_certified': False,
             'Luo_Zha_substantive_overlap': 'UNKNOWN_USER_ACCEPTED_NONBLOCKING',
             'no_new_mathematical_reproof_claim': True, 'final_isolated_checkpoint_still_required': True,
             'evidence': ['EXCLUDED_CURRENT_SOURCE_CHECK.json', 'LIVE_PUBLICATIONS_AND_EXACT_HEAD_MERGES.json', 'FINAL_TRACKER_OWN_ROWS_ONLY.json']}
    save('COMPLETION_AUDIT.json', audit)
    print(json.dumps(audit), flush=True)


if __name__ == '__main__':
    main()
