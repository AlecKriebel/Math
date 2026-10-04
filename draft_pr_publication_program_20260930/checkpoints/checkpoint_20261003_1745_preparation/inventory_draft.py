"""Proposed whole-family inventory in place; no Git, native, or ROOT writes."""
import os
import stat
from common import *
from selection import FAMILIES, ROOT_FILES, CAP_PIDS, STORAGE_FILES, STORAGE_OPERATIONS

P = R / 'draft_pr_publication_program_20260930'


def complete(q):
    files, directories = [], []
    for v in [q] + sorted(q.rglob('*')):
        need(not v.is_symlink(), 'Whole regular family only')
        s = v.lstat()
        if stat.S_ISDIR(s.st_mode):
            directories.append(dict(path=str(v.relative_to(R)), full_mode=stat.S_IMODE(s.st_mode)))
        else:
            files.append(plain_ref(v))
    return dict(root=str(q.relative_to(R)), files=files, directories=directories,
                count=len(files), bytes=sum(v['bytes'] for v in files))


def main():
    started = now()
    families = []
    for relative, marker, sha, status, closer, reader in FAMILIES:
        row = complete(P / relative)
        row.update(declared_custody_status=status, already_actual_ROOT_closer_pid=closer,
                   already_actual_ROOT_separate_reader_pid=reader)
        if marker:
            m = plain_ref(P / relative / marker)
            need(m['sha256'] == sha, 'Exactly named existing source marker')
            row['source_marker'] = m
        families.append(row)
    outside = [plain_ref(P / n) for n in ROOT_FILES]
    found = {}
    for q in (P / 'audits/pr45_9900007').glob('*/CAPTURE.json'):
        m = load(q)
        if m.get('pid') in CAP_PIDS:
            need(m['pid'] not in found, 'Unique actual ROOT capture PID')
            found[m['pid']] = (q, m)
    need(set(found) == set(CAP_PIDS), 'Every named actual capture exists')
    caps = []
    for pid in CAP_PIDS:
        q, m = found[pid]
        row = complete(q.parent)
        need({Path(z['path']).name for z in row['files']} == {'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}, 'Whole exact CAP4')
        need(m['actual_execution'] and m['completed'] and m['operator_unchanged'], 'Actual completed unchanged ROOT operator')
        need(m['exit_code'] == (1 if pid == 42224 else 0), 'Exact genuine historical exit')
        need(digest((q.parent/'prelaunch_operator.py').read_bytes()) == m['operator_sha256'], 'Whole prelaunch operator')
        for key in ['stdout', 'stderr']:
            z = plain_ref(q.parent / (key + '.bin'))
            need(z['bytes'] == m[key]['bytes'] and z['sha256'] == m[key]['sha256'], 'Whole genuine stream')
        row.update(pid=pid, started_utc=m['started_utc'], finished_utc=m['finished_utc'], exit_code=m['exit_code'])
        caps.append(row)
    storage = P / 'storage_compression_20261003'
    storage_sources = [plain_ref(storage / n) for n in STORAGE_FILES]
    operations = [complete(storage / n) for n in STORAGE_OPERATIONS]
    result = dict(schema='checkpoint1745-unfrozen-draft-inventory/v1', actual_collector_pid=os.getpid(),
                  started_utc=started, finished_utc=now(), families=families, outside_ROOT_files=outside,
                  exact_actual_A45_CAP4_sets=caps, storage_sources=storage_sources, storage_operations=operations,
                  final_scope_ROOT_confirmation_pending=True, stage_commit_push_executed=False,
                  no_new_mathematical_review_credit=True, native_SHARED_LOG_or_Git_mutation=False)
    exclusive(N / 'DRAFT_INVENTORY.json', encoded(result))
    print(encoded(dict(status='UNFROZEN_SOURCE_INVENTORY_ONLY', actual_pid=os.getpid(),
                       files=sum(z['count'] for z in families + caps + operations) + len(outside) + len(storage_sources),
                       bytes=sum(z['bytes'] for z in families + caps + operations) + sum(z['bytes'] for z in outside + storage_sources),
                       output=plain_ref(N / 'DRAFT_INVENTORY.json'))).decode(), end='')


if __name__ == '__main__':
    main()
