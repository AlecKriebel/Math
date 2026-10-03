#!/usr/bin/env python3
"""Exact algebra and independent Gaussian/Laguerre checks (not a proof)."""
import json
from pathlib import Path
import sympy as s
import mpmath as mp
X,c,z=s.symbols('X c z', nonzero=True)
A=2*X**2+2*c*X/z+c**2/z**2
B=-3*c*X**2-3*c**2*X/z-c**3/z**2
# Replace pi*i*c by 6 before simplifying.
identity=s.simplify(A/s.Integer(24)+(6/c)/s.Integer(216)*B-c**2/(72*z**2))
assert identity==0
magic=s.Rational(1,12)+s.Rational(-21,5)/216+(-72)*s.Rational(-1,120)/216
assert magic==s.Rational(1,15)
# Coefficients at q^0 and q^1: E2^2=(1,-48,...), E2^3=(1,-72,...).
N=160
sig=[0]*(N+1)
for j in range(1,N+1):
 for k in range(j,N+1,j): sig[k]+=j
e=[1]+[-24*v for v in sig[1:]]
def conv(a,b): return [sum(a[j]*b[n-j] for j in range(n+1)) for n in range(N+1)]
a=conv(e,e); b=conv(a,e)
mp.mp.dps=65
rows=[]
for t in map(mp.mpf,['0.45','0.8','1','1.7','2.2']):
 # f(r)=e^{-pi t r^2}; Fourier_8 f=t^{-4} e^{-pi r^2/t}.
 total=mp.mpf('0')
 for n in range(N+1):
  f=mp.exp(-2*mp.pi*t*n); h=t**-4*mp.exp(-2*mp.pi*n/t)
  total+=a[n]*(f+h)/24+b[n]*(-2*mp.pi)*(t*f+h/t)/432
 target=1/(2*mp.pi**2*t**2)
 error=abs(total-target)
 assert error<mp.mpf('1e-55')
 rows.append({'t':str(t),'error':str(error)})
# Radial oscillator modes: L_k^3(2*pi*r^2)e^{-pi*r^2}; Fourier eigenvalue (-1)^k.
u=s.symbols('u')
laguerre=[]
for k in range(9):
 p=s.assoc_laguerre(k,3,u); dp=s.diff(p,u)
 P=s.lambdify(u,p,'mpmath'); DP=s.lambdify(u,dp,'mpmath')
 total=mp.mpf('0')
 for n in range(N+1):
  x=4*mp.pi*n; exp=mp.exp(-2*mp.pi*n)
  f=P(x)*exp
  dr_over_r=(4*mp.pi*DP(x)-2*mp.pi*P(x))*exp
  total+=(1+(-1)**k)*(a[n]*f/24+b[n]*dr_over_r/432)
 poly=s.Poly(p,u)
 target=sum(mp.mpf(str(v))*2**j*mp.factorial(j+1)/(2*mp.pi**2) for (j,),v in poly.terms())
 error=abs(total-target)
 assert error<mp.mpf('1e-48')
 laguerre.append({'k':k,'error':str(error)})
# Direct Leech first-derivative ansatz identity fails already in the y^2 coefficient.
y=s.symbols('y')
B=s.Function('B')
pure=s.expand(7*(X**6+(X+y)**6)-2*((X+y)**7-X**7)/y)
# This normalization cancels y^0 and y^1; y^2 coefficient is 35 X^4.
assert s.expand(pure).coeff(y,2)==35*X**4
# Weight-eight modular lift: exact Leech weighted-tail value.
leech=(1+432*s.Rational(1,156))/12+(s.Rational(-3587,910)+408*s.Rational(-107,2730)+28872*s.Rational(-1,65520))/216
assert leech==s.Rational(20,91)
# Gaussian checks in dimension 24 for H=E4^2.
sig3=[0]*(N+1)
for j in range(1,N+1):
 for n in range(j,N+1,j): sig3[n]+=j**3
E4=[1]+[240*v for v in sig3[1:]]
H=conv(E4,E4); aa=conv(H,a); bb=conv(H,b)
leech_rows=[]
for t in map(mp.mpf,['0.6','1','1.8']):
 total=mp.mpf('0')
 for n in range(N+1):
  f=mp.exp(-2*mp.pi*t*n); h=t**-12*mp.exp(-2*mp.pi*n/t)
  total+=aa[n]*(f+h)/24+bb[n]*(-2*mp.pi)*(t*f+h/t)/432
 target=sum(H[n]*mp.exp(-2*mp.pi*t*n) for n in range(N+1))/(2*mp.pi**2*t**2)
 error=abs(total-target)
 assert error<mp.mpf('1e-50')
 leech_rows.append({'t':str(t),'error':str(error)})
out={'exact_e8_value':str(magic),'quasimodular_identity_zero':str(identity),'gaussian_tests':rows,'radial_laguerre_tests':laguerre,'direct_leech_ansatz_residual':str(pure),'leech_weighted_tail_value':str(leech),'leech_lift_gaussian_tests':leech_rows,'truncation_n':N,'working_decimal_digits':mp.mp.dps,'caveat':'Floating-point checks are diagnostics; the proof is symbolic and functional-analytic.'}
Path(__file__).with_name('exact_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
