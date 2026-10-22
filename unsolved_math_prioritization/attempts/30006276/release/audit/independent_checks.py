#!/usr/bin/env python3
"""Independent rational checks. Requires SymPy; imports no author implementation.
All mock rings below are logical controls, never geometric counterexamples on A_g.
"""
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'author'
EXPECTED_MANIFEST = '83549a36a97a878966348ab32cdfe0798e235e299b6841973e21c63434afec08'
assertions = 0

def check(condition):
    global assertions
    assertions += 1
    if not condition:
        raise AssertionError(assertions)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

check(sha(AUTHOR / 'SHA256SUMS') == EXPECTED_MANIFEST)
files = []
for line in (AUTHOR / 'SHA256SUMS').read_text().splitlines():
    digest, filename = line.split()
    check(sha(AUTHOR / filename) == digest)
    files.append({'file': filename, 'sha256': digest})
replay = subprocess.run([sys.executable, str(AUTHOR / 'verify_controls.py')],
                        capture_output=True, check=True).stdout
check(replay == (AUTHOR / 'control_results.json').read_bytes())
record = json.loads(replay)
check(record['exact_assertions'] == 5250)
check(record['codimension_controls']['partitions_examined'] == 215267)

# Chern relations with no rewrite algorithm from the author.
def ring(n):
    xs = s.symbols('l1:' + str(n + 1))
    cs = [s.Integer(1), *xs]
    rel = [sum((-1)**j * cs[i] * cs[j]
               for i in range(n+1) for j in range(n+1) if i+j == d)
           for d in range(2, 2*n+1, 2)]
    gb = s.groebner(rel, *xs, order='grevlex', domain=s.QQ)
    def nf(poly):
        return s.expand(gb.reduce(s.sympify(poly))[1])
    mons = [(tuple(i+1 for i in range(n) if mask & (1 << i)),
             s.prod(xs[i] for i in range(n) if mask & (1 << i)))
            for mask in range(1 << n)]
    return xs, gb, nf, mons

ring_results = []
for n in range(1, 8):
    xs, gb, nf, mons = ring(n)
    N = n*(n+1)//2
    top = s.prod(xs)
    top_nf = nf(top)
    check(top_nf != 0)
    top_poly = s.Poly(top_nf, *xs)
    top_lm, top_lc = top_poly.terms()[0]
    def trace(poly):
        reduced = nf(poly)
        coeff = s.Poly(reduced, *xs).coeff_monomial(top_lm) / top_lc
        check(s.expand(reduced - coeff*top_nf) == 0)
        return coeff
    normal = [s.Poly(nf(m), *xs) for _, m in mons]
    mon_set = sorted(set().union(*(set(p.monoms()) for p in normal)))
    matrix = s.Matrix([[p.coeff_monomial(mon) for p in normal] for mon in mon_set])
    check(matrix.rank() == 2**n)
    for inds, mon in mons:
        expected = 0 if n in inds else mon * xs[-1]
        check(nf(xs[-1]*mon-expected) == 0)
    pairings = []
    for d in range(N+1):
        left = [m for inds,m in mons if sum(inds)==d]
        right = [m for inds,m in mons if sum(inds)==N-d]
        check(len(left) == len(right))
        gram = s.Matrix([[trace(a*b) for b in right] for a in left])
        det = gram.det()
        check(det != 0)
        pairings.append({'degree':d, 'dimension':len(left), 'determinant':str(det)})
    ring_results.append({'g':n+1, 'basis_dimension':2**n,
                         'pairings':pairings})

# Source-normalized J_g = Tor_* 1, independently transcribed from v3 Section 1.3.
source_coeffs = {
    5: [(144,(1,2)),(-96,(3,))],
    6: [(768,(1,2,3)),(-2304,(2,4)),(s.Rational(948096,691),(1,5))],
    7: [(1536,(1,2,3,4)),(-13824,(2,3,5)),(s.Rational(4418304,691),(1,4,5)),
        (s.Rational(15044352,691),(1,3,6)),(-s.Rational(17685504,691),(4,6))]
}
torelli=[]
for row in record['torelli_square_right_hand_sides']:
    g=row['g']; xs, gb, nf, mons = ring(g-1)
    def mono(inds): return s.prod(xs[i-1] for i in inds)
    pj=sum(c*mono(inds) for c,inds in source_coeffs[g])
    stated=sum(s.Rational(term['coefficient'])*mono(term['lambda_indices'])
               for term in row['P_J_squared'])
    check(nf(pj**2-stated)==0)
    N=g*(g-1)//2; c=(g-2)*(g-3)//2; delta=N-2*c
    tests=[(inds,m) for inds,m in mons if sum(inds)==delta]
    check({inds for inds,m in tests} ==
          {tuple(t['test_lambda_indices']) for t in row['required_J_squared_test_values']})
    top=s.prod(xs); tn=nf(top); tp=s.Poly(tn,*xs); lm,lc=tp.terms()[0]
    vals=[]
    for inds,m in tests:
        value=nf(pj**2*m)
        coeff=s.Poly(value,*xs).coeff_monomial(lm)/lc
        check(s.expand(value-coeff*tn)==0)
        expected=next(t['normalized_top_pairing'] for t in row['required_J_squared_test_values']
                      if tuple(t['test_lambda_indices'])==inds)
        check(coeff==s.Rational(expected))
        vals.append({'test':list(inds),'normalized_value':str(coeff)})
    # Each nonzero coordinate perturbation in the relevant degree must be detected.
    target_basis=[(inds,m) for inds,m in mons if sum(inds)==2*c]
    for inds,m in target_basis:
        check(any(nf(m*t)!=0 for _,t in tests))
    torelli.append({'g':g,'test_degree':delta,'tests':vals,
                    'nonzero_basis_mutations_detected':len(target_basis),
                    'actual_geometric_left_hand_sides_computed':False})

