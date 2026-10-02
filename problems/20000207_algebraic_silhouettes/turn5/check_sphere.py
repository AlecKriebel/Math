from fractions import Fraction as Q
import json
n=0
def ck(x):
 global n;n+=1;assert x

def tr(A):return list(map(list,zip(*A)))
def mul(A,B):return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
def sub(a,b):return [x-y for x,y in zip(a,b)]
def mv(A,v):return [sum(a*b for a,b in zip(r,v)) for r in A]
def det(A):return sum(A[0][j]*(A[1][(j+1)%3]*A[2][(j+2)%3]-A[1][(j+2)%3]*A[2][(j+1)%3]) for j in range(3))
I=[[1,0,0],[0,1,0],[0,0,1]];R=Q(5,3);f=Q(4,3);K=[[f,0,0],[0,f,0],[0,0,1]];Ki=[[1/f,0,0],[0,1/f,0],[0,0,1]];A1=[[1,0,0],[0,-1,0],[0,0,-1]];t0=[0,0,R];ratios=[]
for a in [Q(i,7) for i in range(1,101)]:
 c=(1-a*a)/(1+a*a);s=2*a/(1+a*a);A2=[[c,0,-s],[0,-1,0],[-s,0,-c]]
 ck(mul(A2,tr(A2))==I);ck(det(A2)==1);ck(mv(A2,[R*s,0,R*c])==[0,0,-R])
 A=mul(A2,tr(A1));t=sub(t0,mv(A,t0));ck(t==[-R*s,0,R*(1-c)])
 tx=[[0,-t[2],t[1]],[t[2],0,-t[0]],[-t[1],t[0],0]];F=mul(mul(Ki,mul(tx,A)),Ki)
 target=[[0,R*(c-1)/f**2,0],[R*(c-1)/f**2,0,R*s/f],[0,-R*s/f,0]]
 ck(F==target);ck(det(F)==0);ck(F[0][1]*F[1][0]!=0);ck(F[1][2]/F[0][1]==-f/a);ratios.append(F[1][2]/F[0][1])
 for X in [[1,0,0],[0,1,0],[0,0,1],[Q(3,5),Q(4,5),0],[Q(2,3),Q(2,3),Q(1,3)]]:
  q1=[x+y for x,y in zip(mv(A1,X),t0)];q2=[x+y for x,y in zip(mv(A2,X),t0)]
  ck(q1[2]>0 and q2[2]>0);x1=mv(K,q1);x2=mv(K,q2);ck(sum(x*y for x,y in zip(x2,mv(F,x1)))==0)
ck(len(set(ratios))==100)
for u in range(-10,11):
 for v in range(-10,11):
  u0=Q(u,7);v0=Q(v,7);ck(R**2-(R**2-1)*(1+(u0*u0+v0*v0)/f**2)==1-u0*u0-v0*v0)
print(json.dumps({'assertions':n,'distinct_rational_matrices':100,'scope':'Exact finite controls; continuum and visibility follow from the analytic proof.'},indent=2))
