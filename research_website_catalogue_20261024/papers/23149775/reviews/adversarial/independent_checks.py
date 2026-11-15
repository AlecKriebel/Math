"""Adversarial exact geometry and finite NONINTERVAL stress evidence.
Only writes its JSON output to stdout. No archived module is imported.
"""
import json,math
import sympy as s
import mpmath as m
checks=0; maxerr=m.mpf(0);m.mp.dps=110
def need(v,label):
 global checks
 if not v:raise ValueError(label)
 checks+=1
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def area(P):return sum(det(P[j],P[(j+1)%len(P)]) for j in range(len(P)))/2
def line(p,q):
 d=sub(q,p);n=(-d[1],d[0]);return n,dot(n,p)
def project(F,n,h):
 z=(h-dot(n,F))/dot(n,n);return (F[0]+z*n[0],F[1]+z*n[1])
def exact0(x,label):need(s.simplify(x)==0,label)
def near(x,y,label,tol='1e-75'):
 global maxerr
 e=abs(x-y)/(1+abs(x)+abs(y));maxerr=max(maxerr,e);need(e<m.mpf(tol),label)

# Euclidean supporting-line computation; no elliptic parametrization used.
r=s.sqrt(21); f=s.sqrt(5);P=[(r,s.Integer(0)),(-3*r/5,s.Rational(16,5)),(-3*r/5,-s.Rational(16,5))]
T=[((x/21,y/16),s.Integer(1)) for x,y in P];L=[line(P[j],P[(j+1)%3]) for j in range(3)]
exact=[]
for sigma in [1,-1]:
 F=(sigma*f,s.Integer(0));Q=[project(F,n,h) for n,h in L];U=[project(F,n,h) for n,h in T];A=s.simplify(area(Q));B=s.simplify(area(U))
 exact0(A-s.Rational(84,625)*(7*r+sigma*f),'exact A');exact0(B-s.Rational(7,10)*(7*r+sigma*f),'exact B');exact0(B-s.Rational(125,24)*A,'exact multiplier');need(A>0 and B>0,'triangle signed positivity')
 exact0(area(list(reversed(Q)))+A,'reversed pedal');exact0(area(Q*3)-3*A,'repeated pedal');exact.append({'focus':sigma,'A':str(A),'B':str(B)})
ratio=s.simplify(s.sympify(exact[0]['A'])/s.sympify(exact[1]['A']));need(ratio>1,'phase nonconstancy negative control');need(1/ratio<1,'inverted reciprocal')

families=[(3,1),(4,1),(5,2),(7,3),(12,5),(17,8),(31,15)]
records=[];geometry_max=m.mpf(0)
for kval in ['0.000001','0.6','0.9999']:
 k=m.mpf(kval);kp=m.sqrt(1-k*k);K=m.ellipk(k*k)
 sn=lambda z:m.ellipfun('sn',z,k*k);cn=lambda z:m.ellipfun('cn',z,k*k);dn=lambda z:m.ellipfun('dn',z,k*k)
 for N,tau in families:
  need(math.gcd(N,tau)==1 and 0<2*tau<N,'admitted primitive family');v=2*K*tau/N;delta=2*v;a=dn(v)/cn(v);b=kp/cn(v);multipliers=[];minarea=m.inf;minincident=m.inf
  for phase in ['0.137','0.711','1.819']:
   w=m.mpf(phase)*K;V=[(-a*sn(w+j*delta),b*cn(w+j*delta)) for j in range(N)];sides=[line(V[j],V[(j+1)%N]) for j in range(N)];tangents=[((x/a**2,y/b**2),m.mpf(1)) for x,y in V]
   for j,(n,h) in enumerate(sides):
    near(n[0]**2+kp**2*n[1]**2,h*h,'caustic tangency')
    contact=(n[0]/h,kp**2*n[1]/h);d=sub(V[(j+1)%N],V[j]);t=dot(sub(contact,V[j]),d)/dot(d,d);need(0<t<1,'actual contact on segment')
    incoming=sub(V[j],V[(j-1)%N]);outgoing=d;incoming=tuple(x/m.sqrt(dot(incoming,incoming)) for x in incoming);outgoing=tuple(x/m.sqrt(dot(outgoing,outgoing)) for x in outgoing);normal=tangents[j][0]
    for z in [0,1]:near(outgoing[z],incoming[z]-2*dot(incoming,normal)*normal[z]/dot(normal,normal),'actual reflection')
   for sigma in [1,-1]:
    F=(sigma*k,m.mpf(0));Q=[project(F,n,h) for n,h in sides];U=[project(F,n,h) for n,h in tangents];A=area(Q);B=area(U);need(A>0 and B>0,'stress positive area');minarea=min(minarea,A,B)
    for X,n,h in [(Q[j],*sides[j]) for j in range(N)]+[(U[j],*tangents[j]) for j in range(N)]:near(dot(n,X),h,'projection incidence')
    for X in [Q,U]:
     relative=[sub(x,F) for x in X]
     for j in range(N):need(det(relative[j],relative[(j+1)%N])>0,'positive individual focus-relative determinant')
     near(area(list(reversed(X))),-area(X),'stress reversal');near(area(X*2),2*area(X),'stress repetition')
    multipliers.append(B/A)
   if N%2==0:
    Ap=area([project((k,m.mpf(0)),n,h) for n,h in sides]);Am=area([project((-k,m.mpf(0)),n,h) for n,h in sides]);near(Ap,Am,'primitive even focus symmetry')
  for C in multipliers[1:]:near(C,multipliers[0],'both foci and phase independent multiplier')
  records.append({'k':kval,'N':N,'tau':tau,'phases':3,'both_foci':True,'C0':m.nstr(multipliers[0],35),'minimum_signed_area':m.nstr(minarea,10)})

