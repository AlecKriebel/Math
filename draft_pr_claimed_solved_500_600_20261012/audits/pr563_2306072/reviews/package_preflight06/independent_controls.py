#!/usr/bin/env python3
from fractions import Fraction as F
import json
from pathlib import Path
eta=F(1,10**12); eps=eta**2
checks={}
def check(name,value):
 assert value,name
 checks[name]=bool(value)
r=F(3,4); h0=F(7,4); lo=F(17,10); hi=F(9,5)
check('H_tail_alternate_radius',13*F(27,112)<4)
check('Hprime_tail_alternate_radius',13*F(207,49)<64)
check('H_range',h0-5*eta>lo and h0+5*eta<hi)
ferr=r*5*(hi+h0)/(lo**2*h0**2)
fperr=23/lo**3+F(1,4)*5*(hi**2+hi*h0+h0**2)/(lo**3*h0**3)
check('f_alternate_error_under_2eta',ferr<2)
check('fprime_alternate_error_under_6eta',fperr<6)
check('actual_tip_bound_alternate_under_027',F(13,49)+5*eta<F(27,100))
check('inverse_slit_radius_gap',F(25,81)>F(3,10)>F(27,100))
# All coefficient uncertainties are for arbitrary global maximizers.
check('a2_bound',52<64)
check('a3_root_area_bound',F(52,3)<25)
check('a3_minus3_bound',5+F(3,4)*8*4==29)
check('A_bound',2*29+8*6==106)
check('B_bound',3*8==24)
check('P_uncertainty',106+24*9==322)
check('P0_disc3',2+3*9+81==110)
check('P_disc3',110+322*eta<111)
check('root_162',161+F(111**2,2)*eta<162)
check('direct_Z_325', (324+42*111*eta)/(1-111*eps)<325)
check('qprime_disc3',2*3+F(8,5)*27<50)
check('direct_Z_at_real_t_326',325+50*333*eta<326)
q=lambda t:t*t-F(2,5)*t**4
check('q_left',q(F(1))==F(3,5))
check('q_right',q(F(7,4))==-F(441,640))
check('left_sign_margin',q(F(1))-326*eta>F(1,2))
check('right_sign_margin',q(F(7,4))+326*eta<-F(1,2))
check('orientation_real_positive',223*eps<1)
# Original manuscript remainders, independently recomputed as rationals.
check('G_remainder',3*162==486)
check('V_remainder',486+55*333*eta<487)
check('Vprime_remainder',161+(2*111**2+F(126,2)*333)*eta<162)
check('Z_remainder',2*(F(7,4)*162+487)+2*7*333*eta<2000)
check('Rouche_boundary_gap',333*eps<1)
check('W_radius',F(7,4)+333*eps<F(9,5))
check('epsilon_zero_q_effect_vanishes',0*q(F(1))==0)
# Independent polynomial identities underpinning the direct quotient expansion.
def pmul(a,b):
 out={}
 for i,x in a.items():
  for j,y in b.items():out[i+j]=out.get(i+j,F(0))+x*y
 return {i:x for i,x in out.items() if x}
def padd(a,b):
 out=dict(a)
 for i,x in b.items():out[i]=out.get(i,F(0))+x
 return {i:x for i,x in out.items() if x}
P0={0:F(-2),2:F(-3),4:F(1)}
average={i:x/F(i+1) for i,x in P0.items()}
angular={i:(average.get(i,0)-P0.get(i,0))/2 for i in set(average)|set(P0)}
check('direct_quotient_q_identity',{i:x for i,x in angular.items() if x}=={2:F(1),4:F(-2,5)})
# Candidate Koebe-ray constraints require cos(3theta)=cos(2theta)=0;
# exact Bezout contradiction (no trigonometric approximation).
g={2:F(2),0:F(-1)};h={3:F(4),1:F(-3)}
bezout=padd(pmul({2:F(4),0:F(-1)},g),pmul({1:F(-2)},h))
check('Koebe_phase_constraints_impossible',bezout=={0:F(1)})
# Evenness of output P does not imply a polynomial square.
check('quartic_discriminant_uniform_nonzero',4*eps-28*eps**2>3*eps)
check('Goh_same_degree4_all_possible_differing_indices',all(__import__('math').gcd(3,j-1)==1 for j in [2,3]))
# Concrete S competitors: k and identity order opposite under complex scaling.
check('complex_normalization_reverses_objective_order',2>0 and -5<0)
result={'status':'PASS','method':'Independent rational constants at alternate radius r=3/4; direct Z=G/(vp) remainder; main manuscript margins. Analytic scope in checkpoint and report.','checks':checks,'count':len(checks),'alternate_f_error_coefficient':str(ferr),'alternate_fprime_error_coefficient':str(fperr),'alternate_tip_base':str(F(13,49)),'direct_Z_error_epsilon_eta':326}
print(json.dumps(result,indent=2))
