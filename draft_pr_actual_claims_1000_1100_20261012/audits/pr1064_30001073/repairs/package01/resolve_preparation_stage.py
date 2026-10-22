#!/usr/bin/env python3
"""Validate the immutable original 103-output seal through exact before bytes.

Never reinterpret OUTPUT_PINS.json as a seal for the repaired stage. Changed
records resolve to before/preprint_v1_0; unchanged records resolve to the package.
"""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
PACKAGE=AUDIT/'preprint_v1_0'
def require(c,m):
 if not c:raise ValueError(m)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(record):
 old=HERE/'before/preprint_v1_0'/record['path']
 current=PACKAGE/record['path']
 candidate=old if old.exists() else current
 require(candidate.is_file() and not candidate.is_symlink(),'missing preserved-stage record')
 require(candidate.stat().st_size==record['bytes'] and digest(candidate)==record['sha256'],'original-stage pin mismatch '+record['path'])
 return candidate
def main():
 seal=json.loads((PACKAGE/'OUTPUT_PINS.json').read_text())
 require(len(seal['entries'])==103,'original output record count changed')
 require((PACKAGE/'OUTPUT_PINS.json').read_bytes()==(HERE/'before/preprint_v1_0/OUTPUT_PINS.json').read_bytes(),'original output seal changed')
 receipt=[{'path':r['path'],'resolved_path':resolve(r).relative_to(AUDIT).as_posix(),'bytes':r['bytes'],'sha256':r['sha256']} for r in seal['entries']]
 print(json.dumps({'pass':True,'scope':'Original preparation stage only; no repaired-stage implication.','original_output_records':len(receipt),'records':receipt},indent=2))
if __name__=='__main__':main()
