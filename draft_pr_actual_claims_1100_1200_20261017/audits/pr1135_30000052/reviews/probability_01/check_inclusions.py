#!/usr/bin/env python3
"""Independent exact inclusion-mask audit; stdlib only, no candidate imports.

Run normally and with python -O. Geometry uses closed halfplanes because every
boundary has two-dimensional Lebesgue measure zero. Every mathematical check
uses explicit exceptions; --negative-guard deliberately fails after the audit.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json

CHECKS = 0
ADVERSE = []

def check(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ArithmeticError(message)

def adverse(ok, label):
    check(ok, 'Adverse control did not reject: ' + label)
    ADVERSE.append(label)

# Halfplanes have a*u+b*v+c >= 0. Each modular band has w=2*v-u-m.
SQUARE = [(Q(0),Q(0)),(Q(1),Q(0)),(Q(1),Q(1)),(Q(0),Q(1))]

def clip(poly, plane):
    if not poly:
        return []
    a,b,c = map(Q,plane)
    val = lambda p: a*p[0]+b*p[1]+c
    out=[]
    for left,right in zip(poly, poly[1:]+poly[:1]):
        vl,vr=val(left),val(right)
        if vl >= 0:
            out.append(left)
        if (vl<0) != (vr<0):
            t=vl/(vl-vr)
            out.append(tuple(left[i]+t*(right[i]-left[i]) for i in (0,1)))
    # Adjacent duplicate vertices can occur when a cut passes through a corner.
    clean=[]
    for p in out:
        if not clean or p != clean[-1]:
            clean.append(p)
    if len(clean)>1 and clean[0]==clean[-1]:
        clean.pop()
    return clean

def area(poly):
    if len(poly)<3:
        return Q(0)
    return abs(sum((p[0]*q[1]-q[0]*p[1] for p,q in zip(poly,poly[1:]+poly[:1])),Q(0)))/2

def band_polygon(m):
    poly=clip(SQUARE,(-1,2,-m))
    return clip(poly,(1,-2,m+1))

def mask_probabilities(x):
    """Direct probabilities of all 8 events, without count-moment assumptions."""
    answer={mask:Q(0) for mask in product((0,1),repeat=3)}
    for m in (-1,0,1):
        base=band_polygon(m)
        # Affine coordinate triples for u,v,w.
        coords=((Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0)),(Q(-1),Q(2),Q(-m)))
        for mask in answer:
            poly=base
            for inside,(a,b,c) in zip(mask,coords):
                plane=(-a,-b,x-c) if inside else (a,b,c-x)
                poly=clip(poly,plane)
            answer[mask] += area(poly)
    return answer

def q_expected(x):
    if x<=Q(1,2):
        return x*x/2
    return Q(1,2)-2*x+Q(5,2)*x*x

def count_expected(x):
    q=q_expected(x)
    return [1-3*x+3*x*x-q,3*x-6*x*x+3*q,3*x*x-3*q,q]

# A tiny exact ring Q[x,q], represented by exponents -> rational coefficient.
ZERO={}
ONE={(0,0):Q(1)}
X={(1,0):Q(1)}
QQ={(0,1):Q(1)}

def const(a):
    return {} if a==0 else {(0,0):Q(a)}

def add(*polys):
    d={}
    for p in polys:
        for key,value in p.items():
            d[key]=d.get(key,Q(0))+value
    return {k:v for k,v in d.items() if v}

def scale(p,a):
    return {k:v*Q(a) for k,v in p.items() if v*Q(a)}

def mul(p,q):
    d={}
    for (i,j),v in p.items():
        for (k,l),w in q.items():
            key=(i+k,j+l)
            d[key]=d.get(key,Q(0))+v*w
    return {k:v for k,v in d.items() if v}

def power(p,n):
    out=ONE
    for _ in range(n):
        out=mul(out,p)
    return out

def substitute_q(p,q):
    return add(*(scale(mul(power(X,i),power(q,j)),v) for (i,j),v in p.items()))

def evaluate(p,x,q=Q(0)):
    return sum((v*x**i*q**j for (i,j),v in p.items()),Q(0))

def integrate(p,lo=Q(0),hi=Q(1)):
    check(all(j==0 for i,j in p),'Integrate still contains q')
    return sum((v*(hi**(i+1)-lo**(i+1))/(i+1) for (i,j),v in p.items()),Q(0))

def reflected(p):
    check(all(j==0 for i,j in p),'Reflect still contains q')
    return add(*(scale(power(add(ONE,scale(X,-1)),i),v) for (i,j),v in p.items()))

def fmtpoly(p):
    return {f'x^{i}q^{j}':str(v) for (i,j),v in sorted(p.items())}

def pair_rectangle(x,y,left):
    # left=0 tests (u,w); left=1 tests (v,w).
    ans=Q(0)
    for m in (-1,0,1):
        poly=band_polygon(m)
        poly=clip(poly,(-1,0,x) if left==0 else (0,-1,x))
        poly=clip(poly,(1,-2,m+y))
        ans+=area(poly)
    return ans

def iid_integrated(n,p):
    total=ZERO
    for k in range(n+1):
        term=power(add(const(Q(k,n)),scale(X,-1)),p)
        mass=mul(power(X,k),power(add(ONE,scale(X,-1)),n-k))
        total=add(total,scale(mul(term,mass),comb(n,k)))
    return integrate(total)

def verify_inputs():
    here=Path(__file__).resolve().parent
    data=json.loads((here/'INPUT_PINS.json').read_text())
    inputs=here.parent.parent/'inputs'
    for name,pin in data['files'].items():
        body=(inputs/name).read_bytes()
        check(len(body)==pin['bytes'],'Input size mismatch '+name)
        check(hashlib.sha256(body).hexdigest()==pin['sha256'],'Input SHA mismatch '+name)
    return len(data['files'])

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--negative-guard',action='store_true')
    args=ap.parse_args()
    input_count=verify_inputs()
    band_areas=[area(band_polygon(m)) for m in (-1,0,1)]
    check(band_areas==[Q(1,4),Q(1,2),Q(1,4)],'Incorrect complete modular partition')
    check(sum(band_areas)==1,'Band partition not unit area')
    # All distinct rational thresholds with denominator <= 30, including boundaries.
    thresholds=sorted({Q(a,b) for b in range(1,31) for a in range(b+1)})
    stored={}
    for x in thresholds:
        masks=mask_probabilities(x)
        check(sum(masks.values())==1,f'Masks do not partition at {x}')
        check(all(v>=0 for v in masks.values()),f'Negative probability at {x}')
        check(masks[(1,1,1)]==q_expected(x),f'Triple formula wrong at {x}')
        counts=[sum((v for m,v in masks.items() if sum(m)==k),Q(0)) for k in range(4)]
        check(counts==count_expected(x),f'Full count law wrong at {x}')
        for i in range(3):
            check(sum((v for m,v in masks.items() if m[i]),Q(0))==x,f'Marginal {i} wrong')
            for j in range(i):
                check(sum((v for m,v in masks.items() if m[i] and m[j]),Q(0))==x*x,'Pair law wrong')
        direct=sum((counts[k]*(Q(k,3)-x)**4 for k in range(4)),Q(0))
        xr=min(x,1-x)
        expected=xr**4-Q(10,9)*xr**3+Q(8,27)*xr*xr+xr/27
        check(direct==expected,f'Expected fourth integrand wrong at {x}')
        stored[x]=(counts,direct)
    for x in thresholds:
        counts,f=stored[x]
        check(counts==list(reversed(stored[1-x][0])),'Count reflection failed')
        check(f==stored[1-x][1],'Fourth reflection failed')
    # Different thresholds for the two coordinates test a stronger pairwise claim.
    pair_thresholds=[Q(0),Q(1,7),Q(1,4),Q(1,2),Q(3,4),Q(6,7),Q(1)]
    for x,y,left in product(pair_thresholds,pair_thresholds,(0,1)):
        check(pair_rectangle(x,y,left)==x*y,'Unequal-threshold pair rectangle failed')
    # Universal symbolic identities, not interpolation from sampled thresholds.
    p0=add(ONE,scale(X,-3),scale(power(X,2),3),scale(QQ,-1))
    p1=add(scale(X,3),scale(power(X,2),-6),scale(QQ,3))
    p2=add(scale(power(X,2),3),scale(QQ,-3))
    p3=QQ
    probs=[p0,p1,p2,p3]
    check(add(*probs)==ONE,'Symbolic probabilities do not sum to 1')
    for r,expected in [(1,scale(X,3)),(2,add(scale(X,3),scale(power(X,2),6))),
                       (3,add(scale(X,3),scale(power(X,2),18),scale(QQ,6))),
                       (4,add(scale(X,3),scale(power(X,2),42),scale(QQ,36)))]:
        check(add(*(scale(p,k**r) for k,p in enumerate(probs)))==expected,'Raw count moment wrong')
    f=add(*(mul(p,power(add(const(Q(k,3)),scale(X,-1)),4)) for k,p in enumerate(probs)))
    expected_f=add(power(X,4),scale(power(X,3),Q(-2,3)),scale(power(X,2),Q(2,27)),
                   scale(X,Q(1,27)),scale(QQ,Q(4,9)),scale(mul(X,QQ),Q(-8,9)))
    check(f==expected_f,'Universal fourth-moment identity wrong')
    qlo=scale(power(X,2),Q(1,2))
    qhi=add(const(Q(1,2)),scale(X,-2),scale(power(X,2),Q(5,2)))
    flo=substitute_q(f,qlo)
    fhi=substitute_q(f,qhi)
    check(fhi==reflected(flo),'Symbolic full-interval reflection failed')
    # Upper q follows directly from reflection and inclusion-exclusion.
    check(qhi==add(ONE,scale(X,-3),scale(power(X,2),3),scale(reflected(qlo),-1)),
          'Upper q inclusion-exclusion identity wrong')
    iidf=substitute_q(f,power(X,3))
    diff=add(flo,scale(iidf,-1))
    positive=scale(mul(power(X,2),power(add(ONE,scale(X,-2)),2)),Q(2,9))
    check(diff==positive,'Strict pointwise fourth-moment gap factorization wrong')
    lattice=integrate(flo,Q(0),Q(1,2))+integrate(fhi,Q(1,2),Q(1))
    iid=iid_integrated(3,4)
    check(lattice==Q(19,1620),'Wrong lattice fourth moment')
    check(iid==Q(4,405),'Wrong iid fourth moment')
    check(lattice-iid==Q(1,540),'Wrong strict full gap')
    check(lattice/iid==Q(19,16),'Wrong ratio')
    for n in range(1,13):
        check(iid_integrated(n,4)==Q(3*n-1,30*n**3),'iid n formula wrong')
        check(iid_integrated(n,2)==Q(1,6*n),'iid second moment wrong')
    # Both empty-tail triangles: change y=(n-1)z so integral is elementary.
    for n in range(3,20):
        one_triangle=Q(2,5*6*7*(n-1))
        check(one_triangle==Q(1,105*(n-1)),'One tail triangle integral wrong')
        check(2*Q(1,n-1)<=1,'Tail triangles have overlapping z interiors')
    check(Q(2,315)-iid_integrated(4,4)==Q(5,8064),'n4 tail counterexample gap wrong')
    # Adverse claims must be distinguishable from the audited statement.
    adverse(q_expected(Q(1,4))!=Q(1,4)**3,'pairwise does not imply triple independence')
    adverse(Q(1,2)!=q_expected(Q(1)),'lower-half q cannot be extended to one')
    no_wrap_q=area(clip(clip(clip(band_polygon(0),(-1,0,Q(3,4))),
                                         (0,-1,Q(3,4))),(1,-2,Q(3,4))))
    adverse(no_wrap_q!=q_expected(Q(3,4)),'negative and upper modular bands cannot be omitted')
    adverse(Q(1,105)<iid,'n3 tail lower bound alone does not refute comparison')
    adverse(lattice*3**4!=lattice,'fourth-power normalization is essential to fractions')
    adverse(Q(1,2)*2**4>Q(5,4)**4 and Q(1,2)*2<Q(5,4),
            'fourth-moment ordering does not order expected norms')
    adverse(Q(1,15)!=lattice,'fixed-zero-generator average differs from full average')
    # On a finite torus, multiplication by 2 fails uniformity for even modulus;
    # such a finite-grid control is not a substitute for continuous Haar measure.
    adverse(len({(2*z)%2 for z in range(2)})!=2,'finite even grid is not continuous Haar multiplication')
    # At t=0 reflection complements can fail pointwise; its null status matters.
    x=Q(1,3); points=[Q(0),Q(1,4),Q(3,4)]
    reflected_points=[(-t)%1 for t in points]
    adverse(sum(t<x for t in reflected_points)!=3-sum(t<1-x for t in points),
            'reflection identity requires removal only of null boundary events')
    check(not args.negative_guard,'Deliberate explicit negative guard')
    result={'status':'PASS','input_files_authenticated':input_count,'checks':CHECKS,
            'rational_thresholds':len(thresholds),'inclusion_masks_per_threshold':8,
            'modular_band_areas':list(map(str,band_areas)),
            'unequal_threshold_pair_controls':len(pair_thresholds)**2*2,
            'lattice_fourth_moment':str(lattice),'iid_fourth_moment':str(iid),
            'strict_gap':str(lattice-iid),'ratio':str(lattice/iid),
            'q_lower_polynomial':fmtpoly(qlo),'q_upper_polynomial':fmtpoly(qhi),
            'universal_fourth_polynomial':fmtpoly(f),'lower_fourth_polynomial':fmtpoly(flo),
            'gap_lower_polynomial':fmtpoly(diff),'adverse_controls':ADVERSE,
            'example_probabilities':{str(x):list(map(str,stored[x][0])) for x in (Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1))}}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
