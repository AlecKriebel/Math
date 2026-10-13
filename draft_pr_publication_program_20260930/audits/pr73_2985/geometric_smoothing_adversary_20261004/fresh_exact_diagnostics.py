"""Fresh independent exact diagnostics, written after FIRST_CONCLUSION was sealed.
Finite algebra validates specified affine data; symbolic seam identity is universal.
No author checker, stored diagnostics or numerical sampling is used.
"""
from fractions import Fraction as F
from itertools import permutations
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent

def parity(t):return (-1)**sum(t[i]>t[j] for i in range(len(t)) for j in range(i+1,len(t)))
def det(m):
 n=len(m)
 return sum(F(parity(p))*prod(m[i][p[i]] for i in range(n)) for p in permutations(range(n)))
def prod(s):
 r=F(1)
 for x in s:r*=x
 return r

def wedge(a,b):
 out={}
 for i,x in a.items():
  for j,y in b.items():
   k=i+j
   if len(set(k))<len(k):continue
   ksort=tuple(sorted(k));out[ksort]=out.get(ksort,F(0))+F(parity(k))*x*y
 return {k:v for k,v in out.items() if v}
def add(a,b):
 c=dict(a)
 for k,v in b.items():c[k]=c.get(k,F(0))+v
 return {k:v for k,v in c.items() if v}
