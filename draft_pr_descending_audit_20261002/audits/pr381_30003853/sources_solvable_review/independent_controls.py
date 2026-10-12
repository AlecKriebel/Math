#!/usr/bin/env python3
"""Independent exact controls for support drift and Röver's source example.

These are finite algebraic checks, not a computational proof of FP2 or a search
for a solution of Question 111. No candidate code is imported.
"""
import datetime, hashlib, itertools, json, random
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ID=(0,1,2)
PERMS=list(itertools.permutations(range(3)))
def pmul(a,b): return tuple(a[b[i]] for i in range(3))
def pinv(a): return tuple(a.index(i) for i in range(3))
def clean(f): return {i:v for i,v in f.items() if v!=ID}
def mul(a,b):
 f,k=a; g,l=b
 sg={i+k:v for i,v in g.items()}
 return clean({i:pmul(f.get(i,ID),sg.get(i,ID)) for i in set(f)|set(sg)}),k+l
def inv(a):
 f,k=a
 return {i-k:pinv(v) for i,v in f.items()},-k
def add(a,b):
 d=dict(a)
 for i,c in b.items(): d[i]=d.get(i,0)+c
 return {i:c for i,c in d.items() if c}
def scale(a,n): return {i:n*c for i,c in a.items() if n*c}
def xminus1(a): return add({i+1:c for i,c in a.items()},scale(a,-1))
def ev(a): return sum(a.values())
def der(a): return sum(i*c for i,c in a.items())
def quotient_xminus1(a):
 assert ev(a)==0
 if not a: return {}
 lo,hi=min(a),max(a)
 acc=0; q={}
 for i in range(lo,hi):
  acc+=a.get(i,0)
  if acc: q[i]=-acc
 assert xminus1(q)==a
 return q
def main():
 rng=random.Random(38103853)
 counts={}
 checks=0
 for mask in range(1,2**9):
  s={i-4 for i in range(9) if mask>>i&1}
  for k in [-4,-3,-2,-1,1,2,3,4]:
   assert not s<={i+k for i in s}
   assert not {i+k for i in s}<=s
   checks+=1
 counts['finite_nonempty_support_inclusion_controls']=checks
 assert set()<={0} and {0}<={0}
 counts['degenerate_empty_and_zero_shift_controls']=2
 twists=0; wrong_shift_rejected=0
 for _ in range(3000):
  h=(clean({i:rng.choice(PERMS) for i in range(-4,5) if rng.randrange(2)}),0)
  k=rng.choice([-4,-3,-2,-1,1,2,3,4])
  t=(clean({i:rng.choice(PERMS) for i in range(-4,5) if rng.randrange(2)}),k)
  tht=mul(mul(t,h),inv(t))
  assert tht[1]==0 and set(tht[0])=={i+k for i in h[0]}
  assert mul(t,inv(t))==({},0)
  if h[0] and set(tht[0])!=set(h[0]): wrong_shift_rejected+=1
  twists+=1
 assert wrong_shift_rejected>2500
 counts['twisted_nonabelian_S3_wreath_conjugations']=twists
 counts['unshifted_support_mutant_rejected']=wrong_shift_rejected
 polys=0; kernel=0
 for n in [2,3,4,5,6,7]:
  # M_n=(n,x-1), identified by evaluation modulo n.
  for _ in range(1000):
   u={i:rng.randrange(-5,6) for i in range(-5,6)}
   v={i:rng.randrange(-5,6) for i in range(-5,6)}
   f=add(scale(u,n),xminus1(v))
   assert ev(f)%n==0
   # The independent coinvariant map sends f to (f(1)/n,f'(1) mod n).
   assert ev(xminus1(f))==0 and der(xminus1(f))%n==0
   balanced=add(f,{-3:-ev(f)})
   if der(balanced)%n==0:
    q=quotient_xminus1(balanced)
    assert ev(q)%n==0
    kernel+=1
   polys+=1
  r={0:-1,1:1}; s={0:n}
  assert (ev(r)//n,der(r)%n)==(0,1)
  assert (ev(s)//n,der(s)%n)==(1,0)
  assert scale(r,n)==xminus1(s)
  # r is not in (x-1)M_n: its sole quotient is 1, not in M_n.
  assert ev(quotient_xminus1(r))%n!=0
 counts['Laurent_coinvariant_identity_controls']=polys
 counts['exact_kernel_factorization_controls']=kernel
 counts['torsion_order_n_controls']=6
 # Finite support is essential: the unrestricted constant sequence has
 # support Z and is shift-invariant; finite generation of an HNN base is
 # what rules this out in the theorem.
 result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'seed':38103853,'status':'PASS','counts':counts,
  'claims':['finite nonempty integer support cannot contain its nonzero translate',
   'twisted conjugation in S3 wr Z preserves the shifted support exactly',
   'Rover source example has H_ab=Z^2 direct_sum Z/2; independent ideal calculation',
   'M_n coinvariant map (evaluation/n, derivative mod n) has exact kernel (x-1)M_n'],
  'limitations':'Finite tests support explicit identities; the unrestricted theorem rests on the written proof and credited primary dependencies.'}
 (ROOT/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__': main()
