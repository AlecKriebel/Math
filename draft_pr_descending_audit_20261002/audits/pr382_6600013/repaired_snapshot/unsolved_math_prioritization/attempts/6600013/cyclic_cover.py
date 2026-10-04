"""Cyclic covers of a product of two two-loop graphs, exact integer chains."""
from rational_linear import matmul

def complex(q):
 # Four oriented loops at each sheet: Xa,Xb,Ya,Yb; increments1,0,1,0.
 D1=[[0]*(4*q) for _ in range(q)];D2=[[0]*(4*q) for _ in range(4*q)]
 def edge(g,k):return 4*g+k
 for g in range(q):
  for k,s in enumerate([1,0,1,0]):D1[g][edge(g,k)]-=1;D1[(g+s)%q][edge(g,k)]+=1
  for i in range(2):
   for j in range(2):
    col=4*g+2*i+j;sx=int(i==0);sy=int(j==0)
    D2[edge(g,i)][col]+=1;D2[edge((g+sx)%q,2+j)][col]+=1;D2[edge((g+sy)%q,i)][col]-=1;D2[edge(g,2+j)][col]-=1
 return D1,D2

def projection(q,Q):
 assert Q%q==0
 mats=[]
 for cells in [1,4,4]:
  M=[[0]*(cells*Q) for _ in range(cells*q)]
  for g in range(Q):
   for k in range(cells):M[cells*(g%q)+k][cells*g+k]=1
  mats.append(M)
 return mats
