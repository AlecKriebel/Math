#!/usr/bin/env python3
"""Exact, finite checks. No finite computation proves general settledness.
Requires Python 3 and SymPy. Polynomials are ascending coefficient lists.
Rabin irreducibility certificates are checked independently of factor_list.
"""
import json, random, sys, warnings
from pathlib import Path
from fractions import Fraction
import sympy as sp
from sympy.utilities.exceptions import SymPyDeprecationWarning
warnings.simplefilter('ignore', SymPyDeprecationWarning)
random.seed(30000492)
x=sp.Symbol('x')

def trim(a,p):
 a=[v%p for v in a]
 while len(a)>1 and not a[-1]: a.pop()
 return a

def add(a,b,p):
 c=[0]*max(len(a),len(b))
 for i,v in enumerate(a):c[i]+=v
 for i,v in enumerate(b):c[i]+=v
 return trim(c,p)

def mul(a,b,p):
 c=[0]*(len(a)+len(b)-1)
 for i,v in enumerate(a):
  for j,w in enumerate(b):c[i+j]=(c[i+j]+v*w)%p
 return trim(c,p)

def rem(a,b,p):
 a=trim(a,p); inv=pow(b[-1],-1,p)
 while a!=[0] and len(a)>=len(b):
  k=len(a)-len(b);s=a[-1]*inv%p
  for j,v in enumerate(b):a[k+j]=(a[k+j]-s*v)%p
  a=trim(a,p)
 return a

def gcd(a,b,p):
 while b!=[0]:a,b=b,rem(a,b,p)
 return trim([v*pow(a[-1],-1,p) for v in a],p)

def modpow(a,n,h,p):
 r=[1]
 while n:
  if n&1:r=rem(mul(r,a,p),h,p)
  a=rem(mul(a,a,p),h,p);n//=2
 return r

