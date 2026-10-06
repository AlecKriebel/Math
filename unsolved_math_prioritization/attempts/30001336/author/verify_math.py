#!/usr/bin/env python3
"""Read-only diagnostics for the explicitly scoped rooted-kernel partials.

No network calls, subprocesses, dynamic source imports, or writes.
Assertions deliberately use explicit exceptions so -O has identical semantics.
"""
import json
from collections import Counter
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
import sympy as sp
import mpmath as mp

COUNTS = Counter()

def require(condition, label, family):
    if not condition:
        raise RuntimeError(label)
    COUNTS[family] += 1


def symbolic_checks():
    a,b,x,y,j,k,z=sp.symbols('a b I_a I_b J_a J_b zeta2')
    den=1-a*b
    A=(1-a)/den; B=(1-b)/den; C=(1-a)*(1-b)/den
    g1=A*(y-b)+B*(x-a)
    L1a=(x*x+x)/a-x-1-j
    L1b=(y*y+y)/b-y-1-k
    M1a=(x*x+x)/a-2*x+a-1
    M1b=(y*y+y)/b-2*y+b-1
    N1ab=B*(j+k+z+y-(y*y+y)/b)
    N1a0=j+z-1
    q1=g1-(x-a)
    recurrence=(A*(M1b-L1b-b)+B*(M1a-L1a-a)
                -a*B*(L1b+N1ab-N1a0)+B*q1*x+C*g1)
    g2=(A*B*(j-a+k-b+(x-a)*(y-b)+a*b*(z+1))
        +A*(b*k-b*y)-a*A*B*(y*y-2*b*y+y)
        +B*(a*j-a*x)-b*A*B*(x*x-2*a*x+x))
    eqs=[(recurrence-g2,'exact original recurrence at order 2'),
         (M1a-L1a-(j-x+a),'M-L cancellation'),
         (L1b+N1ab-N1a0-(B-1)*(j+k+z+y-(y*y+y)/b),'N subtraction'),
         (g1-g1.xreplace({a:b,b:a,x:y,y:x,j:k,k:j}),'g1 symmetry'),
         (g2-g2.xreplace({a:b,b:a,x:y,y:x,j:k,k:j}),'g2 symmetry'),
         (g1.subs({a:0,x:0,j:0})-(y-b),'g1 boundary'),
         (g2.subs({a:0,x:0,j:0})-(k-b*y-b+b*b),'g2 boundary'),
         ((g1-(y-b)).subs(b,1),'g1 endpoint cancellation with symbolic logs'),
         ((g2-(k-b*y-b+b*b)).subs(b,1),'g2 endpoint cancellation with symbolic logs')]
    for expr,label in eqs:
        require(sp.cancel(expr)==0,label,'symbolic')
    # Pointwise integrand identity proving the rooted-tree D lemma.
    u,r=sp.symbols('u r')
    kernel=(r/(1-r*u)-a/(1-a*u))/(r-a)
    require(sp.cancel(kernel-1/((1-r*u)*(1-a*u)))==0,'D kernel','symbolic')
    require(sp.cancel(1/(u*(1-a*u))-1/u-a/(1-a*u))==0,'period split','symbolic')
    require(sp.cancel(r/((1-r)*(1-a*r))-(1/(1-a))*(1/(1-r)-1/(1-a*r)))==0,'K H1-word partial fraction','symbolic')
    # The generic-ring endpoint obstruction, not an actual coefficient of G.
    f=a*a+b*b
    require(f.subs({a:0,b:0})==0,'obstruction zero value','symbolic')
    require(sp.diff(f,a).subs({a:0,b:0})==0,'obstruction zero a derivative','symbolic')
    require(sp.diff(f,b).subs({a:0,b:0})==0,'obstruction zero b derivative','symbolic')
    require(sp.cancel(f-f.subs(a,0)-a*a)==0,'obstruction numerator','symbolic')
    require(sp.limit(sp.integrate(a*a/(1-r),(r,0,u)),u,1,dir='-').subs(a,1)==sp.oo,'obstruction divergence','symbolic')
    # Boundary normalization of published coefficients by actual local series.
    I=sum(a**n/sp.Integer(n) for n in range(1,8))
    J=sum(a**n/sp.Integer(n*n) for n in range(1,8))+I*I/2
    h2=J-a*I-a+a*a
    require(sp.expand(h2).coeff(a,0)==0,'h2 value','symbolic')
    require(sp.expand(h2).coeff(a,1)==0,'h2 derivative','symbolic')


