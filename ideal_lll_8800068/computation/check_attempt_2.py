"""Exact companion-integrality tests for specified finite rational rotations."""
import sympy as s
from sympy.matrices.normalforms import hermite_normal_form
from itertools import permutations

def feasible(B):
    n=B.rows; C=B.T; d=abs(int(C.det())); adj=d*C.inv()
    S=s.zeros(n)
    for i in range(n-1): S[i+1,i]=1
    rhs=-(adj*S*C).reshape(n*n,1)
    A=s.zeros(n*n,n)
    for k in range(n):
        E=s.zeros(n); E[k,n-1]=1
        A[:,k]=(adj*E*C).reshape(n*n,1)
    H=hermite_normal_form(A.row_join(d*s.eye(n*n)))
    sol=H.inv()*rhs
    return all(x.q==1 for x in sol)

for n in (2,3,4):
    t=s.Rational(5,7); B=s.zeros(n)
    for i in range(n):
        if i: B[i,:]=B[i-1,:]/2
        B[i,i]=t**i
    D=s.ilcm(*[x.q for x in B]); B*=D
    tests=0; hits=[]
    for perm in permutations(range(n)):
        P=s.zeros(n)
        for i,j in enumerate(perm):P[i,j]=1
        for a,b,c in ((1,0,1),(3,4,5),(5,12,13),(8,15,17)):
            for i in range(n):
                for j in range(i+1,n):
                    O=s.eye(n);O[i,i]=O[j,j]=s.Rational(a,c);O[i,j]=s.Rational(b,c);O[j,i]=-s.Rational(b,c)
                    R=B*P*O
                    R*=s.ilcm(*[x.q for x in R])
                    ok=feasible(R); tests+=1
                    if ok:hits.append((perm,(a,b,c),i,j,R.tolist()))
    print('n',n,'tests',tests,'hits',len(hits),'examples',hits[:3],flush=True)
