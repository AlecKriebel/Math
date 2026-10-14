#!/usr/bin/env python3
"""Exact elementary checks; no assertions disappear under Python -O."""
import itertools, json, math
from pathlib import Path

counts = {}
def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def mul(A,B,m=None):
    C=tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    return C if m is None else tuple(tuple(x%m for x in row) for row in C)

I=((1,0),(0,1))
# Integer identities, including the arbitrary off-diagonal parameter.
number=0
for b in range(-15,16):
    for z in range(-15,16):
        for sign in (-1,1):
            s=((sign,b),(0,-sign))
            n=((1,z),(0,1))
            require(mul(s,s)==I, ('involution',b,z,sign))
            require(mul(mul(s,n),s)==((1,-z),(0,1)),('conjugation',b,z,sign))
            number+=1
counts['integer_reflection_conjugations']=number

# Exhaustively solve strict and diamond equations in Z/m, using global +/-1 units.
# These tests are ring-level checks, not a claim Z/m is every quadratic residue ring.
strict=diamond=0
for m in (2,3,4,5,7,8,9,12,15,16,18,20,24,25,27,32):
    for u,v in itertools.product(range(m),repeat=2):
        if math.gcd(math.gcd(u,v),m)!=1:
            continue
        d=math.gcd(u,m)
        A=(2*u)%m==0
        B=(2%d)==0
        solutionsB=[b for b in range(m) if (u*b-2*v)%m==0]
        require(bool(solutionsB)==B,('strict solvability',m,u,v,d))
        strict_exists=A or bool(solutionsB)
        brute=False
        for eps,de in ((-1,1),(1,-1)):
            for b in range(m):
                if ((eps-1)*u)%m==0 and (u*b+(de-1)*v)%m==0:
                    brute=True
                    break
        require(strict_exists==brute,('strict criterion',m,u,v))
        strict+=1
        # All a with a^2=1 are checked independently, including non-sign roots at 2.
        for a in range(m):
            if math.gcd(a,m)!=1 or (a*a-1)%m:
                continue
            bs=[b for b in range(m) if ((-1-a)*u)%m==0 and (u*b+(1-a)*v)%m==0]
            for b in bs:
                s=((-1,b),(0,1))
                require(mul(s,s)==I,('diamond square',m,u,v,a,b))
                require(((-u)%m,(u*b+v)%m)==((a*u)%m,(a*v)%m),('diamond marking',m,u,v,a,b))
                diamond+=1
counts['primitive_modular_rows']=strict
counts['diamond_reflection_solutions']=diamond

# All-divisor equivalence (V), over products of up to four abstract prime powers.
boxes=0
for k in range(1,5):
    for es in itertools.product(range(3),repeat=k):
        for ns in itertools.product(range(1,7),repeat=k):
            active=[i for i in range(k) if ns[i]>es[i]]
            V=len(active)<=1 and (not active or ns[active[0]]<=2*es[active[0]]+1)
            # Find an uncovered vector, stopping immediately when one exists.
            covered=True
            for rs in itertools.product(*(range(n+1) for n in ns)):
                low=all(r<=e for r,e in zip(rs,es))
                high=all(r>=n-e for r,n,e in zip(rs,ns,es))
                if not (low or high):
                    covered=False
                    break
            require(covered==V,('all cusp criterion',ns,es))
            boxes+=1
counts['valuation_boxes_checked']=boxes

# Local sign coverage (L) and explicit CRT examples over Z/m.
local=0
for e in range(4):
    for n in range(1,13):
        actual=all(r<=e or r>=n-e for r in range(n+1))
        require(actual==(n<=2*e+1),('local coverage',n,e))
        local+=1
counts['local_depth_thresholds']=local

examples=[]
for m,c in ((8,2),(8,4),(15,3),(15,5),(12,2),(24,6),(32,8),(9,3)):
    u,v=c%m,1
    strict_ref=[]
    diamond_ref=[]
    for eps,de in ((-1,1),(1,-1)):
        for b in range(m):
            if ((eps-1)*u)%m==0 and (u*b+(de-1)*v)%m==0:
                strict_ref.append([eps,b,de])
                break
    for a in range(m):
        if math.gcd(a,m)!=1 or (a*a-1)%m: continue
        for b in range(m):
            if ((-1-a)*u)%m==0 and (u*b+(1-a)*v)%m==0:
                diamond_ref.append([a,b])
                break
    examples.append({'modulus':m,'marking':[u,v],'strict_reflections':strict_ref,'diamond_reflections_a_b':diamond_ref})

# Optional unit-field box tests, including a middle cusp at q3^4.
# Vectors are (v_q2(epsilon-1),v_q3(epsilon-1)); None means infinity.
units={'1':(None,None),'-1':(1,0),'omega':(0,1),'omega2':(0,1),'-omega':(0,0),'-omega2':(0,0)}
def allowed_unit_pair(ns,rs,eps,de):
    ae,ad=units[eps],units[de]
    return all((x is None or r>=n-x) and (y is None or r<=y) for n,r,x,y in zip(ns,rs,ae,ad))
unit_cases=[]
for n2,n3 in itertools.product(range(7),repeat=2):
    if n2+n3==0: continue
    zero=all(any(allowed_unit_pair((n2,n3),rs,e,d) for e in units for d in units if e!=d)
             for rs in itertools.product(range(n2+1),range(n3+1)))
    expected=(n3==0 and n2<=3) or (n2==0 and n3<=3) or (n2,n3) in ((1,1),(1,2),(2,1))
    require(zero==expected,('Eisenstein two-prime boxes',n2,n3))
    unit_cases.append({'n2':n2,'n3':n3,'boundary_H1_zero':zero})
counts['exceptional_unit_level_cases']=len(unit_cases)

# Gaussian test q=(2+i), O/q^2=Z/25 with i=18 (since 18^2=-1).
imod=18
require((imod*imod+1)%25==0,'Gaussian quotient relation')
pi=(2+imod)%25
require(math.gcd(pi,25)==5,'pi valuation one')
units25={1,24,imod,(-imod)%25}
require(len({u%5 for u in units25})==4,'unit injectivity mod q')
principal5={(1+pi*t)%25 for t in range(25)}
require(len(principal5)==5,'principal ray kernel size')
require(principal5.intersection(units25)=={1},'ray kernel/unit intersection')
require(all((a*b)%25 in principal5 for a in principal5 for b in principal5),'ray kernel closure')
require(not any(e!=d and ((e-1)*pi)%25==0 and any((pi*b+d-1)%25==0 for b in range(25)) for e in units25 for d in units25),'Gaussian middle-cusp rotation')
counts['explicit_gaussian_ray_checks']=7

result={'status':'PASS','counts':counts,'examples':examples,'eisenstein_unit_cases':unit_cases,
        'scope':'Exact elementary matrix, congruence and divisor checks only. No K2 values, geometric cocycles, or group homology are computed.'}
path=Path(__file__).with_name('CHECK_RESULTS.json')
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','counts':counts},sort_keys=True))
