#!/usr/bin/env python3
"""Recheck the pinned complete source files supplied externally, without networking."""
from pathlib import Path
import argparse
import hashlib
import json

parser = argparse.ArgumentParser()
parser.add_argument('--catalog', type=Path, required=True)
parser.add_argument('--problems', type=Path, required=True)
parser.add_argument('--research-results', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
binding = json.loads((root/'SOURCE_BINDING.json').read_text())

def digest(data):
    return hashlib.sha256(data).hexdigest()

def checked(path, want, git=False):
    data = path.read_bytes()
    assert len(data) == want['bytes'] and digest(data) == want['sha256'], path.name
    if git:
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == want['git_blob_sha']
    return json.loads(data)

catalog = checked(args.catalog, binding['catalog'], git=True)
problems = checked(args.problems, binding['dataset']['files']['problems.json'])
reports = checked(args.research_results, binding['dataset']['files']['research_results.json'])
rows = [r for r in catalog if str(r['id']) == str(binding['problem_id'])]
selected = [r for r in problems if str(r['id']) == str(binding['problem_id'])]
assert len(rows) == len(selected) == 1
row, source = rows[0], selected[0]
assert source['problem_number'] == row['problem_number'] == binding['problem_code']
assert sum(r['problem_number'] == binding['problem_code'] for r in problems) == 1
assert binding['problem_code'] not in reports
assert len(problems) == binding['records']['problems']
assert len(reports) == binding['records']['research_results']
assert digest(source['statement'].encode()) == row['statement_hash'] == binding['statement_hash']
assert digest(json.dumps([source, {}], sort_keys=True).encode()) == row['review_hash'] == binding['review_hash']
assert row['rank'] == binding['rank'] and row['turns_used'] == 0
print(json.dumps({'status': 'PASS', 'problem_id': binding['problem_id'],
                  'review_hash': binding['review_hash'], 'complete_files_checked': 3,
                  'live_retrieval_performed': False}))
