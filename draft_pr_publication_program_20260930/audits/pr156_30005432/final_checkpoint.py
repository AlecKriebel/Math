"""Prepare factual completion metadata only after the actual original-head merge."""
from pathlib import Path
import datetime, hashlib, importlib.util, json, shutil, sys

A = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('scope156', A / 'prepare_scoped_merge.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def main():
    m.require(len(sys.argv) == 2, 'Pass actual freshly accepted merged MAIN')
    expected = sys.argv[1]
    merge = json.loads((A / 'MERGE_AND_NATIVE_ACCEPTANCE.json').read_text())
    pub = json.loads((A / 'ZENODO_PUBLICATION_READBACK.json').read_text())
    tracker = json.loads((A / 'TRACKER_ACCEPTANCE.json').read_text())
    plan = json.loads((A / 'SCOPED_MERGE_SCOPE_PLAN.json').read_text())
    grant = json.loads((A / 'private/MERGE_WRITER_RETURN.json').read_text())
    m.require(grant['post_merge_fact_only_checkpoint_authorized'], 'Factual completion checkpoint is outside the grant')
    m.require(merge['merge_commit'] == expected and merge['GitHub_PR_state'] == 'MERGED', 'Actual original-head merge required')
    m.require(m.api('git/ref/heads/main')['object']['sha'] == expected, 'MAIN advanced; inspect before preparing metadata')
    pr = m.api('pulls/156')
    m.require(pr['merged'] and pr['head']['sha'] == m.ORIGINAL and pr['merge_commit_sha'] == expected, 'Provider original-head merge changed')
    m.require(pr['body'] == (A / 'PR_BODY_MERGED.md').read_text(), 'Actual final PR body differs')
    m.require(pub['state'] == 'published' and pub['doi'] == tracker['DOI'] and tracker['DOI_count'] == 1, 'Publication/tracker differs')
    parent = m.api('git/commits/' + expected)
    now = datetime.datetime.now(datetime.UTC).isoformat()
    out = A / 'final_checkpoint'
    m.require(not out.exists(), 'Inspect existing completion preparation before replacing it')
    out.mkdir()
    before = A / 'integration_preparation/native_accepted'
    native = A / 'integration_preparation/native_merged'
    m.require(not native.exists(), 'Native final metadata already exists')
    shutil.copytree(before, native)
    readiness = json.loads((native / 'readiness.json').read_text())
    readiness.update({'UTC': now, 'status': 'PUBLISHED_TRACKED_ORIGINAL_HEAD_MERGED', 'merged': True, 'merge_commit': expected, 'case_percent': 100, 'remaining_steps': 'Actual scientific/external steps complete; factual metadata acceptance/readback remains for this preparation.'})
    m.save(native / 'readiness.json', readiness)
    text = (native / 'README.md').read_text()
    m.require('MAIN integration/merge remains pending.' in text, 'Prepared README differs')
    (native / 'README.md').write_text(text.replace('MAIN integration/merge remains pending.', 'Original PR156 head is merged with the current native package and one target QUEUE row. Actual merge: ' + expected + '.'))
    text = (native / 'COUNTEREXAMPLE.md').read_text()
    m.require('Tracker accepted; MAIN integration is pending.' in text, 'Prepared native status differs')
    (native / 'COUNTEREXAMPLE.md').write_text(text.replace('Tracker accepted; MAIN integration is pending.', 'Tracker accepted; original PR156 head merged as ' + expected + '.'))
    with (native / 'RESEARCH_LOG.md').open('a') as handle:
        handle.write('\n' + now + ' — Actual original-head merge ' + expected + ' accepted with all selected native/audit blobs, exact target QUEUE row and provider MERGED state. Science/publication/tracker/merge100%; factual completion metadata checkpoint is being prepared. Priority and independence remain unresolved.\n')
    allowed = {'README.md', 'COUNTEREXAMPLE.md', 'readiness.json', 'RESEARCH_LOG.md'}
    m.require({p.relative_to(native).as_posix() for p in native.rglob('*') if p.is_file()} == {p.relative_to(before).as_posix() for p in before.rglob('*') if p.is_file()}, 'Native inventory changed')
    for path in before.rglob('*'):
        if path.is_file() and path.relative_to(before).as_posix() not in allowed:
            m.require(path.read_bytes() == (native / path.relative_to(before)).read_bytes(), 'Scientific body changed')
    def math_part(text):
        return text.split('## 1.', 1)[1].split('## 6.', 1)[0]
    m.require(math_part((before / 'COUNTEREXAMPLE.md').read_text()) == math_part((native / 'COUNTEREXAMPLE.md').read_text()), 'Proof sections changed')
    pointer = json.loads((A / 'integration_preparation/CURRENT_TEMPLATE.json').read_text())
    pointer.update({'UTC': now, 'current_template': 'native_merged', 'premerge_metadata_template': 'native_accepted', 'MAIN_integration_pending': False, 'merge_commit': expected, 'post_merge_changes': sorted(allowed)})
    m.save(A / 'integration_preparation/CURRENT_TEMPLATE.json', pointer)
    status = json.loads((A / 'CURRENT_CASE_STATUS.json').read_text())
    status.update({'UTC': now, 'status': 'PUBLISHED_TRACKED_ORIGINAL_HEAD_MERGED_FINAL_METADATA_ACCEPTANCE_PENDING', 'merged': True, 'merge_commit': expected, 'case_percent': 100, 'case_workflow_percent': 100, 'publication_cleared': True, 'whole_package_review_round1_ongoing': False, 'whole_package_review_round2_ongoing': False, 'whole_package_reviews_complete': True, 'current_native_template': 'integration_preparation/native_merged', 'fully_completed_count': 31, 'published_count': 18, 'MAIN_window_owner': 'ROOT for the granted fact-only completion checkpoint'})
    m.save(A / 'CURRENT_CASE_STATUS.json', status)
    note = ('\n\n' + now + ' — PR156 original-head merge ' + expected + ' and full selected-body/provider readbacks accepted. Self-contained unrestricted negative answer; known construction ancestry and exact later overlap credited; September30/October11 chronology documented with no historical priority or mutual-independence certificate. Two fresh complete-package reviews clean, final seal-first. Exact publication ' + pub['doi_url'] + ' and one tracker ' + tracker['range'] + ' accepted. All science/external case steps100%; this factual metadata preparation awaits its own actual scoped acceptance. Programme31/dated99=31.31%,18 completed-case publications upon that acceptance; goalactive/incomplete. No157 intake yet.\n')
    with (A / 'RESEARCH_LOG.md').open('a') as handle:
        handle.write(note)
    completion = {'schema': 'audited-pr-workflow-completion/v1', 'UTC': now, 'PR': 156, 'problem_id': 30005432, 'original_head': m.ORIGINAL, 'original_QUEUE_status': 'claimed_solved', 'original_budget': '2/5', 'status': 'ALL_SCIENTIFIC_AND_EXTERNAL_STEPS_ACTUALLY_COMPLETE_FINAL_METADATA_PENDING', 'case_workflow_percent': 100,
                  'mathematics': 'Universal infinite left brace on Z x Z/4Z; complete property-(s) set Z x {0,1}; witness indices2/2 and additive double both infinite; fails additive subgroup/ideal and lambda invariance.',
                  'priority': 'Known finite/semidirect/high-bit ingredients and direct prior-construction implications credited. Exact later Ferudun overlap DOI10.5281/zenodo.23292254 credited; original September30 proof unchanged, later October11 disclosure. Contemporaneous separate disclosures; historical priority and mutual independence unresolved, material publisher gaps disclosed.',
                  'package_review': 'Fresh R1 clean with disclosed initial-summary exposure; new R2 clean with direct-input assessment sealed before prior verdicts. Full package/native/PDF/metadata/negative controls independently checked; ROOT manifests authenticated.',
                  'DOI': pub['doi'], 'Zenodo_record': pub['id'], 'published_title': pub['title'], 'published_files': pub['files'],
                  'GitHub_PR_state': 'MERGED', 'merged_at': merge['merged_at'], 'merge_commit': expected, 'native_files_accepted': merge['native_files_accepted'], 'QUEUE_rows_changed': 1,
                  'tracker_range': tracker['range'], 'tracker_append_requests': tracker['append_requests'], 'tracker_DOI_count': 1, 'tracker_returned_values_and_two_fresh_readbacks_match': True,
                  'persistent_goal_status': 'active', 'persistent_goal_complete': False, 'fully_completed_eligible_count_after_this_case': 31, 'published_count_after_this_case': 18, 'dated_eligible_total': 99, 'next_numeric_intake_cursor': 157,
                  'public_completion_checkpoint': 'This preparation awaits actual scoped nonforce MAIN acceptance and readbacks. Its own future commit and acceptance are not predicted.'}
    m.save(A / 'WORKFLOW_COMPLETION.json', completion)
    prefix = 'draft_pr_publication_program_20260930/'
    j = json.loads(m.body_at(prefix + 'CURRENT_PROGRESS.json', expected))
    m.require(j['fully_completed_count'] == 30 and len(j['fully_completed_eligible_PRs']) == 30 and 156 not in j['fully_completed_eligible_PRs'], 'Completed census differs')
    m.require(j['published_count'] == 18 and len(j['published_PRs']) == 18 and j['published_PRs'].count(156) == 1, 'Actual publication census differs')
    j.setdefault('historical_completed_case_records', []).append({'UTC': now, 'PR': 154, 'fields': {key: value for key, value in j.items() if key.startswith('last_completed_')}, 'note': 'Prior actual completed case retained.'})
    for key in list(j):
        if key.startswith('last_completed_'):
            del j[key]
    j['fully_completed_eligible_PRs'].append(156)
    j.update({'UTC': now, 'updated_UTC': now, 'fully_completed_count': 31, 'fully_completed_fraction_percent': round(3100 / 99, 2), 'workflow_estimate_percent': round(3100 / 99, 2), 'published_count': 18,
              'last_completed_PR': 156, 'last_completed_PR_workflow_percent': 100, 'last_completed_original_head': m.ORIGINAL, 'last_completed_original_budget': '2/5', 'last_completed_original_QUEUE_status': 'claimed_solved',
              'last_completed_mathematical_result_valid': True, 'last_completed_priority_clearance': False, 'last_completed_outcome': 'published_merged_verified_qualified_resolution_priority_unresolved',
              'last_completed_DOI': pub['doi'], 'last_completed_merge_commit': expected, 'last_completed_tracker_range': tracker['range'], 'last_completed_record': 'audits/pr156_30005432/WORKFLOW_COMPLETION.json',
              'last_completed_source_resolution_scope': completion['mathematics'] + ' ' + completion['priority'], 'last_published_PR': 156, 'last_published_DOI': pub['doi'],
              'current_status': 'PUBLISHED_TRACKED_ORIGINAL_HEAD_MERGED_FINAL_METADATA_ACCEPTANCE_PENDING', 'current_PR_workflow_percent': 100, 'current_workflow_estimate_percent': 100,
              'current_Zenodo_published': True, 'current_original_PR_merged': True, 'current_closed': True, 'current_merge_commit': expected, 'current_tracker_updated': True, 'current_publication_disposition_pending': False, 'current_remaining_required_steps': 'All scientific and external steps complete. This factual metadata preparation requires its own actual scope acceptance/readbacks.',
              'current_historical_novelty_or_exclusive_priority_certified': False, 'current_mutual_independence_certified': False,
              'next_numeric_intake_cursor': 157, 'next_eligible_PR_after_current_completion': None, 'next_eligible_order_requires_fresh_status_check': True,
              'remaining_current_step': 'Actual factual completion metadata acceptance and writer release; no scientific or external steps remain for156.',
              'read_only_next_case': {'PR': 156, 'original_literal_status': 'claimed_solved', 'original_head': m.ORIGINAL, 'mathematics_accepted': True, 'case_percent': 100, 'priority_remains_unresolved': True, 'note': 'Original intake case now actually published/tracked/merged; no later PR intake has been performed.'},
              'next_step': 'After actual final metadata acceptance and writer release, continue original-head status-only intake from157, only literal claimed_solved; skip other statuses untouched.',
              'advance_to_next_PR_authorized_now': False, 'persistent_goal_status': 'active', 'persistent_goal_complete': False,
              'workflow_estimate_definition': '31 fully complete eligible cases of preserved dated99 census (31.31%),18 published, conditional on this final metadata acceptance. Priority and independence for156 remain unresolved as disclosed.',
              'program_snapshot_semantics': 'Actual math/package/publication/tracker/original-head merge accepted; this dated metadata preparation requires its own remote acceptance, not a predicted event.',
              'program_snapshot_authority_condition': 'FINAL_CHECKPOINT_ACCEPTANCE.json must show actual MAIN/tree/parent and selected bodies.',
              'active_checkpoint_commit': None, 'active_checkpoint_acceptance_receipt': 'audits/pr156_30005432/FINAL_CHECKPOINT_ACCEPTANCE.json', 'completion_metadata_checkpoint_pending_at_snapshot': True})
    m.save(out / 'CURRENT_PROGRESS.json', j)
    overlay = {prefix + 'CURRENT_PROGRESS.json': out / 'CURRENT_PROGRESS.json'}
    for name in ['CURRENT_PROGRESS.md', 'RESEARCH_LOG.md']:
        path = out / name
        path.write_bytes(m.body_at(prefix + name, expected) + note.encode())
        overlay[prefix + name] = path
    for name in allowed:
        overlay['unsolved_math_prioritization/attempts/30005432/' + name] = native / name
    for name in ['WORKFLOW_COMPLETION.json', 'CURRENT_CASE_STATUS.json', 'RESEARCH_LOG.md', 'MERGE_AND_NATIVE_ACCEPTANCE.json', 'SCOPED_MERGE_PREPARATION.json', 'ROOT_GOAL_ACTIVE_OBSERVATION.json', 'PR_BODY_MERGED.md', 'PR_METADATA_MERGED_ACCEPTANCE.json', 'integration_preparation/CURRENT_TEMPLATE.json']:
        path = A / name
        overlay[path.relative_to(m.C).as_posix()] = path
    m.require(set(overlay) == set(plan['post_merge_fact_only_metadata_scope']), 'Completion paths differ from explicit granted scope')
    pins = {}
    entries = []
    for name, path in sorted(overlay.items()):
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        pins[name] = {'local_path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'git_blob': blob}
        entries.append({'path': name, 'mode': '100644', 'type': 'blob', 'content': data.decode('utf8')})
    tree = m.api('git/trees', 'POST', {'base_tree': parent['tree']['sha'], 'tree': entries})
    anticipated = {name for name, pin in pins.items() if m.lookup(parent['tree']['sha'], name) != ('100644', 'blob', pin['git_blob'])}
    m.require(m.changed_leaves(parent['tree']['sha'], tree['sha']) == anticipated, 'Unselected factual metadata changes')
    for name, pin in pins.items():
        m.require(m.lookup(tree['sha'], name) == ('100644', 'blob', pin['git_blob']), 'Selected completion body differs')
    commit = m.api('git/commits', 'POST', {'message': 'Complete PR156 qualified publication, tracker and original-head merge\n\nAll scientific/external steps actually accepted. Record factual current metadata and programme31/99,18 publications. Historical priority and independence remain unresolved as disclosed. Preserve every other actual MAIN path.', 'tree': tree['sha'], 'parents': [expected]})
    actual = m.api('git/commits/' + commit['sha'])
    m.require(actual['tree']['sha'] == tree['sha'] and [item['sha'] for item in actual['parents']] == [expected], 'Completion commit differs')
    m.require(m.api('git/ref/heads/main')['object']['sha'] == expected, 'MAIN advanced; no stale lease')
    result = {'UTC': datetime.datetime.now(datetime.UTC).isoformat(), 'status': 'SCOPED_FACTUAL_COMPLETION_PREPARED_MAIN_NOT_UPDATED', 'expected_main': expected, 'parent_tree': parent['tree']['sha'], 'tree': tree['sha'], 'commit': commit['sha'], 'selected_files': pins, 'actual_changed_paths': sorted(anticipated), 'all_other_actual_base_tree_paths_preserved': True, 'QUEUE_or_scientific_package_changes': 0, 'fully_completed_count': 31, 'published_count': 18, 'persistent_goal_complete': False}
    m.save(A / 'FINAL_CHECKPOINT_PREPARATION.json', result)
    print(json.dumps({key: result[key] for key in ['status', 'expected_main', 'tree', 'commit', 'fully_completed_count', 'published_count']}))

if __name__ == '__main__':
    main()
