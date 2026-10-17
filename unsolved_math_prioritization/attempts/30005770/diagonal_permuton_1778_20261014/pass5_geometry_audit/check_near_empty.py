#!/usr/bin/env python3
"""Independent full canonical reconstruction for the sparse supplement."""
from pathlib import Path
import json,bisect
P=Path(__file__).resolve().parent
ns={'__file__':str(P/'check_comb_rectangles.py')};exec((P/'check_comb_rectangles.py').read_text().split('rows=[]')[0],ns)
S,std,peel=ns['S'],ns['std'],ns['peel']
def skew(a,b):return tuple(x+len(b) for x in a)+tuple(b)
def D(a):return (a-1,a)+tuple(range(a-2,0,-1))
def merge(a,b,w):
 ia=ib=0;o=[]
 for c in w:
  if c=='U':o.append(a[ia]);ia+=1
  else:o.append(b[ib]);ib+=1
 if ia!=len(a) or ib!=len(b):raise RuntimeError('bad word size')
 return o
def build(states,words):
 raw=[a if i%2==0 else S(a) for i,a in enumerate(states)];r=len(raw)
 points=[[(i,j) for j in range(len(a))] for i,a in enumerate(raw)]
 pos=[]
 for i in range(0,r,2):pos+=points[i] if i+1==r else merge(points[i],points[i+1],words[i])
 byval=[sorted(points[i],key=lambda x:raw[i][x[1]],reverse=True) for i in range(r)]
 desc=list(byval[0])
 for i in range(1,r,2):desc+=byval[i] if i+1==r else merge(byval[i],byval[i+1],words[i])
 values={p:len(pos)-j for j,p in enumerate(desc)}
 return tuple(values[p] for p in pos)
rows=[]
for s in (1,2,3):
 k=2**s;Q=()
 for _ in range(k):Q=skew(Q,tuple(range(1,k+1)))
 A=(1,)+tuple(x+1 for x in Q)
 sizes=[2**j for j in range(1,2*s+1)]
 states=[D(a) for a in sizes]+[A]+[D(a) for a in sizes[::-1]]
 words=[]
 for i,(a,b) in enumerate(zip(states,states[1:])):
  if i==2*s-1:words.append('U'+'L'*len(b)+'U'*(len(a)-1))
  elif i==2*s:words.append('U'+'L'*len(b)+'U'*(len(a)-1))
  else:words.append('ULL'+'U'*(len(a)-1)+'L'*(len(b)-2))
 p=build(states,words);n=len(p)
 cells=peel(p);got=[std([v for _,v in cell]) for cell in cells];got=[a if i%2==0 else S(a) for i,a in enumerate(got)]
 if got!=states:raise RuntimeError(('canonical',s))
 inc=empty=maxm=0
 for i in range(n):
  for j in range(i+1,n):
   if p[i]>=p[j]:continue
   inc+=1;inside=[v for v in p[i+1:j] if p[i]<v<p[j]];m=len(inside)
   if any(x>=y for x,y in zip(inside,inside[1:])):raise RuntimeError('1324')
   empty+=(m==0);maxm=max(maxm,m)
 tails=[]
 for v in p:
  j=bisect.bisect_left(tails,v)
  if j==len(tails):tails.append(v)
  else:tails[j]=v
 expected_inc=2*k**4+(k**3+13*k*k)//2-4*s-9;expected_empty=k**3+5*k*k-k-5
 if (n,inc,empty)!=(5*k*k-3,expected_inc,expected_empty):raise RuntimeError(('totals',s,n,inc,empty))
 if len(tails)>k+3 or maxm>k+1:raise RuntimeError(('chains',s))
 rows.append({'s':s,'k':k,'n':n,'cells':len(states),'inc':inc,'empty':empty,'LIS':len(tails),'max_interior':maxm})
r={'all_checks_passed':True,'scope':'Finite diagnostics; all-size proof independently reviewed','checks':rows}
(P/'NEAR_EMPTY_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
