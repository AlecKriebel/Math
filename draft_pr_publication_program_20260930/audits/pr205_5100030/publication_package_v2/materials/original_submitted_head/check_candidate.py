#!/usr/bin/env python3
"""Exact algebra plus numerical diagnostics; the proof is the all-N telescoping argument."""
import json,math
import sympy as S
import mpmath as mp
checks=[]
def exact(name,expr,gens=(),relations=()):
    num=S.factor(S.together(expr).as_numer_denom()[0])
    if relations:
        num=S.groebner(relations,*gens,order='lex').reduce(S.expand(num))[1]
    assert S.simplify(num)==0,(name,num)
    checks.append(name)
s,c,d,sa,ca,da,m=S.symbols('s c d sa ca da m')
den=1-m*s*s*sa*sa
sp=(s*ca*da+sa*c*d)/den
cp=(c*ca-s*sa*d*da)/den
dp=(d*da-m*s*sa*c*ca)/den
rels=[c*c+s*s-1,d*d+m*s*s-1,ca*ca+sa*sa-1,da*da+m*sa*sa-1]
gens=(c,d,ca,da,s,sa,m)
exact('dn pair-product identity',d*dp-da+m*ca*s*sp,gens,rels)
exact('cn pair-product identity',c*cp-ca+da*s*sp,gens,rels)
exact('bilinear Lorentz pair identity',d*dp-m*c*cp-(da-m*ca)-m*(da-ca)*s*sp,gens,rels)
exact('diagonal Lorentz identity',d*d-m*c*c-(1-m),gens,rels)
exact('contact tangent incidence',da*s*sp+c*cp-ca,gens,rels)
exact('focal normal squared',((1-m)*s*s+c*c)-d*d,gens,rels)
k=S.symbols('k')
exact('ordinary focal-distance product',(1+k*s)*(1-k*s)-(1-k*k*s*s))
a,b,Delta=S.symbols('a b Delta',positive=True)
exact('confocal outer-axis difference', (a*a*da*da-b*b)/ca**2-a*a+b*b,
      (da,ca,b,sa,m,a),[da*da+m*sa*sa-1,ca*ca+sa*sa-1,b*b-a*a*(1-m)])
A,B,D,C,beta,kp,alpha=S.symbols('A B D C beta kp alpha',positive=True)
exact('quarter-shift invariant factor',beta**2*((D/kp)**2-m*(-C/kp)**2)-alpha**2*(D*D-m*C*C),
      (beta,kp,D,C,m,alpha),[beta-alpha*kp])
for N in range(3,32,2):
    for tau in range(1,(N+1)//2):
        if math.gcd(tau,N)==1:
            assert sorted((tau*i)%N for i in range(N))==list(range(N))
    assert all((2*r)%N for r in range(1,N))
checks.append('all odd N <=31 residue permutations and no real sn-zero shifts')
mp.mp.dps=75
maxerr=mp.mpf(0); numeric_cases=0
for N in [3,5,7,9,11]:
 for mm in ['0.09','0.64','0.97']:
  mm=mp.mpf(mm); kk=mp.sqrt(mm);K=mp.ellipk(mm)
  alpha0=mp.mpf(2); beta0=alpha0*mp.sqrt(1-mm); focus=alpha0*kk
  f=lambda name,u:mp.ellipfun(name,u,mm)
  I0=beta0**2*sum(1/f('dn',4*K*i/N) for i in range(N))**2
  nome=mp.exp(-mp.pi*mp.ellipk(1-mm)/K)
  def zeta(u):
   zz=mp.pi*u/(2*K)
   return mp.pi/(2*K)*mp.jtheta(4,zz,nome,1)/mp.jtheta(4,zz,nome)
  for tau in range(1,(N+1)//2):
   if math.gcd(tau,N)>1:continue
   h=2*tau*K/N; aa=alpha0*f('dn',h)/f('cn',h); bb=beta0/f('cn',h)
   assert aa>alpha0 and bb>beta0
   for phase in ['0','0.137','0.729']:
    u=mp.mpf(phase)*K
    verts=[(-aa*f('sn',u+2*i*h),bb*f('cn',u+2*i*h)) for i in range(N)]
    qplus=[];qminus=[]
    for i,P in enumerate(verts):
     Q=verts[(i+1)%N];dx=Q[0]-P[0];dy=Q[1]-P[1];length=mp.hypot(dx,dy)
     cross=lambda x:abs(dx*(0-P[1])-dy*(x-P[0]))/length
     qplus.append(cross(focus));qminus.append(cross(-focus))
     v=u+(2*i+1)*h
     formula=beta0*(1+kk*f('sn',v))/f('dn',v)
     maxerr=max(maxerr,abs(qplus[-1]-formula)/(1+abs(formula)))
     # Reflection, using normalized adjacent chord directions and the ellipse normal.
     Prev=verts[(i-1)%N]
     vin=((P[0]-Prev[0]),(P[1]-Prev[1]));lin=mp.hypot(*vin);vin=[q/lin for q in vin]
     vout=[dx/length,dy/length];normal=[P[0]/aa**2,P[1]/bb**2]
     fac=2*sum(vin[j]*normal[j] for j in (0,1))/sum(q*q for q in normal)
     maxerr=max(maxerr,max(abs(vout[j]-vin[j]+fac*normal[j]) for j in (0,1)))
    I=sum(qplus)*sum(qminus)
    maxerr=max(maxerr,abs(I-I0)/(1+abs(I0)))
    # Independent zeta telescope diagnostics for all nonzero index shifts.
    ts=[u+4*K*i/N for i in range(N)]
    for r in range(1,N):
     ar=4*K*r/N
     corr=sum(f('sn',x)*f('sn',x+ar) for x in ts)
     expect=N*zeta(ar)/(mm*f('sn',ar))
     maxerr=max(maxerr,abs(corr-expect)/(1+abs(expect)))
    numeric_cases+=1
assert maxerr<mp.mpf('1e-60'),maxerr
# A negative parity control: the corresponding four-period expression really varies.
mm=mp.mpf('.64');K=mp.ellipk(mm)
def val(t):
 nd=sum(1/mp.ellipfun('dn',t+K*j,mm) for j in range(4))
 sd=sum(mp.ellipfun('sn',t+K*j,mm)/mp.ellipfun('dn',t+K*j,mm) for j in range(4))
 return nd*nd-mm*sd*sd
variation=abs(val(mp.mpf('.1'))-val(mp.mpf('.3')))
assert variation>mp.mpf('.1')
print(json.dumps({'status':'PASS','exact_checks':len(checks),'exact_check_names':checks,
 'numerical_cases':numeric_cases,'precision_decimal_digits':mp.mp.dps,
 'maximum_relative_or_absolute_diagnostic_error':mp.nstr(maxerr,10),
 'even_four_period_negative_control_variation':mp.nstr(variation,20),
 'versions':{'sympy':S.__version__,'mpmath':mp.__version__},
 'scope':'Exact symbolic checks verify algebra; numerical checks are diagnostic only. All odd N are covered by the written classical-identity proof, not by finite sampling.'},indent=2))
