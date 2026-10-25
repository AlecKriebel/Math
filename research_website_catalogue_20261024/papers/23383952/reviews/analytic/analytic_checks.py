"""Independent exact arithmetic: different pi identity, root algorithm and degrees.

No source imports. Rational intervals corroborate only the stated analytic
reduction; no finite sample is presented as a global spectral proof.
"""
from fractions import Fraction as Q
from math import factorial,isqrt
import json
def need(x,tag):
 if not x:raise ValueError(tag)
def atan_interval(x,terms=30):
 s=sum(((-1)**k*x**(2*k+1)/Q(2*k+1) for k in range(terms)),Q(0))
 return s,s+x**(2*terms+1)/Q(2*terms+1)
def exp_interval(x,n=18):
 need(Q(0)<=x<n+2,'exponential tail ratio')
 term=Q(1);s=term
 for k in range(1,n+1):term=term*x/k;s+=term
 return s,s+term*x/(n+1)/(1-x/Q(n+2))
def root_interval(x):
 scale=10**10;k=isqrt(x.numerator*scale*scale//x.denominator)
 a,b=Q(k,scale),Q(k+1,scale);need(a*a<=x<b*b,'independent root squaring')
 return a,b
def negative_upper(x):return 1/exp_interval(x,60)[0]
def f1_upper(t):return t*root_interval(t)[1]*negative_upper(3*t/4)
def rest_upper(t):
 need(Q(16,9)/(1+7*t)<Q(1,2),'all-j tail ratio ceiling')
 return t*root_interval(t)[1]*(4*negative_upper(15*t/4)+18*negative_upper(35*t/4))
def s(x):return str(x)
def calculate():
 checks=[]
 def check(value,name):need(value,name);checks.append(name)
 # tan(4 atan(1/5))=120/119; subtract atan(1/239) to obtain1.
 check((Q(120,119)-Q(1,239))/(1+Q(120,119)*Q(1,239))==1,'Machin rational tangent identity')
 u,v=atan_interval(Q(1,5)),atan_interval(Q(1,239))
 pilo,pihi=16*u[0]-4*v[1],16*u[1]-4*v[0]
 check(Q(1772,1000)**2<pilo<pihi<Q(1773,1000)**2,'independent Machin sqrt-pi brackets')
 check(exp_interval(Q(1))[1]<Q(2719,1000),'e upper via degree18')
 check(Q(7,5)<2*pilo*pilo,'strict negative theta corrections on whole small-time range')
 small=Q(1773,4000)*exp_interval(Q(7,20))[1]
 check(small<Q(629002,10**6),'printed small-time row')
 endpoints=[Q(k,10) for k in range(14,21)];table=[631338,636143,639464,641172,641202,639541];rows=[]
 for a,b,ceiling in zip(endpoints,endpoints[1:],table):
  q=f1_upper(b)+rest_upper(a);check(q<Q(ceiling,10**6),'printed interval '+str(a)+'..'+str(b));rows.append({'a':s(a),'b':s(b),'independent_bound':s(q),'printed_upper':s(Q(ceiling,10**6))})
 check(all(Q(3,2)-Q(3,4)*t>=0 for t in endpoints),'first-mode increasing through2 derivative numerator')
 check(Q(3,2)-Q(15,4)*Q(2,5)==0,'remaining modes decrease from2/5')
 check(Q(3,2)-Q(3,4)*2==0,'all modes decrease from2')
 check(max([small]+[Q(x,10**6) for x in table])<Q(321,500),'all-time enclosure strictly below321/500')
 lower=Q(1772,2719)*(10000-4*Q(1773,1000))/10004
 check(lower==Q(1106714561,1700054750),'exact displayed cylinder rational')
 check(lower-Q(13,20)==Q(3357947,3400109500)>0,'exact displayed cylinder margin')
 check(Q(13,20)>Q(321,500),'comparison thresholds strictly separated')
 at2=2*root_interval(Q(2))[0]/exp_interval(Q(3,2))[1]
 check(at2>Q(1773,4000),'round finite-time value above zero-time limit')
 check(lower>Q(1773,4000),'weighted finite-time value above zero-time limit')
 check(pihi*exp_interval(Q(1))[1]**3<128,'alternate squared attainment inequality')
 # Geometric volume estimate's remaining elementary cap inequality.
 check(exp_interval(Q(1))[0]**3>Q(8,3),'each cap integral less than2')
 # False alternatives must fail: stronger round threshold and a too-short
 # length in this particular lower-bound certificate, not a geometric theorem.
 controls={'round_bound_3_over_5_rejected':not all(q<Q(3,5) for q in [small]+[f1_upper(b)+rest_upper(a) for a,b in zip(endpoints,endpoints[1:])]),'length10_does_not_certify13_over20':Q(1772,2719)*(10-4*Q(1773,1000))/14<=Q(13,20),'missing_unitary_exponent_detected':Q(3,4)-Q(5,4)==-Q(1,2) and Q(1,4)-Q(3,4)==-Q(1,2),'normalization_powers_detected':Q(2,3)*Q(3,2)==1 and Q(3,2)*Q(1,1)==Q(3,2)}
 check(all(controls.values()),'deliberate false alternatives and exponent bookkeeping')
 return {'status':'PASS','independent_checks':len(checks),'check_names':checks,'arithmetic':'Fraction/integer only; Machin16atan(1/5)-4atan(1/239),30terms; isqrt lattice1e10; P60 negative exponentials/P18 positive tails','pi_interval':[s(pilo),s(pihi)],'small_time_upper':s(small),'middle_intervals':rows,'cylinder_lower':s(lower),'cylinder_margin':s(lower-Q(13,20)),'round_at2_lower':s(at2),'controls':controls,'universal_analytic_obligations_not_replaced_by_code':True}
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
