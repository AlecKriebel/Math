#!/usr/bin/env python3
"""Independent exact/numerical controls. No paper implementation is imported."""
import hashlib,json,platform,urllib.request
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import scipy
from scipy.linalg import sqrtm
import sympy as sp
rng=np.random.default_rng(21699161)
I=np.eye(2,dtype=complex)
pauli=[I,np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
J=np.diag([1,-1,-1,-1]);r=np.column_stack([np.eye(4),[1,1,-1,-1]]);u=np.array([1,1,0,0])
def op(v):return sum(x*s for x,s in zip(v,pauli))
def coord(M):return np.array([np.trace(M@s).real/2 for s in pauli])
def axis():
    n=rng.normal(size=3);return n/np.linalg.norm(n)
def rotation():
    q,_=np.linalg.qr(rng.normal(size=(3,3)))
    if np.linalg.det(q)<0:q[:,0]*=-1
    return q

def local():
    ang=np.array([0,rng.uniform(1.8,2.4),rng.uniform(3.9,4.5)])
    n=np.array([np.cos(ang),np.sin(ang),np.zeros(3)])
    weights=np.linalg.solve(np.vstack([np.ones(3),n[:2]]),np.array([1,0,0]))
    assert min(weights)>0
    n=rotation()@n;v=axis()
    E=np.column_stack([np.r_[.5,v/2],np.r_[.5,-v/2],np.r_[weights[0],weights[0]*n[:,0]],np.r_[weights[1],weights[1]*n[:,1]]])
    if abs(np.linalg.det(E))<1e-3:return local()
    return E,[op(E@r[:,i]) for i in range(5)]

def H(c):
    a,b,c_,d=c;e=a+b+c_+d
    return np.array([[0,0,a,b],[0,0,c_,d],[a,c_,0,e],[b,d,e,0]],float)

def Phi(x):return np.array([x[2]*(x[0]+x[3]),x[3]*(x[0]+x[2]),x[2]*(x[1]+x[3]),x[3]*(x[1]+x[2])])

def invphi(z):
    a,b,c,d=z;det=a*d-b*c
    return np.array([(a-b)*(a-c)*(b-d),(c-d)*(a-c)*(b-d),det*(a-c),det*(b-d)])

results={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'scope':'Independent finite algebraic, random physical and edge controls; not a universal formal proof','environment':{'python':platform.python_version(),'sympy':sp.__version__,'numpy':np.__version__,'scipy':scipy.__version__}}

# Exact discrimination witness, gap and generic projective inverse.
rt=sp.sqrt(2);X=sp.Matrix([[0,1],[1,0]]);Z=sp.diag(1,-1);eye=sp.eye(2)
Ms=[(17*eye-8*X+15*Z)/50,(17*eye-8*X-15*Z)/50,(16*eye+16*X)/50]
W=[3*(eye+Z)/20,3*(eye-Z)/20,(eye+X)/5];Gamma=8*eye/25+2*X/25
assert sum(Ms,sp.zeros(2))==eye
assert all(m.det()==0 and m.trace()>0 for m in Ms)
assert all((Gamma-w)*m==sp.zeros(2) for w,m in zip(W,Ms))
assert all((Gamma-w).det()==0 and (Gamma-w).trace()>0 for w in W)
val=sum(sp.trace(m*w) for m,w in zip(Ms,W));assert val==sp.Rational(16,25)
L0=20*rt+val;U=20*rt+sp.Rational(3,5)+(4+3*rt)/250
assert sp.simplify(L0-U-3*(2-rt)/250)==0
x0,x1,x2,x3=sp.symbols('x0 x1 x2 x3')
z=[x2*(x0+x3),x3*(x0+x2),x2*(x1+x3),x3*(x1+x2)]
a,b,c,d=z;det=a*d-b*c
inv=[(a-b)*(a-c)*(b-d),(c-d)*(a-c)*(b-d),det*(a-c),det*(b-d)]
omega=x2*x3*(x2-x3)*(x0-x1)**2
assert all(sp.expand(v-omega*x)==0 for v,x in zip(inv,[x0,x1,x2,x3]))
results['exact']={'simple_auxiliary':str(val),'gap':str(sp.simplify(L0-U)),'L0':float(L0),'U':float(U),'generic_inverse':'four polynomial identities PASS'}

# Independently derive the robust-comparison identity in Appendix A.
eta,x,y,rr,q=sp.symbols('eta x y rr q');hh=8-3*x-4*y
rad=(-1+eta*(3*x-4*y))**2+24*(1-eta**2)*(1-rr)
cert=2*eta*(eta*(8*(1-y)*(4-3*x)+12*(1-rr))+(q-1)*hh+8*(1-y))
res=sp.Poly(sp.expand((q+eta*hh)**2-rad-cert),q)
assert sp.simplify(res.as_expr()-(q*q-25+24*rr))==0
results['exact']['robust_certificate']='symbolic identity modulo q^2=25-24r PASS'

max_null=max_born=max_hessian=max_inverse=max_rankzero=0.;ranks={};counts=150
for trial in range(counts):
    EA,A=local();EB,B=local()
    Xi=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));Xi/=np.linalg.norm(Xi)
    while abs(np.linalg.det(Xi))<.05:
        Xi=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));Xi/=np.linalg.norm(Xi)
    P=np.array([[np.trace(A[i]@Xi@B[j].T@Xi.conj().T).real for j in range(4)] for i in range(4)])
    g=EA.T@J@EA;Q=np.linalg.inv(g);yy=Q@P@r
    err=np.max(abs(np.diag(r.T@P.T@Q@P@r)));max_null=max(max_null,err)
    assert err<2e-11 and abs(u@P@u-1)<1e-12
    # Rebuild steered states and a canonical purification from the probabilities.
    Sj=[op(np.linalg.solve(EA.T,P@r[:,j])/2) for j in range(5)]
    rho=Sj[0]+Sj[1];Xi2=np.asarray(sqrtm(rho),complex);invXi=np.linalg.inv(Xi2)
    Nj=[(invXi@s@invXi.conj().T).T for s in Sj]
    P2=np.array([[np.trace(A[i]@Xi2@Nj[j].T@Xi2.conj().T).real for j in range(4)] for i in range(4)])
    max_born=max(max_born,float(np.max(abs(P2-P))))
    assert min(np.linalg.eigvalsh(n).min() for n in Nj)>-1e-10
    assert np.max(abs(Nj[0]+Nj[1]-I))<1e-10 and np.max(abs(sum(Nj[2:])-I))<1e-10
    # Full Jacobian rank, with normalized constraint independent even at F=0.
    Jac=np.zeros((6,20))
    for j in range(5):
        Jac[j,:16]=(2*np.outer(yy[:,j],r[:,j])).reshape(-1)
        Jac[j,16:]=[-yy[:,j]@H(np.eye(4)[k])@yy[:,j] for k in range(4)]
    Jac[5,:16]=np.outer(u,u).reshape(-1)
    assert np.linalg.matrix_rank(Jac,tol=1e-9)==6
    d_rank=int(np.linalg.matrix_rank(Jac[:5,16:],tol=1e-9));ranks[d_rank]=ranks.get(d_rank,0)+1
    # Hessian completion with arbitrary variations, no stationarity assumptions.
    dP=rng.normal(size=(4,4));h=H(rng.normal(size=4));ww=np.linalg.solve(P,dP-h@Q@P)
    for j in range(5):
        xx=P@r[:,j];dx=dP@r[:,j]
        before=dx@Q@dx-2*dx@Q@h@Q@xx+xx@Q@h@Q@h@Q@xx
        after=(P@ww@r[:,j])@Q@(P@ww@r[:,j])
        relative=abs(before-after)/(1+abs(before)+abs(after));max_hessian=max(max_hessian,relative)
        assert relative<1e-9
    # Five-ray base locus and independent numerical generic inverse on physical null rays.
    assert np.max(abs(np.array([Phi(r[:,j]) for j in range(5)])))==0
    for _ in range(5):
        ray=np.linalg.solve(EA,np.r_[1,axis()]);ph=Phi(ray);iv=invphi(ph)
        if np.linalg.norm(iv)<1e-8:continue
        cosine=abs(iv@ray)/(np.linalg.norm(iv)*np.linalg.norm(ray));max_inverse=max(max_inverse,abs(1-cosine))
        assert abs(1-cosine)<1e-9
    # Rank-zero transportation using randomly generated strict physical metrics.
    table=r.T@g@r;aa=table[0,2:];bb=table[1,2:];cc=table[2:,2:];dd=(bb-aa)/2
    lows=[-cc[0,1]/2,dd[0]-cc[0,2]/2,-dd[1]-cc[1,2]/2]
    highs=[cc[0,1]/2,dd[0]+cc[0,2]/2,-dd[1]+cc[1,2]/2]
    assert max(lows)<=min(highs)+1e-12
    tt=(max(lows)+min(highs))/2;ff=np.array([[0,tt,dd[0]-tt],[-tt,0,dd[1]+tt],[-dd[0]+tt,-dd[1]-tt,0]])
    qq=cc/2+ff;np.fill_diagonal(qq,0)
    assert min(qq.flatten())>-1e-12 and np.max(qq-cc)<1e-12
    rebuilt=np.zeros((5,5))
    for i in range(3):
        for j in range(3):
            for weight,ab,bbin in [(qq[i,j],0,1),(cc[i,j]-qq[i,j],1,0)]:
                for ai in [ab,i+2]:
                    for bj in [bbin,j+2]:rebuilt[ai,bj]+=weight
    max_rankzero=max(max_rankzero,float(np.max(abs(rebuilt-table))))
    assert np.max(abs(rebuilt-table))<1e-11
