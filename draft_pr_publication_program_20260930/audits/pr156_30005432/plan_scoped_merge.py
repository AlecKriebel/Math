"""Freeze an explicit publication/native allowlist before requesting a writer window."""
from pathlib import Path
import datetime, hashlib, json

A = Path(__file__).resolve().parent
C = A.parents[2]

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def main():
    gate = json.loads((A / 'ROOT_PUBLICATION_GATE.json').read_text())
    pub = json.loads((A / 'ZENODO_PUBLICATION_READBACK.json').read_text())
    tracker = json.loads((A / 'TRACKER_ACCEPTANCE.json').read_text())
    require(gate['status'] == 'READY_FOR_AUTHORIZED_PUBLICATION' and gate['fresh_seal_first_review_clean'], 'Scientific publication gate missing')
    require(pub['state'] == 'published' and pub['doi'] == tracker['DOI'] and tracker['DOI_count'] == 1, 'Actual publication/tracker missing')
    names = ['authenticate_r2_and_gate.py', 'ROOT_PUBLICATION_GATE.json', 'ROOT_WHOLE_PACKAGE_R1_AUTHENTICATION.json', 'ROOT_WHOLE_PACKAGE_R2_AUTHENTICATION.json',
             'CURRENT_CASE_STATUS.json', 'RESEARCH_LOG.md', 'PACKAGE_V1_PREPARATION.json', 'NATIVE_PROPOSAL_V1.json',
             'PR_BODY_PROPOSAL_V1.md', 'PR_BODY_ACCEPTED.md', 'PR_METADATA_ACCEPTANCE.json', 'TRACKER_READ_ONLY_PREPARATION.json',
             'ZENODO_PUBLIC_DOWNLOAD_ACCEPTANCE.json', 'verify_publication_files.py', 'ROOT_R2_INITIAL_SEAL_OBSERVATION.json',
             'ZENODO_STAGE_READBACK.json', 'ZENODO_DRAFT_READBACK.json', 'ZENODO_PUBLICATION_RESPONSE.json', 'ZENODO_PUBLICATION_READBACK.json',
             'TRACKER_ACCEPTANCE.json', 'AUDIT_PRIORITY_CHECKPOINT_ACCEPTANCE.json',
             'sheets_tracking/APPEND_REQUEST.json', 'sheets_tracking/APPEND_RESPONSE.json', 'sheets_tracking/ROW_READBACK.json',
             'integration_preparation/CURRENT_TEMPLATE.json', 'zenodo-deposit.v1.json',
             'run_zenodo.py', 'append_tracker.py', 'prepare_accepted_native.py', 'plan_scoped_merge.py', 'prepare_scoped_merge.py', 'accept_scoped_merge.py', 'final_checkpoint.py', 'accept_final_checkpoint.py']
    files = {}
    def add(relative_path, local):
        require(local.is_file() and not local.is_symlink(), 'Missing selected ordinary file: ' + str(local))
        require(not any(part in ['private', 'private_sources', 'scratch', '__pycache__', '.secrets', '.zenodo-state'] for part in Path(relative_path).parts), 'Private/scratch path selected')
        files[relative_path] = local
    for name in names:
        local = A / name
        add(local.relative_to(C).as_posix(), local)
    for family in ['whole_package_r1', 'whole_package_r2']:
        whitelist = A / family / 'PUBLIC_OUTPUT_WHITELIST.json'
        j = json.loads(whitelist.read_text())
        for name in j.get('public_output_whitelist', j.get('allowed_relative_paths', [])):
            local = A / family / name
            add(local.relative_to(C).as_posix(), local)
    package = A / gate['package']
    for local in sorted(package.rglob('*')):
        if local.is_file():
            add(local.relative_to(C).as_posix(), local)
    native = A / 'integration_preparation/native_accepted'
    for local in sorted(native.rglob('*')):
        if local.is_file():
            add('unsolved_math_prioritization/attempts/30005432/' + local.relative_to(native).as_posix(), local)
    pins = {}
    for name, path in sorted(files.items()):
        data = path.read_bytes()
        pins[name] = {'local_path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'git_blob': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()}
    proposal = json.loads((A / 'NATIVE_PROPOSAL_V1.json').read_text())
    native_prefix = 'unsolved_math_prioritization/attempts/30005432/'
    deletions = [native_prefix + name for name in proposal['original_native_paths_to_relocate'] if native_prefix + name not in pins]
    result = {'UTC': datetime.datetime.now(datetime.UTC).isoformat(), 'status': 'FROZEN_REVIEWED_PUBLISHED_NATIVE_MERGE_ALLOWLIST_NO_REMOTE_OBJECTS',
              'PR': 156, 'original_head': 'aec31742f3f26c5b1e533404da57539d17dc94a1', 'selected_files': pins,
              'selected_bytes': sum(item['bytes'] for item in pins.values()), 'conditional_original_native_deletions': deletions,
              'deletion_condition': 'Only if present at actual granted MAIN with exactly the original authenticated blob; all historical originals are preserved in the reviewed native template.',
              'programme_metadata_paths': ['draft_pr_publication_program_20260930/' + name for name in ['CURRENT_PROGRESS.json', 'CURRENT_PROGRESS.md', 'RESEARCH_LOG.md']],
              'QUEUE_path': 'unsolved_math_prioritization/QUEUE.md', 'QUEUE_target_problem_id': 30005432, 'QUEUE_rows_changed': 1,
              'merge_parent_order': ['fresh actual granted MAIN', 'aec31742f3f26c5b1e533404da57539d17dc94a1'],
              'post_merge_fact_only_metadata_scope': ['draft_pr_publication_program_20260930/' + name for name in ['CURRENT_PROGRESS.json', 'CURRENT_PROGRESS.md', 'RESEARCH_LOG.md']] + ['unsolved_math_prioritization/attempts/30005432/' + name for name in ['README.md', 'COUNTEREXAMPLE.md', 'readiness.json', 'RESEARCH_LOG.md']] + [str((A/name).relative_to(C)) for name in ['WORKFLOW_COMPLETION.json', 'CURRENT_CASE_STATUS.json', 'RESEARCH_LOG.md', 'MERGE_AND_NATIVE_ACCEPTANCE.json', 'SCOPED_MERGE_PREPARATION.json', 'ROOT_GOAL_ACTIVE_OBSERVATION.json', 'PR_BODY_MERGED.md', 'PR_METADATA_MERGED_ACCEPTANCE.json', 'integration_preparation/CURRENT_TEMPLATE.json']],
              'DOI': pub['doi'], 'tracker_range': tracker['range'], 'fresh_bounded_writer_grant_required': True,
              'all_other_actual_MAIN_paths_preserved': True, 'historical_priority_or_mutual_independence_certified': False, 'remote_object_or_ref_mutations': False}
    path = A / 'SCOPED_MERGE_SCOPE_PLAN.json'
    require(not path.exists(), 'Inspect and supersede existing scope explicitly rather than replace a granted plan')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'plan': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'selected_paths': len(pins), 'selected_bytes': result['selected_bytes'], 'conditional_deletions': len(deletions), 'programme_paths': 3, 'QUEUE_rows': 1, 'DOI': pub['doi']}))

if __name__ == '__main__':
    main()
