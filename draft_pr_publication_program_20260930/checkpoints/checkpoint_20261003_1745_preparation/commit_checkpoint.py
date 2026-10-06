"""Proposed exact-parent checkpoint commit with real main compare-and-swap."""
import argparse
import os
from pathlib import Path
from common import *


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--execute', action='store_true', required=True)
    ap.add_argument('--ROOT-personally-read-source', action='store_true', required=True)
    ap.add_argument('--run-name', required=True)
    ap.add_argument('--plan-sha256', required=True)
    args = ap.parse_args()
    need(__debug__, 'No optimized guard execution')
    need(args.run_name.startswith('actual_run_') and args.run_name.replace('_', '').isalnum(), 'Literal runtime name')
    run = N / args.run_name
    need(run.is_dir() and not run.is_symlink(), 'Genuine completed private stage required')
    need(digest((run / 'PLAN.json').read_bytes()) == args.plan_sha256, 'Exact actual staged plan')
    plan = load(run / 'PLAN.json')
    need(plan['schema'] == 'ROOT-exact-owned-private-checkpoint-plan/v1' and plan['checkpoint_committed'] is False, 'Exact pending private plan')
    for key in ['scope', 'source_ready', 'private_index', 'owned_paths_nul']:
        need(plain_ref(path(plan[key]['path'])) == plan[key], 'Actual plan reference changed: ' + key)
    ready = load(N / 'SOURCE_READY.json')
    for z in ready['source_files']:
        need(plain_ref(path(z['path'])) == z, 'Reviewed SOURCE changed')
    scope = load(N / 'SCOPE.json')
    fixed = verify_fixed_scope(scope)
    names = [v['path'] for v in plan['owned_complete_body_modes']]
    expected_names = sorted(fixed | set(plan['included_stamped_logs']) | set(scope['new_preparation_source_paths']))
    need(names == expected_names and not set(names) & set(scope['forbidden_native_paths']), 'Entire exact owned scope')
    need((run / 'OWNED_PATHS.nul').read_bytes() == b''.join(os.fsencode(v) + b'\0' for v in names), 'Whole literal NUL domain')
    for name in plan['absent_optional_logs']:
        need(not path(name).exists() and not path(name).is_symlink(), 'Log domain changed since private stage')
    verify_owned(plan['owned_complete_body_modes'])
    verify_plain_refs(plan['stage_prelaunch_source_refs'])
    commit_prelaunch = source_prelaunch(run, 'commit')
    c = Commands(run / 'commit_commands')
    lock = None
    lock_fd = None
    lock_inode = None
    promoted = False
    published = False
    phase = 'fresh_before_lock'
    try:
        head, gitdir, real_index = repository_gate(c, plan['expected_head'])
        before = protection(c, names, real_index)
        same_protection(plan['foreign_protection_after'], before)
        private = path(plan['private_index']['path'])
        verify_selected_index(c, plan['owned_complete_body_modes'], private)
        need(c.git(['write-tree'], index=private).decode().strip() == plan['proposed_tree'], 'Exact staged tree unchanged')
        space = disk_preflight(real_index)
        lock = gitdir / 'index.lock'
        lock_fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, before['real_index']['full_mode'])
        lock_inode = os.fstat(lock_fd).st_ino
        phase = 'exclusive_real_index_lock'
        # The real index is still untouched. Build a replacement from its exact
        # full original body, changing only the literal selected entries.
        original_index = real_index.read_bytes()
        need(digest(original_index) == before['real_index']['sha256'], 'Index raced lock acquisition')
        reconciled = run / 'RECONCILED_REAL_INDEX'
        exclusive(reconciled, original_index, before['real_index']['full_mode'])
        os.chmod(reconciled, before['real_index']['full_mode'])
        info = b''
        for v in plan['owned_complete_body_modes']:
            mode = '100755' if v['full_mode'] & stat.S_IXUSR else '100644'
            info += (mode + ' ' + v['git_blob_sha1'] + '\t').encode() + os.fsencode(v['path']) + b'\0'
        c.git(['update-index', '-z', '--index-info'], index=reconciled, stdin=info)
        os.chmod(reconciled, before['real_index']['full_mode'])
        summary, _ = index_observation(c, names, index=reconciled)
        need(summary == before['index_summary'], 'Replacement preserves EVERY foreign index entry and flag')
        verify_selected_index(c, plan['owned_complete_body_modes'], reconciled)
        verify_owned(plan['owned_complete_body_modes'])
        same_protection(before, protection(c, names, real_index))
        need(c.git(['rev-parse', 'HEAD']).decode().strip() == head and not (gitdir / 'MERGE_HEAD').exists(), 'Stale HEAD/merge before commit object creation')
        message = b'Checkpoint completed PR48 and PR57-60 research evidence\n\nAdministrative research custody only. Prepared formal accepted snapshot37/180 (20.5556%). The PR57 preprint package remains unpublished. No native mathematical acceptance, DOI or tracker transition by this checkpoint.\n'
        commit = c.git(['commit-tree', plan['proposed_tree'], '-p', head], stdin=message).decode().strip()
        need(len(commit) == 40, 'Exact new unreferenced commit object')
        changed = {os.fsdecode(v) for v in c.git(['diff-tree', '--no-commit-id', '--name-only', '-z', '-r', head, commit]).split(b'\0') if v}
        need(changed and changed <= set(names), 'Entire commit diff is nonempty and exact-owned only')
        commit_body = c.git(['cat-file', '-p', commit])
        headers = commit_body.split(b'\n\n', 1)[0].splitlines()
        need([v for v in headers if v.startswith(b'parent ')] == [('parent ' + head).encode()] and headers[0] == ('tree ' + plan['proposed_tree']).encode(), 'Exact one parent/tree body')
        verify_owned(plan['owned_complete_body_modes'])
        same_protection(before, protection(c, names, real_index))
        replacement = reconciled.read_bytes()
        with os.fdopen(lock_fd, 'wb') as f:
            lock_fd = None
            f.write(replacement)
            f.flush()
            os.fchmod(f.fileno(), before['real_index']['full_mode'])
            os.fsync(f.fileno())
        verify_plain_refs(plan['stage_prelaunch_source_refs'])
        verify_plain_refs(commit_prelaunch)
        phase = 'atomic_main_compare_and_swap'
        # update-ref's old-value comparison is the authority; a child cannot
        # silently adopt a later main as its parent as commit --only could.
        c.git(['update-ref', '-m', 'ROOT exact-owned research checkpoint', 'refs/heads/main', commit, head])
        promoted = True
        phase = 'publish_only_owned_index_entries'
        need(lock.lstat().st_ino == lock_inode and lock.read_bytes() == replacement, 'Exact own index.lock identity')
        os.replace(lock, real_index)
        published = True
        directory_fsync(gitdir)
        need(stat.S_IMODE(real_index.lstat().st_mode) == before['real_index']['full_mode'], 'Real index full mode restored')
        need(c.git(['rev-parse', 'HEAD']).decode().strip() == commit and not (gitdir / 'MERGE_HEAD').exists(), 'Exact actual post-commit main/merge state')
        after = protection(c, names, real_index)
        same_protection(before, after, index_body_may_change=True)
        verify_selected_index(c, plan['owned_complete_body_modes'], real_index)
        verify_owned(plan['owned_complete_body_modes'])
        verify_plain_refs(plan['stage_prelaunch_source_refs'])
        verify_plain_refs(commit_prelaunch)
        receipt = dict(schema='ROOT-exact-owned-actual-research-checkpoint/v1', utc=now(), actual_committer_pid=os.getpid(),
                       status='PASS_LOCAL_EXACT_SCOPE_CHECKPOINT', previous_head=head, commit=commit, tree=plan['proposed_tree'],
                       complete_commit_body=commit_body.decode(), actual_changed_paths=sorted(changed),
                       literal_owned_paths=names, plan=plain_ref(run / 'PLAN.json'),
                       foreign_before=before, foreign_after=after, all_complete_commands=c.records,
                       disk_preflight_before_owned_lock_and_CAS=space,
                       real_index_foreign_entries_flags_staged_blobs_full_worktree_modes_preserved=True,
                       no_native_QUEUE_state_history_inventory_in_scope=True, accepted_inventory_preparation_snapshot='37/180', native_acceptance_changed_by_this_checkpoint=False, stage_prelaunch_source_refs=plan['stage_prelaunch_source_refs'], commit_prelaunch_source_refs=commit_prelaunch,
                       acceptance_or_paper_DOI_tracker_release_approval=False, remote_pushed=False)
        exclusive(run / 'COMMIT_RECEIPT.json', encoded(receipt))
        print(encoded(dict(status=receipt['status'], receipt=plain_ref(run / 'COMMIT_RECEIPT.json'), commit=commit)).decode(), end='')
    except BaseException as exc:
        if lock_fd is not None:
            os.close(lock_fd)
        # An unsuccessful CAS leaves main untouched. Remove only this helper's
        # exclusive lock; preserve its complete replacement in the runtime.
        cas_rejected = phase == 'atomic_main_compare_and_swap' and c.records and c.records[-1]['exit_code'] > 0 and c.records[-1]['error'] is None
        if lock is not None and not published and (not promoted and (phase != 'atomic_main_compare_and_swap' or cas_rejected)):
            if lock.exists() and lock.lstat().st_ino == lock_inode:
                lock.unlink()
        exclusive(run / 'COMMIT_FAILURE.json', encoded(dict(schema='ROOT-checkpoint-actual-commit-failure/v1', utc=now(),
                  actual_pid=os.getpid(), phase=phase, exception=repr(exc), complete_commands=c.records,
                  main_ref_promotion_observed=promoted, real_index_published=published, future_PASS_or_remote_push_claimed=False,
                  promotion_must_be_reconciled_if_CAS_child_did_not_complete_successfully=(phase == 'atomic_main_compare_and_swap' and not cas_rejected and not promoted),
                  retained_own_index_lock=str(lock) if lock is not None and lock.exists() else None)))
        raise


if __name__ == '__main__':
    main()
