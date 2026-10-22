#!/usr/bin/env python3
"""Independent Cartesian algebra and diagnostic physical null-path integration.

The numerical checks supplement the analytic proof; they are not certificates
of the real period identity or of correctness for all parameters.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import math
import subprocess
import sys
import sympy as sy
import mpmath as mp

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parent.parent / "original_head"
COUNTS = Counter()


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    COUNTS[name] += 1


# Rational angular coordinate k=tan(t/2), differentiated directly in R^(2,1).
a, b, c, v, k = sy.symbols("a b c v k", positive=True)
co = (1-k*k)/(1+k*k)
si = 2*k/(1+k*k)
ff = sy.factor(a*si*si+b*co*co)
xyz = [sy.sqrt(a*(a+v)/(a+c))*co,
       sy.sqrt(b*(b+v)/(b+c))*si,
       sy.sqrt(c*(c+ff)*(c-v)/((a+c)*(b+c)))]


def inner(left, right):
    return sy.factor(left[0]*right[0]+left[1]*right[1]-left[2]*right[2])


dk = [sy.diff(q, k) for q in xyz]
dv = [sy.diff(q, v) for q in xyz]
check("cartesian_surface", sy.factor(xyz[0]**2/a+xyz[1]**2/b+xyz[2]**2/c-1) == 0)
check("cartesian_cross", inner(dk, dv) == 0)
check("cartesian_angular", sy.factor(inner(dk, dk)-(v+ff)*ff/(c+ff)*4/(1+k*k)**2) == 0)
check("cartesian_latitude", sy.factor(inner(dv, dv)+(v+ff)*v/(4*(a+v)*(b+v)*(c-v))) == 0)
check("cartesian_normal", sy.factor(xyz[0]**2/a**2+xyz[1]**2/b**2-xyz[2]**2/c**2-ff*v/(a*b*c)) == 0)

# Use a separate, ordinary ellipsoid chart (theta, q=z/sqrt(c)).
q = sy.symbols("q", real=True)
ordinary = [sy.sqrt(a)*sy.sqrt(1-q*q)*co,
            sy.sqrt(b)*sy.sqrt(1-q*q)*si, sy.sqrt(c)*q]
ok = [sy.diff(x, k)*(1+k*k)/2 for x in ordinary]
oq = [sy.diff(x, q) for x in ordinary]
E, B, G = inner(ok, ok), inner(ok, oq), inner(oq, oq)
check("ordinary_E", sy.factor(E-(1-q*q)*ff) == 0)
check("ordinary_B", sy.factor(B-(a-b)*q*si*co) == 0)
check("ordinary_G", sy.factor(G-q*q*(a*co*co+b*si*si)/(1-q*q)+c) == 0)
check("ordinary_discriminant", sy.factor(B*B-E*G-(c*ff-(c*ff+a*b)*q*q)) == 0)

# Boundary expansions independently control the two coordinate gluing claims.
eps = sy.symbols("eps", positive=True)
tau_at_zero = sy.sqrt(v/((a+v)*(b+v)*(c-v)))/2
check("tropic_derivative_order", sy.limit(tau_at_zero/sy.sqrt(v), v, 0) == 1/(2*sy.sqrt(a*b*c)))
tail_derivative = sy.sqrt((c-eps)/((a+c-eps)*(b+c-eps)*eps))/2
check("equator_derivative_order", sy.limit(tail_derivative*sy.sqrt(eps), eps, 0) == sy.sqrt(c)/sy.sqrt((a+c)*(b+c))/2)

# Regularized quadratures never evaluate a square-root endpoint singularity.
mp.mp.dps = 60
period_rows = []
samples = [(3, 1, 2), (1, 3, mp.mpf(".2")), (1, 1, 8),
           (9, mp.mpf(".3"), 2), (4, 1, 100),
           (mp.mpf("1e-8"), 1, mp.mpf("1e-10")),
           (mp.mpf("1e8"), 1, mp.mpf("1e10"))]
for aa, bb, cc in samples:
    aa, bb, cc = map(mp.mpf, (aa, bb, cc))
    quarter = mp.quad(lambda s: mp.sqrt((aa*mp.sin(s)**2+bb*mp.cos(s)**2)/
                         (cc+aa*mp.sin(s)**2+bb*mp.cos(s)**2)),
                      [0, mp.pi/4, mp.pi/2])
    # Distinct regularization and integrand from the angular integral.
    iv = mp.quad(lambda s: 2*cc*mp.sin(s)**2 /
                 mp.sqrt((aa+cc*mp.sin(s)**2)*(bb+cc*mp.sin(s)**2)),
                 [0, mp.pi/4, mp.pi/2])
    error = abs(2*quarter+iv-mp.pi)
    check("diagnostic_period_identity", error < mp.mpf("1e-45"))
    check("diagnostic_rotation_positive", 0 < iv/(4*quarter))
    period_rows.append({"a": str(aa), "b": str(bb), "c": str(cc),
                        "error": str(error), "rotation": str(iv/(4*quarter))})


def rk4(fun, x, y, step):
    j1 = fun(x, y)
    j2 = fun(x+step/2, y+step*j1/2)
    j3 = fun(x+step/2, y+step*j2/2)
    j4 = fun(x+step, y+step*j3)
    return y+step*(j1+2*j2+2*j3+j4)/6


def physical_passage(aa, bb, cc, start, maxstep):
    """Integrate the two null roots in the ordinary ellipsoid chart.

    Integrator does not use the proposed v, S, Y coordinates or rotation formula.
    We stop close to the degenerate metric then switch roots. The distance to
    the tropic and a local slope bound choose safe adaptive q steps.
    """
    def tropic(theta):
        f = aa*math.sin(theta)**2+bb*math.cos(theta)**2
        return math.sqrt(cc*f/(aa*bb+cc*f))

    def rhs(sign):
        def f(q, theta):
            ss, ct = math.sin(theta), math.cos(theta)
            ff = aa*ss*ss+bb*ct*ct
            ee = (1-q*q)*ff
            cross = (aa-bb)*q*ss*ct
            disc = cc*ff-(cc*ff+aa*bb)*q*q
            if disc < -1e-10:
                raise ArithmeticError("Physical null integrator crossed the tropic")
            return (-cross+sign*math.sqrt(max(0.0, disc)))/ee
        return f

    def safe_step(q, theta, slope):
        # An intentionally generous bound for derivative of the varying tropic.
        f = aa*math.sin(theta)**2+bb*math.cos(theta)**2
        fp = (aa-bb)*math.sin(2*theta)
        qt = tropic(theta)
        qtp = cc*aa*bb*fp/(2*qt*(aa*bb+cc*f)**2)
        return (qt-q)*0.15/(1+abs(qtp*slope))

    qq, theta = 0.0, start
    incoming = rhs(+1)
    for count in range(2000000):
        distance = tropic(theta)-qq
        if distance < 1e-12:
            break
        step = min(maxstep, safe_step(qq, theta, incoming(qq, theta)))
        theta = rk4(incoming, qq, theta, step)
        qq += step
    else:
        raise ArithmeticError("Incoming physical integration did not converge")
    impact = {"q": qq, "theta": theta, "distance_to_tropic": distance}
    outgoing = rhs(-1)
    for backcount in range(2000000):
        if qq <= 0:
            break
        step = -min(maxstep, qq,
                    max(1e-13, safe_step(qq, theta, outgoing(qq, theta))))
        theta = rk4(outgoing, qq, theta, step)
        qq += step
    else:
        raise ArithmeticError("Outgoing physical integration did not converge")
    return theta, impact, count+backcount


path_rows = []
for aa, bb, cc, start in [(3., 1., 2., .37), (1., 3., .2, -1.1),
                           (1., 1., 8., .3), (4., 1., 100., .27)]:
    coarse, impact, steps = physical_passage(aa, bb, cc, start, 0.0004)
    fine, impact, steps = physical_passage(aa, bb, cc, start, 0.0002)
    density = lambda t: mp.sqrt((aa*mp.sin(t)**2+bb*mp.cos(t)**2)/
                        (cc+aa*mp.sin(t)**2+bb*mp.cos(t)**2))
    advance = mp.quad(density, [start, (start+fine)/2, fine])
    expected = mp.quad(lambda s: 2*cc*mp.sin(s)**2 /
                 mp.sqrt((aa+cc*mp.sin(s)**2)*(bb+cc*mp.sin(s)**2)),
                 [0, mp.pi/4, mp.pi/2])
    discrepancy = abs(advance-expected)
    check("diagnostic_physical_null_paths", discrepancy < mp.mpf("2e-8"))
    check("diagnostic_path_step_refinement", abs(fine-coarse) < 2e-7)
    path_rows.append({"a": aa, "b": bb, "c": cc, "start": start,
                      "end": fine, "theta_refinement_difference": abs(fine-coarse),
                      "S_advance_error": str(discrepancy), "impact": impact,
                      "steps": steps})

# Check the exact closure count on two different boundary components.
from fractions import Fraction
for numerator in range(1, 20):
    for denominator in range(1, 20):
        rho = Fraction(numerator, denominator)
        for arcs in range(1, 30):
            same_boundary = arcs % 2 == 0
            same_angle = (arcs*rho).denominator == 1
            return_pair = (arcs % 2, (arcs*rho) % 1)
            check("two_boundary_exact_closure", (return_pair == (0, 0)) == (same_boundary and same_angle))

# Reproduce the author script after having read it and record its entire stdout.
author = subprocess.run([sys.executable, str(ORIGINAL/"verify.py")], capture_output=True, text=True, check=True)
author_json = json.loads(author.stdout)
(HERE/"AUTHOR_REPRODUCTION.json").write_text(json.dumps(author_json, indent=2, sort_keys=True)+"\n")
check("author_reproduction", author_json["status"] == "PASS" and author_json["exact_assertions"] == 2087)

receipt = {"status": "PASS", "checked_utc": datetime.now(timezone.utc).isoformat(),
           "reviewer_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "sympy_version": sy.__version__, "mpmath_version": mp.__version__,
           "checks": dict(COUNTS), "check_count": sum(COUNTS.values()),
           "period_diagnostics": period_rows, "physical_null_diagnostics": path_rows,
           "scope": "Exact symbolic identities and exact discrete checks; numerical quadrature/path tests are diagnostic, not proof certificates."}
(HERE/"INDEPENDENT_CHECKS.json").write_text(json.dumps(receipt, indent=2, sort_keys=True)+"\n")
print(json.dumps(receipt, indent=2, sort_keys=True))
