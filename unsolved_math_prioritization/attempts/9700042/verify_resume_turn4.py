#!/usr/bin/env python3
"""Deterministic checks for the C4 proof candidate. No asymptotic proof by testing."""
from heapq import heappop, heappush
from itertools import product, combinations
from math import comb, e, sqrt
from pathlib import Path
from random import Random
import json


def fwd_edges(W,H):
 for x in range(W+1):
  for y in range(H+1):
   if x<W:yield ((x,y),(x+1,y))
   if y<H:yield ((x,y),(x,y+1))

def solve(W,H,closed,with_path=False):
 start=(0,0);end=(W,H);dist={start:0};parent={};heap=[(0,start)];done=set()
 while heap:
  d,u=heappop(heap)
  if u in done:continue
  done.add(u)
  if u==end:break
  x,y=u
  for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
   v=(x+dx,y+dy)
   if not(0<=v[0]<=W and 0<=v[1]<=H):continue
   weight=int((u,v) not in closed) if dx+dy==1 else 0
   nd=d+weight
   if v not in done and nd<dist.get(v,10**9):
    dist[v]=nd;parent[v]=u;heappush(heap,(nd,v))
 D=W+H-dist[end]
 if not with_path:return D
 path=[end]
 while path[-1]!=start:path.append(parent[path[-1]])
 path.reverse();assert len(path)==len(set(path))
 return D,path

def mark_reward(path,closed):
 marks=[];back=0
 for u,v in zip(path,path[1:]):
  if sum(v)>sum(u):
   if (u,v) in closed:marks.append((u,v))
  else:back+=1
 return len(marks)-back,back,marks

def slice_check(N,closed,m,h):
 D,path=solve(N,N,closed,True);L=m*h
 ends=[0];level=L
 for t,v in enumerate(path[1:],1):
  if sum(v)==level:
   ends.append(t);level+=L
 if ends[-1]!=len(path)-1:ends.append(len(path)-1)
 all_marks=set();budget=0;ssum=0;bad_perimeters=0;positive_reward=0;checked=0
 for j,(aa,bb) in enumerate(zip(ends,ends[1:])):
  seg=path[aa:bb+1];u,v=seg[0],seg[-1]
  reward,b,marks=mark_reward(seg,closed);budget+=b;positive_reward+=max(reward,0)
  assert not all_marks.intersection(marks);all_marks.update(marks)
  i=u[0]//h;ip=v[0]//h;s=b//h;ssum+=s;a=(s+1)*h
  lo=(i*h-a,sum(u)-(i+1)*h-a)
  hi=((ip+1)*h+a,sum(v)-ip*h+a)
  W,H=hi[0]-lo[0],hi[1]-lo[1]
  assert W>=h and H>=h
  assert W+H==sum(v)-sum(u)+2*h+4*a
  assert -s-2<=ip-i<=m+s+2
  assert all(lo[0]<=x<=hi[0] and lo[1]<=y<=hi[1] for x,y in seg)
  local={((u[0]-lo[0],u[1]-lo[1]),(v[0]-lo[0],v[1]-lo[1])) for u,v in marks}
  # Only original segment marks are kept; every padding/other edge is open.
  assert solve(W,H,local)>=max(reward,0)
  if s or j==len(ends)-2:bad_perimeters+=W+H
  else:assert W+H==L+6*h
  checked+=1
 assert ssum<=budget//h
 assert bad_perimeters<=(m+10)*budget+L+6*h
 assert positive_reward>=D
 return checked,budget

def lis_marks(closed):
 marks=list(closed);marks.sort(key=lambda z:z[0]);best=[]
 for i,(u,v) in enumerate(marks):
  best.append(1+max([best[j] for j,(a,b) in enumerate(marks[:i]) if a[0]<u[0] and a[1]<u[1]] or [0]))
 return max(best or [0])

def compositions(J,K,prefix=()):
 if J==0:
  yield prefix;return
 for s in range(K+1):yield from compositions(J-1,K-s,prefix+(s,))

def main():
 rng=Random(970004205);slices=cases=positive_backtrack_cases=0
 for N in [2,4,7,12,20]:
  es=list(fwd_edges(N,N))
  for trial in range(36):
   q=[.02,.1,.3,.6][trial%4];closed={ed for ed in es if rng.random()<q}
   for m,h in [(2,1),(3,2),(4,2)]:
    cc,b=slice_check(N,closed,m,h);slices+=cc;cases+=1;positive_backtrack_cases+=int(b>0)
 # Explicit C3 long-strip construction.
 L0=4;R=11;mm=L0+1;N=(2*mm+3)*R
 starts={(L0,(j+1)*R) for j in range(mm)}|{(0,(mm+j+2)*R) for j in range(mm)}
 closed={(u,(u[0],u[1]+1)) for u in starts}
 cc,b=slice_check(N,closed,3,2);cases+=1;slices+=cc;assert b>0
 positive_backtrack_cases+=1
 sparse=0
 es=list(fwd_edges(5,5))
 for pair in combinations(es,2):
  if all(abs(pair[0][0][i]-pair[1][0][i])>2 for i in (0,1)):
   assert solve(5,5,set(pair))==lis_marks(set(pair));sparse+=1
 for k in [3,4,5]:
  N=12*k
  for _ in range(12):
   xs=[1+(k+2)*i for i in range(k)];ys=xs.copy();rng.shuffle(ys)
   closed=set()
   for x,y in zip(xs,ys):
    delta=rng.choice([(1,0),(0,1)]);closed.add(((x,y),(x+delta[0],y+delta[1])))
   assert solve(N,N,closed)==lis_marks(closed);sparse+=1
 skeleton_checks=0
 for m in [1,2,4]:
  for J in range(1,5):
   for K in range(0,6):
    actual=sum(__import__('functools').reduce(lambda a,s:a*(m+2*s+5),ss,1) for ss in compositions(J,K))
    bound=(m+5)**J*e**K*comb(J+K,K)
    assert actual<=bound+1e-8;skeleton_checks+=1
 c_small=2*e**2*(1.5)**6/(32**2)
 c_large=32*e**2*1e-6*6**2
 assert c_small<.25 and c_large<.25
 out={'schema':'oriented-flow-c4-deterministic-checks-v1','seed':970004205,
      'skeleton_path_cases':cases,'segments_and_disjoint_witnesses_checked':slices,
      'positive_backtracking_path_cases':positive_backtrack_cases,
      'sparse_stability_cases':sparse,'small_skeleton_count_cases':skeleton_checks,
      'tail_constants':{'small_k_base_upper':c_small,'large_k_base_upper_at_q_1e_6':c_large,'required_upper':.25},
      'all_checks_passed':True,
      'limits':'These checks do not establish BK, the Poisson theorem, or the infinite-volume asymptotic. The proof candidate requires independent mathematical review.'}
 Path(__file__).with_name('TURN_C4_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
