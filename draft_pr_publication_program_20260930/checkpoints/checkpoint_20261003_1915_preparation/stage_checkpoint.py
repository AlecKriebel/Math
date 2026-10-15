"""Proposed exact-owned PRIVATE-index stage. Does not change real index or HEAD."""
import argparse
import datetime
import os
from pathlib import Path
from common import *


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--execute', action='store_true', required=True)
    ap.add_argument('--ROOT-personally-read-source', action='store_true', required=True)
    ap.add_argument('--scope-sha256', required=True)
    ap.add_argument('--source-ready-sha256', required=True)
    ap.add_argument('--expected-head', required=True)
    ap.add_argument('--log-stamp', required=True)
    ap.add_argument('--run-name', required=True)
    args = ap.parse_args()
    need(__debug__, 'No optimized guard execution')
    need(digest((N / 'SCOPE.json').read_bytes()) == args.scope_sha256, 'Exact ROOT-reviewed scope')
    need(digest((N / 'SOURCE_READY.json').read_bytes()) == args.source_ready_sha256, 'Exact ROOT-reviewed SOURCE handoff')
    ready = load(N / 'SOURCE_READY.json')
    for z in ready['source_files']:
        need(plain_ref(path(z['path'])) == z, 'Reviewed helper/report SOURCE changed')
    scope = load(N / 'SCOPE.json')
    fixed = verify_fixed_scope(scope)
    need(args.run_name.startswith('actual_run_') and args.run_name.replace('_', '').isalnum(), 'New literal local runtime name')
    stamp = datetime.datetime.fromisoformat(args.log_stamp)
    need(stamp.tzinfo is not None and datetime.timedelta(0) <= datetime.datetime.now(datetime.timezone.utc) - stamp <= datetime.timedelta(hours=1), 'Current ROOT-supplied UTC stamp')
    suffix = scope['ROOT_log_marker_suffix']
    need(isinstance(suffix, str) and suffix and '\n' not in suffix and '\r' not in suffix, 'Exact reviewed one-line dated checkpoint context')
    marker = 'Checkpoint 20261003_1915 SOURCE reviewed by ROOT at ' + args.log_stamp + '; ' + suffix
    logs = []
    absent_logs = []
    for name in scope['runtime_stamped_log_paths']:
        q = path(name)
        if q.exists():
            need(q.read_text().splitlines()[-1] == marker, 'ROOT must append the exact current stamp after complete SOURCE review: ' + name)
            prefix = ready['runtime_log_prefix']
            need(prefix['path'] == name and stat.S_IMODE(q.lstat().st_mode) == prefix['full_mode'], 'Dedicated log full mode/path')
            body = q.read_bytes()
            need(digest(body[:prefix['bytes']]) == prefix['sha256'], 'Complete prepared log prefix retained')
            need(body[prefix['bytes']:] == b'\n' + marker.encode() + b'\n', 'Only the exact current ROOT stamp appended')
            logs.append(name)
        else:
            need(not q.is_symlink(), 'Missing log must truly be absent')
            absent_logs.append(name)
    need(scope['runtime_stamped_log_paths'] == [str((N / 'RESEARCH_LOG.md').relative_to(R))], 'Only this dedicated checkpoint log may be stamped')
    need(scope['runtime_stamped_log_paths'][0] in logs, 'Dedicated checkpoint log is required')
    owned_paths = sorted(fixed | set(logs) | set(scope['new_preparation_source_paths']))
    need(not set(owned_paths) & set(scope['forbidden_native_paths']), 'Native state/QUEUE exclusion')
    need(all('\0' not in v and '\n' not in v for v in owned_paths), 'Literal owned path encoding')
    owned = [regular_ref(path(v)) for v in owned_paths]
    run = N / args.run_name
    run.mkdir(exist_ok=False)
    stage_prelaunch = source_prelaunch(run, 'stage')
    nul = b''.join(os.fsencode(v) + b'\0' for v in owned_paths)
    exclusive(run / 'OWNED_PATHS.nul', nul)
    c = Commands(run / 'stage_commands')
    phase = 'before_private_staging'
    try:
        head, gitdir, real_index = repository_gate(c, args.expected_head)
        before = protection(c, owned_paths, real_index)
        space = disk_preflight(real_index, sum(v['bytes'] for v in owned))
        private = run / 'PRIVATE_CHECKPOINT_INDEX'
        c.git(['read-tree', head], index=private)
        # Reject active custom filters/encoding before add; exact literal Git blob
        # identities below also reject any text conversion or unexpected content.
        attrs = c.git(['check-attr', '-z', '--all', '--stdin'], stdin=nul).split(b'\0')
        attrs = [v for v in attrs if v]
        need(len(attrs) % 3 == 0, 'Whole attribute tuple list')
        for i in range(0, len(attrs), 3):
            p, key, value = attrs[i:i+3]
            need(os.fsdecode(p) in owned_paths, 'Attributes outside exact literal scope')
            need(key not in [b'filter', b'working-tree-encoding'] or value in [b'unset', b'unspecified'], 'Active conversion filter needs separately reviewed support')
        phase = 'private_staging'
        c.git(['-c', 'core.autocrlf=false', '-c', 'core.safecrlf=false', '-c', 'core.filemode=true', 'add', '--force',
               '--pathspec-from-file=' + str(run / 'OWNED_PATHS.nul'), '--pathspec-file-nul'], index=private)
        verify_selected_index(c, owned, private)
        tree = c.git(['write-tree'], index=private).decode().strip()
        need(len(tree) == 40, 'Exact proposed tree')
        verify_owned(owned)
        verify_plain_refs(stage_prelaunch)
        repository_gate(c, head)
        after = protection(c, owned_paths, real_index)
        same_protection(before, after)
        phase = 'complete_private_stage_only'
        plan = dict(schema='ROOT-exact-owned-private-checkpoint-plan/v1', utc=now(), actual_stager_pid=os.getpid(),
                    expected_head=head, proposed_tree=tree, private_index=plain_ref(private),
                    owned_paths_nul=plain_ref(run / 'OWNED_PATHS.nul'), owned_complete_body_modes=owned,
                    scope=plain_ref(N / 'SCOPE.json'), source_ready=plain_ref(N / 'SOURCE_READY.json'), stage_prelaunch_source_refs=stage_prelaunch,
                    current_ROOT_log_stamp=args.log_stamp, exact_ROOT_log_marker=marker,
                    included_stamped_logs=logs, absent_optional_logs=absent_logs,
                    foreign_protection_before=before, foreign_protection_after=after,
                    disk_preflight_before_private_staging=space,
                    all_completed_stage_commands=c.records, real_index_unchanged=True, HEAD_unchanged=True,
                    ROOT_acceptance_approval=False, checkpoint_committed=False, remote_pushed=False)
        exclusive(run / 'PLAN.json', encoded(plan))
        print(encoded(dict(status='PASS_PRIVATE_EXACT_SCOPE_STAGE_ONLY', plan=plain_ref(run / 'PLAN.json'),
                           expected_head=head, foreign_staged_count=len(before['foreign_staged']))).decode(), end='')
    except BaseException as exc:
        exclusive(run / 'STAGE_FAILURE.json', encoded(dict(schema='ROOT-checkpoint-actual-stage-failure/v1', utc=now(),
                  actual_pid=os.getpid(), phase=phase, exception=repr(exc), complete_commands=c.records,
                  real_index_or_HEAD_mutation_by_this_stager=False, future_PASS_or_approval=False)))
        raise


if __name__ == '__main__':
    main()
