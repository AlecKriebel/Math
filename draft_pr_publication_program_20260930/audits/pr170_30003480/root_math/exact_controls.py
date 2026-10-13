"""ROOT exact finite controls; all-polynomial theorem still requires the written proof."""
from fractions import Fraction as Q
from itertools import product
from math import prod
import argparse,json
p=argparse.ArgumentParser();p.add_argument("--mutate",choices=["none","weights","reflection","normalization","Q2"],default="none");args=p.parse_args()
counts={}
def require(ok,label):
 if not ok:raise RuntimeError(label)
 counts[label]=counts.get(label,0)+1
def ds(t):return tuple(v*(1-v) for v in t)
def weights(t):
 a,b,c=t;den=3 if args.mutate=="weights" else 2
 return (1-sum(t)/den,(b+c-a)/den,(a+c-b)/den,(a+b-c)/den)
valid=outside=0
for denominator in [4,8,16,24]:
 for ints in product(range(denominator//2+1),repeat=3):
  t=tuple(Q(i,denominator) for i in ints)
  if not all(t[i]<=sum(t)-t[i] for i in range(3)):outside+=1;continue
  valid+=1;w=weights(t)
  require(min(w)>=0 and sum(w)==1,"parity weights nonnegative and sum one")
  require(w[0]>=Q(1,4),"parity constant weight lower bound")
  bitone=(w[2]+w[3],w[1]+w[3],w[1]+w[2])
  require(bitone==t,"exact real parity marginals")
  require(ds(bitone)==ds(t),"exact parity determinants")
for den in range(4,31,2):
 for bi in range(1,den//2):
  for ci in range(1,den//2-bi):
   b,c=Q(bi,den),Q(ci,den);t=(b+c,b,c);d=ds(t)
   gaps=(d[1]+d[2]-d[0],d[0]+d[2]-d[1],d[0]+d[1]-d[2])
   require(gaps==(2*b*c,2*c*(1-b-c),2*b*(1-b-c)) and min(gaps)>0,"true-boundary determinant H interior")
for t in [(Q(1,3),)*3,(Q(2,5),Q(3,10),Q(3,10)),(Q(9,20),Q(7,20),Q(1,5))]:
 d=ds(t);require(sum(t)==1 and max(t)<Q(1,2),"reflected plane strictly in half cube")
 for i in range(3):
  others=[j for j in range(3) if j!=i]
  require(d[others[0]]+d[others[1]]-d[i]==2*t[others[0]]*t[others[1]]>0,"reflected plane H interior")
for t in [(Q(1,4),Q(1,8),Q(1,8)),(Q(1,3),)*3,(Q(7,16),Q(1,8),Q(1,16))]:
 tau=((2 if args.mutate=="reflection" else 1)-t[0],t[1],t[2])
 require(ds(tau)==ds(t),"polynomial-coordinate involution identity")
 require(tau[0]-tau[1]-tau[2]==-(sum(t)-1),"true plane reflected exactly")
 for powers in product(range(5),repeat=3):
  if sum(powers)>6:continue
  require(prod(v**k for v,k in zip(ds(tau),powers))==prod(v**k for v,k in zip(ds(t),powers)),"pullback monomial invariance")
tensor_cases=0
for entries in product([-1,0,1],repeat=8):
 total=sum(x*x for x in entries)
 if not total:continue
 normalized=[]
 for i in range(3):
  rows=[[],[]]
  for bits in product([0,1],repeat=2):
   for value in [0,1]:
    index=list(bits);index.insert(i,value);position=index[0]*4+index[1]*2+index[2];rows[value].append(entries[position])
  aa=sum(x*x for x in rows[0]);bb=sum(x*x for x in rows[1]);ab=sum(x*y for x,y in zip(*rows))
  det=aa*bb-ab*ab
  d=Q(det,total if args.mutate=="normalization" else total*total)
  require(0<=d<=Q(1,4),"normalized integer-tensor determinant bound")
  normalized.append(d)
 for i in range(3):require(normalized[i]<=sum(normalized)-normalized[i],"integer tensor determinant triangles")
 tensor_cases+=1
r=(Q(49,100),Q(36,100),Q(36,100),Q(1,100));d=tuple(x*x for x in r)
q1=prod(sum(d)-2*x for x in d)
signs=list(product([-1,1],repeat=4));signs=signs[:8] if args.mutate=="Q2" else signs
q2=Q(1,2)*prod(sum(s*x for s,x in zip(sign,r)) for sign in signs)
require(q1==Q(168760917,305175781250),"printed Q1 exact value")
require(q2==Q(23632249608,2384185791015625),"printed full-sign Q2 exact value")
require(q1-q2==Q(2589624828909,4768371582031250)>0,"printed positive counterexample passes polynomial")
require(all(0<x<Q(1,4) for x in d) and all(x<sum(d)-x for x in d),"positive counterexample strict cube H interior")
thresholds=(Q(2,5),Q(1,6),Q(1,6),Q(1,100))
require(d[0]>thresholds[0]*(1-thresholds[0]),"largest eigenvalue exact lower bound")
require(all(d[i]<thresholds[i]*(1-thresholds[i]) for i in [1,2,3]),"other eigenvalue exact upper bounds")
require(sum(thresholds[1:])==Q(103,300)<thresholds[0],"counterexample polygon failure exact separation")
d3=(Q(1,4),)*3;r3=(Q(1,2),)*3
ghzq1=prod(sum(d3)-2*x for x in d3)
ghzq2=Q(1,2)*prod(sum(s*x for s,x in zip(sign,r3)) for sign in product([-1,1],repeat=3))
require((ghzq1,ghzq2)==(Q(1,64),Q(9,512)),"GHZ printed formula exact values")
require(ghzq1<ghzq2 and (d3[0]-d3[1])**2+Q(1,2)*(d3[0]+d3[1])==Q(1,4)>Q(3,16),"GHZ printed secondary direction fails")
print(json.dumps(dict(status="EXACT_FINITE_CONTROLS_PASS",mutate=args.mutate,counts=counts,total_checks=sum(counts.values()),valid_eigenvalue_grid_cases=valid,outside_eigenvalue_grid_cases=outside,integer_tensor_cases=tensor_cases,all_polynomial_nonexistence_proved_by_finite_checks=False,exact_counterexample=dict(d=[str(x) for x in d],Q1=str(q1),Q2=str(q2),difference=str(q1-q2))),sort_keys=True))
