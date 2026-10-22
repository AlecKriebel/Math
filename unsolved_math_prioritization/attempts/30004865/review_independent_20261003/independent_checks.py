#!/usr/bin/env python3
"""Independent audit controls. Finite numerical controls are NOT proofs of norm universality."""
import json, math, hashlib, platform
from pathlib import Path
from itertools import product
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
checks=0

def ck(value):
    global checks
    assert bool(value)
    checks+=1

def close(a,b,tol=2e-11):
    ck(np.max(np.abs(np.asarray(a)-np.asarray(b)))<tol)

# Check frozen inputs, independently of the shell command and author programs.
manifest=ROOT/'attempt'/'TURN_5_MANIFEST.json'
ck(hashlib.sha256(manifest.read_bytes()).hexdigest()=='8016d13bc34c45147548324d9b70b2a598340a3ffe50cef0eff446a1f9f0c98b')
for item in json.loads(manifest.read_text())['files']:
    b=(ROOT/'attempt'/item['path']).read_bytes()
    ck(len(b)==item['bytes'])
    ck(hashlib.sha256(b).hexdigest()==item['sha256'])
for f in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_T2.json','SOURCE_ADDITION_T3.json','SOURCE_ADDITION_T5.json']:
    for item in json.loads((ROOT/'attempt'/f).read_text())['sources']:
        b=(ROOT/'sources'/item['file']).read_bytes()
        ck(len(b)==item['bytes'])
        ck(hashlib.sha256(b).hexdigest()==item['sha256'])

# General symbolic identities, rather than grids of rational substitutions.
d,f,c,w,p=sp.symbols('d f c w p',real=True)
a=(d-f)/(d*(d*d-1)); b=(d*f-1)/(d*(d*d-1))
for lhs,rhs in [(a+b,(1+f)/(d*(d+1))), (a-b,(1-f)/(d*(d-1))),
                (d*a+b,1/d), ((d*(d+1)/2)*(a+b)+(d*(d-1)/2)*(a-b),1),
                ((d*(d+1)/2)*(a+b)-(d*(d-1)/2)*(a-b),f)]:
    ck(sp.factor(lhs-rhs)==0)
lam=(3*c*c-1)/(2*c**3); h=1/(2*c)
det=(1-lam*w)*(1-h*w)-h*h*(1-w*w)
ck(sp.factor(det-(4*c*c-1)*(w-c)**2/(4*c**4))==0)
ck(sp.factor(1-lam-(c-1)**2*(2*c+1)/(2*c**3))==0)
ck(sp.factor(lam*c**3+3*h*c*(1-c*c)-1)==0)
ck(sp.factor((3+p)**2-2*(1+p)**3-(1-p)*(2*p*p+7*p+7))==0)
ck(sp.factor(2*(1+p)**3-(1+3*p)**2-(1-p)**2*(2*p+1))==0)
ck(sp.factor((1+p)**3-8*(1-p)**2-(p**3-5*p**2+19*p-7))==0)
ck(sp.factor((3+p)**3-(8-2*sp.sqrt(2)*p)**2-(p**3+p**2+(27+32*sp.sqrt(2))*p-37))==0)

# Explicit 9x9 density matrix and partial transpose, exact.
d0=3
F=sp.zeros(9)
for i,j in product(range(3),repeat=2): F[3*i+j,3*j+i]=1
rho=(19*sp.eye(9)-9*F)/144
ck(rho.trace()==1)
ck((F*rho).trace()==-sp.Rational(1,6))
ck(rho.eigenvals()=={sp.Rational(5,72):6,sp.Rational(7,36):3})
pt=sp.zeros(9)
for i,j,k,l in product(range(3),repeat=4): pt[3*k+j,3*i+l]=rho[3*i+j,3*k+l]
ck(pt.eigenvals()=={sp.Rational(-1,18):1,sp.Rational(19,144):8})

