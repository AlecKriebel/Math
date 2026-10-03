#!/usr/bin/env python3
"""Independent finite/local/model checks; no test of actual L-function moments.

The coefficient construction uses a logarithmic-derivative recurrence rather
than the author's binomial convolution. CUE checks use Toeplitz determinants
of numerical Fourier integrals, separately from the Gamma-product formula.
"""
import json
import math
from pathlib import Path
import sympy as s
import mpmath as mp

ROOT = Path(__file__).resolve().parent
mp.mp.dps = 65
I = s.I
P = {
    'zeta': (1, [1]),
    'q3': (3, [0, 1, -1]),
    'q4': (4, [0, 1, 0, -1]),
    'q5': (5, [0, 1, -1, -1, 1]),
    'quart5': (5, [0, 1, I, -I, -1]),
    'quart5bar': (5, [0, 1, -I, I, -1]),
    'q8': (8, [0, 1, 0, -1, 0, -1, 0, 1]),
    'qminus8': (8, [0, 1, 0, 1, 0, -1, 0, -1]),
    'q12': (12, [0, 1, 0, 0, 0, -1, 0, -1, 0, 0, 0, 1]),
}
CASES = [
    [],
    [('zeta', 30, s.Rational(0))],
    [('zeta', 1, s.Rational(1)), ('zeta', 2, s.Rational(1))],
    [('q3', 3, s.Rational(1, 2)), ('q3', 12, s.Rational(3, 2)), ('q4', 20, s.Rational(1, 3))],
    [('quart5', 5, s.Rational(3, 4)), ('quart5bar', 10, s.Rational(5, 4))],
    [('quart5', 5, s.Rational(1, 4)), ('quart5', 10, s.Rational(3, 4)), ('quart5', 20, s.Rational(2))],
    [('q8', 8, s.Rational(1, 2)), ('qminus8', 24, s.Rational(1, 2)), ('q12', 60, s.Rational(1))],
    [('zeta', 1, s.Rational(1, 3)), ('q5', 35, s.Rational(2, 3)), ('q3', 6, s.Rational(0))],
    [('q4', 4, s.Rational(0)), ('q4', 12, s.Rational(0))],
]

def primitive(name, p):
    f, v = P[name]
    return s.sympify(v[p % f])

def actual(name, q, p):
    assert q % P[name][0] == 0
    return primitive(name, p) if math.gcd(q, p) == 1 else s.Integer(0)

def coeff(terms, degree):
    # n b_n = sum_{k=1}^n (sum_j a_j c_j^k) b_{n-k}.
    power_sums = [None] + [s.expand(sum(a * c**k for c, a in terms)) for k in range(1, degree + 1)]
    b = [s.Integer(1)]
    for n in range(1, degree + 1):
        b.append(s.expand(sum(power_sums[k] * b[n-k] for k in range(1, n+1)) / n))
    return b

def multiply(a, b):
    return [s.expand(sum(a[j] * b[n-j] for j in range(n+1))) for n in range(min(len(a), len(b)))]

def equal(a, b):
    return len(a) == len(b) and all(s.simplify(x-y) == 0 for x, y in zip(a,b))

def group(rows):
    out = {}
    for n, q, a in rows:
        out[n] = out.get(n, 0) + a
    return {k: v for k, v in out.items() if v != 0}

counts = {'lift_identity_cases': 0, 'aggregation_cases': 0, 'zero_omission_cases': 0,
          'regularization_cases': 0, 'distinct_pair_witnesses': 0, 'exact_normalizations': 0,
          'parseval_cases': 0, 'cue_toeplitz_cases': 0, 'cue_integer_exact_cases': 0}
primes = [2, 3, 5, 7, 11, 13, 17, 19]
for rows in CASES:
    Q = math.lcm(*(q for _, q, _ in rows)) if rows else 1
    groups = group(rows)
    for p in primes:
        original = coeff([(actual(n,q,p),a) for n,q,a in rows],10)
        common = [(actual(n,Q,p),a) for n,q,a in rows]
        restored = common + [(primitive(n,p),a) for n,q,a in rows if Q % p == 0 and q % p != 0]
        assert equal(original,coeff(restored,10))
        counts['lift_identity_cases'] += 1
        assert equal(coeff([(primitive(n,p),a) for n,q,a in rows],10),
                     coeff([(primitive(n,p),a) for n,a in groups.items()],10))
        counts['aggregation_cases'] += 1
        assert equal(original,coeff([(actual(n,q,p),a) for n,q,a in rows if a != 0],10))
        counts['zero_omission_cases'] += 1
        if Q % p:
            J = [s.expand(b*s.conjugate(b)) for b in original[:4]]
            ordered = [(primitive(n,p)*s.conjugate(primitive(m,p)),-a*b)
                       for n,a in groups.items() for m,b in groups.items()]
            H = multiply(J,coeff(ordered,3))
            assert H[0] == 1 and s.simplify(H[1]) == 0
            assert all(s.simplify(s.im(c)) == 0 for c in H)
            counts['regularization_cases'] += 1

# Finite witnesses supplement, but do not replace, the uniqueness-of-inducer proof.
names = list(P)
for i,n in enumerate(names):
    for m in names[i+1:]:
        Q = math.lcm(P[n][0],P[m][0])
        assert any(primitive(n,int(p))*s.conjugate(primitive(m,int(p))) != 1
                   for p in s.primerange(2,200) if Q % int(p))
        counts['distinct_pair_witnesses'] += 1

