#!/usr/bin/env python3
"""Independent real geometry: caustic tangency, reflection dynamics, tangent normals.

No submitted checker or prior audit helper is imported. Jacobi functions are used
only to choose ellipse axes for known rational rotation numbers, not to build any
billiard vertex or outer vertex.
"""
import mpmath as mp, math, json, datetime
mp.mp.dps=180
results=[];worst={};assertions=0
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def scale(t,x):return tuple(t*a for a in x)
def norm(x):return mp.sqrt(dot(x,x))
def ck(x,key,tol=mp.mpf('1e-100')):
 global assertions
 x=abs(x);worst[key]=max(worst.get(key,mp.mpf(0)),x);assertions+=1
 if x>tol:raise AssertionError((key,mp.nstr(x,20)))
def meet(n,h,m,g):
 # Independently solve the two equations by mpmath's LU routine.
 z=mp.lu_solve(mp.matrix([list(n),list(m)]),mp.matrix([h,g]))
 return tuple(z)
def avg(Q):return tuple(sum(p[j] for p in Q)/len(Q) for j in (0,1))
def anti(R,M):
 Q=[];dets=[]
 for i in range(len(R)):
  X=R[i];Y=R[(i+1)%len(R)];n=sub(X,M);m=sub(Y,M)
  dets.append(n[0]*m[1]-n[1]*m[0]);U=meet(n,dot(n,X),m,dot(m,Y));Q.append(U)
  ck(dot(n,sub(U,X))/(1+norm(n)*norm(U)),'direct_antipedal_incidence')
 return Q,dets
def area_centroid(Q):
 cr=[Q[i][0]*Q[(i+1)%len(Q)][1]-Q[(i+1)%len(Q)][0]*Q[i][1] for i in range(len(Q))]
 A=sum(cr)/2
 return A,tuple(sum(cr[i]*(Q[i][j]+Q[(i+1)%len(Q)][j]) for i in range(len(Q)))/(6*A) for j in (0,1))
def axes(k,N,tau):
 kp=mp.sqrt(1-k*k);v=2*mp.ellipk(k*k)*tau/N
 a=mp.ellipfun('dn',v,k*k)/mp.ellipfun('cn',v,k*k);b=kp/mp.ellipfun('cn',v,k*k)
 return a,b,kp
def billiard(a,b,kp,N,theta):
 P=(a*mp.cos(theta),b*mp.sin(theta))
 # Tangent point on caustic (cos t,kp sin t), solving P_x cos t+P_y sin t/kp=1.
 rho=mp.sqrt(P[0]**2+(P[1]/kp)**2)
 t=mp.atan2(P[1]/kp,P[0])+mp.acos(1/rho)
 d=sub((mp.cos(t),kp*mp.sin(t)),P);d=scale(1/norm(d),d)
 initial=P;points=[]
 for i in range(N):
  points.append(P)
  AA=d[0]**2/a**2+d[1]**2/b**2
  BB=2*(P[0]*d[0]/a**2+P[1]*d[1]/b**2)
  length=-BB/AA;assert length>0
  nextP=add(P,scale(length,d))
  # A segment must have a repeated intersection with the fixed caustic.
  ca=d[0]**2+d[1]**2/kp**2
  cb=2*(P[0]*d[0]+P[1]*d[1]/kp**2)
  cc=P[0]**2+P[1]**2/kp**2-1
  ck((cb**2-4*ca*cc)/(1+abs(cb**2)+abs(4*ca*cc)),'direct_caustic_discriminant')
  n=(nextP[0]/a**2,nextP[1]/b**2)
  d=sub(d,scale(2*dot(d,n)/dot(n,n),n));P=nextP
 ck(norm(sub(P,initial))/(1+a+b),'direct_reflection_closure')
 for p in points:ck(p[0]**2/a**2+p[1]**2/b**2-1,'original_ellipse_incidence')
 normals=[(p[0]/a**2,p[1]/b**2) for p in points]
 R=[meet(normals[i],1,normals[(i+1)%N],1) for i in range(N)]
 winding=sum(mp.atan2(points[i][0]*points[(i+1)%N][1]-points[i][1]*points[(i+1)%N][0],
                       points[i][0]*points[(i+1)%N][0]/(a/b)+points[i][1]*points[(i+1)%N][1]*(a/b)) for i in range(N))/(2*mp.pi)
 # Normalized angular coordinates give cross numerator /ab and dot /a²,/b²;
 # atan2 above multiplies both by ab, so it is exactly the winding angle.
 return points,R,winding
