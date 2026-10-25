"""Independent exact arithmetic from the manuscript formulas; no source imports."""
from fractions import Fraction as F
from math import isqrt
import json

def need(x,m):
    if not x: raise RuntimeError(m)
def taylor(x,n):
    term=F(1);total=term
    for k in range(1,n+1): term*=x/k;total+=term
    return total
def exp_interval(x,n):
    need(0<=x<n+2,'Taylor ratio hypothesis')
    lower=taylor(x,n);term=F(1)
    for k in range(1,n+2): term*=x/k
    return lower,lower+term/(1-x/F(n+2))
def atan_interval(x):
    need(0<x<1,'alternating arctangent hypothesis')
    partial=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(24)),F())
    return partial,partial+x**49/F(49)
def sqrt_upper(x):
    scale=10**8;q=isqrt(x.numerator*scale**2//x.denominator)
    lower=F(q,scale);upper=F(q+1,scale)
    need(lower**2<=x<upper**2,'integer square-root enclosure')
    return upper
def enc(x): return {'numerator':x.numerator,'denominator':x.denominator}

def main():
    a,b=atan_interval(F(1,3));c,d=atan_interval(F(1,7))
    pi_lo,pi_hi=8*a+4*c,8*b+4*d
    need(F(1772,1000)**2<pi_lo<pi_hi<F(1773,1000)**2,'sqrt pi brackets')
    e_lo,e_hi=exp_interval(F(1),14)
    need(e_hi<F(2719,1000),'e bracket')
    need(8/(3*e_lo**3)<1,'strict cap volume upper bound')
    need(128>pi_hi*e_hi**3,'round interior-value versus endpoint limit')
    weighted=F(1772,2719)*F(10000000-7092,10004000)
    need(weighted==F(1106714561,1700054750),'literal weighted certificate fraction')
    margin=weighted-F(13,20)
    need(margin==F(3357947,3400109500)>0,'weighted strict margin')
    small=F(1773,4000)*exp_interval(F(7,20),14)[1]
    need(small<F(629002,10**6),'small-time bound')
    need(F(16,9)/taylor(F(49,5),50)<F(1,2),'all tail ratios from a>=7/5')
    endpoints=[F(7,5),F(3,2),F(8,5),F(17,10),F(9,5),F(19,10),F(2)]
    ceilings=[631338,636143,639464,641172,641202,639541]
    rows=[]
    for left,right,ceiling in zip(endpoints,endpoints[1:],ceilings):
        A=right*sqrt_upper(right)/taylor(3*right/4,50)
        D=left*sqrt_upper(left)*(4/taylor(15*left/4,50)+18/taylor(35*left/4,50))
        value=A+D;upper=F(ceiling,10**6)
        need(value<upper,'exact table row '+str(left))
        rows.append({'left':enc(left),'right':enc(right),'exact_formula_upper':enc(value),'claimed_ceiling':enc(upper),'strict_slack':enc(upper-value)})
    need(max([F(629002,10**6)]+[F(c,10**6) for c in ceilings])==F(641202,10**6)<F(321,500)<F(129,200),'entire-time-cover numeric margin')
    # Negative numerical sanity checks do not substitute for the analytic hypotheses.
    need(weighted<F(33,50),'certificate does not justify invented weighted .66 bound')
    need(weighted/2<F(13,20),'incorrect halved rescaling prefactor loses claimed lower bound')
    result={'status':'PASS_EXACT_RATIONAL_FORMULAS','source_code_or_historical_verdict_imported':False,
      'proof_scope':'Arithmetic only; cap smoothness, conformal operator equivalence, variational inequalities, Poisson summation and heat asymptotics require the separate written argument and primary applicability.',
      'pi_enclosure':{'lower':enc(pi_lo),'upper':enc(pi_hi)},'e_upper':enc(e_hi),
      'weighted_lower':enc(weighted),'weighted_margin_over_13_20':enc(margin),
      'small_time_formula_upper':enc(small),'all_six_compact_time_rows':rows,
      'round_all_time_bound':enc(F(641202,10**6)),'no_floating_point_acceptance':True,
      'negative_sanity_checks':2,'writes':False}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
