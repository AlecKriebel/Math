"""Independent PR140 geometric controls; never import the author verifier.
Exact rational chords + symbolic simplifications + high-precision periodic families.
Audit reproduction only, not a new central proof-search turn.
"""
from pathlib import Path
from fractions import Fraction as F
import datetime,hashlib,json,math,os,sys
import sympy as sp
import mpmath as mp
ROOT=Path(__file__).resolve().parent
counts={'exact_checks':0,'exact_chords':0,'symbolic_checks':0,'numeric_checks':0,'periodic_orbit_phases':0}
def check(v,label,group='exact_checks'):
 if not v:raise RuntimeError(label)
 counts[group]+=1
def inner(P,Q):return P[0]*Q[0]+P[1]*Q[1]
def minus(P,Q):return (P[0]-Q[0],P[1]-Q[1])
def negate(P):return (-P[0],-P[1])
def antipedal(A,B,M):
 # Direct absolute-coordinate equations, independently derived in initial note.
 r=minus(A,M);s=minus(B,M)
 rhs_A=inner(A,A)-inner(M,A);rhs_B=inner(B,B)-inner(M,B)
 determinant=r[0]*s[1]-r[1]*s[0]
 if determinant==0:raise RuntimeError('undefined antipedal vertex')
 return ((rhs_A*s[1]-rhs_B*r[1])/determinant,(r[0]*rhs_B-s[0]*rhs_A)/determinant)
def rational_direction(z):return ((1-z*z)/(1+z*z),2*z/(1+z*z))
geometries=[(10,6,8),(25,7,24),(29,20,21),(65,63,16),(101,99,20),(1000000,600000,800000)]
mid_slopes=[F(-7,3),F(-4,9),F(0),F(2,7),F(5,4),F(1),F(999,1000)]
half_slopes=[F(1,1000000),F(1,17),F(2,11),F(1,3),F(3,7),F(7,11),F(9,10),F(999999,1000000)]
for aa,bb,cc in geometries:
 a,b,c=map(F,(aa,bb,cc));check(a*a==b*b+c*c,'ellipse focus identity')
 for u in mid_slopes:
  C,S=rational_direction(u)
  for v in half_slopes:
   U,V=rational_direction(v);g=a*a*S*S+b*b*C*C
   lam=V*V*a*a*b*b/g
   if not (0<lam<b*b):continue
   counts['exact_chords']+=1;D=b*b-lam;K=a*a*b*b-lam*c*c
   A=(a*(C*U+S*V),b*(S*U-C*V));B=(a*(C*U-S*V),b*(S*U+C*V))
   check(inner(minus(B,A),minus(B,A))==4*lam*g*g/(a*a*b*b),'squared positive edge length')
   check(a*a*U*U-c*c*C*C==g*D/(b*b),'focal determinant positivity identity')
   check(a*U>c*abs(C),'focus determinant strict sign')
   q0=antipedal(A,B,(F(0),F(0)))
   check(antipedal(negate(A),negate(B),(F(0),F(0)))==negate(q0),'origin opposite cancellation')
   for h in (c,-c):
    M=(h,F(0));q=antipedal(A,B,M);r=antipedal(negate(A),negate(B),M)
    check(inner(minus(A,M),minus(q,A))==0,'first full antipedal line')
    check(inner(minus(B,M),minus(q,B))==0,'second full antipedal line')
    check(q==antipedal(B,A,M),'reversing an edge preserves intersection')
    check((q[0]+r[0])/2==h*(-1+K*C*C/(a*a*D)),'focal mean x')
    check((q[1]+r[1])/2==h*K*S*C/(a*b*D),'focal mean y')
   # Independently compute derivative of squared length for simultaneous
   # eccentric-angle motion, with d fixed.
   Ad=(-a*(S*U-C*V),b*(C*U+S*V));Bd=(-a*(S*U+C*V),b*(C*U-S*V))
   dl2=2*inner(minus(B,A),minus(Bd,Ad))
   check(dl2==8*V*V*c*c*S*C,'unconstrained derivative of squared length')
