#!/usr/bin/env python3
"""Exact controls for the partial focal-feasibility audit. Python 3 + SymPy."""
import json
from pathlib import Path
from itertools import product
import sympy as S
z=S.symbols('z')
checks=0

def ck(c):
    global checks
    if not bool(c): raise AssertionError('control %s failed' % (checks+1))
    checks+=1

def nd(F):
    a,b,c,d,e,f,g,h,i=list(F)
    return (S.expand(-i*(b*c*i-c*c*h+e*f*i-f*f*h)),
            S.expand(a*b*g*i-a*c*g*h+b*b*h*i-b*c*h*h+d*e*g*i-d*f*g*h+e*e*h*i-e*f*h*h))

def rank_guard(F):
    return S.expand(sum(F.extract(i,j).det()**2 for i in [(0,1),(0,2),(1,2)] for j in [(0,1),(0,2),(1,2)]))

def inertia(A):
    """Rational congruence; also handles a zero diagonal with nonzero off-diagonal."""
    A=A.copy(); n0=A.rows; pos=neg=0
    while A.rows:
        n=A.rows
        pivot=next((i for i in range(n) if A[i,i]!=0),None)
        if pivot is None:
            edge=next(((i,j) for i in range(n) for j in range(i+1,n) if A[i,j]!=0),None)
            if edge is None: break
            i,j=edge;Q=S.eye(n);Q[j,i]=1;A=Q.T*A*Q;pivot=i
        if pivot:
            A.row_swap(0,pivot);A.col_swap(0,pivot)
        d=A[0,0];pos+=int(bool(d>0));neg+=int(bool(d<0))
        A=A[1:,1:]-A[1:,0:1]*A[0:1,1:]/d
    return pos,neg,n0-pos-neg

def hermite(p,h):
    p=S.Poly(p,z)
    if p.is_zero: raise ValueError('identically singular pencil is positive-dimensional')
    p=p.sqf_part().monic();n=p.degree()
    if n==0:return S.zeros(0)
    C=S.zeros(n)
    for j in range(n):
        r=S.Poly(z**(j+1),z).rem(p)
        for i in range(n):C[i,j]=r.nth(i)
    h=S.Poly(h,z).rem(p);Hc=S.zeros(n)
    for (i,),a in h.terms():Hc+=a*C**i
    return S.Matrix(n,n,lambda i,j:S.trace(Hc*C**(i+j)))

def tq(p,h):
    a,b,_=inertia(hermite(p,h));return a-b

def chart_count(F):
    p=S.expand(F.det());n1,d1=nd(F);n2,d2=nd(F.T)
    q1=n1*d1;q2=n2*d2;R=rank_guard(F)
    T={(a,b):tq(p,R*q1**a*q2**b) for a in (0,1,2) for b in (0,1,2)}
    numer=sum(T[a,b] for a in (1,2) for b in (1,2))
    ck(numer%4==0)
    return {'real_rank_two':T[0,0], 'positive_in_chart':numer//4,
            'at_least_one_zero_q':T[0,0]-T[2,2],
            'queries':{str(k):v for k,v in T.items()}}

def essential_residual(F,a,b):
    B=F*S.diag(a,a,1)*F.T*S.diag(b,b,1)
    return (2*B*F-S.trace(B)*F).applyfunc(S.factor)

def design(pairs):return S.Matrix([[b*a for b in y for a in x] for x,y in pairs])

def values(F):return [S.cancel(n/d) for n,d in [nd(F),nd(F.T)]]

# Trace-form independent oracle: explicitly known distinct real roots; nonreal
# conjugates and multiplicities are included without numerical root finding.
fixtures=[(z*(z-1)*(z+2),[-2,0,1]),((z-1)**2*(z+2),[-2,1]),
          ((z*z+1)*(z-2),[2]),((z*z+1)**2,[]),(z**3,[0]),(S.Integer(2),[])]
queries=[S.Integer(0),S.Integer(1),z,z*z,z-1,z+2,z*z-1,z**3+2*z-4,z**5-3*z+7]
for p,roots in fixtures:
    for h in queries:
        ck(tq(p,h)==sum(S.sign(h.subs(z,r)) for r in roots))
