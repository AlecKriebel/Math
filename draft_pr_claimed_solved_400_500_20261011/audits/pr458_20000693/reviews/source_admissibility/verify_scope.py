#!/usr/bin/env python3
"""Independent local mathematics checks; never an L-function moment certificate.

Standard library only. Uses a logarithmic-derivative coefficient recurrence,
exact Gaussian rationals, and independent finite phase averages. Guards survive -O.
"""
import argparse
import cmath
from fractions import Fraction as F
import json
import math
import sys


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def scale(a, r):
    return (a[0]*r, a[1]*r)


def conj(a):
    return (a[0], -a[1])


def norm(a):
    return a[0]*a[0]+a[1]*a[1]


ZERO = (F(0), F(0))
ONE = (F(1), F(0))
TABLE = {
    'zeta': (1, [ONE]),
    'q3': (3, [ZERO, ONE, (-F(1), F(0))]),
    'q4': (4, [ZERO, ONE, ZERO, (-F(1), F(0))]),
    'quart5': (5, [ZERO, ONE, (F(0), F(1)), (F(0), -F(1)), (-F(1), F(0))]),
    'quart5bar': (5, [ZERO, ONE, (F(0), -F(1)), (F(0), F(1)), (-F(1), F(0))]),
}


def primitive(name, n):
    f, values = TABLE[name]
    return values[n % f]


def character(name, q, n):
    if q < 1 or q % TABLE[name][0]:
        raise ValueError('modulus not a positive multiple of primitive conductor')
    return primitive(name, n) if math.gcd(q, n) == 1 else ZERO


def validate(rows):
    for name, q, a in rows:
        character(name, q, 1)
        if a < 0:
            raise ValueError('negative weights outside reviewed scope')


def grouping(rows, mutant):
    result = {}
    for name, q, a in rows:
        key = q if mutant == 'modulus_groups' else name
        if mutant == 'conjugacy_groups' and name == 'quart5bar':
            key = 'quart5'
        result[key] = result.get(key, F(0)) + a
    return {key: value for key, value in result.items() if value}


def coefficients(terms, degree):
    # If F(t)=prod(1-z t)^(-a), then n*c_n=sum_{j=1}^n S_j*c_(n-j),
    # where S_j=sum a*z^j. This avoids the author's convolution construction.
    sums = [ZERO for _ in range(degree+1)]
    for z, a in terms:
        power = ONE
        for j in range(1, degree+1):
            power = mul(power, z)
            sums[j] = add(sums[j], scale(power, a))
    c = [ONE]
    for n in range(1, degree+1):
        value = ZERO
        for j in range(1, n+1):
            value = add(value, mul(sums[j], c[n-j]))
        c.append(scale(value, F(1, n)))
    return c


def product_coefficients(a, b, degree):
    return [sum((a[j]*b[n-j] for j in range(n+1)), F(0)) for n in range(degree+1)]


def as_complex(z):
    return complex(float(z[0]), float(z[1]))


