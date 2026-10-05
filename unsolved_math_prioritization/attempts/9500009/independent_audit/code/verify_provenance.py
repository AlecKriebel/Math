#!/usr/bin/env python3
"""Optional offline provenance replay using separately held complete corpus files.

Usage: python3 code/verify_provenance.py problems.json research_results.json catalog.json
No source text is printed or copied. This does not make a new network request.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def check(condition,message):
    if not condition:raise ValueError(message)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('problems',type=Path)
    parser.add_argument('reports',type=Path)
    parser.add_argument('catalog',type=Path)
    args=parser.parse_args()
    evidence=json.loads((ROOT/'SOURCE_PROVENANCE_AUDIT.json').read_text())
    data={}
    for name,path in [('problems.json',args.problems),('research_results.json',args.reports)]:
        b=path.read_bytes();expected=evidence['dataset']['files'][name]
        check(len(b)==expected['bytes'],'corpus size mismatch: '+name)
        check(hashlib.sha256(b).hexdigest()==expected['sha256'],'corpus hash mismatch: '+name)
        data[name]=json.loads(b)
    b=args.catalog.read_bytes();e=evidence['dataset']['catalog']
    check(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'catalog SHA-256 mismatch')
    check(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha'],
          'catalog Git blob mismatch')
    catalog=json.loads(b)
    selected=[p for p in data['problems.json'] if str(p['id'])=='9500009']
    check(len(selected)==1,'numeric ID not unique');p=selected[0]
    check(sum(x['problem_number']==p['problem_number'] for x in data['problems.json'])==1,
          'prior-report join ambiguous')
    report=data['research_results.json'][p['problem_number']]
    row=next(r for r in catalog if str(r['id'])=='9500009')
    statement=hashlib.sha256(p['statement'].encode()).hexdigest()
    review=hashlib.sha256(json.dumps([p,report],sort_keys=True).encode()).hexdigest()
    check(statement==row['statement_hash']==evidence['dataset']['statement_sha256'],'statement hash')
    check(review==row['review_hash']==evidence['review_hash']['reconstructed'],'review hash')
    print(json.dumps(dict(status='PASS',complete_corpus_hashes_verified=True,
                         statement_sha256=statement,review_sha256=review),indent=2))

if __name__=='__main__':main()