# Complex objects tested at a different phase and with both imaginary sheets.
complex_records=[];negative_controls=[];k=m.mpf('.6');kp=m.sqrt(1-k*k);K=m.ellipk(k*k);Kp=m.ellipk(1-k*k)
sn=lambda z:m.ellipfun('sn',z,k*k);cn=lambda z:m.ellipfun('cn',z,k*k);dn=lambda z:m.ellipfun('dn',z,k*k)
for N,tau in [(3,1),(5,2),(8,3),(11,5)]:
 v=2*K*tau/N;delta=2*v;a=dn(v)/cn(v);b=kp/cn(v);q=lambda z:((k-sn(z))/(1-k*sn(z)),kp*cn(z)/(1-k*sn(z)));Q=lambda z:(a*(k-a*sn(z))/(a-k*sn(z)),a*b*cn(z)/(a-k*sn(z)))
 def trace(w,shift=True):return area([q(w+(v if shift else 0)+j*delta) for j in range(N)]),area([Q(w+j*delta) for j in range(N)])
 A,B=trace(K*m.mpf('.137'));C=B/A;z=K*m.mpf('.173')+1j*Kp*m.mpf('.237');Az,Bz=trace(z);At,Bt=trace(z+2j*Kp);Ap,Bp=trace(z+4*K/N)
 near(At,-Az,'anti A');near(Bt,-Bz,'anti B');near(Ap,Az,'reduced real period A');near(Bp,Bz,'reduced real period B');near(Bz,C*Az,'arbitrary complex proportionality')
 r=K+1j*Kp;e=m.mpf('1e-16');x=q(r+e)
 for j,target in enumerate([2/k,2j/k]):near(e*e*x[j],target,'original double germ','1e-27')
 R=(a/(k*sn(v)),1j*a/(k*sn(v)))
 for sign in [-1,1]:
  value=Q(r+sign*v+e)
  for j in [0,1]:near(e*value[j],sign*R[j],'outer signed residue','1e-12')
 for sheet in [1,3]:
  pole=K-v+sheet*1j*Kp;A1,B1=trace(pole+e);A2,B2=trace(pole+2*e);need(abs(e*A1)>m.mpf('1e-12'),'genuine nonzero original residue');need(abs(e*B1)>m.mpf('1e-12'),'genuine nonzero outer residue');near(e*A1,2*e*A2,'simple area pole A','1e-11');near(e*B1,2*e*B2,'simple area pole B','1e-11');near(B1,C*A1,'pole proportionality','1e-65')
 complex_records.append({'N':N,'tau':tau,'both_pole_sheets':True,'epsilon':'1e-16'})
 if (N,tau)==(3,1):
  wrong1=trace(K*m.mpf('.137'),False);wrong2=trace(K*m.mpf('.711'),False);need(abs(wrong1[1]/wrong1[0]-wrong2[1]/wrong2[0])>m.mpf('1e-6'),'wrong midpoint must fail');negative_controls.append('Omitting chord midpoint shift changes multiplier across phases')
negative_controls.append('Phase-constant focal-ratio extension rejected by exact reciprocal triangle')
need(math.gcd(6,2)!=1,'nonprimitive incidence control');negative_controls.append('N6/tau2 is a repetition, not a primitive six-orbit')

for N,tau in [(3,1),(5,2),(8,3),(17,8)]:
 v=m.pi*tau/N;a=1/m.cos(v);delta=2*v;q=[(-m.sin(j*delta),m.cos(j*delta)) for j in range(N)];Q=[(a*x,a*y) for x,y in q];need(area(q)>0,'circle star positivity');near(area(Q)/area(q),1/m.cos(v)**2,'circle multiplier')
print(json.dumps({'status':'PASS','exact_assertions_and_finite_diagnostic_predicates':checks,'precision_decimal_digits':m.mp.dps,'real_families':len(records),'real_phase_geometries':3*len(records),'focal_pairs':6*len(records),'stress_records':records,'complex_families':complex_records,'negative_controls':negative_controls,'maximum_normalized_diagnostic_error_over_mixed_tolerances':m.nstr(maxerr,14),'exact_triangle':exact,'focal_ratio':str(ratio),'evidence_limit':'Finite high-precision NONINTERVAL diagnostics are not universal proofs or interval-certified bounds. Exact triangle identities and analytic derivation are separate.'},indent=2))