def formal_inverse_checks():
    # Different exact rational inputs and independent direct composition sums.
    for nmax in (2,5,11,23):
        h=[Fraction(1)]+[Fraction((-1)**n*(n+2),n+1) for n in range(1,nmax+1)]
        d=[Fraction(1)]
        for n in range(1,nmax+1):
            d.append(-sum(h[j]*d[n-j] for j in range(1,n+1)))
        for n in range(nmax+1):
            require(sum(h[j]*d[n-j] for j in range(n+1))==int(n==0),'inverse convolution','formal')
        g=[Fraction(1)]+[Fraction(n*n+1,n+3) for n in range(1,nmax+1)]
        q=[Fraction(0)]+[sum(g[j]*d[n-j] for j in range(n+1)) for n in range(1,nmax+1)]
        for n in range(nmax+1):
            require(sum(h[j]*q[n-j] for j in range(n+1))==g[n]-h[n],'quotient convolution','formal')


@lru_cache(None)
def shuffle(u,v):
    if not u: return {v:1}
    if not v: return {u:1}
    c=Counter()
    for w,n in shuffle(u[1:],v).items(): c[(u[0],)+w]+=n
    for w,n in shuffle(u,v[1:]).items(): c[(v[0],)+w]+=n
    return dict(c)


def multiply(x,y):
    c=Counter()
    for u,a in x.items():
        for v,b in y.items():
            for w,n in shuffle(u,v).items(): c[w]+=a*b*n
    return {w:n for w,n in c.items() if n}


def graft_symbol(x):
    c=Counter()
    for w,a in x.items():
        z={():a}
        for bit in w:
            nz=Counter()
            for v,b in z.items():
                for q,s in (((0,-1),) if bit==0 else ((0,1),(1,1))): nz[v+(q,)]+=b*s
            z=nz
        for v,b in z.items(): c[v+(1,)]+=b
    return {w:n for w,n in c.items() if n}


def tree_size(t):
    return 1+sum(tree_size(x) for x in t[0])


@lru_cache(None)
def trees(n):
    return tuple((f,) for f in forests(n-1))


@lru_cache(None)
def forests(n):
    if n==0: return ((),)
    ts=[t for k in range(1,n+1) for t in trees(k)]
    sizes={t:tree_size(t) for t in ts}
    ans=[]
    def rec(start,left,cur):
        if left==0:
            ans.append(tuple(cur)); return
        for i in range(start,len(ts)):
            if sizes[ts[i]]<=left: rec(i,left-sizes[ts[i]],cur+[ts[i]])
    rec(0,n,[])
    return tuple(ans)


@lru_cache(None)
def forest_symbol(f):
    z={():1}
    for t in f: z=multiply(z,graft_symbol(forest_symbol(t[0])))
    return z


def modular_rank(rows,cols,prime):
    piv={}
    for row in rows:
        x=[row.get(w,0)%prime for w in cols]
        for i in range(len(cols)):
            if not x[i]: continue
            if i in piv:
                a=x[i]; x=[(b-a*c)%prime for b,c in zip(x,piv[i])]
            else:
                a=pow(x[i],-1,prime); piv[i]=[(a*b)%prime for b in x]; break
    return len(piv)


