#!/usr/bin/env python3
"""Independent exact checks of the frozen packet. Requires Python 3 and SymPy.

Does not import or execute the author verifier. Run from any directory; optionally
pass the public packet directory as the first argument. Certificate leaf paths
are treated as untrusted hints and rechecked by direct affine substitution.
"""
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations
from math import comb, factorial
from pathlib import Path
import sympy as sp

PUBLIC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'public'
EXPECTED_MANIFEST = '66b9a66708d98e240528d2680d8faea6cb0b1ff01d6f229efb7412dbacb4e1f4'

def check_freeze():
    manifest = (PUBLIC / 'MANIFEST.sha256').read_bytes()
    assert hashlib.sha256(manifest).hexdigest() == EXPECTED_MANIFEST
    listed = []
    for line in manifest.decode().splitlines():
        digest, name = line.split()
        assert '/' not in name
        assert hashlib.sha256((PUBLIC / name).read_bytes()).hexdigest() == digest
        listed.append(name)
    assert len(listed) == 8
    assert {p.name for p in PUBLIC.iterdir()} == set(listed + ['MANIFEST.sha256'])
    return {'manifest_sha256': EXPECTED_MANIFEST, 'file_count': 9}


def c40():
    edges = list(combinations(range(5), 2))
    vectors = []
    for omitted in range(5):
        local = [e for e in edges if omitted not in e]
        for bits in range(64):
            negative = {local[j] for j in range(6) if bits & (1 << j)}
            degrees = {v: sum(v in e for e in negative) % 2 for v in range(5)}
            parity = len(negative) % 2
            if any(degrees[(omitted + j) % 5] != (parity if j in (1, 2) else 1 - parity) for j in range(1, 5)):
                continue
            vectors.append([0 if omitted in e else (-1 if e in negative else 1) for e in edges])
    assert len(set(map(tuple, vectors))) == 40
    X = sp.Matrix(vectors)
    return X * X.T


def mul8(a, b):
    p = 0
    for i in range(3):
        for j in range(3):
            if (a >> i) & 1 and (b >> j) & 1:
                p ^= 1 << (i + j)
    for i in (4, 3):
        if p & (1 << i):
            p ^= 0b1011 << (i - 3)
    return p


def c64():
    assert all(mul8(a,b) == mul8(b,a) for a in range(8) for b in range(8))
    assert all(any(mul8(a,b) == 1 for b in range(1,8)) for a in range(1,8))
    H = []
    for p in range(64):
        a,b = divmod(p,8)
        row = []
        for q in range(64):
            c,d = divmod(q,8)
            s = a ^ c
            row.append(7 if p == q else -1 if a == c else
                       -3 if (b ^ d) in (mul8(mul8(s,s),s),mul8(mul8(a,c),s)) else 1)
        H.append(row)
    return sp.Matrix(H)


