import datetime,json,os,pathlib
import sympy as s
import mpmath as mp
out=pathlib.Path(__file__).parent
r=s.sqrt(13);P=[s.Matrix([2,0]),s.Matrix([2*(1-r)/3,s.sqrt(2*r-5)/3]),s.Matrix([2*(1-r)/3,-s.sqrt(2*r-5)/3])]
lam=(8*r-20)/9
exact=[]
def exactzero(v,name):
 if s.simplify(v)!=0:raise RuntimeError(name)
 exact.append(name)
def solve(A,B,F):
 M=s.Matrix([(A-F).T,(B-F).T]);rhs=s.Matrix([A.dot(A-F),B.dot(B-F)])
 return M.inv()*rhs
for i,A in enumerate(P):
 B=P[(i+1)%3];prev=P[(i-1)%3]
 exactzero(A[0]**2/4+A[1]**2-1,'odd_vertex_'+str(i))
 n=s.Matrix([B[1]-A[1],A[0]-B[0]])
 exactzero(n.dot(A)**2-(4-lam)*n[0]**2-(1-lam)*n[1]**2,'odd_tangency_'+str(i))
 length=s.sqrt((B-A).dot(B-A));last=s.sqrt((A-prev).dot(A-prev));t=s.Matrix([-2*A[1],A[0]/2])
 exactzero(((A-prev)/last-(B-A)/length).dot(t),'odd_reflection_'+str(i))
qs=[solve(P[i],P[(i+1)%3],s.zeros(2,1)) for i in range(3)]
mean=s.simplify(sum(qs,s.zeros(2,1))/3)
exactzero(mean[0]-(35-5*r)/24,'odd_nonzero_centroid_formula')
exactzero(mean[1],'odd_centroid_y')
if mean[0].is_positive is not True:raise RuntimeError('odd_nonzero')
if s.simplify(sum(qs+qs,s.zeros(2,1))/6-mean)!=s.zeros(2,1):raise RuntimeError('odd_repeat')
if lam.is_positive is not True or s.simplify(1-lam).is_positive is not True:raise RuntimeError('odd_lambda_domain')
if len(set(tuple(A) for A in P))!=3:raise RuntimeError('odd_least_period')
negative_mean=s.simplify(sum([solve(-P[i],-P[(i+1)%3],s.zeros(2,1)) for i in range(3)],s.zeros(2,1))/3)
exactzero(negative_mean[0]+mean[0],'reflected_odd_centroid_x')
exactzero(negative_mean[1]+mean[1],'reflected_odd_centroid_y')
CP=[s.Matrix([s.cos(s.pi*i/3),s.sin(s.pi*i/3)]) for i in range(6)]
cmean=s.simplify(sum([solve(CP[i],CP[(i+1)%6],s.zeros(2,1)) for i in range(6)],s.zeros(2,1))/6)
exactzero(cmean[0],'circle_mean_x');exactzero(cmean[1],'circle_mean_y')
# Numerical orbit controls generated solely from tangent points of the inner
# ellipse obtained by a linear map from unit-circle tangency.
mp.mp.dps=65
def norm(v):return mp.sqrt(sum(x*x for x in v))
def step(P,a,b,lam):
 ac=mp.sqrt(a*a-lam);bc=mp.sqrt(b*b-lam);u=(P[0]/ac,P[1]/bc);uu=u[0]*u[0]+u[1]*u[1];rad=mp.sqrt(uu-1)
 for sign in (-1,1):
  z=((u[0]-sign*u[1]*rad)/uu,(u[1]+sign*u[0]*rad)/uu)
  d=(ac*z[0]-P[0],bc*z[1]-P[1])
  tau=-2*(P[0]*d[0]/(a*a)+P[1]*d[1]/(b*b))/(d[0]*d[0]/(a*a)+d[1]*d[1]/(b*b))
  B=(P[0]+tau*d[0],P[1]+tau*d[1])
  if P[0]*B[1]-P[1]*B[0]>0:return B
 raise RuntimeError('no left chord')
def orbit(a,b,lam,N,t):
 P=(a*mp.cos(t),b*mp.sin(t));vertices=[P];w=mp.mpf('0')
 for i in range(N):
  B=step(P,a,b,lam)
  dt=mp.atan2(B[1]/b,B[0]/a)-mp.atan2(P[1]/b,P[0]/a)
  if dt<0:dt+=2*mp.pi
  if not 0<dt<mp.pi:raise RuntimeError('angular orientation')
  w+=dt;vertices.append(B);P=B
 return vertices,w
