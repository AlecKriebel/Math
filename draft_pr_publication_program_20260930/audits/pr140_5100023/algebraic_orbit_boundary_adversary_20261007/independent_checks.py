#!/usr/bin/env python3
"""Independent physical billiard shooting and exact projective line checks.
No author code imported; all guards survive -O. Numerical tests falsify only.
"""
from pathlib import Path
from fractions import Fraction as F
from math import sin,cos,sqrt,hypot,atan2,pi,gcd,fsum,isfinite
from datetime import datetime,timezone
import os,sys,json,hashlib
START=datetime.now(timezone.utc).isoformat()
checks=0
class Rejected(ValueError):pass
def need(p,message):
 global checks
 if not p:raise Rejected(message)
 checks+=1
def dot(u,v):return u[0]*v[0]+u[1]*v[1]
def det(u,v):return u[0]*v[1]-u[1]*v[0]
def sub(u,v):return (u[0]-v[0],u[1]-v[1])
def norm(u):return hypot(*u)
def near(x,y,tol,msg):need(isfinite(float(x)) and isfinite(float(y)) and abs(x-y)<=tol,msg)
def antipedal(A,B,m):
 r=(A[0]-m,A[1]);s=(B[0]-m,B[1])
 d=det(r,s)
 need(d!=0,'singular antipedal')
 # Solve the absolute-coordinate line system, not the author relative system.
 k=dot(r,A);l=dot(s,B)
 return ((k*s[1]-l*r[1])/d,(r[0]*l-s[0]*k)/d)
def unit(t):return ((1-t*t)/(1+t*t),2*t/(1+t*t))
def exact_tests():
 rows=0
 for a,b,c in [(F(5),F(3),F(4)),(F(13),F(12),F(5)),(F(17),F(8),F(15))]:
  for t in [F(k,7) for k in range(-8,9)]:
   C,S=unit(t)
   for z in [F(k,17) for k in range(1,17)]:
    U,V=unit(z);D2=C*C/(a*a)+S*S/(b*b);lam=V*V/D2
    if not 0<lam<b*b:continue
    rows+=1;K=a*a*b*b-lam*c*c
    A=(a*(C*U+S*V),b*(S*U-C*V));B=(a*(C*U-S*V),b*(S*U+C*V))
    need(a*a*U*U-c*c*C*C==a*a*(b*b-lam)*D2,'determinant squared gap')
    for m in [-c,c]:
     Q=antipedal(A,B,m);R=antipedal((-A[0],-A[1]),(-B[0],-B[1]),m)
     need(dot((A[0]-m,A[1]),Q)==dot((A[0]-m,A[1]),A),'first line residual')
     need(dot((B[0]-m,B[1]),Q)==dot((B[0]-m,B[1]),B),'second line residual')
     # Independent closed solutions from sum/difference elimination.
     den=a*U-m*C
     x=(C*(a*a+c*c*(U*U-C*C))-m*a*U)/den
     y=(a*S*(b*b-c*c*(U*U+C*C))+2*m*c*c*C*S*U)/(b*den)
     need(Q==(x,y),'independent rational closed solution')
     need(Q[0]+R[0]==2*m*b*b*(C*C-U*U)/(b*b-lam),'x opposite chord')
     need(Q[1]+R[1]==2*m*K*S*C/(a*b*(b*b-lam)),'y opposite chord')
     need(Q[0]+R[0]==-2*m+2*m*K*C*C/(a*a*(b*b-lam)),'published pair expression')
    Q=antipedal(A,B,F(0));R=antipedal((-A[0],-A[1]),(-B[0],-B[1]),F(0))
    need(Q==(-R[0],-R[1]),'origin oddness')
 return rows

