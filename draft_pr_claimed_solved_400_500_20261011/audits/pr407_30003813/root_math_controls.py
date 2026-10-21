#!/usr/bin/env python3
"""Independent subset-DP descent numerator versus original-coordinate transfer.
No candidate checker imports. Exact integers; normal and optimized safety identical.
"""
from pathlib import Path
from itertools import product
from math import comb
import json,hashlib,datetime
C=Path(__file__).resolve().parent

def require(v,m):
    if not v:raise RuntimeError(m)

def labels_and_predecessors(signs,reverse=False):
    n=len(signs)+1;pre=[0]*n
    for i,s in enumerate(signs):
        a,b=(i,i+1) if (s=='-')==(i%2==0) else (i+1,i)
        pre[b]|=1<<a
    chosen=0;labels=[0]*n
    for k in range(n):
        available=[v for v in range(n) if not chosen>>v&1 and not pre[v]&~chosen]
        require(available,'cyclic orientation');v=(max if reverse else min)(available);labels[v]=k;chosen|=1<<v
    return labels,pre

def extension_numerator(signs,labels=None):
    canonical,pre=labels_and_predecessors(signs);labels=canonical if labels is None else labels;n=len(labels)
    # States use subsets and last vertex, without enumerating permutation words.
    states=[{} for _ in range(1<<n)];states[0][-1]=[1]+[0]*(n-1)
    for mask in range((1<<n)-1):
        for last,poly in states[mask].items():
            for v in range(n):
                if mask>>v&1 or pre[v]&~mask:continue
                shift=int(last!=-1 and labels[last]>labels[v]);dest=states[mask|1<<v].setdefault(v,[0]*n)
                for d,c in enumerate(poly):
                    if c:require(d+shift<n,'excess degree');dest[d+shift]+=c
    return [sum(p[d] for p in states[-1].values()) for d in range(n)]

def original_count(signs,m):
    counts=[1]*(m+1)
    for s in signs:
        out=[0]*(m+1)
        for a,c in enumerate(counts):
            for b in range(m+1):
                if (a+b<=m if s=='-' else a+b>=m):out[b]+=c
        counts=out
    return sum(counts)

def main():
    receipt=json.loads((C/'SOURCE_RECEIPT.json').read_bytes());before={e['path']:hashlib.sha256((C/'source_snapshot'/e['path']).read_bytes()).hexdigest() for e in receipt['files']}
    require(all(before[e['path']]==e['sha256'] for e in receipt['files']),'frozen source drift')
    patterns,evaluations=0,0;examples={}
    for n in range(1,9):
        for signs in product('-+',repeat=n-1):
            h=extension_numerator(signs);alt,_=labels_and_predecessors(signs,True);require(h==extension_numerator(signs,alt),'natural-label invariance')
            counts=[original_count(signs,m) for m in range(n+4)]
            recovered=[sum((-1)**j*comb(n+1,j)*counts[k-j] for j in range(k+1)) for k in range(n)]
            require(h==recovered,'h-star extraction mismatch');require(h[0]==1,'constant coefficient')
            for m,value in enumerate(counts):
                require(value==sum(c*comb(m+n-d,n) for d,c in enumerate(h) if m>=d),'binomial series mismatch');evaluations+=1
            patterns+=1
            if n<=4:examples[''.join(signs) or '(empty)']=h
    raw=extension_numerator(('--'),list(range(3)));require(raw==[0,2,0],'raw-label negative control')
    require(original_count(('-',),2)==6 and 1-2<0,'wrong T1 dilation negative control')
    after={e['path']:hashlib.sha256((C/'source_snapshot'/e['path']).read_bytes()).hexdigest() for e in receipt['files']};require(before==after,'source mutated')
    r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS_ROOT_INDEPENDENT_SUBSET_DP_CONTROLS','source_head':receipt['head_sha'],'all_frozen_files_unchanged':13,'sign_patterns':patterns,'max_dimension':8,'exact_lattice_evaluations':evaluations,'mechanism':'Subset/last-vertex DP of natural-label linear extensions compared with dense integer original-coordinate transition counts and direct generating-numerator extraction; two labels per sign word. No candidate code imports/permutation enumeration.','negative_controls':2,'examples':examples,'limits':'Finite checks support the independently read all-dimensions reflection/tie-partition proof; no historical-priority finding.','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    p=C/'ROOT_MATH_CONTROLS.json'
    with p.open('x') as f:json.dump(r,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({k:r[k] for k in ['result','sign_patterns','exact_lattice_evaluations','code_sha256']}))
if __name__=='__main__':main()
