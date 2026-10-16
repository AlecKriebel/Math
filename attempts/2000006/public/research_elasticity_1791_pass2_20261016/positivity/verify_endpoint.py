"""Check algebra used in the endpoint/regularization audit; not a PDE proof."""
import json
from pathlib import Path
import sympy as s

e, d, k, z, tau = s.symbols("epsilon d kappa z tau", positive=True)
J=s.symbols("J", real=True)
line=3/e**2-2*J/e**3
obj=-k*z*z+2*d*z/e**3+3*d/e**2
zstar=d/(k*e**3)
eps_in_interval=3*tau/(4*(1-tau))
mixed_det=(tau-(1-tau)*e)*(tau-2*(1-tau)*e)

checks={
 "tangent_value_matches":s.simplify(line.subs(J,e)-e**-2)==0,
 "tangent_slope_matches":s.simplify(s.diff(line,J)+2/e**3)==0,
 "regularization_ray_optimizer":s.simplify(s.diff(obj,z).subs(z,zstar))==0,
 "regularization_ray_maximum":s.simplify(obj.subs(z,zstar)-(d*d/(k*e**6)+3*d/e**2))==0,
 "interpolation_negative_choice":s.simplify(mixed_det.subs(e,eps_in_interval)+tau*tau/8)==0,
 "barrier_rank_one_hessian":s.simplify(s.diff(J**-2,J,2).subs(J,e)-6/e**4)==0,
 "global_dini_theorem_is_conditional":True,
 "unconditional_higher_integrability_proved":False,
 "benchmark_resolved":False,
}
negative={"unconditional_higher_integrability_proved","benchmark_resolved"}
for name,value in checks.items():
    assert value is (name not in negative),name
out=Path(__file__).with_name("ENDPOINT_CHECKS.json")
out.write_text(json.dumps(checks,indent=2)+"\n")
print(out.read_text(),end="")
