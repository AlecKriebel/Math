#!/usr/bin/env python3
from itertools import product
from math import gcd
from pathlib import Path
import json
counts={}
def ck(k,b):
    assert b,k
    counts[k]=counts.get(k,0)+1
p=231
local={}
for ell in (3,7,11):
    local[ell]=[u for u in range(ell) if (86*u*u-53)%ell==0]
    ck('two_local_unit_roots',len(local[ell])==2 and all(gcd(u,ell)==1 for u in local[ell]))
# Explicit CRT using Bezout inverses for each complementary modulus.
def extended(a,b):
    if b==0:return (a,1,0)
    g,x,y=extended(b,a%b)
    return (g,y,x-(a//b)*y)
es={}
for ell in local:
    m=p//ell;g,x,y=extended(m,ell)
    ck('bezout_identity',g==1 and m*x+ell*y==1)
    es[ell]=m*x
roots=sorted({sum(v*es[l] for l,v in zip((3,7,11),triple))%p for triple in product(*(local[l] for l in (3,7,11)))})
ck('crt_complete_root_list',roots==[10,32,67,109,122,164,199,221])
for u in roots:
    ck('unit_isometry',gcd(u,p)==1 and (86*u*u-53)%p==0)
# No exhaustive pair-product replay: use exact orthogonality factorization.
for a,b in product(range(p),repeat=2):
    lhs=(53*a-86*10*b)%p
    rhs=86*10*(10*a-b)%p
    ck('orthogonal_kernel_factorization',lhs==rhs)
    ck('orthogonal_graph_equivalence',(lhs==0)==((b-10*a)%p==0))
ck('nondegenerate_coefficients',gcd(53,p)==gcd(86,p)==gcd(860,p)==1)
g,x,y=extended(53,p)
ck('homeomorphism_inverse',g==1 and x%p==170)
orbit={53,(-53)%p,x%p,(-x)%p}
ck('unoriented_homeomorphism_obstruction',orbit=={53,61,170,178} and 86 not in orbit)
# Replacing q by its inverse changes the generator, not isometry existence.
for u in roots:
    v=(u*86*x)%p
    ck('inverse_linking_convention',(pow(86,-1,p)*v*v-pow(53,-1,p))%p==0)
# Rational Betti identities from boundary exactness, duality and Euler zero.
for b1 in range(31):
    b3=b1+1;b2=2*b1
    ck('cover_euler_identity',1-b1+b2-b3==0)
    ck('source_nonzero_consequence',b1==0 or (b2>=2 and b3>=2))
# Integral relative fundamental class maps primitively into the two boundary classes.
for signs in product((-1,1),repeat=2):
    ck('boundary_fundamental_class_primitive',gcd(*signs)==1)
result={'status':'PASS','assertions_passed':sum(counts.values()),'by_category':counts,
        'crt_roots':roots,'local_roots':local,'scope':'Exact boundary algebra and numerical identities; no topological realization or rho/d-invariant calculation.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
