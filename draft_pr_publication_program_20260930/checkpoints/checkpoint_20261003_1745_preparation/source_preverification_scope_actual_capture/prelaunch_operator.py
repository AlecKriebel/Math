"""Confirmed bounded SOURCE collector only; no Git or native writes."""
import os
import stat
from pathlib import Path
from common import *
from selection import *

P = R / 'draft_pr_publication_program_20260930'
fixed, directories = {}, {}


def addfile(q):
    row = plain_ref(q)
    need(row['path'] not in fixed or fixed[row['path']] == row, 'Different duplicate')
    fixed[row['path']] = row
    return row


def complete(q):
    need(q.is_dir() and not q.is_symlink(), 'Whole selected regular family')
    result = []
    for v in [q] + sorted(q.rglob('*')):
        need(not v.is_symlink(), 'No symlink selected member')
        s = v.lstat()
        if stat.S_ISDIR(s.st_mode):
            rel = str(v.relative_to(R))
            directories[rel] = dict(path=rel, full_mode=stat.S_IMODE(s.st_mode))
        else:
            result.append(addfile(v))
    return result


def parse_mode(value):
    return int(value, 8) if isinstance(value, str) else value


def verify_index(q, marker, expected):
    index = q / marker
    need(digest(index.read_bytes()) == expected, 'Exact existing manifest/index')
    data = load(index)
    rows = data.get('files', data.get('entries'))
    need(rows is not None, 'Known whole-body source rows')
    if isinstance(rows, dict):
        rows = [dict(value, path=name) for name, value in rows.items()]
    declared = set()
    for z in rows:
        name = z.get('path', z.get('name', z.get('relative_path')))
        need(isinstance(name, str), 'Literal indexed member name')
        v = Path(name) if Path(name).is_absolute() else (path(name) if name.startswith('draft_pr_publication_program_20260930/') else q / name)
        need(v.is_relative_to(q) and '..' not in v.parts, 'Indexed member confined to selected family')
        declared.add(v)
        if v == index:
            # This historical original58 manifest includes a designated
            # self row. The exact actual manifest body itself is pinned above.
            continue
        actual = plain_ref(v)
        need(actual['bytes'] == z['bytes'] and actual['sha256'] == z['sha256'], 'Indexed whole body: ' + name)
        mode = z.get('full_mode_07777', z.get('mode_07777', z.get('full_mode', z.get('mode'))))
        if mode is not None:
            need(actual['full_mode'] == parse_mode(mode), 'Indexed full permission bits: ' + name)
        if isinstance(data.get('file_modes'), dict) and name in data['file_modes']:
            need(actual['full_mode'] == parse_mode(data['file_modes'][name]), 'Manifest complete file mode map')
    actual_files = {v for v in q.rglob('*') if v.is_file()}
    # Exact index/READY/self metadata exclusions are historical explicit fixed
    # source metadata, not omitted evidence; every actual file is selected.
    extras = actual_files - declared
    need(extras <= {q / marker, q / 'READY.json', q / 'SELF_MANIFEST.json'}, 'Unknown active file outside existing fixed index: ' + str(extras))
    need(declared <= actual_files, 'No indexed absent file')
    return plain_ref(index)


