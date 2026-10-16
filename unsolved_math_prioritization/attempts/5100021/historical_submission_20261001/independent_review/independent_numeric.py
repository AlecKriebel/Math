"""Independent110-digit physical-reflection and meromorphic diagnostics.
Real vertices are ray-traced, not sampled as a list of Jacobi points.
"""
import mpmath as mp
from math import gcd
from collections import Counter
import json
mp.mp.dps=110
C=Counter();worst=mp.mpf(0)
def near(x,y,key):
 global worst
 e=abs(x-y)/(1+abs(x)+abs(y));worst=max(worst,e)
 assert e<mp.mpf('1e-60'),(key,mp.nstr(e,15))
 C[key]+=1
def dot(x,y):return x[0]*y[0]+x[1]*y[1]
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def add(x,y):return [x[j]+y[j] for j in (0,1)]
def sub(x,y):return [x[j]-y[j] for j in (0,1)]
def mul(a,x):return [a*x[j] for j in (0,1)]
def area(P):return mp.fsum(det(P[j],P[(j+1)%len(P)]) for j in range(len(P)))/2

def derived(P,F,real=False):
 feet=[];anti=[]
 for i,p in enumerate(P):
  q=P[(i+1)%len(P)];v=sub(q,p)
  feet.append(add(p,mul(dot(sub(F,p),v)/dot(v,v),v)))
  n=sub(p,F);m=sub(q,F);a=dot(n,p);b=dot(m,q);d=det(n,m)
  if real:assert d>0;C['real_antipedal_line_determinant_positive']+=1
  anti.append([(a*m[1]-b*n[1])/d,(n[0]*b-m[0]*a)/d])
 if real:
  for i,p in enumerate(feet):assert det(sub(p,F),sub(feet[(i+1)%len(P)],F))>0;C['real_pedal_edge_positive']+=1
 return area(feet),area(anti)

def trace_orbit(N,a,b,beta,theta):
 p=[a*mp.cos(theta),b*mp.sin(theta)];start=p[:]
 # Solve initial caustic tangency on its affine unit circle.
 z=[p[0],p[1]/beta];rr=dot(z,z);J=[-z[1],z[0]]
 contacts=[add(mul(1/rr,z),mul(sign*mp.sqrt(rr-1)/rr,J)) for sign in (-1,1)]
 candidates=[sub([q[0],beta*q[1]],p) for q in contacts]
 v=next(q for q in candidates if det(p,q)>0);P=[]
 for j in range(N):
  P.append(p[:]);nedge=[-v[1],v[0]];hh=dot(nedge,p)
  near(hh*hh,nedge[0]**2+beta**2*nedge[1]**2,'physical_chord_confocal_tangency')
  t=-2*(p[0]*v[0]/a**2+p[1]*v[1]/b**2)/(v[0]**2/a**2+v[1]**2/b**2)
  q=add(p,mul(t,v));near(q[0]**2/a**2+q[1]**2/b**2,1,'physical_next_point_on_ellipse')
  normal=[q[0]/a**2,q[1]/b**2];v=sub(v,mul(2*dot(v,normal)/dot(normal,normal),normal));p=q
 for j in (0,1):near(p[j],start[j],'physical_closed_orbit')
 return P

