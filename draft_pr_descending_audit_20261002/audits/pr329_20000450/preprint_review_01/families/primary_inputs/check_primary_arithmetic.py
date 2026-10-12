#!/usr/bin/env python3
"""Independent exact checks; Python standard library only, no candidate scripts."""
from fractions import Fraction as F
from dataclasses import dataclass
import json

@dataclass(frozen=True)
class Q5:
    a: F = F(0)
    b: F = F(0)
    def __post_init__(self):
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))
    def __add__(self, y):
        y=cast(y); return Q5(self.a+y.a,self.b+y.b)
    __radd__=__add__
    def __neg__(self): return Q5(-self.a,-self.b)
    def __sub__(self,y): return self+-cast(y)
    def __rsub__(self,y): return cast(y)+-self
    def __mul__(self,y):
        y=cast(y); return Q5(self.a*y.a+5*self.b*y.b,self.a*y.b+self.b*y.a)
    __rmul__=__mul__
    def __truediv__(self,y):
        y=cast(y); norm=y.a*y.a-5*y.b*y.b
        if not norm: raise ZeroDivisionError
        return self*Q5(y.a/norm,-y.b/norm)
    def __pow__(self,n):
        if n<0: return (Q5(1)/self)**(-n)
        out=Q5(1)
        for _ in range(n): out=out*self
        return out
    def show(self): return f"({self.a})+({self.b})r"

def cast(x): return x if isinstance(x,Q5) else Q5(x)
Z=Q5()
def trim(p):
    p=list(map(cast,p))
    while len(p)>1 and p[-1]==Z: p.pop()
    return p
def add(p,q):
    return trim([(p[i] if i<len(p) else Z)+(q[i] if i<len(q) else Z)
                 for i in range(max(len(p),len(q)))])
def neg(p): return [-x for x in p]
def sub(p,q): return add(p,neg(q))
def mul(p,q):
    out=[Z]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): out[i+j]=out[i+j]+cast(x)*cast(y)
    return trim(out)
def scale(p,c): return trim([cast(c)*x for x in p])
def powp(p,n):
    out=[Q5(1)]
    for _ in range(n): out=mul(out,p)
    return out
def diff(p): return trim([i*p[i] for i in range(1,len(p))] or [Z])
def divrem(p,q):
    p=trim(p); q=trim(q)
    if q==[Z]: raise ZeroDivisionError
    quot=[Z]*max(1,len(p)-len(q)+1)
    while p!=[Z] and len(p)>=len(q):
        n=len(p)-len(q); v=p[-1]/q[-1]; quot[n]=v
        p=sub(p,[Z]*n+scale(q,v))
    return trim(quot),p
def gcd(p,q):
    while trim(q)!=[Z]: p,q=q,divrem(p,q)[1]
    return scale(p,Q5(1)/p[-1])
def check(name,p):
    assert trim(p)==[Z], (name,[x.show() for x in trim(p)])
    checks.append(name)

checks=[]
r=Q5(0,1); phi=(1+r)/2; c=phi**5; h=(11-5*r)/2
assert c==Q5(F(11,2),F(5,2))
assert c*h==Q5(-1)
assert 8+5*(phi-1)==c
assert 3-5*(phi-1)==-Q5(1)/c
checks.append("Verdure alpha_5=c, beta_5=-1/c and h=-1/c")

# Fisher identity: N/D = iota(epsilon(tau)^5), N=tau*f, D=g.
N=list(map(cast,[0,1,2,4,3,1])); D=list(map(cast,[1,-3,4,-2,1]))
assert gcd(N,D)==[Q5(1)]
checks.append("Fisher numerator and denominator are coprime; map degree five")
A=[Q5(1),phi]; B=[-phi,Q5(1)]
top=add(scale(powp(A,5),c),powp(B,5))
bot=sub(powp(A,5),scale(powp(B,5),c))
check("Fisher parameter identity by homogeneous degree-nine cross product",sub(mul(N,bot),mul(D,top)))
# Involution matrices square to a scalar, hence work on all of P^1.
assert phi*phi+1!=Z and c*c+1!=Z
checks.append("epsilon and iota have nonzero determinant and square to scalar")
# Branch computation: no critical point away from the two irrational cusps.
check("Fisher derivative numerator=(tau^2-tau-1)^4",
      sub(sub(mul(diff(N),D),mul(N,diff(D))),powp([-Q5(1),-Q5(1),Q5(1)],4)))

# beta=h*lambda/(lambda+5r). Cross-multiply every rational function.
bn=[Z,h]; bd=[5*r,Q5(1)]
itop=add(scale(bn,c),bd); ibot=sub(bn,scale(bd,c))
check("iota(beta)=-1/(lambda+c)",add(mul(itop,[c,Q5(1)]),ibot))
vnum=sub(bn,scale(bd,c)); vden=add(bn,scale(bd,Q5(1)/c))
check("Verdure criterion ratio=-c*(lambda+c)",add(vnum,scale(mul(vden,[c,Q5(1)]),c)))
check("Morton ratio=c*(lambda+c)",sub(neg(vnum),scale(mul(vden,[c,Q5(1)]),c)))
assert (-phi)**5==-c
checks.append("(-phi*theta)^5=-c*a and (phi*theta)^5=c*a")
# Images of all four excluded source-base points.
assert bn[0]==Z
assert h*(-c)/(5*r-c)==c
assert h==-Q5(1)/c
checks.append("lambda 0,-5r,-c,infinity maps to beta 0,infinity,c,-1/c")

# Each line transcribed independently from Morton v4 p5 (same table v1 p3).
# Coefficients here are polynomials in b, in increasing order of b.
morton={10:[5],9:[5,25,5],8:[1,38,44,7,1],7:[0,9,127,26,3,-1],
        6:[0,0,36,248,19,-3,1],5:[0,0,0,84,322,71,3,-1],
        4:[0,0,0,0,126,293,94,12,1],3:[0,0,0,0,0,125,180,50,5],
        2:[0,0,0,0,0,0,80,65,10],1:[0,0,0,0,0,0,0,30,10],
        0:[0,0,0,0,0,0,0,0,5]}
candidate={10:[5],9:[5,-25,5],8:[1,-38,44,-7,1],7:[0,-9,127,-26,3,1],
           6:[0,0,36,-248,19,3,1],5:[0,0,0,-84,322,-71,3,1],
           4:[0,0,0,0,126,-293,94,-12,1],3:[0,0,0,0,0,-125,180,-50,5],
           2:[0,0,0,0,0,0,80,-65,10],1:[0,0,0,0,0,0,0,-30,10],
           0:[0,0,0,0,0,0,0,0,5]}
for j in range(11):
    assert [a*(-1)**i for i,a in enumerate(morton[j])]==candidate[j],j
checks.append("all eleven residual-table coefficients equal Morton under b=-beta")

print(json.dumps({"passed":len(checks),"checks":checks,"c":c.show(),"h":h.show()},indent=2))