def anti(P,Q,h):
 r=(P[0]-h,P[1]);t=(Q[0]-h,Q[1]);D=r[0]*t[1]-r[1]*t[0];u=P[0]*r[0]+P[1]*r[1];v=Q[0]*t[0]+Q[1]*t[1]
 return ((u*t[1]-r[1]*v)/D,(r[0]*v-u*t[0])/D)
checks=0;maxerr=mp.mpf('0');rows=[]
def near(v,scale=1):
 global checks,maxerr
 err=abs(v)/max(1,abs(scale));maxerr=max(maxerr,err)
 if err>mp.mpf('1e-38'):raise RuntimeError('numerical condition '+mp.nstr(err,20))
 checks+=1
for av,bv,N,p in [('2','1',10,3),('1.0001','1',8,3),('5','1',16,1)]:
 a=mp.mpf(av);b=mp.mpf(bv);lo=b*b*mp.mpf('1e-18');hi=b*b*(1-mp.mpf('1e-24'))
 fl=orbit(a,b,lo,N,0)[1]-2*mp.pi*p;fh=orbit(a,b,hi,N,0)[1]-2*mp.pi*p
 if fl>=0 or fh<=0:raise RuntimeError('unbracketed rotation')
 for k in range(165):
  mid=(lo+hi)/2;fm=orbit(a,b,mid,N,0)[1]-2*mp.pi*p
  if fm>0:hi=mid
  else:lo=mid
 lam=(lo+hi)/2;c=mp.sqrt(a*a-b*b);phases=[];raw_perimeters=[]
 for t in [mp.mpf('0.17'),mp.mpf('0.81'),mp.mpf('1.31')]:
  points,w=orbit(a,b,lam,N,t)
  near(w-2*mp.pi*p);near(norm((points[-1][0]-points[0][0],points[-1][1]-points[0][1])),a)
  lengths=[norm((points[i+1][0]-points[i][0],points[i+1][1]-points[i][1])) for i in range(N)]
  L=sum(lengths);raw_perimeters.append(L);C2=[];SC=[]
  for i in range(N):
   A=points[i];B=points[i+1];prev=points[(i-1)%N]
   near(norm((A[0]+points[(i+N//2)%N][0],A[1]+points[(i+N//2)%N][1])),a)
   incoming=((A[0]-prev[0])/lengths[(i-1)%N],(A[1]-prev[1])/lengths[(i-1)%N]);outgoing=((B[0]-A[0])/lengths[i],(B[1]-A[1])/lengths[i]);tangent=(-a*A[1]/b,b*A[0]/a)
   near((incoming[0]-outgoing[0])*tangent[0]+(incoming[1]-outgoing[1])*tangent[1],a)
   nx=B[1]-A[1];ny=A[0]-B[0];W=a*a*nx*nx+b*b*ny*ny;C2.append(a*a*nx*nx/W);SC.append(a*b*nx*ny/W)
  H=a*a/(c*c)*(1-b*L/(2*a*mp.sqrt(lam)*N));K=a*a*b*b-lam*c*c
  near(sum(C2)/N-H);near(sum(SC));cent=[]
  for h in [mp.mpf('0'),c,-c]:
   Q=[anti(points[i],points[i+1],h) for i in range(N)];mean=(sum(q[0] for q in Q)/N,sum(q[1] for q in Q)/N);target=h*(-1+K*H/(a*a*(b*b-lam)))
   near(mean[0]-target,a);near(mean[1],a);cent.append([mp.nstr(x,16) for x in mean])
  phases.append({'phase':str(t),'perimeter':mp.nstr(L,20),'centroids':cent})
 for L in raw_perimeters[1:]:near(L-raw_perimeters[0],a)
 rows.append({'a':av,'b':bv,'N':N,'winding':p,'lambda':mp.nstr(lam,50),'phases':phases})
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'exact_odd_checks':len([v for v in exact if not v.startswith('circle')])+4,'exact_circle_checks':len([v for v in exact if v.startswith('circle')]),'exact_odd_centroid':['(35-5*sqrt(13))/24','0'],'numerical_conditions':checks,'precision_digits':mp.mp.dps,'tolerance_relative':'1e-38','max_scaled_error':mp.nstr(maxerr,20),'numeric_cases':rows,'limitations':'Finite numerical checks are falsification controls only; do not prove exact closure or the all-period theorem.'}
(out/'independent_edge_orbit_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='numeric_cases'},indent=2))
