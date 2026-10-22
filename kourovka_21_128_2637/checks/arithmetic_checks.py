from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
import json

def polynomial(es):
 c=[1]
 for e in es:
  n=[0]*(len(c)+1)
  for i,x in enumerate(c):n[i]+=x;n[i+1]+=e*x
  c=n
 return c
pF=polynomial([5,7,11]);pH=polynomial([11,19,29])
chiF=sum((-1)**i*x for i,x in enumerate(pF));chiH=sum((-1)**i*x for i,x in enumerate(pH))
assert pF==[1,23,167,385] and pH==[1,59,1079,6061]
assert chiF==-240 and chiH==-5040
assert F(chiF,576)==F(-5,12) and F(chiH,7200)==F(-7,10)
assert F(7,10)/F(5,12)==F(42,25)
assert lcm(12//gcd(12,42),30//gcd(30,25))==6
assert [12//gcd(12,w) for w in [2,3]]==[6,4]
assert [60//gcd(60,w) for w in [4,6,10]]==[15,10,6]
assert F(-5,12)*12==-5 and F(-7,10)*60==-42
assert 42*5==5*42==210
cycle=tuple((i+1)%15 for i in range(15));p=tuple(range(15));orders=[]
for k in range(1,16):
 p=tuple(cycle[p[i]] for i in range(15))
 if p==tuple(range(15)):orders.append(k)
assert orders==[15]
out={'Q_F_Poincare':pF,'Q_H_Poincare':pH,'pure_chi':[chiF,chiH],'G_chi':['-5/12','-7/10'],'G_common_index_ratio':'42/25','torsion_free_G_indices':[252,150],'K_indices':[12,60],'K_chi':[-5,-42],'K_common_indices':[42,5],'common_top_L2_for_s_1':210,'basis_cycle_order':15,'scope':'Arithmetic conditional on credited group and arrangement theorems; no full resolution.'}
print(json.dumps(out,indent=2));Path(__file__).with_name('arithmetic_results.json').write_text(json.dumps(out,indent=2)+'\n')
