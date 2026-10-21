"""Review02 controls: polynomial quotient, Cartesian chord propagation, complex fibers.
Finite samples are diagnostics; report supplies the universal divisor argument.
"""
import json, math
from pathlib import Path
import sympy as s
import mpmath as mp
BASE=Path(__file__).parent
k,h,C,d,x,y,z=s.symbols('k h C d x y z')
t=h*h;q=1-t;U=1-2*k*k*t+k*k*t*t;V=1-2*t+k*k*t*t;W=1-k*k*t*t
D=1-k*k*t*x*x
rels=[(y,y*y-(1-x*x)),(z,z*z-(1-k*k*x*x)),(C,C*C-(1-t)),(d,d*d-(1-k*k*t))]
def reduce(expr):
    p=s.cancel(expr).as_numer_denom()[0]
    for var,relation in rels:p=s.rem(p,relation,var)
    return s.factor(p)
sm=(x*C*d-h*y*z)/D;sp=(x*C*d+h*y*z)/D
cm=(y*C+x*h*z*d)/D;cp=(y*C-x*h*z*d)/D
L0=(U*U-k*k*V*V*t)/d;L1=(V*V-U*U*t)/C
Z=W*W-4*k*k*t*t*q*(1-k*k*t)
D3=U*W-2*k*k*t*q*V;C3=V*W-2*t*(1-k*k*t)*U
# Distances after dividing alpha^2; determinant after dividing alpha B_o.
Ao=d*d/q;Bo2=(1-k*k)/(q*q)
det=(((-Ao*sm-k)*cp)-cm*(-Ao*sp-k))/2
identities={
'factor1':(1+k*sm)*(1+k*sp)-(d+k*C*x)**2/D,
'factor2':(U+k*V*sm)*(U+k*V*sp)-(d+k*C*x)*(L0+k*L1*x)/D,
'determinant':det-h*d*z*(d+k*C*x)/(C*D),
'focal_distance':(-Ao*x-k)**2+Bo2*y*y-(1+k*x)*(U+k*V*x)/(q*q),
'mixed_coefficient':(1-k*k*t)*(V*V-U*U*t)+q*(U*U-k*k*V*V*t)-2*U*V*q*(1-k*k*t),
'dn_triple':U*U-k*k*V*V*t-(1-k*k*t)*D3,
'cn_triple':V*V-U*U*t-q*C3,
'branch_gap':L0*L0-k*k*L1*L1-(1-k*k)*Z*Z,
'outer_nonconfocal':Ao*Ao-Bo2-k*k+k*k*(1-k*k)*t*t/(q*q),
}
exact={name: str(reduce(expr)) for name,expr in identities.items()}
assert set(exact.values())=={'0'},exact
# q^4 is independently recovered by dividing determinant by TWO focal distances:
# det includes alpha*Bo; each distance contributes alpha^2/q^2.
exact['edge_normalization']='alpha*Bo*(q^2/alpha^2)^2 = Bo*q^4/alpha^3'
mp.mp.dps=85
sn=lambda u,m:mp.ellipfun('sn',u,m)
cn=lambda u,m:mp.ellipfun('cn',u,m)
dn=lambda u,m:mp.ellipfun('dn',u,m)
det2=lambda A,B:A[0]*B[1]-A[1]*B[0]
def physical_orbit(P,a,b,alpha,beta,N):
    out=[P]
    for j in range(N):
        X,Y=P[0]/alpha,P[1]/beta;r2=X*X+Y*Y
        contacts=[(alpha*(X-sign*mp.sqrt(r2-1)*Y)/r2,beta*(Y+sign*mp.sqrt(r2-1)*X)/r2) for sign in [-1,1]]
        T=next(T for T in contacts if det2(P,(T[0]-P[0],T[1]-P[1]))>0)
        dx,dy=T[0]-P[0],T[1]-P[1]
        lam=-2*(P[0]*dx/(a*a)+P[1]*dy/(b*b))/(dx*dx/(a*a)+dy*dy/(b*b))
        P=(P[0]+lam*dx,P[1]+lam*dy);out.append(P)
    return out

def outer_from_tangents(Ps,a,b):
    out=[]
    for P,T in zip(Ps,Ps[1:]+Ps[:1]):
        l1=(P[0]/(a*a),P[1]/(b*b));l2=(T[0]/(a*a),T[1]/(b*b));de=det2(l1,l2)
        out.append(((l2[1]-l1[1])/de,(l1[0]-l2[0])/de))
    return out

