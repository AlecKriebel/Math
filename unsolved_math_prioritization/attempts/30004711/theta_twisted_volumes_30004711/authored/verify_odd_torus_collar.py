"""Algebraic checks for explicit comparison estimates; not hyperbolic numerics."""
import json
from pathlib import Path
import sympy as s
Y,y=s.symbols('Y y',positive=True)
collar=s.integrate(Y/s.pi*s.sin(s.pi*y/Y),(y,0,Y))
assert s.simplify(collar-2*Y**2/s.pi**2)==0
T=s.symbols('T',positive=True)
assert s.limit((2*s.log(T)+s.log(s.log(T)))/T,T,s.oo)==0
A,M=s.symbols('A M',positive=True)
# T <= M^(2/3)A^(1/3) implies M >= T^(3/2)A^(-1/2).
assert s.simplify((T**s.Rational(3,2)/s.sqrt(A))**s.Rational(2,3)*A**s.Rational(1,3)-T)==0
Y0=s.symbols('Y0',positive=True)
tail=s.integrate(y*s.exp(-2*s.pi*y),(y,Y0,s.oo))
expected=s.exp(-2*s.pi*Y0)*(Y0/(2*s.pi)+1/(4*s.pi**2))
assert s.simplify(tail-expected)==0
report={'long_collar_integral':str(collar),'holder_lower_bound':'T^(3/2)/sqrt(2*pi)','uniform_lower_bound':'2*(T-2)^2/pi^2','uniform_upper_bound':'C*T^2*log(T), via fixed thrice-punctured-sphere comparison','log_metric_sublinear_in_log_inverse_q':True,'NS_tail_integral':str(tail),'smooth_metric_extension_consistent_with_bounds':False,'finite_canonical_boundary_flux_proved_to_exist':False,'actual_torsion_transgression_computed':False,'all_symbolic_checks_passed':True}
Path(__file__).with_name('ODD_TORUS_COLLAR_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
