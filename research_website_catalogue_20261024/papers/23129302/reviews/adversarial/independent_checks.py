"""Independent exact algebra and hostile rough-density controls; no packet imports.
Finite numerical feedback tests corroborate, never prove, universal statements.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import tanh, sqrt
import json, random
import sympy as s
x,r,z,y,a,beta,m,sv,t=s.symbols('x r z y a beta m sv t',real=True)
f=lambda x,r:((r+4)*x+r+1)/(2*r*x+2)
b=lambda z,r:(2*z-r-1)/(r+4-2*r*z)
h=lambda x,r:(x+r/4)/(1+r*x)
w=lambda x,y:(1-y*y/4)/(1-x*y)**2
p=s.Rational(1,2)-(r+y)/(4+r*y)
sigma=2*(y+r)/((r+1)*y+r+4)
tau=2*(y+r)/((r-1)*y-r+4)
identities={
 'f_inverse':s.factor(f(b(z,r),r)-z),
 'h_inverse':s.factor(h(h(x,r),-r)-x),
 'lift_conjugacy':s.factor(f(x,r)-(2*h(x,r)+s.Rational(1,2))),
 'b_parameter_derivative':s.factor(s.diff(b(z,r),r)+(1-4*b(z,r)**2)/(4-r*r)),
 'f_spatial_derivative':s.factor(s.diff(f(x,r),x)-(4-r*r)/(2*(1+r*x)**2)),
 'kernel_branch_identity':s.factor(w(b(x,r),y)*s.diff(b(x,r),x)+w(b(x+1,r),y)*s.diff(b(x+1,r),x)-p*w(x,sigma)-(1-p)*w(x,tau)),
 'kernel_y_zero':w(x,0)-1,
 'source_Assumption_I_margin':s.expand((25-50*a)-(16-100*a*a)-100*(a-s.Rational(1,4))**2-s.Rational(11,4)),
 'sigma_y_monotonicity':s.factor(s.diff(sigma,y)-2*(4-r*r)/((r+1)*y+r+4)**2),
 'sigma_r_monotonicity':s.factor(s.diff(sigma,r)-2*(4-y*y)/((r+1)*y+r+4)**2),
 'tau_y_monotonicity':s.factor(s.diff(tau,y)-2*(4-r*r)/((r-1)*y-r+4)**2),
 'tau_r_monotonicity':s.factor(s.diff(tau,r)-2*(4-y*y)/((r-1)*y-r+4)**2),
 'p_y_monotonicity':s.factor(s.diff(p,y)-(r*r-4)/(4+r*y)**2),
 'p_r_monotonicity':s.factor(s.diff(p,r)-(y*y-4)/(4+r*y)**2),
 'kernel_normalization':s.factor(s.integrate(w(x,y),x).subs(x,s.Rational(1,2))-s.integrate(w(x,y),x).subs(x,-s.Rational(1,2))-1),
}
# Normalization symbolic integration may carry a y=0 removable singularity: check directly too.
C=1+beta/4;den=1+beta*m
L=s.Matrix([[1/den,0],[-beta*t/den,1]])
det=s.expand((C*s.eye(2)-L.T*L).det()).subs(t*t,sv-m*m)
claimed=beta**2*((C*m-s.Rational(1,4))**2+C*(m-sv))/den**2
identities['rank_one_determinant']=s.factor(det-claimed)
U=(2+a)*(4-13*a*a)/(2*(2-a)**3)
identities['uniform_polynomial_certificate']=s.expand(7*(2-a)**3-5*(2+a)*(4-13*a*a)-(172*(a-s.Rational(13,43))**2+s.Rational(12,43)+58*a**3))
identities['kappa_margin']=str(s.Rational(21,25)**2-s.Rational(7,10))
for key,v in identities.items():
 if key!='kappa_margin' and v!=0: raise RuntimeError((key,v))
# Exact monotonicity corner bounds on invariant kernel and sensitivities.
corners=[]
for rr in (Q(-2,5),Q(2,5)):
 for yy in (Q(-2,3),Q(2,3)):
  pp=Q(1,2)-(rr+yy)/(4+rr*yy)
  ss=2*(yy+rr)/((rr+1)*yy+rr+4)
  tt=2*(yy+rr)/((rr-1)*yy-rr+4)
  assert 0<=pp<=1 and Q(-2,3)<=ss<=Q(2,3) and Q(-2,3)<=tt<=Q(2,3)
  corners.append({'r':str(rr),'y':str(yy),'p':str(pp),'sigma':str(ss),'tau':str(tt)})
# Positive zero-fiber section, plus deliberately broken zero-fiber assignment.
ww=list(map(Q,[0,0,0,4]));qgood=list(map(Q,[1,0,1,2]));qbad=list(map(Q,[0,0,0,2]))
p0=lambda v:[(v[0]+v[2])/2,(v[1]+v[3])/2]
v=p0(ww)
assert v==[0,2] and p0(qgood)==[1,1] and p0(qbad)!=[1,1]
assert sum(abs(qgood[i]-ww[i]) for i in range(4))/4==sum(abs(1-vv) for vv in v)/2==1
# Rough not-L2 density v=C|y|^(-3/4) on |y|<=1/4, with correlated old labels.
# Quantile: y=(1/4)*sign(2t-1)*|2t-1|^4, t uniform. Original branch A=1 iff t<1/2.
N=64;orig=[];new=[];terminal=[];labels=[]
for j in range(N):
 tt=Q(2*j+1,2*N);s0=2*tt-1;yy=Q(1,4)*(1 if s0>0 else -1)*s0**4
 A=1 if tt<Q(1,2) else 0
 old=(2*(yy+A)-1)/4;yn=tt-Q(1,2);yn0=(2*(yn+A)-1)/4
 assert (old<0)==(A==0) and (yn0<0)==(A==0)
 assert 2*yn0+Q(1,2)-A==yn
 orig.append(old);new.append(yn0);terminal.append(yn);labels.append(A)
assert sum(orig)==sum(new)==sum(terminal)==0
assert all((tt>0)==(A==0) for tt,A in zip(terminal,labels))
# Lebesgue flats of backward H0: endpoint atoms1/8,1/4,1/8; actual u has zero mass there.
flat_atoms={'minus_half':'1/8','zero':'1/4','plus_half':'1/8'}
assert sum(Q(vv) for vv in flat_atoms.values())==Q(1,2)
# Negative control: sup-close AC monotone onto staircase maps can keep TV distance1.
staircase=[{'cells':n,'sup_displacement':str(Q(1,2*n)),'derivative_L1_error':'1','pushforward_uniform_TV_error':'1','flat_atom_mass':'1/2'} for n in [2,16,256,4096]]
# Numerical, dimension-independent probability-space feedback control.
def inv(zz,rr):return (2*zz-rr-1)/(rr+4-2*rr*zz)
def V(zz,weights,A,B):
 lo,hi=-A,A
 for _ in range(100):
  rr=(lo+hi)/2
  residual=rr-A*tanh(B*sum(pp*inv(vv,rr) for pp,vv in zip(weights,zz))/A)
  if residual>0:hi=rr
  else:lo=rr
 rr=(lo+hi)/2
 return [inv(vv,rr) for vv in zz],rr
rng=random.Random(23129302);numerical=[];maxratio=0
for A in [.4,.2,1e-6]:
 for B in [6.00000001,16.]:
  for n in [1,2,7]:
   for rep in range(12):
    weights=[rng.random() for _ in range(n)];total=sum(weights);weights=[v/total for v in weights]
    zz=[rng.uniform(-.5,1.5) for _ in range(n)];zp=[rng.uniform(-.5,1.5) for _ in range(n)]
    if rep==0:zz=[-.5]*n;zp=[1.5]*n
    vv,rr=V(zz,weights,A,B);vp,rp=V(zp,weights,A,B)
    ratio=sqrt(sum(pp*(v-v1)**2 for pp,v,v1 in zip(weights,vv,vp))/sum(pp*(z-z1)**2 for pp,z,z1 in zip(weights,zz,zp)))
    maxratio=max(maxratio,ratio)
    if ratio>.84+1e-12:raise RuntimeError(('contraction control',A,B,n,ratio))
    numerical.append({'A':A,'B':B,'atoms':n,'ratio':ratio})
out={'exact_symbolic_identities':{k:str(v) for k,v in identities.items()},'exact_kernel_corner_bounds':corners,'zero_fiber_positive':{'w':list(map(str,ww)),'P0w':['0','2'],'correct_section_q':list(map(str,qgood)),'P0correct':list(map(str,p0(qgood))),'exact_L1_section_distance':'1'},'zero_fiber_negative':{'wrong_q':list(map(str,qbad)),'P0wrong':list(map(str,p0(qbad))),'detected':True},'rough_correlated_control':{'terminal_density':'C*|y|^(-3/4) on 0<|y|<=1/4; C=sqrt(2)/8; zero elsewhere','L1_mass':'1','L2_mass':'infinite','old_branch_labels':'A=0 iff y>0; A=1 iff y<0; maximally dependent on corrected future sign','corrected_initial_density':'2 on (-1/4,1/4), zero elsewhere; P0 corrected=1','all_three_means':'0 exactly by reflection','finite_quantile_points_checked':N,'pushforward_uniform_flat_atoms':flat_atoms,'actual_rough_u_mass_on_flats':'0; corrected actual law absolutely continuous'},'negative_sup_displacement_controls':staircase,'rank_one_degenerate_cases':{'beta_zero':'identity','q_constant':'constant direction contracts by 1/(1+beta*q), orthogonal complement identity','q_zero_and_q_one':'included analytically; no division by variance used'},'feedback_numerical_controls':{'count':len(numerical),'maximum_observed_ratio':maxratio,'all_below_21_over_25':True,'universal_proof':False},'limitations':['Only symbolic identities and stated analytic control constructions are exact universal evidence in their stated scope','Finite corner/numerical controls do not certify global convergence or H-shape','No source AssumptionII certification is supplied by this script']}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
