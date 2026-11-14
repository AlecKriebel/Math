"""Own cyclotomic-ring and direct-orbit diagnostics, read before execution.
Only finite evidence; all universal arguments are in the written derivation.
No target imports, network, file writes, numeric character approximations or pip.
"""
from collections import Counter
from fractions import Fraction as F
from math import gcd, isqrt
import json
from sympy import Poly, Symbol, cyclotomic_poly

X = Symbol('X')
checks = 0

def ck(test, why):
    global checks
    checks += 1
    if not test:
        raise RuntimeError(why)

def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p)+1))

def mu(n):
    sign, d = 1, 2
    while d*d <= n:
        if n % d == 0:
            n //= d
            sign = -sign
            if n % d == 0:
                return 0
        d += 1
    return sign if n == 1 else -sign

def phi(n):
    return sum(gcd(k, n) == 1 for k in range(n))

def ramp(t):
    return max(F(0), min(F(1), 2*t-1))

rows, negative = [], []
for p in [q for q in range(3, 32, 2) if prime(q)]:
    n = p-1
    generator = next(g for g in range(1, p) if len({pow(g,k,p) for k in range(n)}) == n)
    log = {pow(generator,k,p): k for k in range(n)}
    mod = Poly(cyclotomic_poly(n, X), X, domain='ZZ')
    def reduce(coef):
        return Poly(sum(c*X**k for k,c in enumerate(coef)), X, domain='ZZ').rem(mod)
    def eta(t):
        return 0 if t % p == 0 else (1 if pow(t % p,n//2,p) == 1 else -1)
    char_rows = []
    for k in range(1,n):
        ss, jj, conjugate = [0]*n, [0]*n, [0]*n
        for u in range(p):
            a = (u*u+1) % p
            if a:
                j = (k*log[a]) % n
                ss[j] += 1
                conjugate[-j % n] += 1
        for t in range(p):
            a = (1-t) % p
            if a:
                jj[(k*log[a]) % n] += eta(t)
        s, j = reduce(ss), reduce(jj)
        ck(s == eta(-1)*j, 'exact Jacobi identity in Q[zeta_(p-1)]')
        norm = (s*reduce(conjugate)).rem(mod)
        expected = 1 if k == n//2 else p
        ck(norm == Poly(expected,X,domain='ZZ'), 'exact squared character modulus')
        char_rows.append({'character_exponent':k,'squared_modulus':expected})
    for exponent in range(n):
        indicator = F(phi(n),n)*sum((F(mu(d),phi(d))*sum(e*mu(d//e) for e in range(1,d+1) if d%e==0 and exponent%e==0) for d in range(1,n+1) if n%d==0),F(0))
        ck(indicator == int(gcd(exponent,n)==1), 'primitive indicator via exact Ramanujan sums')
    multipliers = [(u*u+1)%p for u in range(p)]
    r = multipliers.count(0)
    vertices = {(u,v) for u in range(p) if multipliers[u] for v in range(p)}
    unseen = set(vertices)
    cycle_lengths = []
    while unseen:
        start = min(unseen)
        z = start
        path = []
        while z not in path:
            ck(z in unseen, 'direct regular orbit cannot merge into a previous cycle')
            path.append(z)
            z = (z[0], multipliers[z[0]]*z[1] % p)
        ck(z == start, 'direct regular orbit closes at its starting point')
        unseen.difference_update(path)
        cycle_lengths.append(len(path))
    hist = Counter()
    for d in cycle_lengths:
        hist[d] += d
    total = p*(p-r)
    ck(sum(hist.values()) == total, 'direct point-weighted cycle mass')
    primitive = sum(gcd(log[a],n)==1 for a in multipliers if a)
    moment = sum(F(count,total)*ramp(F(d,p)) for d,count in hist.items())
    ck(moment == (1-F(2,p))*F((p-1)*primitive,total), 'direct cyclotomic/orbit ramp bridge')
    for x in [F(1,2), F(3,4), F(p-1,p)]:
        cdf = F(sum(count for d,count in hist.items() if F(d,p)<=x),total)
        if p*(1-x)>1:
            ck(cdf == 1-F((p-1)*primitive,total), 'direct CDF under strict eventual threshold')
        else:
            ck(cdf == 1, 'direct CDF at/above maximal normalized period')
    if r:
        # Heterogeneous exceptional assignments and partial retention, not just
        # the common assigned period used in the supplied checker.
        periods = [F(0),F(1,p),F(p),F(p*p)]*(r*p//4+1)
        for e in [1,p-1,r*p]:
            extra = periods[:e]
            completed_moment = (total*moment+sum(map(ramp,extra)))/(total+e)
            ck(abs(completed_moment-moment) <= F(r,p), 'heterogeneous exceptional ramp bound')
            for x in [F(1,2),F(3,4),F(1),F(p)]:
                reg = F(sum(count for d,count in hist.items() if F(d,p)<=x),total)
                completed = F(sum(count for d,count in hist.items() if F(d,p)<=x)+sum(t<=x for t in extra),total+e)
                ck(abs(completed-reg)<=F(r,p), 'heterogeneous exceptional CDF bound')
    rows.append({'p':p,'r':r,'primitive_parameters':primitive,'regular_points':total,'direct_cycles':len(cycle_lengths),'histogram':dict(sorted(hist.items())),'character_checks':char_rows})

def reject(label, false_claim):
    try:
        if not false_claim:
            raise RuntimeError('intended mathematical mutation rejected')
    except RuntimeError:
        negative.append({'mutation':label,'status':'EXPECTED_REJECTION'})
        return
    raise RuntimeError('negative control unexpectedly accepted: '+label)

reject('full-affine permutation at p=5', len({(u,((u*u+1)*v)%5) for u in range(5) for v in range(5)})==25)
reject('eventual CDF identity at p=3,x=3/4', F(1)==1-F(2*2,9))
reject('nonprincipal quadratic character has squared modulus p', F(1)==F(7))
reject('principal character counts zero multipliers as 1 at p=5', 5==sum((u*u+1)%5!=0 for u in range(5)))
rr=next(row for row in rows if row['p']==7)
h=rr['histogram'];point=F(sum(c for d,c in h.items() if 4*d<=3*7),49)
cycle=F(sum(c//d for d,c in h.items() if 4*d<=3*7),sum(c//d for d,c in h.items()))
reject('replace uniform point weighting by uniform cycle weighting', point==cycle)
# Even mass2/p at normalized period p^2 defeats an unbounded first moment.
reject('replace bounded ramp by unbounded t in arbitrary completion claim', F(2,101)*101**2 <= F(2,101))
reject('squared multiplier u^2 can be treated as the original nonsquare quadratic family', any(gcd(k,6)==1 for k in [0,2,4]))

print(json.dumps({'scope':'Exact finite cyclotomic and direct-orbit diagnostics only; no empirical proof of limiting prime laws','status':'OWN_FINITE_IDENTITIES_AND_EXPECTED_REJECTIONS_CONFIRMED','positive_checks':checks,'primes':len(rows),'nonprincipal_characters':sum(len(r['character_checks']) for r in rows),'negative_controls':negative,'rows':rows},indent=2))
