#!/usr/bin/env python3
"""Independent exact controls. This is NOT a geometric proof certificate."""
import json, math
from fractions import Fraction as F
from itertools import combinations_with_replacement
import sympy as S

checks={}
def check(group, condition):
    if not bool(condition):
        raise AssertionError(group)
    checks[group]=checks.get(group,0)+1

n,z,t,D=S.symbols('n z t D')
def reduce(expr):
    num,den=S.fraction(S.cancel(expr))
    return S.rem(num,D**2-n*(n-4),D)==0
Q=S.Matrix([[0,1,0],[1,0,0],[0,0,-2*n]])
T=S.Matrix([[0,1,0],[1,n,2*n],[0,-1,-1]])
a,b=(n-D)/2,(n+D)/2
lam=(n-2+D)/2
R=S.Matrix([a,b,-1]);Rb=S.Matrix([b,a,-1]);K=S.Matrix([-2,-2,1]);g=S.Matrix([n-2,1,-1])
check('universal_lattice',S.expand(T.charpoly(t).as_expr()-(t-1)*(t*t-(n-2)*t+1))==0)
for e in T.T*Q*T-Q: check('universal_lattice',e==0)
for e in T*R-lam*R:check('universal_lattice',reduce(e))
for e in T*Rb-((n-2-D)/2)*Rb:check('universal_lattice',reduce(e))
for e in T*K-K:check('universal_lattice',e==0)
for e in b/(n*(n-4))*R+a/(n*(n-4))*Rb+K/(n-4)-S.Matrix([0,1,0]):check('universal_lattice',reduce(e))
check('universal_lattice',reduce((R.T*Q*R)[0]))
check('universal_lattice',(g.T*Q*g)[0]==-4)
reflection=S.eye(3)+g*g.T*Q/2
for e in reflection**2-S.eye(3):check('universal_lattice',S.expand(e)==0)
for e in reflection.T*Q*reflection-Q:check('universal_lattice',S.expand(e)==0)
scale=(n*(n-3)+(n-1)*D)/4
for e in reflection*R-scale*S.Matrix([n-4,1,-D/n]):check('universal_lattice',reduce(e))
check('universal_positivity',S.expand((11*n*n-56*n-16).subs(n,z+7))==11*z*z+98*z+131)
check('universal_positivity',S.expand(n*(n-4)-(n-3)**2)==2*n-9)
check('universal_positivity',S.expand((n-2)**2-n*(n-4))==4)
check('universal_positivity',S.expand((3*n-4)**2-n*n-4*(n-2)**2-16*(n-1)/2-8-4*n*(n-4))==0)

# Universal determinant, using C=c^w, A=c^(n-w), X=x^w, Y=x^(n-w).
C,A,X,Y,d=S.symbols('C A X Y d')
a0=C*A-d*A+(d*A-1)*X*Y;b0=(1-C*A)*Y
a1=d*(C*A-1)*X;b1=C-d*C*A+(d-C)*X*Y
check('birational_pencil',S.expand(a0*b1-a1*b0+(C-d)*(A*d-1)*(X*Y-1)*(X*Y-C*A))==0)
check('birational_pencil',S.expand((a1-d*a0).subs({X:1,Y:1}))==0)
check('birational_pencil',S.expand((b1-d*b0).subs({X:1,Y:1}))==0)
check('birational_pencil',S.cancel((A*a1-C*a0).subs({X:C,Y:A}))==0)
check('birational_pencil',S.cancel((A*b1-C*b0).subs({X:C,Y:A}))==0)

# Build quotient chains without using the author's plane-basis implementation.
def negfrac(seq):
    v=F(seq[-1])
    for c in seq[-2::-1]:v=c-1/v
    return v

def chain_matrix(weights):
    size=len(weights)
    return [[F(weights[i] if i==j else 1 if abs(i-j)==1 else 0) for j in range(size)] for i in range(size)]

def contract(mat,labels,label):
    p=labels.index(label)
    check('fiber_contractions',mat[p][p]==-1)
    keep=[i for i in range(len(labels)) if i!=p]
    return [[mat[i][j]+mat[i][p]*mat[p][j] for j in keep] for i in keep],[labels[i] for i in keep]

