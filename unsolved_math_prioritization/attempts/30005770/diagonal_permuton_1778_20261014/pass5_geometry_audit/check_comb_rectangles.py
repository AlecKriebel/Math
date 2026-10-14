#!/usr/bin/env python3
"""Independent canonical reconstruction and all increasing-rectangle checks."""
from pathlib import Path
import json,math
P=Path(__file__).resolve().parent

def S(p):
 n=len(p);inv=[0]*n
 for i,v in enumerate(p,1):inv[v-1]=i
 return tuple(n+1-v for v in inv[::-1])
def std(p):
 r={v:i+1 for i,v in enumerate(sorted(p))};return tuple(r[v] for v in p)
def combstate(k,L):
 out=[];v=k*(L+1)
 for i in range(1,k+1):
  out.append(i);out.extend(range(v,v-L,-1));v-=L
 return tuple(out)
def reconstruct(states):
 raw=[A if i%2==0 else S(A) for i,A in enumerate(states)];r=len(raw)
 # Every normalized edge word is U, all L, then the remaining U.
 pos=[]
 for i in range(0,r,2):
  up=[(i,j) for j in range(len(raw[i]))]
  if i+1==r:pos+=up
  else:pos+=up[:1]+[(i+1,j) for j in range(len(raw[i+1]))]+up[1:]
 descending=[(0,j) for j in sorted(range(len(raw[0])),key=lambda j:raw[0][j],reverse=True)]
 for i in range(1,r,2):
  left=[(i,j) for j in sorted(range(len(raw[i])),key=lambda j:raw[i][j],reverse=True)]
  if i+1==r:descending+=left
  else:
   right=[(i+1,j) for j in sorted(range(len(raw[i+1])),key=lambda j:raw[i+1][j],reverse=True)]
   descending+=left[:1]+right+left[1:]
 values={point:len(pos)-j for j,point in enumerate(descending)}
 return tuple(values[x] for x in pos),[x[0] for x in pos]
def peel(p):
 rem=list(enumerate(p));cells=[]
 while rem:
  vals=[v for _,v in rem];t=len(vals)
  if len(cells)%2==0:
   suf=[0]*(t+1)
   for j in range(t-1,-1,-1):suf[j]=max(suf[j+1],vals[j])
   cut=max((vals[j] for j in range(t) if any(vals[j]<vals[i]<suf[j+1] for i in range(j))),default=0)
   cell=[x for x in rem if x[1]>cut]
  else:
   pref=[10**9]*(t+1)
   for j in range(t):pref[j+1]=min(pref[j],vals[j])
   bad=next((j for j in range(t) if any(pref[i]<vals[j]<vals[i] for i in range(j))),t)
   cell=rem[:bad]
  if not cell:raise RuntimeError('empty greedy cell')
  chosen=set(cell);rem=[x for x in rem if x not in chosen];cells.append(cell)
 return cells
rows=[]
for L in (2,5):
 for s in range(1,6):
  ks=[2**j for j in range(1,s+1)]+[2**j for j in range(s-1,0,-1)]
  states=[combstate(k,L) for k in ks];p,colors=reconstruct(states);n=len(p)
  cells=peel(p)
  got=[std([v for _,v in cell]) for cell in cells]
  got=[A if i%2==0 else S(A) for i,A in enumerate(got)]
  if got!=states:raise RuntimeError(('canonical reconstruction',L,s))
  pairs=occupied=0
  for i in range(n):
   for j in range(i+1,n):
    if p[i]>=p[j]:continue
    pairs+=1;inside=[p[t] for t in range(i+1,j) if p[i]<p[t]<p[j]];m=len(inside)
    if any(x>=y for x,y in zip(inside,inside[1:])):raise RuntimeError('1324 occurrence')
    hp=j-i-1-m;vq=p[j]-p[i]-1-m
    if abs(colors[i]-colors[j])>1:raise RuntimeError('nonadjacent increasing pair')
    if colors[i]==colors[j]:
     if (hp if colors[i]%2==0 else vq)<L*m:raise RuntimeError(('same cell teeth',L,s,i,j,m,hp,vq))
    elif hp+vq<L*max(0,m-2):raise RuntimeError(('adjacent cell teeth',L,s,i,j,m,hp,vq))
    if L==5 and m>=20:
     occupied+=1
     def e(a,b):return (a+b)*math.log(a+b)-(a*math.log(a) if a else 0)-(b*math.log(b) if b else 0)
     if e(m,hp)+e(m,vq)<=m*math.log(13.5):raise RuntimeError('allocation entropy')
  rows.append({'L':L,'s':s,'n':n,'cells':len(states),'increasing_pairs_checked':pairs,'occupied_pairs_m_at_least_20':occupied})
r={'scope':'Finite diagnostics only; independent reconstruction and exhaustive increasing-pair checks','all_checks_passed':True,'checks':rows}
(P/'COMB_RECTANGLE_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
