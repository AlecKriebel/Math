#!/usr/bin/env python3
"""Independent exact diagnostics; not a replacement for the analytic audit.

Uses sparse tensor matrix units in M_5 tensor M_5^op, with projection ranks
2, 2, 1. This probes the non-scalar diagonal corners absent from the author's
rank-one finite model. Only Python standard-library rational arithmetic is used.
"""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import json

counts = Counter()
negative = []

def check(condition, group):
    assert condition, group
    counts[group] += 1

def reject(condition, name):
    assert not condition, name
    negative.append(name)

def clean(a):
    return {k: v for k, v in a.items() if v}

def add(a, b, scale=F(1)):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, F(0)) + scale*v
    return clean(out)

def scaled(a, c):
    return clean({k: c*v for k, v in a.items()})

def mul(a, b):
    out = {}
    for (i,j), v in a.items():
        for (k,l), w in b.items():
            if j == k:
                out[i,l] = out.get((i,l), F(0)) + v*w
    return clean(out)

def adj(a):
    return {(j,i): v for (i,j),v in a.items()}

def tmul(a, b):
    # E_rs tensor E_uv^op times E_ab tensor E_cd^op.
    out = {}
    for (r,s,u,v), z in a.items():
        for (a0,b0,c0,d0), w in b.items():
            if s == a0 and d0 == u:
                key = (r,b0,c0,v)
                out[key] = out.get(key, F(0)) + z*w
    return clean(out)

def tensor(a, b):
    return {(r,s,u,v): z*w for (r,s),z in a.items()
            for (u,v),w in b.items()}

def jreal(a):
    # The real-coefficient part of the anti-linear coarse flip-star J.
    return {(v,u,s,r): z for (r,s,u,v),z in a.items()}

d = 5
blocks = [tuple(range(2)), tuple(range(2,4)), (4,)]
coeff = [F(1), F(3), F(2)]
q = [F(len(block),d) for block in blocks]
rates = [c*c*qn for c,qn in zip(coeff,q)]
which = {i:n for n,block in enumerate(blocks) for i in block}
eye = {(i,i): F(1) for i in range(d)}
projections = [{(i,i): F(1) for i in block} for block in blocks]
supports = [tensor(p,p) for p in projections]
xi = {}
total_support = {}
for c,p in zip(coeff,supports):
    xi = add(xi,p,c)
    total_support = add(total_support,p)

def left(x, z):
    return tmul(tensor(x,eye),z)

def right(y, z):
    return tmul(tensor(eye,y),z)

def delta0(x):
    # The true real derivation is i*delta0; its energy is unchanged.
    return add(left(x,xi),right(x,xi),F(-1))

def trace(x):
    return sum((v for (i,j),v in x.items() if i==j),F(0))/d

def inner(x, y, normalization):
    return sum((v*y.get(k,F(0)) for k,v in x.items()),F(0))/normalization

def generator(x):
    out = {(i,j):(rates[which[i]]+rates[which[j]])*v
           for (i,j),v in x.items()}
    for c,p in zip(coeff,projections):
        out = add(out,p,-2*c*c*trace(mul(p,x)))
    return clean(out)

basis = [{(i,j):F(1)} for i in range(d) for j in range(d)]
derivs = [delta0(x) for x in basis]
for x,dx in zip(basis,derivs):
    check(jreal(dx)==scaled(delta0(adj(x)),-1),'coarse_reality_sign')
    check(tmul(dx,total_support)==dx,'right_tensor_support')
    for y,dy in zip(basis,derivs):
        check(inner(dx,dy,d*d)==inner(x,generator(y),d),
              'energy_and_generator_gram')
        check(delta0(mul(x,y))==add(left(x,dy),right(y,dx)),
              'opposite_action_leibniz')
check(delta0(eye)=={},'conservativity')

for n,block in enumerate(blocks):
    check(generator(projections[n])=={},'spectral_blocks')
    if len(block)>1:
        z={(block[0],block[0]):F(1),(block[1],block[1]):F(-1)}
        check(generator(z)==scaled(z,2*rates[n]),'spectral_blocks')
        z={(block[0],block[1]):F(1)}
        check(generator(z)==scaled(z,2*rates[n]),'spectral_blocks')
for i in range(d):
    for j in range(d):
        if which[i]!=which[j]:
            x={(i,j):F(1)}
            check(generator(x)==scaled(x,rates[which[i]]+rates[which[j]]),
                  'spectral_blocks')