def numeric_coefficients(terms, degree):
    sums = [0j]*(degree+1)
    for z, a in terms:
        power = 1+0j
        for j in range(1, degree+1):
            power *= z
            sums[j] += float(a)*power
    c = [1+0j]
    for n in range(1, degree+1):
        c.append(sum(sums[j]*c[n-j] for j in range(1, n+1))/n)
    return c


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mutant', choices=['modulus_groups', 'conjugacy_groups',
                        'lift_direction', 'regularizer_sign', 'independent_phase',
                        'ignore_deletion'])
    mutant = parser.parse_args().mutant
    total = 0
    categories = {}

    def check(condition, label, category):
        nonlocal total
        if not condition:
            raise RuntimeError('CHECK FAILED: '+label)
        total += 1
        categories[category] = categories.get(category, 0)+1

    # Validate the explicitly finite primitive character tables independently.
    for name, (f, values) in TABLE.items():
        for a in range(f):
            for b in range(f):
                check(primitive(name, a*b) == mul(values[a], values[b]),
                      name+' multiplicativity', 'character_tables')
        for d in range(1, f):
            if f % d == 0:
                witnesses = [(a,b) for a in range(1,f+1) for b in range(1,f+1)
                             if math.gcd(a,f)==math.gcd(b,f)==1 and a%d==b%d
                             and primitive(name,a)!=primitive(name,b)]
                check(bool(witnesses), name+' primitive at conductor '+str(f),
                      'primitive_conductors')

    cases = [
        [('zeta',1,F(1)),('zeta',2,F(1))],
        [('quart5',5,F(1)),('quart5bar',10,F(1))],
        [('zeta',6,F(1)),('zeta',10,F(1))],
        [('q3',3,F(1,2)),('q3',12,F(3,2)),('q4',20,F(1,3))],
        [('quart5',5,F(1,4)),('quart5',10,F(3,4)),('quart5',20,F(1))],
        [('zeta',30,F(0)),('q4',4,F(1,2))],
        [('zeta',2,F(0))],
        [('q3',3,F(0)),('q4',4,F(0)),('quart5',5,F(0))],
        [('zeta',1,F(2)),('q3',6,F(1)),('q4',12,F(3,2))],
        [('quart5',5,F(1,3)),('quart5bar',5,F(2,3)),('zeta',2,F(1,7))],
    ]
    check(sum(a*a for a in grouping(cases[0], mutant).values())==4,
          'identical primitive inducer across distinct moduli has exponent four', 'aggregation')
    check(sum(a*a for a in grouping(cases[1], mutant).values())==2,
          'distinct quartic conjugate characters have exponent two', 'aggregation')
    check(not grouping(cases[6], mutant), 'all-zero input empty grouping', 'aggregation')

    numerical = []
    for ci, rows in enumerate(cases):
        validate(rows)
        Q = math.lcm(*(q for _,q,_ in rows))
        g = grouping(rows, mutant)
        for p in [2,3,5,7,11,13,17,19]:
            direct_terms = [(character(name,q,p),a) for name,q,a in rows]
            direct = coefficients(direct_terms,12)
            lifted_terms = [(character(name,Q,p),a) for name,q,a in rows]
            lifted_terms += [(primitive(name,p), -a if mutant=='lift_direction' else a)
                             for name,q,a in rows if Q%p==0 and q%p!=0]
            lifted = coefficients(lifted_terms,12)
            for n in range(13):
                check(direct[n]==lifted[n], 'common-modulus lift coefficient', 'local_lift')
            core = coefficients([(primitive(name,p),a) for name,q,a in rows],12)
            aggregated = coefficients([(primitive(name,p),a) for name,a in g.items()],12)
            for n in range(13):
                check(core[n]==aggregated[n], 'primitive aggregation coefficient', 'aggregation')
            if Q%p:
                J = [norm(z) for z in direct[:3]]
                sign = 1 if mutant=='regularizer_sign' else -1
                regularizer = coefficients([(mul(primitive(n,p),conj(primitive(m,p))),
                                            sign*a*b)
                                           for n,a in g.items() for m,b in g.items()],2)
                check(all(z[1]==0 for z in regularizer),'paired regulator real','regularization')
                H = product_coefficients(J,[z[0] for z in regularizer],2)
                check(H[0]==1 and H[1]==0,'regularized first-order term vanishes','regularization')
            if ci not in (6,7) and p in (2,3,5):
                terms = [(as_complex(z),a) for z,a in direct_terms]
                co = numeric_coefficients(terms,160)
                series = sum(abs(z)**2/p**n for n,z in enumerate(co))
                N = 2048
                phases = []
                for j in range(N):
                    phase = cmath.exp(2j*math.pi*j/N)/math.sqrt(p)
                    phases.append(math.prod(abs(1-z*phase)**(-2*float(a)) for z,a in terms))
                average = math.fsum(phases)/N
                relative = abs(series-average)/max(1,abs(average))
                check(relative<2e-13,'independent phase Parseval numeric check','phase_integrals')
                numerical.append({'case':ci,'prime':p,'relative_error':relative})

    # Exact local counterexamples to tempting incorrect substitutions.
    x = F(1,2)
    shared_J = (1+x)/(1-x)**3
    if mutant=='independent_phase': shared_J=1/(1-x)**2
    check(shared_J==12,'two identical local factors common phase gives twelve','negative_controls')
    ratio = (1-x)**2/(1+x)
    if mutant=='ignore_deletion': ratio=F(1)
    check(ratio==F(1,6),'zeta times mod-two principal deletion ratio one sixth','negative_controls')
    check(F(1,12)*F(1,3)*F(8,15)==F(2,135),
          'mod-six and mod-ten principal relative local constant','normalizations')

    for name1,(f1,_) in TABLE.items():
        for name2,(f2,_) in TABLE.items():
            if name1==name2:continue
            q=math.lcm(f1,f2)
            check(any(mul(primitive(name1,n),conj(primitive(name2,n)))!=ONE
                      for n in range(1,q+1) if math.gcd(n,q)==1),
                  'distinct primitive quotient nonprincipal','quotient_characters')

    for rows,label in [([('q3',4,F(1))],'invalid conductor'),
                       ([('zeta',1,F(-1,4))],'negative weight')]:
        rejected=False
        try:validate(rows)
        except ValueError:rejected=True
        check(rejected,label+' explicitly rejected','boundary_input_guards')

    # Matrix constants at integer weights require no special-function library.
    def matrix_integer(N,k):
        return math.prod(F(math.factorial(j-1)*math.factorial(j+2*k-1),
                          math.factorial(j+k-1)**2) for j in range(1,N+1))
    for N in (1,2,3,8,25):
        check(matrix_integer(N,0)==1,'CUE weight zero','matrix_normalizations')
        check(matrix_integer(N,1)==N+1,'CUE weight one exact','matrix_normalizations')
        check(matrix_integer(N,2)==F((N+1)*(N+2)**2*(N+3),12),
              'CUE weight two exact','matrix_normalizations')

    print(json.dumps({'status':'PASS','check_count':total,'categories':categories,
                      'exact_series_degree':12,'cases':len(cases),
                      'phase_integrals':numerical,
                      'scope':'local mathematics and finite CUE identities only',
                      'critical_line_asymptotic_proved':False,
                      'dependency':'Python standard library'},indent=2,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError) as error:
        print(str(error),file=sys.stderr)
        sys.exit(1)
