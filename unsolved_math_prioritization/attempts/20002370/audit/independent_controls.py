#!/usr/bin/env python3
"""Independent, exact controls for the rational-function-field audit.

No test decides a function-field theory. The controls check syntactic movements,
finite arithmetic, polynomial identities, and the integrity of the reviewed text.
"""
from fractions import Fraction as Q
from itertools import product
from math import factorial
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def main():
    assertions = 0
    def require(condition):
        nonlocal assertions
        if not condition:
            raise AssertionError('independent audit control failed')
        assertions += 1

    # Verify the entire frozen file inventory, sizes, and hashes.
    public = ROOT / 'public'
    manifest_path = public / 'FROZEN_AUTHOR_MANIFEST.json'
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    require({p.name for p in public.iterdir() if p.is_file()} ==
            set(manifest['files']) | {manifest_path.name})
    verified = {}
    for name, record in sorted(manifest['files'].items()):
        b = (public / name).read_bytes()
        digest = hashlib.sha256(b).hexdigest()
        require(len(b) == record['bytes'])
        require(digest == record['sha256'])
        verified[name] = {'bytes': len(b), 'sha256': digest}
    replay = subprocess.check_output([sys.executable, str(public/'check_exact.py')])
    expected_bytes = (public/'exact_results.json').read_bytes()
    require(replay == expected_bytes)
    author_result = json.loads(replay)

    # Expand both existential predicates independently and check that moving
    # their witnesses to the final block preserves truth. J encodes C(u)=Ez J;
    # K encodes G(x,u)=Ey K. H is deliberately otherwise unrestricted.
    domain = (0, 1)
    interpretations = 0
    for hm, jm, km in product(range(16), range(16), range(256)):
        H = lambda x, v: (hm >> (2*x+v)) & 1
        J = lambda u, z: (jm >> (2*u+z)) & 1
        K = lambda x, u, y: (km >> (4*x+2*u+y)) & 1
        C = lambda u: any(J(u, z) for z in domain)
        G = lambda x, u: any(K(x, u, y) for y in domain)
        branch = all((not any(H(x, v) for v in domain)) or
                     all(C(u) or G(x, u) for u in domain) for x in domain)
        expanded = all(any((not H(x, v)) or J(u, z) or K(x, u, y)
                           for z, y in product(domain, repeat=2))
                       for x, v, u in product(domain, repeat=3))
        require(branch == expanded)
        interpretations += 1

    # Explicit relational counterexample satisfying the stronger geometric
    # implication H(x,v) => C(x) and C(v). It is not a field.
    H = {(0, 0)}
    C = {0}
    full = all((x,v) not in H or u in C for x,v,u in product(domain,repeat=3))
    diagonal = all((x,u) not in H or u in C for x,u in product(domain,repeat=2))
    require(all(x in C and v in C for x,v in H))
    require(not full and diagonal)

    # Direct finite sums (not the author's digit recurrence) check the first
    # cut failure, the strict boundary, and a positive finite tail.
    cuts = []
    for m in range(2, 7):
        old_positions = [factorial(j) for j in range(1,m+1)]
        stop = factorial(m+1)
        q = sum((Q(1, 1 << i) for i in old_positions), Q(0))
        failures = []
        for n in range(1,stop+1):
            positions = [i for i in old_positions+[stop] if i <= n]
            B = sum(1 << (n-i) for i in positions)
            deviation = abs((1 << n)*q-B)
            require(deviation < 1 if n < stop else deviation == 1)
            if deviation >= 1:
                failures.append(n)
        require(failures == [stop])
        # The next partial sum is strictly inside the radius at each earlier n.
        later = q + Q(1,1 << stop) + Q(1,1 << (stop+1))
        # A finite synthetic tail also checks the geometric-tail bound exactly.
        require(0 < later-q < Q(2,1 << stop))
        cuts.append({'m':m,'first_failure':stop,'boundary_value':'1'})

    offsets=[]
    for p in (2,3,5,7):
        series = sum((Q(1,p**factorial(j)) for j in range(7)), Q(0))
        distinct = sum((Q(1,p**i) for i in sorted({factorial(j) for j in range(7)})),Q(0))
        first_offset = 1+distinct-series
        center_offset = (2+distinct)-(series-1)
        require(series-distinct == Q(1,p))
        require(first_offset == 1-Q(1,p))
        require(center_offset == 3-Q(1,p))
        offsets.append({'base':p,'printed_series_identity_offset':str(first_offset),
                        'polynomial_center_minus_labeled_cut':str(center_offset)})

    # Exact Bezout identity f - (x/4) f' = 1 for f=x^4+1.
    f = [Q(1),Q(0),Q(0),Q(0),Q(1)]
    xp_over_four = [Q(0),Q(0),Q(0),Q(0),Q(1)]
    bezout = [a-b for a,b in zip(f,xp_over_four)]
    require(bezout == [Q(1),Q(0),Q(0),Q(0),Q(0)])
    require((-4+4)//2+1 == 1)  # Double cover, four simple branch points.

    # Polynomial arithmetic cross-multiplication control. Terms are kept as
    # numerator/denominator pairs and no degree truncation is applied to terms.
    def add(a,b):
        z=[0]*max(len(a),len(b))
        for i,c in enumerate(a): z[i]+=c
        for i,c in enumerate(b): z[i]+=c
        return trim(z)
    def trim(a):
        while len(a)>1 and a[-1]==0: a.pop()
        return a
    def mul(a,b):
        z=[0]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b): z[i+j]+=x*y
        return trim(z)
    def neg(a): return [-c for c in a]
    def radd(x,y): return (add(mul(x[0],y[1]),mul(y[0],x[1])),mul(x[1],y[1]))
    def rneg(x): return (neg(x[0]),x[1])
    def rmul(x,y): return (mul(x[0],y[0]),mul(x[1],y[1]))
    polys=[[1],[0,1],[1,1],[1,0,1],[-2,3,1]]
    cross_cases=0
    for p,q,r,s in product(polys,repeat=4):
        x,y=(p,q),(r,s)
        lhs=rmul(radd(x,y),radd(x,rneg(y)))
        rhs=radd(rmul(x,x),rneg(rmul(y,y)))
        require(mul(lhs[0],rhs[1])==mul(rhs[0],lhs[1]))
        cross_cases+=1
    # A nonidentity can vanish at individual specializations; finitely many
    # excluded zeros matter in the existential-closedness argument.
    require(add([1,0,1],neg(mul([0,1],[1,1]))) == [1,-1])

    result = {
        'status':'pass',
        'scope':'Integrity, finite exact arithmetic, and logical/polynomial controls only; not a field-theory proof or decision procedure.',
        'assertions':assertions,
        'reviewed_manifest_sha256':hashlib.sha256(manifest_bytes).hexdigest(),
        'reviewed_files':verified,
        'author_replay_byte_exact':True,
        'author_assertions':author_result['assertions'],
        'existential_expansion_interpretations':interpretations,
        'guarded_diagonal_countermodel':{'domain':[0,1],'H':[[0,0]],'C':[0],'G':[],
                                        'full':False,'diagonal':True},
        'direct_cut_checks':cuts,
        'normalization_offsets':offsets,
        'quartic_bezout_identity':'(1+x^4) - (x/4)*(4*x^3) = 1',
        'cross_multiplication_cases':cross_cases,
    }
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
