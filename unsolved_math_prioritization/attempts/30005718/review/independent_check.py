#!/usr/bin/env python3
"""Independent review controls. No author modules are imported.

Run with Python and SymPy. The analytic uniform estimates are reviewed in
INDEPENDENT_REVIEW.md; these exact controls do not certify an effective N.
"""
from pathlib import Path
from collections import Counter
from math import comb, factorial
import hashlib, json
import sympy as S

ROOT = Path(__file__).resolve().parent
C = Counter()
def check(condition, label):
    assert condition, label
    C[label] += 1
def ident(a, b, label):
    check(S.simplify(S.cancel(a-b)) == 0, label)

# Bind every reconstructed blob, and all historical/final author manifests.
for row in json.loads((ROOT/'REMOTE_BINDINGS.json').read_text())['files']:
    path = ROOT/'author'/row['path']
    data = path.read_bytes()
    check(len(data) == row['bytes'], 'remote_byte_length')
    check(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
          == row['git_blob_sha1'], 'remote_git_blob_identity')
for path in sorted((ROOT/'author').glob('*MANIFEST.json')):
    for entry in json.loads(path.read_text())['files']:
        data = (ROOT/'author'/entry['path']).read_bytes()
        check(len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()
              ==entry['sha256'], 'author_manifest_binding')
sources = json.loads((ROOT/'author/SOURCE_BINDING.json').read_text())['files']
for name, binding in sources.items():
    path = ROOT/'sources'/name
    if path.exists():
        data=path.read_bytes()
        check(len(data)==binding['bytes'] and hashlib.sha256(data).hexdigest()
              ==binding['sha256'], 'available_primary_source_binding')

# Independent scalar second-order recurrence from Cayley-Hamilton, rather
# than the author's three-state recurrence used for the Newton certificate.
z, t, r, x, a = S.symbols('z t r x a', positive=True)
N = S.Matrix([[1+2*z,z],[z+z*z,1+z]])
trace=2+3*z
determinant=1+3*z+z*z-z**3
check((N*N-trace*N+determinant*S.eye(2)).applyfunc(S.expand)==S.zeros(2), 'Cayley_Hamilton_matrix_identity')
u=S.Matrix([[2+z,2]]); v=S.Matrix([2,z])
ident((u*v)[0],4+4*z,'scalar_initial_0')
ident((u*N*v)[0],4+16*z+12*z*z+z**3,'scalar_initial_1')
def trim(p):
    while len(p)>1 and p[-1]==0:p.pop()
    return p
def add(p,q):
    out=[0]*max(len(p),len(q))
    for i,c in enumerate(p):out[i]+=c
    for i,c in enumerate(q):out[i]+=c
    return trim(out)
def mul(p,q):
    out=[0]*(len(p)+len(q)-1)
    for i,c in enumerate(p):
        for j,d in enumerate(q):out[i+j]+=c*d
    return trim(out)
rows=[[4,4],[4,16,12,1]]
for m in range(2,497):
    rows.append(add(mul([2,3],rows[-1]),mul([-1,-3,-1,1],rows[-2])))