# Symbolic identities, no finite sampling used for these algebra reductions.
a,b,lam,X,Y,V,t=sp.symbols('a b lam X Y V t',positive=True)
c2=a*a-b*b;g=a*a*(1-X)+b*b*X
raw=(X*(a*a+c2*(1-X)-c2*(1-Y))-a*a*Y)/(a*a*Y-c2*X)
check(sp.cancel(raw-g*(X-Y)/(a*a*Y-c2*X))==0,'generic raw focal pair simplification','symbolic_checks')
Ycaustic=1-lam*g/(a*a*b*b);K=a*a*b*b-lam*c2
check(sp.cancel(raw.subs(Y,Ycaustic)-(-1+K*X/(a*a*(b*b-lam))))==0,'generic focal perimeter coefficient','symbolic_checks')
check(sp.cancel((a*a*Y-c2*X).subs(Y,Ycaustic)-g*(b*b-lam)/(b*b))==0,'generic positive determinant denominator','symbolic_checks')
gt=a*a*sp.sin(t)**2+b*b*sp.cos(t)**2
actual=sp.diff(2*V*sp.sqrt(gt),t)
check(sp.simplify(actual-2*V*c2*sp.sin(t)*sp.cos(t)/sp.sqrt(gt))==0,'generic unconstrained length derivative','symbolic_checks')
# Genuine oriented tangent iteration, solved via a positive quadratic in tan d.
# No author code or asserted antipodal pairing is used in the generator.
mp.mp.dps=75
def advance(a,b,lam,u):
 sn=mp.sin(u);cs=mp.cos(u)
 A=1-lam*(sn*sn/(a*a)+cs*cs/(b*b))
 B=-2*lam*sn*cs*(1/(b*b)-1/(a*a))
 C=-lam*(cs*cs/(a*a)+sn*sn/(b*b))
 root=mp.sqrt(B*B-4*A*C)
 z=-2*C/(B+root) if B>=0 else (-B+root)/(2*A)
 return u+2*mp.atan(z)
def closure_parameter(a,b,N,p):
 lo=mp.mpf('1e-70')*b*b;hi=(1-mp.mpf('1e-65'))*b*b
 target=2*mp.pi*p
 def f(x):
  u=mp.mpf(0)
  for i in range(N):u=advance(a,b,x,u)
  return u-target
 if not f(lo)<0<f(hi):raise RuntimeError('closure root bracket')
 for _ in range(245):
  mid=(lo+hi)/2
  if f(mid)>0:hi=mid
  else:lo=mid
 return (lo+hi)/2
def near(x,scale=1,tol='1e-48'):
 return abs(x)<=mp.mpf(tol)*max(1,abs(scale))
def centroid(P,M):
 Q=[antipedal(P[i],P[(i+1)%len(P)],M) for i in range(len(P))]
 return tuple(sum(q[j] for q in Q)/len(Q) for j in range(2))
