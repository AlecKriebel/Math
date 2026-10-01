#!/usr/bin/python3
"""Read-only reproduction of frozen-head and pinned-cache checks; prints JSON.

Run /usr/bin/python3 reproduce_provenance_checks.py. No file, queue, Git or
database mutation is performed. The network LFS check is separately recorded.
"""
from pathlib import Path
import hashlib
import json
import sqlite3
import subprocess

own = Path(__file__).resolve().parent
repo = own.parents[3]
audit = own.parent
snapshot = audit / 'source_snapshot'
frozen = json.loads((audit / 'snapshot_manifest.json').read_text())
head = frozen['head']
sha = lambda b: hashlib.sha256(b).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


files = []
for entry in frozen['files']:
    relative = entry['path']
    data = (snapshot / relative).read_bytes()
    git_path = 'unsolved_math_prioritization/attempts/30003713/' + relative
    object_data = git('show', head + ':' + git_path)
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert sha(data) == entry['sha256'] and len(data) == entry['bytes']
    assert blob == entry['git_blob_sha1'] and data == object_data
    files.append({'path': relative, 'sha256': sha(data), 'git_blob_sha1': blob})
paths = git('diff', '--name-only', frozen['actual_merge_base'], head).decode().splitlines()
assert paths == frozen['changed_paths'] and len(paths) == 14 and len(files) == 13

queue_root = repo / 'unsolved_math_prioritization'
manifest = json.loads((queue_root / 'manifest.json').read_text())
cached = {}
for name, entry in manifest['files'].items():
    data = (queue_root / 'cache' / name).read_bytes()
    assert sha(data) == entry['sha256'] and len(data) == entry['bytes']
    cached[name] = json.loads(data)
raw_matches = [p for p in cached['problems.json'] if p['id'] == 30003713]
assert len(raw_matches) == 1
source = raw_matches[0]
prior = cached['research_results.json'].get(source['problem_number'], {})
connection = sqlite3.connect('file:'+str(queue_root/'cache/catalog.sqlite')+'?mode=ro', uri=True)
rows = connection.execute('SELECT payload,report FROM records WHERE key=?', ('30003713',)).fetchall()
assert len(rows) == 1 and json.loads(rows[0][0]) == source and json.loads(rows[0][1]) == prior
assert source == json.loads((snapshot / 'source_record.json').read_text()) and prior == {}
context_hash = sha(json.dumps([source,prior], sort_keys=True).encode())
readiness = json.loads((snapshot/'readiness.json').read_text())
assert context_hash == readiness['review_hash']
assert context_hash != sha((snapshot/'review/REVIEW.md').read_bytes())
turns = [json.loads(line) for line in (snapshot/'turns.jsonl').read_text().splitlines() if line]
assert len(turns) == 1 and turns[0]['turn'] == 1
print(json.dumps({'status':'PASS', 'original_head':head, 'files':files,
                  'actual_paths':paths, 'dataset_revision':manifest['revision'],
                  'unique_target':True, 'raw_sqlite_frozen_equal':True,
                  'prior':prior, 'source_context_sha256':context_hash,
                  'math_review_sha256':sha((snapshot/'review/REVIEW.md').read_bytes()),
                  'substantive_attempts':1, 'maximum_substantive_attempts':5}, indent=2))