for m,row in enumerate(rows):
    n=m+4;d=3*(n-1)//2
    check(len(row)+2==d,'scalar_degree')
    check(all(c>0 for c in row),'scalar_positive_support')
    check(sum(row)==(25*4**m-1)//3,'source_total_count')
    for j,c in enumerate(row[1:-1],1):
        k=j+3
        check(k*(d-k)*c*c >= (k+1)*(d-k+1)*row[j-1]*row[j+1],
              'scalar_finite_ULC')

def coefficient(row,j):return row[j] if 0<=j<len(row) else 0
def margin(row_parameter,parity,index,side):
    row=rows[2*row_parameter+parity];d=len(row)+2
    k=index+3 if side=='lower' else d-index
    get=lambda k:coefficient(row,k-3)
    return k*(d-k)*get(k)**2-(k+1)*(d-k+1)*get(k-1)*get(k+1)

# Recover all 200 vectors by the explicit binomial transform, not the
# author's iterative forward-difference implementation.
certificate=[]
for side,bound in [('lower',60),('upper',40)]:
    for index in range(1,bound+1):
        for parity in [0,1]:
            degree=2*index+1 if side=='lower' else 4*index+3-2*parity
            values=[margin(q,parity,index,side) for q in range(degree+1)]
            coeffs=[sum((-1)**(ell-q)*comb(ell,q)*values[q]
                        for q in range(ell+1)) for ell in range(degree+1)]
            for c in coeffs:check(c>=0,'independent_Newton_coefficient_nonnegative')
            first=next(q for q,c in enumerate(coeffs) if c)
            wanted=max(0,(index-2*parity+2)//3) if side=='lower' else max(0,(index-1-2*parity+2)//3)
            check(first==wanted,'independent_first_strict_row')
            check(coeffs[-1]>0,'independent_top_coefficient_positive')
            for q in [degree+3,degree+5,degree+9]:
                check(sum(c*comb(q,ell) for ell,c in enumerate(coeffs))
                      ==margin(q,parity,index,side),'independent_off_grid_interpolation')
            certificate.append(dict(side=side,index=index,parity=parity,
                                    degree_bound=degree,first_nonzero=first,coefficients=coeffs))
canonical=json.dumps(certificate,separators=(',',':'),sort_keys=True).encode()
digest=hashlib.sha256(canonical).hexdigest()
check(digest=='63f530185b41356c61167ba5cd16b5a3d1d70bb837cd4d8b86c9bb4b00e29e2b',
      'independent_full_Newton_certificate_hash')
if (ROOT/'NEWTON_CERTIFICATE.json').exists():
    check(canonical==(ROOT/'NEWTON_CERTIFICATE.json').read_bytes().rstrip(b'\n'),
          'independent_certificate_exact_byte_comparison')

# Perron formulas, using a CAS rational function implementation, distinct
# from the hand-written rational operations in the author checker.
Z=(t*t-5)/4; L=(t+1)*(t*t+2*t-7)/8
Dt=lambda f:S.cancel((t*t-5)/(2*t)*S.diff(f,t))
alpha=S.cancel(Dt(L)/L); variance=Dt(alpha)
W=t*t+2*t-7
p6=3*t**6+10*t**5+57*t**4-4*t**3-235*t*t+250*t+175
p4=9*t**4+36*t**3-42*t*t+100*t+105
ident(alpha,(t*t-5)*(3*t*t+6*t-5)/(2*t*(t+1)*W),'CAS_alpha')
ident(variance,(t*t-5)*p6/(4*t**3*(t+1)**2*W**2),'CAS_variance')
ident(alpha*(S.Rational(3,2)-alpha)-S.Rational(3,2)*variance,
      (t*t-5)**2*p4/(8*t**3*(t+1)**2*W**2),'CAS_variance_gap')
Pplus=(N-(1+S.Rational(3,2)*z-z*S.sqrt(5+4*z)/2)*S.eye(2))/(z*S.sqrt(5+4*z))
H=2*(1+z)+(z*z+6*z+6)/S.sqrt(5+4*z)
ident((u*Pplus*v)[0],H,'CAS_Perron_amplitude')
Lz=1+S.Rational(3,2)*z+z*S.sqrt(5+4*z)/2
az=S.cancel(z*S.diff(Lz,z)/Lz);sz=S.cancel(z*S.diff(az,z))
limit=S.limit(1/sz-1/az-1/(S.Rational(3,2)-az),z,0)
ident(limit,(3+7*S.sqrt(5))/(45+21*S.sqrt(5)),'CAS_lower_gap_limit')
check(limit>0,'CAS_lower_gap_limit_positive')

# Direct algebraic checks of the upper parity functions. Positive x is a
# legitimate algebraic branch near zero; the resulting identities of
# analytic functions then give the formal coefficient identities.
rad=S.sqrt(1+5*x*x/4)
Lu=rad+S.Rational(3,2)*x+x**3
E=2*x+2*x**3+(1+6*x*x+6*x**4)/(2*rad)
ident(S.simplify(x**3*Lz.subs(z,1/x**2)),Lu,'CAS_upper_eigenvalue_reversal')
ident(S.simplify(x**3*H.subs(z,1/x**2)),E,'CAS_upper_amplitude_reversal')
check(Lu.subs(x,0)==1 and S.diff(Lu**2,x).subs(x,0)==3 and E.subs(x,0)==S.Rational(1,2),
      'CAS_small_saddle_hypotheses')

# Independent combinatorial Gaussian correction expansion to second order.
# A term uses l amplitude derivatives and n_k copies of the k-th phase
# cumulant; its epsilon degree is l+sum((k-2)n_k).
nu=S.symbols('nu',positive=True)
h=S.symbols('h0:5');c=S.symbols('c0:7')
def gaussian(epsilon_degree):
    total=0
    import itertools
    for ell in range(5):
        for powers in itertools.product(range(5),repeat=4):
            if ell+sum((k-2)*powers[k-3] for k in range(3,7))!=epsilon_degree:continue
            ydegree=ell+sum(k*powers[k-3] for k in range(3,7))
            if ydegree%2:continue
            weight=h[ell]/factorial(ell)
            for k,power in zip(range(3,7),powers):
                weight*=c[k]**power/(factorial(k)**power*factorial(power))
            moment=S.factorial2(ydegree-1)/nu**(ydegree//2) if ydegree else 1
            total+=(-1)**(ydegree//2)*weight*moment
    return S.expand(total).subs(h[0],1)
B1=gaussian(2);B2=gaussian(4)
ident(B1,-h[2]/(2*nu)+h[1]*c[3]/(2*nu**2)+c[4]/(8*nu**2)-5*c[3]**2/(24*nu**3),
      'independent_first_Gaussian_correction')
poisson={nu:1,**{h[i]:0 for i in range(1,5)},**{c[i]:1 for i in range(3,7)}}
check(B1.subs(poisson)==-S.Rational(1,12),'independent_Poisson_B1')
check(B2.subs(poisson)==S.Rational(1,288),'independent_Poisson_B2')
check(all(S.denom(term).free_symbols <= {nu} for term in S.Add.make_args(B2)),
      'second_correction_only_positive_variance_denominators')
(ROOT/'GAUSSIAN_SECOND_CORRECTION.txt').write_text(str(B2)+'\n')
shift=S.series(S.log(1+4*x)-S.log(1+3*x),x,0,3).removeO()
ident(shift,x-S.Rational(7,2)*x*x,'CAS_original_monomial_shift')

# A second implementation of exact real-root counting, without importing
# the author's Sturm code or numeric root approximations.
P=S.Poly(sum(q*z**i for i,q in enumerate(rows[3])),z)
check(P.as_expr()==4+40*z+132*z*z+195*z**3+129*z**4+32*z**5+z**6,
      'CAS_Sturm_source_polynomial')
check(P.count_roots(-S.oo,0)==4,'CAS_four_negative_real_roots')
check(P.count_roots(0,S.oo)==0,'CAS_no_nonnegative_real_roots')
check(S.gcd(P,P.diff()).degree()==0,'CAS_no_multiple_roots')

result={'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),
        'independent_certificate_sha256':digest,'finite_rows':[4,500],
        'scope':'Independent exact controls of frozen claims; analytic estimates are separately audited. No effective threshold or full all-n ULC assertion.'}
print(json.dumps(result,indent=2,sort_keys=True))
