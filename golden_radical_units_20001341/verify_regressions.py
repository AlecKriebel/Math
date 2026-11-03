"""Finite exact regressions and deliberately false mathematical mutations, not a proof."""
import argparse,json,math
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--mutation',default='none',choices=['none','prime_obstruction','fourth_obstruction','inverse','degree_drop','mahler','relative_log','relative_height']);args=p.parse_args()
x=s.symbols('x'); checks=[]
def check(name,condition):
 if not bool(condition):raise RuntimeError('mathematical regression failed: '+name)
 checks.append(name)
# Actual factorization witnesses show why both binomial hypotheses are needed.
check('prime_power_counterexample',s.expand((x-2)*(x+2)-(x*x-4))==0)
prime_claim=s.Poly(x*x-4,x).is_irreducible
check('prime_obstruction_required',prime_claim if args.mutation=='prime_obstruction' else not prime_claim)
fourth_claim=s.Poly(x**4+4,x).is_irreducible
check('exceptional_factorization',s.expand((x*x-2*x+2)*(x*x+2*x+2)-(x**4+4))==0)
check('fourth_obstruction_required',fourth_claim if args.mutation=='fourth_obstruction' else not fourth_claim)
phi=(1+s.sqrt(5))/2
for n in [1,2,3,4,6]:
 check('golden_irreducible_'+str(n),s.Poly(x**n-phi,x,extension=s.sqrt(5)).is_irreducible)
for n in [1,2,3,4,6,12,156]:
 f=s.Poly(x**(2*n)-x**n-1,x)
 inv=x**(2*n-1)+x**(n-1) if args.mutation=='inverse' else x**(2*n-1)-x**(n-1)
 check('inverse_'+str(n),s.rem(x*inv-1,f.as_expr(),x)==0)
# Degree drop is checked from an independently calculated minimal polynomial.
for n,k in [(2,2),(3,3),(4,2),(6,3),(6,6)]:
 beta=phi**s.Rational(k,n);degree=s.degree(s.minpoly(beta,x),x)
 expected=2*n if args.mutation=='degree_drop' else 2*n//math.gcd(n,k)
 check('degree_'+str((n,k)),degree==expected)
 # Height k*a/(2n), so intrinsic log M/a = degree*k/(2n).
 actual=s.Rational(degree*k,2*n)
 expected=k if args.mutation=='mahler' else s.Rational(k,math.gcd(n,k))
 check('mahler_'+str((n,k)),actual==expected)
# Logs here are normalized by a>0. Arbitrary rational block coordinates
# exercise the exact Cauchy/positive-part inequalities, including equality.
for plus in [[s.Rational(1,3)]*3,[s.Rational(2),s.Rational(-1),s.Rational(0)]]:
 minus=[-z for z in plus];n=len(plus);r=sum(plus)
 actual=sum(z*z for z in plus+minus)
 lower=(4 if args.mutation=='relative_log' else 2)*r*r/n
 check('relative_log_'+str(len(checks)),actual>=lower)
 height=sum(max(z,0) for z in plus+minus)/(2*n)
 lower=abs(r)/(n if args.mutation=='relative_height' else 2*n)
 check('relative_height_'+str(len(checks)),height>=lower)
print(json.dumps({'status':'PASS','mutation':args.mutation,'checks':checks,'scope':'Finite regressions; all-n proofs and unresolved kernel scope remain in RESEARCH.md.'},indent=2))
