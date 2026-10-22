#!/usr/bin/env python3
"""Independent finite check using union-find boundary corners, not permutation tracing.
No third-party packages; all validations remain active under Python -O.
"""
from collections import Counter
from itertools import product
import json

def need(ok, message):
    if not ok:
        raise ValueError(message)

# Indexed differently from the author's row-major intersection list.
POINTS = [(i, (i+d)%7) for d in (3, 0, 1) for i in range(6,-1,-1)]
A = [[int((i,j) in POINTS) for j in range(7)] for i in range(7)]
CURVES = [[p for p in POINTS if p[0]==i] for i in range(7)] + [[p for p in POINTS if p[1]==j] for j in range(7)]

def ryser(a):
    """Permanent by inclusion-exclusion over column subsets."""
    n=len(a); ans=0
    for bits in product((0,1),repeat=n):
        v=1
        for row in a:
            v*=sum(x*b for x,b in zip(row,bits))
        ans+=(-1)**(n-sum(bits))*v
    return ans

def bareiss(a):
    """Fraction-free determinant, independently implemented."""
    b=[r[:] for r in a]; previous=1; sign=1; n=len(a)
    for k in range(n-1):
        p=next((j for j in range(k,n) if b[j][k]),None)
        if p is None:return 0
        if p!=k:b[k],b[p]=b[p],b[k];sign=-sign
        pivot=b[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                num=b[i][j]*pivot-b[i][k]*b[k][j]
                need(num%previous==0,'Bareiss nonintegral quotient')
                b[i][j]=num//previous
        for i in range(k+1,n):b[i][k]=0
        previous=pivot
    return sign*b[-1][-1]

def matching_checks():
    matches=[]
    def visit(used,p):
        i=len(p)
        if i==7:
            matches.append(tuple(p));return
        for j in range(7):
            if j not in used and A[i][j]:visit(used|{j},p+[j])
    visit(set(),[])
    signs=Counter();coverage=Counter()
    for p in matches:
        unseen=set(range(7)); c=0
        while unseen:
            x=next(iter(unseen));c+=1
            while x in unseen:unseen.remove(x);x=p[x]
        signs[(-1)**(7-c)]+=1
        coverage.update(enumerate(p))
    need(signs=={1:24} and len(coverage)==21 and set(coverage.values())=={8},'matching check failed')
    return {'matching_count':len(matches),'positive_terms':signs[1],'negative_terms':signs[-1], 'edge_coverage':sorted(set(coverage.values()))}

def corners(signs, orientation=1, curves=CURVES):
    """Each crossing has four corner arcs; each untwisted band joins opposite sides.
    The number of components of this 2-regular graph is the number of boundaries.
    Labels (point,k) denote the corner between outgoing rays k and k+1.
    The rays 0,1,2,3 are alpha+, beta+, alpha-, beta- for orientation +1.
    """
    parent={(p,k):(p,k) for p in POINTS for k in range(4)}
    degree=Counter()
    def root(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    def join(x,y):
        degree[x]+=1;degree[y]+=1
        parent[root(x)]=root(y)
    for n,(triple,sgn) in enumerate(zip(curves,signs)):
        triple=triple if sgn==1 else [triple[0],triple[2],triple[1]]
        ray=(0 if n<7 else 1)*orientation%4
        opposite=(ray+2)%4
        for t,x in enumerate(triple):
            y=triple[(t+1)%3]
            join((x,ray),(y,(opposite-1)%4))
            join((x,(ray-1)%4),(y,opposite))
    need(len(degree)==84 and set(degree.values())=={2},'boundary corner graph is not 2-regular')
    return len({root(v) for v in parent})

def main():
    need(len(set(POINTS))==21 and all(len(c)==3 for c in CURVES),'wrong incidence model')
    det=bareiss(A);per=ryser(A)
    need(det==per==24,'algebra mismatch')
    hist=Counter();reversed_hist=Counter(); genus=Counter()
    for signs in product((1,-1),repeat=14):
        b=corners(signs);br=corners(signs,-1)
        need(b==br,'global orientation reversal changes genus')
        need((23-b)%2==0 and b>0,'Euler failure')
        hist[b]+=1;reversed_hist[br]+=1;genus[(23-b)//2]+=1
    need(dict(hist)=={1:2688,3:11680,5:2016},'wrong histogram')
    need(sum(hist.values())==2**14 and min(genus)==9,'wrong completeness or minimum')
    result={'status':'PASS_INDEPENDENT_RESTRICTED_DIAGNOSTIC','problem_id':2851,'full_problem_solved':False,
      'determinant_by_bareiss':det,'permanent_by_ryser':per,'matching_checks':matching_checks(),
      'boundary_histogram':dict(sorted(hist.items())),'genus_histogram':dict(sorted(genus.items())),
      'cases':sum(hist.values()),'global_orientation_reversed_cases':sum(reversed_hist.values()),
      'all_global_orientation_reversal_pairs_agree':True,'boundary_method':'connected components of an undirected corner-band graph',
      'minimum_genus':min(genus),'dependencies':[]}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
