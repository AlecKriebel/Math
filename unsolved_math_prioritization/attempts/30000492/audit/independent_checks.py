#!/usr/bin/env python3
"""Independent audit checks; does not import or execute author code.
Full iterate factorization deliberately avoids stable-branch pruning.
Requires SymPy; exact finite evidence, not a limiting-settledness proof.
"""
import argparse,hashlib,itertools,json,pathlib,sys,warnings
from fractions import Fraction
import sympy as sp
from sympy.utilities.exceptions import SymPyDeprecationWarning
warnings.simplefilter('ignore',SymPyDeprecationWarning)
x=sp.Symbol('x')
def val(P,t,p):return int(P.eval(t))%p
def full_profile(p,coeff,N):
 f=sp.Poly(sum(c*x**i for i,c in enumerate(coeff)),x,modulus=p)
 gamma=(-coeff[1]*pow(2,-1,p))%p
 orbit=[]; b=val(f,gamma,p)
 while b not in orbit:orbit.append(b);b=val(f,b,p)
 P=sp.Poly(x,x,modulus=p);rows=[]
 for n in range(1,N+1):
  # Forward recurrence f(P) differs from the author's per-factor h(f).
  P=(P*P+coeff[1]*P+coeff[0]).set_modulus(p)
  content,fac=P.factor_list(); assert content==1
  product=sp.Poly(1,x,modulus=p);stable_degree=0
  for h,e in fac:
   assert e==1 and h.is_irreducible
   product*=h
   if all(pow(val(h,b,p),(p-1)//2,p)==p-1 for b in orbit):stable_degree+=h.degree()
  assert product==P
  rows.append({'n':n,'full_degree':P.degree(),'factor_count':len(fac),'stable_mass':str(Fraction(stable_degree,2**n))})
 return {'p':p,'coefficients_ascending':coeff,'postcritical_orbit':orbit,'rows':rows}
def valuation(n):
 r=0
 while not n%2:r+=1;n//=2
 return r
def order_checks():
 count=0;qs=[]
 for p in list(sp.primerange(3,101)):
  for k in range(1,5):
   q=int(p)**k
   if q>10000:continue
   qs.append(q)
   s=valuation(q-1);r=valuation(q+1)
   for e in sp.divisors(q-1):
    e=int(e)
    if valuation(e)!=s:continue
    for n in range(1,17):
     M=2**n*e
     assert M//sp.gcd(M,2**n)==e
     d=int(sp.n_order(q,M))
     predicted=2**n if q%4==1 else 2**max(1,n-r+1)
     assert d==predicted,(q,e,n,d,predicted)
     if q%4==3:
      dn=int(sp.n_order(q,2*M))
      assert (dn==2*d)==(n>=r)
     count+=1
 return {'prime_powers':qs,'q_count':len(qs),'root_order_cases':count,'n_range':[1,16]}
def char2_checks():
 counts={};total=0
 f=sp.Poly(x*x+x+1,x,modulus=2)
 for d in [2,4,6,8]:
  counts[str(d)]=0
  for bits in itertools.product(range(2),repeat=d):
   h=sp.Poly(x**d+sum(c*x**i for i,c in enumerate(bits)),x,modulus=2)
   if not h.is_irreducible:continue
   counts[str(d)]+=1;total+=1
   first=h.compose(f)
   assert first.nth(2*d-1)==0
   if first.is_irreducible:assert not first.compose(f).is_irreducible
 return {'all_monic_irreducibles_by_even_degree':counts,'total':total,'first_or_second_composition_reducible':True}
def witness():
 p=7;f=sp.Poly(x*x+1,x,modulus=p);g=sp.Poly(x*x+4*x+5,x,modulus=p)
 I=sp.Poly(x,x,modulus=p)
 for _ in range(4):I=I*I+1
 assert I.rem(g).is_zero
 P=g;rows=[]
 for k in range(4):
  _,fac=P.factor_list();out=[]
  for h,e in fac:
   assert e==1 and h.is_irreducible
   out.append({'coefficients_ascending':[int(c)%p for c in reversed(h.all_coeffs())], 'type':''.join('s' if pow(val(h,b,p),3,p)==1 else 'n' for b in [1,2,5])})
  rows.append(sorted(out,key=lambda z:z['coefficients_ascending']))
  P=P.compose(f)
 assert [len(r) for r in rows]==[1,1,1,2]
 assert [rows[j][0]['type'] for j in range(3)]==['nns','nss','sss']
 assert all(z['type']=='nnn' for z in rows[3])
 old=[t for t in map(''.join,itertools.product('ns',repeat=3)) if t[1]==t[2]]
 excluded=[t for t in old if t[0]!=t[1]]
 assert old==['nnn','nss','snn','sss'] and excluded==['nss','snn']
 return {'levels':rows,'old_support':old,'history_forbidden':excluded}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--author-results');args=ap.parse_args()
 out={'python':sys.version.split()[0],'sympy':sp.__version__,'profiles':[full_profile(p,c,n) for p,c,n in [(7,[1,0,1],9),(5,[2,0,1],8),(3,[2,2,1],8),(11,[1,0,1],7),(13,[5,0,1],7)]],'orders':order_checks(),'characteristic_two':char2_checks(),'witness':witness()}
 if args.author_results:
  source=pathlib.Path(args.author_results).read_bytes();author=json.loads(source)
  for got,expected in zip(out['profiles'],author['odd_profiles']):
   assert [r['stable_mass'] for r in got['rows']]==[r['stable_mass'] for r in expected['rows']]
  out['author_results_sha256']=hashlib.sha256(source).hexdigest();out['all_author_mass_rows_match']=True
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
