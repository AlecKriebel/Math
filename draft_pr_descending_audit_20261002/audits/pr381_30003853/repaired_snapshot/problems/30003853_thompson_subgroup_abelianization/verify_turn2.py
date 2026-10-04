#!/usr/bin/env python3
import itertools,json
n=0
def ck(x):
 global n
 assert x;n+=1
def mul(p,q):return tuple(p[q[i]] for i in range(5))
def inv(p):return tuple(p.index(i) for i in range(5))
def parity(p):return sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2
E=tuple(range(5));A=[p for p in itertools.permutations(range(5)) if parity(p)==0];idx={p:i for i,p in enumerate(A)}
M=[[idx[mul(p,q)] for q in A] for p in A];I=[idx[inv(p)] for p in A];e=idx[E]
def conj(a,b):return M[M[a][b]][I[a]]
def closure(gens):
 s={e};todo=[e]
 while todo:
  x=todo.pop()
  for g in gens:
   y=M[x][g]
   if y not in s:s.add(y);todo.append(y)
 return s
u=idx[(1,2,0,3,4)];v=idx[(1,2,3,4,0)]
ck(len(closure([u,v]))==60)
for a in range(60):
 if a!=e:ck(len(closure({conj(b,a) for b in range(60)}))==60)
comm={M[M[M[a][b]][I[a]]][I[b]] for a in range(60) for b in range(60)}
ck(len(closure(comm))==60)
for twist in [E,(1,0,2,3,4)]:
 alpha=[idx[mul(mul(twist,p),inv(twist))] for p in A]
 ck(len(set(alpha))==60)
 for a,b in itertools.product(range(60),repeat=2):
  normalizes=all(conj(b,alpha[g])==alpha[conj(a,g)] for g in [u,v])
  ck(normalizes==(b==alpha[a]))
for m in range(1,13):
 for a,b,c,d in itertools.product(range(-3,4),repeat=4):
  if (a-c)%m==0:
   z=((a-c)//m,b,c,d)
   ck((m*z[0]+z[2],z[1],z[2],z[3])==(a,b,c,d))
print(json.dumps({'turn':2,'assertions':n,'simple_control_group':'A5','twisted_diagonal_pairs':7200,'scope':'finite controls supplement the general subdirect proof'},sort_keys=True,indent=2))
