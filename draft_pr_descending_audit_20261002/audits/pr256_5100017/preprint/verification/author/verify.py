"""Exact identities and numerical diagnostics for the k307 candidate.
The all-period proof is PROOF.md; diagnostics alone are not proof.
"""
import json, math
from collections import Counter
import sympy as s
import numpy as np
from scipy.special import ellipj,ellipk
C=Counter()
def ck(v,key):
 assert v,key
 C[key]+=1
def eq(a,b,key):ck(s.factor(s.cancel(s.expand(a-b)))==0,key)
a2,b2,lam=s.symbols('a2 b2 lam',nonzero=True);H=(a2+b2)/2;e=(a2-b2)/2;d=1-lam*(1/a2+1/b2);F=H*d+2*lam
A=a2*(1+lam*(1/a2-1/b2));B=b2*(1-lam*(1/a2-1/b2))
eq((A+B)/2,F,'adjacent_bilinear_cos_difference_coefficient');eq((A-B)/2,e*d,'adjacent_bilinear_cos_sum_coefficient')
eq(F+e*d,a2-lam*(a2/b2-1),'positive_first_factor');eq(F-e*d,b2+lam*(1-b2/a2),'positive_second_factor')
D,H,E=s.symbols('D H E',real=True);x,y,t,bt,hi,hj=s.symbols('x y t bt hi hj',nonzero=True)
hx=H+E*(x*x+x**-2)/2;hy=H+E*(y*y+y**-2)/2;hh=D*(y/x+x/y)/2+E*(x*y+1/(x*y))/2
cosdelta=(y/x+x/y)/2;cossum=(x*y+1/(x*y))/2
sq=H*H-E*E-(D*D-E*E)*cosdelta**2+2*E*(H-D)*cossum*cosdelta
eq(hx*hy-hh**2,sq,'squared_normal_relation')
Z=x*x;W=y*y;crossZ=(W/Z-Z/W)/(2*s.I)
eq(crossZ*(Z+W),-s.I*(1+(W/Z+Z/W)/2)*(W-Z),'unit_circle_edge_telescope')
eq(hh*(y/x-x/y)/(2*s.I),D*crossZ/2+E*(y*y-x*x+x**-2-y**-2)/(4*s.I),'area_edge_telescope')
Qi=hi*x-t*x*x;Qj=hj*y-t*y*y;barQi=hi/x-bt/x**2;barQj=hj/y-bt/y**2
edge=(barQi*Qj-Qi*barQj)*(Qi+Qj) # 2i times moment
ct=hj**2*x*x-hi**2*y*y+2*hi*hj*(x**3/y-y**3/x)
cb=hi**2*x*x/y**2-hj**2*y*y/x**2+hi*hj*(x/y-y/x)
pair=s.expand(edge+edge.xreplace({hi:-hi,hj:-hj}))
eq(pair,2*(t*ct+bt*cb-t*t*bt*(W/Z-Z/W)*(Z+W)),'antipodal_edge_moment_cancellation')
ct_sub=hy*x*x-hx*y*y+2*hh*(x**3/y-y**3/x)
cb_sub=hx*x*x/y**2-hy*y*y/x**2+hh*(x/y-y/x)
R=x*x/y**2-y*y/x**2;U=x**4/y**2-y**4/x**2
eq(ct_sub-D*U-s.Rational(3,2)*E*R,(D+H)*(x*x-y*y)+E*(x**4-y**4),'linear_t_edge_coboundary')
eq(cb_sub-(D/2+H)*R-E*U/2,E*(x*x-y*y)/2+E*(y**-2-x**-2),'linear_tbar_edge_coboundary')
# Pairing also removes area terms linear in t,bt.
areaedge=barQi*Qj-Qi*barQj
areapair=s.expand(areaedge+areaedge.xreplace({hi:-hi,hj:-hj}))
eq(areapair,2*(hi*hj*(y/x-x/y)+t*bt*(W/Z-Z/W)),'antipodal_area_cancellation')
# Unified formula and d=0 boundary case.
v,z,zb,rr,dd,FF,HH,EE=s.symbols('v z zb rr d F H E',real=True)
formula=z/2-(z*(D+2*HH+EE*v)+zb*(2*D*v+3*EE+v*rr/2))/(3*(2*D+rr))
unified=z/2-(z*(FF+2*HH*dd+EE*v*dd)+zb*(2*FF*v+3*EE*dd+v*dd*rr/2))/(3*(2*FF+dd*rr))
eq(formula.subs(D,FF/dd),unified,'unified_centroid_formula')
eq(unified.subs({dd:0,v:0}),z/3,'four_period_limit')
eq((2*EE*(HH-D)/(D*D-EE*EE)).subs(D,FF/dd),2*EE*dd*(HH*dd-FF)/(FF*FF-EE*EE*dd*dd),'v_eliminates_D')
# Direct rectangle shoelace with symbolic unrestricted pedal point.
A,B,mx,my=s.symbols('A B mx my',real=True)
def area_moment(Q):
 cr=[Q[i][0]*Q[(i+1)%len(Q)][1]-Q[i][1]*Q[(i+1)%len(Q)][0] for i in range(len(Q))]
 return s.expand(sum(cr)/2),tuple(s.expand(sum(cr[i]*(Q[i][j]+Q[(i+1)%len(Q)][j]) for i in range(len(Q)))) for j in (0,1))
