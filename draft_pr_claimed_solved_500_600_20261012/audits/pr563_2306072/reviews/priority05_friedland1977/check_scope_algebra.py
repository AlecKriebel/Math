"""Exact finite source-comparison checks; not a proof of classical control theorems."""
from fractions import Fraction as F
from pathlib import Path
import json
BASE=Path(__file__).resolve().parent
checks=[]
def ck(n,ok,d):
    assert ok,n
    checks.append({'name':n,'passed':bool(ok),'detail':d})
def plus(a,b):
    c=a.copy()
    for k,v in b.items(): c[k]=c.get(k,F(0))+v
    return {k:v for k,v in c.items() if v}
def scale(a,c):return {k:c*v for k,v in a.items() if c*v}
def mul(a,b):
    c={}
    for k,v in a.items():
        for l,w in b.items():
            n=tuple(x+y for x,y in zip(k,l)) if isinstance(k,tuple) else k+l
            c[n]=c.get(n,F(0))+v*w
    return {k:v for k,v in c.items() if v}
# Ordinary x polynomials for source's exact adjoint family.
A=[{0:F(4),1:F(-20),2:F(30),3:F(-14)}, {1:F(10),2:F(-24),3:F(14)}, {2:F(6),3:F(-6)}, {3:F(1)}]
B=[[F(0),0,0,0],[2,1,0,0],[2,4,2,0],[2,4,6,3]]; D=[1,-1,1,-1]
for i in range(4):
    lhs={k:-k*v for k,v in A[i].items() if k}
    rhs={}
    for j in range(4): rhs=plus(rhs,scale(A[j],-D[i]*B[j][i]*D[j]))
    ck(f'adjoint_ode_component_{i+1}',lhs==rhs,'−x dA/dx = −D BᵀD A, source(4.69)')
ck('initial_a4_functional', [sum(v.values()) for v in A]==[0,0,0,1],'A(1)=(0,0,0,1)')
value={}
for i in range(4):value=plus(value,scale(A[i],i+1))
ck('koebe_saturation',value=={0:F(4)},'A(x)·(1,2,3,4)=4 identically')
reduced=[{k-1:v for k,v in p.items()} for p in A[1:]]
ck('degree_four_weights',reduced==[{0:F(10),1:F(-24),2:F(14)},{1:F(6),2:F(-6)},{2:F(1)}],'λ2=2(7x²−12x+5), λ3=6x(1−x), λ4=x²')
ck('degree_four_bound',{k-1:-v for k,v in A[0].items() if k}=={0:F(20),1:F(-30),2:F(14)},'(4−A1(x))/x=20−30x+14x²')
# Gaussian rational pairs for the exact candidate invariant.
def gm(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def gi(a):
    d=a[0]*a[0]+a[1]*a[1];return(a[0]/d,-a[1]/d)
eps=F(1,10**24); l2=(F(1),F(0));l3=(F(0),-3*eps);l4=(F(0),eps)
inv=gm(gm(l3,l3),gi(gm(l2,l4)))
ck('candidate_rotation_invariant',inv==(0,9*eps) and inv[1]!=0,{'Re':str(inv[0]),'Im':str(inv[1]),'real_prior_family_invariant':'real whenever λ2λ4≠0; candidate all3weights nonzero'})
ck('rotation_phase_exponents',2*2==1+3,'Normalized rotations multiply λ2,λ3,λ4 by q,q²,q³; λ3²/(λ2λ4) unchanged; common phase/scalar cancels.')
# Multivariate formal coefficient extraction: variables a2,a3,a4,J=i*epsilon.
one={(0,0,0,0):F(1)}
a2={(1,0,0,0):F(1)};a3={(0,1,0,0):F(1)};a4={(0,0,1,0):F(1)};J={(0,0,0,1):F(1)}
f=[{},one,a2,a3,a4]
def zprod(a,b):
    out=[{} for _ in range(5)]
    for j in range(5):
        for k in range(5-j):out[j+k]=plus(out[j+k],mul(a[j],b[k]))
    return out
powers={1:f}
for v in range(2,5):powers[v]=zprod(powers[v-1],f)
def L(p):return plus(p[2],mul(J,plus(p[4],scale(p[3],F(-3)))))
a=plus(one,mul(J,plus(plus(scale(a3,2),mul(a2,a2)),scale(a2,-6))))
b=mul(J,plus(scale(a2,3),scale(one,-3)));c=J
for v,expected in [(2,a),(3,b),(4,c)]:
    got=L(powers[v]);ck(f'schiffer_power_coefficient_{v}',got==expected,f'L(f^{v}) matches candidate differential coefficient; sourceA_{v}=L(f^{v})/2')
FS={-3:scale(a,F(1,2)),-4:scale(b,F(1,2)),-5:scale(c,F(1,2))}
QD={-3:scale(a,-1),-4:scale(b,-1),-5:scale(c,-1)}
ck('schiffer_sign_translation',all(FS[k]==scale(QD[k],F(-1,2)) for k in FS),'P_FS(1/w)/w²=−Q_Duren(w)/2; source≤0 equals candidate≥0')
# Local theorem5.4 concerns coefficient size, with k² factored out.
v={1:F(1)};v2=mul(v,v);v2m=plus(v2,{0:F(-1)})
local=plus(scale(mul(v2,v2m),F(-1,9)),scale(mul(v2m,v2m),F(1,9)))
ck('local_coefficient_modulus_expansion',local==scale(v2m,F(-1,9)),'|a_v(s)|²=v²−(k²/9)(v²−1)s²+O(s³), no θ/β sign assertion')
ck('koebe_finite_tip',F(-1)/(1-F(-1))**2==F(-1,4),'Koebe k(−1)=−1/4; omitted ray has constant θ and β=0')
out={'status':'PASS','count':len(checks),'checks':checks,'limits':['Finite identities only; external analytic source theorems are inspected in the report, not formalized here.','Invariant excludes exact matching to explicit Cor4.2family and its phase-scaled rotations, not every implicit/global maximizer addressed by this broad method.','No original or current firstness certificate; unreadZemyan fulltexts remain unclosed.']}
(BASE/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
