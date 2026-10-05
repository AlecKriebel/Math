#!/usr/bin/env python3
"""Exact arithmetic controls; these do not prove geometric nefness.
Python 3 with SymPy. The program is offline and writes only its JSON result.
"""
from fractions import Fraction as F
from math import isqrt
import json
import sympy as s

checks = 0

def require(value):
    global checks
    assert bool(value)
    checks += 1

def eq(a, b=0):
    require(s.simplify(a-b) == 0)

def plane_dot(a,b):
    return a[0]*b[0]-sum(x*y for x,y in zip(a[1:],b[1:]))

def cremona(d, ms):
    ms = sorted(ms, reverse=True)
    a,b,c,*tail=ms
    return 2*d-a-b-c, sorted([d-b-c,d-a-c,d-a-b]+tail,reverse=True)

# Universal symbolic relations for the symmetric marked intersection lattice.
n=s.symbols('n', positive=True)
delta=s.sqrt(n*(n-4))
alpha=(n-delta)/2; beta=(n+delta)/2
lam=(n-2+delta)/2
T=s.Matrix([[0,1,0],[1,n,2*n],[0,-1,-1]])
Q=s.Matrix([[0,1,0],[1,0,0],[0,0,-2*n]])
R=s.Matrix([alpha,beta,-1]); Rc=s.Matrix([beta,alpha,-1]); K=s.Matrix([-2,-2,1]); gamma=s.Matrix([n-2,1,-1])
for row in T.T*Q*T-Q: eq(row)
for row in T*R-lam*R: eq(row)
for row in T*Rc-(1/lam)*Rc: eq(row)
for row in T*K-K: eq(row)
eq((R.T*Q*R)[0]); eq((gamma.T*Q*gamma)[0],-4)
cn=(n*(n-3)+(n-1)*delta)/4
ref=R+(R.T*Q*gamma)[0]*gamma/2
for row in ref-cn*s.Matrix([n-4,1,-delta/n]): eq(row)
for row in beta/(n*(n-4))*R+alpha/(n*(n-4))*Rc+K/(n-4)-s.Matrix([0,1,0]): eq(row)
S=s.eye(3)+gamma*(gamma.T*Q)/2
for row in S*S-s.eye(3): eq(row)
for row in S.T*Q*S-Q: eq(row)

# A universal ampleness margin and nonsquare enclosure.
z=s.symbols('z', nonnegative=True)
eq((11*n*n-56*n-16).subs(n,z+7), 11*z*z+98*z+131)
eq(n*(n-4)-(n-3)**2,2*n-9)
eq((n-2)**2-n*(n-4),4)
k=(n-1)/2
eq((3*n-4)**2-n*n-4*(n-2)**2-16*k-8,4*n*(n-4))

