#!/usr/bin/env python3
"""Pure-Python independent verification of all saved stable certificates.
No author module or computer-algebra library is imported. Descending coefficients.
"""
import hashlib,json,sys

def clean(a,p):
 b=tuple(x%p for x in a)
 j=next((j for j,x in enumerate(b) if x),len(b))
 return b[j:]
def minus(a,b,p):
 n=max(len(a),len(b));a=(0,)*(n-len(a))+a;b=(0,)*(n-len(b))+b
 return clean(tuple(x-y for x,y in zip(a,b)),p)
def product(a,b,p):
 if not a or not b:return ()
 c=[0]*(len(a)+len(b)-1)
 for i,u in enumerate(a):
  for j,v in enumerate(b):c[i+j]+=u*v
 return clean(c,p)
def residue(a,b,p):
 if not b:raise ZeroDivisionError
 while a and len(a)>=len(b):
  t=a[0]*pow(b[0],-1,p)%p
  subtract=tuple(t*u for u in b)+(0,)*(len(a)-len(b))
  a=minus(a,subtract,p)
 return a
def common(a,b,p):
 while b:a,b=b,residue(a,b,p)
 if not a:return ()
 return clean(tuple(u*pow(a[0],-1,p) for u in a),p)
def power(base,e,mod,p):
 out=(1,)
 for bit in bin(e)[2:]:
  out=residue(product(out,out,p),mod,p)
  if bit=='1':out=residue(product(out,base,p),mod,p)
 return out
def evaluate(h,t,p):
 a=0
 for c in h:a=(a*t+c)%p
 return a
def prime_divisors(d):
 out=[];r=2
 while r*r<=d:
  if d%r==0:
   out.append(r)
   while d%r==0:d//=r
  r+=1
 if d>1:out.append(d)
 return out
def irreducible(h,p):
 d=len(h)-1
 if d<1 or h[0]!=1:return False
 if d==1:return True
 needed={d//r for r in prime_divisors(d)}
 z=(1,0)
 for j in range(1,d+1):
  z=power(z,p,h,p)
  difference=minus(z,(1,0),p)
  if j in needed and len(common(h,difference,p))!=1:return False
 return not difference

def verify(path):
 raw=open(path,'rb').read();r=json.loads(raw);counts={};total=0
 for profile in r['odd_profiles']+r['fixed_critical_point_family']:
  p=profile['p'];f=tuple(reversed(profile['f']));orbit=profile['postcritical_orbit'];gamma=profile['critical_point']
  assert evaluate(f,gamma,p)==orbit[0]
  assert all(evaluate(f,a,p)==b for a,b in zip(orbit,orbit[1:]))
  assert evaluate(f,orbit[-1],p) in orbit
  for certificate in profile['newly_stable_certificates']:
   h=tuple(reversed(certificate['coefficients']));n=certificate['depth']
   assert irreducible(h,p)
   # Verify h divides f^n using modular forward recurrence rather than author factor lineage.
   z=(1,0)
   for _ in range(n):
    r0=()
    for c in f:r0=minus(residue(product(r0,z,p),h,p),(-c,),p)
    z=r0
   assert not z
   assert all(pow(evaluate(h,b,p),(p-1)//2,p)==p-1 for b in orbit)
   total+=1;counts[str(p)]=counts.get(str(p),0)+1
 # Reject controls that have the same nominal degrees as positive certificates.
 controls=[((1,0,1),2),((1,0,6),7),((1,0,2,0,1),7),((1,),7)]
 assert all(not irreducible(h,p) for h,p in controls)
 for level in r['markov_missing_transition']['levels']:
  for obj in level:assert irreducible(tuple(reversed(obj['coefficients'])),7)
 return {'status':'passed','author_results_sha256':hashlib.sha256(raw).hexdigest(),'certificates_verified':total,'by_prime':counts,'membership_checks':'Each saved stable certificate divides the full f^n by a modular forward recurrence','irreducibility_checks':'Pure-Python Rabin test, descending-coefficient implementation, no author imports or SymPy','negative_controls':len(controls),'witness_polynomials_verified':sum(map(len,r['markov_missing_transition']['levels']))}
if __name__=='__main__':print(json.dumps(verify(sys.argv[1]),indent=2,sort_keys=True))
