#!/usr/bin/env python3
"""Independent finite arithmetic and combinatorial checks for the embedding proof.
No candidate code is imported. The checks do not certify imported theorems.
"""
from fractions import Fraction
from math import comb
from itertools import combinations
from pathlib import Path
import json

checks=[]
def require(name,condition):
    assert condition,name
    checks.append(name)

n=2**256
m=2**320
p=Fraction(1,2**384)
M=comb(n,3)
W_lower=Fraction(comb(n,7),n-6)-m*M
require('positive surviving witness bound',W_lower>0)
mu_lower=W_lower*p*p
# Exact maximum degree of the auxiliary graph is at most M-1.
denominator=Fraction(M*(M-1),2)*p*p+M*(M-1)*(M-2)*p**3
rate=mu_lower**2/(2*denominator)
# Natural log(n) < 256 and log(m+1) <= m for positive integer m.
entropy_upper=m+(20*n+3*m)*256
net=rate-entropy_upper
require('uniform Janson estimate dominates both entropies',net>2**342)
# exp(-net) <= 1/(1+net), avoiding floating point logarithms/exponentials.
robust_failure_upper=1/(1+net)
conflicts=comb(n,2)*comb(n-2,2)*p*p
triangle_mean=M*p
failure_upper=robust_failure_upper+conflicts/m+4/triangle_mean
require('joint event has positive probability',failure_upper<1)
require('remaining triangle count exceeds vertex count',triangle_mean/2-m>n)
require('quarter-power deletion budget integral',m**4==n**5)
require('hypothesis for displayed coarse W constant',n**7>=107520**4)

# Moment-curve Radon circuits on eight vertices in R^4 alternate signs.
# This is a finite consistency check of witness and dependency counting only.
vertices=range(8)
triangles=list(combinations(vertices,3))
witnesses=[]
for six in combinations(vertices,6):
    witnesses.append(frozenset((six[::2],six[1::2])))
require('cyclic witness count',len(witnesses)==comb(8,6))
for seven in combinations(vertices,7):
    require('a balanced witness in each of seven-set '+str(seven),
            any(set().union(*map(set,pair)).issubset(seven) for pair in witnesses))
incidence={tri:0 for tri in triangles}
for pair in witnesses:
    for tri in pair:incidence[tri]+=1
ordered_overlap=sum(bool(a & b) for a in witnesses for b in witnesses if a!=b)
require('ordered dependency count by shared triangle',
        ordered_overlap==sum(deg*(deg-1) for deg in incidence.values()))
require('candidate dependency upper bound',ordered_overlap<=len(triangles)**3)
for a,b in combinations(witnesses,2):
    require('distinct witness pairs share at most one triangle',len(a&b)<=1)
# Vertices shared across triangles create no shared Bernoulli variable.
require('vertex overlap does not identify a triangle variable',
        frozenset(((0,1,2),(3,4,5))).isdisjoint(frozenset(((0,3,6),(1,4,7)))))

result={'status':'passed','exact_assertions':len(checks),
        'explicit_n':'2^256','explicit_m':'2^320','explicit_p':'2^-384',
        'combined_failure_bound_below_one':True,
        'eight_vertex_balanced_pairs':len(witnesses),
        'eight_vertex_ordered_dependencies':ordered_overlap,
        'checks':checks,
        'scope':'Independent exact arithmetic and finite combinatorial consistency only; no huge sample and no claim of a formal proof of imported geometry.'}
Path(__file__).with_name('independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