for ss in product((-1,0,1),repeat=2):
    a,b=ss;ck((a*a+a)*(b*b+b)/4==int(a==b==1))
for A,expected in [(S.Matrix([[0,1],[1,0]]),(1,1,0)),
                   (S.Matrix([[0,1,0],[1,0,0],[0,0,0]]),(1,1,1)),
                   (S.diag(2,-3,0),(1,1,1)),(S.zeros(3),(0,0,3))]:
    ck(inertia(A)==expected)

# Route 1: same determinant, different focal signs, with actual rank-seven data.
F0=S.Matrix([[-7,2,16],[5,-4,4],[-20,25,-70]])
G=S.diag(1,2,3);F=F0+z*G;H=S.diag(2,S.Rational(1,2),1);Fhat=H.inv().T*F
p=6*z**3-194*z**2+1854*z
ck(S.expand(F.det())==p);ck(S.expand(Fhat.det())==p)
ck(S.discriminant(6*z*z-194*z+1854,z)<0)
ck(S.degree(S.gcd(p,S.diff(p,z)),z)==0);ck(F0.rank()==2)
ck(values(F0)==[4,25]);ck(values(Fhat.subs(z,0))==[-S.Rational(112,377),-S.Rational(1925,67)])
U=S.Matrix([[S.Rational(2,3),-S.Rational(1,3),S.Rational(2,3)],
 [S.Rational(2,3),S.Rational(2,3),-S.Rational(1,3)],
 [-S.Rational(1,3),S.Rational(2,3),S.Rational(2,3)]])
Tx=S.Matrix([[0,-2,3],[2,0,-1],[-3,1,0]])
ck(U.T*U==S.eye(3));ck(U.det()==1)
ck(F0==30*S.diag(S.Rational(1,5),S.Rational(1,5),1)*Tx*U*S.diag(S.Rational(1,2),S.Rational(1,2),1))
uv=[(-1,0),(-1,1),(-2,0),(-2,1),(-3,-1),(-3,2),(-4,1)]
pairs=[]
for u,v in uv:
    x=S.Matrix([u,v,1]);y=(F0*x).cross(G*x)
    ck(y[2]!=0);ck((y.T*F0*x)[0]==0);ck((y.T*G*x)[0]==0);pairs.append((x,y))
A=design(pairs);Ahat=design([(x,H*y) for x,y in pairs]);ck(A.rank()==7);ck(Ahat.rank()==7)
for a,b in [(A,F0),(A,G),(Ahat,H.inv().T*F0),(Ahat,H.inv().T*G)]:ck(a*S.Matrix(list(b))==S.zeros(7,1))
base=chart_count(F);changed=chart_count(Fhat)
ck(base['positive_in_chart']==1);ck(changed['positive_in_chart']==0)
ck(base['at_least_one_zero_q']==0);ck(changed['at_least_one_zero_q']==0)
ck(essential_residual(F0,4,25)==S.zeros(3))

# Route 2: repeated roots, rank guards, roots at projective infinity, and zeros.
rankone=S.diag(z,z,1);ck(rankone.det()==z*z);ck(tq(rankone.det(),1)==1)
ck(tq(rankone.det(),rank_guard(rankone))==0)
repeat=S.Matrix([[z,1,0],[0,z,1],[0,0,1]])
ck(repeat.det()==z*z);ck(repeat.subs(z,0).rank()==2);ck(tq(repeat.det(),rank_guard(repeat))==1)
rev=G+z*F0;ck(S.degree(rev.det(),z)==2);ck(tq(rev.det(),1)==0)
ck(values(F0)==[4,25]) # the omitted infinity point is positive
ck(chart_count(rev)['positive_in_chart']==0) # affine only, deliberately
ck(base['positive_in_chart']==chart_count(rev)['positive_in_chart']+1)
ck(chart_count(-3*F)['positive_in_chart']==1)

