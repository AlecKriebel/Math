"""Exact finite diagnostics for EP783; no author code, no asymptotic certificate."""
from fractions import Fraction as F
from itertools import combinations
from math import gcd, prod
from pathlib import Path
import json, hashlib

count=0
def check(t):
    global count
    count+=1
    if not t: raise ArithmeticError(count)

def primes(n):
    return [p for p in range(2,n+1) if all(p%d for d in range(2,int(p**.5)+1))]

ps=primes(100)
tail=[]
for p in reversed(ps):
    if sum((F(1,q) for q in tail),F())+F(1,p)>F(1,2): break
    tail.append(p)
A=sorted(tail);B=sorted(set(A)-{17,23}|{7})
check(p==13 and A==[17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97])
for s in (A,B):
    check(all(gcd(a,b)==1 for a,b in combinations(s,2)))
    check(sum((F(1,a) for a in s),F())<F(1,2))
    check(all(a*b>100 for a,b in combinations(s,2)))
    check(sum(any(n%a==0 for a in s) for n in range(1,101))==sum(100//a for a in s))
check(sum(all(n%a for a in A) for n in range(1,101))==62)
check(sum(all(n%a for a in B) for n in range(1,101))==57)
check(sum((F(1,a) for a in A),F())==F(35224176913494639959138427813071,76775489974875738420016721522869))
check(sum((F(1,a) for a in B),F())==F(686355084015973446882109176506,1374497262977315010077025705013))
# All coprime subsets of [2,15], and each N<=40: genuine avoidance event.
families=[()]
for a in range(2,16):
    families += [s+(a,) for s in list(families) if all(gcd(a,b)==1 for b in s)]
for s in families:
    for N in range(1,41):
        exact=F(sum(all(n%a for a in s) for n in range(1,N+1)),N)
        for r in range(min(len(s),4)+1):
            trunc=sum((F((-1)**j*(N//prod(c)),N) for j in range(r+1) for c in combinations(s,j)),F())
            check(trunc>=exact if r%2==0 else trunc<=exact)
        check(exact>=1-sum((F(1,a) for a in s),F()))
check((2%4!=0) and gcd(2,4)!=1)  # Detect the printed wrong gcd indicator.
check((F(1,10)+F(1,10))>F(1,10)) # Fixed errors must add.
out={'verdict':'PASS','checks':count,'N100':{'greedy':A,'replacement':B,'unsieved':[62,57]},'families':len(families),'source_programs_executed':False,'scope':'Finite diagnostics only; asymptotic proof is written and uses explicit classical inputs.','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(out,sort_keys=True,indent=2))