# Hermitian basis containing genuinely imaginary off-diagonals checks the flip,
# and eliminates a real-only proof accidentally replacing F by |Omega><Omega|.
def hermitian_basis(d):
    basis=[np.eye(d)/np.sqrt(d)]
    for k in range(1,d):
        x=np.zeros((d,d),complex)
        for j in range(k): x[j,j]=1
        x[k,k]=-k
        basis.append(x/np.sqrt(k*(k+1)))
    for i in range(d):
        for j in range(i+1,d):
            x=np.zeros((d,d),complex);x[i,j]=x[j,i]=1/np.sqrt(2);basis.append(x)
            y=np.zeros((d,d),complex);y[i,j]=-1j/np.sqrt(2);y[j,i]=1j/np.sqrt(2);basis.append(y)
    return basis
for dim in [2,3,4,5]:
    bas=hermitian_basis(dim)
    fl=np.zeros((dim*dim,dim*dim),complex)
    for i,j in product(range(dim),repeat=2):fl[dim*i+j,dim*j+i]=1
    close(sum(np.kron(x,x) for x in bas),fl)
    close([[np.trace(x.conj().T@y) for y in bas] for x in bas],np.eye(dim*dim))

# Certified S1-to-Hilbert contraction constructions, followed by genuinely
# complex unequal-dimensional output contractions. This samples maps only.
rng=np.random.default_rng(0x30004865)
dim=3; bas=hermitian_basis(dim)
rhon=np.array(rho,complex)
C=rhon.reshape(dim,dim,dim,dim).transpose(0,2,1,3).reshape(dim*dim,dim*dim)
tr=np.eye(dim).reshape(1,-1)

def tester(n,t):
    base=np.vstack([math.sqrt(t)*tr,math.sqrt(1-t)*np.eye(dim*dim)])
    Z=rng.normal(size=(n,dim*dim+1))+1j*rng.normal(size=(n,dim*dim+1))
    # divide by spectral norm gives contraction after the certified base tester
    Z/=np.linalg.svd(Z,compute_uv=False)[0]
    return Z@base

max_sample_value=0.; pair_cases=0
for n,m in product([1,2,4,10,17],[1,3,7,10,19]):
    for _ in range(12):
        E=tester(n,rng.uniform());G=tester(m,rng.uniform())
        out=E@C@G.T
        val=np.linalg.svd(out,compute_uv=False).sum()
        En=np.array([E@x.reshape(-1) for x in bas]);Gn=np.array([G@x.reshape(-1) for x in bas])
        eu=np.linalg.norm(En[0]); gu=np.linalg.norm(Gn[0])
        eS=np.linalg.norm(En[1:])**2; gS=np.linalg.norm(Gn[1:])**2
        ck(eu*eu/3+eS/12 <=1+1e-12);ck(gu*gu/3+gS/12 <=1+1e-12)
        upper=eu*gu/3+np.sqrt(eS*gS)/16
        ck(val<=upper+1e-12);ck(upper<=1+1e-12)
        close(out,En[0,:,None]*Gn[0,None,:]/3-sum(En[i,:,None]*Gn[i,None,:] for i in range(1,9))/16)
        max_sample_value=max(max_sample_value,float(val));pair_cases+=1
close(tr@C@tr.T,np.ones((1,1)))

# Complex multilinear tests in several perpendicular dimensions; equality is
# also checked on repeated real unit vectors. The analytic bound is in review.
form_cases=0;max_form=0.
for perp in [1,2,5,9]:
    for c0 in [1/math.sqrt(2),math.sqrt(2/3),math.sqrt(3/4),.95,1.]:
        L=(3*c0*c0-1)/(2*c0**3);H=1/(2*c0)
        def form(x,y,z):
            return L*x[0]*y[0]*z[0]+H*(x[0]*np.dot(y[1:],z[1:])+y[0]*np.dot(x[1:],z[1:])+z[0]*np.dot(x[1:],y[1:]))
        v=np.zeros(perp+1);v[0]=c0;v[1]=math.sqrt(max(0,1-c0*c0));close(form(v,v,v),1.)
        for _ in range(100):
            vs=[]
            for k in range(3):
                x=rng.normal(size=perp+1)+1j*rng.normal(size=perp+1);vs.append(x/np.linalg.norm(x))
            q=abs(form(*vs));ck(q<=1+1e-12);max_form=max(max_form,float(q));form_cases+=1

