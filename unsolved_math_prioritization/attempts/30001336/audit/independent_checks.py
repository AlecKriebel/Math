#!/usr/bin/env python3
"""Independent read-only finite checks. No author imports, network, or writes.

Run with python -I -B, optionally -O. Exact and numerical counts are separate.
"""
import itertools
import json
from collections import defaultdict, Counter
from functools import lru_cache
from fractions import Fraction
import sympy as s
import mpmath as m

COUNTS = Counter()

def need(ok, label, kind='exact'):
    if not ok:
        raise RuntimeError(label)
    COUNTS[kind] += 1

@lru_cache(None)
def interleavings(left, right):
    """Choose positions instead of using the author's recursive shuffle rule."""
    out=defaultdict(int)
    for selected in itertools.combinations(range(len(left)+len(right)), len(left)):
        occupied=set(selected); a=iter(left); b=iter(right)
        word=''.join(next(a) if i in occupied else next(b) for i in range(len(left)+len(right)))
        out[word]+=1
    return dict(out)

def product(p,q):
    out=defaultdict(int)
    for x,c in p.items():
        for y,d in q.items():
            for w,e in interleavings(x,y).items(): out[w]+=c*d*e
    return {w:c for w,c in out.items() if c}

def root(p):
    """Direct matrix coefficients: an input 0 forces output 0 and contributes -1."""
    out=defaultdict(int)
    for word,c in p.items():
        allowed=[['0'] if v=='0' else ['0','1'] for v in word]
        sign=(-1)**word.count('0')
        for target in itertools.product(*allowed): out[''.join(target)+'1']+=sign*c
    return {w:c for w,c in out.items() if c}

def forest_data(max_weight):
    # Canonical bracket strings are separate from the author's nested tuple trees.
    by_weight={0:[()]}; tree_weight={}; tree_symbols={}; symbols={():{'':1}}
    for weight in range(1,max_weight+1):
        for children in by_weight[weight-1]:
            tree='['+''.join(children)+']'
            tree_weight[tree]=weight
            tree_symbols[tree]=root(symbols[children])
        available=sorted(tree_weight)
        bag={()}
        # Iterative multiset enumeration, filtered by total weight.
        frontier=[()]; found=[]
        while frontier:
            forest=frontier.pop(); total=sum(tree_weight[t] for t in forest)
            if total==weight: found.append(forest); continue
            for tree in available:
                if (not forest or tree>=forest[-1]) and total+tree_weight[tree]<=weight:
                    next_forest=forest+(tree,)
                    if next_forest not in bag: bag.add(next_forest); frontier.append(next_forest)
        by_weight[weight]=sorted(found)
        for forest in by_weight[weight]:
            p={'':1}
            for tree in forest: p=product(p,tree_symbols[tree])
            symbols[forest]=p
    return by_weight,tree_weight,symbols

def rank_mod(rows,columns,p):
    # Column-oriented elimination on the transpose, rather than streaming rows.
    matrix=[[row.get(word,0)%p for row in rows] for word in columns]
    row=0
    for col in range(len(rows)):
        pivot=next((i for i in range(row,len(matrix)) if matrix[i][col]),None)
        if pivot is None: continue
        matrix[row],matrix[pivot]=matrix[pivot],matrix[row]
        inv=pow(matrix[row][col],-1,p)
        matrix[row]=[(x*inv)%p for x in matrix[row]]
        for k in range(row+1,len(matrix)):
            factor=matrix[k][col]
            if factor: matrix[k]=[(x-factor*y)%p for x,y in zip(matrix[k],matrix[row])]
        row+=1
        if row==len(matrix): break
    return row

def finite_span_checks():
    by_weight,tree_weight,symbols=forest_data(9)
    output=[]; primes=(1000033,1000037)
    for p in primes: need(bool(s.isprime(p)), 'independent modulus primality')
    for n in range(1,10):
        fs=by_weight[n]; cols=[''.join(t)+'1' for t in itertools.product('01',repeat=n-1)]
        need(len(fs)==[1,2,4,9,20,48,115,286,719][n-1],'forest count')
        need(sum(v==n for v in tree_weight.values())==[1,1,2,4,9,20,48,115,286][n-1],'tree count')
        need(all(set(symbols[f])<=set(cols) for f in fs),'word orientation')
        ranks={str(p):rank_mod([symbols[f] for f in fs],cols,p) for p in primes}
        for rank in ranks.values(): need(rank==2**(n-1),'independent finite rank')
        output.append({'weight':n,'forests':len(fs),'dimension':len(cols),'ranks':ranks})
    need(interleavings('01','1')=={'011':2,'101':1},'shuffle multiplicities and orientation')
    need(root({'001':1})=={'0001':1,'0011':1},'two zero letters')
    need(root({'101':1})=={'0001':-1,'0011':-1,'1001':-1,'1011':-1},'interior zero letter')
    return output

