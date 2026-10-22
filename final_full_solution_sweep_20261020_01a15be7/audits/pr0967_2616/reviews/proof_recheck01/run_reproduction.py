#!/usr/bin/env python3
"""Recheck snapshot custody; run inspected author harness only from a fresh private copy."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile


def need(ok, msg):
    if not ok:
        raise RuntimeError(msg)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(original, snapshot):
    rows = []
    expected = {r['path'] for r in snapshot['files']}
    actual = {str(p.relative_to(original)) for p in original.rglob('*') if p.is_file()}
    need(actual == expected, 'source snapshot file set mismatch')
    for r in snapshot['files']:
        p = original/r['path']
        need(not p.is_symlink(), 'source symlink')
        b = p.read_bytes()
        sha = digest(b)
        blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
        need(len(b) == r['bytes'] and sha == r['sha256'] and blob == r['git_blob'], 'source custody mismatch')
        rows.append({'path': r['path'], 'bytes': len(b), 'sha256': sha, 'git_blob': blob})
    return rows


def main():
    root = Path(__file__).resolve().parent
    source_root = root.parents[1]
    original = source_root/'original'
    snapshot_path = source_root/'SOURCE_SNAPSHOT.json'
    snapshot = json.loads(snapshot_path.read_bytes())
    before = inventory(original, snapshot)
    # No original script is executed. This complete new copy is the only packet
    # supplied to the author harness. All its temporary writes remain private.
    private = root/'private'
    counter = 1
    while (private/('replay_' + str(counter).zfill(2))).exists():
        counter += 1
    replay = private/('replay_' + str(counter).zfill(2))
    replay.mkdir()
    shutil.copytree(original/'author', replay/'author')
    scratch = replay/'scratch'
    scratch.mkdir()
    pin = '31bd2aed10d96d5ada5344531e2207dd4388c8cb1328e3c448ac89be5b78ec8c'
    for path in (replay/'author').rglob('*'):
        if path.is_file():
            relative = str(path.relative_to(replay))
            need(digest(path.read_bytes()) == next(r['sha256'] for r in before if r['path'] == relative),
                 'copied source mismatch')
    env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
    cmd = [sys.executable, '-I', '-S', '-B', str(replay/'author/external/test_harness.py'),
           str(replay/'author/public'), str(replay/'author/external'), pin]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc = subprocess.run(cmd, cwd=replay, env=env, capture_output=True, timeout=180)
    completed = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (replay/'harness_stdout.json').write_bytes(proc.stdout)
    (replay/'harness_stderr.txt').write_bytes(proc.stderr)
    need(proc.returncode == 0 and not proc.stderr, 'author harness rerun failed')
    result = json.loads(proc.stdout)
    need(result['ok'] is True and result['all_original_hashes_unchanged'] is True, 'harness receipt failure')
    need(os.getuid() == os.geteuid() != 0, 'nonroot execution required')
    (root/'AUTHOR_HARNESS_RERUN.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    archive = original/'expansive_group_2616_frozen.tar.gz'
    members = []
    with tarfile.open(archive, mode='r:gz') as tf:
        for member in tf.getmembers():
            need(member.name not in {m['name'] for m in members}, 'duplicate archive member')
            need(member.isdir() or member.isfile(), 'unsafe archive type')
            if member.isfile():
                body = tf.extractfile(member).read()
                path = original/'author'/member.name
                need(path.is_file() and path.read_bytes() == body, 'archive body mismatch')
                members.append({'name': member.name, 'kind': 'file', 'bytes': len(body), 'sha256': digest(body)})
            else:
                need(member.name in {'public','external'}, 'unexpected archive directory')
                members.append({'name': member.name, 'kind': 'directory'})
    need({m['name'] for m in members if m['kind'] == 'file'} ==
         {str(p.relative_to(original/'author')) for p in (original/'author').rglob('*') if p.is_file()},
         'archive member set mismatch')
    after = inventory(original, snapshot)
    need(before == after, 'original source changed')
    custody = {'status': 'PASS', 'head_claim_in_supplied_snapshot': snapshot['head'],
               'snapshot_bytes': snapshot_path.stat().st_size, 'snapshot_sha256': digest(snapshot_path.read_bytes()),
               'original_files_before_and_after': before, 'original_unchanged': True,
               'archive_members': members, 'copy_and_harness_started_utc': started,
               'copy_and_harness_completed_utc': completed, 'harness_returncode': proc.returncode,
               'harness_execution_copy': str(replay.relative_to(root)),
               'interpreter': sys.executable, 'python_version': sys.version,
               'uid': os.getuid(), 'euid': os.geteuid(), 'harness_command': cmd,
               'temporary_directory': str(scratch),
               'limits': 'Locally checks supplied immutable snapshot against sizes, SHA256 and Git blob IDs; no fresh GitHub API authentication or publication checker execution is claimed.'}
    (root/'CUSTODY.json').write_text(json.dumps(custody, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': 'PASS', 'source_files_unchanged': len(before),
                      'archive_regular_files': sum(m['kind'] == 'file' for m in members),
                      'harness_modes': [r['mode'] for r in result['reports']],
                      'harness_optimization_input_rejections_per_mode': [len(r['hostile_fixtures_rejected']) for r in result['reports']],
                      'harness_packet_manifest_controls': len(result['tamper_controls_rejected_in_all_modes'])}, indent=2))


if __name__ == '__main__':
    main()
