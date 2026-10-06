"""Independent publication replay over exact fractions; no external dependencies."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
    raise SystemExit('Python -I -S -B required')
from fractions import Fraction as F
import json, random

def need(ok,why):
    if not ok: raise ValueError(why)
def zeros(n,m):return [[F(0) for _ in range(m)] for _ in range(n)]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def tr(A):return [list(r) for r in zip(*A)]
def add(A,B,sign=1):return [[a+sign*b for a,b in zip(x,y)] for x,y in zip(A,B)]
def mul(A,B):
    BT=tr(B)
    return [[sum((a*b for a,b in zip(x,y)),F(0)) for y in BT] for x in A]
def hs(*As):return [sum((list(A[i]) for A in As),[]) for i in range(len(As[0]))]
def rr(A):
    A=[list(map(F,row)) for row in A];n=len(A);m=len(A[0]) if n else 0;r=0;p=[]
    for c in range(m):
        k=next((k for k in range(r,n) if A[k][c]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r];v=A[r][c];A[r]=[x/v for x in A[r]]
        for k in range(n):
            if k!=r and A[k][c]:
                v=A[k][c];A[k]=[x-v*y for x,y in zip(A[k],A[r])]
        p.append(c);r+=1
        if r==n:break
    return A,p
def rank(A):return len(rr(A)[1])
def null(A):
    R,p=rr(A);m=len(A[0]);free=[c for c in range(m) if c not in p];out=zeros(m,len(free))
    for j,c in enumerate(free):
        out[c][j]=F(1)
        for i,v in enumerate(p):out[v][j]=-R[i][c]
    return out
def inv(A):
    n=len(A);R,p=rr(hs(A,eye(n)));need(p[:n]==list(range(n)),'singular matrix');return [r[n:] for r in R]
def block(A,row,col,B):
    for i,r in enumerate(B):
        for j,v in enumerate(r):A[row+i][col+j]=v
def scaled(A,c):return [[c*x for x in r] for r in A]
def diag(*As):
    n=sum(len(A) for A in As);out=zeros(n,n);i=0
    for A in As:block(out,i,i,A);i+=len(A)
    return out
def jordan(n,lam=1):return [[F(lam if i==j else (1 if j==i+1 else 0)) for j in range(n)] for i in range(n)]
def cycle(T,n):
    r=len(T);I=eye(r);A=zeros(n*r,n*r);D=zeros(n*r,n*r)
    for i in range(n-1):block(A,i*r,i*r,I);block(A,i*r,(i+1)*r,scaled(I,-1))
    block(A,(n-1)*r,(n-1)*r,I);block(A,(n-1)*r,0,scaled(T,-1))
    block(D,0,0,I);block(D,0,(n-1)*r,scaled(inv(T),-1))
    for i in range(1,n):block(D,i*r,i*r,I);block(D,i*r,(i-1)*r,scaled(I,-1))
    M=add(T,I,-1);B=null(M);J=B*n
    need(mul(D,J)==zeros(n*r,len(B[0])),'cycle kernel inclusion')
    need(n*r-rank(D)==len(B[0]),'cycle kernel equality')
    Q=tr(null(tr(M)))
    if Q:
        L=hs(*([Q]*n));need(mul(L,A)==zeros(len(L),n*r),'quotient kernel inclusion'); lr=rank(L)
    else:lr=0
    ra=rank(A);need(ra==n*r-lr,'quotient kernel equality')
    KD=null(D);intersect=ra+rank(KD)-rank(hs(A,KD));expect=rank(M)-rank(mul(M,M));rda=rank(mul(D,A))
    need(ra-rda==intersect==expect,'defect identity')
    signs=[F(-1 if i%3==0 else 1) for i in range(n*r)];SA=[[signs[i]*x for x in row] for i,row in enumerate(A)];DS=[[x*signs[j] for j,x in enumerate(row)] for row in D]
    need(mul(DS,SA)==mul(D,A),'orientation change')
    Mi=add(inv(T),I,-1);need(rank(Mi)-rank(mul(Mi,Mi))==expect,'holonomy inversion')
    return {'n':n,'coefficient_rank':r,'rank_A':ra,'rank_DA':rda,'defect':expect,'rank_wrong_transpose_A':rank(mul(tr(A),A))}
def main():
    Ts=[('I1',eye(1)),('I3',eye(3)),('scalar2',[[F(2)]]),('J2_1',jordan(2)),('J3_1',jordan(3)),('J4_1',jordan(4)),('J2_1_plus_J2_1',diag(jordan(2),jordan(2))),('diag1_2',diag([[F(1)]],[[F(2)]])),('J2_2',jordan(2,2)),('mixed',diag(jordan(2),jordan(2,2)))]
    P=[[F(x) for x in r] for r in [[1,2,0],[0,1,1],[1,0,1]]]
    Ts += [('rational_conjugate_J3',mul(mul(P,jordan(3)),inv(P))),('rational_no1',[[F(1,2),F(2,3)],[F(0),F(-3,5)]])]
    rows=[dict(case=name,**cycle(T,n)) for name,T in Ts for n in (3,4,5,7)]
    random.seed(30002618);abstract=[]
    for k in range(30):
        m=random.randrange(1,8);a=random.randrange(1,7);d=random.randrange(1,7)
        A=[[F(random.randrange(-2,3)) for j in range(a)] for i in range(m)];D=[[F(random.randrange(-2,3)) for j in range(m)] for i in range(d)]
        if k%4==0:
            for r in A:r[0]=F(0)
        if k%5==0:D=zeros(d,m)
        KD=null(D);ra=rank(A);inter=ra+rank(KD)-rank(hs(A,KD));quotient=tr(null(tr(A)));dim=len(KD[0])-(rank(mul(quotient,KD)) if quotient else 0);rda=rank(mul(D,A))
        need(inter==dim==ra-rda,'abstract formula')
        abstract.append({'case':k,'C1_dimension':m,'rank_A':ra,'rank_DA':rda,'defect':inter})
    return {'problem_id':30002618,'arithmetic':'Python standard-library fractions, exact rational arithmetic','cycle_case_count':len(rows),'abstract_case_count':len(abstract),'cycle_cases':rows,'abstract_cases':abstract,'all_checks_passed':True,'scope':'Publication auxiliary diagnostics; not a formal proof or an isocrystal realization certificate.'}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
