#!/usr/bin/env python3
"""Exact rational controls for turn 5; universal claims use the written proof."""
from fractions import Fraction as Q
from itertools import product
import json

checks = 0

def ck(value):
    global checks
    assert value
    checks += 1

def add(z, w):
    return z[0] + w[0], z[1] + w[1]

def mul(z, w):
    return z[0]*w[0] - z[1]*w[1], z[0]*w[1] + z[1]*w[0]

def conj(z):
    return z[0], -z[1]

def scale(z, c):
    return c*z[0], c*z[1]

def sq(z):
    return z[0]*z[0] + z[1]*z[1]

zero, one = (Q(0), Q(0)), (Q(1), Q(0))
roots = [one, (Q(0), Q(1)), (-Q(1), Q(0)), (Q(0), -Q(1))]
bits = list(product(range(2), repeat=3))
phases = roots + [(Q(3,5), Q(4,5)), (Q(-5,13), Q(12,13))]

def density_average(vectors, squared_norm):
    return [[scale(tuple(sum(mul(v[i],conj(v[j]))[k] for v in vectors)
                          for k in range(2)), Q(1,len(vectors)*squared_norm))
             for j in range(8)] for i in range(8)]

def sigma(phi):
    vectors = []
    for a,b in product(range(4), repeat=2):
        vectors.append([mul(roots[(a*x[0]+b*x[1]-(a+b)*x[2])%4],
                            conj(phi) if x[2] else one) for x in bits])
    return density_average(vectors,8)

def tau_cut(phi,j):
    others = [k for k in range(3) if k != j]
    vectors = []
    for a in range(4):
        v = []
        for x in bits:
            if x[others[0]] != x[others[1]]:
                v.append(zero)
            else:
                k=x[others[0]]
                v.append(mul(roots[(a*x[j]-a*k)%4],conj(phi) if k else one))
        vectors.append(v)
    return density_average(vectors,4)

def state(p,t,phi):
    a,b=(1+3*p)/8,(1-p)/8
    r=[[zero for _ in range(8)] for _ in range(8)]
    for j in range(8):
        r[j][j]=(a if j in (0,7) else b,Q(0))
    r[0][7]=scale(phi,t/2)
    r[7][0]=conj(r[0][7])
    return r

def pt(r,j):
    out=[[zero for _ in range(8)] for _ in range(8)]
    for i,k in product(range(8), repeat=2):
        x,y=list(bits[i]),list(bits[k])
        x[j],y[j]=y[j],x[j]
        out[bits.index(tuple(x))][bits.index(tuple(y))]=r[i][k]
    return out

decomposition_cases=0
for phi in phases:
    ck(sq(phi)==1)
    s=sigma(phi)
    cuts=[tau_cut(phi,j) for j in range(3)]
    tau=[[scale(add(add(cuts[0][i][k],cuts[1][i][k]),cuts[2][i][k]),Q(1,3))
          for k in range(8)] for i in range(8)]
    for i,k in product(range(8),repeat=2):
        want_s=want_t=zero
        if i==k:
            want_s=(Q(1,8),Q(0))
            want_t=(Q(1,4) if i in (0,7) else Q(1,12),Q(0))
        elif (i,k)==(0,7):
            want_s, want_t=scale(phi,Q(1,8)),scale(phi,Q(1,4))
        elif (i,k)==(7,0):
            want_s, want_t=scale(conj(phi),Q(1,8)),scale(conj(phi),Q(1,4))
        ck(s[i][k]==want_s)
        ck(tau[i][k]==want_t)
    for n in range(21):
        p=Q(n,20);a,b=(1+3*p)/8,(1-p)/8
        for k in range(21):
            t=(1+3*p)*Q(k,80)
            r=state(p,t,phi)
            ck(a-t/2>=0 and b>=0)
            ck(2*a+6*b==1)
            for j in range(3):
                rp=pt(r,j)
                x=[0,0,0];x[j]=1; ix=bits.index(tuple(x))
                iy=7-ix
                ck(rp[ix][ix]==(b,Q(0)) and rp[iy][iy]==(b,Q(0)))
                ck(sq(rp[ix][iy])==t*t/4)
                ck((b-t/2>=0)==(t<=(1-p)/4))
            if t<=2*b:
                ck(a-t/2>=0 and b-t/2>=0 and 4*t<=1)
                ck(4*t+2*(a-t/2)+6*(b-t/2)==1)
                for i,j in product(range(8),repeat=2):
                    v=scale(s[i][j],4*t)
                    if i==j:
                        v=add(v,(a-t/2 if i in (0,7) else b-t/2,Q(0)))
                    ck(v==r[i][j])
                decomposition_cases+=1
            if t<=6*b:
                ck(a-t/2>=0 and b-t/6>=0 and 2*t<=1)
                ck(2*t+2*(a-t/2)+6*(b-t/6)==1)
                for i,j in product(range(8),repeat=2):
                    v=scale(tau[i][j],2*t)
                    if i==j:
                        v=add(v,(a-t/2 if i in (0,7) else b-t/6,Q(0)))
                    ck(v==r[i][j])
                decomposition_cases+=1

# Pure cut-product matrix-element equality. No normalization is needed:
# both sides of the squared equality are homogeneous of degree four.
for j in range(3):
    for n in range(1,31):
        alpha=[(Q(n),Q(1)),(Q(2),Q(-n))]
        beta=[(Q(k-n),Q(k+1)) for k in range(4)]
        others=[k for k in range(3) if k!=j]
        v=[mul(alpha[x[j]],beta[2*x[others[0]]+x[others[1]]]) for x in bits]
        x=[0,0,0];x[j]=1;ix=bits.index(tuple(x));iy=7-ix
        ck(sq(mul(v[0],conj(v[7])))==sq(v[ix])*sq(v[iy]))

for n in range(101):
    p=Q(n,100)
    ck((3+p)**2-2*(1+p)**3==(1-p)*(2*p*p+7*p+7))
    ck(2*(1+p)**3-(1+3*p)**2==(1-p)**2*(2*p+1))
    ck(2*(3+p)>4)  # strict derivative sign for theta_S-theta_B
    if p<1:
        ck((1-p)*(2*p*p+7*p+7)>0)
        ck((1-p)**2*(2*p+1)>0)
    ck((p<=(1-p)/4)==(p<=Q(1,5)))
    ck((p<=3*(1-p)/4)==(p<=Q(3,7)))
    ck(((1+3*p)/4>3*(1-p)/4)==(p>Q(1,3)))

ck(Q(343,1000)<Q(3,5)**2)
ck(Q(125,343)>Q(4,7)**2)
ck(Q(1,2)>Q(3,7))
ck(Q(1,5)<Q(2,5)<Q(3,7))
ck((1+Q(1))**3/8==1 and (3+Q(1))**3/64==1)

print(json.dumps({
    'exact_assertions':checks,
    'phase_choices':len(phases),
    'physical_parameter_cases':len(phases)*21*21,
    'checked_convex_decompositions':decomposition_cases,
    'full_separability_threshold':'(1-p)/4',
    'biseparability_threshold':'3(1-p)/4',
    'strict_threshold_order':'theta_F < theta_R < theta_B < theta_S for 0<=p<1',
    'proof_source':'TURN_5.md; finite controls are not universal proof',
    'general_mixed_state_classification':False
},indent=2))
