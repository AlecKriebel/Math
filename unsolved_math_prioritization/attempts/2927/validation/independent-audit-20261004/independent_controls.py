#!/usr/bin/env python3
"""Independent exact audit; does not import or alter the frozen checker."""
from pathlib import Path
from itertools import combinations
import hashlib, json
import sympy as s

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
x=s.symbols('x', nonzero=True)
star=lambda M:M.T.subs(x,1/x)
clean=lambda M:M.applyfunc(s.expand)
a=x+1/x
L=s.Matrix([[1+a+a*a,a+a*a,1+a,a],[a+a*a,1+a+a*a,a,1+a],
            [1+a,a,2,0],[a,1+a,0,2]])
P=s.Matrix([[0,0,1,-1,-1],[0,0,0,1,-1],[1,1,-1-1/x,1,a+1],
            [0,1,-1/x,0,a+1],[1,2,x-1-1/x,1,1]])
J=s.diag(L,-1)
G=s.diag(s.ones(1),s.Matrix([[0,1],[1,0]]),s.eye(2))
assert clean(star(P)*J*P)==G
assert s.simplify(P.det())==-1
assert s.simplify(L.det())==1
assert clean(star(L)-L)==s.zeros(4)
assert clean(L[:2,:2]-L[:2,2:]*L[2:,:2]/2)==s.eye(2)/2

# Independently verify every algebraic step in the derivation, not just the result.
e=[s.eye(5)[:,i] for i in range(5)]
h=lambda v,w:s.expand((star(v)*J*w)[0])
u=e[2]+e[4]
A=e[2]+e[3]+2*e[4]
w=e[0]-(1+a)*u-a*e[3]
B=w+x*A
assert [h(u,u),h(A,A),h(u,A),h(A,w),h(w,w)]==[1,0,0,1,-a]
assert [h(B,B),h(A,B),h(u,B)]==[0,1,0]
perp=lambda z:clean(z-u*h(u,z)-A*h(B,z)-B*h(A,z))
C,E=perp(e[1]),perp(e[2])
assert clean(s.Matrix([[h(C,C),h(C,E)],[h(E,C),h(E,E)]]))==clean(s.Matrix([[2*a*a+2*a+1,2*a+1],[2*a+1,2]]))
assert clean(s.Matrix.hstack(u,A,B,C-a*E,E-C+a*E))==P
assert clean(P.inv()*P)==s.eye(5)

# Coefficient extraction in scalar pairings (different assembly from frozen code).
def terms(f):
    return [(int(t.as_powers_dict().get(x,0)),s.expand(t/x**t.as_powers_dict().get(x,0)))
            for t in s.Add.make_args(s.expand(f)) if t]
def coefficient_mod(f,n):
    return sum(c for k,c in terms(f) if k%n==0)
def cover(H,n):
    r=H.rows
    return s.Matrix(r*n,r*n,lambda I,J:coefficient_mod(x**((J%n)-(I%n))*H[I//n,J//n],n))
cover_results=[]
for n in range(1,13):
    Q=cover(L,n)
    assert Q==Q.T
    # This exact Schur complement certifies positivity and determinant without
    # numerical eigenvalue sampling or reusing the frozen LDL implementation.
    Bn=Q[:2*n,2*n:]
    assert Q[2*n:,2*n:]==2*s.eye(2*n)
    assert Q[:2*n,:2*n]-Bn*Bn.T/2==s.eye(2*n)/2
    w=s.Matrix([0]*(2*n)+[1]*(2*n))
    c=w-2*s.eye(4*n)[:,0]
    assert all((int((Q*c)[i])-int(Q[i,i]))%2==0 for i in range(4*n))
    wn,cn=int((w.T*Q*w)[0]),int((c.T*Q*c)[0])
    assert wn==4*n and cn==({1:12,2:8}.get(n,4*n-8))
    assert all(int((Q*w)[i])==(5 if i<2*n else 2) for i in range(4*n))
    cover_results.append({'n':n,'rank':4*n,'w_norm':wn,'c_norm':cn,
                          'characteristic':True,'exact_schur_positive':True,
                          'determinant_by_schur':1,'short_characteristic':cn<4*n})

# Exhaustive graph-lifting stress test over selected small admissible parameters.
# These finite controls supplement, and do not replace, the general argument.
unwrapping_tests=[]
for p,d,K in [(5,1,2),(7,1,3),(11,2,2),(13,2,3),(17,2,4),(19,3,3)]:
    assert p>2*d*K
    connected=0
    for q in range(1,K+1):
        # Translation invariant: every support is a translate of one containing 0.
        for rest in combinations(range(1,p),q-1):
            vertices=(0,)+rest
            edges={}
            for u0,v0 in combinations(vertices,2):
                delta=(v0-u0)%p
                if delta>p//2: delta-=p
                if abs(delta)<=d: edges[u0,v0]=delta
            lifts={0:0}
            while True:
                changed=False
                for (u0,v0),delta in edges.items():
                    if u0 in lifts and v0 not in lifts:
                        lifts[v0]=lifts[u0]+delta; changed=True
                    if v0 in lifts and u0 not in lifts:
                        lifts[u0]=lifts[v0]-delta; changed=True
                if not changed: break
            if len(lifts)!=q: continue
            connected+=1
            assert max(lifts.values())-min(lifts.values())<=d*(q-1)
            assert all(lifts[v0]-lifts[u0]==delta for (u0,v0),delta in edges.items())
            assert all((lifts[v0]-v0)%p==0 for v0 in vertices)
    unwrapping_tests.append({'p':p,'d':d,'K':K,'connected_supports_checked':connected})

# Build highly asymmetric Laurent shears to stress star rather than transpose.
V=s.Matrix([[1,x**4-2*x**-2,3*x],[0,1,1-x**-3],[0,0,1]])
H=clean(star(V)*V)
W=clean(V.inv())
assert clean(star(W)*H*W)==s.eye(3)
asymmetric=[]
for n in [3,5,7,11]:
    Q,F,R=cover(H,n),cover(V,n),cover(W,n)
    T=cover(x*s.eye(3),n)
    assert Q==F.T*F
    assert F*R==s.eye(3*n)
    assert R.T*Q*R==s.eye(3*n)
    assert T.T*Q*T==Q and T.trace()==0 and T**n==s.eye(3*n)
    assert F*T*R==T
    asymmetric.append(n)

# Negative controls: ordinary transpose would fail; a corrupt coefficient fails.
assert clean(P.T*J*P)!=G
bad=P.copy(); bad[2,2]+=1
assert clean(star(bad)*J*bad)!=G

manifest=BASE/'public'/'SHA256SUMS'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='1bddbd487f555afa16feb2b822dc09ef819343f8ab908b21021fafb6de0561da'
for line in manifest.read_text().splitlines():
    expected,name=line.split(maxsplit=1)
    assert hashlib.sha256((manifest.parent/name).read_bytes()).hexdigest()==expected
result={'status':'PASS','sympy':s.__version__,
        'exact_stabilization_and_derivation':True,'star_negative_controls':True,
        'cover_results':cover_results,'unwrapping_tests':unwrapping_tests,
        'asymmetric_extended_primes':asymmetric,'frozen_public_hashes_verified':True,
        'limits':'Finite checks supplement the separate mathematical audit; no general indefinite theorem or prior descent proof is certified.'}
(ROOT/'independent_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