def irreducible(h,p):
 d=len(h)-1
 if d<1:return False
 if d==1:return True
 targets={d//int(r) for r in sp.factorint(d)}
 y=[0,1]
 for i in range(1,d+1):
  y=modpow(y,p,h,p)
  z=add(y,[0,-1],p)
  if i in targets and gcd(h,z,p)!=[1]:return False
 return z==[0]

def compose(g,f,p):
 r=[0]
 for a in reversed(g):r=add(mul(r,f,p),[a],p)
 return r

def evaluate(g,t,p):
 r=0
 for a in reversed(g):r=(r*t+a)%p
 return r

def factor(g,p):
 _,fs=sp.Poly.from_list(list(reversed(g)),x,modulus=p).factor_list()
 answer=[]; prod=[1]
 for h,e in fs:
  h=[int(v)%p for v in reversed(h.all_coeffs())]
  assert irreducible(h,p)
  for _ in range(e):answer.append(h);prod=mul(prod,h,p)
 assert prod==g,(prod,g)
 return sorted(answer,key=lambda a:(len(a),a))

def orbit(f,p):
 gamma=-f[1]*pow(2,-1,p)%p
 vals=[];t=evaluate(f,gamma,p)
 while t not in vals:vals.append(t);t=evaluate(f,t,p)
 return gamma,vals,vals.index(t)

def typ(g,O,p):
 vals=[evaluate(g,t,p) for t in O]
 assert 0 not in vals
 return ''.join('s' if pow(v,(p-1)//2,p)==1 else 'n' for v in vals)

def profile(f,p,N):
 assert f[-1]==1 and irreducible(f,p)
 gamma,O,tail=orbit(f,p)
 assert 0 not in O
 active=[f];stable_mass=Fraction(0); rows=[]; newly=[]
 for n in range(1,N+1):
  remaining=[];now=[]
  for h in active:
   assert (len(h)-1)%2==0 and irreducible(h,p)
   T=typ(h,O,p)
   if set(T)=={'n'}:
    stable_mass+=Fraction(len(h)-1,2**n);now.append(h)
    newly.append({'depth':n,'coefficients':h,'type':T})
   else:remaining.append(h)
  assert stable_mass+sum((Fraction(len(h)-1,2**n) for h in remaining),Fraction())==1
  rows.append({'n':n,'stable_mass':str(stable_mass),'new_stable_factors':len(now),'unstable_factors':len(remaining),'unstable_types':{T:sum(len(h)-1 for h in remaining if typ(h,O,p)==T) for T in sorted(set(typ(h,O,p) for h in remaining))}})
  if n<N:active=[k for h in remaining for k in factor(compose(h,f,p),p)]
 return {'p':p,'f':f,'critical_point':gamma,'postcritical_orbit':O,'tail_from_postcritical_orbit':tail,'rows':rows,'newly_stable_certificates':newly}

def fixed_family():
 out=[]
 for p in [3,5,7,11,13,17,31]:
  a=next(a for a in range(1,p) if pow((-a)%p,(p-1)//2,p)==p-1)
  f=[(a*a+a)%p,(-2*a)%p,1]
  r=0;u=p+1
  while u%2==0:r+=1;u//=2
  threshold=1 if p%4==1 else r
  P=profile(f,p,min(threshold+2,7))
  for row in P['rows']:assert Fraction(row['stable_mass'])==int(row['n']>=threshold)
  P['proved_stable_threshold']=threshold
  # Independently factor complete iterates up to bounded depth and check degree formula.
  I=[0,1]; degrees=[]
  for n in range(1,min(threshold+1,6)+1):
   I=compose(I,f,p);fs=factor(I,p)
   predicted=2**n if p%4==1 else 2**max(1,n-r+1)
   assert all(len(h)-1==predicted for h in fs)
   degrees.append({'n':n,'degree':predicted,'factor_count':len(fs)})
  P['full_factor_degree_checks']=degrees;out.append(P)
 return out

def markov_witness():
 p=7;f=[1,0,1];g=[5,4,1];O=[1,2,5]
 I=[0,1]
 for _ in range(4):I=compose(I,f,p)
 assert rem(I,g,p)==[0]
 fourth=factor(I,p)
 assert g in fourth
 assert irreducible(g,p) and typ(g,O,p)=='nns'
 current=[g]; levels=[]
 for k in range(4):
  levels.append([{'coefficients':h,'type':typ(h,O,p)} for h in current])
  if k<3:current=[v for h in current for v in factor(compose(h,f,p),p)]
 assert len(current)==2
 assert all(pow(evaluate(h,1,p)*evaluate(h,2,p)%p,3,p)==1 for h in current)
 # Old one-step model: nns -> nss -> sss. Postcritical tail has length 2,
 # so identical child types must have second digit equal to third.
 allowed=['nnn','nss','snn','sss']
 forbidden=[T for T in allowed if T[0]!=T[1]]
 assert forbidden==['nss','snn']
 return {'p':p,'f':f,'g':g,'levels':levels,'old_model_grandchild_types':allowed,'theorem_excludes':forbidden,'occurs_at_iterate':4,'fourth_iterate_factors':fourth}

def characteristic_two():
 f=[1,1,1];I=[0,1];rows=[]
 for n in range(1,7):
  I=compose(I,f,2);fs=factor(I,2)
  assert all((len(h)-1)%2==0 for h in fs)
  for h in fs:
   first=compose(h,f,2)
   if irreducible(first,2):assert not irreducible(compose(first,f,2),2)
  rows.append({'n':n,'degree':len(I)-1,'factor_degrees':[len(h)-1 for h in fs]})
 return {'f':f,'p':2,'rows':rows,'first_three':[[1,1,1],[1,1,0,0,1],[1,1,1,0,1,0,0,0,1]],'stable_mass_all_n_by_proof':'0'}

def main():
 result={'problem_id':30000492,'scope':'exact finite evidence and checks of proved special cases; no general settledness proof','software':{'python':sys.version.split()[0],'sympy':sp.__version__},'odd_profiles':[profile(f,p,n) for p,f,n in [(7,[1,0,1],9),(5,[2,0,1],8),(3,[2,2,1],8),(11,[1,0,1],7),(13,[5,0,1],7)]],'fixed_critical_point_family':fixed_family(),'markov_missing_transition':markov_witness(),'characteristic_two':characteristic_two()}
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
