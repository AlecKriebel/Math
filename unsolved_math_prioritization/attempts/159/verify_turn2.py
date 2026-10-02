"""Support-only certificates and exact recurrence boundary controls."""
from itertools import product
from fractions import Fraction as F
import json
N=0
def ck(b):
 global N
 N+=1
 assert b
def sums(U,V):
 E={}
 for u in U:
  for v in V:E.setdefault(u+v,[]).append((u,v))
 return E
def supports(d):
 return [(0,)+tuple(i+1 for i in range(d-1) if bits>>i&1)+(d,) for bits in range(1<<(d-1))]
def main():
 direct=excluded=unresolved=coverage=0;examples=[]
 for m in range(1,9):
  for n in range(m,9):
   for U,V in product(supports(m),supports(n)):
    E=sums(U,V);edges=[ps[0] for ps in E.values() if len(ps)==1]
    UA={u for u,v in edges};VB={v for u,v in edges}
    ck({0,m}<=UA and {0,n}<=VB)
    bad=[(u,v) for u,v in product(UA,VB) if len(E[u+v])>1]
    unique=all(len(ps)==1 for ps in E.values())
    if unique:direct+=1;ck(UA==set(U) and VB==set(V));ck(len(E)==len(U)*len(V))
    elif bad:excluded+=1;u,v=bad[0];ck((u,v) in E[u+v] and len(E[u+v])>=2)
    else:
     unresolved+=1
     if len(examples)<5:examples.append({'U':U,'V':V,'forced_U':sorted(UA),'forced_V':sorted(VB)})
    if UA==set(U) and VB==set(V):coverage+=1;ck(unique or bool(bad))
 recurrences=0
 for den in range(2,31):
  for num in range(1,den):
   a=F(num,den)
   for r in range(2,31):
    q=F(1)
    for k in range(1,r):
     q=1-a*q;ck(q>0 and q<1);ck(q==(1-(-a)**(k+1))/(1+a));recurrences+=1
    ck(1+a*q>1)
 print(json.dumps({'problem_id':159,'turn':2,'status':'PASS','exact_assertions':N,'support_scan_max_degrees':[8,8],'direct_sum_pairs':direct,'unit_collision_exclusions':excluded,'unresolved_support_pairs':unresolved,'full_unique_vertex_coverage_pairs':coverage,'first_unresolved_examples':examples,'exact_recurrence_steps':recurrences,'scope':'Finite support filters are not feasibility decisions for residual patterns. All-degree residue exclusion is established in the written proof.'},indent=2))
if __name__=='__main__':main()
