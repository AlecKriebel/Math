"""Own exact and numerical controls for k906, not a replacement for PROOF.md."""
import json, math
import sympy as s
import numpy as np
from scipy.special import ellipj,ellipk
from collections import Counter
checks=Counter()
def eq(x,y,key):
 assert s.simplify(s.radsimp(x-y))==0,(key,s.simplify(x-y))
 checks[key]+=1
# Domain/axis identity: m denotes k^2, t=sn(v)^2.
m,t=s.symbols('m t',real=True);q=1-t;d2=1-m*t;V=1-2*t+m*t*t
assert s.expand(d2*d2-(1-m)-m*V)==0;checks['outer_axis_identity']+=1
assert s.expand(q*d2-m*V-(1-m)*(q+m*t*t))==0;checks['focus_inside_original_when_horizontal']+=1
# Algebraic data for the primitive 8/3 family.
p=s.Rational(25,144);mm=1-p*p;tt=s.Rational(96,221)
x=s.sqrt(tt);y=s.sqrt(1-tt);d=s.sqrt(1-mm*tt)
den=1-mm*x**4
S=2*x*y*d/den;C=(y*y-x*x*d*d)/den;D=(d*d-mm*x*x*y*y)/den
eq(S,s.Rational(12,13),'quarter_double_sn')
eq(C,s.Rational(5,13),'quarter_double_cn')
eq(D,s.Rational(5,12),'quarter_double_dn')
den2=1-mm*S**4
eq(2*S*C*D/den2,1,'half_double_sn')
eq((C*C-S*S*D*D)/den2,0,'half_double_cn')
eq((D*D-mm*S*S*C*C)/den2,p,'half_double_dn')
z=y/d;r=p*x/d
eq(x,4*s.sqrt(1326)/221,'quarter_sn_radical')
eq(y,5*s.sqrt(1105)/221,'quarter_cn_radical')
eq(d,5*s.sqrt(30)/36,'quarter_dn_radical')
eq(z,6*s.sqrt(1326)/221,'three_quarter_sn_radical')
eq(r,s.sqrt(1105)/221,'three_quarter_cn_radical')
AA=1/tt;BB=(1-mm*tt)/(p*tt);fc=221*s.sqrt(91)/288
eq(AA,s.Rational(221,96),'outer_A')
eq(BB,s.Rational(1105,144),'outer_B')
eq(BB*BB-AA*AA,fc*fc,'own_focus_vertical')
a2=1/tt;b2=(1-mm*tt)/tt
eq(a2-b2,mm,'confocality')
assert a2>1 and b2>p*p>0;checks['strictly_nested']+=1
pairs0=[(0,1),(S,-C),(-1,0),(S,C),(0,-1),(-S,C),(1,0),(-S,-C)]
pairsh=[(x,y),(x,-y),(-z,r),(z,r),(-x,-y),(-x,y),(z,-r),(-z,-r)]
def exact_area(pairs,focus):
 pts=[]
 for u,v in pairs:
  xx=-AA*u;yy=BB*v-focus
  pts.append((xx/(xx*xx+yy*yy),yy/(xx*xx+yy*yy)))
 return s.simplify(sum(pts[i][0]*pts[(i+1)%8][1]-pts[(i+1)%8][0]*pts[i][1] for i in range(8))/2)
pos=s.Rational(1473536,30525625);neg=-s.Rational(51985629184,12455533443925)*s.sqrt(30)
for sign in [1,-1]:
 eq(exact_area(pairs0,sign*fc),pos,'positive_phase_area')
 eq(exact_area(pairsh,sign*fc),neg,'negative_phase_area')
assert pos>0 and neg<0;checks['exact_IVT_signs']+=1
# Generic inversion equivariance after cancelling translations.
xx,yy,fx,fy=s.symbols('x y fx fy',real=True)
r2=(xx-fx)**2+(yy-fy)**2
for v in [fx+(xx-fx)/r2,fy+(yy-fy)/r2]:
 eq(v.xreplace({xx:-xx,yy:-yy,fx:-fx,fy:-fy}),-v,'inversion_half_turn')
