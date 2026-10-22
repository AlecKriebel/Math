#!/usr/bin/env python3
"""Independent exact controls; standard library, no candidate code imported.
Squarefree-radicand dictionary arithmetic and exact complex conjugation.
Finite controls supplement, not replace, the all-real-time proof.
"""
from fractions import Fraction
from math import gcd, isqrt
import json

class R:
    def __init__(self, x=0):
        self.d = dict(x.d) if isinstance(x,R) else ({1:Fraction(x)} if x else {})
    @classmethod
    def terms(cls,d):
        z=cls(); z.d={k:v for k,v in d.items() if v}; return z
    def __add__(x,y):
        y=R(y); z=dict(x.d)
        for k,v in y.d.items():z[k]=z.get(k,Fraction(0))+v
        return R.terms(z)
    __radd__=__add__
    def __neg__(x):return R.terms({k:-v for k,v in x.d.items()})
    def __sub__(x,y):return x+-R(y)
    def __rsub__(x,y):return R(y)+-x
    def __mul__(x,y):
        y=R(y);z={}
        for a,c in x.d.items():
            for b,d in y.d.items():
                g=gcd(a,b); k=a*b//(g*g)
                z[k]=z.get(k,Fraction(0))+c*d*g
        return R.terms(z)
    __rmul__=__mul__
    def __truediv__(x,y):return R.terms({k:v/Fraction(y) for k,v in x.d.items()})
    def __eq__(x,y):return x.d==R(y).d
    def __repr__(x):return repr({k:str(v) for k,v in x.d.items()})

def root(q):
    q=Fraction(q);assert q>=0
    if not q:return R()
    n=q.numerator*q.denominator; outside=1;inside=1;p=2
    while p*p<=n:
        power=0
        while n%p==0:n//=p;power+=1
        outside*=p**(power//2)
        if power%2:inside*=p
        p+=1
    inside*=n
    return R.terms({inside:Fraction(outside,q.denominator)})

class C:
    def __init__(self,x=0,y=0):
        if isinstance(x,C):self.x,self.y=x.x,x.y
        else:self.x,self.y=R(x),R(y)
    def __add__(a,b):b=C(b);return C(a.x+b.x,a.y+b.y)
    __radd__=__add__
    def __neg__(a):return C(-a.x,-a.y)
    def __sub__(a,b):return a+-C(b)
    def __rsub__(a,b):return C(b)+-a
    def __mul__(a,b):b=C(b);return C(a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x)
    __rmul__=__mul__
    def __truediv__(a,q):return C(a.x/q,a.y/q)
    def star(a):return C(a.x,-a.y)
    def __eq__(a,b):b=C(b);return a.x==b.x and a.y==b.y

def matrix(rows):return tuple(tuple(C(v) for v in row) for row in rows)
def zero(n=2):return matrix([[0]*n for _ in range(n)])
def unit(n=2):return matrix([[int(i==j) for j in range(n)] for i in range(n)])
def add(a,b):return tuple(tuple(x+y for x,y in zip(r,s)) for r,s in zip(a,b))
def neg(a):return tuple(tuple(-x for x in r) for r in a)
def sub(a,b):return add(a,neg(b))
def scale(q,a):return tuple(tuple(C(q)*x for x in r) for r in a)
def mul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))) for i in range(len(a)))
def adj(a):return tuple(tuple(a[j][i].star() for j in range(len(a))) for i in range(len(a[0])))
def conjugate(u,a):return mul(mul(u,a),adj(u))
def delta(a):return matrix([[a[0][0],0],[0,a[1][1]]])
def inner(a,b):return delta(mul(adj(a),b))
def rot(r):
    c=root((1+r)/2);s=root((1-r)/2)
    return matrix([[c,-s],[s,c]])
I=unit();Z=zero();q=matrix([[1,0],[0,0]]);q2=sub(I,q)
basis=[matrix([[int(i==r and j==c) for j in range(2)] for i in range(2)]) for r in range(2) for c in range(2)]
checks=[]
def check(name,condition):
    if not condition:raise AssertionError(name)
    checks.append(name)

for value in [Fraction(0),Fraction(1,2),Fraction(3,4),Fraction(5,8),Fraction(7,9),Fraction(17,32),Fraction(5),Fraction(15)]:
    check('sqrt_square_'+str(value),root(value)*root(value)==value)
check('complex_i_square',C(0,1)*C(0,1)==-1)
check('complex_i_adjoint',C(0,1).star()==C(0,-1))

