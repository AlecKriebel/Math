"""Independent SymPy magnetic-band and all-direction 8x8 Hessian controls.
Run with the pre-existing absolute SymPy interpreter specified in provenance.
No imports from the candidate packet. Exact algebra throughout core controls.
"""
import json, math, sys, hashlib
from pathlib import Path
from fractions import Fraction
import sympy as S

count=0
checks={}
def check(b, key=None):
    global count
    if not bool(b): raise AssertionError(key)
    count+=1
    if key: checks[key]=True
r=S.sqrt(3); I=S.I
E,z,w=S.symbols('E z w', nonzero=True)
d=[z+1/z, I*z-I/z, -z-1/z, -I*z+I/z]
F=S.diag(*d)
for j in range(3): F[j,j+1]=F[j+1,j]=1
F[3,0]=w; F[0,3]=1/w
expected=E**4-8*E**2+4-z**4-z**-4-w-w**-1
check(S.expand((E*S.eye(4)-F).det()-expected)==0,'harper_laurent_determinant')

# Independent square-root derivative controls; all-degree proof is in the report.
t=S.symbols('t', real=True)
f=S.sqrt(4+S.sqrt(12+2*t))
derivatives=[]
for m in range(1,9):
    dm=S.diff(f,t,m)
    for tv in [-2,-1,0,1,2]:
        check(S.sign(dm.subs(t,tv))==(-1)**(m-1))
    derivatives.append({'order':m,'sign':(-1)**(m-1)})
alpha,beta=S.symbols('alpha beta', real=True)
energy=-4*S.sqrt(4+S.sqrt(12+2*S.cos(alpha)+2*S.cos(beta)))
loop_hess=S.hessian(energy,(alpha,beta)).subs({alpha:0,beta:0})
check(loop_hess==S.eye(2)*S.sqrt(2)/8,'4x4_holonomy_hessian')

# Derive 8x8 spectral projectors independently by Lagrange interpolation.
lambdas=[-1-r,1-r,-1+r,1+r]
p=S.Symbol('p')
projector_coefficients=[]
for k,lam in enumerate(lambdas):
    q=S.prod((p-other)/(lam-other) for j,other in enumerate(lambdas) if j!=k)
    poly=S.Poly(S.expand(q),p)
    co=[S.simplify(poly.nth(j)) for j in range(4)]
    projector_coefficients.append(co)
    check(S.simplify(sum(co[j]*lam**j for j in range(4))-1)==0)
    for j,other in enumerate(lambdas):
        check(S.simplify(sum(co[d]*other**d for d in range(4)))==(1 if j==k else 0))
L=8; N=L*L
idx=lambda x,y:(x%L)+L*(y%L)
T=S.zeros(N)
edges=[]
for y in range(L):
    for x in range(L):
        u=idx(x,y)
        for v,h in [(idx(x+1,y),-1 if x==L-1 else 1),(idx(x,y+1),I**x*(-1 if y==L-1 else 1))]:
            T[u,v]=h;T[v,u]=S.conjugate(h);edges.append((u,v,h))
T2=T*T; T3=T2*T; T4=T2*T2
check((T4-8*T2+4*S.eye(N)).applyfunc(S.expand)==S.zeros(N),'8x8_minimal_polynomial')
check(T==T.conjugate().T,'8x8_hermitian')
powers=[S.eye(N),T,T2,T3]
projectors=[]
for co in projector_coefficients:
    P=sum((powers[d]*co[d] for d in range(4)),S.zeros(N))
    P=P.applyfunc(S.expand)
    projectors.append(P)
    check(S.simplify(S.trace(P))==16)
    check((T*P-lambdas[len(projectors)-1]*P).applyfunc(S.expand)==S.zeros(N))
P=projectors[0]
for u,v,h in edges:
    check(S.simplify(I*h*P[v,u]-I*S.conjugate(h)*P[u,v])==0)
check(lambdas[1]-lambdas[0]==2,'occupied_gap_2')

# Independent sparse edge contractions of the spectral-projector derivative.
# Two first rows determine all rows by a separately proved magnetic-translation symmetry.
def derivative_terms(edge):
    u,v,h=edge
    return [(u,v,I*h),(v,u,-I*S.conjugate(h))]
def hessian_element(e,f):
    direct=-(P[edges[e][1],edges[e][0]]*edges[e][2]+P[edges[e][0],edges[e][1]]*S.conjugate(edges[e][2])) if e==f else 0
    ans=direct
    for lam,Q in zip(lambdas[1:],projectors[1:]):
        term=0
        for a,b,k in derivative_terms(edges[e]):
            for c,d,l in derivative_terms(edges[f]):
                term+=P[d,a]*Q[b,c]*k*l
        ans += 2*S.re(S.expand(term))/(lambdas[0]-lam)
    return S.expand(ans)
row=[[],[]]
for e in range(2):
    for fedge in range(2*N):row[e].append(hessian_element(e,fedge))
H=S.zeros(2*N)
for e in range(2*N):
    ve,oe=divmod(e,2);xe,ye=ve%L,ve//L
    for fe in range(2*N):
        vf,of=divmod(fe,2);xf,yf=vf%L,vf//L
        H[e,fe]=row[oe][2*idx(xf-xe,yf-ye)+of]