# Numerical diagnostic: construct actual consecutive tangent intersections,
# rather than merely feeding the outer-locus formula to inversion.
worst={'outer_locus_relative_error':0.0,'half_turn_relative_error':0.0,'area_equality_relative_error':0.0,'caustic_tangency_relative_error':0.0}
cases=0;simple_positive=0
for N in range(4,22,2):
 for tau in range(1,N//2):
  if math.gcd(tau,N)!=1:continue
  assert tau%2==1;checks['primitive_even_turning_is_odd']+=1
  for k in [.05,.4,.8,.95,.99]:
   kk=k*k;K=ellipk(kk);v=2*K*tau/N;delta=2*v;_,cv,dv,_=ellipj(v,kk)
   beta=math.sqrt(1-kk);a=dv/cv;b=beta/cv;A=a*dv/cv;B=b/cv
   focus=np.array([math.sqrt(max(0,A*A-B*B)),math.sqrt(max(0,B*B-A*A))])
   for phase in [0,.123*K,.421*K,.891*K]:
    uu=phase-v+np.arange(N)*delta;ss,cc,_,_=ellipj(uu,kk);P=np.column_stack((-a*ss,b*cc))
    normals=P/np.array([a*a,b*b]);Q=np.array([np.linalg.solve(np.stack([normals[j],normals[(j+1)%N]]),np.ones(2)) for j in range(N)])
    sn,cn,_,_=ellipj(phase+np.arange(N)*delta,kk);formula=np.column_stack((-A*sn,B*cn))
    err=np.max(np.linalg.norm(Q-formula,axis=1))/(1+max(A,B));worst['outer_locus_relative_error']=max(worst['outer_locus_relative_error'],float(err));assert err<2e-10
    anti=np.max(np.linalg.norm(Q+np.roll(Q,N//2,axis=0),axis=1))/(1+max(A,B));worst['half_turn_relative_error']=max(worst['half_turn_relative_error'],float(anti));assert anti<2e-10
    # Line through billiard points is tangent to alpha=1,beta caustic.
    for j in range(N):
     edge=P[(j+1)%N]-P[j];n=np.array([-edge[1],edge[0]]);h=n@P[j]
     residual=abs(h*h-(n[0]*n[0]+beta*beta*n[1]*n[1]))/(1+h*h)
     worst['caustic_tangency_relative_error']=max(worst['caustic_tangency_relative_error'],float(residual));assert residual<2e-10
    ars=[]
    for f in [focus,-focus]:
     dd=Q-f;inv=dd/np.sum(dd*dd,axis=1)[:,None];ar=np.sum(inv[:,0]*np.roll(inv[:,1],-1)-inv[:,1]*np.roll(inv[:,0],-1))/2;ars.append(ar)
    err=abs(ars[0]-ars[1])/(1+abs(ars[0])+abs(ars[1]));worst['area_equality_relative_error']=max(worst['area_equality_relative_error'],float(err));assert err<2e-10
    if tau==1:assert min(ars)>0;simple_positive+=1
    cases+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),'exact_families':dict(checks),'star_witness':{'caustic_axes':['1','25/144'],'billiard_axes_squared':['221/96','27625/20736'],'outer_axes':['221/96','1105/144'],'own_focus_y':'221*sqrt(91)/288','least_period':8,'turning':3,'phase_0_area':str(pos),'phase_K_over_4_area':str(neg),'conclusion':'Continuity and exact opposite signs force a simultaneous zero; ratio is undefined there.'},'numerical_cases':cases,'numerical_simple_positive_cases':simple_positive,'numerical_max_errors':worst,'limitations':'The all-N equality, nonvanishing domain and IVT conclusion use PROOF.md. Numerical tests are diagnostics; exact star signs are symbolic.'},indent=2))