# Closed two-factor local identity, with u on the unit circle and u != 1.
x,u = s.symbols('x u', nonzero=True)
from_geometric = (2/(1-x)-u/(1-u*x)-(1/u)/(1-x/u))/(2-u-1/u)
closed = (1-x*x)/((1-x)**2*(1-u*x)*(1-x/u))
assert s.factor(from_geometric-closed) == 0
assert s.simplify(s.limit(closed,u,1)-(1+x)/(1-x)**3) == 0
assert s.simplify(closed.subs(u,-1)-1/(1-x*x)) == 0
assert s.simplify(closed*(1-x)**2*(1-u*x)*(1-x/u)-(1-x*x)) == 0
counts['exact_normalizations'] += 4
J1 = 1/(1-x)
J2 = (1+x)/(1-x)**3
assert s.simplify((1-x)**4*J2-(1-x*x)) == 0
assert s.simplify(J1/J2-(1-x)**2/(1+x)) == 0
assert (J1/J2).subs(x,s.Rational(1,2)) == s.Rational(1,6)
assert s.simplify((1-x)**4/(1-x*x)-(1-x)**3/(1+x)) == 0
assert s.simplify((1-x)/(1-x*x)-1/(1+x)) == 0
assert s.simplify((1-x)**2/(1-x*x)-(1-x)/(1+x)) == 0
assert closed.subs({u:-1,x:s.Rational(1,3)}) == s.Rational(9,8)
assert J1.subs(x,s.Rational(1,3))**2 == s.Rational(9,4)
counts['exact_normalizations'] += 8

def num(z):
    z = s.sympify(z)
    return mp.mpc(str(s.N(s.re(z),70)),str(s.N(s.im(z),70)))

phase_results=[]
for case in [2,3,4,5,6,7]:
    for p in [2,3,5]:
        terms = [(num(actual(n,q,p)),mp.mpf(int(a.p))/int(a.q)) for n,q,a in CASES[case]]
        S = [mp.mpc(0)] + [sum(a*c**k for c,a in terms) for k in range(1,241)]
        b = [mp.mpc(1)]
        for n in range(1,241):
            b.append(sum(S[k]*b[n-k] for k in range(1,n+1))/n)
        series = sum(abs(b[n])**2/mp.mpf(p)**n for n in range(241))
        phase = mp.quad(lambda t: mp.fprod(abs(1-c*mp.e**(1j*t)/mp.sqrt(p))**(-2*a) for c,a in terms),
                        [0,mp.pi,2*mp.pi])/(2*mp.pi)
        error=abs(series-phase)
        assert error < mp.mpf('1e-45')
        counts['parseval_cases'] += 1
        phase_results.append({'case':case,'p':p,'error':mp.nstr(error,12)})

# Weyl integration gives a Toeplitz determinant of Fourier coefficients.
# Compute these coefficients from their integrals, not from Gamma functions.
cue_results=[]
for m in [mp.mpf('0.25'),mp.mpf('0.5'),mp.mpf('1.5'),mp.mpf('2.25')]:
    fourier=[mp.quad(lambda t,k=k:(2*abs(mp.sin(t/2)))**(2*m)*mp.cos(k*t),
                     [0,mp.pi,2*mp.pi])/(2*mp.pi) for k in range(5)]
    for N in [1,2,3,4,5]:
        determinant=mp.det(mp.matrix([[fourier[abs(j-k)] for k in range(N)] for j in range(N)]))
        gamma=mp.fprod(mp.gamma(j)*mp.gamma(j+2*m)/mp.gamma(j+m)**2 for j in range(1,N+1))
        error=abs(determinant/gamma-1)
        assert error < mp.mpf('1e-45')
        counts['cue_toeplitz_cases'] += 1
        cue_results.append({'m':str(m),'N':N,'relative_error':mp.nstr(error,12)})
for m in [1,2]:
    for N in range(1,13):
        def fc(k):
            return s.Integer((-1)**abs(k))*s.binomial(2*m,m+k) if abs(k)<=m else s.Integer(0)
        det=s.det(s.Matrix([[fc(j-k) for k in range(N)] for j in range(N)]))
        closedN=N+1 if m==1 else s.Rational((N+1)*(N+2)**2*(N+3),12)
        assert det == closedN
        counts['cue_integer_exact_cases'] += 1
assert abs(mp.barnesg(2)**2/mp.barnesg(3)-1) < mp.mpf('1e-60')
assert abs(mp.barnesg(3)**2/mp.barnesg(5)-mp.mpf(1)/12) < mp.mpf('1e-60')
counts['exact_normalizations'] += 2

report={'status':'PASS','scope':'Independent exact local identities and finite random-matrix/phase checks only; no L-function moment asymptotic is proved or numerically certified.',
        'methods':['logarithmic-derivative coefficient recurrence','exact geometric-series local identity',
                   'independent high-precision phase integrals','CUE Toeplitz determinants from numerical Fourier integrals'],
        'counts_by_case_family':counts,'total_cases':sum(counts.values()),
        'case_count_convention':'One case per listed prime/input or matrix size; coefficientwise assertions are not counted separately.',
        'parseval_results':phase_results,'cue_results':cue_results,'asymptotic_proved':False,
        'versions':{'sympy':s.__version__,'mpmath':mp.__version__}}
(ROOT/'REVIEWER_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
