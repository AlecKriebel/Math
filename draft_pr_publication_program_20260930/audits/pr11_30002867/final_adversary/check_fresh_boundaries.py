#!/usr/bin/env python3
"""Independent exterior-boundary checks from monomial ideals and algebraic inputs.

No candidate/reviewer code is imported. Generic wedge contraction constructs all
Koszul differentials. Expectations for H1 and Hd come from minimal complementary
monomials and maximal staircase monomials, rather than the proposed rank formula.
"""
from datetime import datetime, timezone
from itertools import combinations, product
from pathlib import Path
import json
import sympy as sp
from sympy.polys.matrices import DomainMatrix

HERE=Path(__file__).resolve().parent

def rank(m):
    if not m.rows or not m.cols:
        return 0
    dm=DomainMatrix.from_Matrix(m, extension=True).to_field()
    assert not dm.domain.is_EX
    return dm.rank()

def partitions(n, limit=None):
    if n == 0:
        yield ()
    else:
        for first in range(min(n, n if limit is None else limit), 0, -1):
            for tail in partitions(n-first, first):
                yield (first,)+tail

def quotient(staircase):
    basis=sorted(staircase)
    assert basis
    d=len(basis[0]); N=len(basis); ix={m:i for i,m in enumerate(basis)}
    mats=[sp.zeros(N) for _ in range(d)]; border=set(); maximal=[]
    for j,m in enumerate(basis):
        up=[]
        for i in range(d):
            if m[i]:
                low=tuple(a-(i==k) for k,a in enumerate(m))
                assert low in ix
            new=tuple(a+(i==k) for k,a in enumerate(m))
            up.append(new)
            if new in ix:
                mats[i][ix[new],j]=1
            else:
                border.add(new)
        if all(new not in ix for new in up):
            maximal.append(m)
    minimal=[m for m in border if not any(other != m and
               all(a<=b for a,b in zip(other,m)) for other in border)]
    return mats, len(minimal), len(maximal)

def differentials(mats, point):
    d=len(mats); N=mats[0].rows
    shifted=[m-v*sp.eye(N) for m,v in zip(mats,point)]
    ans=[]
    for k in range(1,d+1):
        low=list(combinations(range(d),k-1)); high=list(combinations(range(d),k))
        dx=sp.zeros(len(low)*N,len(high)*N)
        for col,wedge in enumerate(high):
            for pos,var in enumerate(wedge):
                reduced=wedge[:pos]+wedge[pos+1:]
                row=low.index(reduced)
                dx[row*N:(row+1)*N,col*N:(col+1)*N]=(-1)**pos*shifted[var]
        ans.append(dx)
    for left,right in zip(ans,ans[1:]):
        assert left*right == sp.zeros(left.rows,right.cols)
    ranks=[rank(a) for a in ans]
    homology=[sp.binomial(d,k)*N-(ranks[k-1] if k else 0)-
              (ranks[k] if k<d else 0) for k in range(d+1)]
    return ranks, list(map(int,homology))

def check(name, mats, support):
    d=len(mats); N=mats[0].rows; points=[]
    for point, mu, socle in support:
        ranks,h=differentials(mats,point)
        assert h[0] == 1 and h[1] == mu and h[d] == socle, (name,h,mu,socle)
        assert ranks[0] == N-1
        r2=ranks[1] if d>=2 else 0
        assert mu == (d-1)*N+1-r2
        assert (r2 == (d-1)*(N-1)) == (mu == d)
        if mu == d:
            assert h == [int(sp.binomial(d,k)) for k in range(d+1)]
        points.append({'point':list(map(str,point)), 'ranks':ranks,
                       'homology_dimensions':h, 'independent_local_mu':mu,
                       'independent_socle_dimension':socle})
    outside=tuple(sp.Integer(97+i) for i in range(d))
    _,h=differentials(mats,outside)
    assert h == [0]*(d+1), (name,'outside',h)
    return {'name':name, 'd':d, 'N':N, 'points':points,
            'outside_support_homology':h}

def main():
    results=[]
    for n in range(1,10):
        for widths in partitions(n):
            mats,mu,socle=quotient({(i,j) for j,w in enumerate(widths) for i in range(w)})
            results.append(check('plane_partition_'+str(widths),mats,[((0,0),mu,socle)]))
    cube=list(product(range(2),repeat=3))
    for mask in range(1,1<<len(cube)):
        cells={cube[j] for j in range(len(cube)) if mask&(1<<j)}
        if not all(tuple(a-(i==k) for k,a in enumerate(m)) in cells
                   for m in cells for i,v in enumerate(m) if v):
            continue
        mats,mu,socle=quotient(cells)
        results.append(check('three_variable_lower_cube_'+str(mask),mats,
                             [((0,0,0),mu,socle)]))
    t,mu,socle=quotient({(i,) for i in range(5)})
    nil=t[0]
    curved=[nil,nil**2,nil**3,sp.zeros(5)]
    S=sp.eye(5)
    for i in range(4):
        S[i,i+1]=i+1
    arbitrary=[S*m*S.inv() for m in curved]
    results.append(check('nonminimal_four_coordinates_curved_CI_after_similarity',
                         arbitrary,[((0,0,0,0),4,1)]))
    # Redundant third coordinate must not turn a non-CI quotient into a CI.
    plane,mu,socle=quotient({(0,0),(1,0),(0,1)})
    results.append(check('nonminimal_three_coordinates_nonCI',plane+[sp.zeros(3)],
                         [((0,0,0),4,2)]))
    local,mu,socle=quotient({(0,0),(1,0),(0,1)})
    good,_,_=quotient(set(product(range(2),repeat=2)))
    mixed=[sp.diag(local[i],good[i]+(2,3)[i]*sp.eye(4),sp.Matrix([[(-1,4)[i]]]))
           for i in range(2)]
    results.append(check('three_supports_nilpotent_nonCI_CI_reduced',mixed,
                         [((0,0),3,2),((2,3),2,1),((-1,4),2,1)]))
    candidates=product(*(m.eigenvals().keys() for m in mixed))
    selected=sorted([p for p in candidates if differentials(mixed,p)[0][0]<mixed[0].rows])
    assert selected == [(-1,4),(0,0),(2,3)]
    # Algebraic spectral coordinates challenge rational-only implicit scope.
    companion=sp.Matrix([[0,2],[1,0]])
    results.append(check('algebraic_two_support_univariate', [companion],
                         [((sp.sqrt(2),),1,1),((-sp.sqrt(2),),1,1)]))
    # A noncyclic commuting tuple violates the promised rank at its support.
    bad=[sp.zeros(2),sp.zeros(2)]
    rr,hh=differentials(bad,(0,0))
    assert rr[0] == 0 != 1 and hh[0] == 2
    report={'generated_at':datetime.now(timezone.utc).isoformat(), 'status':'PASS',
            'case_count':len(results), 'cases':results,
            'spectral_cartesian_filter':[[int(v) for v in p] for p in selected],
            'noncyclic_exclusion':{'D1_rank':rr[0],'H0_dimension':hh[0]},
            'scope':'Exact finite boundary checks; global theorem verified by proof and original source.'}
    (HERE/'fresh_boundary_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS',len(results),'fresh ideal-derived boundary cases')

if __name__ == '__main__':
    main()
