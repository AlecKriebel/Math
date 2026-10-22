#!/usr/bin/env python3
"""Exact algebra checks for the attributed minimum-area solution.

Requires SymPy. These checks do not prove the representation or geometric
symmetrization theorems, which are explicitly cited in PROOF.md.
"""
import json
import sympy as S

t, z, a, p, y, s = S.symbols('t z a p y s', real=True)
checks = []
def zero(name, value):
    assert S.simplify(value) == 0, (name, S.simplify(value))
    checks.append(name)

# Coefficients from the exact Pick relation through cubic order.
p3 = t*z + 2*t*(1-t)*z**2 + (3*t-8*t**2+5*t**3)*z**3
residual = S.series(p3/(1-p3)**2-t*z/(1-z)**2,z,0,4).removeO()
zero('Pick_relation_through_degree_3', residual)
f3 = S.series((p3+p3**2/2)/t,z,0,4).removeO().expand()
zero('first_coefficient_one', f3.coeff(z,1)-1)
zero('second_coefficient', f3.coeff(z,2)-(2-3*t/2))
zero('third_coefficient', f3.coeff(z,3)-3*(1-t)**2)
zero('prescribed_second_coefficient', (2-3*t/2-a).subs(t,2*(2-a)/3))

# Direct implicit differentiation, followed by the Pick relation.
kpz = (1+z)/(1-z)**3
kpp = (1+p)/(1-p)**3
fp = S.cancel((t*kpz/kpp)*(1+p)/t)
zero('implicit_derivative_formula', fp-(1+z)*(1-p)**3/(1-z)**3)
# Squared branch-sensitive identity after substitution of (1-p)^2.
zero('squared_derivative_identity',
     (1+z)**2*(p*(1-z)**2/(t*z))**3/(1-z)**6
     -(1+z)**2*(p/z)**3/t**3)

# Area and the integrated affine support function, with pi factored out.
zero('area_parameter_conversion',
     (S.Rational(3,2)/t**2).subs(t,2*(2-a)/3)-S.Rational(27,8)/(2-a)**2)
zero('support_function_average',
     ((3*t-2+a)/t**3-S.Rational(3,2)/t**2).subs(a,2-3*t/2))
# s=sqrt(y^2-t), y>sqrt(t). Identity proves positivity because every
# factor in s*(4*y^2-t)/y is positive in that range.
zero('slit_kernel_nonnegative_remainder',
     (4*y**2-3*t-(y-s)**3/y-s*(4*y**2-t)/y).subs(t,y*y-s*s))
# Polynomial triple-angle identity after sin(phi/2)=y/sqrt(t).
u = S.symbols('u')
zero('triple_angle_support_polynomial',
     3*u-4*u**3-u*(3-4*u**2))
zero('piecewise_join', (1+2*a*a-S.Rational(27,8)/(2-a)**2).subs(a,S.Rational(1,2)))
zero('strict_improvement_factorization',
     S.Rational(27,8)-(1+2*a*a)*(2-a)**2-(5-2*a)*(2*a-1)**3/8)

# The incorrect denominator seven is strictly larger than the attained area.
zero('publisher_denominator_discrepancy',
     S.Rational(27,7)/(2-a)**2-S.Rational(27,8)/(2-a)**2
     -S.Rational(27,56)/(2-a)**2)

# In the repaired comparison, -G(-x) <= |f(-x)| gives b >= a.
# This checks only the Taylor-sign calculation, not the slit inclusion.
x, b, d, e = S.symbols('x b d e', real=True)
fminus = -x+a*x**2+(d+S.I*e)*x**3
mod_squared = S.expand(fminus*S.conjugate(fminus))
mod_series = x*S.series(S.sqrt(mod_squared/x**2),x,0,3).removeO()
zero('negative_ray_modulus_expansion',
     S.series(mod_series-(x-a*x**2),x,0,3).removeO())
zero('comparison_coefficient_direction',
     S.expand((x-a*x**2)-(x-b*x**2))/x**2-(b-a))

result = {'status':'PASS', 'arithmetic':'exact symbolic',
          'sympy_version':S.__version__, 'checks':checks,
          'check_count':len(checks),
          'scope':'Algebra only. No numerical grid, theorem-prover certificate, or verification of external symmetrization results.'}
print(json.dumps(result,indent=2))
