"""Authenticate the actual original-head merge and every selected native/audit blob."""
from pathlib import Path
import datetime, hashlib, importlib.util, json

A = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('scope170', A / 'prepare_scoped_merge.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def main():
    p = json.loads((A / 'SCOPED_MERGE_PREPARATION.json').read_text())
    m.require(m.api('git/ref/heads/main')['object']['sha'] == p['commit'], 'Actual MAIN differs')
    actual = m.api('git/commits/' + p['commit'])
    m.require(actual['tree']['sha'] == p['tree'] and [item['sha'] for item in actual['parents']] == [p['expected_main'], p['original_PR_head']], 'Actual merge tree/parents differ')
    m.require(m.changed_leaves(p['parent_tree'], p['tree']) == set(p['actual_changed_paths']), 'Actual changed scope differs')
    for name, pin in p['selected_files'].items():
        m.require(m.lookup(p['tree'], name) == ('100644', 'blob', pin['git_blob']), 'Selected actual blob differs: ' + name)
        data = Path(pin['local_path']).read_bytes()
        m.require(len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'], 'Local selected body changed: ' + name)
    for name in p['conditional_native_deletions_applied']:
        m.require(m.lookup(p['tree'], name) is None, 'Obsolete native body remains')
    pr = m.api('pulls/170')
    m.require(pr['merged'] and pr['state'] == 'closed' and pr['head']['sha'] == p['original_PR_head'] and pr['merge_commit_sha'] == p['commit'], 'Provider original-head merged state not confirmed')
    readbacks = []
    for name in ['unsolved_math_prioritization/QUEUE.md', 'unsolved_math_prioritization/attempts/30003480/COUNTEREXAMPLE.md', 'unsolved_math_prioritization/attempts/30003480/readiness.json', 'unsolved_math_prioritization/attempts/30003480/publication_package/metadata.json', 'draft_pr_publication_program_20260930/CURRENT_PROGRESS.json']:
        data = m.body_at(name, p['commit'])
        m.require(hashlib.sha256(data).hexdigest() == p['selected_files'][name]['sha256'], 'Fresh provider body differs: ' + name)
        readbacks.append({'path': name, 'sha256': hashlib.sha256(data).hexdigest()})
    result = {'UTC': datetime.datetime.now(datetime.UTC).isoformat(), 'status': 'ORIGINAL_HEAD_MERGE_AND_ALL_SELECTED_NATIVE_BODIES_ACCEPTED', 'PR': 170, 'problem_id': 30003480, 'original_head': p['original_PR_head'], 'original_QUEUE_status': 'claimed_solved', 'GitHub_PR_state': 'MERGED', 'merged_at': pr['merged_at'], 'merge_commit': p['commit'], 'tree': p['tree'], 'parents': [p['expected_main'], p['original_PR_head']], 'native_files_accepted': p['native_paths'], 'QUEUE_rows_changed': 1, 'selected_files_verified': len(p['selected_files']), 'all_changed_paths_and_selected_blob_ids_verified': True, 'fresh_provider_body_readbacks': readbacks, 'all_other_actual_base_tree_paths_preserved': True, 'DOI': p['DOI'], 'tracker_range': p['tracker_range'], 'final_completion_metadata_pending': True}
    m.require(m.api('git/ref/heads/main')['object']['sha'] == p['commit'], 'MAIN moved during acceptance')
    m.save(A / 'MERGE_AND_NATIVE_ACCEPTANCE.json', result)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