families=0;signs=set();summaries=[]
for N in (4,8,12,16,20):
 for tau in range(1,N//2):
  if gcd(tau,N)!=1:continue
  for ks in ('.2','.6','.96'):
   k=mp.mpf(ks);par=k*k;beta=mp.sqrt(1-par);K=mp.ellipk(par);Kp=mp.ellipk(1-par)
   v=2*K*tau/N;delta=2*v;sn=lambda x:mp.ellipfun('sn',x,par);cn=lambda x:mp.ellipfun('cn',x,par);dn=lambda x:mp.ellipfun('dn',x,par)
   a=dn(v)/cn(v);b=beta/cn(v);T=lambda x:mp.fsum(dn(x+j*delta) for j in range(N));const=None;cf=None;cb=None
   for theta in (mp.mpf(0),mp.mpf(2)/7,mp.mpf(8)/9):
    P=trace_orbit(N,a,b,beta,theta);w=mp.ellipf(theta-mp.pi/2,par)
    for j,p in enumerate(P):
     near(p[0],-a*sn(w+j*delta),'physical_vs_canonical_vertex_x');near(p[1],b*cn(w+j*delta),'physical_vs_canonical_vertex_y')
    Ap,Bp=derived(P,[k,0],True);Am,Bm=derived(P,[-k,0],True)
    near(Ap,Am,'physical_both_focal_pedal_areas');near(Bp,Bm,'physical_both_focal_antipedal_areas')
    if const is None:const=Ap*Bp;cf=Ap/T(w+K+v);cb=Bp/T(w)
    near(Ap*Bp,const,'physical_target_product')
    near(Ap,cf*T(w+K+v),'physical_pedal_complementary_trace');near(Bp,cb*T(w),'physical_antipedal_trace')
    signs.add(int(mp.sign(Bp)))
    Ar,Br=derived(list(reversed(P)),[k,0]);near(Ar,-Ap,'traversal_reversal_pedal');near(Br,-Bp,'traversal_reversal_antipedal')
    scale=mp.mpf(7)/5;As,Bs=derived([mul(scale,p) for p in P],[scale*k,0]);near(As*Bs,scale**4*const,'fourth_power_scaling')
   if N==4:near(const,16*beta**2,'all_aspect_N4_product')
   families+=1
   if ks=='.6' and N<=12:summaries.append({'N':N,'turning':tau,'product':mp.nstr(const,18)})
   # Selected independent complex tests solve the source lines directly.
   if ks!='.6' or N>12:continue
   def direct_complex(w):
    P=[[-a*sn(w+j*delta),b*cn(w+j*delta)] for j in range(N)]
    return derived(P,[k,0])
   for w in (K/7+mp.j*Kp/9,K/3+mp.j*Kp/5,mp.j*Kp+mp.mpf('1e-14'),K+mp.j*Kp-v+mp.mpf('1e-14')):
    Ap,Bp=direct_complex(w)
    near(Ap,cf*T(w+K+v),'nonreal_direct_pedal_trace');near(Bp,cb*T(w),'nonreal_direct_antipedal_trace');near(Ap*Bp,const,'nonreal_direct_product')
   eps=mp.mpf('1e-14');p=mp.j*Kp;_,Bp=direct_complex(p+eps);_,Bm=direct_complex(p-eps)
   near(eps*eps*(Bp+Bm),0,'actual_double_pole_coefficient_cancellation')
   x=K/7+mp.j*Kp/9;_,B0=direct_complex(x);_,Be=direct_complex(-x);_,Ba=direct_complex(x+2*mp.j*Kp)
   near(B0,Be,'source_line_area_evenness');near(Ba,-B0,'source_line_area_imaginary_antiperiod')
   half=2*K/N;near(T(half+p),0,'actual_half_real_period_trace_zero')
   near(T(x)*T(x+half),T(0)*T(half),'nonreal_trace_product_divisor_control')
# Incorrect parity gives a varying product; no unsupported ratio division needed.
for N in (6,10):
 k=mp.mpf('.8');par=k*k;K=mp.ellipk(par);beta=mp.sqrt(1-par);v=2*K/N
 a=mp.ellipfun('dn',v,par)/mp.ellipfun('cn',v,par);b=beta/mp.ellipfun('cn',v,par);vals=[]
 for theta in (mp.mpf(0),mp.mpf(2)/7):
  P=trace_orbit(N,a,b,beta,theta);Ap,Bp=derived(P,[k,0],True);vals.append(Ap*Bp)
 assert abs(vals[0]-vals[1])>mp.mpf('1e-35');C['excluded_parity_product_varies']+=1
print(json.dumps({'status':'PASS','diagnostic_assertions':sum(C.values()),'families':dict(sorted(C.items())),'precision_decimal_digits':110,'maximum_scaled_error':mp.nstr(worst,15),'physical_billiard_families':families,'observed_antipedal_area_signs':sorted(signs),'sample_products':summaries,'limits':'Non-interval numerical diagnostics only. Real vertices are independently ray-traced; complex constructions use actual bilinear line equations. The all-period proof is audited in the written review.'},indent=2,sort_keys=True))