cases=[('.17',4,1),('.63',6,1),('.94',8,1),('.63',8,3),('.94',10,3),('.31',14,5),('.94',18,7),('1e-15',8,3),('0.999999999999999',10,3),('.63',30,7)]
for ks,N,tau in cases:
 k=mp.mpf(ks);a,b,kp=axes(k,N,tau);centroids=[];minimum=mp.inf
 for theta in (mp.mpf('.1'),mp.mpf('.71'),mp.mpf('1.53')):
  P,R,winding=billiard(a,b,kp,N,theta)
  ck(abs(winding)-tau,'direct_turning_number')
  mindist=min(norm(sub(P[i],P[j])) for i in range(N) for j in range(i))
  assert mindist>mp.mpf('1e-70') # all N vertices are distinct: genuine least period.
  Q,ds=anti(R,(k,0));c=avg(Q);centroids.append(c);minimum=min(minimum,min(abs(d) for d in ds))
  ck(c[1]/(1+norm(c)),'direct_focal_axis')
  Qm,_=anti(R,(-k,0));cm=avg(Qm);ck(norm(add(c,cm))/(1+norm(c)),'direct_focus_negation')
  if N==4:ck(norm(c)/(1+a+b),'direct_N4_origin')
 for c in centroids[1:]:ck(norm(sub(c,centroids[0]))/(1+norm(c)),'direct_phase_constancy')
 results.append({'k':ks,'N':N,'tau':tau,'positive_focus_centroid':[mp.nstr(x,35) for x in centroids[0]],'minimum_abs_antipedal_determinant':mp.nstr(minimum,25)})
# Original versus outer-locus focus control, using the ellipse through dynamic outer vertices.
k=mp.mpf('.63');N=6;tau=1;a,b,kp=axes(k,N,tau);K=mp.ellipk(k*k);v=2*K*tau/N
A=mp.ellipfun('dn',v,k*k)**2/mp.ellipfun('cn',v,k*k)**2;B=kp/mp.ellipfun('cn',v,k*k)**2
outer_focus=(mp.sqrt(A*A-B*B),mp.mpf(0));outer_c=[];area_c=[];vertex_c=[]
for theta in (mp.mpf('.1'),mp.mpf('.71')):
 P,R,_=billiard(a,b,kp,N,theta)
 for r in R:ck(r[0]**2/A**2+r[1]**2/B**2-1,'dynamic_outer_locus_incidence')
 q,_=anti(R,outer_focus);outer_c.append(avg(q))
 q,_=anti(R,(k,0));vertex_c.append(avg(q));area_c.append(area_centroid(q)[1])
outer_gap=norm(sub(*outer_c));area_gap=norm(sub(*area_c));assert outer_gap>mp.mpf('1e-10');assert area_gap>mp.mpf('1e-10')
# Repeated odd orbit has an even list length, but retains its odd centroid variation.
k=mp.mpf('.63');N=3;tau=1;a,b,kp=axes(k,N,tau);odd_c=[];repeat_c=[]
for theta in (mp.mpf('.1'),mp.mpf('.71')):
 P,R,_=billiard(a,b,kp,N,theta);q,_=anti(R,(k,0));odd_c.append(avg(q));q2,_=anti(R+R,(k,0));repeat_c.append(avg(q2));ck(norm(sub(odd_c[-1],repeat_c[-1])),'odd_repetition_preserves_mean')
odd_gap=norm(sub(*odd_c));assert odd_gap>mp.mpf('1e-10')
# Direct circle model, independent of the elliptic parameter limit.
circle=[]
for theta in (mp.mpf('.1'),mp.mpf('.71')):
 P=[(mp.cos(theta+2*mp.pi*3*j/8),mp.sin(theta+2*mp.pi*3*j/8)) for j in range(8)]
 R=[meet(P[j],1,P[(j+1)%8],1) for j in range(8)];Q,_=anti(R,(0,0));c=avg(Q);ck(norm(c),'direct_circle_centroid');circle.append(c)
print(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','decimal_digits':mp.mp.dps,'assertions':assertions,'cases':results,'maximum_residuals':{k:mp.nstr(v,20) for k,v in worst.items()},'negative_controls':{'outer_locus_own_focus_phase_gap':mp.nstr(outer_gap,35),'area_centroid_phase_gap':mp.nstr(area_gap,35),'odd_primitive_and_repeated_even_phase_gap':mp.nstr(odd_gap,35)},'method':'Direct Euclidean caustic tangency plus specular reflection; Jacobi functions select axes only; all outer and antipedal intersections solved independently by LU.','interval_certificate':False},indent=2))
