#!/usr/bin/env python3
"""Independently authored symbolic algebra and byte binding adversarial controls.

This is a regression/algebra artifact, not a formal proof or ODE certificate.
No imports from the submitted proof or submitted control code are used.
"""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

import sympy as s

HERE = Path(__file__).resolve().parent
AUDIT_ROOT = HERE.parents[1]
NATIVE_ROOT = AUDIT_ROOT / "native"
PACKET = NATIVE_ROOT / "unsolved_math_prioritization/attempts/2306086"
checks = []


def need(ok, label, kind="symbolic"):
    if not ok:
        raise ValueError(label)
    checks.append({"label": label, "kind": kind})


def zero(expression, label):
    need(s.cancel(expression) == 0, label)


z, zb, p, v, xi = s.symbols("z zb p v xi")
a, u = s.symbols("a u", real=True)
norm_factor = 1-z*zb
phi = (z+a)/(1+a*z)
phib = (zb+a)/(1+a*zb)
dphi = (1-a*a)/(1+a*z)**2
phase = (1+a*zb)/(1+a*z)
Pg = p*dphi-2*a/(1+a*z)
zero(norm_factor*Pg-2*zb-phase*((1-phi*phib)*p-2*phib),
     "covariance_identity_for_arbitrary_pre_schwarzian")
zero(phase*((1+a*z)/(1+a*zb))-1, "covariance_phase_modulus_one")
zero((phi-a)/(1-a*phi)-z, "real_mobius_inverse")
fvalue, fa, fpa = s.symbols("fvalue fa fpa", nonzero=True)
c = (1-a*a)*fpa
g_at_inverse = (fvalue-fa)/c
g_at_minus_a = -fa/c
gprime_at_minus_a = 1/((1-a*a)**2*fpa)
zero((g_at_inverse-g_at_minus_a)/((1-a*a)*gprime_at_minus_a)-fvalue,
     "normalized_koebe_transform_inverse")
zero(1-phi*phib-(1-a*a)*norm_factor/((1+a*z)*(1+a*zb)),
     "disk_metric_transform")
zero((phi-phib)-(1-a*a)*(z-zb)/((1+a*z)*(1+a*zb)),
     "imaginary_part_transform")
zero(1-phi**2-(1-a*a)*(1-z*z)/(1+a*z)**2, "one_minus_square_transform")
delta2 = -(z-zb)**2/(4*(1-z*z)*(1-zb*zb))
delta2_phi = -(phi-phib)**2/(4*(1-phi**2)*(1-phib**2))
zero(delta2_phi-delta2, "delta_squared_invariance")
zero((1-z*z)*(1-zb*zb)-((1-z*zb)**2-(z-zb)**2),
     "delta_domain_identity")
x, y = s.symbols("x y", real=True)
r2 = x*x+y*y
phi_minus = ((x+s.I*y)-a)/(1-a*(x+s.I*y))
realnum = x*a*a-(1+r2)*a+x
zero(s.re(s.together(phi_minus))*(1-2*a*x+a*a*r2)-realnum,
     "orbit_real_part_quadratic")
D = (1+r2)**2-4*x*x
zero(D-((1-r2)**2+4*y*y), "orbit_discriminant_positive_in_disk")
alpha = 2*x/(1+r2+s.sqrt(D))
need(s.simplify(realnum.subs(a, alpha)) == 0,
     "specified_orbit_parameter_solves_quadratic")
t, d = s.symbols("t d", real=True)
tau = 2*d/(1+s.sqrt(1-4*d*d))
need(s.simplify(tau/(1+tau*tau)-d) == 0, "inverse_delta_t_relation")


def A(P, w=z, wc=zb):
    return (1-w*wc)*P-2*wc


for sign in (1, -1):
    k = z/(1-sign*z)**2
    P = s.diff(k, z, 2)/s.diff(k, z)
    zero(P-(4*sign+2*z)/(1-z*z), "koebe_P_"+str(sign))
    Az = A(P)
    Abar = A(P.subs(z, zb), zb, z)
    zero(Az*Abar-(16-48*delta2), "koebe_squared_norm_"+str(sign))
    zero(Az.subs(zb,z)-4*sign, "real_koebe_equality_"+str(sign))
h = z/(1-z*z)
Ph = s.diff(h,z,2)/s.diff(h,z)
zero(Ph-(2*z/(1+z*z)+4*z/(1-z*z)), "two_slit_log_derivative")
w = s.symbols("w")
zero(h-w/(1-w*w)-(z-w)*(1+z*w)/((1-z*z)*(1-w*w)),
     "two_slit_univalence_factorization")
zero(A(Ph).subs({z:s.I*t,zb:-s.I*t})-8*s.I*t/(1+t*t),
     "two_slit_imaginary_axis_value")
zero(16-48/s.Integer(7)-64/s.Integer(7), "lower_bound_crossover_delta_squared_1_over_7")
need(s.Rational(208,25) == (16-48*delta2).subs({z:s.I/2,zb:-s.I/2}),
     "koebe_at_i_over_2_exact_squared")
need(s.Rational(256,25) == (64*delta2).subs({z:s.I/2,zb:-s.I/2}),
     "two_slit_at_i_over_2_exact_squared")
need(s.Rational(256,25)>s.Rational(208,25), "koebe_not_extremal_at_i_over_2")
need(s.limit(16-48*d*d,d,0) == 16, "real_geodesic_limiting_obstruction_squared")
need(s.limit(8*t/(1+t*t),t,1,dir="-") == 4,
     "boundary_limiting_obstruction")
