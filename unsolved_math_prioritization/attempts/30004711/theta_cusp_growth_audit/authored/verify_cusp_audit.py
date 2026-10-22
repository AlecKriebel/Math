"""Reproduce elementary identities and audit pins, without modifying input files.

This script is not a numerical uniformization calculation or a formal verification
of the analytic/geometric proof. Those arguments are in the authored audit.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

here = Path(__file__).resolve().parent
workspace = here.parents[1]
inputs = workspace / "theta_twisted_volumes_30004711" / "authored"
source_dir = here.parent / "private_sources"
acceptance = json.loads((here / "PINNED_CUSP_CORRECTION_ACCEPTANCE.json").read_text())
manifest = json.loads((here / "PUBLIC_CUSP_AUDIT_SOURCE_MANIFEST.json").read_text())


def check_pin(path, pin):
    data = path.read_bytes()
    assert len(data) == pin["bytes"], path
    assert hashlib.sha256(data).hexdigest() == pin["sha256"], path


for pin in [acceptance["frozen_candidate"], *acceptance["other_inspected_authored_inputs"]]:
    check_pin(inputs / pin["filename"], pin)
check_pin(here / acceptance["audit_report"]["filename"], acceptance["audit_report"])
for pin in manifest["sources"]:
    check_pin(source_dir / pin["retrieved_filename"], pin)

Y, y, T, A, r, t, k = s.symbols("Y y T A r t k", positive=True)
collar = s.integrate(Y / s.pi * s.sin(s.pi * y / Y), (y, 0, Y))
assert s.simplify(collar - 2 * Y**2 / s.pi**2) == 0
holder = T ** s.Rational(3, 2) / s.sqrt(A)
assert s.simplify(holder ** s.Rational(2, 3) * A ** s.Rational(1, 3) - T) == 0
tail = s.integrate(y * s.exp(-2 * s.pi * y), (y, Y, s.oo))
expected_tail = s.exp(-2 * s.pi * Y) * (Y / (2 * s.pi) + 1 / (4 * s.pi**2))
assert s.simplify(tail - expected_tail) == 0
assert s.limit((2 * s.log(t) + s.log(s.log(t))) / t, t, s.oo) == 0
assert s.limit((2 * s.log(k * t) + s.log(s.log(k * t))) / t, t, s.oo) == 0
primitive = -s.log(1 / r) ** 2 / 2
assert s.simplify(s.diff(primitive, r) - s.log(1 / r) / r) == 0
assert s.limit(primitive, r, 0, dir="+") == -s.oo
oscillatory_model = 2 * s.log(t) + s.sin(t**2)
assert s.simplify(s.diff(oscillatory_model, t) - (2 / t + 2 * t * s.cos(t**2))) == 0

report = {
    "frozen_candidate_sha256": acceptance["frozen_candidate"]["sha256"],
    "all_authored_input_and_report_pins_match": True,
    "all_fresh_source_pins_match": True,
    "collar_integral": str(collar),
    "holder_lower_bound": "T^(3/2)/sqrt(2*pi)",
    "NS_tail_integral": str(s.simplify(tail)),
    "log_metric_sublogarithmic": True,
    "sublogarithmic_after_ramified_base_change": True,
    "central_Ramond_radial_norm_integral_diverges": True,
    "bounded_growth_does_not_bound_derivatives_example_checked": True,
    "analytic_and_geometric_proof_in_authored_report": True,
    "hyperbolic_metric_computed_numerically": False,
    "finite_boundary_flux_existence_proved": False,
    "actual_torsion_comparison_proved": False,
    "all_checks_passed": True,
}
(here / "CUSP_AUDIT_CHECK.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
