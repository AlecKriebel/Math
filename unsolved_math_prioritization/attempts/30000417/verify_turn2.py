#!/usr/bin/env python3
from itertools import combinations,product
from random import Random
import json
count=0

def check(v,label):
 global count
 count+=1
 if not v:raise AssertionError(label)

def path_color(lists,d):
 lists=[sorted(a)[:2*d] for a in lists]
 delta=[2*d-len(a) for a in lists]
 if sum(delta)>=2*d:return None
 if not lists:return []
 layers=[set(lists[0])]
 for i,A in enumerate(lists[1:],1):
  layers.append({b for b in A if any(abs(a-b)>=d for a in layers[-1])})
  check(len(layers[-1])>=2*d-sum(delta[:i+1]),'terminal-cardinality induction')
 check(bool(layers[-1]),'nonempty weighted terminal set')
 out=[min(layers[-1])]
 for B in reversed(layers[:-1]):out.append(next(a for a in sorted(B) if abs(a-out[-1])>=d))
 return out[::-1]

def certificate(L,d,r,c):
 I=[i for i in range(len(L)) if i%3==r]
 if not I or not all(c in L[i] for i in I):return None
 J=[i for i in range(len(L)) if i not in I]
 A=[{x for x in L[j] if abs(x-c)>=d} for j in J]
 out=path_color(A,d)
 if out is None:return None
 f=[c]*len(L)
 for j,x in zip(J,out):f[j]=x
 check(all(f[i] in L[i] for i in range(len(L))),'source list membership')
 check(all(abs(f[i]-f[j])>=d for i in range(len(L)) for j in range(i+1,min(i+3,len(L)))),'all original constraints')
 return f

# Exhaustive proof-lemma sanity for short ordinary paths.
A=[set(x) for k in range(1,5) for x in combinations(range(1,5),k)]
weighted=0
for d in [1,2,3]:
 for L in product(A,repeat=3):
  if sum(max(0,2*d-len(x)) for x in L)<2*d:
   out=path_color(L,d)
   check(out is not None and all(out[i] in L[i] for i in range(3)),'weighted path witness')
   check(all(abs(out[i]-out[i+1])>=d for i in range(2)),'weighted path edges')
   weighted+=1
check(path_color([{1,2},{1,2}],2) is None,'strict budget equality negative control')
# Exact induced-path geometry for each offset and all boundaries in the range.
for n in range(3,101):
 for r in range(3):
  J=[i for i in range(n) if i%3!=r]
  for a,b in combinations(range(len(J)),2):
   check((J[b]-J[a]<=2)==(b==a+1),'residual graph exactly path')
# All-parameter integer ceiling inequality controls.
for n in range(3,101):
 for d in range(1,51):
  k=(3*d*(n-1))//n+1;h=(3*d+n-1)//n-1;q=(2*n)//3
  check(k==3*d-h,'floor/ceiling identity')
  check(q*h<2*d,'strict deficit budget')
  check(k-d>0,'positive remaining lower cardinality')
# Structured sparse global extrema and their reflections.
rng=Random(300004172);structured=0;nonextreme=0
for n in range(3,28):
 for d in range(1,8):
  k=(3*d*(n-1))//n+1
  sizes=[sum(i%3==r for i in range(n)) for r in range(3)]
  for r in range(3):
   if sizes[r]!=max(sizes):continue
   for rep in range(4):
    L=[]
    for i in range(n):
     if i%3==r:L.append({1,*rng.sample(range(2,8*d+20),k-1)})
     else:L.append(set(rng.sample(range(2,8*d+20),k)))
    check(certificate(L,d,r,1) is not None,'sparse global minimum family')
    top=10*d+100;R=[{top-x for x in a} for a in L]
    check(certificate(R,d,r,top-1) is not None,'reflected global maximum family')
    structured+=2
# Nonextremal common labels: retained lists avoid the forbidden interval and have 2d labels.
for n in range(4,21):
 for d in range(1,6):
  c=100;r=0;L=[]
  for i in range(n):
   if i%3==r:L.append({c,200,*range(1,2*d+1)})
   else:L.append(set(range(1,2*d+1)))
  check(min(set().union(*L))<c<max(set().union(*L)),'genuinely nonextremal common label')
  check(certificate(L,d,r,c) is not None,'nonextremal common-label certificate')
  nonextreme+=1
print(json.dumps(dict(problem_id=30000417,turn=2,status='all controls passed',assertions=count,weighted_path_assignments=weighted,structured_extremum_assignments=structured,nonextremal_assignments=nonextreme,scope='All-size sufficient theorem; original arbitrary-list floor conjecture remains unresolved.',dependencies='Python 3 standard library'),indent=2))
