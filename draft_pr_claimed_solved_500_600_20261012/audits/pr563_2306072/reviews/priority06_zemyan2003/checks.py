#!/usr/bin/env python3
"""Source-first reproducible controls. Requires mpmath; no copyrighted text.

The interval calculations certify arithmetic of the published example, not
Brown's support-point theorem. Exact rational controls supplement the analytic
angle and continuation arguments in REPORT.md.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import mpmath as m

BASE = Path(__file__).resolve().parent
PROGRAM = BASE.parents[3]
AUDIT = BASE.parents[1]
SOURCE = PROGRAM / "sources/pr563/user_supplied_20261013/zemyan2003.pdf"
PROOF = AUDIT / "original/unsolved_math_prioritization/attempts/2306072/PROOF.md"
MANUSCRIPT = AUDIT / "publication/support_slit.tex"
EXPECTED_SOURCE_SHA = "a444de051594f2981e1787ed47e70dcc3401c5e0e863856243f8cb8eff382079"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def add(a, b):
    out = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += x
    return out


def divide_series(a, b, n):
    """Power series quotient with nonzero constant denominator."""
    assert b[0]
    q = []
    for i in range(n):
        residual = a[i] if i < len(a) else F(0)
        residual -= sum(q[i-j]*b[j] for j in range(1, min(i, len(b)-1)+1))
        q.append(residual/b[0])
    return q


def exact_controls():
    # The denominator identity underlying the source differential.
    one_minus_s_sq = mul([F(1), F(-1)], [F(1), F(-1)])
    one_plus_s_sq = mul([F(1), F(1)], [F(1), F(1)])
    assert add(one_minus_s_sq, [F(0), F(4)]) == one_plus_s_sq
    # theta'-phi' has numerator -2s over 1-s^2.
    assert add(one_plus_s_sq, [F(-1), F(-4), F(-1)]) == [F(0), F(-2), F(0)]

    # Laurent coefficients obtained by rational series division of s=exp(-xi).
    # Output index n represents xi^(n-1).
    import math
    s = [F((-1)**j, math.factorial(j)) for j in range(12)]
    den = add([F(1)], [-x for x in s])
    num = add([F(1)], s)
    theta = divide_series(num, den[1:], 8)
    s_sq = mul(s, s)[:12]
    phi_num = add(add([F(1)], [4*x for x in s]), s_sq)
    phi_den = add([F(1)], [-x for x in s_sq])
    phi = divide_series(phi_num, phi_den[1:], 8)
    beta = [a-b for a, b in zip(theta, phi)]
    assert theta[:5] == [F(2), F(0), F(1,6), F(0), F(-1,360)]
    assert phi[:5] == [F(3), F(0), F(0), F(0), F(1,60)]
    assert beta[:5] == [F(-1), F(0), F(1,6), F(0), F(-7,360)]

    # Exact first-order candidate mechanism and robust endpoint bounds.
    d = [F(0), F(1), F(0), F(1,2), F(0), F(-1,10)]
    d_prime = [(i+1)*d[i+1] for i in range(len(d)-1)]
    p0 = [F(-2), F(0), F(-3), F(0), F(1)]
    assert p0 == [-2*x for x in d_prime]
    q = add(d_prime, [-x for x in d[1:]])
    assert q == [F(0), F(0), F(1), F(0), F(-2,5)]
    evaluate = lambda c, t: sum(x*t**i for i, x in enumerate(c))
    q1, qT = evaluate(q, F(1)), evaluate(q, F(7,4))
    eta, eps = F(1,10**12), F(1,10**24)
    assert q1 == F(3,5) and qT == -F(441,640)
    assert q1 - 2000*eta > F(1,2)
    assert qT + 2000*eta < -F(1,2)
    assert F(7,25)+7*eta < F(3,10) < F(25,81)
    assert F(25,81)-F(3,10) == F(7,810)
    assert F(7,4)+333*eps < F(9,5)
    assert 1541+4662*eta < 2000
    assert max(F(111**2,2)*eta, 18315*eta, 45621*eta) < 1
    assert 322*eta+110 < 111
    assert F(222)*eps/(1-111*eps) < 223*eps
    return {
        "source_differential_denominator_identity": True,
        "source_theta_minus_phi_identity": True,
        "source_Laurent_series_coefficients": {
            "theta_factor": list(map(str, theta[:5])),
            "phi_factor": list(map(str, phi[:5])),
            "beta_factor": list(map(str, beta[:5])),
            "coefficient_index_means": "xi^(index-1)",
        },
        "candidate_P0_equals_minus_2_dprime": True,
        "candidate_q_equals_dprime_minus_d_over_t": True,
        "candidate_q1": str(q1),
        "candidate_q7over4": str(qT),
        "candidate_sign_margins_over_eps": {
            "at_1_lower": str(q1-2000*eta),
            "at_7over4_upper": str(qT+2000*eta),
        },
        "candidate_tip_radius_separation": str(F(7,810)),
        "candidate_scalar_error_and_orientation_controls": True,
    }


def interval_controls():
    iv = m.iv
    iv.dps = 65
    m.mp.dps = 95
    r = iv.mpf(2)/5
    R = iv.log(7/iv.mpf(3))
    eta_lo = "1.79119112133250053117"
    eta_hi = "1.79119112133250053118"
    root_fun = lambda x: x+R*iv.sin(x)-5*iv.pi/6
    flo, fhi = root_fun(iv.mpf(eta_lo)), root_fun(iv.mpf(eta_hi))
    assert flo.b < 0 < fhi.a
    assert (1-R).a > 0  # global strict monotonicity, hence unique root
    eta = iv.mpf([eta_lo, eta_hi])
    b = r/(1-r*r)*iv.exp(R*iv.cos(eta))
    B = b*iv.exp(iv.j*eta)
    e = iv.exp(-iv.j*eta)

    def sqrt_upper(z):
        assert z.imag.a > 0
        return iv.sqrt((abs(z)+z.real)/2)+iv.j*iv.sqrt((abs(z)-z.real)/2)

    def clog(z):
        return iv.log(abs(z))+iv.j*iv.atan2(z.imag, z.real)

    A = sqrt_upper(1+1/(r*e))
    C = sqrt_upper(1+r/e)
    Q = (A+C)**2
    M = (C-r*A)**2/(1-r*r)
    T = iv.sqrt(b)/iv.cos(eta/2)*(iv.log(abs(Q))-(e*clog(M)).real+iv.log(r/(1-r*r)))
    sqrtB = iv.sqrt(b)*iv.exp(iv.j*eta/2)
    ytip = T*iv.sin(eta/2)/iv.sqrt(b)
    assert T.a > 0 and ytip.a > 0 and ytip.b < iv.pi.a
    assert eta.a > (iv.pi/2).b and eta.b < iv.pi.a
    s0 = iv.exp(-T/sqrtB)
    vtip = -(1-r*r)*iv.exp(e*clog(M))/(r*e*Q)
    residual = s0+vtip
    assert residual.real.a <= 0 <= residual.real.b
    assert residual.imag.a <= 0 <= residual.imag.b
    assert abs(s0).b < 1 and abs(vtip).b < 1
    assert abs(1/vtip).a > 1
    # The reciprocity ambiguity in the tip formula is resolved by these moduli;
    # small residual enclosure is a consistency check, not an identity proof.
    z0 = r*iv.exp(5*iv.j*iv.pi/6)
    normalization_residual = B*(1-r*r)*iv.exp(-e*R)/z0-1
    assert normalization_residual.real.a <= 0 <= normalization_residual.real.b
    assert normalization_residual.imag.a <= 0 <= normalization_residual.imag.b
    a2_source = ((1+r*r)/2+e*r)/z0-1/(2*B)
    assert a2_source.real.b < 0  # excludes the candidate near +a2=2 class

    def interval_string(x):
        return str(x)

    def pair(z):
        return {"real": interval_string(z.real), "imag": interval_string(z.imag)}

    samples = []
    for t_string in ["0", "0.40", "0.45", "1"]:
        t = iv.mpf(t_string)
        s = iv.exp((t-T)/sqrtB)
        w = -4*B*s/(1-s)**2
        ratio = (1/sqrtB)*(1+s)/(1-s)
        phi_prime = ((1/sqrtB)*(1+s/(1+s)+3*s/(1-s))).imag
        theta_prime = ratio.imag
        beta_prime = theta_prime-phi_prime
        beta = -iv.atan2(ratio.imag, ratio.real)
        assert ratio.real.a > 0 and theta_prime.b < 0 and beta_prime.b < 0 and beta.a > 0
        if t_string in ["0", "0.40"]:
            assert phi_prime.b < 0
        else:
            assert phi_prime.a > 0
        samples.append({
            "t": t_string, "w": pair(w),
            "theta_prime": interval_string(theta_prime),
            "phi_prime": interval_string(phi_prime),
            "source_beta_prime": interval_string(beta_prime),
            "source_beta": interval_string(beta),
            "outward_beta": interval_string(-beta),
            "radius_log_derivative": interval_string(ratio.real),
        })

    # Separate high precision reproduction of the waver location.
    rr = m.mpf(2)/5
    RR = m.log(7/m.mpf(3))
    et = m.findroot(lambda x:x+RR*m.sin(x)-5*m.pi/6, (m.mpf(eta_lo), m.mpf(eta_hi)))
    bb = rr/(1-rr*rr)*m.exp(RR*m.cos(et))
    BB, ee = bb*m.exp(m.j*et), m.exp(-m.j*et)
    AA, CC = m.sqrt(1+1/(rr*ee)), m.sqrt(1+rr/ee)
    QQ, MM = (AA+CC)**2, (CC-rr*AA)**2/(1-rr*rr)
    TT = m.sqrt(bb)/m.cos(et/2)*(m.log(abs(QQ))-(ee*m.log(MM)).real+m.log(rr/(1-rr*rr)))
    qq = 1/m.sqrt(BB)
    def angular_rate(t):
        s = m.exp((t-TT)*qq)
        return (qq*(1+s/(1+s)+3*s/(1-s))).imag
    twaver = m.findroot(angular_rate, (m.mpf(".40"), m.mpf(".45")))
    ss = m.exp((twaver-TT)*qq)
    wwaver = -4*BB*ss/(1-ss)**2
    return {
        "method": "mpmath directed interval arithmetic, 65 decimal digit precision",
        "mpmath_version": m.__version__,
        "root_interval": [eta_lo, eta_hi],
        "root_endpoint_residuals": [str(flo), str(fhi)],
        "root_uniqueness_lower_bound_1_minus_R": str(1-R),
        "B": pair(B), "T": str(T), "ytip": str(ytip),
        "Mtip": pair(M), "Mtip_principal_argument": str(iv.atan2(M.imag, M.real)),
        "tip_inside_disk_moduli": {"s0": str(abs(s0)), "Vtip": str(abs(vtip))},
        "tip_reciprocal_outside_disk_modulus": str(abs(1/vtip)),
        "tip_phase_residual_enclosure": pair(residual),
        "normalization_residual_enclosure": pair(normalization_residual),
        "source_example_a2": pair(a2_source),
        "samples": samples,
        "all_interval_assertions_passed": True,
        "high_precision_waver_reproduction_only": {
            "t": m.nstr(twaver, 50),
            "w_real": m.nstr(wwaver.real, 50),
            "w_imag": m.nstr(wwaver.imag, 50),
            "phi_prime_residual": m.nstr(angular_rate(twaver), 10),
        },
        "scope_limit": "Arithmetic certification only. No scan proves global geometry; exact inequalities in REPORT.md do. Support realization relies on the Brown theorem used by Zemyan.",
    }


def main():
    assert sha(SOURCE) == EXPECTED_SOURCE_SHA
    results = {
        "source_identity": {"path": str(SOURCE), "sha256": sha(SOURCE)},
        "candidate_inputs": [{"path": str(p), "sha256": sha(p)} for p in [PROOF, MANUSCRIPT]],
        "exact_controls": exact_controls(),
        "interval_controls": interval_controls(),
        "all_controls_passed": True,
    }
    (BASE/"CHECKS.json").write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps({"all_controls_passed": True, "source": sha(SOURCE), "output": str(BASE/"CHECKS.json")}, indent=2))


if __name__ == "__main__":
    main()