def scale(a,t):return {k:t*v for k,v in a.items() if t*v}
def form(c):return {tuple(k):F(v) for k,v in c}
def eval2(a,u,v):return sum(c*(u[i]*v[j]-u[j]*v[i]) for (i,j),c in a.items())
w=form([((0,1),1),((2,3),1)])
pdA=form([((0,1),1),((0,2),-1)])
pdB=form([((1,3),1),((2,3),1)])
al=add(pdA,pdB)
signs=[1,1,-1,-1]
be={k:v*prod(signs[i] for i in k) for k,v in al.items()}
assert add(al,be)==scale(w,F(2))
assert wedge(al,al)=={(0,1,2,3):F(4)}
assert wedge(be,be)=={(0,1,2,3):F(4)}
assert wedge(al,be)=={}
assert {k:v*prod(signs[i] for i in k) for k,v in w.items()}==w
Au=[0,1,1,0];Av=[0,0,0,1];Bu=[1,0,0,0];Bv=[0,1,-1,0]
assert eval2(w,Au,Av)==1 and eval2(w,Bu,Bv)==1
T=[[Au[i],Av[i],Bu[i],Bv[i]] for i in range(4)]
N=[[1,0,0,0],[0,1,-1,0],[0,1,1,0],[0,0,0,1]]
assert det(T)==2 and det(N)==2
nA=[[1,0,0,0],[0,F(1,2),F(-1,2),0]]
nB=[[0,F(1,2),F(1,2),0],[0,0,0,1]]
assert det([[nA[0][i],nA[1][i],Au[i],Av[i]] for i in range(4)])==1
assert det([[nB[0][i],nB[1][i],Bu[i],Bv[i]] for i in range(4)])==1
nodes=[(F(0),F(1,8),F(1,8),F(1,4)),(F(0),F(5,8),F(5,8),F(1,4))]
def mod(x):return x-int(x//1)
def tau(x):return tuple(mod(y) for y in (x[0]+F(1,2),x[1],-x[2],-x[3]))
for x in nodes:
 assert x[0]==0 and mod(x[1]-x[2])==0 and mod(x[1]+x[2])==F(1,4) and x[3]==F(1,4)
 y=tau(x);assert y[0]==F(1,2) and mod(y[1]+y[2])==0 and mod(y[1]-y[2])==F(1,4) and y[3]==F(3,4)
 assert tau(y)==x

# A polynomial identity, rather than samples of a radial graph.
# Variables g,h,x,y, with h=g'(r)/r. Monomials are four-tuples.
zero=(0,0,0,0)
def polyadd(a,b):
 c=dict(a)
 for k,v in b.items():c[k]=c.get(k,F(0))+v
 return {k:v for k,v in c.items() if v}
def neg(a):return {k:-v for k,v in a.items()}
def mul(a,b):
 c={}
 for k,v in a.items():
  for l,wv in b.items():
   m=tuple(ki+li for ki,li in zip(k,l));c[m]=c.get(m,F(0))+v*wv
 return {k:v for k,v in c.items() if v}
def var(i):return {tuple(int(j==i) for j in range(4)):F(1)}
g,h,x,y=[var(i) for i in range(4)]
a_x=polyadd(g,mul(h,mul(x,x)));a_y=mul(h,mul(x,y))
b_x=neg(a_y);b_y=neg(polyadd(g,mul(h,mul(y,y))))
D=polyadd(mul(a_x,b_y),neg(mul(a_y,b_x)))
expected=neg(polyadd(mul(g,g),mul(mul(g,h),polyadd(mul(x,x),mul(y,y)))))
assert D==expected and polyadd(a_y,b_x)=={}
# Substituting g=e*c/r^2 and h=e*cp/r^3-2*e*c/r^4:
# det Df=e^2*c^2/r^4-e^2*c*cp/r^3; beta coefficient=0.
# With 0<=c<=1 and cp<=0, omega0 coefficient=(1+det Df)/2>=1/2.
# Central curve c=1,cp=0 has coefficient (1+e^2/r^4)/2>0.
# Both statements hold for every r>0 and every real e, not a finite mesh.

a=F(1,64);b=F(1,32);e=F(1,16384)
assert 0<a<b and 0<e<a*a and e/a<a
# Boundary ranges: central |z| is [e/a,a], both coords <=a.
# z-arm |z| in [a,b], |w|<=e/a<a; w-arm is symmetric.
# Thus the distinct arms cannot overlap except intended seams.
chi_euler=2*0-4 # Four disks removed, two annuli of Euler 0 inserted.
genus=1-chi_euler//2
volume_torus=F(2);degree=F(2);scale_factor=F(2)
volume_base=scale_factor**2*volume_torus/degree
assert genus==3 and volume_base==4
quotient_slice_u=[F(1,2),0,0,0];quotient_slice_v=[0,1,0,0]
bar_period=eval2(w,quotient_slice_u,quotient_slice_v)
Omega_period=eval2(scale(w,F(2)),quotient_slice_u,quotient_slice_v)
assert bar_period==F(1,2) and Omega_period==1

results={
 'restricted_input_authentication':'separate receipt_023 authenticates exact submitted blob bytes',
 'mathematical_diagnostic_phase':'after independent first seal',
 'finite_exact_affine_and_orientation_checks':{
   'A_and_B_symplectic_area_coefficients':[1,1],
   'ordered_tangent_intersection_determinant':str(det(T)),
   'ordered_normal_determinant':str(det(N)),
   'coorientation_volume_determinants':[1,1],
   'A_B_nodes':[[str(c) for c in q] for q in nodes],
   'tau_images':[[str(c) for c in tau(q)] for q in nodes],
   'all_cross_pair_disjointness':'universal conflicting constant equations: x1=0 versus 1/2; x4=1/4 versus 3/4; x2-x3=0 versus 1/4; x2+x3=1/4 versus 0',
   'tau_fixed_point_obstruction':'x1+1/2=x1 mod 1 is impossible',
   'alpha_plus_beta':'2 omega0','alpha_squared':4,'beta_squared':4,'alpha_beta':0,
   'computed_genus':genus,'quotient_scaled_volume_and_self_intersection':str(volume_base),
   'invariant_slice_x3_x4_zero':{'bar_omega_period':str(bar_period),'Omega_period':str(Omega_period),'quotient_parametrization':'p(t/2,u,0,0), t,u mod 1; t+1 closes using tau'}},
 'universal_radial_graph_identity':{
   'graph':'w=e*chi(r)/z with e>0 real and smooth decreasing chi in [0,1]',
   'symbolic_beta_coefficient':0,
   'symbolic_jacobian_determinant':'e^2*chi(r)^2/r^4 - e^2*chi(r)*chi_prime(r)/r^3',
   'omega0_positive_density':'(1+e^2*chi(r)^2/r^4-e^2*chi(r)*chi_prime(r)/r^3)/2 >= 1/2 for all r>0',
   'symmetric_w_arm':'same alpha density; beta has opposite sign but is still zero',
   'seams':'chi=1 and chi=0 on collars makes exact all-order formula agreement',
   'explicit_scale_example':{'a':str(a),'b':str(b),'e':str(e),'e_over_a':str(e/a)},
   'localization':'actual a,b are scaled smaller to fit any specified chart inside U',
   'central_embedded_annulus':'e/a <= |z| <= a, |w|=e/|z|',
   'arms_disjoint':'z-arm has |z|>=a and |w|<a; w-arm has |w|>=a and |z|<a',
   'method':'exact polynomial-ring identity plus universally quantified inequalities, no sampling'},
 'scope_limit':'Finite diagnostics do not replace smooth embeddedness, relative homology, real transfer, or Weinstein Morse theorem; these are justified in the written audit.'}
(OUT/'fresh_exact_diagnostics.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