pairs=[(4,1),(6,1),(8,1),(8,3),(10,1),(10,3),(12,1),(12,5),(14,3),(16,7)]
phases=[mp.mpf(0),mp.mpf('0.173'),mp.mpf('0.819'),mp.mpf('2.111')]
summary=[];max_error=mp.mpf(0)
for astr,bstr in [('2','1'),('3','2'),('1.00001','1')]:
 a,b=mp.mpf(astr),mp.mpf(bstr);c=mp.sqrt(a*a-b*b)
 for N,p in pairs:
  check(math.gcd(N,p)==1 and N%2==0 and p<N/2,'primitive numerical rotation data','numeric_checks')
  lam=closure_parameter(a,b,N,p);baseL=None;baseCentroid=None;errors=[]
  for phase in phases:
   us=[phase]
   for _ in range(N):us.append(advance(a,b,lam,us[-1]))
   P=[(a*mp.cos(u),b*mp.sin(u)) for u in us[:-1]]
   counts['periodic_orbit_phases']+=1
   err=abs(us[-1]-phase-2*mp.pi*p)
   check(near(err),'actual full orbit closure','numeric_checks')
   check(all(near(P[i][j]+P[(i+N//2)%N][j],a) for i in range(N) for j in range(2)),'independently observed half-period antipodality','numeric_checks')
   stationary=mp.mpf(0)
   for i in range(N):
    incoming=minus(P[i],P[(i-1)%N]);outgoing=minus(P[(i+1)%N],P[i])
    li=mp.sqrt(inner(incoming,incoming));lo=mp.sqrt(inner(outgoing,outgoing))
    force=(incoming[0]/li-outgoing[0]/lo,incoming[1]/li-outgoing[1]/lo)
    tangent=(-a*mp.sin(us[i]),b*mp.cos(us[i]))
    check(near(inner(force,tangent),a),'actual billiard reflection/stationarity','numeric_checks')
    midpoint=(us[i]+us[i+1])/2;stationary+=mp.sin(midpoint)*mp.cos(midpoint)
   check(near(stationary,N),'midpoint cross sum cancellation','numeric_checks')
   L=sum(mp.sqrt(inner(minus(P[(i+1)%N],P[i]),minus(P[(i+1)%N],P[i]))) for i in range(N))
   H=a*a/(c*c)*(1-b*L/(2*a*mp.sqrt(lam)*N));K=a*a*b*b-lam*c*c
   obs=[]
   for h in (mp.mpf(0),c,-c):
    M=(h,mp.mpf(0));Cen=centroid(P,M)
    target=mp.mpf(0) if h==0 else h*(-1+K*H/(a*a*(b*b-lam)))
    check(near(Cen[0]-target,a),'actual full antipedal centroid x','numeric_checks')
    check(near(Cen[1],a),'actual full antipedal centroid y','numeric_checks')
    reverse=centroid(list(reversed(P)),M)
    check(all(near(reverse[j]-Cen[j],a) for j in (0,1)),'reversing full orientation leaves centroid','numeric_checks')
    obs.append(Cen)
   if baseL is None:baseL=L;baseCentroid=obs
   else:
    check(near(L-baseL,L),'perimeter invariant across actual phases','numeric_checks')
    check(all(near(obs[k][j]-baseCentroid[k][j],a) for k in range(3) for j in (0,1)),'centroids invariant across actual phases','numeric_checks')
   errors.append(err);max_error=max(max_error,err)
  summary.append({'a':astr,'b':bstr,'least_period':N,'winding':p,'lambda':mp.nstr(lam,35),'perimeter':mp.nstr(baseL,35),'focus_plus_centroid_x':mp.nstr(baseCentroid[1][0],35),'phases':len(phases),'max_closure_error':mp.nstr(max(errors),8)})
# A repeated odd orbit labelled by an even list length: explicit boundary.
a,b=mp.mpf(2),mp.mpf(1);oddlam=closure_parameter(a,b,3,1);odd_centroids=[];repeat_centroids=[]
for phase in (mp.mpf(0),mp.pi):
 us=[phase]
 for _ in range(3):us.append(advance(a,b,oddlam,us[-1]))
 P=[(a*mp.cos(u),b*mp.sin(u)) for u in us[:-1]]
 C=centroid(P,(mp.mpf(0),mp.mpf(0)));R=centroid(P+P,(mp.mpf(0),mp.mpf(0)))
 check(all(near(C[j]-R[j]) for j in (0,1)),'odd repetition preserves odd centroid','numeric_checks')
 odd_centroids.append(C);repeat_centroids.append(R)
check(abs(repeat_centroids[0][0]-repeat_centroids[1][0])>mp.mpf('0.1'),'even list of repeated odd orbit violates centroid invariance','numeric_checks')
boundary={'a':'2','b':'1','lambda':mp.nstr(oddlam,40),'true_least_period':3,'list_length':6,'origin_centroids':[[mp.nstr(x,35) for x in C] for C in repeat_centroids],'interpretation':'Explicit counterexample to extending even parity to an even-length repetition of an odd primitive trajectory. Not a counterexample to the candidate least-period theorem.'}
result={'schema':'pr140-independent-geometric-variational-controls/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'mode':'optimized' if sys.flags.optimize else 'normal','python':sys.version,'SymPy':sp.__version__,'mpmath':mp.__version__,'decimal_precision':mp.mp.dps,'counts':counts,'status':'PASS','numeric_tolerance_relative_to_unit_or_axes':'1e-48','numeric_root_bisection_steps':245,'periodic_cases':summary,'repeated_odd_boundary':boundary,'max_periodic_closure_error':mp.nstr(max_error,8),'author_verifier_imported_or_executed':False,'other_family_or_imported_review_read':False,'no_new_central_proof_search_turn':True,'numerical_evidence_is_not_all_period_proof':True,'all_period_proof_mechanism':'Frozen independent opposite-edge geometry, classical Poncelet circle map plus finite cyclic action, and unconstrained first variation before imposing caustic relation.'}
out=ROOT/('GEOMETRIC_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'GEOMETRIC_CONTROLS_NORMAL.json')
if out.exists():raise RuntimeError('Preserve prior controls')
out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'UTC':result['UTC'],'PID':os.getpid(),'mode':result['mode'],'status':'PASS','counts':counts,'max_closure_error':result['max_periodic_closure_error'],'repeated_odd_centroids':boundary['origin_centroids']}))

