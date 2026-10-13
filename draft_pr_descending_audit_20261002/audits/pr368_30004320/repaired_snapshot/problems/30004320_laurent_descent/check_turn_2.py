#!/usr/bin/env python3
"""Exact controls for the smooth wound torsor and its convergent lift."""
import json,itertools
import sympy as s
checks=0

def ck(t):
 global checks
 assert t
 checks+=1
x,y,a,b,d,t,v,z=s.symbols('x y a b d t v z')
primes=(2,3,5,7,11)
for p in primes:
 def mod(f):return s.Poly(s.expand(f),x,y,a,b,d,t,v,z,modulus=p).as_expr()
 F=y**p-a*x**p-x
 ck(mod(s.diff(F,x)+1)==0)
 # Coordinate inverse after adjoining d^p=a, for every torsor level b.
 xx=z**p-b;yy=z+d*xx
 expr=s.Poly(mod(F.subs({x:xx,y:yy,a:d**p})-b),z,d,b,modulus=p)
 ck(expr.is_zero)
 # The uncorrected lift has exactly error c=(-b)^p*t*v.
 expr=mod(F.subs({x:-b,y:-b*v})-b)
 expr=s.rem(s.Poly(expr,v,x,y,a,b,d,t,z,modulus=p),s.Poly(v**p-t*v-a,v,x,y,a,b,d,t,z,modulus=p)).as_expr()
 ck(mod(expr-(-b)**p*t*v)==0)
 # Sparse polynomial delta in a,c; Frobenius powers are exact in F_p.
 # Each truncation delta_N+a delta_N^p-c has just the next high-order term.
 for N in range(8):
  terms={((p**j-1)//(p-1),p**j):(-1)**((p**j-1)//(p-1))%p for j in range(N+1)}
  out=dict(terms)
  for (ea,ec),coef in terms.items():
   key=(1+p*ea,p*ec);out[key]=(out.get(key,0)+coef)%p
  out[(0,1)]=(out.get((0,1),0)-1)%p
  out={k:c for k,c in out.items() if c}
  en=(p**N-1)//(p-1)
  ck(out=={(1+p*en,p**(N+1)):(-1)**en%p})
  ck(p**(N+1)>p**N)
 # Finite valuation controls for the nontriviality proof at b=infinity.
 for vx,vy in itertools.product(range(-15,6),repeat=2):
  if min(vx,vy)>=0:ck(min(p*vx,p*vy,vx)>=0)
  else:
   m=min(vx,vy);ck(p*m<vx);ck(p*m!=-1)
print(json.dumps({'status':'PASS','primes_checked':list(primes),'exact_assertions':checks,'scope':'Polynomial identities, Frobenius truncations and valuation arithmetic only; the profinite section and torsor arguments require the written proof. The counterexample concerns a section-fixed-field shortcut, not the original Laurent descent statement.'},indent=2,sort_keys=True))
