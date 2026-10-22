#!/usr/bin/env python3
"""Verify the credited, range-qualified source-result publication."""
from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent;checks=0
for name in ['SOURCE_RESULT_MANIFEST.json','independent_review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
 m=p/name
 for f in json.loads(m.read_text())['files']:
  d=(m.parent/f['path']).read_bytes();assert len(d)==f['bytes'] and hashlib.sha256(d).hexdigest()==f['sha256'],(name,f['path']);checks+=1
assert hashlib.sha256((p/'SOURCE_RESULT_MANIFEST.json').read_bytes()).hexdigest()=='1751d8a73e2bf9828ebe2f13512406b7e5d5ae80ad837386274767000fc70a20'
assert hashlib.sha256((p/'independent_review/REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='e0afddf9aa4d9fd67d293e00845722da61b0e65f66ed0f99a2b2c1bab5516415'
a=subprocess.check_output([sys.executable,str(p/'verify_known_result.py')],cwd=p);assert a==(p/'KNOWN_RESULT_CHECKS.json').read_bytes()
b=subprocess.check_output([sys.executable,str(p/'independent_review'/'independent_checks.py')],cwd=p);assert b==(p/'independent_review'/'INDEPENDENT_CHECKS.json').read_bytes()
print(json.dumps(dict(status='PASS_CREDITED_STANDARD_RANGE_COROLLARY',digest_checks=checks,author_controls=2652,independent_controls=10659,author_turns=0,range='0<epsilon,delta<1;1<=s<=d<=m'),indent=2,sort_keys=True))
