#!/usr/bin/env python3
"""Independent diagnostic controls for Stachel's k117 theorem application.
Exact rational N=4 checks plus high-precision geometric star-family controls.
Finite tests are not the proof; the cited theorem is the mathematical input.
"""
import json,math
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
mp.mp.dps=65
count_exact=0;count_numerical=0;max_residual=mp.mpf('0');examples=[]
def exact(c):
 global count_exact
 assert c;count_exact+=1

def near(actual,expected):
 global count_numerical,max_residual
 residual=abs(actual-expected)/max(mp.mpf(1),abs(expected));max_residual=max(max_residual,residual)
 assert residual<mp.mpf('1e-52'),(actual,expected,residual)
 count_numerical+=1

# Orthogonal four-orbit examples; exact lengths verified from squared norms.
for a,b,s in [(4,3,5),(12,5,13),(15,8,17),(20,21,29)]:
 a,b,s=map(F,(a,b,s));a,b=max(a,b),min(a,b);lam=a*a*b*b/(s*s)
 pp=[(a,F(0)),(F(0),b),(-a,F(0)),(F(0),-b)]
 qq=[(a**3/s**2,b**3/s**2),(-a**3/s**2,b**3/s**2),(-a**3/s**2,-b**3/s**2),(a**3/s**2,-b**3/s**2)]
 ls=[b*b/s,a*a/s,b*b/s,a*a/s];rs=[a*a/s,b*b/s,a*a/s,b*b/s]
 for i in range(4):
  exact(sum((pp[i][j]-qq[i][j])**2 for j in range(2))==ls[i]**2)
  exact(sum((pp[(i+1)%4][j]-qq[i][j])**2 for j in range(2))==rs[i]**2)
 exact(math.prod(ls)==math.prod(rs)==lam**2)

# Direct Euclidean distances in parametrized genuine Poncelet families.
# mp.ellipfun takes parameter m^2, whereas Stachel's m is the modulus.
for modulus in [mp.mpf(1)/3,mp.mpf(3)/5,mp.mpf(4)/5]:
 m2=modulus**2;ac=mp.mpf(1);bc=mp.sqrt(1-m2);K=mp.ellipk(m2)
 sn=lambda u:mp.ellipfun('sn',u,m2);cn=lambda u:mp.ellipfun('cn',u,m2);dn=lambda u:mp.ellipfun('dn',u,m2)
 for n in range(4,19,2):
  for tau in range(1,n//2):
   if math.gcd(n,tau)!=1:continue
   shift=2*tau*K/n;ae=dn(shift)/cn(shift);be=bc/cn(shift);lam=ae**2-ac**2
   near(lam,be**2-bc**2)
   phase_values=[]
   for phase in [mp.mpf('0.071'),mp.mpf('0.283'),mp.mpf('0.697')]:
    u0=4*K*phase
    p=[(-ae*sn(u0+2*i*shift),be*cn(u0+2*i*shift)) for i in range(n)]
    q=[(-ac*sn(u0+(2*i+1)*shift),bc*cn(u0+(2*i+1)*shift)) for i in range(n)]
    ls=[];rs=[]
    for i in range(n):
     v=p[i];w=p[(i+1)%n];z=q[i];edge=(w[0]-v[0],w[1]-v[1])
     near(v[0]**2/ae**2+v[1]**2/be**2,1)
     near(z[0]**2/ac**2+z[1]**2/bc**2,1)
     near(edge[0]*(z[0]-v[0])+edge[1]*(z[1]-v[1]),mp.sqrt(edge[0]**2+edge[1]**2)*mp.sqrt((z[0]-v[0])**2+(z[1]-v[1])**2))
     near(edge[0]*z[0]/ac**2+edge[1]*z[1]/bc**2,0)
     ls.append(mp.sqrt(sum((z[j]-v[j])**2 for j in range(2))))
     rs.append(mp.sqrt(sum((w[j]-z[j])**2 for j in range(2))))
    near(mp.fprod(ls),lam**(n//2));near(mp.fprod(rs),lam**(n//2))
    near(mp.fprod(rs[-1:]+rs[:-1]),mp.fprod(rs))
    if n%4==0:near(mp.fprod(ls[:n//2]),lam**(n//4))
    phase_values.append(mp.nstr(mp.fprod(ls),12))
   examples.append({'N':n,'turning_number':tau,'modulus':mp.nstr(modulus,12),'phase_products':phase_values})

# Negative control: even traversal length with odd primitive period is excluded.
m2=mp.mpf('0.36');K=mp.ellipk(m2);n=6;tau=2;shift=2*tau*K/n
sn=lambda u:mp.ellipfun('sn',u,m2);cn=lambda u:mp.ellipfun('cn',u,m2);dn=lambda u:mp.ellipfun('dn',u,m2)
ae=dn(shift)/cn(shift);be=mp.sqrt(1-m2)/cn(shift);lam=ae**2-1;u0=mp.mpf('0.137')
p=[(-ae*sn(u0+2*i*shift),be*cn(u0+2*i*shift)) for i in range(n)]
q=[(-sn(u0+(2*i+1)*shift),mp.sqrt(1-m2)*cn(u0+(2*i+1)*shift)) for i in range(n)]
prod=mp.fprod(mp.sqrt(sum((p[i][j]-q[i][j])**2 for j in range(2))) for i in range(n))
relative=abs(prod/lam**3-1);assert relative>mp.mpf('1e-6')
receipt={'status':'PASS','exact_assertions':count_exact,'high_precision_assertions':count_numerical,'max_normalized_residual':mp.nstr(max_residual,10),'genuine_primitive_families':len(examples),'three_phases_per_family':True,'star_families':sum(x['turning_number']>1 for x in examples),'repeated_odd_negative_control_relative_mismatch':mp.nstr(relative,15),'examples':examples,'scope':'Independent diagnostic controls; not a proof or implemented universal decision test.'}
print(json.dumps({k:v for k,v in receipt.items() if k!='examples'},indent=2));Path(__file__).with_name('independent_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
