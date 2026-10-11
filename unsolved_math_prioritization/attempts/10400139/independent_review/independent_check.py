#!/usr/bin/env python3
"""Independent source-formula controls; no author checker imports or network.
Exact finite fields and cellular chains are diagnostics for the written proof.
CG reconstruction is separately labelled non-interval complex arithmetic.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib,json
import sympy as sp
import mpmath as mp

counts=Counter()
def check(value,kind):
    assert value,kind
    counts[kind]+=1

# Independent oriented 3-sphere chains: stellar subdivisions of boundary Delta4.
chain={T:(-1)**next(i for i in range(5) if i not in T)
       for T in combinations(range(5),4)}
for stage in range(9):
    boundary=Counter(); gauge=Fraction(1)
    for T,sign in chain.items():
        for j in range(4):
            face=T[:j]+T[j+1:]
            exp=sign*(-1)**j
            boundary[face]+=exp
            # Arbitrary signed face factors, including auxiliary square-root signs.
            factor=Fraction((-1)**sum(face)*(2+sum((k+1)*(v+1) for k,v in enumerate(face))),11)
            gauge*=factor**exp
    for value in boundary.values():check(value==0,'closed_face_incidence')
    check(gauge==1,'signed_face_gauge')
    E=set(); V=set()
    for T in chain: E.update(combinations(T,2));V.update(T)
    # Closed 3-manifold Euler relation, Hamiltonian H has V edges.
    check(len(E)-len(V)==len(chain),'edge_scaling_count')
    T=sorted(chain)[stage%len(chain)];sign=chain.pop(T);new=max(V)+1
    for j in range(4):
        F=T[:j]+T[j+1:]
        chain[F+(new,)]=-sign*(-1)**j

# Exact finite-field forms of the powered h and charge identities.
for N in range(3,32,2):
    p=1000*N*N+1
    while not sp.isprime(p):p+=N
    root=pow(int(sp.primitive_root(p)),(p-1)//N,p)
    inv=lambda x:pow(x%p,-1,p)
    half=pow(2,-1,N);m=(N-1)//2
    def hnewN(u):
        ans=1
        for j in range(1,N):ans=ans*pow((1-u*pow(root,-j,p))*inv(1-pow(root,-j,p))%p,j,p)%p
        return ans
    def holdN(u):
        ans=pow(u,-m*N,p)
        for j in range(1,N):ans=ans*pow((1-u*pow(root,j,p))*inv(1-pow(root,j,p))%p,j,p)%p
        return ans
    def omega(u,v,n):
        ans=1
        for j in range(1,n%N+1):ans=ans*v*inv(1-u*pow(root,j,p))%p
        return ans
    primitive=int(sp.primitive_root(p))
    powers={pow(primitive,N*k,p):pow(primitive,k,p) for k in range((p-1)//N)}
    tested=0
    for u in range(2,p):
        vn=(1-pow(u,N,p))%p
        if not vn or vn not in powers:continue
        v=powers[vn];hn=hnewN(u)
        check(holdN(inv(u))==hn,'powered_h_reversal')
        for a in range(N):
            check(hnewN(u*pow(root,a,p)%p)==hn*pow(omega(u,v,a),N,p)%p,'powered_h_shift')
            telescope=(1-u*pow(root,a,p))*inv(1-u)*omega(u,v,a)*inv(omega(u*inv(root)%p,v,a))%p
            check(telescope==1,'negative_scalar_cancellation')
            for n in range(N):
                check(omega(u,v,n+a)==omega(u,v,n)*omega(u*pow(root,n,p)%p,v,a)%p,'cyclic_omega_cocycle')
        tested+=1
        if tested==6:break
    check(tested==6,'nonsingular_fermat_samples')
    for V in range(4,17):
        check(Fraction(N)**(2-V)/Fraction(N)**(-V)==N*N,'vertex_normalization')
    check((-1)**N==-1,'uncancelled_sign_negative_control')
    check((half*2)%N==1,'odd_half_charge')

# Reconstruct 6j coefficients from the CG intertwiner linear system itself.
# This route does not use either published finite-rho sum used by the author.
mp.mp.dps=85;worst=mp.mpf(0);numeric=0
def near(a,b):
    global worst,numeric
    err=abs(a-b)/max(1,abs(a),abs(b));worst=max(worst,err);numeric+=1
    assert err<mp.mpf('1e-65'),mp.nstr(err,12)
for N in (3,5):
    z=mp.exp(2j*mp.pi/N);half=(N+1)//2;m=(N-1)//2
    for raw in ((1,2,4),(2,3,5)):
        p,q,r=map(mp.mpf,raw)
        rt=lambda a:mp.power(a,mp.mpf(1)/N)
        def om(x,y,Z,n):return mp.fprod(y/(Z-x*z**j) for j in range(1,n%N+1))
        def h(x):
            return x**(-m)*mp.exp(sum(mp.mpf(j)/N*(mp.log(1-x*z**j)-mp.log(1-z**j)) for j in range(1,N)))
        def nu(a,b):return h(rt(a+b)/rt(b))
        def cg(a,b,alpha,i,j):return nu(a,b)*z**(alpha*j+half*alpha*alpha)*om(rt(b),rt(a),rt(a+b),i-alpha)
        xpq,xqr,xpqr,xq,xp,xr=map(rt,(p+q,q+r,p+q+r,q,p,r))
        X=xpqr*xq;Y=xp*xr;Z=xpq*xqr
        phases=[]
        for beta in range(N):
            B=mp.matrix([[cg(q,r,(beta-g)%N,j,(-j)%N)*cg(p,q+r,g,0,0) for g in range(N)] for j in range(N)])
            for alpha in range(N):
                L=mp.matrix([cg(p,q,alpha,0,j)*cg(p+q,r,beta,j,(-j)%N) for j in range(N)])
                coeff=mp.lu_solve(B,L)
                for gamma in range(N):
                    delta=(beta-gamma)%N
                    explicit=h(Z/X)*z**(alpha*delta+half*alpha*alpha)*om(X,Y,Z,gamma-alpha)
                    phases.append(coeff[gamma]/explicit)
                # All physical output states with k=0; extra k controls for N3.
                for k in (range(N) if N==3 else (0,2)):
                    for i in range(N):
                        for j in range(N):
                            ell=(k-i-j)%N
                            lhs=cg(p,q,alpha,i,j)*cg(p+q,r,beta,(i+j)%N,ell)
                            rhs=sum(coeff[g]*cg(q,r,(beta-g)%N,j,ell)*cg(p,q+r,g,i,(j+ell)%N) for g in range(N))
                            near(lhs,rhs)
        for phase in phases:near(phase,phases[0]);near(phase**N,1)

out={'problem_id':10400139,'exact_controls':sum(counts.values()),'exact_by_kind':dict(sorted(counts.items())),
     'independent_CG_reconstruction_diagnostics':numeric,'mpmath_dps':mp.mp.dps,'worst_relative_error':mp.nstr(worst,12),
     'numeric_tolerance':'1e-65','numeric_is_interval_proof':False,
     'scope':'Independent cellular cancellation, finite-field powered dilogarithm identities, normalization and direct CG intertwiner reconstruction. All-link and all-N conclusions rely on the written source/convention audit, not finite controls.',
     'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(out,sort_keys=True,indent=2))
