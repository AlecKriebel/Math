#!/usr/bin/env python3
"""Small independent exact verifier. Standard library only; not a proof of geometry."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent

def require(p, label):
    if not p:
        raise RuntimeError(label)

def mm(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))

def det(A):
    a,b,c=A[0];d,e,f=A[1];g,h,i=A[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)

ID=((1,0,0),(0,1,0),(0,0,1))

def mpow(A,n,mod=None):
    B=ID
    while n:
        if n&1:
            B=mm(B,A)
            if mod: B=tuple(tuple(t%mod for t in row) for row in B)
        A=mm(A,A)
        if mod: A=tuple(tuple(t%mod for t in row) for row in A)
        n//=2
    return B

def trace(A): return sum(A[i][i] for i in range(3))

def charpoly(A):
    s=trace(A)
    return (1,-s,F(s*s-trace(mm(A,A)),2),-det(A))

# Ring arithmetic rebuilt from theta^3=3theta-1.
def mul(a,b):
    c=[0]*5
    for i in range(3):
        for j in range(3): c[i+j]+=a[i]*b[j]
    for k in (4,3):
        c[k-2]+=3*c[k];c[k-3]-=c[k]
    return tuple(c[:3])

ONE=(1,0,0);THETA=(0,1,0);THETA2=(0,0,1)

def mrep(a):
    cols=[mul(a,b) for b in (ONE,THETA,THETA2)]
    return tuple(tuple(cols[j][i] for j in range(3)) for i in range(3))

def basechange(A,d):
    return tuple(tuple(F(A[i][j]*d[j],d[i]) for j in range(3)) for i in range(3))

def integral(A): return all(F(t).denominator==1 for row in A for t in row)

def span(vs,p):
    out={(0,0,0)}
    for v in vs:
        out={tuple((a[i]+t*v[i])%p for i in range(3)) for a in out for t in range(p)}
    return frozenset(out)

def subspaces(p):
    allv=list(product(range(p),repeat=3))
    levels={span([],p)};out=set(levels)
    for _ in range(3):
        levels={span(list(w)+[v],p) for w in levels for v in allv}
        out.update(levels)
    return out

def stabilizer(w,p):
    return frozenset(a for a in product(range(p),repeat=3)
        if all(tuple(t%p for t in mul(a,b)) in w for b in w))

def saturation(w,p):
    return span([tuple(t%p for t in mul(a,b)) for a in (ONE,THETA,THETA2) for b in w],p)

own_manifest=json.loads((ROOT/'MANIFEST.json').read_text())
require(own_manifest['status']=='CLOSED','closed report state')
for entry in own_manifest['entries']:
    body=(ROOT/entry['path']).read_bytes()
    require(len(body)==entry['bytes'] and hashlib.sha256(body).hexdigest()==entry['sha256'],'own manifest '+entry['path'])
pins=json.loads((ROOT/'PINS.json').read_text())
for pin in pins['immutable_git_files']:
    b=(ROOT/'inputs'/Path(pin['path']).name).read_bytes()
    require(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'immutable pin '+pin['path'])
manifest=json.loads((ROOT/'inputs'/'MANIFEST.json').read_text())
require(set(manifest['members'])=={p.name for p in (ROOT/'inputs').iterdir()},'exact ten inputs')
for e in manifest['entries']:
    b=(ROOT/'inputs'/e['file']).read_bytes()
    require(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'candidate manifest '+e['file'])

C=mrep(THETA)
require(C==((0,0,-1),(1,0,3),(0,1,0)),'companion representation')
A=mpow(C,6)
B=basechange(A,(1,3,3))
require(A==((1,-9,6),(-6,28,-27),(9,-6,28)),'A displayed')
require(B==((1,-27,18),(-2,28,-27),(3,-6,28)),'B displayed')
require(charpoly(A)==charpoly(B)==(1,-57,570,-1),'same characteristic polynomial')
require(det(A)==det(B)==1,'SL3 realization')
def peval(t): return t**3-57*t*t+570*t-1
require(peval(0)<0<peval(1) and peval(10)>0>peval(20) and peval(57)>0,'three distinct positive root intervals')
require(peval(1)!=0 and peval(-1)!=0,'cubic irreducibility rational roots')
G=tuple(tuple(trace(mrep(mul(x,y))) for y in (ONE,THETA,THETA2)) for x in (ONE,THETA,THETA2))
require(G==((3,0,6),(0,6,-3),(6,-3,18)) and det(G)==81,'trace Gram')
require(det(basechange(ID,(1,3,3)))==1,'basischange sanity')
DGD=tuple(tuple(G[i][j]*(1,3,3)[i]*(1,3,3)[j] for j in range(3)) for i in range(3))
require(det(DGD)==6561,'order discriminant')

# Full symbolic formula is linear in a,b,c, so the three basis tests suffice.
for f in (1,2,3,5):
    for a,b,c in (ONE,THETA,THETA2):
        displayed=((a,-f*c,-f*b),(F(b,f),a+3*c,3*b-c),(F(c,f),b,a+3*c))
        require(basechange(mrep((a,b,c)),(1,f,f))==displayed,'multiplier formula')

# Recheck the norm cubic on an unisolvent degree-three simplex grid.
for x,y,z in product(range(4),repeat=3):
    if x+y+z<=3:
        val=x**3+6*x*x*z-3*x*y*y+3*x*y*z+9*x*z*z-y**3+3*y*z*z+z**3
        require(det(mrep((x,y,z)))==val,'norm cubic')

# Genuine automorphism has order three; this does not authorize all S3 permutations.
beta=(-2,0,1)
tau=tuple(tuple(t[i] for t in (ONE,beta,mul(beta,beta))) for i in range(3))
require(mul(mul(beta,beta),beta)==tuple(3*beta[i]-ONE[i] for i in range(3)),'beta minimal relation')
require(mpow(tau,3)==ID and tau!=ID and det(tau)==1,'genuine automorphism order')
require(mm(tau,C)==mm(mrep(beta),tau),'semilinear conjugation')

# Positive unit theta^2 has finite residue order modulo f. This power is 1 mod f,
# hence its multiplication and inverse preserve Z+fZ[theta].
residue_orders={}
U=mm(C,C)
for f in range(1,13):
    residue_ID=tuple(tuple(t%f for t in row) for row in ID)
    power=residue_ID
    for e in range(1,100000):
        power=tuple(tuple(t%f for t in row) for row in mm(power,U))
        if power==residue_ID:
            residue_orders[str(f)]=e;break
    else: raise RuntimeError('residue order bound')
    # The only first-column constraints in the R_f basis are met by congruence.
    require(power[1][0]==power[2][0]==0,'R_f preservation residue')

# Finite conductor intervals include proper noninvertible R-lattices.
finite={}
for p in (2,3):
    subs=subspaces(p)
    scalar=span([ONE],p)
    eligible=[w for w in subs if len(saturation(w,p))==p**3 and stabilizer(w,p)==scalar]
    finite[str(p)]={'all_subspaces':len(subs),'full_span_exact_scalar_multiplier':len(eligible),
       'eligible_sizes':{str(n):sum(len(w)==n for w in eligible) for n in (1,p,p*p,p*p*p)}}
require(finite['2']['all_subspaces']==16 and finite['2']['full_span_exact_scalar_multiplier']==14,'mod2 full enumeration')
require(finite['3']['all_subspaces']==28 and finite['3']['full_span_exact_scalar_multiplier']==18,'mod3 full enumeration')
W=span([ONE,THETA],2)
require(len(W)==4 and len(saturation(W,2))==8 and stabilizer(W,2)==span([ONE],2),'noninvertible witness finite module')
# Direct rational multiplication: I=<1,theta,2theta^2>, multiplier requires a integer,
# b/2 integer,c/2 integer. First and last columns make this exact, not a bounded search.
for a,b,c in product(range(-2,3),repeat=3):
    require(integral(basechange(mrep((a,b,c)),(1,1,2)))==(b%2==0 and c%2==0),'noninvertible witness multiplier')

negative_controls={
 'operator_discriminant_equals_order_discriminant': (-4*(-57)**3*(-1)+(-57)**2*570**2-4*570**3-27*(-1)**2+18*(-57)*570*(-1))==81,
 'f_squared_instead_of_f_fourth': 3**2*81==6561,
 'all_full_span_subspaces_have_exact_scalar_multiplier': all(stabilizer(w,3)==span([ONE],3) for w in subspaces(3) if len(saturation(w,3))==27),
 'noninvertible_witness_has_rank_one_conductor_quotient': len(W)==2,
}
require(not any(negative_controls.values()),'false arithmetic controls')
result={'status':'PASS','input_pins':len(pins['immutable_git_files']),'candidate_manifest':'PASS',
 'exact_pair':{'A':[list(r) for r in A],'B':[[int(t) for t in r] for r in B],'characteristic_polynomial':[1,-57,570,-1],
 'order_discriminants':[81,6561]},'finite_intervals':finite,'residue_orders':residue_orders,
 'automorphism_order':3,'norm_unisolvent_tests':20,'noninvertible_witness':'I=<1,theta,2theta^2>; R=<1,2theta,2theta^2>',
 'false_controls_rejected':list(negative_controls),'limitation':'Exact arithmetic support; universal geometry and all-field theorems require the written proof.'}
print(json.dumps(result,sort_keys=True,indent=2))
