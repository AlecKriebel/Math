from fractions import Fraction as F
import json
out=[]
for k in [2,10,100,1000]:
 s=k**4;Q=k*k;rare=k;lr=F(k**3,4);lc=F(s,4*(s-k));B=2*(F(rare,s)*lr+F(s-rare,s)*lc);w=lr/s;L=Q*w;r=F(3,2)
 assert B==1 and L==F(k,4) and w==F(1,4*k)
 assert 2*F(rare,s)*lr/B==F(1,2)
 up=r*(1+w)/(r*(1+w)+(Q-1)*w);down=(1+(Q-1)*w)/(1+(Q-1)*w+r*w);local=up/(up+down)
 out.append({'k':k,'Q_over_s':str(F(Q,s)),'max_lambda_over_s':str(w),'aggregate_rare_endpoint_portal_load':str(L),'rare_incidence_mass':'1/2','first_local_change_success':str(local),'first_local_change_success_decimal':float(local)})
assert out[-1]['first_local_change_success_decimal']<0.01
print(json.dumps({'diagnostic_not_global_fixation_counterexample':True,'exact_rational_checks':out},indent=2))