def orbit(a,b,lam,N,phase,validate=False):
 need(a>=b>0 and 0<lam<b*b,'invalid nested parameter')
 P=(a*cos(phase),b*sin(phase));initial=P
 n=(P[0]/(a*a),P[1]/(b*b));nn=norm(n)
 eta=sqrt(lam)/(a*b*nn)
 need(0<eta<1,'inadmissible starting tangent')
 v=(-eta*n[0]/nn-sqrt(1-eta*eta)*n[1]/nn,-eta*n[1]/nn+sqrt(1-eta*eta)*n[0]/nn)
 points=[];advance=0.0;max_tangent=0.;max_ellipse=0.;max_unit=0.
 for i in range(N):
  points.append(P)
  t=-2*(P[0]*v[0]/(a*a)+P[1]*v[1]/(b*b))/(v[0]*v[0]/(a*a)+v[1]*v[1]/(b*b))
  need(t>0 and isfinite(t),'positive second intersection')
  B=(P[0]+t*v[0],P[1]+t*v[1])
  u=(P[0]/a,P[1]/b);w=(B[0]/a,B[1]/b)
  angle=atan2(det(u,w),dot(u,w))
  need(0<angle<pi,'short oriented eccentric increment')
  advance+=angle
  if validate:
   max_ellipse=max(max_ellipse,abs(B[0]**2/a**2+B[1]**2/b**2-1))
   ch=sub(B,P);q=(ch[1],-ch[0]);r=dot(q,P)
   max_tangent=max(max_tangent,abs(r*r-((a*a-lam)*q[0]**2+(b*b-lam)*q[1]**2))/max(1.,r*r))
   max_unit=max(max_unit,abs(dot(v,v)-1))
  n=(B[0]/(a*a),B[1]/(b*b));fac=2*dot(v,n)/dot(n,n)
  v=(v[0]-fac*n[0],v[1]-fac*n[1]);P=B
 return points,P,advance,{'ellipse':max_ellipse,'tangent':max_tangent,'unit':max_unit}
def shoot(a,b,N,p):
 need(N>=3 and 0<2*p<N and gcd(N,p)==1,'primitive rotation scope')
 lo=b*b*1e-9;hi=b*b*(1-1e-11);target=2*pi*p
 need(orbit(a,b,lo,N,0)[2]<target<orbit(a,b,hi,N,0)[2],'shooting bracket')
 for k in range(64):
  mid=(lo+hi)/2
  if orbit(a,b,mid,N,0)[2]<target:lo=mid
  else:hi=mid
 return (lo+hi)/2

