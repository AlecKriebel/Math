"""Symbolic and rational checks; theorem applications still require mathematical audit."""
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as s
r,eps,t=s.symbols('r eps t',positive=True)
I=s.integrate(-s.log(r),(r,0,eps))
assert s.simplify(I-eps*(1-s.log(eps)))==0
assert s.limit(I,eps,0,dir='+')==0
# (1/2)(K+D)+(1/2)D = (1/2)K+D.
assert F(1,2)+F(1,2)==1
m_upper=2*s.log(t)+s.log(s.log(t))
assert s.limit(m_upper/t,t,s.oo)==0
assert s.limit((1+s.log(s.log(t)))/t,t,s.oo)==0
value=F(3,2)*F(1,2)*F(1,24)
assert value==F(1,32)
report={'multiplier_ideal_transverse_integral':str(I),'transverse_integral_finite_and_tends_zero':True,'twist_line':'L=ell(D), L^2=K(2D)','twist_curvature_identity':'c1(L)=1/2*c1(K(D))+1/2*[D]','weight_on_L':'rho^(-1)*|z|^(-2)','canonical_odd_component_integral':str(value),'flux_bound_limit_zero':True,'direct_image_applied_only_over_smooth_base':True,'actual_torsion_comparison_verified':False,'higher_rank_top_chern_extension_verified':False,'all_symbolic_checks_passed':True}
Path(__file__).with_name('POSITIVE_CURRENT_REPAIR_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
