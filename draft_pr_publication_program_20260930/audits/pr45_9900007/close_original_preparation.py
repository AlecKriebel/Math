"""Freeze only this preparer's enumerated original-evidence authorship."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat

A = Path(__file__).resolve().parent
ROOT_FILES = [
    'capture_original_command.py', 'export_original.py', 'EXPORT_PRELAUNCH_SOURCE.py',
    'finish_original_export.py', 'FINISH_EXPORT_PRELAUNCH_SOURCE.py',
    'original_diff.patch', 'original_queue_in_head.md', 'original_pr_metadata.json',
    'snapshot_manifest.json', 'inspect_and_inventory_original.py',
    'ORIGINAL_INSPECTION_PRELAUNCH_SOURCE.py', 'ORIGINAL_COMPLETE_READ_RECEIPT.json',
    'ORIGINAL_CLAIM_INVENTORY.md', 'RESEARCH_LOG.md', 'close_original_preparation.py',
    'ORIGINAL_CLOSURE_PRELAUNCH_SOURCE.py']
OWN_DIRS = ['source_snapshot', 'original_git_commands', 'github_metadata_actual_capture',
    'github_changed_files_actual_capture', 'original_head_fetch_actual_capture',
    'original_export_actual_capture', 'original_export_repair_actual_capture',
    'original_full_inspection_actual_capture']

def sha(b):
    return hashlib.sha256(b).hexdigest()

def write(p, b):
    with p.open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())

def verify_capture(d, expected):
    c = json.loads((d / 'CAPTURE.json').read_bytes())
    assert c['actual_execution'] is True and c['completed'] is True
    assert type(c['pid']) is int and c['pid'] > 0 and c['exit_code'] == expected
    assert dt.datetime.fromisoformat(c['started_utc']) < dt.datetime.fromisoformat(c['finished_utc'])
    for field in ('stdout', 'stderr'):
        b = (d / c[field]['path']).read_bytes()
        assert len(b) == c[field]['bytes'] and sha(b) == c[field]['sha256']
    if 'operator_sha256' in c:
        b = (d / 'prelaunch_operator.py').read_bytes()
        assert sha(b) == c['operator_sha256'] and b == (A / 'capture_original_command.py').read_bytes()
        assert c['operator_unchanged'] is True
    return {'path': d.relative_to(A).as_posix() + '/CAPTURE.json', 'pid': c['pid'],
            'exit_code': c['exit_code'], 'started_utc': c['started_utc'], 'finished_utc': c['finished_utc']}

def main():
    source = Path(__file__).read_bytes()
    write(A / 'ORIGINAL_CLOSURE_PRELAUNCH_SOURCE.py', source)
    caps = []
    for name in OWN_DIRS[2:]:
        d = A / name
        assert {p.name for p in d.iterdir()} == {'CAPTURE.json', 'prelaunch_operator.py', 'stdout.bin', 'stderr.bin'}
        caps.append(verify_capture(d, 1 if name == 'original_export_actual_capture' else 0))
    git_dirs = sorted((A / 'original_git_commands').iterdir())
    assert len(git_dirs) == 41 and all(d.is_dir() and not d.is_symlink() for d in git_dirs)
    for d in git_dirs:
        assert {p.name for p in d.iterdir()} == {'CAPTURE.json', 'stdout.bin', 'stderr.bin'}
        caps.append(verify_capture(d, 0))
    m = json.loads((A / 'snapshot_manifest.json').read_bytes())
    assert m['original_files'] == len(m['files']) == 18
    for r in m['files']:
        p = A / 'source_snapshot' / r['relative_path']
        b = p.read_bytes()
        assert r['git_mode'] == '100644' and len(b) == r['bytes'] and sha(b) == r['sha256']
        assert stat.S_IMODE(p.stat().st_mode) == 0o444
    rr = json.loads((A / 'ORIGINAL_COMPLETE_READ_RECEIPT.json').read_bytes())
    assert rr['original_files_read_in_full'] == 18 and rr['all_18_added_hunks_reconstructed_and_byte_exact'] is True
    assert rr['helper_execution_performed'] is False and rr['mathematical_predicates_reproduced'] is False
    assert rr['acceptance_verdict'] is None and rr['fresh_foreign_primary_content_read'] is False
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    with (A / 'RESEARCH_LOG.md').open('a') as f:
        f.write('\n## ' + now + ' — original-evidence self-only closure\n\n')
        f.write('The closure child PID' + str(os.getpid()) + ' verified all47 earlier actual command captures and complete streams, all18 original bodies and the complete read receipt. It freezes only the explicitly enumerated preparer-owned files, leaving independent reviewer folders outside its authorship boundary. Its own outer closure capture is separately retained after child exit and is not retroactively included in an earlier manifest. Original-evidence preparation:100%; this preparer’s independent mathematical audit:0%; new full-problem discovery:0%. No acceptance verdict, replay, primary-source certification, paper, DOI, tracker row, canonical/native mutation, commit or push was performed.\n')
        f.flush()
        os.fsync(f.fileno())
    paths = [A / n for n in ROOT_FILES]
    for name in OWN_DIRS:
        paths.extend(p for p in (A / name).rglob('*') if p.is_file())
    assert len(paths) == len(set(paths))
    rows = []
    for p in sorted(paths):
        assert p.is_file() and not p.is_symlink()
        assert all(not q.is_symlink() for q in [p] + list(p.parents) if q == A or A in q.parents)
        b = p.read_bytes()
        assert len(b) < 100 * 1024 * 1024
        os.chmod(p, 0o444)
        assert stat.S_IMODE(p.stat().st_mode) == 0o444
        rows.append({'path': p.relative_to(A).as_posix(), 'bytes': len(b), 'sha256': sha(b), 'full_mode': 0o444})
    dirs = sorted({p.parent.relative_to(A).as_posix() for p in paths if p.parent != A} |
                  {q.relative_to(A).as_posix() for p in paths for q in p.parents if q != A and A in q.parents})
    rec = {'schema': 'pr45-original-preparation-self-only-manifest/v1', 'created_utc': now,
       'actual_pid': os.getpid(), 'head': m['head'], 'github_base': m['github_base'], 'merge_base': m['merge_base'],
       'original_manifest_sha256': sha((A / 'snapshot_manifest.json').read_bytes()),
       'files_count': len(rows), 'files': rows, 'owned_directories': dirs,
       'authorship_root_files': ROOT_FILES, 'authorship_directory_roots': OWN_DIRS,
       'self_excluded': ['ORIGINAL_PREPARATION_MANIFEST.json'],
       'separately_completed_outer_capture': 'original_preparation_closure_actual_capture',
       'independent_reviewer_sibling_directories_are_not_this_preparers_authorship': True,
       'complete_prior_actual_captures': caps, 'complete_prior_actual_captures_count': len(caps),
       'all_owned_files_full_mode': 0o444, 'no_foreign_primary_bodies_in_authorship': True,
       'source_primary_content_freshly_read': False, 'mathematical_reproduction_performed': False,
       'acceptance_verdict': None, 'original_substantive_turns': 1, 'new_substantive_turns': 0,
       'audit_consumes_turns': 0, 'original_preparation_completion_estimate_percent': 100,
       'independent_mathematical_audit_completion_estimate_percent': 0}
    target = A / 'ORIGINAL_PREPARATION_MANIFEST.json'
    write(target, (json.dumps(rec, indent=2, sort_keys=True) + '\n').encode())
    os.chmod(target, 0o444)
    assert Path(__file__).read_bytes() == source
    for r in rows:
        p = A / r['path']
        b = p.read_bytes()
        assert len(b) == r['bytes'] and sha(b) == r['sha256'] and stat.S_IMODE(p.stat().st_mode) == 0o444
    print(json.dumps({'status': 'PASS_ORIGINAL_PREPARATION_ONLY', 'manifest_bytes': target.stat().st_size,
       'manifest_sha256': sha(target.read_bytes()), 'owned_files': len(rows), 'original_files': 18,
       'prior_actual_captures': len(caps), 'acceptance_verdict': None, 'helper_replays': 0}, sort_keys=True))

if __name__ == '__main__':
    main()