# Independent descending partition enumeration (different recurrence/order).
def descending(n, cap=None, prefix=()):
    if n==0:
        yield prefix
    else:
        for p in range(min(n, cap or n),0,-1):
            yield from descending(n-p,p,prefix+(p,))
# Unrelated coin-change DP verifies the total enumeration count.
p=[1]+[0]*50
for coin in range(1,51):
    for j in range(coin,51): p[j]+=p[j-coin]
counts=[]; subtotal=0; extended=0
for g in range(2,51):
    found=set(); count=0
    for part in descending(g):
        if len(part)==1: continue
        count+=1
        q=(g*g-sum(x*x for x in part))//2
        if q<=2*g-3: found.add(tuple(sorted(part)))
    expect={(1,g-1)}
    if g>=4: expect.add((2,g-2))
    if g>=3: expect.add((1,1,g-2))
    if g==6: expect.add((3,3))
    check(found==expect)
    check(count==p[g]-1)
    if g<=40: subtotal+=count
    extended+=count
    counts.append({'g':g,'partitions':count,'surviving_shapes':len(found)})
check(subtotal==215267)
for g in range(2,1001):
    c=(g-2)*(g-3)//2; N=g*(g-1)//2
    check((2*c<=N)==(g<=7))

# Discriminator A: the annihilator alone cannot imply P(I^2)=0.
x=s.Symbol('x')
def trunc(poly,k): return s.rem(s.expand(poly), x**k, domain=s.QQ)
def proj(poly):
    p=s.Poly(trunc(poly,3),x)
    return p.coeff_monomial(1)+p.coeff_monomial(x**2)*x**2
for a,b,c in itertools.product([1,x,x*x],repeat=3):
    check(trunc(trunc(a*b,3)*c,3)==trunc(a*trunc(b*c,3),3))
for a,r in itertools.product([1,x,x*x],[1,x*x]):
    check(proj(trunc(a*r,3))==trunc(proj(a)*r,3))
check(proj(x)==0)
check(trunc(x*x*x,3)==0)
check(proj(x*x)==x*x)
check(trunc(proj(x)*proj(x),3)==0)

# Discriminator B: homogeneous kernel squares alone do not test mixed degrees.
y=s.Symbol('y'); h=s.groebner([x*x,y*y],x,y,domain=s.QQ)
def hn(poly): return s.expand(h.reduce(s.sympify(poly))[1])
def hp(poly):
    p=s.Poly(hn(poly),x,y)
    return p.coeff_monomial(1)+p.coeff_monomial(x*y)*x*y
check(hp(x)==hp(y)==0)
check(hp(x*x)==hp(y*y)==0)
check(hp(x*y)==x*y)
check(hp((x+y)**2)==2*x*y)
# Discriminator C: genus-one lambda_0=1 does not satisfy the displayed g>=2 lemma.
check(1*1!=0)

output={'verdict':'passed_with_genus_one_scope_correction','author_manifest':EXPECTED_MANIFEST,
        'author_replay':{'exact_assertions':5250,'partition_cases':215267,'byte_identical':True},
        'sympy_version':s.__version__,'independent_exact_assertions':assertions,
        'groebner_and_pairing_checks':ring_results,'torelli_checks':torelli,
        'partition_check':{'range':[2,50],'cases':extended,'original_range_cases':subtotal,'counts':counts},
        'self_product_cutoff_range':[2,1000],
        'logical_discriminators':[
            'Q[x]/(x^3), R=Q[x^2]: lambda I=0 and P(I)^2=0, but P(I^2) nonzero.',
            'Q[x,y]/(x^2,y^2), deg x=1, deg y=2: homogeneous kernel squares zero; mixed product detected.',
            'g=1: lambda_0=1, so Ann(lambda_0)=0 and lambda_0^2=1.'],
        'limitations':['No mock ring is a counterexample on A_g.',
                       'No unknown geometric intersection number is evaluated.',
                       'Finite checks do not prove the all-genus claim.']}
print(json.dumps(output,indent=2,sort_keys=True))
