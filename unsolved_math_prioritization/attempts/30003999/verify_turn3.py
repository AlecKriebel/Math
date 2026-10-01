"""Exact tests for zero-block deletion and adaptive bounded normalization."""
from fractions import Fraction
from itertools import combinations,product
import json

def sgn(x):return (x>0)-(x<0)
def collect(terms):
 d={}
 for e,a in terms:d[e]=d.get(e,0)+a
 return sorted((e,a) for e,a in d.items() if a)
def remove_zero_blocks(p,q,terms):
 ts=collect(terms)
 if not ts:return []
 B=sum(abs(a) for e,a in ts).bit_length();blocks=[];cur=[]
 for t in ts:
  if cur and t[0]-cur[-1][0]>B:blocks.append(cur);cur=[]
  cur.append(t)
 blocks.append(cur);kept=[]
 for block in blocks:
  lo=block[0][0];base=Fraction(p,q)
  value=sum((a*base**(e-lo) for e,a in block),Fraction(0))
  if value:kept+=block
 return kept

def interval(p,q,ts,P):
 A=sum(abs(a) for e,a in ts);B=A.bit_length();E=ts[-1][0]
 c=1
 while p**c<2*q**c:c+=1
 D=c*(P+B+2);rho=Fraction(q,p)
 S=sum((a*rho**(E-e) for e,a in ts if E-e<D),Fraction(0))
 error=A*rho**D
 return S,error,D

def adaptive(p,q,terms):
 ts=remove_zero_blocks(p,q,terms)
 if not ts:return 0,0,0
 P=1;maxD=0
 while True:
  S,error,D=interval(p,q,ts,P);maxD=max(maxD,D)
  if S>error:return 1,P,maxD
  if S<-error:return -1,P,maxD
  P*=2

cases=0;maxP=0
for p,q in ((2,1),(3,2),(5,3),(5,4)):
 alpha=Fraction(p,q)
 for m in range(1,5):
  for exps in combinations(range(6),m):
   for coeff in product((-2,-1,1,2),repeat=m):
    terms=list(zip(exps,coeff));value=sum((a*alpha**e for e,a in terms),Fraction(0))
    answer,P,D=adaptive(p,q,terms)
    assert answer==sgn(value)
    cases+=1;maxP=max(maxP,P)
# A symbolic zero high block with a 101-digit gap is stripped in small bit work.
E=10**100;terms=[(E+2,4),(E+1,-12),(E,9),(0,-1)]
assert remove_zero_blocks(3,2,terms)==[(0,-1)];cases+=1
assert adaptive(3,2,terms)[0]==-1;cases+=1
S,error,D=interval(3,2,collect(terms),1)
assert S==0 and error>0;cases+=1
# Actual slow-width family of Turn 2; no large power is expanded here.
families=[]
for m in (3,4,5,8,12,20,50,100,300):
 B=m.bit_length();Ws=[0];gaps=[]
 for j in range(1,m):
  gap=2*(B+Ws[-1]+1)-1;gaps.append(gap);Ws.append(Ws[-1]+gap)
 assert Ws[-1]==(2*B+1)*(3**(m-1)-1)//2;cases+=1
 assert Fraction(m)*Fraction(2,3)**gaps[0]<Fraction(2,3);cases+=1
 E=Ws[-1];ts=[(E,1)]+[(E-Ws[j],-1) for j in range(1,m)]
 answer,P,D=adaptive(3,2,ts)
 assert answer==1 and P==1;cases+=1
 families.append({'terms':m,'largest_exponent_bitlength':E.bit_length(),'conservative_expanded_width_bitlength':Ws[-1].bit_length(),'adaptive_precision':P,'largest_power_expanded_by_truncation_below':D})
print(json.dumps({'status':'PASS','exact_cases_and_assertions':cases,'finite_enumeration_max_precision':maxP,'slow_conservative_fast_adaptive_families':families,'limitations':'An actual cost obstruction for one conservative implementation and a precision-dependent exact alternative, not a lower bound for the original problem or a general polynomial-time sign result.'},indent=2))
