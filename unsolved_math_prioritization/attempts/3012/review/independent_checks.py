"""Exact rational diagnostics for explicit interval fibers and the product collar.
These bounded controls do not prove any topological straightening theorem.
Run with Python 3; standard library only. Receipt written beside this script.
"""
from fractions import Fraction as Q
from pathlib import Path
from collections import Counter
import hashlib, json
counts = Counter()
def ck(group, statement):
    assert statement, group
    counts[group] += 1

def b(c, y):
    return y / (1+c-c*abs(y))
def bi(c, y):
    return (1+c)*y/(1+c*abs(y))
def p(z):
    return max(map(abs,z))
def mul(r,z):
    return tuple(r*v for v in z)
def h(s,z):
    x,y=z
    return (b(s,x), b(s*(1+x/2),y))
def hi(s,z):
    X,Y=z
    x=bi(s,X)
    return (x,bi(s*(1+x/2),Y))
def E(s,z,inv=False):
    r=p(z)
    if r<=1:
        return (hi if inv else h)(s,z)
    if r>=2:
        return z
    u=mul(1/r,z)
    return mul(r,(hi if inv else h)(s*(2-r),u))
vals=[Q(i,4) for i in range(-4,5)]
times=[Q(i,8) for i in range(9)]
cs=[Q(i,4) for i in range(-3,9)]
for c in cs:
    for y in vals:
        ck('fiber_inverse',bi(c,b(c,y))==y)
        ck('fiber_inverse',b(c,bi(c,y))==y)
        ck('fiber_range',abs(b(c,y))<=1)
    ck('fiber_endpoints',b(c,-1)==-1 and b(c,0)==0 and b(c,1)==1)
    ck('fiber_monotone',all(b(c,vals[i])<b(c,vals[i+1]) for i in range(len(vals)-1)))
for s in times:
    for x in vals:
        for y in vals:
            z=(x,y)
            ck('product_inverse',hi(s,h(s,z))==z)
            ck('product_inverse',h(s,hi(s,z))==z)
            ck('product_boundary',(p(h(s,z))==1)==(p(z)==1))
            ck('zero_section',(h(s,z)[1]==0)==(y==0))
            # Fiber contraction from x to the origin in the base.
            c=1+(1-s)*x/2
            ck('contracted_inverse',bi(c,b(c,y))==y)
            if s==1:
                ck('constant_terminal_fiber',b(c,y)==b(Q(1),y))
    for u in [(x,y) for x in vals for y in vals if max(abs(x),abs(y))==1]:
        for r in [Q(i,4) for i in range(1,13)]:
            z=mul(r,u)
            ck('collar_inverse',E(s,E(s,z),True)==z)
            ck('collar_inverse',E(s,E(s,z,True))==z)
            if r>=1:
                ck('collar_shell',p(E(s,z))==r)
            if r==1:
                ck('inner_seam',E(s,z)==h(s,z))
            if r==2:
                ck('outer_seam',E(s,z)==z)
            if r>=2:
                ck('fixed_exterior',E(s,z)==z)
            if s==0:
                ck('initial_identity',E(s,z)==z)
            ck('collar_zero_section',(E(s,z)[1]==0)==(z[1]==0))
ck('nontrivial_witness',h(Q(1),(Q(1,2),Q(1,2)))!=(Q(1,2),Q(1,2)))
# Algebraic matching of boundary coordinates uses E^{-1} E = id.
# No purported geometric model of arbitrary charts is tested.
here=Path(__file__).resolve().parent
source=here/'OBSTRUCTION.md'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='eb6986ba77d7639e6f4df4d41cc2d89b23865d5040be01454ea832b4c2d73bd3'
receipt={'verdict':'PASS','assertions':sum(counts.values()),'groups':dict(sorted(counts.items())),
'artifact_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
'scope':'Bounded exact rational controls for n=k=1 product-fiber isotopies and collar inverse/seam formulas. No general straightening, relative annulus, or source-target proof certification.'}
(here/'independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
