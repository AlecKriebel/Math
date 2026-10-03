"""Literal PR49 original Git/source export, without executing scientific helpers."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, stat, subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
HEAD = '036a5ed59bee5ed79f08349290481584610f1456'
BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
ID = '30000703'
PREFIX = 'unsolved_math_prioritization/attempts/' + ID + '/'

def sha(body): return hashlib.sha256(body).hexdigest()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def write(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(body); stream.flush(); os.fsync(stream.fileno())
def js(path, value): write(path, (json.dumps(value, indent=2, sort_keys=True) + '\n').encode())

def command(label, argv):
    directory = A / 'original_git_commands' / label
    directory.mkdir(parents=True)
    source = Path(__file__).read_bytes()
    write(directory / 'prelaunch_operator.py', source)
    record = dict(schema='pr49-original-readonly-git-command/v1', argv=argv, cwd=str(R), operator_pid=os.getpid(), operator_sha256=sha(source), started_utc=now(), actual_execution=False, completed=False, pid=None, exit_code=None, stdin_supplied=False)
    js(directory / 'PRELAUNCH.json', record)
    child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate()
    record.update(actual_execution=True, completed=True, pid=child.pid, exit_code=child.returncode, finished_utc=now(), operator_unchanged=Path(__file__).read_bytes() == source)
    for name, body in [('stdout', out), ('stderr', err)]:
        write(directory / (name + '.bin'), body)
        record[name] = dict(path=name + '.bin', bytes=len(body), sha256=sha(body))
    js(directory / 'CAPTURE.json', record)
    for path in directory.iterdir(): os.chmod(path, 0o444)
    assert child.returncode == 0 and record['operator_unchanged'] is True, label
    return out

def tree_parse(body):
    rows = []
    for entry in body.split(b'\0'):
        if not entry: continue
        metadata, path = entry.split(b'\t')
        mode, kind, oid = metadata.decode().split(' ')
        rows.append(dict(path=path.decode(), git_mode=mode, git_kind=kind, git_object=oid))
    return rows

def main():
    source = Path(__file__).read_bytes()
    write(A / 'EXPORT_PRELAUNCH_SOURCE.py', source)
    metadata = json.loads((A / 'github_metadata_actual_capture/stdout.bin').read_bytes())
    api_files = sum(json.loads((A / 'github_changed_files_actual_capture/stdout.bin').read_bytes()), [])
    assert metadata['number'] == 49 and metadata['draft'] is True and metadata['state'] == 'open' and metadata['head']['sha'] == HEAD and metadata['base']['sha'] == BASE
    for item in ['branch', 'head', 'index']:
        assert (A / ('before_fetch_' + item + '_actual_capture/stdout.bin')).read_bytes() == (A / ('after_fetch_' + item + '_actual_capture/stdout.bin')).read_bytes()
    assert command('current_branch', ['git', 'branch', '--show-current']) == b'main\n'
    main_head = command('current_main_head', ['git', 'rev-parse', 'HEAD']).decode().strip()
    merge_base = command('actual_merge_base', ['git', 'merge-base', BASE, HEAD]).decode().strip()
    for label, ref in [('head_commit', HEAD), ('github_base_commit', BASE), ('actual_merge_base_commit', merge_base)]:
        command(label, ['git', 'cat-file', 'commit', ref])
    name_bytes = command('complete_changed_paths', ['git', 'diff', '--name-status', '-z', merge_base, HEAD])
    names = name_bytes.split(b'\0'); assert names.pop() == b'' and len(names) % 2 == 0
    changes = [dict(status=names[i].decode(), path=names[i + 1].decode()) for i in range(0, len(names), 2)]
    assert len(changes) == metadata['changed_files'] == len(api_files) == 17
    assert {row['path'] for row in changes} == {row['filename'] for row in api_files}
    diff = command('complete_diff', ['git', 'diff', '--no-ext-diff', '--no-textconv', '--binary', merge_base, HEAD, '--'])
    write(A / 'original_diff.patch', diff)
    whole_tree_body = command('complete_repository_head_tree', ['git', 'ls-tree', '-r', '-t', '-z', HEAD])
    science_tree_body = command('complete_scientific_tree', ['git', 'ls-tree', '-r', '-t', '-z', HEAD, '--', PREFIX])
    whole_tree = tree_parse(whole_tree_body); science_tree = tree_parse(science_tree_body)
    js(A / 'original_full_tree.json', dict(head=HEAD, whole_repository_entries=whole_tree, scientific_entries=science_tree, whole_repository_tree_bytes=len(whole_tree_body), whole_repository_tree_sha256=sha(whole_tree_body), scientific_tree_bytes=len(science_tree_body), scientific_tree_sha256=sha(science_tree_body)))
    files = []
    queue = None; queue_binding = None
    for index, change in enumerate(changes):
        path = change['path']
        assert change['status'] in ('A', 'M') and (path.startswith(PREFIX) or path == 'unsolved_math_prioritization/QUEUE.md')
        rows = tree_parse(command('file_%02d_tree' % index, ['git', 'ls-tree', '-z', HEAD, '--', path]))
        assert len(rows) == 1 and rows[0]['path'] == path and rows[0]['git_kind'] == 'blob'
        row = rows[0]
        body = command('file_%02d_body' % index, ['git', 'cat-file', 'blob', row['git_object']])
        row.update(bytes=len(body), sha256=sha(body), change_status=change['status'])
        assert next(v['sha'] for v in api_files if v['filename'] == path) == row['git_object']
        if path.startswith(PREFIX):
            relative = path[len(PREFIX):]; pp = PurePosixPath(relative)
            assert relative and not pp.is_absolute() and '..' not in pp.parts
            destination = A / 'source_snapshot' / relative
            write(destination, body); os.chmod(destination, 0o444)
            row.update(relative_path=relative, snapshot_full_mode=stat.S_IMODE(destination.stat().st_mode))
            files.append(row)
        else:
            assert queue is None
            queue = body; queue_binding = row
            write(A / 'original_queue_in_head.md', body)
    assert len(files) == 16 and {row['path'] for row in science_tree if row['git_kind'] == 'blob'} == {row['path'] for row in files}
    queue_rows = [line for line in queue.decode().splitlines() if line.startswith('|') and any(cell.strip() == ID or cell.strip().startswith(ID + ' / ') for cell in line.split('|')[1:-1])]
    assert len(queue_rows) == 1
    js(A / 'original_pr_metadata.json', dict(schema='pr49-original-github-and-git-metadata/v1', number=49, problem_id=ID, url=metadata['html_url'], title=metadata['title'], body=metadata['body'], head=HEAD, github_base=BASE, merge_base=merge_base, observed_main_head=main_head, github_state=metadata['state'], github_draft=metadata['draft'], all_changed_paths=changes, changed_files=len(changes), original_queue_row=queue_rows[0], original_queue_git_binding=queue_binding, full_diff=dict(path='original_diff.patch', bytes=len(diff), sha256=sha(diff)), captured_utc=now(), actual_pid=os.getpid(), acceptance_verdict=None, mathematical_reproduction_performed=False, fetch_changed_local_objects_only=True, branch_head_cached_diff_equal_before_after_fetch=True))
    js(A / 'snapshot_manifest.json', dict(schema='pr49-original-source-snapshot/v1', head=HEAD, github_base=BASE, merge_base=merge_base, files=files, original_files=len(files), scientific_tree_entries=science_tree, whole_repository_diff_files=len(changes), created_utc=now(), actual_pid=os.getpid(), helper_execution_performed=False, acceptance_verdict=None))
    assert Path(__file__).read_bytes() == source
    print(json.dumps(dict(status='ORIGINAL_SOURCE_EXPORT_COMPLETED_ONLY', head=HEAD, github_base=BASE, merge_base=merge_base, observed_main_head=main_head, original_files=len(files), scientific_tree_entries=len(science_tree), whole_repository_tree_entries=len(whole_tree), diff_files=len(changes), diff_bytes=len(diff), diff_sha256=sha(diff), original_queue_row=queue_rows[0], helper_execution_performed=False, acceptance_verdict=None), sort_keys=True))

if __name__ == '__main__': main()
