"""Check the actual final factual checkpoint without moving any ref."""
from pathlib import Path
import datetime, hashlib, importlib.util, json

A = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('scope170', A / 'prepare_scoped_merge.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def main():
    p = json.loads((A / 'FINAL_CHECKPOINT_PREPARATION.json').read_text())
    m.require(m.api('git/ref/heads/main')['object']['sha'] == p['commit'], 'Final actual MAIN differs')
    actual = m.api('git/commits/' + p['commit'])
    m.require(actual['tree']['sha'] == p['tree'] and [item['sha'] for item in actual['parents']] == [p['expected_main']], 'Actual final tree/parent differs')
    m.require(m.changed_leaves(p['parent_tree'], p['tree']) == set(p['actual_changed_paths']), 'Actual final changed scope differs')
    for name, pin in p['selected_files'].items():
        m.require(m.lookup(p['tree'], name) == ('100644', 'blob', pin['git_blob']), 'Final selected body differs')
        data = Path(pin['local_path']).read_bytes()
        m.require(len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'], 'Local final body changed')
    checks = []
    for name in ['draft_pr_publication_program_20260930/CURRENT_PROGRESS.json', 'draft_pr_publication_program_20260930/audits/pr170_30003480/WORKFLOW_COMPLETION.json', 'unsolved_math_prioritization/attempts/30003480/readiness.json']:
        data = m.body_at(name, p['commit'])
        m.require(hashlib.sha256(data).hexdigest() == p['selected_files'][name]['sha256'], 'Fresh final provider body differs')
        checks.append({'path': name, 'sha256': hashlib.sha256(data).hexdigest()})
    pr = m.api('pulls/170')
    m.require(pr['merged'] and pr['state'] == 'closed' and pr['head']['sha'] == m.ORIGINAL and pr['merge_commit_sha'] == p['expected_main'], 'Provider merged state differs')
    result = {'UTC': datetime.datetime.now(datetime.UTC).isoformat(), 'status': 'ACTUAL_FINAL_FACTUAL_COMPLETION_CHECKPOINT_ACCEPTED', 'PR': 170, 'MAIN': p['commit'], 'tree': p['tree'], 'sole_parent': p['expected_main'], 'merge_commit': pr['merge_commit_sha'], 'selected_files_verified': len(p['selected_files']), 'full_tree_scope_and_selected_blobs_verified': True, 'fresh_provider_body_readbacks': checks, 'QUEUE_or_scientific_package_changes': 0, 'case_percent': 100, 'fully_completed_count': 34, 'published_count': 19, 'dated_eligible_total': 99, 'programme_percent': round(3400 / 99, 2), 'actual_goal_runtime_status_last_read': 'blocked; direct human-authorized work continues', 'persistent_goal_complete': False, 'all_other_actual_base_paths_preserved': True}
    m.require(m.api('git/ref/heads/main')['object']['sha'] == p['commit'], 'MAIN moved during final acceptance')
    m.save(A / 'FINAL_CHECKPOINT_ACCEPTANCE.json', result)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
