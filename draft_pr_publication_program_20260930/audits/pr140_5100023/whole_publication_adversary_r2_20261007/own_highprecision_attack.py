import mpmath as math
import json,pathlib,datetime
math.mp.dps=85
def dist(P,Q):return math.sqrt(sum((x-y)**2 for x,y in zip(P,Q)))
math.dist=dist
a,b=math.mpf(5),math.mpf(3); c=math.sqrt(a*a-b*b)
def point(t):return (a*math.cos(t),b*math.sin(t))
def step(t,lam):
    P=point(t); al=math.sqrt(a*a-lam); be=math.sqrt(b*b-lam); x,y=P[0]/al,P[1]/be; r2=x*x+y*y; q=math.sqrt(r2-1)
    for sg in [1,-1]:
      T=(al*(x-sg*q*y)/r2,be*(y+sg*q*x)/r2); d=(T[0]-P[0],T[1]-P[1]); r=-2*(P[0]*d[0]/a**2+P[1]*d[1]/b**2)/(d[0]**2/a**2+d[1]**2/b**2); Q=(P[0]+r*d[0],P[1]+r*d[1]); det=P[0]*Q[1]-P[1]*Q[0]
      if det>0:
        nt=math.atan2(Q[1]/b,Q[0]/a); dt=(nt-t)%(2*math.pi)
        if not 0<dt<math.pi:raise RuntimeError("arc direction")
        return t+dt
    raise RuntimeError("no tangent")
def orbit(t,lam,N):
    ts=[t]
    for _ in range(N):ts.append(step(ts[-1],lam))
    return ts
def close(N,k):
    lo,hi=math.mpf("1e-20"),b*b*(1-math.mpf("1e-70"))
    for _ in range(240):
      m=(lo+hi)/2; z=orbit(math.mpf(".271"),m,N)[-1]-math.mpf(".271")-2*math.pi*k
      if z<0:lo=m
      else:hi=m
    return (lo+hi)/2
def intersection(A,B,h):
    dx,dy=A[0]-h,A[1]; ex,ey=B[0]-h,B[1]; R=dx*dx+dy*dy; T=ex*ex+ey*ey; det=dx*ey-dy*ex
    return ((R*ey-dy*T)/det+h,(dx*T-R*ex)/det)
cases=[]; maxima={"closure":0.0,"reflection":0.0,"opposite":0.0,"moment_cross":0.0,"centroid":0.0,"perimeter":0.0}
for N,k in [(4,1),(6,1),(8,1),(8,3),(10,3),(12,5),(14,3),(18,7),(22,9)]:
  lam=close(N,k); baseL=None
  for initial in map(math.mpf,["0",".137",".7","1.21","2.919"]):
    ts=orbit(initial,lam,N); ps=[point(t) for t in ts]; ls=[]; cs=[]; ss=[]
    maxima["closure"]=max(maxima["closure"],abs(ts[-1]-initial-2*math.pi*k))
    refl=0.0
    for i in range(N):
      A=ps[i]; B=ps[i+1]; length=math.dist(A,B); ls.append(length); s=(ts[i]+ts[i+1])/2; cs.append(math.cos(s)); ss.append(math.sin(s)); Pprev=ps[(i-1)%N]; il=math.dist(Pprev,A); inc=((A[0]-Pprev[0])/il,(A[1]-Pprev[1])/il); out=((B[0]-A[0])/length,(B[1]-A[1])/length); tang=(-a*math.sin(ts[i]),b*math.cos(ts[i])); refl=max(refl,abs((inc[0]-out[0])*tang[0]+(inc[1]-out[1])*tang[1]))
      j=(i+N//2)%N; maxima["opposite"]=max(maxima["opposite"],math.hypot(A[0]+ps[j][0],A[1]+ps[j][1]))
    maxima["reflection"]=max(maxima["reflection"],refl); maxima["moment_cross"]=max(maxima["moment_cross"],abs(sum(x*y for x,y in zip(cs,ss))))
    L=sum(ls); K=a*a*b*b-lam*c*c; H=a*a/c**2*(1-b*L/(2*a*math.sqrt(lam)*N)); expected=c*(-1+K*H/(a*a*(b*b-lam)))
    if baseL is None:baseL=L
    maxima["perimeter"]=max(maxima["perimeter"],abs(L-baseL))
    for h in [0.0,c,-c]:
      qs=[intersection(ps[i],ps[i+1],h) for i in range(N)]; centroid=(sum(q[0] for q in qs)/N,sum(q[1] for q in qs)/N); e=0.0 if h==0 else expected*(h/c); maxima["centroid"]=max(maxima["centroid"],abs(centroid[0]-e),abs(centroid[1]))
    cases.append({"b2_minus_lambda":b*b-lam,"N":N,"winding":k,"initial":initial,"lambda":lam,"perimeter":L,"predicted_Fplus_x":expected})
if any(v>math.mpf("1e-60") for v in maxima.values()):raise RuntimeError(maxima)
r={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"PASS","mechanism":"Direct tangent-to-caustic intersections and bisection closure, independent of supplied programs","max_abs_residuals":maxima,"cases":cases,"limitations":["85-digit finite numerical tests are corroboration, not proof","Parameters approach elliptical endpoint without including degenerate caustic"]}; pathlib.Path(__file__).with_name("own_highprecision_attack_result.json").write_text(json.dumps(r,indent=2,default=str)+"\n");print(json.dumps({"status":r["status"],"cases":len(cases),"maxima":maxima},default=str))
