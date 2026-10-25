#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product

A,C,G,T=range(4)
XOR=((0,1,2,3),(1,0,3,2),(2,3,0,1),(3,2,1,0))

def det(M):
    M=[list(map(F,row)) for row in M]
    n=len(M); ans=F(1)
    for j in range(n):
        p=next((i for i in range(j,n) if M[i][j]),None)
        assert p is not None
        if p!=j: M[j],M[p]=M[p],M[j]; ans=-ans
        q=M[j][j]; ans*=q
        for k in range(j,n): M[j][k]/=q
        for i in range(j+1,n):
            q=M[i][j]
            if q:
                for k in range(j,n): M[i][k]-=q*M[j][k]
    return ans

def vec(s,g): return (F(1),F(s),F(g),F(s))

def sunlet_q(labels, retic_leaf=2):
    # symmetric parameter assignment; evaluate orientation 3 then permute leaves
    rho=F(1,2); t=F(1,3); k=F(1,2); delta=F(1,2)
    a=b=c=vec(rho,rho); f=vec(t,t); d=e=vec(k,k)
    perm=[i for i in range(3) if i!=retic_leaf]+[retic_leaf]
    inv=[0,0,0]
    for j,i in enumerate(perm): inv[j]=labels[i]
    x,y,z=inv
    if XOR[XOR[x][y]][z]!=A: return F(0)
    return a[x]*b[y]*c[z]*(delta*f[y]*d[z]+(1-delta)*f[x]*e[z])

def transition(s,g):
    return ((1+2*s+g)/4,(1-g)/4,(1-2*s+g)/4,(1-g)/4)

# Physical and CT checks.
for s,g in [(F(1,2),F(1,2)),(F(1,3),F(1,3))]:
    assert all(x>0 for x in transition(s,g))
    assert 0<s<1 and s*s<g<1

# One common strict tensor for all three triangle orientations.
tensors=[]
for r in range(3):
    q={lab:sunlet_q(lab,r) for lab in product(range(4),repeat=3)}
    tensors.append(q)
assert tensors[0]==tensors[1]==tensors[2]
q=tensors[0]
pairs=[]; triples=[]
for lab,val in q.items():
    if val==0 or lab==(A,A,A): continue
    nz=sum(x!=A for x in lab)
    (pairs if nz==2 else triples).append(val)
assert len(pairs)==9 and len(triples)==6
assert set(pairs)=={F(1,12)}
assert set(triples)=={F(1,48)}

# Observable K2P tree equations.
def Q(s): return q[tuple('ACGT'.index(ch) for ch in s)]
X_s,X_g=Q('CCA'),Q('GGA')
Y_s,Y_g=Q('CAC'),Q('GAG')
Z_s,Z_g=Q('ACC'),Q('AGG')
U,V,W=Q('CGT'),Q('CTG'),Q('GCT')
T1=U*U*Y_g-Y_s*Y_s*X_g*Z_g
T2=V*V*X_g-X_s*X_s*Y_g*Z_g
T3=W*W*Z_g-Z_s*Z_s*X_g*Y_g
assert T1==T2==T3==F(-1,82944)

# Exact rank split: 4 JC-symmetric tangent directions and 5 anisotropy directions.
J0=[
 [1,1,0,1],
 [1,0,1,F(1,4)],
 [0,1,1,F(1,4)],
 [1,1,1,1],
]
Jperp=[
 [1,1,0,0,1],
 [1,0,1,F(3,4),F(1,4)],
 [0,1,1,F(1,4),F(1,4)],
 [-1,1,0,0,0],
 [-1,0,1,F(1,2),F(-1,2)],
]
d0=det(J0); dp=det(Jperp)
assert d0==F(-1,2)
assert dp==F(-1,4)
assert d0*dp==F(1,8)

# Exact factor identity behind the tree--sunlet sign obstruction.
try:
    import sympy as sp
except Exception as exc:
    raise SystemExit('SymPy required for the symbolic factor gate') from exc
D,E,f,delta=sp.symbols('D E f delta')
bar=1-delta
N=delta*D+bar*E
L=delta*D+bar*f*E
M=delta*f*D+bar*E
identity=sp.expand(f*N**2-L*M + delta*bar*D*E*(1-f)**2)
assert identity==0

# Strict numerical rational regression of the complete invariant factor.
as_,ag=F(2,5),F(1,3)
bs,bg=F(3,7),F(2,7)
cs,cg=F(4,9),F(1,4)
fs,fg=F(2,5),F(3,8)
ds,dg=F(1,3),F(2,9)
es,eg=F(1,5),F(3,10)
delta=F(2,5); bar=1-delta
qCCA=as_*bs*fs
qGGA=ag*bg*fg
qGAG=ag*cg*(delta*dg+bar*fg*eg)
qAGG=bg*cg*(delta*fg*dg+bar*eg)
qCTG=as_*bs*cg*fs*(delta*dg+bar*eg)
obs=qCTG*qCTG*qGGA-qCCA*qCCA*qGAG*qAGG
fact=-(as_**2)*(bs**2)*ag*bg*(cg**2)*(fs**2)*delta*bar*dg*eg*((1-fg)**2)
assert obs==fact<0

print('K2P_TRIANGLE_COMMON_TENSOR_PASS')
print('K2P_TRIANGLE_RANK9_PASS')
print('K2P_TREE_SUNLET_SIGN_FACTOR_PASS')
print('ALL_CONTINUATION_2_EXACT_CHECKS_PASS')
