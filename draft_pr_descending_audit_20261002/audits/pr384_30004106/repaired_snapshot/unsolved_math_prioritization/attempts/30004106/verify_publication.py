#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
bindings=0
for base,name in [(p,'FINAL_AUTHOR_MANIFEST.json'),(p/'review','REVIEW_MANIFEST.json'),(p,'PUBLICATION_MANIFEST.json')]:
 m=json.loads((base/name).read_text())
 for x in m['files']:
  b=(base/x['path']).read_bytes()
  assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
  bindings+=1
out=subprocess.check_output([sys.executable,str(p/'replay_author.py')],cwd=p)
assert out==(p/'AUTHOR_REPLAY.json').read_bytes()
out2=subprocess.check_output([sys.executable,str(p/'review'/'independent_check.py')],cwd=p/'review')
assert out2==(p/'review'/'INDEPENDENT_CHECKS.json').read_bytes()
print(json.dumps({'problem_id':30004106,'status':'unsolved','author_turns':5,'manifest_entries_verified':bindings,'author_exact_assertions':json.loads(out)['total_exact_assertions'],'independent_receipt':json.loads(out2),'all_replays_byte_exact':True},indent=2))