def recurrence_checks():
    # Arbitrary rational coefficient arrays: independently expand the complete
    # formal source expression with SymPy, then compare each extracted coefficient.
    t=s.Symbol('t'); nmax=8; a=s.Rational(2,7); b=s.Rational(3,8)
    A=(1-a)/(1-a*b); B=(1-b)/(1-a*b); C=(1-a)*(1-b)/(1-a*b)
    seq=lambda offset:[s.Rational((-1)**(n+offset)*(n*n+offset+1),n+offset+2) for n in range(nmax+1)]
    g=[s.Integer(1)]+seq(1)[1:]; h=[s.Integer(1)]+seq(2)[1:]
    ma,mb,la,lb,nab,na0,y=[seq(k) for k in range(3,10)]
    poly=lambda x:sum(c*t**n for n,c in enumerate(x))
    quotient=s.series(poly(g)/poly(h)-1,t,0,nmax+1).removeO().expand()
    full=(A*(poly(mb)-poly(lb)-b*poly(y))+B*(poly(ma)-poly(la)-a*poly(y))
          +B*quotient*(poly(ma)-poly(la)+a*poly(na0))
          -a*B*(poly(lb)+poly(nab)-poly(na0))+C*(poly(g)-1)*poly(y)).expand()
    inverse=[s.Integer(1)]
    for n in range(1,nmax+1): inverse.append(-sum(h[j]*inverse[n-j] for j in range(1,n+1)))
    q=[0]+[sum(g[j]*inverse[n-j] for j in range(n+1)) for n in range(1,nmax+1)]
    for n in range(nmax+1):
        F=A*(mb[n]-lb[n]-b*y[n])+B*(ma[n]-la[n]-a*y[n])-a*B*(lb[n]+nab[n]-na0[n])
        rhs=F+B*sum(q[k]*(ma[n-k]-la[n-k]+a*na0[n-k]) for k in range(1,n+1))+C*sum(g[k]*y[n-k] for k in range(1,n+1))
        need(s.cancel(rhs-full.coeff(t,n))==0,'full formal coefficient extraction')
    # Integrand identities, including the real 0/1 operator orientation.
    a,r,u=s.symbols('a r u')
    need(s.cancel((r/(1-r*u)-a/(1-a*u))/(r-a)-1/((1-r*u)*(1-a*u)))==0,'resolvent divided difference')
    need(s.cancel(1/(u*(1-a*u))-1/u-a/(1-a*u))==0,'period decomposition')
    R=s.Symbol('R')
    need(s.cancel(R/(1-a*R)-1/(1-a)+(1-R)/((1-a*R)*(1-a)))==0,'exact H1 cutoff cancellation')


def numerical_checks():
    m.mp.dps=70
    I=lambda a:-m.log1p(-a)
    J=lambda a:m.polylog(2,a)+I(a)**2/2
    H011=lambda a:m.zeta(3)+m.log1p(-a)**2*m.log(a)/2+m.log1p(-a)*m.polylog(2,1-a)-m.polylog(3,1-a)
    H101=lambda a:I(a)*m.polylog(2,a)-2*H011(a)
    K=lambda f,a:m.quad(lambda r:a*f(r)/(1-a*r),[0,m.mpf('.4'),m.mpf('.9'),1])
    def eq(v,w,label): need(m.isfinite(v) and abs(v-w)<m.mpf('1e-45')*(1+abs(w)),label,'numerical')
    def g(a,b): return ((1-a)*(I(b)-b)+(1-b)*(I(a)-a))/(1-a*b)
    for a,b in [(m.mpf('.07'),m.mpf('.91')),(m.mpf('.93'),m.mpf('.87')),(m.mpf('.41'),m.mpf('.41'))]:
        eq(K(lambda r:g(a,r),a),(I(a)**2+I(a))/a-2*I(a)+a-1,'M1 actual kernel')
        eq(m.quad(lambda r:(I(a)-a-a*(I(r)-r))/(1-a*r),[0,.4,.9,1]),(I(a)**2+I(a))/a-I(a)-1-J(a),'L1 cancelled actual kernel')
        eq(m.quad(lambda r:(g(r,b)-g(a,b))/(r-a) if r!=a else m.diff(lambda q:g(q,b),a),[0,a,1]),(1-b)/(1-a*b)*(J(a)+J(b)+m.zeta(2)+I(b)-(I(b)**2+I(b))/b),'N1 actual kernel including diagonal')
        eq(K(lambda r:m.polylog(2,r),a),m.zeta(2)*I(a)-m.polylog(3,a)-H011(a),'K H01 orientation')
        eq(K(lambda r:H101(r),a),m.quad(lambda v:(m.zeta(2)*I(v)-m.polylog(3,v)-H011(v))/(v*(1-v)),[0,a]),'K H101 orientation')
        eq(m.diff(lambda v:K(lambda r:I(r)**2/2,v),a),J(a)/(a*(1-a)),'K H11 derivative')
    for power in (1,2,3,7,10):
        eq(m.quad(lambda v:v**power/m.expm1(v),[0,1,10,m.inf]),m.factorial(power)*m.zeta(power+1),'all-size star representative')
    # Correct boundary factor in the differentiated cutoff K integral.
    # Its O(1-R) decay absorbs every fixed logarithmic power.
    a=m.mpf('.83')
    for k in (3,7,13):
        R=1-m.mpf(10)**(-k)
        eq(R/(1-a*R)-1/(1-a),-(1-R)/((1-a*R)*(1-a)),'H1 cutoff cancellation factor')


def main():
    recurrence_checks(); ranks=finite_span_checks(); numerical_checks()
    print(json.dumps({'status':'PASS_INDEPENDENT_SCOPED_CHECKS','original_problem':'UNRESOLVED','checks':dict(COUNTS),'finite_spans':ranks,'limits':['Finite ranks through weight 9 only','Quadratures are diagnostics, not all-size proofs','No restricted mixed-prefactor or all-order closure claim']},sort_keys=True,indent=2))

if __name__=='__main__': main()
