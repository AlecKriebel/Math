"""Fresh analytic-review controls: exact multiaffine environment polynomials.

No submitted checker is imported. Polynomial coefficient integration replaces
environment enumeration. Finite evidence cannot establish asymptotic rates.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import product
from math import comb
from functools import lru_cache
from pathlib import Path
import datetime, hashlib, json

C = Counter()
def check(ok, family):
    if not ok:
        raise AssertionError(family)
    C[family] += 1

def add(dst, src, scale=1):
    for monomial, coefficient in src.items():
        dst[monomial] = dst.get(monomial, 0) + coefficient*scale
        if not dst[monomial]:
            del dst[monomial]

def kernel_polynomials(n, start=0, drift=Q(), radius=None):
    # Coefficients are signed integers; environment variables are formal.
    rows = {start: {frozenset(): 1}}
    for t in range(n):
        nxt = defaultdict(dict)
        for x, poly in rows.items():
            variable = (t, x)
            check(all(variable not in monomial for monomial in poly),
                  'fresh_time_variable_is_not_reused')
            positive = {monomial | {variable}: c for monomial, c in poly.items()}
            negative = dict(poly)
            add(negative, positive, -1)
            for y, term in [(x+1, positive), (x-1, negative)]:
                if radius is None or abs(Q(y)-start-drift*(t+1)) <= radius:
                    add(nxt[y], term)
        rows = dict(nxt)
    return rows

def coarse(rows, width, shift):
    out = defaultdict(dict)
    for x, poly in rows.items():
        add(out[(Q(x)-shift)//width], poly)
    return dict(out)

@lru_cache(None)
def integrated_pair(left, right, q, ep2):
    return ep2**len(left & right) * q**len(left ^ right)

def expectation(poly, q):
    return sum((Q(c)*q**len(m) for m,c in poly.items()), Q())

def square_expectation(poly, q, ep2):
    return sum((Q(c*d)*integrated_pair(m,k,q,ep2)
                for m,c in poly.items() for k,d in poly.items()), Q())

def annealed(n, q):
    return {2*j-n: Q(comb(n,j))*q**j*(1-q)**(n-j) for j in range(n+1)}

def sticky(a, delta, n):
    rows={0:Q(1)}
    for t in range(n):
        nxt=defaultdict(Q)
        for x,w in rows.items():
            d=delta if x==0 else a
            nxt[x-1]+=w*d; nxt[x]+=w*(1-2*d); nxt[x+1]+=w*d
        rows=dict(nxt)
    return rows.get(0,Q())

laws=[[(Q(2,9),Q(1))], [(Q(1,101),Q(2,7)),(Q(100,101),Q(5,7))],
      [(Q(1,7),Q(1,4)),(Q(3,8),Q(1,3)),(Q(9,10),Q(5,12))]]
polys=[kernel_polynomials(n) for n in range(5)]
for law in laws:
    q=sum((p*w for p,w in law),Q())
    ep2=sum((p*p*w for p,w in law),Q())
    delta=q-ep2; a=q*(1-q); sigma=ep2-q*q
    check(0<delta<=a<=Q(1,4),'law_parameters')
    for n,rows in enumerate(polys):
        an=annealed(n,q)
        mass={}
        for p in rows.values(): add(mass,p)
        check(mass=={frozenset():1},'polynomial_probability_normalization')
        for x,p in rows.items():
            check(expectation(p,q)==an[x],'annealed_mean_by_polynomial_integration')
        overlap=sum((square_expectation(p,q,ep2) for p in rows.values()),Q())
        check(overlap==sticky(a,delta,n),'replica_identity_by_polynomial_integration')
        if n==0: continue
        for width,shift in product([Q(1),Q(7,6),Q(5,2),Q(31,4)],
                                   [Q(-9,7),Q(),Q(11,13)]):
            cells=coarse(rows,width,shift)
            for cell,p in cells.items():
                variance=square_expectation(p,q,ep2)-expectation(p,q)**2
                predicted=Q()
                for s in range(n):
                    tail=annealed(n-s-1,q)
                    for x,oldpoly in polys[s].items():
                        grad=sum((w*(int((Q(x+1+y)-shift)//width==cell)-
                                     int((Q(x-1+y)-shift)//width==cell))
                                  for y,w in tail.items()),Q())
                        predicted+=sigma*square_expectation(oldpoly,q,ep2)*grad*grad
                check(variance==predicted,'interval_variance_polynomial_vs_martingale')
                check(variance>=0,'cell_variance_nonnegative')

# Exact polynomial dependency rather than numerical changed-environment tests.
for n,start,v,radius in product(range(1,6),[-3,0,4],
                               [Q(-999,1000),Q(2,9),Q(999,1000)],[1,2,4]):
    rows=kernel_polynomials(n,start,v,radius)
    variables=set().union(*(set(m) for p in rows.values() for m in p)) if rows else set()
    for t,y in variables:
        check(abs(Q(y)-start-v*t)<=radius,'formal_kernel_variables_inside_tube')
        k=(Q(y)-v*t)//radius
        check(k*radius-radius-1<=start<=(k+1)*radius+radius+1,
              'formal_strip_dependency_implies_start_in_influence_interval')
    candidates=range(start//radius-5,start//radius+6)
    check(sum(k*radius-radius-1<=start<=(k+1)*radius+radius+1 for k in candidates)<=6,
          'influence_overlap_uniform_bound')

# Explicit excluded-law falsifications, including a genuinely correlated law.
def cprob(mu,width):
    out=defaultdict(Q)
    for x,p in mu.items(): out[x//width]+=p
    return dict(out)
def l1(p,q):
    return sum((abs(p.get(x,Q())-q.get(x,Q())) for x in p.keys()|q.keys()),Q())
negative={}
n=256; width=4
alpha=annealed(n,Q(1,2)); peak=max(alpha.values())
arrow_lower=2*(1-(width+1)*peak)
check(arrow_lower>Q(3,2),'excluded_arrow_law_large_coarse_discrepancy')
negative['arrow_n256_M4_L1_lower_bound']=str(arrow_lower)
# Single global p selected once: strict ellipticity without time/space iid.
left=annealed(n,Q(1,4));right=annealed(n,Q(3,4))
mix={x:(left[x]+right[x])/2 for x in left}
correlated=l1(cprob(left,width),cprob(mix,width))
check(correlated>Q(99,100),'strict_ellipticity_alone_does_not_replace_independence')
negative['global_p_correlated_n256_M4_L1']=str(correlated)
for n in range(33):
    check(l1(annealed(n,Q(2,7)),{x+1:p for x,p in annealed(n,Q(2,7)).items()})==2,
          'opposite_parity_kernel_L1_is_two')
for d in [Q(1,10**j) for j in range(1,10)]:
    gamma=Q(1,4)+d;beta=Q(1,4)+d/2;eta=d/4
    check(beta-eta-(Q(1,2)-gamma)==5*d/4>0,'sign_entropy_power_margin')
    check(2*beta-Q(1,2)-eta==3*d/4>0,'boundary_variance_power_margin')
check(Q(5,16)-Q(3,8)==-Q(1,16),'closure_coupling_exponent')
check(2*Q(3,8)-Q(1,32)-Q(1,2)-2*Q(1,32)==Q(5,32),
      'old_mass_tail_exponent')

here=Path(__file__)
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'status':'PASS','source_sha256':hashlib.sha256(here.read_bytes()).hexdigest(),
                  'assertions':sum(C.values()),'families':dict(C),
                  'negative_controls':negative,
                  'mechanism':'Exact multiaffine-polynomial integration and formal variable dependencies; no imported checker or random simulation.',
                  'scope':'Finite algebra and boundary controls only. Analytic proof, novelty and human peer review are separate.'},indent=2))
