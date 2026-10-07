#!/usr/bin/env python3
from itertools import permutations,product,combinations
import json,random
P=list(permutations(range(3)));pi={p:i for i,p in enumerate(P)}
M=[[pi[tuple(a[b[i]] for i in range(3))] for b in P] for a in P]
I=[next(j for j in range(6) if M[i][j]==0 and M[j][i]==0) for i in range(6)]
def gm(a,b):return (M[a[0]][b[0]],M[a[1]][b[1]])
def gi(a):return (I[a[0]],I[a[1]])
def conj(a,b):return gm(gm(a,b),gi(a))
G=list(product(range(6),repeat=2));one=(0,0);checks=configs=covariances=0

def run(H,HI,alpha,u,full):
 global checks,configs,covariances
 n=len(H);ai=[alpha.index(i) for i in range(n)];e=0
 V=[((y+1)%6,(2*y+3)%6) for y in range(n)]
 def F(f):
  out=[]
  for y in range(n):
   z=(f[ai[y]][1],f[ai[H[y][HI[u]]]][0])
   out.append(conj(V[y],z))
  return tuple(out)
 def theta_inv(z):return (M[M[I[V[u][1]]][z[1]]][V[u][1]],M[M[I[V[e][0]]][z[0]]][V[e][0]])
 def b(h,y):return gm(V[y],gi(V[H[HI[alpha[h]]][y]]))
 def invF(w):
  out=[]
  for h in range(n):
   z=one
   for s in [e,u]:
    y=H[alpha[h]][s];v=(w[y][0],0) if s==e else (0,w[y][1])
    z=gm(z,conj(gi(b(h,y)),v))
   out.append(theta_inv(z))
  return tuple(out)
 if full:iterator=product(G,repeat=n)
 else:
  def it():
   yield (one,)*n
   for size in [1,2]:
    for ss in combinations(range(n),size):
     for vals in product([g for g in G if g!=one],repeat=size):
      f=[one]*n
      for s,v in zip(ss,vals):f[s]=v
      yield tuple(f)
  iterator=it()
 seen=set()
 for f in iterator:
  w=F(f);assert invF(w)==f;checks+=1
  sf={i for i,v in enumerate(f) if v!=one};sw={i for i,v in enumerate(w) if v!=one}
  assert sw<={H[alpha[h]][s] for h in sf for s in [e,u]};checks+=1
  assert sf<={ai[H[y][HI[s]]] for y in sw for s in [e,u]};checks+=1
  if full:assert w not in seen;seen.add(w);checks+=1
  if configs%127==0:
   for h in range(n):
    hf=tuple(f[H[HI[h]][y]] for y in range(n));lhs=F(hf)
    rhs=tuple(conj(b(h,y),w[H[HI[alpha[h]]][y]]) for y in range(n))
    assert lhs==rhs;checks+=1;covariances+=1
  configs+=1
 if full:assert len(seen)==len(G)**n;checks+=1
 # Nonabelian cocycle identity on every pair and output coordinate.
 for h,k,y in product(range(n),repeat=3):
  assert b(H[h][k],y)==gm(b(h,y),b(k,H[HI[alpha[h]]][y]));checks+=1
# C3, nonidentity quotient automorphism, all 36^3 base configurations.
H=[[(a+b)%3 for b in range(3)] for a in range(3)]
run(H,[0,2,1],[0,2,1],1,True)
# Nonabelian S3 acting group, inner quotient automorphism, support <=2.
a=pi[(1,2,0)];alpha=[M[M[a][h]][I[a]] for h in range(6)]
run(M,I,alpha,1,False)
print(json.dumps({'status':'PASS','exact_assertions':checks,'base_configurations':configs,'twisted_covariance_controls':covariances,'scope':'Finite exact orientation, cocycle, factor and inverse controls; the general theorem is proved in TURN_1.md.'},indent=2))