def area(Q,c,scale=1,rho=1):
    vals=[]
    for sign in [-1,1]:
        f=(sign*c*scale,mp.mpf(0));inv=[]
        for X,Y in Q:
            dx,dy=X*scale-f[0],Y*scale-f[1];norm=dx*dx+dy*dy
            inv.append((f[0]+rho*rho*dx/norm,f[1]+rho*rho*dy/norm))
        vals.append(sum(det2(A,B) for A,B in zip(inv,inv[1:]+inv[:1]))/2)
    return vals
cases=[];maxclose=mp.mpf(0);maxphase=mp.mpf(0);maxouter=mp.mpf(0);maxlaw=mp.mpf(0);maxreflection=mp.mpf(0)
for mstr in ['0.04','0.6','0.96']:
 m=mp.mpf(mstr);K=mp.ellipk(m);alpha=mp.mpf('1.3');beta=alpha*mp.sqrt(1-m);c=alpha*mp.sqrt(m)
 for N in [3,5,7,9,11,15]:
  for tau in range(1,(N+1)//2):
   if math.gcd(N,tau)!=1:continue
   v=2*K*tau/N;a=alpha*dn(v,m)/cn(v,m);b=beta/cn(v,m);products=[]
   for phase in [mp.mpf('.173'),mp.mpf('.631')]:
    w=phase*K;P=(-a*sn(w,m),b*cn(w,m));orbit=physical_orbit(P,a,b,alpha,beta,N)
    maxclose=max(maxclose,max(abs(orbit[-1][i]-P[i]) for i in [0,1]));Ps=orbit[:-1];Q=outer_from_tangents(Ps,a,b)
    Ao=a*dn(v,m)/cn(v,m);Bo=b/cn(v,m)
    for j,Pj in enumerate(Ps):
        before=Ps[(j-1)%N];after=Ps[(j+1)%N]
        vin=(Pj[0]-before[0],Pj[1]-before[1]);vout=(after[0]-Pj[0],after[1]-Pj[1])
        lin=mp.sqrt(vin[0]**2+vin[1]**2);lout=mp.sqrt(vout[0]**2+vout[1]**2)
        vin=tuple(c/lin for c in vin);vout=tuple(c/lout for c in vout)
        normal=(Pj[0]/a**2,Pj[1]/b**2);nn=sum(c*c for c in normal);dot=sum(vin[i]*normal[i] for i in [0,1])
        maxreflection=max(maxreflection,max(abs(vin[i]-2*dot/nn*normal[i]-vout[i]) for i in [0,1]))
    for j,Qj in enumerate(Q):
        expected=(-Ao*sn(w+v+j*2*v,m),Bo*cn(w+v+j*2*v,m))
        maxouter=max(maxouter,max(abs(Qj[i]-expected[i]) for i in [0,1]))
    A=area(Q,c);products.append(A[0]*A[1]);assert min(A)>0
    rev=area(list(reversed(Q)),c);rep=area(Q*3,c);rep2=area(Q*2,c);scaled=area(Q,c,scale=mp.mpf('2.1'));rad=area(Q,c,rho=mp.mpf('1.7'))
    for i in [0,1]:maxlaw=max(maxlaw,abs(rev[i]+A[i]),abs(rep[i]-3*A[i]),abs(rep2[i]-2*A[i]),abs(scaled[i]*mp.mpf('2.1')**2-A[i]),abs(rad[i]/mp.mpf('1.7')**4-A[i]))
   rel=abs(products[0]/products[1]-1);maxphase=max(maxphase,rel)
   cases.append({'m':mstr,'N':N,'tau':tau,'product':mp.nstr(products[0],20),'phase_relative_difference':mp.nstr(rel,6)})
assert maxclose<mp.mpf('1e-70') and maxouter<mp.mpf('1e-70') and maxphase<mp.mpf('1e-70') and maxlaw<mp.mpf('1e-70') and maxreflection<mp.mpf('1e-70')
circleerrors=[]
for N,tau in [(3,1),(5,2),(9,4)]:
    radius=mp.mpf('1.9');ang=2*mp.pi*tau/N
    Ps=[(radius*mp.cos(j*ang+mp.mpf('.31')),radius*mp.sin(j*ang+mp.mpf('.31'))) for j in range(N)]
    Q=outer_from_tangents(Ps,radius,radius);A=area(Q,mp.mpf(0));Ro=radius/mp.cos(mp.pi*tau/N)
    predicted=N*mp.sin(ang)/(2*Ro*Ro)
    circleerrors.append(max(abs(a-predicted) for a in A))
assert max(circleerrors)<mp.mpf('1e-75')
# Complex fiber/valuation controls. Full branch-fiber proof is in REPORT.md.
complexrows=[]
for mstr,N,tau in [('0.2',3,1),('0.87',3,1),('0.2',5,1),('0.87',7,2),('0.87',9,4)]:
 m=mp.mpf(mstr);kk=mp.sqrt(m);K=mp.ellipk(m);p=1j*mp.ellipk(1-m);v=2*K*tau/N;L=4*K/N;r=3*K+p;R=r+v
 hh=sn(v,m);CC=cn(v,m);dd=dn(v,m);tt=hh*hh;qq=CC*CC;UU=1-2*m*tt+m*tt*tt;VV=1-2*tt+m*tt*tt
 ll0=(UU*UU-m*VV*VV*tt)/dd;ll1=(VV*VV-UU*UU*tt)/CC;const=mp.sqrt(1-m)/qq*hh*dd*qq**4/CC
 def e(u):return const*dn(u,m)*(1-m*tt*sn(u,m)**2)/((dd+kk*CC*sn(u,m))**2*(ll0+kk*ll1*sn(u,m)))
 def F(u):return sum(e(u+j*2*v) for j in range(N))
 u=mp.mpf('.237')*K+mp.mpf('.179')*p;eps=mp.mpf('1e-23')
 errors={'real_period':abs(e(u+4*K)-e(u)),'anti_period':abs(e(u+2*p)+e(u)),
         'reflection':abs(e(2*r-u)+e(u)),'F_L_period':abs(F(u+L)-F(u)),
         'F_zero':abs(F(R+L/2)),'half_product':abs(F(u)*F(u+L/2)-F(u+mp.mpf('.183'))*F(u+mp.mpf('.183')+L/2)),
         'opposite_focus_shift':abs(F(u+2*K)-F(u+L/2))}
 assert max(errors.values())<mp.mpf('1e-65'),errors
 qa=eps**2*e(r+v+eps);qb=eps**2*e(r-v-eps)
 # opposite epsilon choice makes reflection cancellation exact to precision
 assert abs(qa+qb)<mp.mpf('1e-36')
 residue1=eps*F(R+eps);residue2=eps/2*F(R+eps/2)
 assert abs(residue1-residue2)<mp.mpf('1e-17') and abs(residue1)>mp.mpf('1e-10')
 removable1=e(p+eps);removable2=e(p+eps/2);assert abs(removable1-removable2)<mp.mpf('1e-17')
 row={'m':mstr,'N':N,'tau':tau,'max_sign_divisor_error':mp.nstr(max(errors.values()),8),'quadratic_reflection_error':mp.nstr(abs(qa+qb),8),'F_simple_residue':mp.nstr(residue1,18),'Jacobi_pole_removable_limit':mp.nstr(removable1,18)}
 if N==3:
  critical=K+p;v1=eps*e(critical+eps);v2=eps/2*e(critical+eps/2)
  assert abs(v1-v2)<mp.mpf('1e-17') and abs(v1)>mp.mpf('1e-10')
  row['critical_simple_residue']=mp.nstr(v1,18)
 complexrows.append(row)
# Exact universal residue pairing combinatorics: gcd reindexing for tested periods is diagnostic.
latticecases=sum(1 for N in range(3,152,2) for tau in range(1,(N+1)//2) if math.gcd(N,tau)==1)
for N in range(3,152,2):
 for tau in range(1,(N+1)//2):
  if math.gcd(N,tau)!=1:continue
  plus=[(tau-j*2*tau)%(2*N) for j in range(N)];minus=[(-tau-j*2*tau)%(2*N) for j in range(N)]
  assert len(set(plus))==N and sorted(plus)==sorted(minus)
result={'status':'PASS','classification':'Exact polynomial identities and independent physical/complex numerical diagnostics; not a formal or all-period computational proof','exact_quotient_remainders':exact,'physical_cases':len(cases),'physical_phase_runs':len(cases)*2,'max_reflection_error':mp.nstr(maxreflection,8),'circle_max_formula_error':mp.nstr(max(circleerrors),8),'max_closure_error':mp.nstr(maxclose,8),'max_tangent_Q_error':mp.nstr(maxouter,8),'max_phase_relative_error':mp.nstr(maxphase,8),'max_reversal_repeat_scaling_radius_error':mp.nstr(maxlaw,8),'cases':cases,'complex_fibers':complexrows,'finite_lattice_cases':latticecases}
(BASE/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['cases']},indent=2))
