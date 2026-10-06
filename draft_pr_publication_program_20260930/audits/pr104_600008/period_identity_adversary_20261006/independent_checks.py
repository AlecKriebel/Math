#!/usr/bin/env python3
"""Independent diagnostic checks. Numerical results do not replace the proof."""
import json
import platform
from datetime import datetime, timezone

import mpmath as mp
import sympy as sp

print(json.dumps({"started_utc": datetime.now(timezone.utc).isoformat(),
                  "python": platform.python_version(),
                  "sympy": sp.__version__, "mpmath": mp.__version__}))

# Direct coordinate differentiation, with h=sin(t)^2. No imported verifier.
a, b, c, v, h = sp.symbols("a b c v h", positive=True)
D = (a+c)*(b+c)
F = a*h+b*(1-h)
gtt = a*(a+v)*h/(a+c)+b*(b+v)*(1-h)/(b+c)-c*(c-v)*(a-b)**2*h*(1-h)/(D*(c+F))
gvv = a*(1-h)/(4*(a+c)*(a+v))+b*h/(4*(b+c)*(b+v))-c*(c+F)/(4*D*(c-v))
# g_tv is sin(t)cos(t) times this coefficient.
gtv_coefficient = -a/(2*(a+c))+b/(2*(b+c))+c*(a-b)/(2*D)
ellipsoid = (a+v)*(1-h)/(a+c)+(b+v)*h/(b+c)+(c+F)*(c-v)/D
checks = {
    "ellipsoid": sp.factor(ellipsoid-1),
    "gtt": sp.factor(gtt-(v+F)*F/(c+F)),
    "gvv": sp.factor(gvv+(v+F)*v/(4*(a+v)*(b+v)*(c-v))),
    "gtv": sp.factor(gtv_coefficient),
}
assert all(x == 0 for x in checks.values()), checks
print(json.dumps({"symbolic_metric_residuals": {k: str(x) for k,x in checks.items()}}))

q = sp.symbols("q", positive=True)
residues = [sp.simplify(-q/(2*sheet*sp.I*q)) for sheet in [1,-1]]
assert residues == [sp.I/2,-sp.I/2]
print(json.dumps({"quartic_dS_residues_at_infinity": [str(x) for x in residues]}))

mp.mp.dps = 70
partition = [mp.mpf(0), mp.pi/16, mp.pi/8, mp.pi/4,
             3*mp.pi/8, 7*mp.pi/16, mp.pi/2]

def periods(aa, bb, cc):
    aa,bb,cc = map(mp.mpf,(aa,bb,cc))
    # Iu uses the smooth trig pullback; at a=b this is the limiting period.
    iu = 2*mp.quad(lambda t: mp.sqrt((aa*mp.sin(t)**2+bb*mp.cos(t)**2)/
                                   (cc+aa*mp.sin(t)**2+bb*mp.cos(t)**2)), partition)
    # Independently evaluate Iv under v=c sin(theta)^2.
    iv = mp.quad(lambda t: 2*cc*mp.sin(t)**2/
                          mp.sqrt((aa+cc*mp.sin(t)**2)*(bb+cc*mp.sin(t)**2)), partition)
    return iu,iv

cases = [(5,2,7),(2,5,7),(1,1,3),(1,1,mp.mpf("1e-12")),
         (1,1,mp.mpf("1e12")),(mp.mpf("1.000000000001"),1,3),
         (mp.mpf("1e8"),1,mp.mpf("1e4")),
         (mp.mpf("1e-8"),1,mp.mpf("1e-4")),
         (5,2,mp.mpf("1e-10")),(5,2,mp.mpf("1e10"))]
max_error = mp.mpf(0)
for case in cases:
    iu,iv = periods(*case)
    error = abs(iu+iv-mp.pi)
    max_error=max(max_error,error)
    assert error < mp.mpf("1e-55"), (case,error)
    rho1 = iv/(2*iu)
    rho2 = (mp.pi-iu)/(2*iu)
    assert abs(rho1-rho2) < mp.mpf("1e-49")
    print(json.dumps({"axes": [str(x) for x in case],
                      "Iu": mp.nstr(iu,30), "Iv": mp.nstr(iv,30),
                      "period_sum_minus_pi": mp.nstr(iu+iv-mp.pi,8),
                      "rho": mp.nstr(rho1,30)}))