epsilon = s.symbols("epsilon", positive=True)
endpoint_path = 1-epsilon+s.I*epsilon
endpoint_conjugate = 1-epsilon-s.I*epsilon
need(s.simplify(s.limit(delta2.subs({z:endpoint_path,zb:endpoint_conjugate}),epsilon,0)) == s.Rational(1,8),
     "imaginary_part_to_zero_near_endpoint_does_not_imply_delta_to_zero")

q = z*(1+z*z)/(1-z*z)**2
zero(s.diff(q,z)-(1+6*z*z+z**4)/(1-z*z)**3, "convex_average_derivative")
z0 = s.I*(s.sqrt(2)-1)
need(s.simplify(s.diff(q,z).subs(z,z0)) == 0, "convex_average_critical_point")
need(s.simplify(s.diff(q,z,2).subs(z,z0)) != 0, "convex_average_simple_critical_point")
N = 1+6*z*z+z**4
R = 4*z*(1+z*z)
qe = q+epsilon*2*z*z/(1-z*z)**2
zero(s.diff(qe,z)-(N+epsilon*R)/(1-z*z)**3,
     "typically_real_convex_perturbation_derivative")
residue_in_epsilon = s.simplify((s.diff(N,z)/R).subs(z,z0))
need(residue_in_epsilon != 0, "fixed_point_relaxed_P_divergence_nonzero_leading_coefficient")
zero(s.diff(qe,z,2)/s.diff(qe,z)
     -((s.diff(N,z)+epsilon*s.diff(R,z))/(N+epsilon*R)+6*z/(1-z*z)),
     "perturbation_pre_schwarzian_exact_formula")

p_u = (1-z*z)/(1-2*u*z+z*z)
herglotz_average = ((1+xi*z)/(1-xi*z)+(1+z/xi)/(1-z/xi))/2
zero(herglotz_average-p_u.subs(u,(xi+1/xi)/2), "two_atom_herglotz_identity")
L = 1/z+(u-1)/(z-1)-(u+1)/(z+1)
zero(z*L-1/p_u, "tail_starlikeness_logarithmic_derivative")
zero((L+s.diff(L,z)/L).subs(u,1)-(-4+2*z)/(1-z*z), "tail_plus_one_is_negative_koebe")
zero((L+s.diff(L,z)/L).subs(u,-1)-(4+2*z)/(1-z*z), "tail_minus_one_is_positive_koebe")
flow = s.Function("w")(z)
V = s.Function("V")
zero(s.diff(V(flow),z)-s.diff(V(flow),flow)*s.diff(flow,z), "flow_first_jet_chain_rule")
zero(s.diff(V(flow),z,2)-s.diff(V(flow),flow,2)*s.diff(flow,z)**2
     -s.diff(V(flow),flow)*s.diff(flow,z,2), "flow_second_jet_chain_rule")
H = s.Function("H")
composition = H(flow)
zero(s.diff(composition,z,2)/s.diff(composition,z)
     -(s.diff(H(flow),flow,2)/s.diff(H(flow),flow)*s.diff(flow,z)
       +s.diff(flow,z,2)/s.diff(flow,z)), "composition_pre_schwarzian_jet_formula")

need(s.cancel(1/phase-phase) != 0, "negative_wrong_phase_rejected")
need(s.cancel((16-47*delta2)-(16-48*delta2)) != 0, "negative_wrong_deficit_rejected")
need(s.simplify(s.Rational(256,25)-s.Rational(208,25)) > 0,
     "negative_koebe_only_extremizer_rejected")
snapshot = json.loads((AUDIT_ROOT/"SCOPE_AND_SNAPSHOT.json").read_text())
native_bindings = []
for relative, record in snapshot["original_blobs"].items():
    data = (NATIVE_ROOT/relative).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    need(len(data) == record["size"] and digest == record["sha256"],
         "snapshot_sha256_"+relative, "byte_binding")
    native_bindings.append({"path":relative,"bytes":len(data),"sha256":digest})
archive_reports = []
for folder, filename in (("author","FUNCTION_THEORY_2306086_AUTHORED_FREEZE.zip"),
                         ("audit","FUNCTION_THEORY_2306086_INDEPENDENT_SAFE_AUDIT.zip")):
    archive_path = PACKET/"archives"/filename
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        actual = {str(p.relative_to(PACKET/folder)) for p in (PACKET/folder).rglob("*") if p.is_file()}
        need(len(names) == len(set(names)) and set(names) == actual,
             "archive_exact_inventory_"+folder, "byte_binding")
        for name in names:
            need(archive.read(name) == (PACKET/folder/name).read_bytes(),
                 "archive_member_exact_bytes_"+folder+"/"+name, "byte_binding")
        archive_reports.append({"filename":filename,"members":len(names),
                                "bytes":archive_path.stat().st_size,
                                "sha256":hashlib.sha256(archive_path.read_bytes()).hexdigest()})

print(json.dumps({"status":"PASS","sympy_version":s.__version__,
                  "python_version":sys.version,"checks":len(checks),"details":checks,
                  "native_bindings":native_bindings,"archives":archive_reports,
                  "limits":"Symbolic identities and byte replay supplement written arguments; no ODE enclosure, sharp upper bound, formal certificate, or priority certification."},
                 indent=2,sort_keys=True))