check(H==H.T,'full_hessian_symmetric')
G=S.zeros(2*N,N)
for e,(u,v,h) in enumerate(edges):G[e,u]=-1;G[e,v]=1
check(G.rank()==63,'gauge_rank_63')
check((H*G).applyfunc(S.expand)==S.zeros(2*N,N),'full_gauge_kernel')

# Fourier blocks, computed as actual matrices, not only trace samples.
blocks=[];positive=0;nulls=0
D=10**15
bounds={2:(1414213562373095,1414213562373096),3:(1732050807568877,1732050807568878),6:(2449489742783178,2449489742783179)}
for rad,(lo,hi) in bounds.items():check(lo*lo<rad*D*D<hi*hi)
def radical_co(expr):
    ex=S.expand(expr)
    co=[ex.coeff(S.sqrt(6)),ex.coeff(S.sqrt(3)),ex.coeff(S.sqrt(2))]
    a=S.expand(ex-co[0]*S.sqrt(6)-co[1]*S.sqrt(3)-co[2]*S.sqrt(2))
    return [a,co[2],co[1],co[0]]
def strict_lower(expr):
    co=radical_co(expr)
    val=co[0]*D
    for c,k in zip(co[1:],[2,3,6]):val+=c*(bounds[k][0] if c>=0 else bounds[k][1])
    return val/D
kappa=(7*r-9)/144
for ky in range(L):
    for kx in range(L):
        B=S.zeros(2)
        for y in range(L):
            for x in range(L):
                # 8th roots explicitly represented to avoid transcendental simplification.
                angle=(kx*x+ky*y)%8
                phase=[1,(1+I)/S.sqrt(2),I,(-1+I)/S.sqrt(2),-1,(-1-I)/S.sqrt(2),-I,(1-I)/S.sqrt(2)][angle]
                for a in range(2):
                    for b in range(2):B[a,b]+=row[a][2*idx(x,y)+b]*phase
        B=B.applyfunc(S.expand)
        check(B==B.conjugate().T)
        tr=S.expand(S.trace(B));det=S.expand(B.det())
        check(strict_lower(tr)>0)
        if kx==ky==0:
            check(B==S.eye(2)*kappa,'zero_frequency_two_positive')
            positive+=2
        else:
            check(det==0)
            check(S.simplify(tr-kappa)>0)
            positive+=1;nulls+=1
        blocks.append({'kx':kx,'ky':ky,'matrix':[[str(B[a,b]) for b in range(2)] for a in range(2)],'trace':str(tr),'determinant':str(det),'strict_trace_lower':str(strict_lower(tr))})
check((positive,nulls)==(65,63),'complete_inertia_65_63')

# Full matrix values bind exact independent reproduction, with compact Fourier proof.
out=Path(__file__).resolve().parent
htext='\n'.join(','.join(str(H[i,j]) for j in range(2*N)) for i in range(2*N))+'\n'
(out/'independent_full_hessian.txt').write_text(htext)

# Holonomy curvature for L8 from uniform class n2.
a,b=S.symbols('a b',real=True)
c0,c1=S.cos(a/2),-S.cos(a/2)
d0,d1=S.cos(b/2),-S.cos(b/2)
e8=-4*sum(f.subs(t,c+d) for c in [c0,c1] for d in [d0,d1])
loop8=S.hessian(e8,(a,b)).subs({a:S.pi,b:S.pi}).applyfunc(S.simplify)
# A distributed holonomy direction has 64 entries 1/8 and norm one.
check(loop8==S.eye(2)*kappa,'8x8_loop_curvature_matches_full_hessian')

# Wrong Hessian transition sign is detected by exact gauge invariance.
wrong=2*(1+r)/8*S.eye(2*N)-H
check((wrong*G).applyfunc(S.expand)!=S.zeros(2*N,N),'wrong_transition_sign_mutant_rejected')
missing=H-(1+r)/8*S.eye(2*N)
check((missing*G).applyfunc(S.expand)!=S.zeros(2*N,N),'missing_direct_term_mutant_rejected')

# Smoothness countercontrol: an occupied/unoccupied degeneracy gives a cusp.
u=S.symbols('u',real=True)
check(S.limit((-S.Abs(u)-0)/u,u,0,dir='+')==-1)
check(S.limit((-S.Abs(u)-0)/u,u,0,dir='-')==1)
result={'assertions':count,'checks':checks,'sympy_version':S.__version__,'python':sys.version,'projector_coefficients':[[str(x) for x in co] for co in projector_coefficients],'spectral_values':[str(x) for x in lambdas],'spectral_multiplicities':[16]*4,'gap':2,'derivative_sign_controls':derivatives,'hessian_positive':positive,'hessian_nullity':nulls,'kappa':str(kappa),'holonomy_hessian_4x4':str(loop_hess),'holonomy_hessian_8x8':str(loop8),'full_hessian_sha256':hashlib.sha256(htext.encode()).hexdigest(),'fourier_blocks':blocks,'scope':'Exact full 8x8 phase Hessian via independent symbolic projectors and magnetic translation; all-size uniform holonomy proof checked separately in report.'}
print(json.dumps(result,indent=2,sort_keys=True))
