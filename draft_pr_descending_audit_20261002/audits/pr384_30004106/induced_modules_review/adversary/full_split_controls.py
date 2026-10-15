#!/usr/bin/env python3
"""Adversarial exact control of full/stable units for actual cyclic cores.
Finite controls only; imports no candidate or parent-control implementation.
"""
from fractions import Fraction as F
import json

checks=0

def check(x):
    global checks
    assert x
    checks += 1

def matmul(A,B,p):
    return [[sum(A[i][j]*B[j][k] for j in range(len(B)))%p for k in range(len(B[0]))] for i in range(len(A))]

def identity(n):
    return [[int(i==j) for j in range(n)] for i in range(n)]

def rank(A,p):
    A=[row[:] for row in A]
    pivot_row=0
    for j in range(len(A[0])):
        k=next((k for k in range(pivot_row,len(A)) if A[k][j]),None)
        if k is None: continue
        A[pivot_row],A[k]=A[k],A[pivot_row]
        inv=pow(A[pivot_row][j],-1,p)
        A[pivot_row]=[(x*inv)%p for x in A[pivot_row]]
        for i in range(len(A)):
            if i!=pivot_row:
                c=A[i][j]
                A[i]=[(x-c*y)%p for x,y in zip(A[i],A[pivot_row])]
        pivot_row+=1
        if pivot_row==len(A): break
    return pivot_row

def add(x,y): return tuple(a+b for a,b in zip(x,y))
def scale(x,a): return tuple(a*b for b in x)

cases=[]
for p in [3,5,7]:
    # Ω_C(k) is a (p-1)-dimensional Jordan block. Determine its tensor
    # decomposition independently by every nilpotent-power rank.
    m=p-1
    U=identity(m)
    for i in range(m-1): U[i][i+1]=1
    action=[[U[i//m][j//m]*U[i%m][j%m]%p for j in range(m*m)] for i in range(m*m)]
    I=identity(m*m)
    N=[[(a-b)%p for a,b in zip(ar,br)] for ar,br in zip(action,I)]
    power=I
    for j in range(1,p+1):
        power=matmul(power,N,p)
        check(rank(power,p)==(p-2)*max(p-j,0))
    # Thus U⊗U = k ⊕ (p-2)kC. Use the full actual Green multiplication
    # on basis k,U,P to check J and both factor identities, with P=kC.
    one=(F(1),F(0),F(0));u=(F(0),F(1),F(0));P=(F(0),F(0),F(1))
    def mul(x,y):
        a,b,c=x;d,f,g=y
        return (a*d+b*f,a*f+b*d,
                a*g+c*d+(p-2)*b*f+(p-1)*(b*g+c*f)+p*c*g)
    e=scale(P,F(1,p));jk=add(one,scale(e,-1));ju=add(u,scale(e,-(p-1)))
    check(mul(e,e)==e)
    check(mul(jk,jk)==jk)
    check(mul(jk,ju)==ju)
    check(mul(ju,ju)==jk)
    check(mul(e,jk)==(0,0,0))
    check(mul(e,ju)==(0,0,0))
    check(add(e,jk)==one)
    for a,b,d,f in [(F(2,3),F(-5,4),F(-3,7),F(8,9)),(F(1),F(-1),F(1),F(1))]:
        X=add(scale(jk,a),scale(ju,b));Y=add(scale(jk,d),scale(ju,f))
        check(mul(X,Y)==add(scale(jk,a*d+b*f),scale(ju,a*f+b*d)))
        norm=abs(a)+(p-1)*abs(b)
        Jnorm=abs(X[0])+m*abs(X[1])+p*abs(X[2])
        check(Jnorm==norm+abs(a+(p-1)*b))
        check(norm<=Jnorm<=2*norm)
    cases.append({'p':p,'actual_tensor_decomposition':'k plus (p-2) copies of kC',
                  'full_units':'e=P/p; J(k)=1-e; global unit=e+J(k)'})
print(json.dumps({'exact_assertions':checks,'cases':cases,
                  'finite_control_only':True,'universal_symmetry_claimed':False},indent=2))
