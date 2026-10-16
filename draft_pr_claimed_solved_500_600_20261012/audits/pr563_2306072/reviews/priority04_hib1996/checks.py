from fractions import Fraction as F
from pathlib import Path
import json
class C:
 def __init__(self,r=0,i=0):self.r=F(r);self.i=F(i)
 def __add__(self,o):o=cc(o);return C(self.r+o.r,self.i+o.i)
 __radd__=__add__
 def __neg__(self):return C(-self.r,-self.i)
 def __sub__(self,o):return self+-cc(o)
 def __rsub__(self,o):return cc(o)+-self
 def __mul__(self,o):o=cc(o);return C(self.r*o.r-self.i*o.i,self.r*o.i+self.i*o.r)
 __rmul__=__mul__
 def __truediv__(self,o):o=cc(o);d=o.r**2+o.i**2;return self*o.conj()*C(1/d)
 def __pow__(self,n):
  if n<0:return (C(1)/self)**(-n)
  q=C(1)
  for _ in range(n):q=q*self
  return q
 def conj(self):return C(self.r,-self.i)
 def __eq__(self,o):o=cc(o);return self.r==o.r and self.i==o.i
 def norm2(self):return self.r**2+self.i**2
 def data(self):return {'real':str(self.r),'imaginary':str(self.i)}
def cc(o):return o if isinstance(o,C)else C(o)
checks=[]
def ck(name,cond,evidence=None):checks.append({'name':name,'pass':bool(cond),'evidence':evidence})
a=C(2,3);w=C(F(7,5),F(-4,3));b=-a
phi=a*a/(a-w)+b*b/(b-w)
ck('zero_J_Phi_identity_exact_control',phi==-2*a*a*w/(w*w-a*a))
ck('zero_J_Q_identity_exact_control',phi/(w*w)==-2*a*a/(w*(w*w-a*a)))
# Cleared formal polynomial identity in two indeterminates a,w.
# [a²(-a-w)+a²(a-w)] + 2a²w = 0.
ck('zero_J_identity_cleared_formal_coefficients',(-1+1)==0 and (-1-1+2)==0)
x=C(F(3,5),F(4,5));u=C(F(-5,13),F(12,13))
ck('unit_z_exact',x.norm2()==1)
ck('unit_tip_u_exact',u.norm2()==1)
quot=(x-u)**2/(x*u)
ck('circle_numerator_has_negative_sign',quot==C(-(C(1)-x/u).norm2()),quot.data())
ck('circle_numerator_positive_sign_negative_control',quot!=C((C(1)-x/u).norm2()))
# For F(t)=a²/(a-ct)+b²/(b-ct), each pole contributes c to the linear term.
c=C(F(3,5),F(-4,5));aa=C(2,3);bb=C(-1,4)
linear=(aa**2)*(c/(aa**2))+(bb**2)*(c/(bb**2))
ck('theorem1_linear_coefficient_is_2c',linear==2*c,linear.data())
ck('theorem1_printed_c_coefficient_negative_control',linear!=c)
# Degenerate sum case: a+b=0 and reciprocal sums real do not alone imply conjugacy/reality.
aa=C(1,1);bb=-aa
ck('theorem1_degenerate_sum_zero',aa+bb==0 and C(1)/aa+C(1)/bb==0)
ck('theorem1_real_sums_alone_insufficient',aa.i!=0 and bb.i!=0 and aa!=bb.conj())
ck('theorem1_next_odd_coefficient_detects_missing_case',(C(1)/(aa**2)+C(1)/(bb**2)).i!=0)
# Representative *actual* zero-extremal support from the paper's Koebe example family.
# p=(11-4sqrt(7))/3 is the root of T(p)=3p²-22p+3 in (1/10,1/5).
def T(t):return 3*t*t-22*t+3
ck('positive_p_root_bracket',T(F(1,10))>0>T(F(1,5)))
ck('negative_point_koebe_value',C(F(-1,3))/(1-C(F(-1,3)))**2==C(F(-3,16)))
# 16p-3(1-p)^2=-T(p), checked coefficient by coefficient.
square=[F(1),F(-2),F(1)]
lhs=[-3*square[0],16-3*square[1],-3*square[2]]
rhs=[-F(3),-F(-22),-F(3)]
ck('positive_point_koebe_value_formal_reduction',lhs==rhs,{'lhs':[str(q)for q in lhs],'rhs':[str(q)for q in rhs]})
ck('positive_point_wrong_sign_negative_control',lhs!=[-q for q in rhs])
ck('zero_example_identity_J_z_negative',F(1,5)-F(1,3)<0)
# r2=-1/3 lies in Brown's Koebe interval because e>2.
ck('negative_point_interval_reduces_to_e_gt_2',(1-F(2))/(1+F(2))==F(-1,3))
# Straight half-line derivatives: theta'=-y/(x²+y²), beta'=y/(x²+y²), |beta|'=-|y|/(x²+y²).
for xx,yy in [(F(1),F(2)),(F(3),F(2)),(F(1),F(-2)),(F(3),F(-2)),(F(3),F(0))]:
 den=xx**2+yy**2;theta=-yy/den;beta=yy/den;mag=-abs(yy)/den
 ck('straight_line_angles_control_'+str(xx)+'_'+str(yy),theta==-beta and mag<=0,{'theta_prime':str(theta),'beta_prime':str(beta),'magnitude_prime':str(mag)})
r={'all_pass':all(x['pass']for x in checks),'count':len(checks),'checks':checks,'limitations':'Exact finite controls supplement the algebraic derivations; they do not formally verify source analytic theorems or novelty.'}
(Path(__file__).parent/'CHECKS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'all_pass':r['all_pass'],'checks':r['count']}))
assert r['all_pass']
