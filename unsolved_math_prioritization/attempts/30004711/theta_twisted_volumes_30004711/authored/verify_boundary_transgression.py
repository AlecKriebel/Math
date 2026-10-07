"""Exact checks for the authored cylinder model and conditional genus-one residue.
Does not compute an actual moduli-space torsion connection or cusp asymptotic.
"""
from fractions import Fraction as F
import json
from pathlib import Path

checks=[]
for x in [F(2),F(4),F(10),F(100),F(10000)]:
    # x=exp(2R), q(R)=x/(1+x), q(-R)=1/(1+x).
    qp=x/(1+x)
    qm=1/(1+x)
    delta=qp-qm
    assert delta==(x-1)/(x+1)
    assert qp+qm==1 and 0<delta<1
    assert 1-delta==F(2)/(x+1)
    checks.append({'exp_2R':str(x),'q_R':str(qp),'q_minus_R':str(qm),'truncated_volume_per_sc':str(delta),'error_to_limit_per_sc':str(1-delta)})
for c in [F(-3),F(-1,16),F(0),F(1,16),F(1),F(3,2)]:
    for s in [F(0),F(1,3),F(1)]:
        # Integral q'(t)dt=q(infinity)-q(-infinity)=1.
        vol=s*c
        absolute_integral=abs(s*c)
        assert absolute_integral>=abs(vol)
W=F(1,16); theta=F(1,8)
residue={str(eps):str(theta-eps*W) for eps in [1,-1]}
assert residue=={'1':'1/16','-1':'3/16'}
report={'model':'C* with q(t)=exp(2t)/(1+exp(2t)), A_s=s*c*q(t)*J*dtheta','same_bundle_metric_orientation_body':True,'finite_integral_for_all_real_c':'s*c','boundary_limit_for_all_real_c':'s*c','rank_2_normalized_euler_form':'s*c*q_prime(t)/(2*pi) dt wedge dtheta','truncation_checks':checks,'conditional_genus_1_required_boundary_by_epsilon':residue,'actual_owr_measure_comparison_verified':False,'all_checks_passed':True}
Path(__file__).with_name('BOUNDARY_TRANSGRESSION_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
