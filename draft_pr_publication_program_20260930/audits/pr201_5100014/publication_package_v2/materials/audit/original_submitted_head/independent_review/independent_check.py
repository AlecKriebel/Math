"""Independent finite controls for the k303,a proof.
Exact symbolic identities/dihedral incidence, then separate numerical diagnostics.
"""
from collections import Counter
from math import gcd
from pathlib import Path
import sympy as s,json
C=Counter();D=Counter()
def ck(g,b):
 assert b,g
 C[g]+=1
A,B,L=s.symbols('A B L',positive=True);c=A-B;al=A-L;be=B-L
xx=A*A/c;yy=-B*B/c
ck('isotropic_contact_on_E',s.cancel(xx/A+yy/B-1)==0)
ck('isotropic_normal',s.cancel(xx/A**2+yy/B**2)==0)
ck('common_tangent_dual',s.cancel(al*xx/A**2+be*yy/B**2-1)==0)
ck('unramified_finite_pedal_pole',s.cancel(xx/al+yy/be-1+L*L/(al*be))==0)
ck('transversality_determinant',s.cancel(1/(A*be)-1/(B*al)-L*(A-B)/(A*B*al*be))==0)
ck('infinite_tangent_not_C_tangent',s.cancel(al/A-be/B-L*(1/B-1/A))==0)
# First-order pedal pole residues are collinear, independently of arbitrary M.
u,v,r0,r1,b0,b1,d0,d1,z=s.symbols('u v r0 r1 b0 b1 d0 d1 z')
Q0=s.Matrix([r0*u/z+b0,r0*v/z+b1]);Q1=s.Matrix([r1*u/z+d0,r1*v/z+d1])
ck('double_pedal_pole_cancels',s.expand(s.det(s.Matrix.hstack(Q0,Q1))).coeff(z,-2)==0)
# On each orbit through sigma-fixed z, model T by +1, sigma by negation,
# tau by 1-j and central inversion by +m. Test all exact congruences.
for N in range(6,1003,4):
 m=N//2
 kvals=[j for j in range(N) if (2*j-(1-m))%N==0]
 ck('odd_m_infinity_congruence',len(kvals)==2)
 for j in kvals:ck('tau_equals_central_at_infinity',(1-j)%N==(m+j)%N)
 fixed={j for j in range(N) if j==(-j)%N};ck('only_two_sigma_fixed',fixed=={0,m})
 feet=fixed|{(j+1)%N for j in fixed};ck('all_four_singular_feet',feet=={0,1,m,m+1})
 adjacent={(j,(j+1)%N) for j in feet if (j+1)%N in feet}
 ck('only_two_adjacent_singular_pairs',adjacent=={(0,1),(m,m+1)})
for N in range(4,1001,4):
 m=N//2;ck('excluded_parity_congruence_unsolvable',all((2*j-(1-m))%N for j in range(N)))
# Independent actual orbits using the canonical parametrization. Numerical only.
import mpmath as mp
mp.mp.dps=80;maxerr=mp.mpf(0)
def close(g,x,y):
 global maxerr
 e=abs(x-y)/max(1,abs(x),abs(y));maxerr=max(maxerr,e)
 assert e<mp.mpf('1e-60'),(g,e)
 D[g]+=1
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(p):return sum(det(p[j],p[(j+1)%len(p)]) for j in range(len(p)))/2
for k in [mp.mpf('.27'),mp.mpf('.67'),mp.mpf('.91')]:
 par=k*k;K=mp.ellipk(par);kp=mp.sqrt(1-par)
 sn=lambda u:mp.ellipfun('sn',u,par)
 cn=lambda u:mp.ellipfun('cn',u,par)
 dn=lambda u:mp.ellipfun('dn',u,par)
 for N in [6,10,14,18,22]:
  for tau in range(1,N//2):
   if gcd(N,tau)!=1:continue
   v=2*K*tau/N;delta=2*v;a=dn(v)/cn(v);b=kp/cn(v)
   for M in [(mp.mpf(0),mp.mpf(0)),(mp.mpf(1),mp.mpf(2)),(mp.mpf(-2),mp.mpf('.4'))]:
    ref=None;ratio=None
    for phase in [mp.mpf('.039'),mp.mpf('.372'),mp.mpf('.881')]:
     u=phase*K;P=[(-a*sn(u+j*delta),b*cn(u+j*delta)) for j in range(N)]
     O=[];Q=[]
     for j,p in enumerate(P):
      r=P[(j+1)%N];dd=det(p,r);O.append((a*a*(r[1]-p[1])/dd,b*b*(p[0]-r[0])/dd))
      normal=(p[0]/(a*a),p[1]/(b*b));sq=normal[0]**2+normal[1]**2
      f=(1-normal[0]*M[0]-normal[1]*M[1])/sq
      Q.append((M[0]+f*normal[0],M[1]+f*normal[1]))
     ap=area(P);ao=area(O);aq=area(Q)
     if ref is None:ref=ao*aq;ratio=aq/ap
     close('full_outer_pedal_product',ao*aq,ref)
     close('pedal_original_area_ratio',aq/ap,ratio)
     close('orientation_reversal_A',area(list(reversed(P))),-ap)
     close('orientation_reversal_pedal',area(list(reversed(Q))),-aq)
     for j,p in enumerate(P):
      # Outer side is the tangent at p: endpoints O_(j-1),O_j.
      for r in [O[j-1],O[j]]:close('outer_side_tangent_identity',p[0]*r[0]/(a*a)+p[1]*r[1]/(b*b),1)
      close('foot_on_actual_outer_side',p[0]*Q[j][0]/(a*a)+p[1]*Q[j][1]/(b*b),1)
      r=O[j];ss=O[j-1];close('foot_perpendicular_to_outer_side',(Q[j][0]-M[0])*(r[0]-ss[0])+(Q[j][1]-M[1])*(r[1]-ss[1]),0)
root=Path(__file__).resolve().parent
r={'verdict':'PASS','exact_assertions':sum(C.values()),'exact_groups':dict(C),'numerical_diagnostics':sum(D.values()),'numerical_groups':dict(D),'digits':80,'maximum_scaled_error':mp.nstr(maxerr,12),'limits':'Finite controls do not prove flag-curve geometry or all-N result; see independent written audit.'};(root/'independent_receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
