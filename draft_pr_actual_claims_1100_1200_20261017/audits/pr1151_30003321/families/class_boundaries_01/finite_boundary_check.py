#!/usr/bin/env python3
"""Finite falsification checks, not a proof for transfinite signs or class groups."""
import itertools, json, hashlib, datetime, random
from fractions import Fraction
from functools import cmp_to_key
from pathlib import Path

def prefixes(s):
    return tuple(s[:i] for i in range(len(s)))

def cmp(s,t):
    for a,b in zip(s,t):
        if a!=b: return -1 if a=='-' else 1
    if len(s)==len(t): return 0
    if len(s)<len(t): return -1 if t[len(s)]=='+' else 1
    return 1 if s[len(t)]=='+' else -1

def surgery(s,alpha):
    a='-'*alpha
    if s==a: return ''
    assert cmp(s,a)>0
    if not s.startswith(a): return '+'+s
    assert s[alpha]=='+'
    return '+'+a+s[alpha+1:]

def all_signs(depth):
    return [''.join(t) for n in range(depth+1) for t in itertools.product('-+',repeat=n)]

def independent_minimum_first_cuts(domain,minimum,candidates):
    # Independently realizes the sealed pre-candidate mechanism: minimum first,
    # then birthday order, and shortest separating finite sign sequence.
    image={minimum:''}
    ordered=sorted((s for s in domain if s!=minimum),key=lambda s:(len(s),s))
    for s in ordered:
        lowers=[v for t,v in image.items() if cmp(t,s)<0]
        uppers=[v for t,v in image.items() if cmp(t,s)>0]
        lo=max(lowers,key=cmp_to_key(cmp)) if lowers else None
        hi=min(uppers,key=cmp_to_key(cmp)) if uppers else None
        good=[v for v in candidates if (lo is None or cmp(lo,v)<0) and (hi is None or cmp(v,hi)<0)]
        assert good
        n=len(good[0]); shortest=[v for v in good if len(v)==n]
        assert len(shortest)==1, (s,shortest)
        image[s]=shortest[0]
    return image

def add(x,y):
    z=dict(x)
    for k,v in y.items():
        z[k]=z.get(k,Fraction(0))+v
        if not z[k]: del z[k]
    return z

def sign(x):
    if not x: return 0
    k=max(x,key=cmp_to_key(cmp))
    return 1 if x[k]>0 else -1

def transform(x,alpha,n):
    a='-'*alpha
    return {surgery(k,alpha):v*(2**n if k==a else 1) for k,v in x.items()}

def inverse_surgery(z,alpha):
    a='-'*alpha
    if not z: return a
    assert z[0]=='+'
    v=z[1:]
    return a+'+'+v[alpha:] if v.startswith(a) else v

rng=random.Random(115130003321)
depth=8
nodes=all_signs(depth)
candidates=all_signs(depth+1)
counts={'domains':0,'nodes':0,'ordered_node_pairs':0,'prefix_sets':0,'independent_cut_matches':0,'coefficient_trials':0}
by_alpha=[]
for alpha in range(depth+1):
    a='-'*alpha
    domain=[s for s in nodes if cmp(s,a)>=0]
    f={s:surgery(s,alpha) for s in domain}
    assert len(set(f.values()))==len(domain)
    assert f[a]==''
    assert all(not z or z[0]=='+' for z in f.values())
    independent=independent_minimum_first_cuts(domain,a,candidates)
    for s in domain:
        assert f[s]==independent[s], (alpha,s,f[s],independent[s])
        assert inverse_surgery(f[s],alpha)==s
        expected={''}|{f[v] for v in prefixes(s) if v!=a} if s!=a else set()
        assert set(prefixes(f[s]))==expected, (alpha,s,f[s],expected)
        counts['prefix_sets']+=1
        counts['independent_cut_matches']+=1
        for t in domain:
            assert cmp(s,t)==cmp(f[s],f[t])
            if s!=a and t!=a:
                assert (s in prefixes(t))==(f[s] in prefixes(f[t]))
            if f[s] in prefixes(f[t]) and cmp(f[s],f[t])>0:
                assert s in prefixes(t) and cmp(s,t)>0
            counts['ordered_node_pairs']+=1
    for trial in range(300):
        n=trial%6
        def vector():
            chosen=rng.sample(domain,min(len(domain),rng.randrange(1,7)))
            # All non-bottom coefficients are sampled from D, and the bottom
            # from 2^-n Z: legal coefficient groups for every tested domain.
            return {k:(Fraction(rng.randrange(-9,10),2**(n if k==a else rng.randrange(0,5)))) for k in chosen}
        x,y=vector(),vector()
        x={k:v for k,v in x.items() if v}; y={k:v for k,v in y.items() if v}
        assert transform(add(x,y),alpha,n)==add(transform(x,alpha,n),transform(y,alpha,n))
        assert sign(x)==sign(transform(x,alpha,n))
        image=transform(x,alpha,n)
        restored={inverse_surgery(k,alpha):v/(2**n if inverse_surgery(k,alpha)==a else 1) for k,v in image.items()}
        assert restored==x
        counts['coefficient_trials']+=1
    counts['domains']+=1; counts['nodes']+=len(domain)
    by_alpha.append({'alpha':alpha,'domain_nodes':len(domain),'largest_image_length':max(map(len,f.values()))})
report={'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','max_finite_birthday':depth,'counts':counts,'by_alpha':by_alpha,'scope':'Finite sign trees; all ordered pairs, all prefix sets, comparison with independent minimum-first simplest-cut realization; sampled rational coefficient addition/sign/inverse. No transfinite or class-size claim is inferred from this computation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
