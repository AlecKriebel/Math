#!/usr/bin/env python3
"""Independent, reproducible falsification controls for the pinned EPnI proof.
These finite controls do not prove the theorem. Proof reasoning is in REVIEW.md.
Run with the bundled Python (NumPy only); no build/install/network required.
"""
from pathlib import Path
from datetime import datetime, timezone
from itertools import product
from math import sinh, cosh, sqrt, log, comb
from fractions import Fraction
import json
import numpy as np

OUT=Path(__file__).resolve().parent
rng=np.random.default_rng(23203100)

def f(x):
    if abs(x)<1e-5: return 1-x*x/6+7*x**4/360
    return x/sinh(x)

def b(x):
    if abs(x)<1e-5: return 1+x*x/3-x**4/45
    return x*cosh(x)/sinh(x)

def extra_e(x,y):
    s,t=f(x)**2,f(y)**2
    if abs(x*x-y*y)<1e-10:
        if abs(x)<1e-5: return .5
        return s*(b(x)-1)/(b(x)-s)
    return (t-s)/(2*(b(x)-b(y)))

def weights(m,x,y):
    return [m*f(x)*np.exp(x),m*f(x)*np.exp(-x),
            m*f(y)*np.exp(y),m*f(y)*np.exp(-y),m*f(x)*f(y)/f(x+y)]

scalar_errors=[]
for x,y in list(product([-6.,-2.,-.1,0.,.1,2.,6.],repeat=2))+[tuple(z) for z in rng.uniform(-6,6,(200,2))]:
    e=extra_e(x,y)
    assert e>0
    a=b(x)+b(y)
    val=.5*(a-(x-y)**2/(a+2*e))
    expected=f(x)*f(y)/f(x+y)
    scalar_errors.append(abs(val-expected)/max(1.,abs(expected)))

largest_F_norm=0.
largest_four_norm=0.
for trial in range(600):
    ds,dt=4,7
    ms,mt=np.exp(rng.uniform(-2,2,ds)),np.exp(rng.uniform(-2,2,dt))
    xs,ys=rng.uniform(-5,5,(2,ds)); xt,yt=rng.uniform(-5,5,(2,dt))
    ws=np.array([weights(*z) for z in zip(ms,xs,ys)]).T
    wt=np.array([weights(*z) for z in zip(mt,xt,yt)]).T
    T=rng.normal(size=(dt,ds))+1j*rng.normal(size=(dt,ds))
    def opnorm(k):
        return np.linalg.svd(np.sqrt(wt[k])[:,None]*T/np.sqrt(ws[k])[None,:],compute_uv=False)[0]
    T/=max(opnorm(k) for k in range(4))*(1+1e-12)
    largest_four_norm=max(largest_four_norm,max(opnorm(k) for k in range(4)))
    largest_F_norm=max(largest_F_norm,opnorm(4))
assert max(scalar_errors)<1e-11
assert largest_F_norm<=1+1e-10

# Entire finite-total-number sectors: no local-mode CCR replacement is made.
def basis(modes,K):
    return sorted((z for z in product(range(K+1),repeat=modes) if sum(z)<=K),key=lambda z:(sum(z),z))

def annihilators(bs):
    index={z:i for i,z in enumerate(bs)}
    result=[]
    for j in range(len(bs[0])):
        a=np.zeros((len(bs),len(bs)),complex)
        for k,z in enumerate(bs):
            if z[j]:
                zz=list(z); zz[j]-=1
                a[index[tuple(zz)],k]=sqrt(z[j])
        result.append(a)
    return result

def lind(rho,ds,r):
    ans=np.zeros_like(rho)
    for d in ds:
        dd=d.conj().T
        for c,op in [(r+1,d),(r,dd)]:
            od=op.conj().T; sq=od@op
            ans+=c*(op@rho@od-.5*(sq@rho+rho@sq))
    return ans

def q(rho,d,Z,r):
    mu=np.trace(rho@d)
    dp=d-mu*np.eye(len(d))
    return (r+1)*np.trace(rho@dp.conj().T@Z)-r*np.trace(rho@Z@dp.conj().T)