SA,TA=area_moment([(A,my),(mx,B),(-A,my),(mx,-B)])
eq(SA,2*A*B,'rectangle_area');eq(TA[0],6*SA*mx/3,'rectangle_centroid_x');eq(TA[1],6*SA*my/3,'rectangle_centroid_y')
# Exact noncircular 8/3 star, constructed directly as billiard vertices.
a2=s.Rational(221,96);b2=s.Rational(27625,20736);L=s.Rational(125,96);aa=s.sqrt(a2);bb=s.sqrt(b2)
pairs=[(0,1),(-s.Rational(12,13),-s.Rational(5,13)),(1,0),(-s.Rational(12,13),s.Rational(5,13)),(0,-1),(s.Rational(12,13),s.Rational(5,13)),(-1,0),(s.Rational(12,13),-s.Rational(5,13))]
P=[s.Matrix([aa*u,bb*w]) for u,w in pairs]
def det(u,w):return u[0]*w[1]-u[1]*w[0]
for i,p0 in enumerate(P):
 p1=P[(i+1)%8];pminus=P[(i-1)%8];edge=p1-p0;n=s.Matrix([-edge[1],edge[0]]);c=n.dot(p0)
 eq(p0[0]**2/a2+p0[1]**2/b2,1,'exact_star_on_ellipse')
 eq(c*c,(a2-L)*n[0]**2+(b2-L)*n[1]**2,'exact_star_confocal_tangency')
 ck(s.simplify(det(p0,p1))>0,'exact_star_positive_successive_orientation')
 incoming=p0-pminus;outgoing=p1-p0;normal=s.Matrix([p0[0]/a2,p0[1]/b2])
 incoming=incoming/s.sqrt(incoming.dot(incoming));outgoing=outgoing/s.sqrt(outgoing.dot(outgoing))
 reflected=incoming-2*incoming.dot(normal)/normal.dot(normal)*normal
 for j in (0,1):eq(reflected[j],outgoing[j],'exact_star_physical_reflection')
ck(len(set(pairs))==8,'exact_star_least_period_eight')
winding=sum(1 if P[i][1]<=0<P[(i+1)%8][1] and s.simplify(det(P[i],P[(i+1)%8]))>0 else -1 if P[(i+1)%8][1]<=0<P[i][1] and s.simplify(det(P[i],P[(i+1)%8]))<0 else 0 for i in range(8))
ck(winding==3,'exact_star_winding_three')
HH=(a2+b2)/2;EE=(a2-b2)/2;dd=s.factor(1-L*(1/a2+1/b2));FF=s.factor(HH*dd+2*L);vv=s.factor(-4*EE*L*dd/(FF**2-EE**2*dd**2));rho2=s.factor(-2*FF/dd)
ck(dd<0 and FF>0 and rho2>0,'exact_star_undefined_circle_positive_radius')
# Direct projection checks at finite rational M and on the exact zero circle.
star_data=[]
for X,Y in [(s.Rational(13,10),s.Rational(7,10)),(s.Rational(1,3),s.Rational(-2,5)),(s.sqrt(rho2),s.Integer(0))]:
 Q=[]
 for p0 in P:
  n=s.Matrix([p0[0]/a2,p0[1]/b2]);m=s.Matrix([X,Y]);q=m+(1-n.dot(m))*n/n.dot(n);Q.append(tuple(s.simplify(c) for c in q))
 ar,moment=area_moment(Q);ar=s.factor(ar);G=2*FF+dd*(X*X+Y*Y)
 if G==0:eq(ar,0,'exact_star_zero_circle_area')
 else:
  zz=X+s.I*Y;pred=s.factor(zz/2-(zz*(FF+2*HH*dd+EE*vv*dd)+s.conjugate(zz)*(2*FF*vv+3*EE*dd+vv*dd*(X*X+Y*Y)/2))/(3*G))
  eq(moment[0]+s.I*moment[1],6*ar*pred,'exact_star_direct_centroid')
 star_data.append({'M':[str(X),str(Y)],'area':str(ar)})
