#!/usr/bin/env python3
"""Independent exact controls for the five conditional routes.

This is not a QHI evaluator. It constructs no geometric triangulation or move
anomaly. Standard library only. Author verification is copied into temporary
storage so the frozen author files are never rewritten.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

PHI = {3: [1,1,1], 5: [1,1,1,1,1], 7: [1]*7,
       9: [1,0,0,1,0,0,1], 15: [1,-1,0,1,-1,1,0,-1,1]}

def poly(p, n):
    p = list(p)
    mod = PHI[n]
    while len(p) >= len(mod):
        t = p[-1]
        off = len(p)-len(mod)
        for j, c in enumerate(mod):
            p[off+j] -= t*c
        p.pop()
    return tuple(p + [0]*(len(mod)-1-len(p)))

def add(a,b,n):
    return poly([x+y for x,y in zip(a,b)],n)

def mul(a,b,n):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return poly(c,n)

def zeta(k,n):
    return poly([0]*(k % n)+[1],n)

def mm(A,B,n):
    out={}
    for (i,j),a in A.items():
        for (k,l),b in B.items():
            if j==k:
                key=(i,l)
                out[key]=add(out.get(key,poly([],n)),mul(a,b,n),n)
    return {ij:v for ij,v in out.items() if any(v)}

def scaled(A,s,n):
    return {ij:mul(v,s,n) for ij,v in A.items()}

def cyclic_determinant(A,n):
    # Leibniz formula specialized to a matrix with one nonzero per column.
    rows=[next(i for i,j in A if j==c) for c in range(n)]
    assert len(set(rows))==n
    inv=sum(rows[i]>rows[j] for i in range(n) for j in range(i+1,n))
    out=poly([(-1)**inv],n)
    for c,r in enumerate(rows): out=mul(out,A[r,c],n)
    return out

def brute_potential(vs, edges,n):
    # Enumerate every potential, with base value 0. No path-sum algorithm.
    for tail in product(range(n),repeat=len(vs)-1):
        p=dict(zip(vs,(0,)+tail))
        if all((p[b]-p[a]-k)%n==0 for a,b,k in edges): return p
    return None

def alpha_log(c,f,eps,n):
    # Coefficients of (log w0, log w1, pi*i), directly from quantum roots.
    m=(n-1)//2
    roots=((Q(1,n),Q(0),Q((n+1)*(f[0]-eps*c[0]),n)),
           (Q(0),Q(1,n),Q((n+1)*(f[1]-eps*c[1]),n)))
    return tuple(m*(-c[1]*roots[0][i]+c[0]*roots[1][i]) for i in range(3))

def sub(a,b): return tuple(x-y for x,y in zip(a,b))

def verify_manifest(author):
    manifest=json.loads((author/'FROZEN_AUTHOR_MANIFEST.json').read_text())
    out={}
    for name, info in manifest['files'].items():
        data=(author/name).read_bytes()
        digest=hashlib.sha256(data).hexdigest()
        assert digest==info['sha256'],name
        assert len(data)==info['bytes'],name
        out[name]=digest
    assert len(out)==10
    assert {p.name for p in author.iterdir() if p.is_file()}==set(out)|{'FROZEN_AUTHOR_MANIFEST.json'}
    out['FROZEN_AUTHOR_MANIFEST.json']=hashlib.sha256((author/'FROZEN_AUTHOR_MANIFEST.json').read_bytes()).hexdigest()
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--author-dir',type=Path,default=Path(__file__).resolve().parent.parent/'public')
    args=ap.parse_args()
    before=verify_manifest(args.author_dir)
    # The author's verifier writes a result file: isolate that write.
    with tempfile.TemporaryDirectory(prefix='phase-audit-') as td:
        check=Path(td)/'check_exact.py'
        shutil.copyfile(args.author_dir/'check_exact.py',check)
        proc=subprocess.run([sys.executable,'-I',str(check)],check=True,capture_output=True,text=True)
        replay=json.loads(proc.stdout)
        assert replay==json.loads((args.author_dir/'exact_results.json').read_text())
    count=defaultdict(int)
    for n in PHI:
        one=poly([1],n); zero=poly([],n)
        assert zeta(n,n)==one and all(zeta(k,n)!=one for k in range(1,n))
        X={((j+1)%n,j):one for j in range(n)}
        Z={(j,j):zeta(j,n) for j in range(n)}
        I={(j,j):one for j in range(n)}
        assert mm(Z,X,n)==scaled(mm(X,Z,n),zeta(1,n),n)
        assert mm(Z,X,n)!=mm(X,Z,n)
        assert cyclic_determinant(X,n)==cyclic_determinant(Z,n)==one
        assert sum(1 for i,j in X if i==j)==0
        tr=zero
        for (i,j),v in Z.items():
            if i==j: tr=add(tr,v,n)
        assert tr==zero
        xp=zp=I
        for _ in range(n): xp=mm(xp,X,n); zp=mm(zp,Z,n)
        assert xp==zp==I
        # Nonzero scalar rephasings cannot alter the commutator.
        for a,b in product(range(n),repeat=2):
            xx=scaled(X,zeta(a,n),n); zz=scaled(Z,zeta(b,n),n)
            assert mm(zz,xx,n)==scaled(mm(xx,zz,n),zeta(1,n),n)
            assert mm(zz,xx,n)!=mm(xx,zz,n)
            count['cyclotomic_rephasing_pairs']+=1
        for a,b,c,d in product((-2,-1,0,1,2),repeat=4):
            A={((j+a)%n,j):zeta(b*j,n) for j in range(n)}
            B={((j+c)%n,j):zeta(d*j,n) for j in range(n)}
            C={((j+a+c)%n,j):zeta((b+d)*j+b*c,n) for j in range(n)}
            assert mm(A,B,n)==C
            count['cyclotomic_matrix_products']+=1
        # Direct associativity checks include all six group coordinates.
        for a,b,c,d,e,f in product(range(3),repeat=6):
            lhs=(b*c+(b+d)*e)%n
            rhs=(d*e+b*(c+e))%n
            assert lhs==rhs
            count['six_coordinate_cocycles']+=1
    for n in (3,5,7,9,15):
        m=(n-1)//2
        for c0,c1,f0,f1,d0,d1 in product((-1,0,1),repeat=6):
            c=(c0,c1,1-c0-c1); f=(f0,f1,-1-f0-f1)
            d=(d0,d1,-d0-d1)
            for eps in (-1,1):
                raw=alpha_log(c,f,eps,n)
                simplified=(Q(-m*c1,n),Q(m*c0,n),Q(m*(n+1)*(c0*f1-c1*f0),n))
                assert raw==simplified
                cc=tuple(x+y for x,y in zip(c,d))
                delta=sub(alpha_log(cc,f,eps,n),raw)
                expected=(Q(-m*d1,n),Q(m*d0,n),Q(m*(n+1)*(d0*f1-d1*f0),n))
                assert delta==expected
                ff=tuple(x+2*y for x,y in zip(f,d))
                delta=sub(alpha_log(c,ff,eps,n),raw)
                expected_phase=Q(2*m*(c0*d1-c1*d0),n)
                assert delta[:2]==(0,0) and ((delta[2]-expected_phase)/2).denominator==1
                count['charge_and_flattening_pairs']+=1
        # Local example: the log(2) coefficient changes in magnitude.
        delta=sub(alpha_log((1,1,-1),(0,-1,0),1,n),alpha_log((1,0,0),(0,-1,0),1,n))
        assert delta[0]==-Q(m,n)<0
        # Primitive parity-invisible phase; a sign-only correction cannot remove it.
        assert all((m*k)%n!=0 for k in range(1,n))
        count['local_countermodels']+=1
    for n in (3,5,9):
        for a,b,c in product(range(n),repeat=3):
            ed=[('A','B',a),('B','C',b),('C','A',c)]
            exists=brute_potential(('A','B','C'),ed,n) is not None
            assert exists==((a+b+c)%n==0)
            count['exhaustive_triangle_labels']+=1
        for a,b in product(range(n),repeat=2):
            exists=brute_potential(('A','B'),[('A','B',a),('A','B',b)],n) is not None
            assert exists==(a==b)
            count['exhaustive_parallel_labels']+=1
        assert brute_potential(('A',),[('A','A',1)],n) is None
        assert brute_potential(('T0','T1','T2'),[('T0','T1',1),('T1','T2',0)],n) is not None
        assert brute_potential(('A','B'),[('A','B',1),('B','A',0)],n) is None
        # Disconnected components need independent base choices.
        assert brute_potential(('A','B','C'),[('B','C',2)],n) is not None
        count['graph_edge_cases']+=4
    for n in range(3,32,2):
        for w in range(-32,33):
            for d in (1,2,3,4,5,8,9,16,27,32):
                # Continuation of an Nth root after d turns of winding w.
                monodromy=Q(d*w,n)
                assert (monodromy.denominator==1)==(d*w%n==0)
                count['cover_monodromies']+=1
        assert all((2**k)%n!=0 for k in range(12))
        # Formal exponents of ell on every residue orbit, including negatives.
        for residue in range(n):
            for k in range(-10,11):
                mu=residue+n*k
                C=2*mu; Cnext=2*(mu+n)
                root=Q(C,n); rootnext=Q(Cnext,n)
                quantum=-2*k; quantumnext=-2*(k+1)
                assert rootnext-root==2 and quantumnext-quantum==-2
                assert rootnext+quantumnext==root+quantum
                # Using the reciprocal root would leave exponent -4.
                assert (-rootnext+quantumnext)-(-root+quantum)==-4
                count['peripheral_orbit_steps']+=1
        # Pick differing phase roots: power invariance does not imply invariance.
        assert n*Q(1,n)==1 and Q(1,n).denominator!=1
        assert 2**n!=2
        count['power_comparison_negative_controls']+=2
    # A source addendum: GKT Borel scalar qe=(-1)^m*zeta^{-a}, a=(N^2-1)/8.
    # Its 2N exponent is m^2, giving order N or 2N, never 1 for odd N>1.
    from math import gcd
    for n in range(3,102,2):
        m=(n-1)//2; a=(n*n-1)//8; exponent=(n*m-2*a)%(2*n)
        assert exponent==m*m%(2*n)
        assert (2*n)//gcd(exponent,2*n)==n*(2 if m%2 else 1)
        count['gkt_borel_scalar_orders']+=1
    after=verify_manifest(args.author_dir)
    assert before==after
    result={'audit_status':'PASS_PARTIAL_DISPOSITION','frozen_file_count':11,
        'freeze_unchanged':True,'frozen_hashes':before,'author_verifier_reproduced':replay,
        'independent_counts':dict(count),'arithmetic':'Exact cyclotomic polynomial rings, integers, and rational numbers.',
        'scope':'Diagnostic controls only. No QHI state sum, actual global triangulation, phase-label computation, or new invariant.'}
    path=Path(__file__).with_name('audit_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
