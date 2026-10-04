"""Portable additive entry point, Python standard library only."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--sources',type=Path);a=ap.parse_args();d=Path(__file__).resolve().parent;r=d/'final_review'
assert hashlib.sha256((r/'REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='f356e30ed9d6673d5529f18024f327b445beb612d3f5b303f7e49e27097bd492'
for f in json.loads((r/'REVIEW_MANIFEST.json').read_text())['files']:
 b=(r/f['path']).read_bytes();assert len(b)==f['bytes'];assert hashlib.sha256(b).hexdigest()==f['sha256']
cmd=[sys.executable,str(r/'verify_review.py'),'--author',str(d)]
if a.sources:cmd+=['--sources',str(a.sources.resolve())]
subprocess.run(cmd,check=True)