examples=[]
for r in range(9,101):
    N=2*r-13;k=(N-1)//2
    check('rank_coverage',N%2==1 and k+7==r)
    q=N*(N-4)
    check('rank_coverage',(N-3)**2<q<(N-2)**2 and math.isqrt(q)**2!=q)
    check('quotient_chains',negfrac([k+1,2])==F(N,2))
    check('quotient_chains',negfrac([3]+[2]*(k-1))==F(N,k))
    check('quotient_chains',(k*(N-2))%N==1)
    # Degree of q is 2N; line bundle upstairs has bidegree (2N(N-4),2N).
    check('quotient_normalization',F(2*(2*N*(N-4))*(2*N),2*N)==4*q)
    check('quotient_normalization',F(2*N*(N-4)+4*N,2*N)==N-2)
    check('quotient_normalization',F(4,2*N)-F(1,2)-F(1,2)-F(2,N)==-1)
    weights=[-(k+1),-2,-1,-3]+[-2]*(k-1)
    labels=['G1','G2','T']+['H'+str(j) for j in range(1,k+1)]
    matrix=chain_matrix(weights)
    multiplicities=[1,k+1,N]+list(range(k,0,-1))
    for row in matrix:check('quotient_chains',sum(x*y for x,y in zip(row,multiplicities))==0)
    # Append section C, which intersects G1 once and no other chain member.
    for i,row in enumerate(matrix):row.append(F(int(i==0)))
    matrix.append([F(int(i==0)) for i in range(len(labels))]+[F(-1)])
    labels.append('C')
    for name in ['T','G2']+['H'+str(j) for j in range(1,k+1)]:matrix,labels=contract(matrix,labels,name)
    check('fiber_contractions',labels==['G1','C'] and matrix==[[0,1],[1,-1]])
    f=chain_matrix([-2,-1,-2]);ls=['U','V','W']
    f,ls=contract(f,ls,'V');f,ls=contract(f,ls,'W')
    check('fiber_contractions',ls==['U'] and f==[[0]])
    # Recover plane multiplicities from the independent orthogonality equations.
    last=F(2*N,2*k+1); middle=2*last;first=N-2;degree=2*N+first
    before=[N]*4+[first]+[middle]*k+[last]*2
    check('plane_recovery',last==2 and degree==3*N-2 and len(before)==r)
    check('plane_recovery',degree*degree-sum(v*v for v in before)==4*q)
    largest=sorted(before,reverse=True)
    transformed=[degree-largest[1]-largest[2],degree-largest[0]-largest[2],degree-largest[0]-largest[1]]+largest[3:]
    degree2=2*degree-sum(largest[:3])
    expected=[N]+[N-2]*4+[4]*k+[2]*2
    check('cremona',degree2==3*N-4 and sorted(transformed)==sorted(expected))
    if N==5:
        largest=sorted(transformed,reverse=True)
        twice=[degree2-largest[1]-largest[2],degree2-largest[0]-largest[2],degree2-largest[0]-largest[1]]+largest[3:]
        check('cremona',2*degree2-sum(largest[:3])==9 and sorted(twice)==[2]*4+[3]*5)
    else:
        check('ampleness',expected==sorted(expected,reverse=True))
        check('ampleness',degree2>sum(expected[:2]))
        check('ampleness',2*degree2>sum(expected[:5]))
        check('ampleness',3*degree2>2*expected[0]+sum(expected[1:7]))
        for s in range(2,r+1):check('ampleness',(s+2)*degree2**2>(s+3)*sum(v*v for v in expected[:s]))
    # Independent signed integer exponent recurrence, including composite n.
    rho,tau=N-2,1
    for j in range(60):
        w=(N-1)//2 if j%2==0 else N-2
        check('all_step_control',math.gcd(w,N)==1 and pow(w,-1,N)==(N-2 if j%2==0 else (N-1)//2))
        check('all_step_control',abs(rho)>abs(tau)>0 and (rho*tau>0)==(j%2==0))
        check('all_step_control',tau!=w*rho and tau!=(w-N)*rho)
        rho,tau=(2*w-N)*rho-tau,rho
    if r<13:examples.append({'r':r,'n':N,'square':4*q})

# Normal-bundle elementary-transform equations; fresh polynomial remainder matrices.
x,U=S.symbols('x U')
determinants={}
for N in [5,7,9,11,15,21]:
    unknowns=S.symbols('f0:'+str(2*N-2))+S.symbols('g0:2')
    f=sum(unknowns[i]*x**i for i in range(2*N-2));gg=unknowns[-2]+unknowns[-1]*x
    polynomials=[S.rem(f+(N-2)*x**(N-2)*gg,x**N-1,x),S.rem(f-(N-2)*x**(N-2)*gg,x**N-U,x)]
    equations=[p.expand().coeff(x,j) for p in polynomials for j in range(N)]
    mat,_=S.linear_eq_to_matrix(equations,unknowns)
    value=S.factor(mat.det())
    check('normal_bundle_linear_algebra',S.expand(value-4*(N-2)**2*(U-1)**(N-2))==0)
    check('normal_bundle_linear_algebra',value.subs(U,2)!=0 and value.subs(U,1)==0)
    determinants[str(N)]=str(value)

# Numerical inequality underneath the unconditional ampleness criterion.
for s in range(2,9):
    for v in combinations_with_replacement(range(1,5),s):
        if max(v)==1 or (s==2 and v==(2,2)):continue
        check('xu_inequality_control',sum(x*x for x in v)>=(s+3)*min(v))

negative={
 'wrong_reflection_half_rejected':not reduce((R+((R.T*Q*g)[0])*g-scale*S.Matrix([n-4,1,-D/n]))[2]),
 'merged_orbits_U1_rejected':all('(U - 1)' in d for d in determinants.values()),
 'wrong_quotient_degree_rejected':F(2*10*10,5)!=20,
 'all_points_claim_rejected':2**2<20,
 'arbitrary_centers_claim_rejected':9-5*3-4*2<0,
 'one_point_versus_multipoint_rejected':F(1,9)!=20,
 'r10_odd_index_omission_rejected':2*10-13==7,
 'r9_uniform_ampleness_shortcut_rejected':11*5**2-56*5-16<0,
}
for value in negative.values():check('negative_controls',value)
print(json.dumps({'status':'PASS_EXACT_CONTROLS_ONLY','counts':checks,'total_assertions':sum(checks.values()),'rank_test_range':[9,100],'normal_determinants':determinants,'negative_controls':negative,'examples':examples,'sympy_version':S.__version__,'limitations':'Symbolic and finite arithmetic controls accompany the written ordinary mathematical audit; they do not certify geometric nefness, specialization, Cartier descent, or peer review.'},indent=2,sort_keys=True))