# Route 3: an undefined chart hides a positive continuum at the sole real root.
T=S.Matrix([[0,0,0],[0,0,-1],[0,1,0]]);critical=T+z*G
ck(critical.det()==6*z**3+z);ck(tq(critical.det(),1)==1)
ck(T.rank()==2);ck(nd(T)==(0,0));ck(nd(T.T)==(0,0))
cpairs=[];world=[]
for u,v in uv:
    u=S.Rational(u);v=S.Rational(v);up=-(2*v*v+3)/u
    x=S.Matrix([u,v,1]);y=S.Matrix([up,v,1]);cpairs.append((x,y))
    Z=1/(up-u);X=S.Matrix([u*Z,v*Z,Z]);world.append(X)
    ck(Z>0);ck(X/X[2]==x);Xp=X+S.Matrix([1,0,0]);ck(Xp/Xp[2]==y)
    ck((y.T*T*x)[0]==0);ck((y.T*G*x)[0]==0)
ck(design(cpairs).rank()==7)
critical_count=chart_count(critical)
ck(critical_count['positive_in_chart']==0);ck(critical_count['at_least_one_zero_q']==1)
a,b=S.symbols('a b')
R=essential_residual(T,a,b)
ck(R==S.Matrix([[0,0,0],[0,0,a-b],[0,a-b,0]]))
for focal in (S.Rational(1,3),S.Integer(1),S.Integer(2),S.Integer(11)):
    K=S.diag(focal,focal,1);ck(K*T*K==focal*T)
    ck(essential_residual(T,focal*focal,focal*focal)==S.zeros(3))
try:tq(S.Integer(0),1)
except ValueError:checks+=1
else:raise AssertionError('zero determinant was silently accepted')

# Route 4: radical-free essential feasibility; rank/positivity are not omitted.
D=S.diag(1,2,0);RD=essential_residual(D,a,b)
ck(RD==S.diag(-3*a*b,6*a*b,0))
ck(essential_residual(S.diag(1,0,0),a,b)==S.diag(a*b,0,0))
for M in (F0,Fhat.subs(z,0)):
    a0,b0=values(M);ck(essential_residual(M,a0,b0)==S.zeros(3))

# Route 5: arbitrarily close rank-two matrices lie across a true chart pole.
t=S.symbols('t');M=S.Matrix([[1,2,1],[2,1,2],[t+2,2*t+1,t+2]])
ck(M.det()==0);ck(M[:2,:2].det()==-3)
s1=-(t+2)*(2*t-1)/(4*(t-1)*(t+1));s2=-(t+2)*(2*t+1)/4
ck(S.cancel(values(M)[0]-s1)==0);ck(S.cancel(values(M)[1]-s2)==0)
ck(nd(M)[1].subs(t,-1)==0);ck(nd(M)[0].subs(t,-1)!=0)
ck(nd(M.T)[1].subs(t,-1)!=0);ck(s2.subs(t,-1)==S.Rational(1,4))
for den in (3,5,10,100,1000,1000000):
    eps=S.Rational(1,den);L=M.subs(t,-1-eps);R=M.subs(t,-1+eps)
    l1,l2=values(L);r1,r2=values(R)
    ck(l1>0);ck(l2>0);ck(r1<0);ck(r2>0)
    ck(L.rank()==R.rank()==2);ck(max(abs(v) for v in L-R)==4*eps)
    ck(essential_residual(L,l1,l2)==S.zeros(3));ck(essential_residual(R,r1,r2)==S.zeros(3))

out={'problem_id':20000190,'status':'unsolved','turns_used':5,
     'exact_assertions':checks,'sympy_version':S.__version__,
     'determinant_preserving_control':{'p':str(p),'original_focal_squares':['4','25'],
        'transformed_focal_squares':['-112/377','-1925/67'],'original':base,'transformed':changed},
     'critical_pencil':critical_count,
     'controls':['trace signatures versus explicit real roots, including multiplicities and nonreal roots',
       'zero-sign indicator truth table and exact rational inertia',
       'rank-seven epipolar design and determinant-preserving sign reversal',
       'projective infinity, repeated roots and rank-one rejection',
       'undefined quartic chart with a cheiral positive-camera continuum',
       'polynomial essential constraint and strict positivity controls',
       'six exact pole-approach scales'],
     'not_established':['full primary-question resolution','production runtime advantage',
       'complete critical-fiber classification','noise-certified estimation','cheirality of arbitrary positive candidates'],
     'arithmetic':'exact rationals and symbolic polynomials; no numeric root approximations'}
print(json.dumps(out,indent=2,sort_keys=True))
