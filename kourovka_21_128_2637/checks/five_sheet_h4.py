"""A natural five-sheet cover of the index-60 H4 kernel, checked over F_101.
A maximal modular rank certifies rational H1=0; a nonmaximal rank only bounds it.
"""
from itertools import permutations,product
from collections import deque
from pathlib import Path
import json
from cover_homology import relators

def mul(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):return tuple(p.index(i) for i in range(len(p)))
def order(p):
 q=tuple(range(len(p)));k=0
 while True:
  k+=1;q=mul(q,p)
  if q==tuple(range(len(p))):return k

def even(p):return sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2==0
I=tuple(range(5));A5=[p for p in permutations(range(5)) if even(p)]
quads=[]
for b in A5:
 if order(b)!=5:continue
 for c in A5:
  if order(c)!=2 or order(mul(b,inv(c)))!=3:continue
  for d in A5:
   if order(d)==2 and order(mul(b,inv(d)))==2 and order(mul(c,inv(d)))==3:
    quads.append([I,b,c,d])
    break
  if quads:break
 if quads:break
assert quads
G=quads[0];perms=[]
for g in G:
 gi=inv(g)
 perms.append(tuple(5*((l+1)%60)+(gi[x] if l%2==0 else g[x]) for l in range(60) for x in range(5)))
invs=[inv(p) for p in perms];n=300
seen={0};todo=[0]
for x in todo:
 for p in perms:
  if p[x] not in seen:seen.add(p[x]);todo.append(p[x])
assert len(seen)==n
rels=relators({(0,1):5,(1,2):3,(2,3):3},15)
# Store each lifted relator boundary as a row. Rank equals rank of cellular d2.
rows=[]
for w in rels:
 for start in range(n):
  pos=start;row={}
  for a in w:
   j=abs(a)-1
   if a>0:edge=4*pos+j;value=1;pos=perms[j][pos]
   else:pos=invs[j][pos];edge=4*pos+j;value=-1
   row[edge]=row.get(edge,0)+value
  assert pos==start
  # Boundary of every relation is zero. Since edges form a connected graph,
  # rank(d2) over any field is at most 4n-(n-1)=3n+1.
  boundary={}
  for edge,c in row.items():
   pos,j=divmod(edge,4)
   boundary[pos]=boundary.get(pos,0)-c
   boundary[perms[j][pos]]=boundary.get(perms[j][pos],0)+c
  assert not any(boundary.values())
  rows.append({k:v for k,v in row.items() if v})

def rank_mod(rows,p):
 basis={}
 for row in rows:
  row={k:v%p for k,v in row.items() if v%p}
  while row:
   k=min(row)
   if k not in basis:
    a=pow(row[k],-1,p);basis[k]={j:v*a%p for j,v in row.items()};break
   a=row[k]
   for j,v in basis[k].items():
    z=(row.get(j,0)-a*v)%p
    if z:row[j]=z
    else:row.pop(j,None)
 return len(basis)
p=101;r=rank_mod(rows,p);upper=3*n+1-r
out={'A5_elements':[list(g) for g in G],'degree':n,'relative_degree_in_K_H':5,'connected':True,'relators_close':True,'boundary_squared_zero':True,'field_prime':p,'rank_d2_mod_p':r,'rank_d1':n-1,'b1_Q_upper_bound':upper,'b1_Q_exact':0 if upper==0 else None,'scope':'One explicitly specified cover only; no exhaustive index-five subgroup classification.'}
print(json.dumps(out,indent=2));Path(__file__).with_name('five_sheet_h4_results.json').write_text(json.dumps(out,indent=2)+'\n')
