"""Exact domain-control for Theorem 3.1; no manuscript/source repair."""
from pathlib import Path
import datetime, hashlib, json
import sympy as s

eta = s.sqrt(2)/10
v24 = s.Matrix([0,3,-3])
v27 = s.Matrix([1,1,-2])
v29 = s.Matrix([3,0,-3])
delta_field_coefficient = v24 - 3*v27 + v29
assert delta_field_coefficient == s.zeros(3,1)
assert eta > 0 and eta < s.Rational(1,3)
changed_rates = [1629+eta, 1-3*eta, 653+eta]
assert all(value > 0 for value in changed_rates)
assert (653+eta).is_rational is False
out = {
    'created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'COUNTEREXAMPLE_TO_UNRESTRICTED_REAL_RATE_READING_ONLY',
    'paper_location': 'current v2 PDF pp.4–5, Theorem 3.1; p is defined over Q on p.3',
    'base_rates': 'clean specialization, Eq. (17) and Appendix A',
    'changed_directed_rates': {'k24':str(changed_rates[0]), 'k27':str(changed_rates[1]), 'k29':str(changed_rates[2])},
    'other_rates': 'unchanged from the clean specialization',
    'common_source_monomial': 'z^3',
    'delta_vector_identity': '(0,3,-3)-3(1,1,-2)+(3,0,-3)=(0,0,0)',
    'all_twenty_rates_positive': True,
    'field_exactly_unchanged': True,
    'field_still_has_rational_coefficients_and_belongs_to_p': True,
    'free_parameter_a_is_irrational': True,
    'rational_rate_interpretation_refuted': False,
    'explicit_constructions_refuted': False,
    'source_modified': False,
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
}
Path(__file__).with_name('domain-counterexample.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
