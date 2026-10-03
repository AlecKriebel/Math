"""Close the complete original export after repairing only the queue-row selector."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat

A = Path(__file__).resolve().parent
HEAD = 'd9b4acf5d070d1f04ffac86a4f08916a5629ff16'
BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
PREFIX = 'unsolved_math_prioritization/attempts/9900007/'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def write(p, b):
    assert len(b) < 100 * 1024 * 1024
    with p.open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())

def js(p, obj):
    write(p, (json.dumps(obj, indent=2, sort_keys=True) + '\n').encode())

def captured(d, argv=None, expected=0):
    c = json.loads((d / 'CAPTURE.json').read_bytes())
    assert c['actual_execution'] is True and c['completed'] is True
    assert type(c['pid']) is int and c['pid'] > 0 and c['exit_code'] == expected
    assert dt.datetime.fromisoformat(c['started_utc']) < dt.datetime.fromisoformat(c['finished_utc'])
    if argv is not None:
        assert c['argv'] == argv
    for field in ('stdout', 'stderr'):
        b = (d / c[field]['path']).read_bytes()
        assert len(b) == c[field]['bytes'] and sha(b) == c[field]['sha256']
    return (d / 'stdout.bin').read_bytes()

def git(label, argv):
    return captured(A / 'original_git_commands' / label, argv)

def main():
    source = Path(__file__).read_bytes()
    write(A / 'FINISH_EXPORT_PRELAUNCH_SOURCE.py', source)
    failure = captured(A / 'original_export_actual_capture',
       ['/usr/bin/python3', '-B', str(A / 'export_original.py')], expected=1)
    assert failure == b''
    assert (A / 'EXPORT_PRELAUNCH_SOURCE.py').read_bytes() == (A / 'export_original.py').read_bytes()
    assert 'assert len(matches) == 1' in (A / 'original_export_actual_capture/stderr.bin').read_text()
    metadata = json.loads(captured(A / 'github_metadata_actual_capture', ['gh', 'api', 'repos/AlecKriebel/Math/pulls/45']))
    api = sum(json.loads(captured(A / 'github_changed_files_actual_capture',
       ['gh', 'api', '--paginate', '--slurp', 'repos/AlecKriebel/Math/pulls/45/files'])), [])
    assert metadata['head']['sha'] == HEAD and metadata['base']['sha'] == BASE
    assert metadata['number'] == 45 and metadata['state'] == 'open' and metadata['draft'] is True
    assert git('current_branch', ['git', 'branch', '--show-current']) == b'main\n'
    mb = git('merge_base', ['git', 'merge-base', BASE, HEAD]).decode().strip()
    names = git('changed_paths', ['git', 'diff', '--name-status', '-z', mb, HEAD]).split(b'\0')
    assert names[-1] == b''
    names = names[:-1]
    assert len(names) == 38
    changes = [{'status': names[i].decode(), 'path': names[i+1].decode()} for i in range(0, len(names), 2)]
    assert len(api) == metadata['changed_files'] == len(changes) == 19
    assert {r['path'] for r in changes} == {r['filename'] for r in api}
    assert changes[0] == {'status': 'M', 'path': 'unsolved_math_prioritization/QUEUE.md'}
    assert all(r['status'] == 'A' and r['path'].startswith(PREFIX) for r in changes[1:])
    diff = git('whole_diff', ['git', 'diff', '--no-ext-diff', '--no-textconv', '--binary', mb, HEAD, '--'])
    assert diff == (A / 'original_diff.patch').read_bytes() and diff.count(b'diff --git ') == 19
    rows = []
    for i, row in enumerate(changes[1:]):
        path = row['path']
        rel = path[len(PREFIX):]
        tree = git('tree_%02d' % i, ['git', 'ls-tree', '-z', HEAD, '--', path])
        assert tree.endswith(b'\0') and tree.count(b'\0') == 1
        head, literal = tree[:-1].split(b'\t')
        mode, kind, oid = head.decode().split(' ')
        assert mode == '100644' and kind == 'blob' and literal.decode() == path
        b = git('body_%02d' % i, ['git', 'cat-file', 'blob', HEAD + ':' + path])
        p = A / 'source_snapshot' / rel
        assert p.read_bytes() == b and not p.is_symlink() and stat.S_IMODE(p.stat().st_mode) == 0o444
        rows.append({'path': path, 'relative_path': rel, 'git_mode': mode, 'git_object': oid,
                     'bytes': len(b), 'sha256': sha(b), 'snapshot_mode': '0444'})
    assert {p.relative_to(A / 'source_snapshot').as_posix() for p in (A / 'source_snapshot').rglob('*') if p.is_file()} == {r['relative_path'] for r in rows}
    queue = git('queue_body', ['git', 'cat-file', 'blob', HEAD + ':unsolved_math_prioritization/QUEUE.md'])
    assert queue == (A / 'original_queue_in_head.md').read_bytes()
    matches = [line for line in queue.decode().splitlines() if '| 9900007 / AMR-098-0007 |' in line]
    assert len(matches) == 1
    cells = [x.strip() for x in matches[0].strip('|').split('|')]
    assert cells[1] == '9900007 / AMR-098-0007' and cells[7] == 'unsolved' and cells[8] == '1/5'
    turns = [json.loads(x) for x in (A / 'source_snapshot/turns.jsonl').read_text().splitlines() if x.strip()]
    assert len(turns) == 1
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    js(A / 'original_pr_metadata.json', {'schema': 'pr45-original-github-and-git-metadata/v1',
       'number': 45, 'problem_id': '9900007', 'head': HEAD, 'github_base': BASE, 'merge_base': mb,
       'original_queue_row': matches[0], 'original_status': 'unsolved', 'original_substantive_turns': 1,
       'github_state': metadata['state'], 'github_draft': metadata['draft'], 'title': metadata['title'],
       'body': metadata['body'], 'all_changed_paths': changes, 'changed_files': 19,
       'full_diff': {'path': 'original_diff.patch', 'bytes': len(diff), 'sha256': sha(diff)},
       'prepared_utc': now, 'preparation_pid': os.getpid(), 'acceptance_verdict': None,
       'mathematical_reproduction_performed': False,
       'export_repair': 'Original export reached all18 bodies; queue selector omitted rank column. Full failed capture preserved; this separate source validates every saved Git command and original body before closing metadata.'})
    js(A / 'snapshot_manifest.json', {'schema': 'pr45-original-source-snapshot/v1',
       'head': HEAD, 'github_base': BASE, 'merge_base': mb, 'original_files': 18, 'files': rows,
       'complete_18_original_git_bodies': True, 'whole_repository_diff_files': 19,
       'source_claim_validation_completed': False, 'created_utc': now, 'actual_pid': os.getpid(),
       'original_substantive_turns': 1, 'new_substantive_turns': 0, 'audit_consumes_turns': 0})
    assert Path(__file__).read_bytes() == source
    print(json.dumps({'status': 'PASS_ORIGINAL_EXPORT_ONLY', 'head': HEAD, 'base': BASE,
       'merge_base': mb, 'original_files': 18, 'original_turns': 1, 'full_diff_bytes': len(diff),
       'full_diff_sha256': sha(diff), 'snapshot_manifest_sha256': sha((A / 'snapshot_manifest.json').read_bytes()),
       'original_queue_row': matches[0]}, sort_keys=True))

if __name__ == '__main__':
    main()
