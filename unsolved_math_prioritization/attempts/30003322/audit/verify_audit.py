#!/usr/bin/env python3
"""Independent exact controls; no external packages, network, or source mutation.
Usage: python3 verify_audit.py [path-to-original-safe-package]
Finite checks do not certify surreal initiality or model-theoretic universals.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib, json, random, subprocess, sys

EXPECTED_MANIFEST = '4a0a5cece35d143c2ebdf3683f0a7a115588f2a42b5730af77ac21aee7a84a54'

def clean(p):
    return {e: Q(c) for e,c in p.items() if c}

def add(p,q):
    z=dict(p)
    for e,c in q.items(): z[e]=z.get(e,Q(0))+c
    return clean(z)

def scale(p,c):
    return clean({e:v*c for e,v in p.items()})

def mul(p,q):
    z={}
    for e,c in p.items():
        for f,d in q.items(): z[e+f]=z.get(e+f,Q(0))+c*d
    return clean(z)

def sign_laurent(p):
    p=clean(p)
    return (p[min(p)]>0)-(p[min(p)]<0) if p else 0

def signcmp(s,t):
    for i in range(max(len(s),len(t))):
        a=s[i] if i<len(s) else 0
        b=t[i] if i<len(t) else 0
        if a!=b:return (a>b)-(a<b)
    return 0

def run(original=None):
    out={}
    if original is not None:
        mbytes=(original/'MANIFEST.json').read_bytes()
        assert hashlib.sha256(mbytes).hexdigest()==EXPECTED_MANIFEST
        manifest=json.loads(mbytes)
        listed=set()
        for ent in manifest['files']:
            d=(original/ent['path']).read_bytes()
            assert len(d)==ent['bytes']
            assert hashlib.sha256(d).hexdigest()==ent['sha256']
            listed.add(ent['path'])
        assert {p.name for p in original.iterdir() if p.is_file()}==listed|{'MANIFEST.json'}
        replay=subprocess.run([sys.executable,'-B',str(original/'check_controls.py')],capture_output=True,check=True)
        assert json.loads(replay.stdout)==json.loads((original/'CONTROL_RESULTS.json').read_text())
        out['original_manifest_and_nine_payloads']='PASS'
        out['original_replay_json_equal']=True
        out['original_replay_byte_equal']=replay.stdout==(original/'CONTROL_RESULTS.json').read_bytes()
    # Exhaustive finite analogue of the crucial first-disagreement assertion.
    seqs=[s for n in range(10) for s in product((-1,1),repeat=n)]
    bounds=[s for s in seqs if len(s)<=6]
    pairs=successes=0
    for s in bounds:
        L=[s[:i] for i in range(len(s)) if s[i]==1]
        R=[s[:i] for i in range(len(s)) if s[i]==-1]
        for y in seqs:
            between=all(signcmp(l,y)<0 for l in L) and all(signcmp(y,r)<0 for r in R)
            extends=len(y)>=len(s) and y[:len(s)]==s
            assert between==extends
            pairs+=1;successes+=between
    out['prefix_cut_pairs_exhaustively_checked']=pairs
    out['prefix_cut_extensions']=successes
    # Independent generating-function representation: p(t)+a/(1-t).
    # Numerator N=(1-t)p+a has N(1)=a, so infinite-tail membership
    # is controlled by evaluation at 1, not by finite coefficients.
    rng=random.Random(66430003322)
    for _ in range(2000):
        p={i:Q(rng.randint(-30,30),rng.randint(1,11)) for i in range(rng.randrange(12))}
        a=Q(rng.randint(-20,20))
        N=add(mul(p,{0:Q(1),1:Q(-1)}),{0:a})
        assert sum(N.values(),Q(0))==a
        d=rng.randint(1,12)
        assert sum(scale(N,Q(1,d)).values(),Q(0))==a/d
        # Coefficients of N/(1-t) are its partial sums, hence eventually N(1).
        coeff=[sum((v for i,v in N.items() if i<=j),Q(0)) for j in range(20)]
        assert coeff[-1]==a
        assert all(coeff[i]==Q(p.get(i,0))+a for i in range(20))
    out['generating_function_tail_trials']=2000
    out['tail_one_over_two_not_integral']=Q(1,2).denominator!=1
    out['tail_one_over_three_not_dyadic']=Q(1,3).denominator & (Q(1,3).denominator-1)!=0
    # Independent squarefreeness certificate: f - (u/n) f' = 1.
    for n in range(1,513):
        f={0:Q(1),n:Q(1)}
        df={n-1:Q(n)}
        assert add(f,scale(mul({1:Q(1)},df),Q(-1,n)))=={0:Q(1)}
    out['squarefree_bezout_certificates_n_1_to_512']=512
    # Integer-part branches, including negative constants and either infinitesimal sign.
    branches={'nonintegral_constant':0,'integral_nonnegative_tail':0,'integral_negative_tail':0}
    for _ in range(3000):
        p=clean({i:Q(rng.randint(-20,20),rng.randint(1,7)) for i in range(-6,7)})
        c=p.get(0,Q(0)); tail={i:v for i,v in p.items() if i>0}
        k=c.numerator//c.denominator
        if c.denominator==1:
            if sign_laurent(tail)<0:k-=1;branches['integral_negative_tail']+=1
            else:branches['integral_nonnegative_tail']+=1
        else:branches['nonintegral_constant']+=1
        z=clean({**{i:v for i,v in p.items() if i<0},0:Q(k)})
        diff=add(p,scale(z,-1))
        assert sign_laurent(diff)>=0
        assert sign_laurent(add({0:Q(1)},scale(diff,-1)))>0
        assert all(i<=0 for i in z) and z.get(0,Q(0)).denominator==1
    assert all(branches.values())
    out['integer_part_laurent_trials']=3000
    out['integer_part_branches']=branches
    # Positive rational surreal powers + integer constants form a ring.
    for _ in range(1000):
        def sample():
            d={Q(0):Q(rng.randint(-10,10))}
            for _ in range(8):
                e=Q(rng.randint(1,30),rng.randint(1,12))
                d[e]=d.get(e,Q(0))+Q(rng.randint(-10,10),rng.randint(1,9))
            return clean(d)
        a,b=sample(),sample()
        for c in [add(a,b),mul(a,b),scale(a,-1)]:
            assert all(e>=0 for e in c)
            assert c.get(Q(0),Q(0)).denominator==1
    out['integer_part_ring_trials']=1000
    # Bezout decomposition for D + Z[1/3] = Z[1/6].
    bezout=0
    for a in range(1,21):
        for b in range(1,21):
            two,three=2**a,3**b
            A=pow(three,-1,two)
            B=(1-A*three)//two
            assert Q(A,two)+Q(B,three)==Q(1,two*three)
            bezout+=1
    out['localization_hull_bezout_cases']=bezout
    out['status']='PASS'
    out['limits']=[
        'Finite rational-coefficient controls, not a formal proof of surreal arithmetic or arbitrary real coefficients.',
        'Squarefreeness for all positive n, initiality, and infinite-support claims require the accompanying proofs.',
        'No control establishes either universal set-model converse or independence from NBG.'
    ]
    return out

if __name__=='__main__':
    p=Path(sys.argv[1]) if len(sys.argv)>1 else None
    print(json.dumps(run(p),indent=2))