# Direct qubit SIC construction and independent coefficient-matrix calculations.
I=np.eye(2); X=np.array([[0,1],[1,0]]); Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
paulis=[I,X,Y,Z]
verts=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
Ps=[(I+sum(v[j]*paulis[j+1]/np.sqrt(3) for j in range(3)))/2 for v in verts]
S=np.sqrt(3/4)*np.array([P.T.reshape(-1) for P in Ps])
D=np.zeros((4,4),complex)
for i in range(4):
    M=np.eye(4)[i].reshape(2,2)
    D[:,i]=(M+(np.sqrt(3)-1)*np.trace(M)*I/2).reshape(-1)/np.sqrt(2)
close(S.conj().T@S,D.conj().T@D)
for P in Ps:close(np.linalg.eigvalsh(P),[0,1])
for pv in [0.,4/15,.5,1.]:
    v=np.array([1,0,0,1])/np.sqrt(2)
    eta=pv*np.outer(v,v)+(1-pv)*np.kron(np.diag([1,0]),I/2)
    B=eta.reshape(2,2,2,2).transpose(0,2,1,3).reshape(4,4)
    close(np.linalg.svd(B,compute_uv=False).sum(),pv+np.sqrt((1+pv*pv)/2))
    close(np.linalg.svd(S@B@S.T,compute_uv=False).sum(),(pv+np.sqrt(3+pv*pv))/2)

# Independent symbolic Fourier selection rules for both convex decompositions:
# checking all coordinates suffices for an arbitrary phase, which is retained.
phi=sp.symbols('u',nonzero=True)
roots=[sp.S.One,sp.I,-sp.S.One,-sp.I]
bits=list(product([0,1],repeat=3))
for x,y in product(bits,repeat=2):
    delta=[x[j]-y[j] for j in range(3)]
    fsum=sum(roots[(a*(delta[0]-delta[2])+b*(delta[1]-delta[2]))%4] for a,b in product(range(4),repeat=2))/16
    want=int(x==y or (x,y) in [((0,0,0),(1,1,1)),((1,1,1),(0,0,0))])
    ck(sp.simplify(fsum-want)==0)
    for cut in range(3):
        rest=[j for j in range(3) if j!=cut]
        if x[rest[0]]!=x[rest[1]] or y[rest[0]]!=y[rest[1]]: continue
        exponent=delta[cut]-delta[rest[0]]
        avg=sum(roots[(a*exponent)%4] for a in range(4))/4
        ck(sp.simplify(avg-want)==0)

# Parametric exact reconstruction and weights for arbitrary phase u.
a=(1+3*p)/8;b=(1-p)/8;t=sp.symbols('t',real=True)
ck(sp.expand(4*t+2*(a-t/2)+6*(b-t/2)-1)==0)
ck(sp.expand(2*t+2*(a-t/2)+6*(b-t/6)-1)==0)
ck(sp.expand(4*t*phi/8-t*phi/2)==0)
ck(sp.expand(2*t*phi/4-t*phi/2)==0)

# Author reruns must reproduce the stored JSON byte-for-byte.
for k in range(1,6):
    ck((OUT/f'RERUN_TURN_{k}.json').read_bytes()==(ROOT/'attempt'/f'TURN_{k}_CHECKS.json').read_bytes())

print(json.dumps({'result':'PASS','independent_assertions':checks,
 'scope':'symbolic identities, exact explicit matrix, source/frozen hashes, and separately labeled finite controls',
 'author_rerun_assertions':507443,'unequal_complex_tester_pairs':pair_cases,
 'maximum_sample_tester_value':max_sample_value,'trace_pair_value':1,
 'complex_trilinear_samples':form_cases,'maximum_sample_trilinear_value':max_form,
 'universal_conclusions_from_finite_sampling':False,
 'python':platform.python_version(),'numpy':np.__version__,'sympy':sp.__version__},indent=2))