b = [F(1,2),F(2,3),F(3,5)]
v = [F(2,5),F(3,7),F(4,9)]

def heat(x, params):
    out={(i,j):params[which[i]]*params[which[j]]*a
         for (i,j),a in x.items()}
    for n,(p,qn) in enumerate(zip(projections,q)):
        out=add(out,p,(1-params[n]**2)*trace(mul(p,x))/qn)
    return clean(out)

def kraus_heat(x, params):
    diag={(i,i):params[which[i]] for i in range(d)}
    out=mul(mul(diag,x),diag)
    for n,block in enumerate(blocks):
        weight=(1-params[n]**2)/len(block)
        for i in block:
            for j in block:
                e={(i,j):F(1)}
                out=add(out,mul(mul(e,x),adj(e)),weight)
    return out

for x in basis:
    check(heat(x,b)==kraus_heat(x,b),'positive_kraus_representation')
    check(trace(heat(x,b))==trace(x),'trace_preservation')
    check(heat(adj(x),b)==adj(heat(x,b)),'star_preservation')
    check(heat(heat(x,b),v)==heat(x,[bn*vn for bn,vn in zip(b,v)]),
          'semigroup_composition')
    for y in basis:
        check(inner(x,heat(y,b),d)==inner(heat(x,b),y,d),
              'heat_hilbert_symmetry')
check(heat(eye,b)==eye,'heat_unitality')
for bn,block in zip(b,blocks):
    check((1-bn**2)/len(block)>0,'positive_kraus_weights')

# Exact random-walk distribution by repeated convolution, not binomial sums.
distribution={0:1}
for n in range(1,65):
    nxt=Counter()
    for value,multiplicity in distribution.items():
        nxt[value-1]+=multiplicity
        nxt[value+1]+=multiplicity
    distribution=dict(nxt)
    second=F(sum(value**2*m for value,m in distribution.items()),2**n)
    fourth=F(sum(value**4*m for value,m in distribution.items()),2**n)
    tail=F(sum(m for value,m in distribution.items() if 2*value**2>=n),2**n)
    check(second==n,'rademacher_second_moment')
    check(fourth==3*n*n-2*n,'rademacher_fourth_moment')
    check(tail>=F(1,12),'rademacher_escape_probability')

for n in range(1,65):
    qn=F(1,2**n)
    c_squared=F(2**(2*n),n)
    check(qn*c_squared==F(2**n,n),'infinite_family_rate_identity')
    check(qn*qn*c_squared==F(1,n),'infinite_family_energy_identity')
    check(sum((F(1,2**k) for k in range(1,n+1)),F(0))==1-qn,
          'projection_trace_tail')
for j in range(1,13):
    harmonic=sum((F(1,n) for n in range(1,2**j+1)),F(0))
    check(harmonic>=1+F(j,2),'harmonic_energy_divergence_control')

# Explicit false alternatives, each independently required to fail.
x={(0,2):F(1)}
dx=delta0(x)
reject(tmul(total_support,dx)==dx,'right_support_cannot_be_replaced_by_left_support')
check(tmul(total_support,dx)=={},'off_block_left_support_mixing')
reject(generator({(0,1):F(1)})=={},'diagonal_corner_is_not_all_zero_energy')
reject(generator(x)==scaled(x,coeff[0]**2+coeff[1]**2),
       'generator_rate_must_include_projection_trace')
diag={(i,i):b[which[i]] for i in range(d)}
reject(mul(diag,diag)==eye,'omitting_conditional_expectation_breaks_unitality')
ordinary=add(tmul(tensor(x,eye),xi),tmul(xi,tensor(x,eye)),F(-1))
reject(ordinary==dx,'ordinary_tensor_algebra_commutator_is_not_coarse_derivation')
reject(jreal(dx)==delta0(adj(x)), 'imaginary_implementer_sign_is_essential_for_reality')

result={
    'status':'pass',
    'method':'Independent sparse tensor matrix units and exact rational arithmetic',
    'dimension':d,
    'projection_ranks':[len(block) for block in blocks],
    'projection_traces':[str(z) for z in q],
    'generator_rates':[str(z) for z in rates],
    'independent_assertions_passed':sum(counts.values()),
    'assertions_by_group':dict(counts),
    'negative_controls_rejected':len(negative),
    'negative_controls':negative,
    'rademacher_sizes':{'first':1,'last':64},
    'scope':'Finite algebra/sign/normalization and moment controls only. The full analytic audit supplies all infinite-dimensional claims.'
}
Path(__file__).with_name('audit_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
