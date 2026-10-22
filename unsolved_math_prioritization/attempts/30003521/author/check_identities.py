"""Supplementary finite exact checks. Not a PDE/NLS approximation verifier."""
from fractions import Fraction as F
import json

checks = {}
c = F(1, 3)
s_over_sqrt2 = F(2, 3)
s_squared = F(8, 9)
checks['trig_pythagoras'] = c*c + s_squared == 1
checks['f_link_end_values'] = 1 == 1 and c - 2*s_over_sqrt2 == -1
checks['f_arc_end_values'] = -c - s_over_sqrt2 == -1
# Derivatives divided by q*sqrt(2).
link_left = F(-1)
link_right = -s_over_sqrt2 - c
arc_left = F(-1, 2)
arc_right = s_over_sqrt2 - c/2
checks['f_internal_flux'] = link_right == 2*arc_left
checks['f_antiperiodic_flux'] = 2*arc_right == -link_left
checks['monodromy_trace'] = 2*c*c - F(5, 2)*s_squared == -2
checks['monodromy_not_minus_identity'] = c*c - s_squared/2 != -1
checks['transfer_determinants'] = c*c + s_squared == 1
checks['g_periodic_flux'] = -1 == 2*F(-1, 2) and 1 == 2*F(1, 2)
# Formal coefficients of x=a^2 and y=pi^2 in 3*ell^2+4*x-y.
ell2 = (F(-4, 3), F(1, 3))
checks['exact_frequency_resonance'] = (3*ell2[0]+4, 3*ell2[1]-1) == (0, 0)
checks['higher_domain_trace_mismatch'] = len(set(-2*a*a for a in (1, -1, 0))) > 1
assert all(checks.values()), checks
print(json.dumps({
    'passed': True,
    'checks': checks,
    'count': len(checks),
    'scope': 'Finite exact rational checks of displayed identities only.',
    'not_checked': ['analytic integration', 'infinite-band bounds', 'long-time PDE evolution', 'NLS approximation theorem', 'literature completeness'],
    'proof_dependency': 'None: the report gives analytic proofs.'
}, indent=2, sort_keys=True))