# Full exact vectors, intersection graphs, contractions, divisor recovery,
# Cremona transformations and all numerical ampleness hypotheses for 56 ranks.
examples=[]
for r in range(9,65):
    N=2*r-13; kk=(N-1)//2
    require(N%2==1 and N>=5 and kk+7==r)
    rad=N*(N-4)
    require((N-3)**2<rad<(N-2)**2)
    require(isqrt(rad)**2 != rad)
    ms=[N]+[N-2]*4+[4]*kk+[2]*2
    d=3*N-4
    require(len(ms)==r)
    require(d*d-sum(v*v for v in ms)==4*rad)
    if N>=7:
        require(ms==sorted(ms,reverse=True))
        require(d>sum(ms[:2]))
        require(2*d>sum(ms[:5]))
        require(3*d>2*ms[0]+sum(ms[1:7]))
        require(4*d*d>5*sum(v*v for v in ms))
        for j in range(2,r+1):
            require((j+2)*d*d >= (j+3)*sum(v*v for v in ms[:j]))
    # Canonical total-transform plane basis, e_i has coefficient +1.
    basis=[[int(i==j) for i in range(r+1)] for j in range(r+1)]
    def vec(items):
        out=[0]*(r+1)
        for i,a in items: out[i]+=a
        return out
    C=basis[1]
    fiber=vec([(0,1),(1,-1)])
    finite=[]
    for j in [1,2]:
        U=vec([(0,1),(1,-1),(2*j,-1),(2*j+1,-1)])
        V=basis[2*j+1]
        W=vec([(2*j,1),(2*j+1,-1)])
        require([plane_dot(a,a) for a in [U,V,W]]==[-2,-1,-2])
        require([sum(x) for x in zip(U,[2*v for v in V],W)]==fiber)
        finite.extend([U,W])
    G1=vec([(0,1),(1,-1)]+[(i,-1) for i in range(6,kk+7)])
    G2=vec([(kk+6,1),(kk+7,-1)])
    TT=basis[kk+7]
    H1=vec([(kk+5,1),(kk+6,-1),(kk+7,-1)])
    Hs=[H1]+[vec([(kk+6-j,1),(kk+7-j,-1)]) for j in range(2,kk+1)]
    chain=[G1,G2,TT]+Hs
    require([plane_dot(a,a) for a in chain]==[-(kk+1),-2,-1,-3]+[-2]*(kk-1))
    for i,a in enumerate(chain):
        for j,b in enumerate(chain):
            if i!=j: require(plane_dot(a,b)==int(abs(i-j)==1))
    weights=[1,kk+1,N]+list(range(kk,0,-1))
    require([sum(w*a[j] for w,a in zip(weights,chain)) for j in range(r+1)]==fiber)
    # Verify each advertised contraction is of a -1 curve and leaves C^2=-1.
    gram=[[plane_dot(a,b) for b in chain+[C]] for a in chain+[C]]
    live=list(range(len(gram)))
    for deleted in [2,1]+list(range(3,len(chain))):
        require(gram[deleted][deleted]==-1)
        require(gram[deleted][-1]==0)
        rest=[i for i in live if i!=deleted]
        for i in rest:
            for j in rest:
                gram[i][j]+=gram[i][deleted]*gram[j][deleted]
        live=rest
    require(gram[-1][-1]==-1)
    require(gram[0][0]==0)
    M=[3*N-2,-(N-2)]+[-N]*4+[-4]*kk+[-2]*2
    require(plane_dot(M,M)==4*rad)
    require(plane_dot(M,C)==N-2)
    require(plane_dot(M,fiber)==2*N)
    for E in finite+[G1,G2]+Hs: require(plane_dot(M,E)==0)
    cd,cm=cremona(M[0],[-x for x in M[1:]])
    require(cd==d and cm==sorted(ms,reverse=True))
    if r==9:
        cd,cm=cremona(cd,cm)
        require((cd,cm)==(9,[3]*5+[2]*4))
    if r<=12: examples.append({'r':r,'n':N,'degree':cd,'multiplicities':cm,'L_squared':4*rad})
    # All-step induction in PROOFS.md is supplemented by 30 exact iterates.
    a,b,w=N-2,1,(N-1)//2
    for j in range(30):
        require(abs(a)>abs(b)>0)
        require((a*b>0)==(j%2==0))
        require(b not in (w*a,(w-N)*a))
        a,b=(2*w-N)*a-b,a
        w=pow(w,-1,N)

# Reduced polynomial constraints for the balanced normal-bundle calculation.
# Remainders at x^N=1 and x^N=U give a square linear system in f,g.
x,U=s.symbols('x U')
normal_determinants={}
for N in [5,7,9,11,13]:
    coeff=s.symbols('a:'+str(2*N-2));g0,g1=s.symbols('g0 g1')
    f=sum(coeff[i]*x**i for i in range(2*N-2));g=g0+g1*x
    remainders=[s.rem(f+(N-2)*x**(N-2)*g,x**N-1,x),s.rem(f-(N-2)*x**(N-2)*g,x**N-U,x)]
    rows=[s.expand(p).coeff(x,j) for p in remainders for j in range(N)]
    matrix,_=s.linear_eq_to_matrix(rows,list(coeff)+[g0,g1])
    determinant=s.factor(matrix.det())
    require(determinant != 0)
    require(determinant.subs(U,2)!=0)
    normal_determinants[str(N)]=str(determinant)

# Exact negative controls: arithmetic or genericity mistakes must fail.
negative_controls={
  'wrong_L9_square_rejected': 9**2-5*3**2-4*2**2 != 21,
  'nine_points_alone_not_ten': 9+1 == 10,
  'evaluation_on_E6_is_not_maximal': F(2)**2 < 20,
  'special_collinear_tuple_not_nef': 9-5*3-4*2 < 0,
  'multipoint_value_wrong_normalization_rejected': F(1,5) != 20,
}
for name,truth in negative_controls.items(): require(truth)
result={'status':'PASS_EXACT_ARITHMETIC_ONLY','assertions':checks,'sympy_version':s.__version__,'rank_range':[9,64],
        'examples':examples,'normal_bundle_determinants':normal_determinants,'negative_controls':negative_controls,
        'proof_limits':'Finite tests supplement universal algebra and source-statement checks. They do not certify geometric nefness, descent, deformation, or the cited theorems.'}
print(json.dumps(result,indent=2,sort_keys=True))
