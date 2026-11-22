#!/usr/bin/env python3
"""Exact braid KL checks; three computational routes; no external dependencies."""
import json, math
from fractions import Fraction

def require(ok, msg):
    if not ok: raise ValueError(msg)

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c

def stirling(N):
    s=[[0]*(N+1) for _ in range(N+1)];s[0][0]=1
    for n in range(1,N+1):
        for k in range(1,n+1):s[n][k]=s[n-1][k-1]+k*s[n-1][k]
    return s

def z_method(N):
    s=stirling(N);p={1:[1]}
    for n in range(2,N+1):
        r=[0]*n
        for k in range(1,n):
            for j,c in enumerate(p[k]):r[n-k+j]+=s[n][k]*c
        p[n]=[r[n-1-i]-r[i] for i in range((n-2)//2+1)]
        z=r[:]
        for i,c in enumerate(p[n]):z[i]+=c
        require(z==z[::-1],f'Z palindromicity n={n}')
        require(all(c>=0 for c in p[n]),f'nonnegative n={n}')
    return p

def partitions(n,least=1):
    if n==0:yield ()
    for a in range(least,n+1):
        for rest in partitions(n-a,a):yield (a,)+rest

def characteristic_method(N):
    p={1:[1]};chi={1:[1]}
    for n in range(2,N+1):chi[n]=mul(chi[n-1],[-(n-1),1])
    for n in range(2,N+1):
        r=[0]*n
        for parts in partitions(n):
            k=len(parts)
            if k==n:continue
            counts={a:parts.count(a) for a in set(parts)}
            denominator=math.prod(math.factorial(a)**b*math.factorial(b) for a,b in counts.items())
            weight=math.factorial(n)//denominator
            q=[1]
            for a in parts:q=mul(q,chi[a])
            q=mul(q,p[k])
            for i,c in enumerate(q):r[i]+=weight*c
        p[n]=[r[n-1-i] for i in range((n-2)//2+1)]
        lhs=[0]*n
        for i,c in enumerate(p[n]):lhs[n-1-i]=c;r[i]+=c
        require(lhs==r,f'full characteristic identity n={n}')
    return p

def dfact(n):return math.prod(range(n,0,-2))
def leading(n):
    if n<=2:return Fraction(1)
    if n%2==0:
        m=n//2;return Fraction(dfact(2*m-3)*(2*m-1)**(m-2))
    m=(n+1)//2
    return Fraction(dfact(2*m-3)*(2*m-1)**(m-2))-Fraction(m-2)*Fraction(m-1)**(m-5)*Fraction(math.factorial(2*m-1),3*math.factorial(m-2))

def enumeration_method(N):
    # PXY2025 Thm 1.6: associated Stirling numbers count permutations
    # without fixed points, classified by cycle count.
    d=[[0]*(N+1) for _ in range(2*N+1)];d[0][0]=1
    for n in range(2,2*N+1):
        for k in range(1,N+1):d[n][k]=(n-1)*(d[n-2][k-1]+d[n-1][k])
    e={}
    for n in range(1,N):
        e[n]=[0]*(n+1)
        for k in range(1,n+1):
            r=2*k-n
            if not 0<=r<=k:continue
            value=Fraction(0)
            for p in range(1,r+1):
                for i in range(r-p+1):
                    value+=d[2*k-p-1][k-p]*(-1)**(i+p+1)*Fraction(2*k-p-i)**(k-p-1)/math.factorial(i)/math.factorial(r-p-i)
            require(value.denominator==1 and value>=0,f'enumeration integrality {n},{k}')
            e[n][k]=int(value)
    s={0:[1]}
    for n in range(1,N):
        s[n]=[0]*(n+1)
        for j in range(1,n+1):
            q=mul(e[j],s[n-j]);factor=math.comb(n-1,j-1)
            for k,v in enumerate(q):s[n][k]+=factor*v
    return {n:[s[n-1][n-1-i] for i in range(1 if n==1 else (n-2)//2+1)] for n in range(1,N+1)}

def main():
    p=z_method(60);q=characteristic_method(18);e=enumeration_method(18)
    require(all(p[n]==e[n] for n in e),'PXY2025 enumeration mismatch')
    require(all(p[n]==q[n] for n in q),'independent coefficient mismatch')
    require(all(p[n][-1]==leading(n) for n in p),'published leading formula mismatch')
    require(p[4]==[1,1] and p[5]==[1,5] and p[6]==[1,16,15],'small values')
    result={'status':'PASS','arithmetic':'exact Python integers and Fraction',
            'all_coefficient_independent_recurrence_range':[1,18],
            'PXY2025_all_coefficient_enumeration_range':[1,18],
            'Z_palindromicity_and_nonnegative_range':[1,60],
            'published_leading_formulas_range':[1,60],
            'polynomials_ascending_coefficients':{str(n):p[n] for n in range(1,19)},
            'finite_checks_are_not_general_proof':True}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
