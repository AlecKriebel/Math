#!/usr/bin/env python3
"""Finite checks and optional full-input identity replay. This is not a proof checker."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PINNED = {
 'catalog': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
 'problems': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 'reports': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
 'pdf': (432079, '9654af66b347f47df1bc2dd807f1c1950a3afce4f4fe0ece8973fdb4d7d5fa53'),
}
STATEMENT = '583e23540df12cb7c9315490febf0e1d184ede1129d0b813cf2b6b1f275fb725'
PAIR = 'f52f8c63ea451e4c7291492e30ee56ffcb16c96041ddef4e957fec3a642dfa51'

def require(value, message):
    if not value:
        raise ValueError(message)

def digest(b): return hashlib.sha256(b).hexdigest()
def F(n): return n*(n+1)//6
def Q(n,s): return F(n+s)-s*(s+1)//2

def check_partition(edges, parts):
    counts=Counter()
    for part in parts:
        require(len(part)>=2 and len(set(part))==len(part), 'invalid vertex set')
        for e in combinations(sorted(part),2):
            require(e in edges, 'nonedge in clique')
            counts[e]+=1
            require(counts[e]==1, 'overlapping edge')
    require(set(counts)==edges, 'missing edge')
    return True

def book(k,b,s):
    a=k-s
    edges=set(combinations(range(a),2))|{(u,v) for u in range(k) for v in range(k,k+b)}
    triangles=[(i,j,k+(i+j)%a) for i,j in combinations(range(a),2)]
    used={tuple(sorted(e)) for t in triangles for e in combinations(t,2)}
    parts=triangles+[e for e in sorted(edges-used)]
    return edges,parts

def expect_reject(function):
    try:
        function()
    except ValueError:
        return
    raise ValueError('negative control was accepted')

def finite_checks():
    counts={'increment':0,'quadratic_identity':0,'quadratic_maximum':0,'palette_slack':0,'book_partitions':0,'negative_controls':0}
    for n in range(1,5001):
        require(F(n)-F(n-1)==(n+1)//3,'increment identity')
        counts['increment']+=1
    for s in range(9):
        for n in range(181):
            best=None
            for c in range(n+s+2):
                val=c*(n-c)-(c-s)*(c-s-1)//2
                left=24*val
                right=(2*(n+s)+1)**2-12*s*(s+1)-(6*c-2*(n+s)-1)**2
                require(left==right,'square completion')
                counts['quadratic_identity']+=1
                best=val if best is None else max(best,val)
            require(best==Q(n,s),'integer quadratic maximum')
            counts['quadratic_maximum']+=1
    for s in range(1001):
        lam=Fraction(1,100*(s+1));rho=lam/100
        require(8*rho<lam/3 and 4*lam<Fraction(1,6),'palette strictness')
        counts['palette_slack']+=1
    for s in range(5):
        for k in range(s+1,13):
            for b in range(k,21):
                e,p=book(k,b,s)
                check_partition(e,p)
                require(len(p)==k*b-(k-s)*(k-s-1)//2,'book count')
                counts['book_partitions']+=1
    e,p=book(4,7,1)
    for bad in [lambda:check_partition(e,p[:-1]),lambda:check_partition(e,p+[p[0]]),lambda:check_partition(e-{next(iter(e))},p)]:
        expect_reject(bad);counts['negative_controls']+=1
    require(any(F(n)!=n*n//6 for n in range(2,100)), 'linear-term negative control')
    counts['negative_controls']+=1
    return counts

def state_checks():
    st=json.loads((ROOT/'status.json').read_text())
    expected={'problem_id':1917,'problem_number':'EP-81','rank':883,'status':'PRIOR_CLAIM_PENDING_INDEPENDENT_AUDIT','fresh_approaches_used':0,'approach_limit':5,'new_solution_claimed':False,'independent_full_theorem_accepted':False,'queue_edited':False,'publication_performed':False}
    for k,v in expected.items():
        require(type(st[k]) is type(v) and st[k]==v,'status mismatch: '+k)
    pr=json.loads((ROOT/'provenance.json').read_text())
    require(pr['statement_sha256']==STATEMENT and pr['complete_pair_sha256']==PAIR,'identity metadata mismatch')
    require(pr['complete_record_and_report_inspected'] is True and pr['inherited_report_empty'] is True and pr['substantive_inherited_work_found'] is False,'gate metadata mismatch')
    require(len(pr['corpora'])==3,'corpus count')
    for c in pr['corpora']:
        require((c['bytes'],c['sha256'])==PINNED[c['role']],'corpus pin mismatch')
    return 'PASS'

def load_pinned(path,role):
    b=Path(path).read_bytes()
    require((len(b),digest(b))==PINNED[role],role+' bytes/hash mismatch')
    return b

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for role in ['catalog','problems','reports','pdf']:
        parser.add_argument('--'+role,help='Separately supplied '+role+' input; contents are not included in this packet.')
    args=parser.parse_args()
    supplied=[bool(args.catalog),bool(args.problems),bool(args.reports)]
    require(not any(supplied) or all(supplied),'supply all three corpus inputs together')
    result={'status_metadata':state_checks(),'finite_checks':finite_checks(),'complete_corpus_replay':'NOT_RUN','source_pdf_replay':'NOT_RUN','proof_certification':False}
    if all(supplied):
        cat=json.loads(load_pinned(args.catalog,'catalog')); problems=json.loads(load_pinned(args.problems,'problems'));reports=json.loads(load_pinned(args.reports,'reports'))
        require(type(cat) is list and len(cat)==15458 and type(problems) is list and len(problems)==15458 and type(reports) is dict,'corpus structure')
        cs=[x for x in cat if str(x.get('id'))=='1917'];ps=[x for x in problems if x.get('id')==1917]
        require(len(cs)==len(ps)==1,'unique target')
        c=cs[0];p=ps[0];r=reports.get(p['problem_number'],{})
        require(c['rank']==883 and p['problem_number']=='EP-81' and r=={},'target fields')
        require(digest(p['statement'].encode())==STATEMENT,'statement hash')
        require(digest(json.dumps([p,r],sort_keys=True).encode())==PAIR,'complete pair hash')
        result['complete_corpus_replay']='PASS'
    if args.pdf:
        b=load_pinned(args.pdf,'pdf');require(b.startswith(b'%PDF'),'PDF magic')
        result['source_pdf_replay']='PASS'
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
