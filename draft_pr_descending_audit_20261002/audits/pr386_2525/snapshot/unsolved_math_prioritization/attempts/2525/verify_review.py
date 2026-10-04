"""Portable additive entry point; Python standard library only."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--sources',type=Path);a=ap.parse_args();d=Path(__file__).resolve().parent;r=d/'final_review'
assert hashlib.sha256((r/'REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='ec4415f6911c0a0f763c901e6b939fd0f906796887144a7fe62c9fb57057a18b'
assert hashlib.sha256((d/'FINAL_FROZEN_MANIFEST.json').read_bytes()).hexdigest()=='1e13e0fd20d6a43f6f3a77ba9e7182cd3777b61786f615000e2ec3fd12627490'
for f in json.loads((r/'REVIEW_MANIFEST.json').read_text())['files']:
 b=(r/f['path']).read_bytes();assert len(b)==f['bytes'];assert hashlib.sha256(b).hexdigest()==f['sha256']
cmd=[sys.executable,str(d/'REPLAY_ALL.py')]
if a.sources:cmd+=['--sources',str(a.sources.resolve())]
v=json.loads(subprocess.check_output(cmd));assert v['author_assertions']==311547 and v['manifest_entries_verified']==156
b=subprocess.check_output([sys.executable,str(r/'independent_check.py')]);assert b==(r/'INDEPENDENT_CHECKS.json').read_bytes();assert json.loads(b)['assertions']==6833
print(json.dumps(dict(review='PASS_SCOPED',author_assertions=311547,independent_assertions=6833,primary_source_pdfs_verified=v['primary_source_pdfs_verified']),sort_keys=True))
