#!/usr/bin/env python3
"""Universal n=5 obstruction certificate from all possible collision relations."""
import itertools, json, math
from pathlib import Path
from fractions import Fraction

def rank(rows):
 a=[[Fraction(x) for x in row] for row in rows]; r=0
 for c in range(4):
  pivot=next((i for i in range(r,len(a)) if a[i][c]),None)
  if pivot is None:continue
  a[r],a[pivot]=a[pivot],a[r]
  z=a[r][c];a[r]=[x/z for x in a[r]]
  for i in range(len(a)):
   if i!=r:
    z=a[i][c];a[i]=[x-z*y for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r

def det(a):
 if not a:return 1
 return sum((-1)**j*a[0][j]*det([row[:j]+row[j+1:] for row in a[1:]]) for j in range(len(a)))

def gcd_minors(rows,r):
 if r==0:return 1
 ans=0
 for I in itertools.combinations(range(len(rows)),r):
  for J in itertools.combinations(range(4),r):
   val=abs(det([[rows[i][j] for j in J] for i in I]))
   ans=math.gcd(ans,val)
   if ans==1:return 1
 return ans

def forced_equalities(rows):
 rnk=rank(rows) if rows else 0
 d=gcd_minors(rows,rnk)
 out=[]
 for i,j in itertools.combinations(range(5),2):
  v=[int(k==i)-int(k==j) for k in range(1,5)]
  if rank(rows+[v])!=rnk:continue
  d2=gcd_minors(rows+[v],rnk)
  order=d//d2
  if order and order&(order-1)==0:out.append({'pair':[i,j],'power_of_two_order':order})
 return out

def main():
 cycles=[(0,)+p for p in itertools.permutations(range(1,5)) if p[0]<p[-1]]
 ce=[{tuple(sorted((a[i],a[(i+1)%5]))) for i in range(5)} for a in cycles]
 events=[]; groups=[]
 for Q in itertools.combinations(range(5),4):
  a,b,c,d=Q
  g=[]
  for left,right in [((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))]:
   row=[int(k in left)-int(k in right) for k in range(1,5)]
   cover=sum(1<<i for i,E in enumerate(ce) if left in E and right in E)
   g.append(len(events));events.append({'edges':[left,right],'row':row,'cover':cover})
  groups.append(g)
 full=(1<<len(cycles))-1; covers=[]
 for choices in itertools.product(range(-1,3),repeat=5):
  ids=[groups[i][x] for i,x in enumerate(choices) if x>=0]
  mask=0
  for j in ids:mask|=events[j]['cover']
  if mask!=full:continue
  # Store only inclusion-minimal covers.
  if any((__import__('functools').reduce(int.__or__,[events[j]['cover'] for j in ids if j!=q],0)==full) for q in ids):continue
  eq=forced_equalities([events[j]['row'] for j in ids])
  covers.append({'event_indices':ids,'forced_equalities':eq})
 result={'n':5,'cycles':cycles,'events':events,'minimal_hitting_patterns':covers,'all_impossible_in_odd_groups':all(x['forced_equalities'] for x in covers)}
 Path('five_vertex_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
 print('minimal patterns',len(covers),'impossible',result['all_impossible_in_odd_groups'])
 for c in covers:print(c)
if __name__=='__main__':main()