bs=basis(4,5); local=basis(2,2); outbs=basis(2,5)
idx={z:i for i,z in enumerate(bs)}; li={z:i for i,z in enumerate(local)}; oi={z:i for i,z in enumerate(outbs)}
va=np.zeros(len(local),complex)
va[li[(0,0)]]=sqrt(.4); va[li[(1,1)]]=sqrt(.35); va[li[(1,0)]]=1j*sqrt(.25)
ra=.7*np.outer(va,va.conj()); ra[li[(0,2)],li[(0,2)]]+=.3
vb=np.zeros(len(local),complex)
for z,v in [((0,0),sqrt(.3)),((1,0),sqrt(.2)*np.exp(.3j)),((0,1),sqrt(.1)),((2,0),sqrt(.4))]: vb[li[z]]=v
rb=np.outer(vb,vb.conj())
rho=np.zeros((len(bs),len(bs)),complex)
for a,ap,bp,bpp in product(range(len(local)),repeat=4):
    rho[idx[local[a]+local[bp]],idx[local[ap]+local[bpp]]]=ra[a,ap]*rb[bp,bpp]
# A port's partial transpose certifies internal two-mode entanglement in this control.
ra9=np.zeros((9,9),complex)
for i,z in enumerate(local):
    for j,zz in enumerate(local): ra9[3*z[0]+z[1],3*zz[0]+zz[1]]=ra[i,j]
pt=ra9.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)
ptmin=float(np.linalg.eigvalsh(pt)[0]); assert ptmin<-.01

ds=annihilators(bs); ods=annihilators(outbs)
lam=.37; theta=np.arccos(sqrt(lam))
G=theta*sum(ds[j].conj().T@ds[j+2]-ds[j+2].conj().T@ds[j] for j in range(2))
vals,vecs=np.linalg.eigh(1j*G)
U=(vecs*np.exp(-1j*vals)[None,:])@vecs.conj().T
assert np.linalg.norm(U.conj().T@U-np.eye(len(bs)))<1e-10

def reduce_first(X):
    Y=np.zeros((len(outbs),len(outbs)),complex)
    for i,z in enumerate(bs):
        for j,zz in enumerate(bs):
            if z[2:]==zz[2:]: Y[oi[z[:2]],oi[zz[:2]]]+=X[i,j]
    return Y

def lift(Z):
    Y=np.zeros_like(rho)
    for i,z in enumerate(bs):
        for j,zz in enumerate(bs):
            if z[2:]==zz[2:]: Y[i,j]=Z[oi[z[:2]],oi[zz[:2]]]
    return Y

gamma=reduce_first(U@rho@U.conj().T)
r1,r2=.23,1.7; r0=lam*r1+(1-lam)*r2
weak_errors=[]
for trial in range(8):
    Z=rng.normal(size=gamma.shape)+1j*rng.normal(size=gamma.shape)
    Z/=np.linalg.norm(Z,2)
    Zpull=U.conj().T@lift(Z)@U
    for j in range(2):
        lhs=q(gamma,ods[j],Z,r0)
        rhs=sqrt(lam)*q(rho,ds[j],Zpull,r1)+sqrt(1-lam)*q(rho,ds[j+2],Zpull,r2)
        weak_errors.append(float(abs(lhs-rhs)))
assert max(weak_errors)<1e-10
Djoint=lind(rho,ds[:2],r1)+lind(rho,ds[2:],r2)
Dret=reduce_first(U@Djoint@U.conj().T)
Ddirect=lind(gamma,ods,r0)
covariance_error=float(np.linalg.norm(Dret-Ddirect,'fro'))
assert covariance_error<1e-10

