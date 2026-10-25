"""Bounded check of the EXISTING regular-sector proof; no debt-bound repair."""
from pathlib import Path
import json,hashlib,datetime
import sympy as s

n,k,q,u=s.symbols('n k q u',positive=True)
two=s.Integer(2)
Q=lambda j:4*j*(j-1)*(n-j)*(n-j-1)/(n*(n-1)*(n-2)*(n-3))
O=lambda j:2*j*(n-j)*(n-j-1)/(n*(n-1)*(n-2))
I=lambda j:2*j*(j-1)*(n-j)/(n*(n-1)*(n-2))
# rho is suppressed throughout this symbolic sign comparison, exactly as in
# the published verifier. u=2^k and q=2^(k-n) retain all other scaling.
w=lambda shift:(n+k+shift-2*n*q*two**shift)/((k+shift)*(n-k-shift))
p=lambda j:2*(n-1)**2/(n-1+j)**2
r=lambda j:2*(n-1)**2/(n+j-2)**2
d=lambda shift:(n+k+shift-1)/((n-1)*u*two**shift)
ell=2*(w(0)*(p(k)+r(k))*Q(k)+w(-1)*p(k-1)*(-Q(k-1)+2*O(k-1))+w(1)*r(k+1)*(-Q(k+1)+2*I(k+1)))
f=2*(n-1)*(n+k)/(u*(n+k-1)*(n+k-2))
bar=s.Rational(21,20)*(n+k)/(4*n-2*k)*f
j=k-1
direct=w(-1)*(4*(n-1)**3*d(-1)*O(j)/(n-1+j)**3+4*(n-1)**3*d(-2)*I(j)/(n+j-2)**3)
C=j**3+3*j*j*n-3*j*j+3*j*n*n-10*j*n+6*j+n**3-7*n*n+12*n-6
A=k*n-3*k+n*n-3*n+3
B=k*k+2*k*n-6*k+n*n-4*n+5
H=20*(n+k-1-n*q)*C*(2*n-k)*(n-3)*(n+k-1)**2-21*n*(n-1)*(n+k)**2*(A-q*B)*(n+k-3)**2
factor=4*(n-1)/(5*n*u*(2*n-k)*(n-3)*(n-2)*(k+n-3)**2*(k+n-2)**2*(k+n-1)**2)
assert s.factor(direct-ell*bar-factor*H)==0

a,b,c=s.symbols('a b c',nonnegative=True,integer=True)
shifted=s.expand(H.subs({n:a+b+4,k:a+2}))
certificate=[]
for bv in range(5):
    poly=s.Poly(s.expand(shifted.subs({b:bv,a:c+5-bv,q:s.Rational(1,2**(bv+2))})),c)
    assert poly.degree()==8 and len(poly.coeffs())==9
    assert min(poly.coeffs())==(784,696,652,630,619)[bv]
    certificate.append({'b':bv,'terms':len(poly.coeffs()),'minimum_coefficient':str(min(poly.coeffs()))})
H0=s.Poly(shifted,q).coeff_monomial(1);H1=s.Poly(shifted,q).coeff_monomial(q)
assert s.expand(shifted-H0-q*H1)==0
for label,expr,expected in [('H0',H0,19),('128H0+H1',128*H0+H1,2413)]:
    poly=s.Poly(s.expand(expr.subs(b,c+5)),a,c)
    assert len(poly.terms())==45 and min(poly.coeffs())==expected
    certificate.append({'label':label,'terms':45,'minimum_coefficient':str(min(poly.coeffs()))})

# Reconstruct the existing supersolution residual from its actual killed
# forward cut-chain operator. Omitted boundary coefficients are zero.
nn=a+b+4;kk=a+2
up=lambda z:2*z/(nn-1+z)
down=lambda z:(nn-z)/(nn+z-2)
forcing=lambda z:2*(nn-1)*(nn+z)/(two**z*(nn+z-1)*(nn+z-2))
barrier=lambda z:s.Rational(21,20)*(nn+z)/(4*nn-2*z)*forcing(z)
residual=s.factor((up(kk)*(nn-kk)+down(kk)*kk)*barrier(kk)-up(kk)*(nn-kk-2)*barrier(kk+1)-down(kk)*(kk-2)*barrier(kk-1)-forcing(kk))
num,den=s.fraction(residual)
poly=s.Poly(s.cancel(num/(a+b+3)),a,b)
assert len(poly.terms())==45 and min(poly.coeffs())==16
assert s.factor(den/(80*two**a*(a+2*b+5)*(a+2*b+6)*(a+2*b+7)*(2*a+b+3)*(2*a+b+4)**2*(2*a+b+5)**2*(2*a+b+6)))==1

# Exact conversion connects this regular symmetric-sector result to the same
# inverse-mean eigenvalue used in the paper. ||Delta||_F^2=2 E.
conversion={}
for order,eigenvalue,expected in [(4,s.Rational(3,208),-s.Rational(27,637)),(5,s.Rational(359,26660),-s.Rational(367616,7498125))]:
    rho=s.Rational((order-1)*2**(order-2),order*(2**(order-1)-1))
    value=-4*order*rho*rho*eigenvalue
    assert value==expected
    conversion[str(order)]=str(value)

finite_ratios={}
for order,expected in [(6,s.Rational(265019,275520)),(7,s.Rational(32970550983,36455056000)),(8,s.Rational(383371803381,446439422000))]:
    def at(expr,rank):
        return s.cancel(expr.subs({n:order,k:rank,u:two**rank,q:two**(rank-order)}))
    # direct above is D_(k-1), so use k=2,...,n to include all n-1 terms.
    direct_sum=sum(at(direct,rank) for rank in range(2,order+1))
    response_bound=sum(at(ell*bar,rank) for rank in range(2,order-1))
    ratio=s.cancel(response_bound/direct_sum)
    assert ratio==expected and ratio<1
    finite_ratios[str(order)]=str(ratio)

out={'status':'EXISTING_ALTERNATIVE_SYMMETRIC_PROOF_SUPPORTED',
     'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'direct_comparison_factor':str(factor),
     'factor_domain':'strictly positive for n>=9, 2<=k<=n-2, u=2^k>0',
     'supersolution_positive_polynomial_terms':45,'supersolution_min_coefficient':16,
     'existing_tail_certificates':certificate,'curvature_normalization':conversion,
     'finite_closure_ratios':finite_ratios,
     'scope':'This validates an existing separate forward-subset proof of the same symmetric-balanced curvature sign. It does not establish A.31 or repair false support Eq. (35).',
     'replay':'No new broad replay; the advertised regular-sector verifier already completed in the captured earlier package run.'}
Path(__file__).with_name('alternative_scope_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