# Canonical square-root branch as the product of paired principal roots.
aa,bb,cc = map(mp.mpf,(5,2,7))
def R(z):
    return mp.sqrt(z+aa)*mp.sqrt(z+bb)*mp.sqrt(z)*mp.sqrt(z-cc)
for x in [-(aa+bb)/2,cc/2]:
    eps = mp.mpf("1e-25")
    positive_integrand = mp.sqrt(x/((aa+x)*(bb+x)*(cc-x)))
    quotient = (x+1j*eps)/R(x+1j*eps)/positive_integrand
    assert abs(quotient+1j)<mp.mpf("1e-23")
    print(json.dumps({"upper_bank_x": str(x), "normalized_z_over_R": str(quotient)}))

# A large circle: trapezoidal rule converges exponentially because the
# branch points lie inside, away from this contour.
radius=mp.mpf(50)
N=512
integral=sum((lambda z: z/R(z)*(1j*z))
             (radius*mp.exp(2j*mp.pi*k/N)) for k in range(N))*2*mp.pi/N
assert abs(integral-2j*mp.pi)<mp.mpf("1e-55")
print(json.dumps({"outer_circle_radius":str(radius),"nodes":N,
                  "integral":str(integral),
                  "error_from_2pi_i":mp.nstr(abs(integral-2j*mp.pi),8)}))

# Degeneration at a=b=A, evaluated independently from the v integral.
A,C = mp.mpf(3),mp.mpf(11)
iu,iv=periods(A,A,C)
mu=mp.sqrt(A/(A+C))
assert abs(iu-mp.pi*mu)<mp.mpf("1e-55")
assert abs(iv-mp.pi*(1-mu))<mp.mpf("1e-55")
print(json.dumps({"degenerate_axes":[str(A),str(A),str(C)],
                  "emerging_pole_residue":mp.nstr(mu,30),
                  "limiting_Iu":mp.nstr(iu,30),
                  "direct_Iv":mp.nstr(iv,30)}))

# Scale, swap, monotonicity, and strict c bounds at one nontrivial target.
iu,iv=periods(5,2,7)
for scaled in [(500,200,700),(mp.mpf("5e-20"),mp.mpf("2e-20"),mp.mpf("7e-20"))]:
    j,k=periods(*scaled)
    assert abs(j-iu)+abs(k-iv)<mp.mpf("1e-55")
swapped=periods(2,5,7)
assert abs(swapped[0]-iu)+abs(swapped[1]-iv)<mp.mpf("1e-55")
ms=[periods(5,2,x)[0]/mp.pi for x in [mp.mpf("1e-8"),1,7,100,mp.mpf("1e8")]]
assert all(ms[i]>ms[i+1] for i in range(len(ms)-1))

target=mp.mpf(3)/5 # n=3,r=1; rho=1/3
factor=1/target**2-1
lo,hi=2*factor,5*factor
# Bisection stays entirely inside the proven strict bounds.
left,right=lo,hi
for _ in range(120):
    middle=(left+right)/2
    if periods(5,2,middle)[0]/mp.pi>target:
        left=middle
    else:
        right=middle
root=(left+right)/2
assert lo<root<hi
root_mu=periods(5,2,root)[0]/mp.pi
print(json.dumps({"symmetries":"swap and scales 100,1e-20 verified",
                  "monotone_mu_samples":[mp.nstr(x,24) for x in ms],
                  "target_mu":str(target),"strict_c_bounds":[str(lo),str(hi)],
                  "bisection_c":mp.nstr(root,40),
                  "target_error":mp.nstr(abs(root_mu-target),8)}))

print(json.dumps({"status":"PASS", "maximum_period_identity_error":mp.nstr(max_error,10),
                  "finished_utc":datetime.now(timezone.utc).isoformat(),
                  "limitations":"Adaptive arbitrary-precision diagnostics, not certified interval quadrature; exact proof in REPORT.md."}))
