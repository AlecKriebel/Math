#!/usr/bin/env python3
"""New independent finite falsification by set enumeration and compatibility search.
Explicit guards survive optimization; these are corroboration, never a hardness proof.
"""
from itertools import combinations
import json

def require(c,m):
 if not c: raise RuntimeError(m)

def subs(xs):
 xs=tuple(xs)
 for k in range(len(xs)+1):
  for a in combinations(xs,k):yield frozenset(a)

def sums(a,n=None):
 return frozenset(x+y if n is None else (x+y)%n for x,y in combinations_with_diagonal(a))

def combinations_with_diagonal(a):
 a=sorted(a)
 for i,x in enumerate(a):
  for y in a[i:]:yield x,y

def int_yes(s):
 if not s:return True
 lo,hi=min(s),max(s)
 if lo%2 or hi%2:return False
 return any(sums(a)==s for a in subs(range(lo//2,hi//2+1)))

def cyclic_yes_by_compatibility(n,b):
 # Every possible root element has diagonal 2a in b. Search ALL such elements,
 # including large residues; no anchor or no-wrap conclusion is assumed.
 if not b:return True
 candidates=[a for a in range(n) if (2*a)%n in b]
 def visit(start,chosen,covered):
  if covered==b:return True
  for idx in range(start,len(candidates)):
   x=candidates[idx]
   extra=frozenset({(2*x)%n}|{(x+y)%n for y in chosen})
   if extra<=b and visit(idx+1,chosen+(x,),covered|extra):return True
  return False
 return visit(0,(),frozenset())

def transfer(s,restricted=False):
 if not s:return 3,frozenset({0}) if restricted else frozenset()
 t=min(s)
 if t%2:return 5,frozenset({0,1})
 b=frozenset(x-t for x in s)
 return max(3,2*max(b)+1),b

def prime(n):
 for p in range(max(3,n),max(4,2*n)):
  if all(p%d for d in range(2,int(p**0.5)+1)):return p
 raise RuntimeError('prime unavailable')

counts={'roots_enumerated':0,'odd_every_root_checks':0,'even_translated_root_checks':0,'signed_source_sets':0,'restriction_checks':0,'sidon_sizes':0}
for n in range(1,15):
 for a in subs(range(n)):
  b=sums(a,n);counts['roots_enumerated']+=1
  require(len(a)<=len(b),'cardinality')
  if 0 in b and all(2*x<n for x in b):
   if n%2:
    require(0 in a and a<=b and sums(a)==b,'odd universal root')
    counts['odd_every_root_checks']+=1
   else:
    anchor=next(x for x in a if (-x)%n in a)
    shifted=frozenset((x-anchor)%n for x in a)
    require((2*anchor)%n==0 and 0 in shifted and sums(shifted)==b,'even translation')
    counts['even_translated_root_checks']+=1
for s in subs(range(-6,7)):
 truth=int_yes(s)
 for restricted in [False,True]:
  n,b=transfer(s,restricted)
  require(cyclic_yes_by_compatibility(n,b)==truth,'total signed reduction '+repr(s))
  if restricted:
   require(n%2 and b and 0 in b and all(2*x<n for x in b),'restricted image')
   counts['restriction_checks']+=1
 counts['signed_source_sets']+=1
for q in range(1,201):
 p=prime(q)
 points=[2*p*x+(x*x)%p for x in range(q)]
 values=list(x+y for x,y in combinations_with_diagonal(points))
 require(len(set(values))==q*(q+1)//2 and max(points)<=4*q*q,'corrected Sidon')
 counts['sidon_sizes']+=1
# Demonstrate the literal graph failure and the repaired value.
full=[22*x+(x*x)%11 for x in range(11)]
require(len(full)==11 and max(full)==221>4*6*6 and max(full[:6])==113,'literal graph control')
require(sums({1,4},5)=={0,2,3} and not int_yes({0,2,3}),'no-wrap control')
require(sums({3},5)=={1} and not int_yes({1}),'normalization control')
require(sums({2},4)=={0} and sums({2})!={0},'even all-root control')
require(sums({1,3},4)=={0,2} and not int_yes({0,2}),'strict equality control')
require(frozenset((x+y)%5 for x,y in combinations({1,4},2))=={0},'distinct pair control')
require(8*(4*5**8)+2==12500002<2**24 and 512*(16**2)==2**17,'coarse constants')
print(json.dumps({'all_checks_passed':True,'finite_role':'corroboration only','mechanism':'full small-group unordered pairs; general diagonal-candidate compatibility search, with no assumed root anchor','counts':counts,'countercontrols':6},sort_keys=True,indent=2))
