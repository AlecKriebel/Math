"""Exact rational certificates for the planar suffix-splice counterexample.

Taylor bounds below are alternating-series bounds on 0<=x<=1.4.
The grid is combined with a proved Lipschitz bound, not used as sampling.
"""
from fractions import Fraction as Q
from math import factorial,comb
from collections import Counter
import json
C=Counter()
def ck(b,k):
 assert b,k
 C[k]+=1

def cos_upper(x):return sum((Q((-1)**j)*x**(2*j)/factorial(2*j) for j in range(7)),Q(0))
def cos_lower(x):return sum((Q((-1)**j)*x**(2*j)/factorial(2*j) for j in range(8)),Q(0))
def sin_lower(x):return sum((Q((-1)**j)*x**(2*j+1)/factorial(2*j+1) for j in range(8)),Q(0))
sg=Q(23,20);step=Q(1,100);grid_margin=Q(61,1000)
for i in range(141):
 x=i*step
 # sigma*(sqrt(26-10 cos x)-1)-(3+x) >= 0.061.
 rhs=1+(3+x+grid_margin)/sg
 ck(26-10*cos_upper(x)>rhs*rhs,'certified_grid_budget')
ck(grid_margin-(sg+1)*step/2>Q(1,20),'interval_budget_via_Lipschitz')
blo=Q(1369438,10**6);bhi=Q(1369439,10**6)
ck(cos_lower(blo)>Q(1,5),'tangent_angle_lower')
ck(cos_upper(bhi)<Q(1,5),'tangent_angle_upper')
dlo=Q(4898979,10**6);dhi=Q(4898980,10**6)
ck(dlo*dlo<24<dhi*dhi,'tangent_length_sqrt_bracket')
delta=Q(7,10);Ulo=dlo-1+delta;Uhi=dhi-1+delta
B_lo=blo+delta;B_hi=bhi+delta
G_lo=sg*Ulo-(3+B_hi);G_hi=sg*Uhi-(3+B_lo)
ck(0<G_lo<G_hi<delta**2/2,'positive_suffix_length')
l=Q(69,50);h=Q(139,100);width=h-l
ck(bhi<l,'patch_after_initial_tangent')
ck(2*G_hi<(B_lo-h)**2,'patch_before_all_suffix_contacts')
ck(3+2*sin_lower(B_lo/2)-Uhi>Q(1,10),'lower_route_gap')
ck(B_hi<3,'upper_semicircle_parameter')
# eta(z)=256*z^4*(1-z)^4, z in [0,1].
p=[Q(0)]*9
for j in range(5):p[j+4]=Q(256*(-1)**j*comb(4,j))
p1=[(i+1)*p[i+1] for i in range(8)]
p2=[(i+1)*p1[i+1] for i in range(7)]
A=width*sum((v/Q(i+1) for i,v in enumerate(p)),Q(0))
Bp=[Q(0)]*15
for i,x in enumerate(p1):
 for j,y in enumerate(p1):Bp[i+j]+=x*y
B=Q(1,width)*sum((v/Q(i+1) for i,v in enumerate(Bp)),Q(0))
M2=sum(abs(v) for v in p2)/width**2
ck(A==Q(32,7875),'bump_integral')
ck(B>0 and M2>0,'bump_derivative_bounds')
eps0=min(Q(1,100),A/(4*B),1/(4*(1+M2)))
eps=eps0/2
ck(eps>0 and eps<eps0,'explicit_perturbation')
ck(1-eps-eps*M2>0,'strict_convexity_lower_bound')
ck(eps*A-eps**2*B>eps*A/2,'strict_length_saving_lower_bound')
ck(Q(1,20)-(sg-1)*eps*(A+2)>0,'modified_prefix_budget_positive')
ck(Q(1,10)-eps*(A+3)>0,'perturbed_lower_route_gap_positive')
# Exact terminal formula for any positive saving, normalized here to saving 1.
ck(sg*(-1)-(-1)==-(sg-1)<0,'terminal_budget_defect_sign')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'sigma':str(sg),'tangent_angle_bracket':[str(blo),str(bhi)],'suffix_length_bracket':[str(G_lo),str(G_hi)],'bump_integral':str(A),'bump_derivative_square_integral':str(B),'explicit_epsilon':str(eps),'scope':'Rational enclosures plus Lipschitz interpolation certify the continuum inequalities. Shortest-path classification and geometric perturbation argument are in TURN_4.md. This is a nonconfining-prefix splice obstruction, not an optimizer counterexample.'},indent=2,sort_keys=True))
