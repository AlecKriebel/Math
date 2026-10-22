#!/usr/bin/env python3
"""Seal actual-outcome reconciliation after every publication and readback."""
from pathlib import Path
import datetime, hashlib, json

ROOT = Path(__file__).resolve().parent
EXPECTED = [1205, 1211, 1216, 1225, 1241, 1261, 1262, 1268, 1271, 1274, 1280, 1283]
# These are actual independently verified historical evidence files, selected
# explicitly because the first three cases predate the later receipt format.
MERGE_EVIDENCE = {
    1205: ['publication/MERGE_RECEIPT.json', 'publication/MERGED_TREE_VERIFICATION.json'],
    1211: ['publication/MERGE_RECEIPT.json', 'publication/MERGED_TREE_VERIFICATION.json'],
    1216: ['publication/MERGE_OPERATION.json', 'publication/MERGED_FILES_VERIFICATION.json'],
}

def need(value, message):
    if not value:
        raise RuntimeError(message)

def load(path):
    return json.loads(path.read_text())

def binding(path):
    body = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(body),
            'sha256': hashlib.sha256(body).hexdigest()}

def main():
    folder = ROOT / 'final_scope_refresh'
    destination = folder / 'FINAL_RECONCILIATION.json'
    need(not destination.exists(), 'Preserve final adjudication')
    state = load(ROOT / 'PROGRAM_STATE.json')
    eligibility = load(ROOT / 'FINAL_ELIGIBILITY.json')
    identities = load(folder / 'FINAL_SCOPE_IDENTITY_CHECK.json')
    tracker = load(folder / 'FINAL_TRACKER_RECONCILIATION.json')
    comparison = load(folder / 'FINAL_METADATA_COMPARISON.json')
    original = load(ROOT / 'PR_OUTCOME_METADATA.json')['data']['repository']
    live = load(folder / 'FINAL_LIVE_METADATA.json')['data']['repository']
    need(state['completed_prs'] == state['eligible_prs'] == eligibility['eligible_prs'] == EXPECTED
         and state['current_pr'] is None, 'Scope/completion mismatch')
    need(identities['records'] == 101 and len(identities['completed']) == 12
         and len(identities['skipped']) == 89 and not identities['excluded_drift_prs']
         and not identities['nonempty_activity'], 'Changed excluded outcomes/activity need adjudication')
    need(tracker['status'] == 'PASS' and tracker['completed_publications'] == 12
         and tracker['gid'] == 1254632077, 'Fresh designated-sheet exact12-row readback required')
    need(comparison['changed_body_prs'] == comparison['changed_head_prs'] == EXPECTED,
         'Unexpected live outcome changes')
    need(len({p['doi'] for p in state['publications']}) == 12, 'Distinct12 DOI required')
    skipped = []
    for number in sorted(set(range(1200, 1301)) - set(EXPECTED)):
        before, after = original['p' + str(number)], live['p' + str(number)]
        need(all(before[k] == after[k] for k in ['body', 'headRefOid', 'headRefName', 'updatedAt',
                                                'state', 'isDraft', 'baseRefName']),
             'Excluded metadata drift PR' + str(number))
        need(after['comments']['totalCount'] == after['reviews']['totalCount'] == 0,
             'Activity requires semantic reading')
        prior = next(r for r in eligibility['records'] if r['pr'] == number)
        need(prior['eligible_recommendation'] is False
             and prior['proof_audit_or_priority_research_performed'] is False,
             'Original exclusion inconsistent')
        skipped.append({'pr': number, 'initial_disposition': prior['disposition'],
                        'initial_reason': prior['reason'], 'metadata_and_immutable_head_unchanged': True,
                        'new_comment_review_count': 0, 'initial_exclusion_retained': True,
                        'mathematical_review_repair_publication_or_PR_mutation_performed': False})
    completed = []
    for publication in state['publications']:
        number = publication['pr']
        audit = ROOT / 'audits' / ('pr' + str(number) + '_' + str(publication['problem_id']))
        need(load(audit / 'FINAL_DISPOSITION.json') == publication, 'Saved disposition/state drift')
        need(any(r['pr'] == number and r['doi'] == publication['doi']
                 and r['merge_commit'] == publication['merge_commit'] for r in identities['completed']),
             'Live completion mismatch')
        completed.append({
            'pr': number, 'problem_id': publication['problem_id'], 'doi': publication['doi'],
            'doi_url': publication['doi_url'], 'tracker_range': publication['tracker_range'],
            'reviewed_head': publication['reviewed_head'], 'merge_commit': publication['merge_commit'],
            'disposition': binding(audit / 'FINAL_DISPOSITION.json'),
            'immutable_merge_evidence': [binding(audit / name) for name in
                                         MERGE_EVIDENCE.get(number, ['publication/MERGE_RECEIPT.json'])],
            'publication_receipt': binding(audit / 'publication/PUBLICATION_RECEIPT.json'),
            'public_download_verification': binding(audit / 'publication/PUBLIC_DOWNLOAD_VERIFICATION.json'),
            'final_review_gate': binding(audit / 'publication/FINAL_REVIEW_GATE.json'),
        })
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    report = {
        'schema': 'math-pr1200-1300-final-outcome-reconciliation-v1', 'at_utc': now, 'status': 'PASS',
        'scope': {'first': 1200, 'last': 1300, 'direction': 'ascending',
                  'admission': 'Explicit full original-target claim in actual PR outcome; stale QUEUE.md superseded by human instruction.'},
        'records': 101, 'admitted_and_complete': 12, 'excluded_unchanged': 89,
        'new_outcome_claims': 0, 'actual_comments_and_reviews_total': 0,
        'semantic_adjudication': 'All89 excluded bodies, immutable heads/branches and activity/state/base metadata equal the independently adjudicated initial outcomes. Captured outcome files at those same heads are unchanged. No new activity exists, so initial exclusions stand. No excluded proof, priority audit, repair, merge, close, comment or publication work was performed. All12 admissions now have exact live reviewed heads, MERGED/non-draft/main identities, merge commits and DOI-bearing bodies. Fresh designated-sheet readback verifies all12 exact complete rows with unique DOIs.',
        'evidence': [binding(ROOT / 'FINAL_ELIGIBILITY.json'), binding(ROOT / 'PR_OUTCOME_METADATA.json'),
                     *[binding(folder / name) for name in ['FINAL_LIVE_METADATA.json',
                        'FINAL_METADATA_COMPARISON.json', 'FINAL_SCOPE_IDENTITY_CHECK.json',
                        'FINAL_TRACKER_RECONCILIATION.json']]],
        'completed': completed, 'skipped': skipped,
        'assembly_history': 'Initial root assembly assumed one uniform merge-receipt filename and stopped before writing any final adjudication or completion state when PR1216 used its earlier verified format. Actual historical evidence names are now explicitly selected above; no publication, mathematical or service repair was needed.',
        'scope_limits': 'Accepted exact mathematical targets and attributed results; no firstness/current-worldwide-openness, external human review or formal certification inferred. Per-case source-access, execution and AI/unrefereed qualifications remain in sealed notes/reports.',
        'completion_estimate_percent': 100,
    }
    destination.write_text(json.dumps(report, indent=2) + '\n')
    state.update(status='complete', completion_estimate_percent=100, current_pr_stage='complete',
                 current_pr_completion_estimate_percent=100, remaining_current_pr=[],
                 inventory='Final101 actual-outcome refresh and exact12-row readback PASS; all89 exclusions unchanged',
                 final_reconciliation='final_scope_refresh/FINAL_RECONCILIATION.json',
                 completed_at_utc=now, last_completed_pr=1283)
    if 'current_pr_math_gate_families' in state:
        state['last_completed_pr_math_gate_families'] = state.pop('current_pr_math_gate_families')
    (ROOT / 'PROGRAM_STATE.json').write_text(json.dumps(state, indent=2) + '\n')
    line = ('\n' + now + ' — PROGRAM COMPLETE100% after final101-PR actual-outcome refresh: all12 admitted full original-target claims published with verification packages, tracked and expected-head merged;89 excluded PRs unchanged and no new comment/review outcomes. Fresh designated-gid readback verifies all12 full4cell rows and unique DOIs. All12 saved dispositions equal program/live merge identities. PR1283 DOI10.5281/zenodo.23446275, rowA173:D173, mergec66a617b02217490fcb84682bb8fb25e4c19f0b6. No excluded mathematical processing or other-shard communication. Attribution, extensive AI/unrefereed and source/execution qualifications retained. Final narrow checkpoint and pushed-byte authentication follow. Program estimate100%.\n')
    for path in [ROOT / 'RESEARCH_LOG.md', ROOT / 'audits/pr1283_30005434/RESEARCH_LOG.md']:
        with path.open('a') as stream:
            stream.write(line)
    print(json.dumps({'status': 'complete', 'admitted_and_complete': 12,
                      'skipped_unchanged': 89, 'new_claims': 0, 'estimate': 100}, indent=2))

if __name__ == '__main__':
    main()
