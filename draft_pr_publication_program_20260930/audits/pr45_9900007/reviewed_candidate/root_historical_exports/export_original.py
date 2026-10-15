"""Export exact PR45 Git bodies without changing any branch, index, or native record."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
HEAD = 'd9b4acf5d070d1f04ffac86a4f08916a5629ff16'
BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
PREFIX = 'unsolved_math_prioritization/attempts/9900007/'

def digest(b):
    return hashlib.sha256(b).hexdigest()

def write(p, b):
    assert type(b) is bytes and len(b) < 100 * 1024 * 1024
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())

def js(p, obj):
    write(p, (json.dumps(obj, indent=2, sort_keys=True) + '\n').encode())

def command(label, argv):
    d = A / 'original_git_commands' / label
    d.mkdir(parents=True)
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    p = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    end = dt.datetime.now(dt.timezone.utc).isoformat()
    write(d / 'stdout.bin', out)
    write(d / 'stderr.bin', err)
    js(d / 'CAPTURE.json', {'schema': 'pr45-original-git-command/v1', 'argv': argv, 'cwd': str(R),
       'actual_execution': True, 'pid': p.pid, 'started_utc': start, 'finished_utc': end,
       'completed': True, 'exit_code': p.returncode,
       'stdout': {'path': 'stdout.bin', 'bytes': len(out), 'sha256': digest(out)},
       'stderr': {'path': 'stderr.bin', 'bytes': len(err), 'sha256': digest(err)}})
    assert p.returncode == 0, (label, p.returncode)
    return out

def main():
    source = Path(__file__).read_bytes()
    write(A / 'EXPORT_PRELAUNCH_SOURCE.py', source)
    metadata = json.loads((A / 'github_metadata_actual_capture/stdout.bin').read_bytes())
    api = sum(json.loads((A / 'github_changed_files_actual_capture/stdout.bin').read_bytes()), [])
    assert metadata['number'] == 45 and metadata['state'] == 'open' and metadata['draft'] is True
    assert metadata['head']['sha'] == HEAD and metadata['base']['sha'] == BASE
    assert len(api) == metadata['changed_files'] == 19
    assert command('current_branch', ['git', 'branch', '--show-current']) == b'main\n'
    mb = command('merge_base', ['git', 'merge-base', BASE, HEAD]).decode().strip()
    assert len(mb) == 40
    names = command('changed_paths', ['git', 'diff', '--name-status', '-z', mb, HEAD]).split(b'\0')
    assert names[-1] == b''
    names = names[:-1]
    assert len(names) == 38
    changes = [{'status': names[i].decode(), 'path': names[i+1].decode()} for i in range(0, len(names), 2)]
    assert {r['path'] for r in changes} == {r['filename'] for r in api}
    assert changes[0] == {'status': 'M', 'path': 'unsolved_math_prioritization/QUEUE.md'}
    assert all(r['status'] == 'A' and r['path'].startswith(PREFIX) for r in changes[1:])
    diff = command('whole_diff', ['git', 'diff', '--no-ext-diff', '--no-textconv', '--binary', mb, HEAD, '--'])
    assert diff.count(b'diff --git ') == 19
    write(A / 'original_diff.patch', diff)
    snapshot = A / 'source_snapshot'
    snapshot.mkdir()
    rows = []
    for index, row in enumerate(changes[1:]):
        path = row['path']
        rel = path[len(PREFIX):]
        pp = PurePosixPath(rel)
        assert not pp.is_absolute() and all(x not in ('', '.', '..') for x in pp.parts)
        tree = command('tree_%02d' % index, ['git', 'ls-tree', '-z', HEAD, '--', path])
        assert tree.endswith(b'\0') and tree.count(b'\0') == 1
        meta, literal = tree[:-1].split(b'\t')
        mode, kind, oid = meta.decode().split(' ')
        assert mode == '100644' and kind == 'blob' and literal.decode() == path
        body = command('body_%02d' % index, ['git', 'cat-file', 'blob', HEAD + ':' + path])
        dest = snapshot / rel
        write(dest, body)
        os.chmod(dest, 0o444)
        assert stat.S_IMODE(dest.stat().st_mode) == 0o444
        rows.append({'path': path, 'relative_path': rel, 'git_mode': mode, 'git_object': oid,
                     'bytes': len(body), 'sha256': digest(body), 'snapshot_mode': '0444'})
    queue = command('queue_body', ['git', 'cat-file', 'blob', HEAD + ':unsolved_math_prioritization/QUEUE.md'])
    write(A / 'original_queue_in_head.md', queue)
    matches = [line for line in queue.decode().splitlines() if line.startswith('| 9900007 |')]
    assert len(matches) == 1
    assert '| unsolved |' in matches[0]
    js(A / 'original_pr_metadata.json', {'schema': 'pr45-original-github-and-git-metadata/v1',
       'number': 45, 'problem_id': '9900007', 'head': HEAD, 'github_base': BASE, 'merge_base': mb,
       'original_queue_row': matches[0], 'original_status': 'unsolved', 'github_state': metadata['state'],
       'github_draft': metadata['draft'], 'title': metadata['title'], 'body': metadata['body'],
       'all_changed_paths': changes, 'changed_files': 19,
       'full_diff': {'path': 'original_diff.patch', 'bytes': len(diff), 'sha256': digest(diff)},
       'prepared_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'preparation_pid': os.getpid(),
       'acceptance_verdict': None, 'mathematical_reproduction_performed': False})
    js(A / 'snapshot_manifest.json', {'schema': 'pr45-original-source-snapshot/v1',
       'head': HEAD, 'github_base': BASE, 'merge_base': mb, 'original_files': 18,
       'files': rows, 'complete_18_original_git_bodies': True,
       'whole_repository_diff_files': 19, 'source_claim_validation_completed': False,
       'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_pid': os.getpid()})
    assert Path(__file__).read_bytes() == source
    print(json.dumps({'status': 'PASS_ORIGINAL_EXPORT_ONLY', 'head': HEAD, 'base': BASE, 'merge_base': mb,
       'original_files': len(rows), 'full_diff_bytes': len(diff), 'full_diff_sha256': digest(diff),
       'snapshot_manifest_sha256': digest((A / 'snapshot_manifest.json').read_bytes()),
       'original_queue_row': matches[0]}, sort_keys=True))

if __name__ == '__main__':
    main()
