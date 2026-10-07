#!/usr/bin/env python3
"""Independent standard-library audit controls; imports no author implementation."""
from fractions import Fraction as F
from itertools import combinations
from math import comb, isqrt
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sqrt_rational(q):
    q = F(q)
    if q < 0:
        return None
    p, r = isqrt(q.numerator), isqrt(q.denominator)
    if p*p == q.numerator and r*r == q.denominator:
        return F(p, r)
    return None


def entries(values):
    return [(i+1, j+1, a*b+1, sqrt_rational(a*b+1))
            for i, a in enumerate(values) for j, b in enumerate(values) if i <= j]


def is_strong(values):
    return bool(values) and 0 not in values and len(set(values)) == len(values) and all(
        r is not None for i, j, q, r in entries(values))


def gf2rank(rows):
    basis = {}
    for row in rows:
        while row:
            col = row.bit_length()-1
            if col in basis:
                row ^= basis[col]
            else:
                basis[col] = row
                break
    return len(basis)


class P:
    """Sparse integer polynomials in four formal variables a,b,c,t."""
    def __init__(self, x=0):
        self.d = x if isinstance(x, dict) else {(0,0,0,0): x}
        self.d = {m:v for m,v in self.d.items() if v}

    def __add__(self, other):
        other = other if isinstance(other, P) else P(other)
        d = self.d.copy()
        for m,v in other.d.items(): d[m] = d.get(m,0)+v
        return P(d)
    __radd__ = __add__

    def __neg__(self): return P({m:-v for m,v in self.d.items()})
    def __sub__(self, other): return self + -(other if isinstance(other,P) else P(other))
    def __rsub__(self, other): return P(other) + -self

    def __mul__(self, other):
        other = other if isinstance(other,P) else P(other)
        d = {}
        for m,v in self.d.items():
            for n,w in other.d.items():
                p = tuple(x+y for x,y in zip(m,n)); d[p] = d.get(p,0)+v*w
        return P(d)
    __rmul__ = __mul__

    def __pow__(self, n):
        ans = P(1)
        for _ in range(n): ans = ans*self
        return ans


def zero(p, label): require(not p.d, label)


