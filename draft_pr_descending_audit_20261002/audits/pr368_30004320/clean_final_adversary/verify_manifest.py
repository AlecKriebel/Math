#!/usr/bin/env python3
"""Verify this immutable original independent-audit packet.
Future additive live/post-merge/provenance namespaces are intentionally separate.
"""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
EXCLUDED_DIRS={'final_live','post_merge','provenance_appendix','__pycache__'}
def public(p):
 rel=p.relative_to(HERE)
 return p.is_file() and not any(part.startswith('private_') or part in EXCLUDED_DIRS for part in rel.parts) and str(rel)!='PUBLIC_MANIFEST.json'
def main():
 m=json.loads((HERE/'PUBLIC_MANIFEST.json').read_bytes());actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if public(p)}
 expected={r['path'] for r in m['files']};assert actual==expected,{'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}
 for r in m['files']:
  b=(HERE/r['path']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
 for sealname in ['SOURCE_FIRST_SEAL.json','MATHEMATICAL_SEAL.json']:
  seal=json.loads((HERE/sealname).read_bytes());b=(HERE/seal['file']).read_bytes();assert len(b)==seal['bytes'] and hashlib.sha256(b).hexdigest()==seal['sha256'],sealname
 for r in json.loads((HERE/'FINAL_SEAL.json').read_bytes())['bindings']:
  b=(HERE/r['path']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
 print(json.dumps({'status':'PASS','public_files_bound':len(expected),'original_source_math_final_seals_unchanged':True,'live_acceptance_pending':True},sort_keys=True))
if __name__=='__main__':main()
