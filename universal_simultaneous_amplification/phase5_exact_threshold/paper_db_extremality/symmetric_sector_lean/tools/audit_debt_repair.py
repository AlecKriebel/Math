#!/usr/bin/env python3
"""Independent exact-arithmetic falsification checks; not part of Lean's trust path.
Equations are entered directly from manuscript A.13/A.15/A.16.
"""
from fractions import Fraction as F
from math import comb
import json


def dot(a,b): return sum((x*y for x,y in zip(a,b)), F(0))
def qdiag(N,k): return F(N*(k-2)+k, 2*k*N)
def qlower(N,k): return F(N-k-1,2*N)
def qupper(N,k): return F(k*(k-1),2*(k+1)*N)
def solve_tridiagonal(lower, diag, upper, rhs):
    b, y = diag[:], rhs[:]
    for j in range(1,len(b)):
        r=lower[j]/b[j-1]
        b[j]-=r*upper[j-1]
        y[j]-=r*y[j-1]
    x=[F(0)]*len(b)
    x[-1]=y[-1]/b[-1]
    for j in range(len(b)-2,-1,-1): x[j]=(y[j]-upper[j]*x[j+1])/b[j]
    return x

def audit(N):
    ranks=list(range(2,N)); m=len(ranks)
    g=[F(comb(N-2,j-1),2**(N-1)*(N+1)) for j in range(1,N)]
    negb=[F(comb(N-3,k-2),2**(N-2)*(N+1)) for k in ranks]
    Z=[F(2,3*(k-1)) for k in ranks]
    Y=[F(2*(k+1),3*k*(k-1)) for k in ranks]
    c0=F(2**N-1,N*2**(N-1)); d={0:F(0),N:F(0)}
    for k in range(1,N): d[k]=(F(k-1)*d[k-1]+2*N*(F(1,k)-c0))/(N-k)
    sb=[d[k-1]/(2*k) for k in ranks]
    # The transpose has lower coefficient Q(k-1,k), upper Q(k+1,k).
    lower=[F(0) if k==2 else -qupper(N,k-1) for k in ranks]
    diag=[1-qdiag(N,k) for k in ranks]
    upper=[F(0) if k==N-1 else -qlower(N,k+1) for k in ranks]
    occ=solve_tridiagonal(lower,diag,upper,sb)
    residual=[]
    for j,k in enumerate(ranks):
        r=diag[j]*Z[j]+(lower[j]*Z[j-1] if j else 0)+(upper[j]*Z[j+1] if j+1<m else 0)-F(1,k*(k-1))
        expected=F(1,3*N) if k==2 else F(N-3,3*N*(N-1)*(N-2)) if k==N-1 else F(2*k-3,3*N*k*(k-1))
        assert r==expected and r>0
        residual.append(r)
    assert all(a<=z<=y for a,z,y in zip(occ,Z,Y))
    debt=dot(occ,negb)
    repaired=F(4,3*(N-2))*sum(g[:-1])
    printed=sum((F(4*(j+2),3*(j+1)*(N-2))*g[j-1] for j in range(1,N-1)),F(0))
    assert dot(Z,negb)==repaired
    assert debt<=repaired<=printed
    # Q barrier (A.22) including the two omitted neighbors.
    if N>=25:
        wbar=[F(7*N,25)*w for w in negb]
        for j,k in enumerate(ranks):
            qw=qdiag(N,k)*wbar[j]+(qlower(N,k)*wbar[j-1] if j else 0)+(qupper(N,k)*wbar[j+1] if j+1<m else 0)
            assert wbar[j]-qw>=negb[j]
        for j in range(1,N):
            cw=(F(j,2*(j+1)*N)*wbar[j-1] if j<N-1 else 0)+(F(N-j,2*j*N)*wbar[j-2] if j>1 else 0)
            assert cw<=F(14,25)*g[j-1]
    return {'N':N,'minimum_Z_residual':str(min(residual)),
            'direct_Y_pairing_minus_printed':str(dot(Y,negb)-printed),
            'actual_debt':str(debt) if N<=5 else '(large exact rational checked)',
            'repaired_bound':str(repaired), 'printed_bound':str(printed)}

if __name__=='__main__':
    data=[audit(n) for n in [4,5,6,10,24,25,39,40,100,288]]
    print(json.dumps({'checked_orders':[r['N'] for r in data], 'results':data},indent=2))
