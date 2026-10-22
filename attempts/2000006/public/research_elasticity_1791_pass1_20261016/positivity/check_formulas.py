"""Reproduce elementary symbolic and exponent checks for the positivity lane."""
import json
from fractions import Fraction
from pathlib import Path

import sympy as s

u, v, t = s.symbols("u v t", positive=True)
gamma, p = s.symbols("gamma p", positive=True)
r2 = u*u + v*v + t*t
r = s.sqrt(r2)

interior_h = t * r2**(gamma/2)
interior_q = r2**(gamma/2) + gamma*t*t*r2**(gamma/2-1)
boundary_h = t*t/2 + interior_h
boundary_q = t + interior_q

L = s.log(s.E/r)
log_h = t*t/2 + t*r2*L**p
log_q = t + r2*L**p + t*t*(2*L**p-p*L**(p-1))

rho, eps = s.symbols("rho eps", positive=True)
normal_integral = 1/rho**gamma - 1/(eps+rho**gamma)

checks = {
    "interior_determinant_formula": s.simplify(s.diff(interior_h, t)-interior_q) == 0,
    "boundary_determinant_formula": s.simplify(s.diff(boundary_h, t)-boundary_q) == 0,
    "logarithmic_boundary_determinant_formula": s.simplify(s.diff(log_h, t)-log_q) == 0,
    "inverse_square_normal_integral": s.simplify(
        s.integrate((t+rho**gamma)**-2, (t, 0, eps))-normal_integral
    ) == 0,
    "interior_example_gamma_5_over_4_finite_barrier": 2*Fraction(5, 4) < 3,
    "interior_example_gamma_5_over_4_nonintegrable_piola": 3*Fraction(5, 4) >= 3,
    "boundary_example_gamma_7_over_4_finite_barrier": Fraction(7, 4) < 2,
    "interior_holder_threshold_alpha": str(Fraction(3, 2)-1),
    "boundary_holder_threshold_alpha": str(Fraction(2, 1)-1),
    "logarithmic_boundary_integrability": "integral dr/(r log(e/r)^p) finite iff p>1",
    "benchmark_resolved": False,
    "examples_are_minimizers": False,
}
negative_status_fields = {"benchmark_resolved", "examples_are_minimizers"}
for name, value in checks.items():
    if isinstance(value, bool):
        assert value is (name not in negative_status_fields), name

out = Path(__file__).with_name("formula_checks.json")
out.write_text(json.dumps(checks, indent=2) + "\n")
print(out.read_text(), end="")
