#!/usr/bin/env python3
"""Publish owned research files on remote main without altering shared state."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, tempfile

project = Path(__file__).resolve().parents[1]
repo = project.parent

def git(*args, env=None):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env, text=True).strip()

message = sys.argv[1]
receipt_name = sys.argv[2]
shared_head = git('rev-parse', 'HEAD')
index_path = Path(git('rev-parse', '--path-format=absolute', '--git-path', 'index'))
index_before = hashlib.sha256(index_path.read_bytes()).hexdigest()
owned = git('ls-files', '--cached', '--others', '--exclude-standard', '--', project.name).splitlines()
owned = [x for x in owned if (repo/x).is_file()]
if not owned:
    raise SystemExit('No owned files')
for attempt in range(3):
    git('fetch', 'origin', 'main')
    base = git('rev-parse', 'refs/remotes/origin/main')
    handle, temporary = tempfile.mkstemp(prefix='temporary-index-', dir=project/'receipts')
    os.close(handle)
    os.unlink(temporary)
    env = dict(os.environ, GIT_INDEX_FILE=temporary)
    try:
        git('read-tree', base, env=env)
        git('add', '--', *owned, env=env)
        tree = git('write-tree', env=env)
        if tree == git('rev-parse', base+'^{tree}'):
            commit = base
            break
        commit = git('commit-tree', tree, '-p', base, '-m', message, env=env)
        pushed = subprocess.run(['git','-C',str(repo),'push','origin',commit+':refs/heads/main'], text=True, capture_output=True)
        if pushed.returncode == 0:
            break
        if attempt == 2:
            raise RuntimeError(pushed.stderr)
    finally:
        Path(temporary).unlink(missing_ok=True)
else:
    raise SystemExit('No safe push completed')
head_after = git('rev-parse', 'HEAD')
index_after = hashlib.sha256(index_path.read_bytes()).hexdigest()
remote = git('ls-remote', 'origin', 'refs/heads/main').split()[0]
ancestor = subprocess.run(['git','-C',str(repo),'merge-base','--is-ancestor',commit,remote]).returncode == 0 if remote == commit else None
record = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':commit,'base_remote_main':base,'remote_main_at_verification':remote,'exact_remote_match':remote==commit,'shared_head_before':shared_head,'shared_head_after':head_after,'shared_index_sha256_before':index_before,'shared_index_sha256_after':index_after,'shared_state_preserved':shared_head==head_after and index_before==index_after,'owned_files':owned,'message':message}
(project/'receipts'/receipt_name).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='owned_files'},indent=2))
if not record['shared_state_preserved']:
    raise SystemExit('Concurrent shared HEAD/index change detected; investigate without restoring shared state')