def main():
    started = now()
    final = (N/'SOURCE_VERIFICATION.json').exists()
    if final:
        need(load(N/'SOURCE_VERIFICATION.json')['status'] == 'PASS_READONLY_SOURCE_CHECKS', 'Genuine earlier SOURCE checks required')
        need((N/'SCOPE_PREVERIFICATION.json').exists(), 'Retain exact inspected earlier scope')
    family_rows = []
    for relative, marker, sha, status, closer, reader in FAMILIES:
        q = P / relative
        index = verify_index(q, marker, sha) if marker else None
        rows = complete(q)
        family_rows.append(dict(root=str(q.relative_to(R)), files=len(rows), bytes=sum(z['bytes'] for z in rows),
                                exact_existing_index=index, existing_custody_stage=status,
                                actual_prior_ROOT_closer_pid=closer, actual_prior_ROOT_reader_pid=reader,
                                new_math_priority_or_ROOT_review_credit=False))
    outside = [addfile(P / n) for n in ROOT_FILES]
    runtime = []
    for n in EXTRA_DIRECTORIES:
        rows = complete(P / n)
        runtime.append(dict(root=str((P/n).relative_to(R)), files=len(rows), bytes=sum(z['bytes'] for z in rows),
                            role='Genuine V5 failed author read-only runtime; no epoch/native output'))
    found = {}
    for a in [P / 'audits/pr45_9900007', P / 'audits/pr48_2961']:
        for q in a.glob('*/CAPTURE.json'):
            m = load(q)
            if m.get('pid') in CAP_PIDS:
                need(m['pid'] not in found, 'Unique named actual CAP')
                found[m['pid']] = (q, m)
    need(set(found) == set(CAP_PIDS), 'All literal named actual ROOT CAPs')
    caps = []
    for pid in CAP_PIDS:
        q, m = found[pid]
        rows = complete(q.parent)
        need({Path(z['path']).name for z in rows} == {'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}, 'Actual whole CAP4 topology')
        need(m['actual_execution'] and m['completed'] and m['operator_unchanged'], 'Actual unchanged completed operator')
        need(m['exit_code'] == (1 if pid in [42224,41530] else 0), 'Truthful actual historical exit')
        need(digest((q.parent/'prelaunch_operator.py').read_bytes()) == m['operator_sha256'], 'Actual prelaunch whole operator')
        for key in ['stdout','stderr']:
            z = plain_ref(q.parent/(key+'.bin'))
            need(z['bytes'] == m[key]['bytes'] and z['sha256'] == m[key]['sha256'], 'Complete actual streams')
        caps.append(dict(root=str(q.parent.relative_to(R)), pid=pid, metadata=plain_ref(q),
                         started_utc=m['started_utc'], finished_utc=m['finished_utc'], exit_code=m['exit_code'],
                         evidence_only_not_approval_of_this_checkpoint=True))
    install = load(found[40952][0].parent / 'stdout.bin')
    need(install['actual_pid'] == 40952 and install['status'] == 'PASS_EXACT_ROOT_V5_SOURCE_INSTALL_ONLY', 'Actual installed source receipt')
    for z in install['files']:
        need(plain_ref(path(z['path'])) == z and z['path'] in fixed, 'All six installed source bytes/modes pinned')
    storage = P / 'storage_compression_20261003'
    storage_sources = [addfile(storage/n) for n in STORAGE_FILES]
    storage_rows, saved = [], 0
    for n in STORAGE_OPERATIONS:
        q = storage / n
        rows = complete(q)
        failed = n == 'pr39-catalog_n_atp_92'
        receipt = load(q/('failure.json' if failed else 'receipt.json'))
        need(digest((q/'helper.prelaunch.py').read_bytes()) == receipt['helper_sha256'] == digest((storage/'compress_completed_v3.py').read_bytes()), 'Actual exact V3 operator')
        pid = receipt['operator_pid']
        need(pid in CAP_PIDS and found[pid][1]['exit_code'] == (1 if failed else 0), 'Actual receipt and ROOT CAP operator identity')
        if failed:
            need(receipt['status'] == 'ABORTED_ORIGINAL_PATH_UNREPLACED' and receipt['source_replaced'] is False and 'saved_allocated_bytes' not in receipt, 'Failed first storage run gives no saving')
        else:
            need(receipt['status'] == 'COMPRESSED' and receipt['source_replaced'] is True, 'Actual successful storage receipt')
            before, after = receipt['before'], receipt['after']
            need(before['sha256'] == after['sha256'], 'Original logical bytes preserved')
            for key in ['st_size','st_mode','st_uid','st_gid','st_mtime_ns']:
                need(before['stat'][key] == after['stat'][key], 'Original full mode/owner/mtime/size preserved')
            need(before['acl_base64'] == after['acl_base64'], 'Original ACL preserved')
            need(all(after['xattrs'].get(k) == v for k,v in before['xattrs'].items()), 'Original xattr values preserved')
            need(receipt['saved_allocated_bytes'] > 0, 'Genuine per-file allocated-block saving')
            saved += receipt['saved_allocated_bytes']
        storage_rows.append(dict(root=str(q.relative_to(R)), actual_receipt=plain_ref(q/('failure.json' if failed else 'receipt.json')),
                                 actual_operator_pid=pid, status=receipt['status'],
                                 saved_allocated_bytes=receipt.get('saved_allocated_bytes'),
                                 allowed_inode_ctime_birthtime_compression_flags_changes_not_misreported=True))
    own = {str(q.relative_to(R)) for q in N.rglob('*') if q.is_file() and q.name != 'RESEARCH_LOG.md' and '__pycache__' not in q.parts}
    # A running SOURCE capture completes its own five actual files after return.
    # This declares only own literal path topology; READY is written only after
    # every real complete stream exists and its body has been checked.
    for q in N.glob('source_*_actual_capture'):
        own |= {str((q/n).relative_to(R)) for n in ['CAPTURE.json','prelaunch_operator.py','prelaunch_common.py','stdout.bin','stderr.bin']}
    own |= {str((N/n).relative_to(R)) for n in ['SCOPE.json','SOURCE_READY.json']}
    forbidden = ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/catalog.json','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.json',
                 str((P/'inventory.json').relative_to(R)),str((P/'review_state.json').relative_to(R)),str((P/'review_history.json').relative_to(R)),str((P/'RESEARCH_LOG.md').relative_to(R)),
                 str((P/'audits/pr48_2961/ROOT_RESEARCH_LOG.md').relative_to(R))]
    need(not set(fixed) & set(forbidden), 'No live native/shared log selection')
    scope = dict(schema='ROOT-exact-owned-research-checkpoint-scope/v1', prepared_utc=now(), actual_collector_pid=os.getpid(),
                 started_utc=started, source_only=True, fixed_files=[fixed[k] for k in sorted(fixed)],
                 fixed_directories=[directories[k] for k in sorted(directories)], completed_fixed_families=family_rows,
                 outside_actual_ROOT_records_and_installed_sources=outside, genuine_failed_V5_runtime=runtime,
                 actual_ROOT_CAP4_sets=caps, storage_V3_sources=storage_sources, storage_V3_actual_operations=storage_rows,
                 total_V3_actual_saved_allocated_bytes=saved,
                 ROOT_log_marker_suffix=ROOT_LOG_MARKER_SUFFIX,
                 runtime_stamped_log_paths=[str((N/'RESEARCH_LOG.md').relative_to(R))],
                 new_preparation_source_paths=sorted(own), forbidden_native_paths=forbidden,
                 exclusions=['outside private primary corpora/cache/giant captured responses','copied temporary Git index bodies and storage target bodies',
                             'outside ROOT preview PNGs','foreign/unrelated chat directories and native state','active PR48V6 and unclosed PR49/46',
                             'shared program and PR48 research logs'],
                 confirmed_scope_from_ROOT='2026-10-03 ROOT message: finalize existing complete evidence; include whole fixed packets plus priority and V5 failed runtime; exclude V6 and active49/46',
                 dated_context=dict(formal_accepted_inventory=FORMAL_INVENTORY, accepted_percent=20.5556,
                                    PR48='Merge and push completed; actual V5 author41530 failed before epoch/native/final roles; recovery pending',
                                    PR57='Final package ROOT-ready, unpublished; original target fixed finite integer plane/sphere; bounded priority',
                                    PR58='already_solved0/5, no paper', PR59='already_solved1/5, no paper',
                                    PR60='Original unsolved1/5, completed SOURCE only; ROOT custody/approval not inferred'),
                 new_math_or_priority_verdict=False, ROOT_review_of_this_SOURCE_not_claimed=True,
                 stage_commit_push_executed=False, native_acceptance_changed=False)
    output = N/('SCOPE.json' if final else 'SCOPE_PREVERIFICATION.json')
    if not final:
        scope['new_preparation_source_paths'].append(str(output.relative_to(R)))
        scope['new_preparation_source_paths'].sort()
    exclusive(output, encoded(scope))
    print(encoded(dict(status='PREPARED_CONFIRMED_SOURCE_SCOPE_ONLY', selected_fixed_files=len(fixed),
                       selected_fixed_directories=len(directories), selected_bytes=sum(v['bytes'] for v in fixed.values()),
                       completed_fixed_families=len(family_rows), exact_actual_ROOT_CAP4_sets=len(caps),
                       storage_V3_saved_allocated_bytes=saved, scope=plain_ref(output), final_scope=final, no_git_calls=True)).decode(), end='')


if __name__ == '__main__':
    main()