def gegenbauer(n,t,k):
    # Direct finite Laplace-moment expansion, independent of the recurrence.
    moment = Q(1)
    total = Q(0)
    for j in range(k//2 + 1):
        if j:
            moment *= Q(2*j-1,n+2*j-3)
        total += comb(k,2*j) * t**(k-2*j) * (-1)**j * (1-t*t)**j * moment
    return total


def code_check(H,n,d,L,expected):
    N = H.rows
    assert H == H.T and H.diagonal() == sp.ones(1,N)*d
    assert H*H == (N*d//n)*H
    assert H.rank() == n
    assert H*sp.ones(N,1) == sp.zeros(N,1)
    assert sum(int(v)**3 for v in H) == 0
    for i in range(N):
        assert Counter(int(H[i,j]) for j in range(N) if i != j) == expected
    for h,m in expected.items():
        A = H.applyfunc(lambda v: int(v == h))
        assert H*A == sp.Rational(m*h,d)*H
    certs=[]
    for i in range(N):
        V = d*H-H[:,i]*H[i,:]
        _,I = V.rref()
        assert len(I) == n-1
        T = V.extract(I,I)
        # Positive-definite Gram basis, checked by all leading principal minors.
        assert all(T[:j,:j].det() > 0 for j in range(1,n))
        J = [j for j in range(N) if H[i,j] == max(expected)]
        M = V.extract(I,J)*V.extract(J,I)-sp.Rational(L.numerator,L.denominator)*d*d*T
        assert M == M.T
        coeff = M.charpoly().all_coeffs()
        # det(x I + M) has nonnegative coefficients. For real symmetric M,
        # it cannot have a negative eigenvalue, which would give a positive root.
        signed = [int(c)*(-1)**j for j,c in enumerate(coeff)]
        assert all(c >= 0 for c in signed)
        rank = max(j for j,c in enumerate(signed) if c)
        assert rank == (6 if N == 40 else 7)
        for k in (1,2,3):
            Qmat = sp.zeros(n-1)
            for j in range(N):
                if j == i: continue
                t = sp.Rational(H[i,j],d)
                gp = k*(1+t)**(k-1)
                gpp = 0 if k==1 else k*(k-1)*(1+t)**(k-2)
                col = V.extract(I,[j])
                Qmat += gpp*col*col.T-d*d*gp*t*T
            assert Qmat == k*2**(k-1)*d*d*T
        certs.append({'point':i,'basis':list(I),'bound_rank':rank,
                      'det_xI_plus_M_coefficients':list(map(str,signed))})
    moments=[1+sum(m*gegenbauer(n,Q(h,d),k) for h,m in expected.items()) for k in range(1,8)]
    assert moments[:3] == [0,0,0] and all(m>0 for m in moments[3:])
    b=max(Q(h*h,d*d) for h in expected)
    momentsU=[Q(1)]
    for j in range(1,5): momentsU.append(momentsU[-1]*Q(2*j-1,n+2*j-3))
    tail=sum(comb(4,j)*b**(4-j)*(1-b)**j*momentsU[j] for j in range(5))
    margin=1-(N-1)*tail
    assert margin>0
    s=Q(max(expected),d)
    q4=3*L/(1+s)-expected[max(expected)]*s
    assert q4>0
    return {'N':N,'dimension':n,'rank':n,'tangent_certificate_count':len(certs),
            'frame_certificates':certs,'moments_degrees_1_to_7':list(map(str,moments)),
            'tail_bound':str(tail),'tail_margin':str(margin),'quartic_bracket':str(q4)}


def pmul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c


def polynomial_gap(k):
    # Expand the pair-energy bases by repeated multiplication, not binomial code.
    bases=[(48,[12]),(72,[20]),(96,[18,-54]),(288,[18,18]),
           (72,[0,0,648]),(36,[36,0,-648]),(96,[36,0,-486]),(72,[0,0,324]),
           (-160,[9]),(-60,[12]),(-80,[18]),(-480,[21])]
    p=[0]*(2*k+1)
    for weight,base in bases:
        term=[1]
        for _ in range(k): term=pmul(term,base)
        for i,c in enumerate(term): p[i]+=weight*c
    return p


def certify_leaf_direct(p,path):
    # a=(ell+x)/den for x in [0,1]. Clear den^D, then convert the
    # resulting power polynomial to Bernstein form with a positive D! scale.
    D=len(p)-1
    ell=int(path,2) if path else 0
    den=5*2**len(path)
    affine=[sum(p[i]*comb(i,j)*ell**(i-j)*den**(D-i) for i in range(j,D+1)) for j in range(D+1)]
    weights=[affine[i]*factorial(i)*factorial(D-i) for i in range(D+1)]
    coeff=[sum(weights[i]*comb(j,i) for i in range(j+1)) for j in range(D+1)]
    assert min(coeff)>0
    return hashlib.sha256((' '.join(map(str,coeff))).encode()).hexdigest()


def rival_check(hints):
    P=list(permutations(range(4)))
    sign=lambda p:(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
    # Reconstruct the tensor-grid Gram and the projection inner products.
    grid=list((i,j) for i in range(4) for j in range(4))
    tet=lambda i,j:Q(1) if i==j else Q(-1,3)
    gram=lambda ij,kl:tet(ij[0],kl[0])*tet(ij[1],kl[1])
    assert Counter(gram(u,v) for u,v in combinations(grid,2)) == {Q(-1,3):48,Q(1,9):72}
    for p in P:
        for i,j in grid:
            assert -Q(9,4)*sum(gram((r,p[r]),(i,j)) for r in range(4)) == (-3 if p[i]==j else 1)
        assert Q(81,16)*sum(gram((r,p[r]),(s,p[s])) for r in range(4) for s in range(4)) == 27
    pairs=Counter()
    for p,q in combinations(P,2):
        projection=Q(81,16)*sum(gram((r,p[r]),(s,q[s])) for r in range(4) for s in range(4))
        eps=sign(p)*sign(q)
        pairs[(eps,projection-27*eps)]+=1
    assert pairs == {(-1,Q(36)):72,(1,Q(-36)):36,(1,Q(-27)):96,(-1,Q(18)):72}
    assert polynomial_gap(0)==[0] and polynomial_gap(1)==[0,0,0]
    assert polynomial_gap(2)==[72000,0,-4665600,0,75582720]
    leaves=[]
    for k in range(3,100):
        p=polynomial_gap(k)
        paths=hints[str(k)]
        # Check complete disjoint cover, not just total dyadic length.
        intervals=sorted((Q(int(s,2) if s else 0,2**len(s)),Q((int(s,2) if s else 0)+1,2**len(s))) for s in paths)
        assert intervals[0][0]==0 and intervals[-1][1]==1
        assert all(intervals[j][1]==intervals[j+1][0] for j in range(len(intervals)-1))
        for path in paths:
            leaves.append({'k':k,'path':path,'positive_coefficients_sha256':certify_leaf_direct(p,path)})
    assert len(leaves)==351 and max(len(c['path']) for c in leaves)==9
    assert Q(7,6)**100>300
    assert 288*Q(176,175)**100>481
    assert 96*Q(4458,4375)**100>481
    return {'power_count':97,'leaf_count':len(leaves),'max_depth':9,'leaf_certificates':leaves,
            'tail_base_cases_exact':True}


def hermite_check():
    t=sp.Symbol('t')
    output=[]
    for n,nodes,counts,expected in (
        (10,[-sp.Rational(1,2),-sp.Rational(1,3),sp.Integer(0),sp.Rational(1,6)],
         [160,60,80,480],[sp.Rational(500,9),sp.Rational(80,9),sp.Rational(40,27),0]),
        (14,[-sp.Rational(3,7),-sp.Rational(1,7),sp.Rational(1,7)],
         [448,224,1344],[sp.Rational(12288,343),0])):
        p=sp.Integer(1)
        energies=[]
        for i,node in enumerate([r for r in nodes for _ in range(2)]):
            energies.append(sp.expand(sum(m*p.subs(t,r) for m,r in zip(counts,nodes))))
            if i<4: assert all(c>=0 for c in sp.Poly(p,t).all_coeffs())
            p *= t-node
        assert energies[4:]==expected
        output.append({'dimension':n,'remaining_inequalities':len(expected),
                       'target_energies':list(map(str,energies))})
    return output


def main():
    freeze=check_freeze()
    hints=json.loads((PUBLIC/'CHECK_RESULTS.json').read_text())['rival_family']['dyadic_Bernstein_leaf_paths']
    result={'freeze':freeze,'arithmetic':'Exact integers/rationals, SymPy '+sp.__version__,
            'codes':[code_check(c40(),10,6,Q(2),Counter({-3:8,-2:3,0:4,1:24})),
                     code_check(c64(),14,7,Q(20,7),Counter({-3:14,-1:7,1:42}))],
            'rival':rival_check(hints),'hermite':hermite_check()}
    assert check_freeze()==freeze
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__': main()
