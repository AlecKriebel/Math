#!/usr/bin/env python3
"""Read-only freeze/replay verification. Default author directory is ../author."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

here=Path(__file__).resolve().parent
author=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else here.parent/'author'
binding=json.loads((here/'FREEZE_BINDING.json').read_text())
expected=binding['author_manifest_expected_sha256']
def sha(data):return hashlib.sha256(data).hexdigest()
assert sha((author/'AUTHOR_MANIFEST.json').read_bytes())==expected
assert {p.name for p in author.iterdir()}=={entry['path'] for entry in binding['files']}
for entry in binding['files']:
    raw=(author/entry['path']).read_bytes()
    assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],entry['path']
manifest=json.loads((author/'AUTHOR_MANIFEST.json').read_text())
for entry in manifest['files']:
    raw=(author/entry['path']).read_bytes()
    assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],entry['path']
for line in (author/'SHA256SUMS').read_text().splitlines():
    digest,name=line.split('  ',1)
    assert sha((author/name).read_bytes())==digest,name
run=subprocess.run([sys.executable,'-B',str(author/'check_controls.py')],capture_output=True,check=True)
assert run.stdout==(author/'CONTROL_RESULTS.json').read_bytes()
assert not run.stderr
author_result=json.loads(run.stdout)
assert author_result['total_assertions']==sum(author_result['groups'].values())==226926
independent=subprocess.run([sys.executable,'-B',str(here/'independent_controls.py')],capture_output=True,check=True)
assert independent.stdout==(here/'INDEPENDENT_RESULTS.json').read_bytes()
assert not independent.stderr
independent_result=json.loads(independent.stdout)
assert independent_result['total_assertions']==sum(independent_result['groups'].values())
# Recheck every original byte after both executions.
for entry in binding['files']:
    raw=(author/entry['path']).read_bytes()
    assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256']
print(json.dumps({'status':'PASS','author_manifest_sha256':expected,
 'author_file_count':len(binding['files']),'author_checks':author_result['total_assertions'],
 'author_output_sha256':sha(run.stdout),'author_replay_byte_identical':True,
 'independent_checks':independent_result['total_assertions'],
 'independent_output_sha256':sha(independent.stdout),'independent_replay_byte_identical':True,
 'negative_controls':len(independent_result['negative_controls']),
 'original_freeze_unchanged_after_execution':True,
 'source_downloads_replayed':False,'geometric_realizations_certified':False},indent=2,sort_keys=True))
