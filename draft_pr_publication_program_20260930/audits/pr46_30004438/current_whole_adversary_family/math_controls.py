"""Fresh exact independent diagnostics for universal written proofs."""
from pathlib import Path
import json,os,sys
import sympy as s
assert __debug__ and not sys.flags.optimize
F=Path(__file__).absolute().parent;z=s.symbols('z');checks=[]
def ck(n,v):
 if not bool(v):raise AssertionError(n)
 checks.append(n)
def compose(p,q,P,Q,d):
 return s.Poly(sum(p.nth(j)*P.as_expr()**j*Q.as_expr()**(d-j) for j in range(d+1)),z),s.Poly(sum(q.nth(j)*P.as_expr()**j*Q.as_expr()**(d-j) for j in range(d+1)),z)
for d,periods in [(2,4),(3,3),(4,2),(5,1)]:
 p=s.Poly(2*z*s.prod(z-j for j in range(1,d))-sum(s.prod(z-k for k in range(1,d) if k!=j) for j in range(1,d)),z)
 q=s.Poly(s.prod(z-j for j in range(1,d)),z);P,Q=p,q
 ck('seed degree '+str(d),p.degree()==d and q.degree()==d-1 and s.gcd(p,q).degree()==0)
 for n in range(1,periods+1):
  e=d**n;fixed=P-s.Poly(z,z)*Q
  ck('growth degrees '+str((d,n)),P.degree()==e and Q.degree()==e-1)
  ck('growth finite fixed '+str((d,n)),fixed.degree()==e and fixed.count_roots(-s.oo,s.oo)==e)
  ck('growth fixed simple '+str((d,n)),s.gcd(fixed,fixed.diff()).degree()==0)
  ck('growth projective no cancellation '+str((d,n)),s.gcd(P,Q).degree()==0)
  ck('growth infinity multiplier '+str((d,n)),s.limit(Q.as_expr()*z/P.as_expr(),z,s.oo)==s.Rational(1,2**n))
  if n<periods:P,Q=compose(p,q,P,Q,d)
 # Conjugacy moves infinity to finite r and introduces the ambient missing direction.
 r=s.Rational(7,3);inv=1/(r-z)
 conjugated=s.cancel(r-1/(p.as_expr().subs(z,inv)/q.as_expr().subs(z,inv)))
 cp,cq=[s.Poly(v,z) for v in s.fraction(conjugated)]
 ck('conjugacy equal degrees '+str(d),cp.degree()==cq.degree()==d)
 ck('conjugacy finite fixed point '+str(d),s.cancel(conjugated.subs(z,r)-r)==0)
 ck('conjugacy finite attracting multiplier '+str(d),s.simplify(s.diff(conjugated,z).subs(z,r))==s.Rational(1,2))
 ck('conjugacy real poles '+str(d),cq.count_roots(-s.oo,s.oo)==d and s.gcd(cq,cq.diff()).degree()==0)
 ck('conjugacy fixed real '+str(d),(cp-s.Poly(z,z)*cq).count_roots(-s.oo,s.oo)==d+1)
# Exact all full coefficient-chart directions at an equal-degree seed.
p0=s.Poly((z+1)*(z+3),z);q0=s.Poly((z+2)*(z+4),z)
for which,j in [('p',j) for j in range(3)]+[('q',j) for j in range(2)]:
 for sign in [-1,1]:
  perturb=s.Poly(s.Rational(sign,1000)*z**j,z)
  p=p0+perturb if which=='p' else p0;q=q0+perturb if which=='q' else q0
  tag=str((which,j,sign));ck('chart full dimension '+tag,len(p.all_coeffs())+len(q.all_coeffs())-1==5)
  for polynomial,centers in [(p,[-1,-3]),(q,[-2,-4])]:
   for c in centers:ck('strict root interval '+tag+str(c),polynomial.count_roots(c-s.Rational(1,10),c+s.Rational(1,10))==1)
  ck('positive coefficient '+tag,all(x>0 for x in p.all_coeffs()+q.all_coeffs()))
  P,Q=p,q
  for n in [1,2]:
   fixed=P-s.Poly(z,z)*Q;e=2**n
   ck('chart iterate no common factor '+tag+str(n),s.gcd(P,Q).degree()==0)
   ck('chart iterate all real poles '+tag+str(n),Q.degree()==e and Q.count_roots(-s.oo,0)==e and s.gcd(Q,Q.diff()).degree()==0)
   ck('chart iterate all real fixed '+tag+str(n),fixed.degree()==e+1 and fixed.count_roots(-s.oo,s.oo)==e+1)
   ck('chart iterate positive coefficients '+tag+str(n),all(x>0 for x in P.all_coeffs()+Q.all_coeffs()))
   if n==1:P,Q=compose(p,q,P,Q,2)
x,y,b,c,a=s.symbols('x y b c a',real=True)
ck('uniform imaginary part identity',s.simplify(s.im(a*(x+s.I*y)-c/(x+s.I*y-b))-y*(a+c/((x-b)**2+y**2)))==0)
C=(z*z-1)/(2*z)
ck('realfiber insufficient positive fixed',s.cancel(C.subs(z,s.I)-s.I)==0)
ck('realfiber insufficient negative fixed',s.cancel(C.subs(z,-s.I)+s.I)==0)
ck('swapping halfplane nonreal twocycle',s.cancel((-C).subs(z,s.I)+s.I)==0 and s.cancel((-C).subs(z,-s.I)-s.I)==0)
neutral=z-1/z
ck('neutral boundary nonreal nearby fixed',s.cancel(((1-s.Rational(1,100))*z-1/z).subs(z,10*s.I)-10*s.I)==0)
out={'schema':'pr46-whole-independent-mathematical-controls/v1','actual_pid':os.getpid(),'sympy_version':s.__version__,'passed':len(checks),'failed':0,'checks':checks,'universal_scope_supplied_by_written_proof':True,'future_acceptance_approved':False}
(F/'MATH_CONTROLS_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['schema','actual_pid','sympy_version','passed','failed','universal_scope_supplied_by_written_proof']},indent=2))
