"""Independent bounded adversarial checks; no imports from the release checker.

Finite evidence supports interfaces and arithmetic, not the universal theorem.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import log
import json


def char(x, p):
    return 0 if x % p == 0 else (1 if pow(x % p, (p-1)//2, p) == 1 else -1)


def trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def mod(a, b, p):
    a = trim(list(a))
    while len(a) >= len(b) and a != [0]:
        q = a[-1] * pow(b[-1], -1, p) % p
        off = len(a)-len(b)
        for j in range(len(b)):
            a[off+j] = (a[off+j]-q*b[j]) % p
        trim(a)
    return a


def coprime(a, b, p):
    a, b = trim(list(a)), trim(list(b))
    while b != [0]:
        a, b = b, mod(a, b, p)
    return len(a) == 1


def sectors():
    out = []
    for p, degree in ((3, 9), (3, 10), (5, 6), (7, 5)):
        count = Counter()
        for cs in product(range(p), repeat=degree):
            if not cs[0]:
                continue
            poly = list(cs)+( [1] )
            at_minus_one = sum(c*(-1)**i for i, c in enumerate(poly)) % p
            if not at_minus_one:
                continue
            deriv = [i*poly[i] % p for i in range(1, degree+1)]
            if coprime(poly, deriv, p):
                count[char(cs[0], p), char(at_minus_one, p)] += 1
        assert sum(count.values()) >= F(p**degree, 3)
        sums = [sum(n * (x, y, x*y)[j] for (x,y), n in count.items()) for j in range(3)]
        half = degree//2
        expected = [1-(p-1)*half]*3
        if degree % 2:
            expected = [x*s for x,s in zip(expected, (-1, -char(-1,p), -1))]
        assert sums == expected, (p, degree, sums, expected)
        if degree >= 8:
            assert min(count.values()) >= F(p**degree,16)
        out.append(dict(p=p, degree=degree, counts={str(k):v for k,v in sorted(count.items())}, character_sums=sums))
    return out


def oorder(n, determinant_character, q):
    if n == 0:
        assert determinant_character == 1
        return 1
    r = n//2
    value = 2*q**(r*r)
    if n % 2:
        for j in range(1,r+1):
            value *= q**(2*j)-1
    else:
        eps = (-1 if q%4 == 3 and r%2 else 1)*determinant_character
        value = 2*q**(r*(r-1))*(q**r-eps)
        for j in range(1,r):
            value *= q**(2*j)-1
    return value


def graph_fibers():
    # Enumerate all maps A->B directly, including positive codimension and q=5.
    out = []
    for p, b in ((3,2),(3,3),(5,2),(5,3),(7,2)):
        nonsquare = next(x for x in range(1,p) if char(x,p) == -1)
        for last_a,last_b in product((1,nonsquare), repeat=2):
            ca,cb = char(last_a,p),char(last_b,p)
            hist = Counter()
            ksets = {}
            for entries in product(range(p), repeat=2*b):
                s00=s01=s11=0
                for row in range(b):
                    weight = last_b if row == b-1 else 1
                    x,y = entries[2*row:2*row+2]
                    s00 += weight*x*x
                    s01 += weight*x*y
                    s11 += weight*y*y
                k00,k01 = s00%p,s01%p
                k10,k11 = s01*pow(last_a,-1,p)%p,s11*pow(last_a,-1,p)%p
                determinant = (k00*k11-k01*k10)%p
                trace = (k00+k11)%p
                if not determinant or char(1+trace+determinant,p) != 1:
                    continue
                if (trace*trace-4*determinant)%p == 0:
                    continue
                key = (determinant, -trace%p, 1)
                hist[key] += 1
                ksets.setdefault(key,set()).add((k00,k01,k10,k11))
            oa,ob = oorder(2,ca,p),oorder(b,cb,p)
            for poly, n in hist.items():
                ck = char(poly[0],p)
                complement = cb*ca*ck
                oc = oorder(b-2,complement,p)
                assert n == F(oa*ob,2*oc), (p,b,last_a,last_b,poly,n)
                assert len(ksets[poly]) == oa//2
            out.append(dict(p=p, dim_b=b, disc_a=ca, disc_b=cb, polynomials=len(hist), graphs=sum(hist.values())))
    return out


def mass_and_subspace_arithmetic():
    minimum = None
    minimum_at = None
    for q in (3,5,7,9,11):
        for a in range(1,25):
            for b in range(a,2*a+1):
                for ca,cb,ck in product((-1,1),repeat=3):
                    cc = ca*cb*ck
                    if b == a and cc != 1:
                        continue
                    m = F(oorder(a,ca,q)**2 * oorder(b,cb,q)**2 * q**a,
                          2*oorder(a+b,ca*cb,q)*oorder(b-a,cc,q))
                    assert m > F(1,8)
                    if minimum is None or m < minimum:
                        minimum, minimum_at = m,(q,a,b,ca,cb,ck)
    checked = 0
    for e in range(6,81):
        for a in range((e+2)//3,2*e//3+1):
            b = e-a
            for k in range(1,e//2+1):
                for i in range(max(0,k-b),min(a,k)+1):
                    j=k-i
                    assert 12*(i*b+j*a-2*i*j) >= e*k
                    if 2*i <= a and 2*j <= b:
                        assert 12*(i*b+j*a-3*i*j) >= e*k
                    checked += 1
    for k in range(1,1001):
        assert 128*(k+1) <= 256**k <= 3**(8*k)
    # q=3 is the worst case for each exponential absorption bound.
    assert F(-1,2)+F(1,16)+F(1,14) <= F(-1,3)
    assert F(21,256)**45 * 3**256 >= 1  # class-size bound at e=16
    assert 12 < 13*(1-F(1,3**(11*384)))
    return dict(normalized_orth_mass_min=str(minimum), minimum_at=minimum_at,
                exponent_cases=checked, constant_absorption_checks=1000)


def threshold_checks():
    out=[]
    for threshold,multiplier,sample_constant,mass_denominator in ((8192,12,40000,1536),(32768,32,5000000,49152)):
        aa={threshold,threshold+1,2*threshold,10**6,10**12}
        # Test around every power-of-two jump in the distinguished degree scale.
        for h in range(7,15):
            z=(2**h)/multiplier-1
            if 0 < z < 29:
                from math import exp
                a=int(exp(z))
                aa.update(x for x in (a-1,a,a+1) if x >= threshold)
        for a in sorted(aa):
            d=1
            while d < multiplier*(1+log(a)):
                d*=2
            assert a >= 24*d
            minimum_n = 4*a if multiplier == 12 else 2*a
            assert mass_denominator*d < sample_constant*log(minimum_n)
            for b in (a,a+1,3*a//2,2*a-1,2*a):
                intervals=((F(a,3),F(2*a,3)),(F(b,3),min(F(2*b,3),F(5*a,6))))
                for lo,hi in intervals:
                    assert hi-lo >= F(a,6)
                    # Count odd multiples of d using exact floor arithmetic.
                    first = -((-lo.numerator)//(lo.denominator*d))
                    last = hi.numerator//(hi.denominator*d)
                    count=(last+1)//2-first//2
                    assert count >= F(a,24*d), (a,b,lo,hi,d,count)
        out.append(dict(threshold=threshold, distinct_a_values=len(aa)))
    return out


def conditioning():
    # Explicitly sum every sequence in a nonuniform law, rather than invoke
    # the geometric-series identity used in the manuscript.
    law = [F(1,11),F(2,11),F(3,11),F(5,11)]
    event = {1,3}
    for length in (1,2,3,4,5):
        selected=Counter()
        for sequence in product(range(4),repeat=length):
            weight=F(1)
            for x in sequence:
                weight*=law[x]
            first=next((x for x in sequence if x in event),None)
            if first is not None:
                selected[first]+=weight
        total=sum(selected.values())
        for x in event:
            assert selected[x]/total == law[x]/sum(law[y] for y in event)
    # Enumerate actual Klein-four coefficient-type assignments: for s factors,
    # fixing total discriminant leaves exactly half each distinguished sign.
    for factors in range(2,13):
        for total in (-1,1):
            good=[]
            for assignment in product((-1,1),repeat=factors):
                value=1
                for sign in assignment:
                    value*=sign
                if value == total:
                    good.append(assignment[0])
            assert good.count(1) == good.count(-1) == 2**(factors-2)
    return dict(first_success_lengths=[1,2,3,4,5], coefficient_type_factor_counts=[2,12])


if __name__ == '__main__':
    result = dict(status='PASS', universal_theorem_certified=False,
                  sectors=sectors(), graph_fibers=graph_fibers(),
                  mass_and_subspace_arithmetic=mass_and_subspace_arithmetic(),
                  threshold_checks=threshold_checks(), conditioning=conditioning())
    print(json.dumps(result,indent=2))