def symbol_checks():
    prime=1000003
    require(bool(sp.isprime(prime)),'modulus prime','symbols')
    rows=[]
    known_forests=[1,2,4,9,20,48,115,286,719]
    known_trees=[1,1,2,4,9,20,48,115,286]
    for n in range(1,10):
        fs=forests(n)
        require(len(set(fs))==len(fs),'unique forest enumeration','symbols')
        require(all(sum(tree_size(t) for t in f)==n for f in fs),'forest weights','symbols')
        require(len(fs)==known_forests[n-1],'forest inventory','symbols')
        require(len(trees(n))==known_trees[n-1],'tree inventory','symbols')
        cols=sorted({w for f in fs for w in forest_symbol(f)})
        require(len(cols)==2**(n-1),'word inventory','symbols')
        require(all(len(w)==n and w[-1]==1 for w in cols),'word domain','symbols')
        rank=modular_rank([forest_symbol(f) for f in fs],cols,prime)
        require(rank==2**(n-1),'finite leading-word full rank','symbols')
        rows.append({'weight':n,'trees':len(trees(n)),'forests':len(fs),'rank_mod_1000003':rank,'word_dimension':len(cols)})
    # Independent small cases catch order/sign/shuffle multiplicity mutations.
    require(graft_symbol({():1})=={(1,):1},'leaf symbol','symbols')
    require(graft_symbol({(1,):1})=={(0,1):1,(1,1):1},'chain two symbol','symbols')
    require(multiply({(1,):1},{(1,):1})=={(1,1):2},'shuffle multiplicity','symbols')
    require(graft_symbol({(0,1):1})=={(0,0,1):-1,(0,1,1):-1},'zero-letter substitution sign','symbols')
    return rows


def numerical_checks():
    mp.mp.dps=55
    I=lambda a:-mp.log1p(-a)
    J=lambda a:mp.polylog(2,a)+I(a)**2/2
    def g1(a,b):
        return ((1-a)*(I(b)-b)+(1-b)*(I(a)-a))/(1-a*b)
    def integral(f,a=None):
        return mp.quad(f,[0,a,1] if a is not None else [0,mp.mpf('0.5'),1])
    def close(actual,expected,label):
        require(mp.isfinite(actual) and abs(actual-expected)<mp.mpf('1e-32')*(1+abs(expected)),label,'numerical')
    for a,b in [(mp.mpf(1)/5,mp.mpf(1)/3),(mp.mpf(1)/2,mp.mpf(2)/3),(mp.mpf(4)/5,mp.mpf(1)/4)]:
        m=integral(lambda r:a*g1(a,r)/(1-a*r))
        l=integral(lambda r:(g1(a,r)-g1(0,r))/(1-r))
        n=integral(lambda r:(g1(r,b)-g1(a,b))/(r-a) if r!=a else mp.diff(lambda t:g1(t,b),a),a)
        close(m,(I(a)**2+I(a))/a-2*I(a)+a-1,'actual M1 kernel')
        close(l,(I(a)**2+I(a))/a-I(a)-1-J(a),'actual L1 kernel')
        close(n,(1-b)/(1-a*b)*(J(a)+J(b)+mp.zeta(2)+I(b)-(I(b)**2+I(b))/b),'actual N1 kernel')
        close(integral(lambda r:(I(r)-I(a))/(r-a) if r!=a else 1/(1-a),a),J(a)+mp.zeta(2),'D leaf')
        close(integral(lambda r:(J(r)-J(a))/(r-a) if r!=a else I(a)/(a*(1-a)),a),-2*mp.polylog(3,-a/(1-a))+2*mp.zeta(3),'D chain')
        close(integral(lambda r:a*mp.polylog(2,r)/(1-a*r)),mp.zeta(2)*I(a)-mp.polylog(3,a)-mp.quad(lambda t:I(t)**2/(2*t),[0,a]),'K zero-letter word transform')
    for m in range(6):
        close(integral(lambda x:I(x)**(m+1)/x),mp.factorial(m+1)*mp.zeta(m+2),'star period')
    # Cutoff divergence diagnostic has an exact analytic reference.
    a=mp.mpf(2)/3
    for k in (2,5,9):
        cutoff=1-mp.mpf(10)**(-k)
        close(mp.quad(lambda r:a*a/(1-r),[0,cutoff]),a*a*k*mp.log(10),'endpoint obstruction cutoff')


def main():
    symbolic_checks()
    formal_inverse_checks()
    rows=symbol_checks()
    numerical_checks()
    result={'status':'PASS_SCOPED_PARTIAL_DIAGNOSTICS','original_problem':'UNRESOLVED',
            'assertions_by_family':dict(sorted(COUNTS.items())),
            'leading_word_spans':rows,
            'limitations':['No all-order polynomial closure certified.','No nonperturbative existence result established by this checker.','Finite ranks through weight 9 only.','Numerical quadratures are diagnostics, not proofs.']}
    expected_path=Path(__file__).resolve().with_name('expected_results.json')
    if json.loads(expected_path.read_text())!=result:
        raise RuntimeError('Output differs from frozen expected_results.json')
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