# Recompute witnesses for multiple exact times r=exp(-s), plus boundary controls.
for r in [Fraction(1),Fraction(3,4),Fraction(1,2),Fraction(1,3),Fraction(1,7),Fraction(0)]:
    v=rot(r);w=rot(r*r);u=mul(adj(v),w)
    for label,m in [('v',v),('w',w),('u',u)]:
        check(f'{r}_{label}_left_unitary',mul(adj(m),m)==I)
        check(f'{r}_{label}_right_unitary',mul(m,adj(m))==I)
    check(f'{r}_cocycle',mul(v,u)==w)
    Q=conjugate(v,q);Qs=conjugate(u,q)
    a0=sub(mul(mul(q,Q),q),scale((1+r)/2,q))
    at=sub(mul(mul(q,Qs),q),scale((1+r)/2,q))
    d=(root(1+r*r)-r)*(1-r*r)/2
    check(f'{r}_kernel_witness',a0==Z)
    check(f'{r}_coefficient',at==scale(d,q))
    translated=conjugate(v,at)
    check(f'{r}_translated_witness',translated==scale(d,Q))
    check(f'{r}_translated_square',mul(adj(translated),translated)==scale(d*d,Q))
    check(f'{r}_compressed_witness',delta(translated)==scale(d,matrix([[(1+r)/2,0],[0,(1-r)/2]])))
    check(f'{r}_nonzero_or_boundary',translated==Z if r==1 else translated!=Z)
    if r==Fraction(1,2):
        check('claimed_radical_coefficient',d==(root(5)-1)*Fraction(3,16))
        check('claimed_Q',Q==matrix([[Fraction(3,4),root(3)/4],[root(3)/4,Fraction(1,4)]]))
        check('e12_generation',scale(root(3)*Fraction(4,3),mul(mul(q,Q),q2))==basis[1])

# Full complex GNS/right-module/expectation controls.
for n,a in enumerate(basis+[matrix([[C(1,2),C(-3,4)],[C(5,-6),C(-7,-8)]])]):
    check(f'delta_kraus_{n}',delta(a)==add(mul(mul(q,a),q),mul(mul(q2,a),q2)))
    check(f'delta_idempotent_{n}',delta(delta(a))==delta(a))
    for j,b in enumerate([q,q2,matrix([[C(2,3),0],[0,C(5,-7)]])]):
        check(f'expectation_right_module_{n}_{j}',delta(mul(a,b))==mul(delta(a),b))
        check(f'expectation_left_module_{n}_{j}',delta(mul(b,a))==mul(b,delta(a)))
    for j,b in enumerate(basis):
        check(f'inner_symmetry_{n}_{j}',inner(a,b)==adj(inner(b,a)))
        for k,h in enumerate(basis):
            check(f'left_action_adjoint_{n}_{j}_{k}',inner(mul(a,b),h)==inner(b,mul(adj(a),h)))

# Conditional expectation at matrix level 2: explicit Kraus decomposition.
B=matrix([[C(1,2),C(3,-1),4,5],[6,C(-2,1),7,8],[9,10,C(3,5),11],[12,13,14,C(2,-4)]])
positive=mul(adj(B),B)
D0=matrix([[int(i==j and i%2==0) for j in range(4)] for i in range(4)])
D1=sub(unit(4),D0)
def amplified_delta(a):return matrix([[a[i][j] if i%2==j%2 else 0 for j in range(4)] for i in range(4)])
check('matrix_level2_kraus',amplified_delta(positive)==add(conjugate(D0,positive),conjugate(D1,positive)))
check('matrix_level2_gram',amplified_delta(positive)==add(mul(adj(mul(B,D0)),mul(B,D0)),mul(adj(mul(B,D1)),mul(B,D1))))

# Symbolic-coefficient semigroup proof reduced to complementary projections.
J=matrix([[Fraction(1,2),Fraction(1,2)],[Fraction(1,2),Fraction(1,2)]])
H=sub(I,J)
for name,condition in [('J_squared',mul(J,J)==J),('H_squared',mul(H,H)==H),('JH',mul(J,H)==Z),('HJ',mul(H,J)==Z)]:check(name,condition)
print(json.dumps({'result':'PASS','independent_assertions':len(checks),'arithmetic':'exact rational squarefree-radicand dictionaries with exact complex conjugation','candidate_code_imported':False,'checks':checks,'limits':['Finite controls do not establish continuity, algebraic generation, or all-real-time properties; those are reviewed in AUDIT.md.','r=0 is a limiting algebra control, not a finite time.']},indent=2))
