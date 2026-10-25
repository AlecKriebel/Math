"""Independent finite algebra and marking controls; not an asymptotic certificate."""
import json, math
from fractions import Fraction as F
import sympy as sp
import mpmath as mp

def counts(n,j=1):
    if j>n:
        yield ()
    elif j==n:
        for c in range(n//j+1):
            if n-j*c==0: yield (c,)
    else:
        for c in range(n//j+1):
            rem=n-j*c
            if rem==0: yield (c,)+(0,)*(n-j)
            else:
                for tail in parts(rem,j+1,n): yield (c,)+tail

def parts(rem,j,n):
    if j>n:
        if rem==0: yield ()
    else:
        for c in range(rem//j+1):
            for tail in parts(rem-j*c,j+1,n): yield (c,)+tail

def falling(c,r):
    return math.prod(range(c-r+1,c+1)) if c>=r else 0

N=9
# zeta(2j)/pi^(2j) is rational; the common pi^(2n) cancels after conditioning.
a=[F(0)]+[F(sp.Rational((-1)**(j+1)*sp.bernoulli(2*j)*2**(2*j-1),math.factorial(2*j)*2*j)) for j in range(1,N+1)]
h=[F(1)]
for n in range(1,N+1): h.append(sum(j*a[j]*h[n-j] for j in range(1,n+1))/n)
assert a[1]==F(1,12) and a[2]==F(1,360)
checks=0; records=[]
for n in range(1,N+1):
    rows=[]
    for cs in parts(n,1,n):
        w=math.prod(a[j]**cs[j-1]/math.factorial(cs[j-1]) for j in range(1,n+1))
        rows.append((cs,w))
    assert sum(w for cs,w in rows)==h[n]; checks+=1
    for j in range(1,n+1):
        for r in [1,2,3]:
            got=sum(w*falling(cs[j-1],r) for cs,w in rows)/h[n]
            want=a[j]**r*h[n-j*r]/h[n] if j*r<=n else 0
            assert got==want; checks+=1
    if n>=3:
        got=sum(w*cs[0]*cs[1] for cs,w in rows)/h[n]
        want=a[1]*a[2]*h[n-3]/h[n]
        assert got==want; checks+=1
    records.append({'n':n,'partitions':len(rows),'rational_h_without_pi':str(h[n])})
g,k=sp.symbols('g k',integer=True,positive=True)
A=lambda kk:sp.factorial(6*g-5-2*kk)*2**(3*kk-3)/(sp.factorial(g-kk)*sp.factorial(3*g-3-kk)*3**(g-kk))
ratio=sp.factor(sp.simplify((A(k+1)/2**(k+1))/(A(k)/2**k)))
assert sp.simplify(ratio-12*(g-k)*(3*g-3-k)/((6*g-5-2*k)*(6*g-6-2*k)))==0
checks+=1
# Gamma marks have shape 2j and total shape2n. Dirichlet monomial density needs exponent2j−1.
for js in [(1,1),(1,2),(2,3),(1,1,2),(1,2,4)]:
    n=sum(js); exps=[2*j-1 for j in js]
    integral=F(math.prod(math.factorial(e) for e in exps),math.factorial(sum(exps)+len(exps)-1))
    normalization=F(math.factorial(2*n-1),math.prod(math.factorial(2*j-1) for j in js))
    assert integral*normalization==1
    assert sum(F(2*j,2*n) for j in js)==1
    checks+=2
mp.mp.dps=65
limit=mp.log(2)/2
marks=[]
for q in [1,2,4,8,16,32]:
    cutoff=4*q+120
    value=mp.fsum(mp.zeta(2*j)/(2*j)*mp.gammainc(2*j,2*q,4*q,regularized=True) for j in range(1,cutoff+1))
    marks.append({'q':q,'sum_j_to':cutoff,'gamma_marked_infinite_assembly_window_mean':mp.nstr(value,40),'difference_from_intermediate_lambda':mp.nstr(value-limit,30)})
assert abs(mp.mpf(marks[0]['gamma_marked_infinite_assembly_window_mean'])-limit)>mp.mpf('.01')
# Independent negative controls: primitive-only and all-heights microscopic marks differ;
# macroscopic window[.6,.9] count is at most1, so cannot converge to positive-mean Poisson.
primitive_q1=mp.fsum(mp.mpf(1)/(2*j)*mp.gammainc(2*j,2,4,regularized=True) for j in range(1,125))
assert abs(mp.mpf(marks[0]['gamma_marked_infinite_assembly_window_mean'])-primitive_q1)>mp.mpf('.01')
eta=mp.mpf(3)/5*mp.log(mp.mpf(11)/10)-mp.mpf(1)/20
assert eta>mp.mpf(1)/220 and mp.mpf(3)/5*mp.log(2)<1
out={'status':'finite_controls_passed','exact_checks':checks,'partition_records':records,'prefactor_ratio':str(ratio),'eta':mp.nstr(eta,40),'marked_window_controls':marks,'lambda':mp.nstr(limit,40),'negative_controls':{'primitive_q1_mean':mp.nstr(primitive_q1,40),'microscopic_not_intermediate':True,'macro_count_at_most_one':[.6,.9],'normalization_total_parameter':'2n=6g−6, not4g−4'},'limits':'Finite exact controls and numerical diagnostics only; no geometric, asymptotic, novelty or published-input certificate.'}
print(json.dumps(out,indent=2))