def analyze(a,b,N,p,lam,phase):
 P,end,adv,res=orbit(a,b,lam,N,phase,True);scale=max(a,b)
 closure=norm(sub(end,P[0]))/scale
 near(closure,0,2e-8,'closure')
 near(adv,2*pi*p,2e-8,'winding')
 for name,x in res.items():near(x,0,2e-8,'physical '+name)
 need(min(norm(sub(P[i],P[j])) for i in range(N) for j in range(i))>scale*1e-7,'distinct vertices')
 c=sqrt(max(0.,a*a-b*b));K=a*a*b*b-lam*c*c
 L=fsum(norm(sub(P[(i+1)%N],P[i])) for i in range(N))
 centroids=[];line_error=0.
 for m in [0.,c,-c]:
  Q=[antipedal(P[i],P[(i+1)%N],m) for i in range(N)]
  for i,q in enumerate(Q):
   for pt in [P[i],P[(i+1)%N]]:
    rr=(pt[0]-m,pt[1]);line_error=max(line_error,abs(dot(rr,q)-dot(rr,pt))/max(1.,abs(dot(rr,pt))))
  centroids.append((fsum(q[0] for q in Q)/N,fsum(q[1] for q in Q)/N))
 near(line_error,0,2e-8,'numerical antipedal residual')
 symmetric=max(norm((P[i][0]+P[(i+N//2)%N][0],P[i][1]+P[(i+N//2)%N][1])) for i in range(N))/scale if N%2==0 else None
 if N%2==0:
  near(symmetric,0,2e-8,'even half period pairing')
  H=(a*a/c**2)*(1-b*L/(2*a*sqrt(lam)*N)) if c else .5
  expected=c*(-1+K*H/(a*a*(b*b-lam))) if c else 0.
  near(centroids[0][0],0,2e-7*scale,'origin centroid x');near(centroids[0][1],0,2e-7*scale,'origin centroid y')
  near(centroids[1][0],expected,2e-7*scale,'focus plus formula');near(centroids[2][0],-expected,2e-7*scale,'focus minus formula')
  near(centroids[1][1],0,2e-7*scale,'focus plus y');near(centroids[2][1],0,2e-7*scale,'focus minus y')
 else:expected=None
 return {'a':a,'b':b,'N':N,'p':p,'lambda':lam,'lambda_over_b2':lam/(b*b),'phase':phase,'closure_relative':closure,'physical_residuals':res,'half_period_error':symmetric,'perimeter':L,'centroids':centroids,'formula_x':expected,'line_relative_error':line_error},P

def false_controls():
 controls=[]
 tests=[('guard_false',lambda:need(False,'false control')),
        ('singular_focus_line',lambda:antipedal((F(1),F(0)),(F(-1),F(0)),F(0))),
        ('invalid_lambda_zero',lambda:orbit(5.,3.,0.,4,0)),
        ('invalid_lambda_b2',lambda:orbit(5.,3.,9.,4,0)),
        ('repeated_odd_even_count',lambda:shoot(5.,3.,6,2)),
        ('corrupted_centroid',lambda:near(.01,0,1e-6,'corrupt centroid')),
        ('corrupted_focal_formula',lambda:near(.01,0,1e-6,'corrupt formula'))]
 for name,fn in tests:
  try:fn()
  except Rejected:controls.append(name)
  else:raise Rejected('negative control not rejected: '+name)
 return controls

def main():
 exact=exact_tests();rows=[]
 specs=[(5.,3.,4,1),(5.,3.,6,1),(5.,3.,8,1),(5.,3.,8,3),(5.,3.,10,3),(5.,3.,14,5),(2.,1.,10,1),(2.,1.,14,5),(1.00001,1.,6,1),(1.00001,1.,8,3),(5.,3.,30,1),(1.,1.,8,3),(15.,9.,8,3)]
 for a,b,N,p in specs:
  lam=shoot(a,b,N,p);group=[]
  for phase in [0.,.137,.731,1.491,2.637]:
   row,P=analyze(a,b,N,p,lam,phase);rows.append(row);group.append(row)
   if N%2==0:
    # Reversal and cyclic shift preserve the same full line intersections.
    for perm in [list(reversed(P)),P[3:]+P[:3],P+P]:
     q=[antipedal(perm[i],perm[(i+1)%len(perm)],sqrt(max(0.,a*a-b*b))) for i in range(len(perm))]
     C=(fsum(x[0] for x in q)/len(q),fsum(x[1] for x in q)/len(q))
     near(C[0],row['centroids'][1][0],1e-8*max(a,b),'orientation/shift/repetition x')
     near(C[1],row['centroids'][1][1],1e-8*max(a,b),'orientation/shift/repetition y')
  for row in group[1:]:
   near(row['perimeter'],group[0]['perimeter'],2e-8*max(a,b)*N,'perimeter phase invariance')
   for j in range(3):
    near(row['centroids'][j][0],group[0]['centroids'][j][0],4e-7*max(a,b),'centroid phase x')
    near(row['centroids'][j][1],group[0]['centroids'][j][1],4e-7*max(a,b),'centroid phase y')
 # Repeated odd triangles are a real excluded counterexample, not a central pair.
 lam=shoot(5.,3.,3,1);odd=[]
 for phase in [0.,.731,1.491]:
  row,P=analyze(5.,3.,3,1,lam,phase);Q=P+P
  qq=[antipedal(Q[i],Q[(i+1)%6],0.) for i in range(6)]
  C=(fsum(x[0] for x in qq)/6,fsum(x[1] for x in qq)/6)
  near(C[0],row['centroids'][0][0],1e-10,'odd repeated centroid x')
  near(C[1],row['centroids'][0][1],1e-10,'odd repeated centroid y')
  odd.append({'phase':phase,'repeated_N':6,'least_period':3,'origin_centroid':C})
 need(norm(sub(odd[0]['origin_centroid'],odd[1]['origin_centroid']))>.01,'odd repetition falsification witness')
 controls=false_controls()
 result={'schema':'pr140-independent-algebraic-orbit-tests/v1','verdict':'PASS','actual_PID':os.getpid(),'UTC_start':START,'UTC_end':datetime.now(timezone.utc).isoformat(),'optimized':sys.flags.optimize>0,'checks':checks,'exact_rational_chords':exact,'physical_periodic_family_count':len(specs),'physical_orbit_count':len(rows),'orbit_rows':rows,'repeated_odd_witnesses':odd,'negative_controls_rejected':controls,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'proof_status':'numerical and finite rational evidence supplement analytic proof; not a proof by testing','original_head':'9e908ae58b5ceee6a0825bbebd8acf565db55340','author_code_imported':False,'other_family_or_imported_review_read':False}
 out=Path(sys.argv[1]);out.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['verdict','actual_PID','UTC_end','optimized','checks','exact_rational_chords','physical_periodic_family_count','physical_orbit_count','negative_controls_rejected']}))
if __name__=='__main__':main()
