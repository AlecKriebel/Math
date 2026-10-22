#!/usr/bin/env python3
"""Independent finite controls, not a formal verification of the analytic proof."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import scipy.integrate as integrate
import sympy as sp

AUDIT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--manuscript", type=Path, default=AUDIT.parent / "harmonic_spheres_30006419" / "public")
parser.add_argument("--sources", type=Path, default=AUDIT / "sources", help="Directory containing freshly retrieved source PDFs")
parser.add_argument("--output", type=Path, default=AUDIT / "checks" / "results.json")
args = parser.parse_args()
AUTHOR = args.manuscript.resolve()
checks = []


def require(name, condition, detail=None):
    ok = bool(condition)
    checks.append({"name": name, "passed": ok, "detail": detail})
    if not ok:
        raise RuntimeError(f"Check failed: {name}: {detail}")


expected = {
    "PROOF.md": "2634e714b9a06a1770ae39b0201031c7d2a7ce6e97f3330f8745d0e2453d4fef",
    "KOREVAAR_SCHOEN.md": "4bac91a7e34b266391051d48ae2ef10adc60d10b6ed0d57d1c5cb8395e2a6abe",
    "MANIFEST.json": "9cb1f5c242224d4f04a34b1d28e660a29fb2f63d47215d16257f5d4073c001cb",
}
for name, digest in expected.items():
    require("frozen_" + name, hashlib.sha256((AUTHOR / name).read_bytes()).hexdigest() == digest)
manifest = json.loads((AUTHOR / "MANIFEST.json").read_text())
for name, entry in manifest["files"].items():
    data = (AUTHOR / name).read_bytes()
    require("manifest_" + name, len(data) == entry["bytes"] and hashlib.sha256(data).hexdigest() == entry["sha256"])

source_expected = {
    "meier_vikman_wenger_v1.pdf": (366176, "23c2b27bf9a39649cea4dc820815c73cb983224488f66de2ccdfe0fc9254dc28"),
    "owr_2025_30.pdf": (565665, "ca3edd8679e6fcc0c95d934b031eaf398d0d4d2b3d0038a38358c2d15b362801"),
}
for name, (size, digest) in source_expected.items():
    data = (args.sources / name).read_bytes()
    require("independently_retrieved_" + name, len(data) == size and hashlib.sha256(data).hexdigest() == digest)


def H(x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    # Equivalent to B(x)/(B(x)+B(1-x)), with stable arithmetic.
    delta = 1 / x - 1 / (1 - x)
    if delta > 700:
        return 0.0
    if delta < -700:
        return 1.0
    return 1 / (1 + math.exp(delta))


def a(t):
    eta = 1 - H((16 * t * t - 1) / 3)
    return eta * t * t + 1 - eta


c = integrate.quad(lambda t: 1 - a(t), 0, 0.5, points=[0.25], epsabs=1e-12)[0]


def h(t):
    if abs(t) >= 0.5:
        return t - math.copysign(c, t)
    if abs(t) <= 0.25:
        return t**3 / 3
    return math.copysign(integrate.quad(a, 0, abs(t), points=[0.25], epsabs=1e-12)[0], t)


def rho(s):
    return math.exp(-abs(s) * H(abs(s) - 2))


require("compression_constant_positive_below_half", 0 < c < 0.5, c)
grid = np.linspace(-6, 6, 6001)
require("sampled_a_bounds", all(0 <= a(t) <= 1 for t in grid))
require("sampled_even_a", max(abs(a(t) - a(-t)) for t in grid) == 0)
require("sampled_zero_only_equator", all(a(t) > 0 for t in grid if t != 0))
require("central_polynomial", all(abs(a(t) - t*t) < 1e-15 and h(t) == t**3/3 for t in np.linspace(-0.25, 0.25, 101)))
require("outside_half_linear", all(a(t) == 1 and abs(h(t) - (t - math.copysign(c,t))) < 1e-15 for t in grid if abs(t) >= 0.5))
require("target_flat_belt", all(rho(t) == 1 for t in np.linspace(-2, 2, 101)))
require("pole_metric_exponential", all(abs(rho(t) - math.exp(-abs(t))) < 1e-15 for t in grid if abs(t) >= 3))
require("sampled_h_strict_increase", all(h(t) < h(t+0.002) for t in np.linspace(-2, 1.998, 2000)))
require("sampled_h_compression", all(abs(h(t)) <= abs(t)+1e-14 for t in np.linspace(-2, 2, 1001)))
require("negative_pole_scaling", abs(math.exp(h(-5)) / math.exp(-5) - math.exp(c)) < 1e-14)
require("positive_pole_scaling", abs(math.exp(-h(5)) / math.exp(-5) - math.exp(c)) < 1e-14)

area = 2*math.pi*(4 + 2*integrate.quad(lambda s: rho(s)**2, 2, 3, epsabs=1e-12)[0] + math.exp(-6))
# Independent integration of the energy on source coordinates, including exact tails.
energy = 4*math.pi*(integrate.quad(lambda t: rho(h(t))**2, 0, 3+c,
                                 points=[0.25, 0.5, 2+c], epsabs=1e-11)[0] + math.exp(-6)/2)
require("global_energy_gap", abs((energy-area)-4*math.pi*c) < 1e-10,
        {"area":area,"energy":energy,"gap":energy-area,"four_pi_c":4*math.pi*c})
for Q in [1, 2, 10, 100, 10000, 10**9]:
    delta = min(0.25, 1/(2*math.sqrt(Q)))
    t = delta/2
    require("positive_measure_distortion_"+str(Q), 1/t**2 > Q and 4*math.pi*math.tanh(delta) > 0,
            {"witness_t":t,"distortion":1/t**2,"band_round_area":4*math.pi*math.tanh(delta)})

# The full-cylinder angular coordinate would be an invalid substitute for a convex patch.
seam_epsilon = 0.01
require("negative_control_global_angle_fails", 2*math.pi-2*seam_epsilon > 2*seam_epsilon)

rng = np.random.default_rng(30006419)
for k in range(300):
    A = rng.normal(size=(2,2))
    op2 = np.linalg.norm(A,ord=2)**2
    ell = rng.normal(size=2)
    ell /= max(1,np.linalg.norm(ell))
    coeff = rng.uniform(-1,1)
    require(f"scalar_calibration_matrix_{k}", np.linalg.norm(ell@A)**2 <= op2+1e-12)
    require(f"two_form_calibration_matrix_{k}", coeff*np.linalg.det(A) <= op2+1e-12)

for m in [0.01,0.1,0.49]:
    b = m/(1-m)
    require("cap_cutoff_comass_"+str(m), -1 < -b <= 0 and abs((1+b)*1-b-1)<1e-14)
    require("cap_cutoff_zero_integral_"+str(m), abs((1+b)*m-b) < 1e-14)

# Exact KS first variation with a nonnegative compactly supported W^{1,2}_0 test.
# Its zero extension is C^1; smooth nonnegative tests follow by approximation.
t,x = sp.symbols("t x", real=True)
ta,tb = sp.Rational(1,16),sp.Rational(1,8)
psi = (t-ta)**2*(tb-t)**2*x**2*(1-x)**2
first = sp.integrate(2*t*t*sp.diff(psi,t),(x,0,1),(t,ta,tb))
parts = -4*sp.integrate(t*psi,(x,0,1),(t,ta,tb))
second = sp.integrate(sp.diff(psi,t)**2+sp.diff(psi,x)**2,(x,0,1),(t,ta,tb))
require("exact_KS_negative_first_variation", first == parts and first < 0, str(first))
eps = -first/(2*second)
target_upper = tb**3/3 + eps*(tb-ta)**4/256
require("exact_KS_energy_decrease", eps*first+eps**2*second < 0 and target_upper < 2,
        {"epsilon":str(eps),"decrement":str(eps*first+eps**2*second),"target_coordinate_upper_bound":str(target_upper)})

# Separately audit the angular KS stress formulas, including nonsmooth norms.
N=65536
theta = 2*np.pi*np.arange(N)/N
W = np.column_stack([np.cos(theta),np.sin(theta)])
kernel = 4*np.einsum("ni,nj->nij",W,W)-2*np.eye(2)
norms = {
    "ellipsoid": lambda V: np.sqrt(3*V[:,0]**2 + 0.4*V[:,0]*V[:,1] + 0.7*V[:,1]**2),
    "l1": lambda V: np.abs(V[:,0])+np.abs(V[:,1]),
    "linf": lambda V: np.maximum(np.abs(V[:,0]),np.abs(V[:,1])),
    "rank_one": lambda V: 1.3*np.abs(V[:,0]),
}
Bmat = np.array([[.3,-.2],[.5,-.4]])
Amat = np.array([[1.2,.17],[-.13,.8]])
angle=.413
R=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
errors={}
for name, norm in norms.items():
    s2=norm(W)**2
    T=2*np.mean(s2[:,None,None]*kernel,axis=0)
    require("stress_tracefree_"+name, abs(np.trace(T)) < 1e-12)
    def F(A):
        return 2*np.mean(norm(W@A.T)**2)/np.linalg.det(A)
    lhs=F(Amat)
    Ainv=np.linalg.inv(Amat)
    rhs=2*np.mean(s2/np.sum((W@Ainv.T)**2,axis=1)**2)/np.linalg.det(Amat)**2
    derivative=(F(np.eye(2)+1e-5*Bmat)-F(np.eye(2)-1e-5*Bmat))/(2e-5)
    predicted=np.sum(T*Bmat)
    rotated=2*np.mean(norm(W@R.T)[:,None,None]**2*kernel,axis=0)
    errors[name]={"angular_change_error":abs(lhs-rhs),"derivative_error":abs(derivative-predicted),
                  "rotation_error":float(np.max(np.abs(rotated-R.T@T@R)))}
    require("angular_change_"+name, abs(lhs-rhs)<5e-8, errors[name]["angular_change_error"])
    require("stress_derivative_"+name, abs(derivative-predicted)<5e-5, errors[name]["derivative_error"])
    require("stress_rotation_"+name, np.max(np.abs(rotated-R.T@T@R))<5e-8, errors[name]["rotation_error"])
    if name in ["l1","linf"]:
        require("nonround_balanced_"+name,np.linalg.norm(T)<1e-12 and abs(norm(np.array([[1,0]]))[0]-norm(np.array([[2**-.5,2**-.5]]))[0])>.1)
    if name=="rank_one":
        require("rank_one_nonzero_stress",np.max(np.abs(T-1.3**2*np.diag([1,-1])))<1e-12)
    if name=="ellipsoid":
        G=np.array([[3,.2],[.2,.7]])
        require("inner_product_stress",np.max(np.abs(T-(2*G-np.trace(G)*np.eye(2))))<1e-12)

m=sp.sqrt(17)-4
require("seminorm_bound_root",sp.simplify(m*m+8*m-1)==0 and bool(m>0))
require("seminorm_bound_reciprocal",sp.simplify(1/m-(4+sp.sqrt(17)))==0)
for small in [.001,.01,.1,.2,.5,1]:
    s=np.sqrt(W[:,0]**2+small**2*W[:,1]**2)
    r=np.abs(W[:,0])
    Ts=2*np.mean(s[:,None,None]**2*kernel,axis=0)
    Tr=np.diag([1.,-1.])
    require("sampled_seminorm_pointwise_"+str(small), np.max(np.abs(s-r))<=small+1e-12)
    require("sampled_seminorm_stress_bound_"+str(small),np.linalg.norm(Ts-Tr,ord=2)<=8*small+1e-12)

result={"status":"PASS","checks":len(checks),"failed":0,"c":c,"ks_stress_errors":errors,
        "limitations":"Finite checks support algebra, source identity, and negative controls. They do not verify Sobolev calculus, de Rham exactness, or the complete analytic proof.",
        "results":checks}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:result[k] for k in ["status","checks","failed","c","ks_stress_errors","limitations"]},indent=2))