def main():
    a,b,c,t = (P({tuple(1 if j==i else 0 for j in range(4)):1}) for i in range(4))
    zero((t*t-1)**2+4*t*t-(t*t+1)**2, 'new diagonal identity')
    zero(2*t*(a*t*t+2*t-a)-2*t*(a*(t*t-1)+2*t), 'cover identity')
    zero(a*(a-b)+(a*b+1)-(a*a+1), 'pivot cross identity')
    zero((a-b)**2+(a*b+1)**2-(a*a+1)*(b*b+1), 'transformed diagonal')
    zero((a-b)*(a-c)+(a*b+1)*(a*c+1)-(a*a+1)*(b*c+1), 'transformed cross')
    zero((a-b)*(a*c+1)-(a-c)*(a*b+1)-(c-b)*(a*a+1), 'injectivity numerator')
    zero((a-b)-a*(a*b+1)+b*(a*a+1), 'no pivot collision')
    zero((a*t*t+2*t-a)-(b*t*t+2*t-b)-(a-b)*(t*t-1), 'root separation identity')

    almost = tuple(map(F, ['140/51','2223/30464','278817/33856','3182740/17661']))
    triple = tuple(map(F, ['1976/5607','3780/1691','14596/1197']))
    exceptional = tuple(map(F, ['37620/26299','195/28','-28/195']))
    rows = entries(almost)
    require([(i,j) for i,j,q,r in rows if r is None] == [(3,4)], 'only missing edge')
    require(rows[8][2] == F(459627303,309488), 'exact bad value')
    require(21438**2 < rows[8][2].numerator < 21439**2, 'bad numerator bounds')
    require(556**2 < rows[8][2].denominator < 557**2, 'bad denominator bounds')
    require(is_strong(triple) and is_strong(exceptional), 'source triples')
    require(sqrt_rational(F(2223,3046)**2+1) is None, 'printed typo fails diagonal')
    require(not is_strong((F(1),F(3),F(8),F(120))), 'ordinary not strong')
    require(not is_strong(triple+(F(0),)) and not is_strong(triple+(triple[0],)), 'distinct/nonzero guards')

    regular=[]
    u,v,w=triple
    base=u+v+w+2*u*v*w
    delta=2*sqrt_rational(u*v+1)*sqrt_rational(u*w+1)*sqrt_rational(v*w+1)
    for d in (base-delta,base+delta):
        require(all(sqrt_rational(q*d+1) is not None for q in triple), 'ordinary extension crosses')
        require(sqrt_rational(d*d+1) is None, 'ordinary extension diagonal fails')
        regular.append(str(d))
    require(regular==['135938/106533','789662/11837'], 'regular exact values')

    base=(F(3,4),F(-4,3)); t=F(3,4); x=(t*t-1)/(2*t)
    require(is_strong(base) and x==F(-7,24), 'nonlifting base')
    vals=[q*x+1 for q in base]; qs=[q*t*t+2*t-q for q in base]
    require(vals==[F(25,32),F(25,18)], 'nonlifting values')
    require(all(sqrt_rational(v) is None for v in vals), 'individual nonsquares')
    require(sqrt_rational(vals[0]*vals[1])==F(25,24), 'product square')
    require(qs==[F(75,64),F(25,12)] and sqrt_rational(qs[0]*qs[1])==F(25,16), 'quotient point')

    lifting_checks=0
    for fixed in (almost[:2],triple,exceptional):
        for n in range(-12,13):
            if n==0: continue
            for den in range(1,10):
                t=F(n,den); x=(t*t-1)/(2*t)
                lifted=x!=0 and x not in fixed and all(
                    sqrt_rational(2*t*(a*t*t+2*t-a)) is not None for a in fixed)
                require(lifted==is_strong(fixed+(x,)), 'independent equivalence fixture')
                lifting_checks+=1
        roots=[]
        for a in fixed:
            s=sqrt_rational(a*a+1)
            for r in ((-1+s)/a,(-1-s)/a):
                require(r!=0 and a*r*r+2*r-a==0 and r not in roots,'distinct branch roots')
                roots.append(r)
    for x in almost[2:]:
        for t in (x+sqrt_rational(x*x+1),x-sqrt_rational(x*x+1)):
            require((t*t-1)/(2*t)==x and all(sqrt_rational(2*t*(a*t*t+2*t-a)) is not None for a in almost[:2]), 'known lift in both sheets')
    x=exceptional[2];t=x+sqrt_rational(x*x+1)
    require(all(sqrt_rational(2*t*(a*t*t+2*t-a)) is not None for a in exceptional[:2]),'zero cross lift allowed')

    genus=[]
    for k in range(1,9):
        private_rows=[1<<i for i in range(k) for _ in range(2)]
        common=(1<<k)-1
        require(gf2rank(private_rows)==k, 'global independence')
        require(gf2rank([common])==1, 'common-place inertia rank is one')
        N=2**k; B=len(private_rows)+2
        g=1+(-2*N+B*(N//2))//2
        require(g==1+2**(k-1)*(k-1), 'Riemann-Hurwitz arithmetic')
        require(g==sum(comb(k,s)*(s-1+(s%2)) for s in range(1,k+1)), 'character quotient genus crosscheck')
        genus.append({'k':k,'degree':N,'branch_points':B,'common_inertia_index':2,'genus':g})

    signed=tuple(map(F,['140/51','187/84','-427/1836']))
    sign_checks=0
    for fixed in (triple,signed,tuple(-x for x in signed),tuple(-x for x in triple),almost[:3],(almost[0],almost[1],almost[3])):
        require(is_strong(fixed),'normalization input')
        vals=fixed if max(fixed)>0 else tuple(-x for x in fixed)
        a=max(vals)
        out=(a,)+tuple((a-b)/(a*b+1) for b in vals if b!=a)
        require(all(x>0 for x in out) and len(out)==len(vals) and is_strong(out),'positive output')
        sign_checks+=1
    require(exceptional[1]*exceptional[2]+1==0,'zero exception is genuine')
    grid=tuple(map(F,['-3','-2','-1','-1/2','-1/3','0','1/3','1/2','1','2','3']))
    ordered_checks=0
    for k in range(2,6):
        for values in combinations(grid,k):
            pairs=list(combinations(values,2))
            if any(a*b+1<0 for a,b in pairs):continue
            edges=[(a,b) for a,b in pairs if a*b+1==0]
            require(len(edges)<=1, 'at most one zero edge')
            require(not edges or edges==[(min(values),max(values))], 'zero edge endpoints')
            ordered_checks+=1
    return {'outcome':'PASS', 'problem_id':8500009,'symbolic_polynomial_identities':8,
            'lifting_fixtures':lifting_checks,'positive_normalization_fixtures':sign_checks,
            'zero_edge_order_fixtures':ordered_checks,'genus_crosschecks':genus,
            'almost_bad_pair':[3,4], 'regular_extensions':regular,
            'quotient_witness_Q_values':[str(q) for q in qs],
            'scope':'Independent finite exact and symbolic algebra controls, plus combinatorial genus arithmetic; abstract proof is audited separately. No exhaustive rational search.'}


if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