# High-coverage double-precision checks, including actual tangency/reflection residuals.
# Jacobi sampling is only a generator; every generated edge is checked geometrically.
worst={'ellipse':0.,'caustic':0.,'reflection':0.,'antipodal':0.,'area_identity':0.,'centroid_formula':0.,'phase_centroid_variation':0.}
cases=0;simple_all_M=0;singular_cases=0
for N in range(4,25,2):
 for winding in range(1,N//2):
  if math.gcd(N,winding)!=1:continue
  for mm in [.04,.4,.8,.96]:
   K=ellipk(mm);step=4*K*winding/N;_,cv,dv,_=ellipj(step/2,mm);a=dv/cv;b=math.sqrt(1-mm)/cv;lam=a*a-1;H=(a*a+b*b)/2;e=(a*a-b*b)/2;d=1-lam*(1/a**2+1/b**2);F=H*d+2*lam;v=-4*e*lam*d/(F*F-e*e*d*d)
   if abs(d)<1e-12:d=0.;v=0.
   Mlist=[0j,.2+.7j,1.3+.7j,-4+3j]
   if d<0:Mlist.append(complex(math.sqrt(-2*F/d),0))
   previous={}
   for phase in [0,.071,.231,.413]:
    uu=phase*K+step*np.arange(N);sn,cn,_,_=ellipj(uu,mm);P=np.column_stack((-a*sn,b*cn));n=P/np.array([a*a,b*b]);g2=np.sum(n*n,axis=1);Q0=n/g2[:,None]
    def near(value,key):
     value=float(abs(value));worst[key]=max(worst[key],value);assert value<2e-8,(N,winding,mm,phase,key,value)
    near(np.max(abs(np.sum(P*P/np.array([a*a,b*b]),axis=1)-1)),'ellipse')
    near(np.max(abs(P+np.roll(P,N//2,axis=0)))/(1+a+b),'antipodal')
    edges=np.roll(P,-1,axis=0)-P;normals=np.column_stack((-edges[:,1],edges[:,0]));cs=np.sum(normals*P,axis=1)
    near(np.max(abs(cs*cs-(normals[:,0]**2+(1-mm)*normals[:,1]**2))/(1+cs*cs)),'caustic')
    incoming=np.roll(edges,1,axis=0);incoming=incoming/np.linalg.norm(incoming,axis=1)[:,None];outgoing=edges/np.linalg.norm(edges,axis=1)[:,None]
    reflected=incoming-2*np.sum(incoming*n,axis=1)[:,None]*n/g2[:,None]
    near(np.max(abs(reflected-outgoing)),'reflection')
    def am(Q):
     R=np.roll(Q,-1,axis=0);cross=Q[:,0]*R[:,1]-Q[:,1]*R[:,0]
     return cross.sum()/2,(cross[:,None]*(Q+R)).sum(axis=0)
    S0,_=am(Q0);assert S0>0
    for z in Mlist:
     M=np.array([z.real,z.imag]);Q=M+(1-n@M)[:,None]*n/g2[:,None];S,T=am(Q);G=2*F+d*abs(z)**2
     near((S-S0*G/(2*F))/(1+abs(S0)+abs(S)),'area_identity')
     if abs(G)<1e-9:
      singular_cases+=1;continue
     pred=z/2-(z*(F+2*H*d+e*v*d)+z.conjugate()*(2*F*v+3*e*d+v*d*abs(z)**2/2))/(3*G)
     actual=complex(*list(T/(6*S)))
     near((actual-pred)/(1+abs(pred)),'centroid_formula')
     if z in previous:near((actual-previous[z])/(1+abs(pred)),'phase_centroid_variation')
     previous[z]=actual
     if winding==1:assert S>0;simple_all_M+=1
     cases+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'exact_families':dict(sorted(C.items())),'star':{'billiard_axes_squared':[str(a2),str(b2)],'lambda':str(L),'d':str(dd),'F':str(FF),'v':str(vv),'undefined_circle_radius_squared':str(rho2),'direct_projection_controls':star_data},'numerical_diagnostics':{'defined_centroid_cases':cases,'simple_positive_area_cases':simple_all_M,'undefined_circle_cases':singular_cases,'maximum_normalized_residuals':worst},'limitations':'The all-N result and exact domain use the written proof; numerical diagnostics are not proof. The exact star is reused from campaign5100065, not claimed as a new construction.'},indent=2,sort_keys=True))
