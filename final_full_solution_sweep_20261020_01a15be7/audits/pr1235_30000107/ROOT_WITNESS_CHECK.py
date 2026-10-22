#!/usr/bin/env python3
"""Root independent exact rhombus/weighted-sum checks; no external code or service."""
from fractions import Fraction as Q
from itertools import combinations
import json
checks=0
def need(c,s):
 global checks
 checks+=1
 if not c:raise ValueError(s)
def rows_for(r):
 H=[(i,j,r-i-j) for i in range(r+1) for j in range(r-i+1)]
 pos={x:i for i,x in enumerate(H)};rows={}
 for i,j,k in H:
  if i<1 or j<1:continue
  terms=[[(i,j-1,k+1),(i-1,j+1,k),(i,j,k),(i-1,j,k+1)],[(i,j,k),(i-1,j-1,k+2),(i,j-1,k+1),(i-1,j,k+1)],[(i+1,j-1,k),(i-1,j,k+1),(i,j,k),(i,j-1,k+1)]]
  for t,points in enumerate(terms,1):
   v=[0]*len(H)
   for x,s in zip(points,[1,1,-1,-1]):v[pos[x]]+=s
   rows[(t,i,j,k)]=tuple(v)
 # Separate geometric generation by perpendicular unit-rhombus diagonals.
 embed={h:(h[1]-h[0],h[0]+h[1]) for h in H};diags={}
 for a,b in combinations(H,2):
  x,y=embed[a];u,v=embed[b];norm=(x-u)**2+3*(y-v)**2
  if norm in (4,12):diags.setdefault((x+u,y+v),[]).append((norm,a,b,(x-u,y-v)))
 geo=set()
 for pairs in diags.values():
  for left,right in combinations(pairs,2):
   if {left[0],right[0]}!={4,12}:continue
   short,long=sorted([left,right])
   if short[3][0]*long[3][0]+3*short[3][1]*long[3][1]!=0:continue
   v=[0]*len(H)
   for x in long[1:3]:v[pos[x]]+=1
   for x in short[1:3]:v[pos[x]]-=1
   geo.add(tuple(v))
 need(set(rows.values())==geo,'all primitive rows agree with geometry')
 need(len(rows)==3*r*(r-1)//2==len(geo),'row counts/duplicates')
 return H,pos,rows
certificates={6:([
 (3,1,4,1,1),(1,1,5,0,1),(1,2,1,3,1),(2,2,1,3,2),(2,2,2,2,1),(3,2,3,1,1),(1,4,2,0,1),(1,5,1,0,1)],[(3,2,1,3,2),(1,2,2,2,2),(1,2,3,1,1),(2,2,3,1,2),(2,2,4,0,1),(3,3,2,1,3),(3,4,1,1,3),(3,4,2,0,3),(3,5,1,0,3)]),7:([
 (2,1,5,1,1),(3,1,5,1,1),(1,3,4,0,1),(1,4,3,0,1),(1,5,2,0,1),(1,6,1,0,1)],[(2,1,1,5,1),(2,1,2,4,1),(2,1,3,3,1),(1,2,2,3,1),(3,2,2,3,1),(1,2,3,2,2),(3,3,3,1,2),(2,4,1,2,1),(3,4,2,1,2),(3,4,3,0,2),(3,5,1,1,1),(3,5,2,0,2),(3,6,1,0,1)])}
witnesses={6:[(1,1,4),(1,3,2),(2,1,3),(2,3,1)],7:[(1,4,2),(1,5,1),(2,1,4),(2,2,3)]}
def main():
 results=[]
 for r in [6,7]:
  H,pos,rows=rows_for(r);interior=[x for x in H if min(x)>0];target=witnesses[r][0];h=[Q(1,2) if x in witnesses[r] else Q(0) for x in H]
  rhs={key:-(-sum(v*x for v,x in zip(row,h)).numerator//sum(v*x for v,x in zip(row,h)).denominator) for key,row in rows.items()}
  slacks={key:Q(rhs[key])-sum(v*x for v,x in zip(row,h)) for key,row in rows.items()}
  need(all(s>=0 for s in slacks.values()),'real nonnegative slack')
  need(all(h[pos[x]]==0 for x in H if min(x)==0),'zero boundary')
  need(sum(h)==2,'four half entries')
  for cert,sign in zip(certificates[r],[-1,1]):
   weighted=[sum(w*rows[(t,i,j,k)][pos[x]] for t,i,j,k,w in cert) for x in interior]
   weighted_rhs=sum(w*rhs[(t,i,j,k)] for t,i,j,k,w in cert)
   need(weighted==[sign*2 if x==target else 0 for x in interior],'exact interior cancellation')
   need(weighted_rhs==sign,'exact RHS forces half')
   need(all(w>0 for t,i,j,k,w in cert),'nonnegative weights')
   t,i,j,k,w=cert[0];changed=weighted[:]
   changed=[a+rows[(t,i,j,k)][pos[x]] for a,x in zip(changed,interior)]
   need(changed!=weighted,'changed certificate weight detected')
   need(weighted_rhs+w!=sign,'changed used bound detected')
  q=[sum(y*y for y in x) for x in H]
  need(all(sum(a*b for a,b in zip(row,q))==2 for row in rows.values()),'positive-bound translation')
  need(Q(1,2)+q[pos[target]]==(Q(37,2) if r==6 else Q(43,2)),'translated forced coordinate')
  degree=sum(h)+sum(slacks.values());need(degree==(Q(25,2) if r==6 else 13),'total coefficient mass')
  results.append({'r':r,'coordinates':len(H),'boundary':len(H)-len(interior),'primitive_rows':len(rows),'forced_coordinate':target,'forced_value':'1/2','integral_point_impossible':True,'total_augmented_coefficient_mass':str(degree),'affine_triangulation_implication':'not certified by this finite checker'})
 print(json.dumps({'status':'PASS','checks':checks,'cases':results,'no_network_or_author_code':True,'scope':'Exact feasibility, primitive geometry, dual identities and scalar invariants only; source scope/priority/unimodularity theorem require separate written review.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
