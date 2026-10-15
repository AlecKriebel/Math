"""Exact finite controls; these check stress examples, not the PDE theorem."""
import datetime, fractions, json, pathlib
from fractions import Fraction as Q
root=pathlib.Path(__file__).resolve().parent
rho=Q(7,10)
states=(-1,1)
P={(a,b):(1+rho*a*b)/2 for a in states for b in states}
def pow_p(k,a,b):
    return (1+rho**k*a*b)/2
variance=sum(Q(1,2)*P[a,b]*(a+b)**2 for a in states for b in states)
covs=[]
for lag in range(1,6):
    cov=sum(Q(1,2)*P[a,b]*pow_p(lag-1,b,c)*P[c,d]*(a+b)*(c+d)
            for a in states for b in states for c in states for d in states)
    expected=(1+rho)**2*rho**(lag-1)
    assert cov==expected
    assert abs(cov)<=rho**(lag-1)*variance
    covs.append(dict(lag=lag,covariance=str(cov),variance=str(variance),
                     correct_bound=str(rho**(lag-1)*variance),
                     false_rho_to_lag_bound=str(rho**lag*variance),
                     false_bound_fails=cov>rho**lag*variance))
assert covs[0]['false_bound_fails']
# Product uniform-kernel convolution of the indicator of the unit cube.
# This exact stress example illustrates L2 boundary order, not the smooth K
# selected in the proof. Smooth even kernels likewise retain boundary bias.
dimension=4
bias=[]
for h in (Q(1,10),Q(1,100),Q(1,1000),Q(1,10000)):
    error_squared=(1-Q(5,6)*h)**dimension-2*(1-h/2)**dimension+1
    assert error_squared>0
    ratio=error_squared/h
    bias.append(dict(h=str(h),L2_error_squared=str(error_squared),
                     squared_error_over_h=float(ratio)))
assert abs(bias[-1]['squared_error_over_h']-dimension/6)<0.001
# Operator norm alone cannot control HS: B_n = n^(-1/2) I on n dimensions.
operator_control=[dict(n=n,operator_norm=n**(-0.5),HS_norm=1.0) for n in (10,100,1000,10000)]
# Checking the polynomial/exponential summability ratio rather than a
# misleading small-j finite sum (large d can put the maximum at large j).
summability=[]
for d in (2,10,100):
    exponent=16*d+2
    j=max(100,4*exponent)
    ratio=Q(j+2,j+1)**exponent/2
    assert ratio<1
    summability.append(dict(d=d,j=j,successive_term_ratio=float(ratio),limit=0.5))
result=dict(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            overlap_covariance=covs,boundary_bias=bias,
            operator_norm_insufficient=operator_control,summability=summability,
            mathematical_proof_dependency=False,checks_passed=True)
(root/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