results['physical_controls']={'random_residual_strategies':counts,'jacobian_rank':6,'metric_differential_ranks':ranks,'max_incidence_residual':max_null,'max_reconstructed_Born_error':max_born,'max_hessian_relative_error':max_hessian,'max_projective_inverse_cosine_error':max_inverse,'max_rankzero_simulation_error':max_rankzero}

# Global-state PVM support stress: optimize the state by largest Bell-operator
# eigenvalue for every sampled set of measurement directions and support pattern.
def obs(n):return op(np.r_[0,n])
def proj(n):return (I+obs(n))/2
best=-1; support_results={}
for support in [(0,),(1,),(2,),(0,1),(0,2),(1,2)]:
    maximum=-1
    for trial in range(300):
        # Half random directions; half close to the locking point.
        if trial<150:
            B0=obs(axis());B1=obs(axis());A0=obs(axis());A1=obs(axis());aux=proj(axis())
        else:
            def pert(n):
                v=np.array(n)+rng.normal(size=3)*.04;return v/np.linalg.norm(v)
            B0=obs(pert([0,0,1]));B1=obs(pert([1,0,0]));A0=obs(pert([1,0,1]));A1=obs(pert([-1,0,1]));aux=proj(axis())
        if trial%20==0:A0=I if trial%40==0 else -I
        M=[np.zeros((2,2),complex) for _ in range(3)]
        M[support[0]]=I if len(support)==1 else aux
        if len(support)==2:M[support[1]]=I-aux
        bell=10*(np.kron(A0,B0+B1)+np.kron(A1,B0-B1))+.6*np.kron(M[0],(I+B0)/2)+.6*np.kron(M[1],(I-B0)/2)+.8*np.kron(M[2],(I+B1)/2)
        value=float(np.linalg.eigvalsh(bell)[-1]);maximum=max(maximum,value)
        assert value<float(U)+1e-10
    support_results[str(support)]=maximum;best=max(best,maximum)
results['pvm_stress']={'state_optimized_samples':1800,'all_six_auxiliary_support_patterns':support_results,'maximum_sampled':best,'analytic_upper_bound':float(U),'role':'falsification search only; the analytic proof establishes the global bound'}
results['status']='PASS'
Path('independent-controls.json').write_text(json.dumps(results,indent=2)+'\n')
print('INDEPENDENT_CONTROLS_PASS',json.dumps({'physical_cases':counts,'pvm_state_optimized_cases':1800,'sampled_maximum':best,'U':float(U),'gap':float(L0-U)}))
# Resolve the public annotated release tag and bind its commit to the local extraction.
p=Path('source-receipt.json');receipt=json.loads(p.read_text());obj=receipt['remote_tag_ref']['object']
if obj['type']=='tag':
    with urllib.request.urlopen(obj['url'],timeout=30) as f:tag=json.load(f)
    receipt['remote_annotated_tag']=tag;obj=tag['object']
assert obj['type']=='commit' and obj['sha']==receipt['local_release_commit']
receipt['public_release_commit_verified']=True;p.write_text(json.dumps(receipt,indent=2)+'\n')
