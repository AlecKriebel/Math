#!/usr/bin/env python3
"""Finite exact checks for formulas used in DERIVATION.md; not a proof substitute."""
from itertools import product
from pathlib import Path
import json
import sys
sys.set_int_max_str_digits(100000)

def matmul(x,y):
 a,b,c,d=x; e,f,g,h=y
 return (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h)
def inverse(x):
 a,b,c,d=x
 assert a*d-b*c==1
 return (d,-b,-c,a)
def power(x,n):
 if n<0: return power(inverse(x),-n)
 out=(1,0,0,1)
 while n:
  if n&1: out=matmul(out,x)
  x=matmul(x,x); n//=2
 return out
def commutator(x,y):
 return matmul(matmul(matmul(x,y),inverse(x)),inverse(y))
def trace(x):return x[0]+x[3]
def reduce_word(w):
 out=[]
 for x in w:
  if out and out[-1]==-x: out.pop()
  else: out.append(x)
 return tuple(out)
def invword(w):return tuple(-x for x in reversed(w))
def cyclic_reduce(w):
 w=reduce_word(w); i=0; j=len(w)
 while i<j and w[i]==-w[j-1]:i+=1;j-=1
 return w[i:j]
def concat(*words):return reduce_word(x for w in words for x in w)
def minrotation(w):
 n=len(w)
 if not n:return w
 s=w+w;i=0;j=1;k=0
 while i<n and j<n and k<n:
  if s[i+k]==s[j+k]:k+=1;continue
  if s[i+k]>s[j+k]:
   i=i+k+1
   if i<=j:i=j+1
  else:
   j=j+k+1
   if j<=i:j=i+1
  k=0
 start=min(i,j)
 return s[start:start+n]
def rootfree(w):
 n=len(w); pi=[0]*n
 for i in range(1,n):
  j=pi[i-1]
  while j and w[i]!=w[j]:j=pi[j-1]
  if w[i]==w[j]:j+=1
  pi[i]=j
 period=n-pi[-1]
 return not(period<n and n%period==0)
def horowitz_word(signs):
 w=(1,)
 for m,epsilon in enumerate(signs,1):
  u=w if epsilon==1 else invword(w)
  v=invword(u)
  w=concat(v,(2,)*(2*m),u,(2,)*(2*m-1),v,(2,)*(2*m),u)
 return w
def eval_word(w,A,B):
 mats={1:A,-1:inverse(A),2:B,-2:inverse(B)}
 out=(1,0,0,1)
 for x in w:out=matmul(out,mats[x])
 return out

out={'description':'Exact finite consistency checks; mathematical proof is in DERIVATION.md.','commutators':[],'horowitz':[]}
for mu in (4,5,6):
 A=(1,mu,0,1);B=(1,0,-mu,1);C=A
 for r in range(2,6):
  C=commutator(B,C)
  assert C[1]==-mu**(2**r-1)
  assert trace(C)==2+mu**(2**r)
  out['commutators'].append({'mu':mu,'r':r,'upper_right':str(C[1]),'trace':str(trace(C)),'verified':True})
reps=[((2,1,1,1),(3,2,1,1)),((1,4,0,1),(1,0,-4,1)),((5,2,2,1),(2,3,1,2))]
for m in range(1,6):
 words=[horowitz_word(e) for e in product((-1,1),repeat=m)]
 cyc=[cyclic_reduce(w) for w in words]
 canonical=[minrotation(w) for w in cyc]
 assert len(set(canonical))==2**m
 assert all(rootfree(w) for w in cyc)
 assert not any(minrotation(invword(w)) in set(canonical) for w in cyc)
 trace_digits=[]
 for A,B in reps:
  traces={trace(eval_word(w,A,B)) for w in words}
  assert len(traces)==1
  trace_digits.append(len(str(abs(next(iter(traces))))))
 out['horowitz'].append({'m':m,'number_of_words':len(words),'distinct_conjugacy_classes':len(set(canonical)),'all_root_free':True,'no_inverse_conjugate_pairs':True,'trace_equal_in_three_exact_representations':True,'cyclic_word_lengths':sorted(set(map(len,cyc))),'common_trace_decimal_digits':trace_digits})
p=Path(__file__).with_name('verification_results.json')
p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'commutator_checks':len(out['commutators']),'horowitz_levels':[x['m'] for x in out['horowitz']],'largest_word_family':out['horowitz'][-1]['number_of_words'],'all_checks_passed':True}))
