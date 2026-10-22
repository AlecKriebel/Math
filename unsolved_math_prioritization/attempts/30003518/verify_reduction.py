#!/usr/bin/env python3
from pathlib import Path
import sympy as s,json
from collections import Counter
C=Counter()
def ck(cat,test):
 assert test,cat
 C[cat]+=1
e=s.symbols('e',positive=True)
for N in range(1,9):
 d=[s.Rational(i+2,i+1) for i in range(N+1)]
 a=[s.Rational(i+3,i+2) for i in range(N)]
 q=[s.Rational(i+4,i+3) for i in range(N)]
 Q=s.prod(d[j]+q[j]*e for j in range(1,N))
 p=[s.Integer(1)]
 for i in range(1,N):p.append(s.cancel(q[i-1]*e*p[-1]/(d[i]+q[i]*e)))
 p.append(s.cancel(q[N-1]*e*p[-1]/d[N]))
 g=s.cancel(Q*sum(a[i]*p[i] for i in range(N)))
 h=s.cancel(Q*sum(p)+e*g)
 ck('polynomial_g_degree',s.Poly(g,e).degree()<=N-1)
 ck('polynomial_h_degree',s.Poly(h,e).degree()==N)
 for i in range(N+1):ck('nonnegative_polynomial_coefficients',all(z>=0 for z in s.Poly(s.cancel(Q*p[i]),e).all_coeffs()))
 # Reconstruction at arbitrary rational enzyme, with positive prescribed free pools.
 ee=s.Rational(2,3);Et=s.Rational(5,2)
 G=sum(a[i]*p[i] for i in range(N));cc0=s.cancel((Et-e)/(e*G))
 cs=[s.cancel(cc0*p[i]) for i in range(N+1)];bs=[s.cancel(a[i]*e*cs[i]) for i in range(N)]
 ck('enzyme_conservation_identity',s.cancel(e+sum(bs)-Et)==0)
 for i in range(1,N):ck('interior_balance_identity',s.cancel(q[i-1]*e*cs[i-1]-(d[i]+q[i]*e)*cs[i])==0)
 ck('terminal_balance_identity',s.cancel(q[-1]*e*cs[-2]-d[-1]*cs[-1])==0)
 ck('source_equals_dissociation_identity',s.cancel((d[0]+q[0]*e)*cs[0]-sum(d[i]*cs[i] for i in range(N+1)))==0)
 for v in cs+bs:ck('positive_species_controls',v.subs(e,ee)>0)
# Exact nonphysical positive-root control: all original rates/totals equal1, N=1.
z=s.symbols('z');P=4*z**4+5*z**3-6*z**2-6*z+4
ck('two_positive_raw_roots',s.Poly(P,z).count_roots(0,s.oo)==2)
ck('first_root_isolated',s.Poly(P,z).count_roots(s.Rational(56,100),s.Rational(57,100))==1)
ck('second_root_isolated',s.Poly(P,z).count_roots(s.Rational(89,100),s.Rational(90,100))==1)
W=lambda x:2*(1-x*x)/x
ck('first_root_nonphysical',W(s.Rational(57,100))>1)
ck('second_root_physical',W(s.Rational(89,100))<1 and W(s.Rational(90,100))>0)
out={'status':'PASS_EXACT','assertions':sum(C.values()),'categories':dict(C),'scope':'Supporting controls for all-N Lck scalar reconstruction; raw polynomial roots require physical filtering'}
Path(__file__).with_name('reduction_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
