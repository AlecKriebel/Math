"""Independent diagnostic for an adaptive Fisher-information identity.
Requires mpmath. All integral values below are divided by conserved mass.
The analytic derivation is in ADVERSARIAL_REVIEW.md; this is not a proof checker.
"""
import json
import mpmath as mp

mp.mp.dps = 60
d = 3
n = mp.mpf(4)
m = 1 - 1/n
q = d/(2*n)
a = 1-q
b = 2*q
h = a*(1-b)
A = [mp.mpf('0.5'), mp.mpf(1), mp.mpf(2)]
C = mp.fprod(A)**(-1/(2*n-d))
sigma = C*sum(1/x for x in A)/d
eta = sigma**a
L = [2*(eta*x-1) for x in A]
trL = sum(L)
Cp = trL*C/n
Ap = [(trL/n-2*li)*ai for li,ai in zip(L,A)]
sigmap = (Cp*sum(1/x for x in A)-C*sum(dx/x**2 for x,dx in zip(A,Ap)))/d
etap = a*eta*sigmap/sigma
H = n-1-mp.mpf(d)/2
entropy = C*(n-1)/H
f = n*(n-1)*(sigma**q-C)/H
Q = sum(li**2/ai for li,ai in zip(L,A))
Qp = 4*(2*eta*etap*sum(A)+eta**2*sum(Ap)-2*d*etap-sum(dx/x**2 for x,dx in zip(A,Ap)))
prefactor = (n-1)/(2*n-d-2)
j = prefactor*C*Q/eta
jp = prefactor*((Cp/eta-C*etap/eta**2)*Q+C*Qp/eta)
R = 2*entropy*(sum(li**2 for li in L)-trL**2/n)
lhs = jp+4*j
corrected = a*sigmap/sigma*(j-4*b*f)-R
printed = b*(j-4*f)*sigmap/sigma+h*j*sigmap/sigma-sigma**(2*a)*R
fp = n*(n-1)/H*(q*sigma**(q-1)*sigmap-Cp)
# Explicit exceptions keep this diagnostic active under python -O.
if abs(lhs-corrected) > mp.mpf('1e-55'):
    raise RuntimeError('Corrected identity diagnostic failed')
if abs(fp+j) > mp.mpf('1e-55'):
    raise RuntimeError('Independent entropy dissipation diagnostic failed')
if abs(lhs-printed) < 1:
    raise RuntimeError('Example did not separate the printed identity')
print(json.dumps({
    'method': 'analytic derivatives of explicit anisotropic-profile integrals',
    'precision_digits': mp.mp.dps,
    'dimension': d,
    'm': str(m),
    'sigma': mp.nstr(sigma, 40),
    'lhs_per_mass': mp.nstr(lhs, 40),
    'corrected_rhs_per_mass': mp.nstr(corrected, 40),
    'corrected_residual': mp.nstr(lhs-corrected, 8),
    'printed_rhs_per_mass': mp.nstr(printed, 40),
    'printed_residual_per_mass': mp.nstr(lhs-printed, 40),
    'entropy_dissipation_residual': mp.nstr(fp+j, 8),
}, indent=2))