# A faithful non-number-diagonal state with a geometric tail. In finite Fock
# truncations the source entropy-production identity needs the exact CCR defect.
def defect_control(dim,qgeom,r):
    p=(1-qgeom)*qgeom**np.arange(dim); p/=p.sum()
    V=np.eye(dim,dtype=complex)
    V[:2,:2]=np.array([[3/5,4/5],[-4/5,3/5]])
    rho=(V*p[None,:])@V.conj().T
    d=np.diag(np.sqrt(np.arange(1,dim)),1)
    mu=np.trace(rho@d); dp=d-mu*np.eye(dim)
    de=V.conj().T@dp@V
    h=log(1+1/r)
    pl,pr=p[:,None],p[None,:]
    logdiff=np.log(pl)-np.log(pr)
    ell=np.empty_like(logdiff)
    mask=np.abs(logdiff)>1e-12
    np.divide(pl-pr,logdiff,out=ell,where=mask)
    ell[~mask]=np.broadcast_to(pl,ell.shape)[~mask]
    v=logdiff/h
    F=np.array([[f(h*z/2)*f(-h/2)/f(h*(z-1)/2)/h for z in row] for row in v])
    K=(r+1)*pr-r*pl
    qnorm=float(np.sum(K*K/(h*ell*F)*np.abs(de)**2))
    qnorm_alt=float(np.sum((1-v)*K*np.abs(de)**2))
    H=(V*(-np.log(p))[None,:])@V.conj().T
    sigma=float(np.trace(lind(rho,[d],r)@H).real/h)
    energy=float(np.trace(rho@d.conj().T@d).real-abs(mu)**2)
    ccr=float(np.trace(rho@(d@d.conj().T-d.conj().T@d)).real)
    corrected=sigma-(qnorm-(energy-r*ccr))
    uncorrected=sigma-(qnorm-(energy-r))
    predicted=-r*dim*float(rho[-1,-1].real)
    assert abs(corrected)<2e-11
    assert abs(uncorrected-predicted)<2e-11
    assert abs(qnorm-qnorm_alt)<2e-11
    return dict(dimension=dim,reference_r=r,mean_abs=float(abs(mu)),
                qnorm=qnorm,sigma=sigma,ccr_expectation=ccr,
                corrected_identity_error=float(abs(corrected)),
                uncorrected_identity_residual=float(uncorrected),
                exact_boundary_prediction=predicted)

defects=[defect_control(dim,.4,r) for dim in (12,32,64) for r in (.1,1.3,4.)]

# Exact rational bookkeeping for cancellation and leading fourth-moment drift.
coeff_checks=[]
for eps,w in [(Fraction(1,13),Fraction(5,17)),(Fraction(2,7),Fraction(3,8))]:
    coeff=-w+(1+eps)*w-eps*w
    assert coeff==0
    coeff_checks.append(str(coeff))
# Expand (r+1)N[N^4-(N+1)^4]+r(N+n)[(N+2)^4-(N+1)^4].
def poly_mul(a,b):
    ans=[Fraction(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): ans[i+j]+=x*y
    return ans
moment=[]
for r,n in [(Fraction(1,5),1),(Fraction(17,4),7)]:
    down=[-Fraction(comb(4,k)) for k in range(4)]+[Fraction(0)]
    up=[Fraction(comb(4,k)*(2**(4-k)-1)) for k in range(5)]
    a=poly_mul([0,r+1],down); bb=poly_mul([r*n,r],up)
    p=[x+y for x,y in zip(a,bb)]
    assert p[5]==0 and p[4]==-4
    moment.append(dict(r=str(r),n=n,ascending_coefficients=[str(z) for z in p]))

result=dict(status='PASS',scope='Finite falsification controls, not a theorem proof',
    timestamp_utc=datetime.now(timezone.utc).isoformat(),seed=23203100,
    scalar_minimization=dict(cases=len(scalar_errors),max_relative_error=max(scalar_errors)),
    four_weight_operator_comparison=dict(cases=600,largest_hypothesis_operator_norm=largest_four_norm,
        largest_conclusion_operator_norm=largest_F_norm),
    internally_entangled_multimode_control=dict(modes_per_port=2,ports=2,total_number_cutoff=5,
        input_support_total_number_at_most=4,joint_dimension=len(bs),port_A_partial_transpose_min_eigenvalue=ptmin,
        weak_convolution_cases=len(weak_errors),weak_convolution_max_absolute_error=max(weak_errors),
        generator_covariance_frobenius_error=covariance_error),
    finite_Fock_boundary_controls=defects,exact_centered_energy_cancellation_coefficients=coeff_checks,
    exact_fourth_moment_polynomials=moment,numpy_version=np.__version__)
(OUT/'verification_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='finite_Fock_boundary_controls'},indent=2))
