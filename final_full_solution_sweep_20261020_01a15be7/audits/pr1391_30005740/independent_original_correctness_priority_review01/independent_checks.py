"""Own exact algebra controls; never imports or executes the claimant's programs."""
import json
from collections import defaultdict
from math import comb
import sympy as s
x=s.symbols('x')
def need(ok,message):
    if not ok: raise RuntimeError(message)
def zero(a):return s.cancel(a)==0

def bar_boundary(h,reverse_correction=False):
    """Basis tuple (left PBW monomial, normalized middle, right PBW monomial)."""
    z=(0,0);X=(1,0);Y=(0,1);out=defaultdict(lambda:s.S.Zero)
    def add(l,m,r,v):
        if m!=z:out[(l,m,r)]+=v
    add(Y,X,z,1);add(z,Y,X,1);add(X,Y,z,-1);add(z,X,Y,-1)
    # -[Yx]+[xY]=-[h]; normalized constants disappear.
    for (n,),c in s.Poly(h,x).terms():add(z,(n,0),z,-c)
    sign=1 if reverse_correction else -1
    for (n,),c in s.Poly(h,x).terms():
        for i in range(1,n):
            add((i,0),X,(n-1-i,0),sign*c)
            add(z,(i+1,0),(n-1-i,0),-sign*c)
            add(z,(i,0),(n-i,0),sign*c)
    expected=defaultdict(lambda:s.S.Zero)
    for k,v in [((Y,X,z),1),((z,Y,X),1),((X,Y,z),-1),((z,X,Y),-1)]:expected[k]+=v
    for (n,),c in s.Poly(h,x).terms():
        for i in range(n):expected[((i,0),X,(n-1-i,0))]-=c
    return {k:s.expand(v) for k,v in out.items() if v}!={k:s.expand(v) for k,v in expected.items() if v}

def main():
    factors=[x,x-1,x+2,x*x+1,x*x+x+1]
    # Each nonlinear factor is irreducible over Q; no field extension is used.
    cases=[]
    for u in factors:
        for e in range(2,5):
            for lead in [s.Rational(1),s.Rational(-7,3)]:cases.append((s.expand(lead*u**e*(x-3)),u))
    cases += [(s.expand(5*(x*x+1)**3*(x-1)**2*(x+2)),x*x+1),(s.expand(5*(x*x+1)**3*(x-1)**2*(x+2)),x-1)]
    bar_cases=[s.Integer(7),x+3,x*x+2*x+7,x**5-3*x**3+2*x+5]+[h for h,u in cases]
    for h in bar_cases:need(not bar_boundary(h),'bar comparison boundary')
    reciprocal_checks=0
    rows=[]
    for h,u in cases:
        d=s.Poly(s.gcd(h,s.diff(h,x)),x).monic().as_expr(); pi=s.cancel(h/d);g=s.cancel(d/u)
        L=s.cancel(pi*s.diff(d,x)/d);q=s.expand(s.cancel(L*g-pi*s.diff(g,x)))
        need(s.Poly(L,x).is_univariate and s.Poly(q,x).is_univariate,'polynomial existence')
        need(zero(L*h+h*s.diff(pi,x)-s.diff(h,x)*pi),'actual derivation relation')
        need(s.rem(s.expand(g*pi),d,x)==0,'cup-zero mod d')
        need(zero(q-h*s.diff(u,x)/u**2),'commutator identity')
        need(q!=0 and s.degree(q,x)<s.degree(h,x) and s.rem(q,h,x)!=0,'noninner bracket')
        need(s.degree(d,x)<s.degree(h,x) and s.degree(g,x)<s.degree(d,x),'independent central pair')
        P=s.Integer(1)
        for j in range(6):
            # Reciprocal recurrence supplies all orders in the written centrality proof.
            need(zero(s.diff(1/pi,x,j)-P/pi**(j+1)),'reciprocal derivative identity')
            need(zero(pi*h**j*s.diff(1/pi,x,j)-d**j*P),'normalizer coefficient in A')
            P=s.expand(pi*s.diff(P,x)-(j+1)*s.diff(pi,x)*P);reciprocal_checks+=1
        rows.append({'h':str(h),'u':str(u),'d':str(d),'q':str(q)})
    # Direct finite linear coefficient consequence of c cup z=[c,z]=0.
    # c=e0, independent z=e1: lambda(c)e1-lambda(z)e0=0 forces both coefficients0.
    matrix=s.Matrix([[0,-1],[1,0]])
    need(matrix.rank()==2,'central-annihilator coefficient injectivity')
    # Decisive corruptions: each is rejected by the relevant exact mathematical condition.
    need(bar_boundary(x*x+2*x+7,True),'wrong correction-sign mutant detected')
    h=(x*x+1)**2;u=x*x+1;d=u;pi=u;g=1;L=2*x
    need(not zero(-L*h+h*s.diff(pi,x)-s.diff(h,x)*pi),'wrong b(Y) sign detected')
    need(not zero(L*g-pi*s.diff(g,x)-h/u**2),'omitted u-prime mutant detected')
    # The misleading ambient ad(pi*y) has an additional term for Y=yh.
    h=x**3;d=x*x;pi=x;L=2
    extra=s.expand(pi*s.diff(h,x,2)-L*s.diff(h,x))
    need(extra==0,'x3 extra cancellation control')
    h=(x*x+1)**2;d=x*x+1;pi=x*x+1;L=2*x
    extra=s.expand(pi*s.diff(h,x,2)-L*s.diff(h,x))
    need(extra!=0,'ambient identification mutant detected on nonsplit factor')
    return {'status':'PASS','author_programs_executed':False,'exact_factor_cases':len(cases),'bar_comparison_cases':len(bar_cases),'normalizer_reciprocal_checks':reciprocal_checks,'central_linear_rank':matrix.rank(),'mathematical_mutants_rejected':4,'ambient_extra_term_nonsplit':str(extra),'factor_cases':rows,'scope':'Finite diagnostics supplement the all-order written proof; no finite check certifies all fields.'}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
