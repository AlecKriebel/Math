#!/usr/bin/env python3
"""Auditor-authored exact checks; imports none of the frozen author code.
Q# is computed through so(n) structure constants and 2x2 minors.
Finite checks are diagnostics, not a proof of the missing global inequality.
"""
import json
from itertools import combinations, product
from functools import lru_cache
import sympy as s

CHECKS=[]
def check(ok,label):
    if not bool(ok): raise ValueError(label)
    CHECKS.append(label)

def ip(X,Y): return s.trace(X.T*Y)
def edges(n): return list(combinations(range(n),2))

@lru_cache(None)
def brackets(n):
    pp=edges(n); lookup={p:k for k,p in enumerate(pp)}; out=[[] for _ in pp]
    for a,(i,j) in enumerate(pp):
        for b in range(a+1,len(pp)):
            k,l=pp[b]; z={}
            for u,v,c in [(i,l,int(j==k)),(j,l,-int(i==k)),(i,k,-int(j==l)),(j,k,int(i==l))]:
                if c and u!=v:
                    idx=lookup[tuple(sorted((u,v)))]; z[idx]=z.get(idx,0)+c*(1 if u<v else -1)
            for idx,c in z.items():
                if c: out[idx].append((a,b,c))
    return out

def Q(n,M):
    cc=brackets(n); N=len(cc); out=M*M
    for a in range(N):
        for b in range(a,N):
            x=sum(c*d*(M[i,k]*M[j,l]-M[i,l]*M[j,k]) for i,j,c in cc[a] for k,l,d in cc[b])
            out[a,b]+=x
            if a!=b: out[b,a]+=x
    return out

def entry(n,M,i,j,k,l):
    if i==j or k==l: return s.S.Zero
    ix={p:z for z,p in enumerate(edges(n))}
    return (1 if i<j else -1)*(1 if k<l else -1)*M[ix[tuple(sorted((i,j)))],ix[tuple(sorted((k,l)))]]

def ric(n,M):
    return s.Matrix(n,n,lambda i,j:sum(entry(n,M,i,k,j,k) for k in range(n)))

def outer_wedge(A):
    pp=edges(A.rows)
    return s.Matrix([[A[i,k]*A[j,l]-A[i,l]*A[j,k] for k,l in pp] for i,j in pp])

def ric_piece(S):
    n=S.rows; I=s.eye(n)
    return (outer_wedge(I+S)-outer_wedge(I)-outer_wedge(S))/(n-2)

def decompose(n,M):
    r=ric(n,M); a=s.trace(r)/(n*(n-1)); S=r-(n-1)*a*s.eye(n)
    return a,S,M-a*s.eye(M.rows)-ric_piece(S)

def algebraic(n,M):
    return M==M.T and all(entry(n,M,i,j,k,l)+entry(n,M,i,k,l,j)+entry(n,M,i,l,j,k)==0 for i,j,k,l in product(range(n),repeat=4))

def two_block(p,q):
    return s.diag(*[s.Rational(q,p-1) if j<p else s.Rational(p,q-1) if i>=p else -1 for i,j in edges(p+q)])

def embedded_H(n,idx):
    pp=edges(n); ix={p:z for z,p in enumerate(pp)}
    vectors=[]
    for components in [[(0,1,1),(2,3,1)],[(0,2,1),(1,3,-1)],[(0,3,1),(1,2,1)]]:
        v=s.zeros(len(pp),1)
        for a,b,c in components:
            i,j=idx[a],idx[b];v[ix[tuple(sorted((i,j)))]]=c*(1 if i<j else -1)
        vectors.append(v)
    # Vectors have norm sqrt(2), so the spectral weights are halved.
    return sum((c*v*v.T for c,v in zip([2,-1,-1],vectors)),s.zeros(len(pp)))

def main():
    for n in [4,5,6,12]:
        I=s.eye(n*(n-1)//2)
        check(Q(n,I)==(n-1)*I,f'Q(I) normalization n={n}')
    for n in [4,5,6]:
        A=s.Matrix(n,n,lambda i,j:((i+j+2)*(i*j+3))%7-3)
        B=s.diag(*[i-2 for i in range(n)])
        R=outer_wedge(A)+3*outer_wedge(B)+2*s.eye(n*(n-1)//2)
        a,S,W=decompose(n,R); qr=Q(n,R); qw=Q(n,W)
        check(algebraic(n,R),f'non-diagonal algebraic input n={n}')
        check(ric(n,W)==s.zeros(n),f'Weyl projection n={n}')
        check(s.trace(ric(n,qr))==ip(ric(n,R),ric(n,R)),f'scalar Q n={n}')
        check(ric(n,qw)==s.zeros(n),f'Q Weyl closure n={n}')
        check(Q(n,W+s.eye(W.rows))-qw-Q(n,s.eye(W.rows))==s.zeros(W.rows),f'B(I,W)=0 n={n}')
        check(ip(qr,W)==ip(qw,W)+ip(outer_wedge(S),W)/(n-2),f'full tangency n={n}')
        PS=decompose(n,outer_wedge(S))[2];u=ip(S,S);v=s.trace(S**4)
        check(ip(PS,PS)==s.Rational(n*n-3*n+3,2*(n-1)*(n-2))*u*u-s.Rational(n,2*(n-2))*v,f'fourth moment n={n}')
        E=ric_piece(S); ae,se,we=decompose(n,Q(n,E))
        check(ae==u/(n*(n-1)) and we==PS/(n-2),f'apex velocity n={n}')
    H=embedded_H(4,[0,1,2,3])
    check(algebraic(4,H) and ric(4,H)==s.zeros(4),'self-dual H Bianchi and Ricci')
    check(sorted(H.eigenvals().items())==[(-2,2),(0,3),(4,1)],'H spectral projection')
    check(ip(H,H)==24 and Q(4,H)==6*H and ip(Q(4,H),H)==144,'H norm and cubic')
    check(s.Rational(144**2,24**3)==s.Rational(3,2),'H squared ratio')
    lows=[]
    for n in range(4,12):
        p=n//2;q=n-p;S=s.diag(*([q]*p+[-p]*q));PW=decompose(n,outer_wedge(S))[2]
        L=s.cancel(2*n*(n-1)*ip(PW,PW)/(n-2)**2/ip(S,S)**2);U=s.Rational(4*(n-1),3*n)
        check(L>U,f'explicit incompatibility n={n}')
        lows.append({'n':n,'lower':str(L),'upper':str(U),'gap':str(L-U)})
    check(lows[-1]['gap']=='122/24057','dimension 11 gap')
    V=two_block(6,6); QV=Q(12,V);T=ip(V,V)
    check(QV==11*V and T==s.Rational(396,5),'balanced n12 eigenoperator and norm')
    # Independently compute the mixed coefficient of Q, not just its inferred value.
    t=s.symbols('t'); pencils=[]
    for idx,expected in [([0,1,2,3],0),([0,6,7,8],0),([0,1,6,7],s.Rational(44,5)),([0,6,1,7],-s.Rational(22,5))]:
        H=embedded_H(12,idx);QH=Q(12,H);cross=Q(12,V+H)-QV-QH;ell=ip(V,H)
        check(ric(12,H)==s.zeros(12) and QH==6*H and ip(H,H)==24,f'embedded H {idx}')
        check(ell==expected,f'pencil overlap {idx}')
        check(ip(QV,H)+ip(cross,V)==33*ell and ip(cross,H)+ip(QH,V)==18*ell,f'direct cubic coefficients {idx}')
        cubic=ip(QV,V)+t*(ip(QV,H)+ip(cross,V))+t*t*(ip(cross,H)+ip(QH,V))+t**3*ip(QH,H)
        norm=T+2*ell*t+24*t*t
        P=s.Poly(s.expand(s.Rational(55,36)*norm**3-cubic**2),t)
        check(P.nth(0)==P.nth(1)==0,f'pencil double root {idx}')
        quart=s.Poly(s.cancel(P.as_expr()/t**2),t);A=quart.nth(4);B=quart.nth(3)
        rem=s.Poly(s.expand(quart.as_expr()-A*(t*t+B*t/(2*A))**2),t)
        disc=rem.nth(1)**2-4*rem.nth(2)*rem.nth(0)
        check(A>0 and rem.degree()==2 and rem.nth(2)>0 and disc<0,f'all-real pencil certificate {idx}')
        pencils.append({'indices':idx,'inner_product':str(ell),'residual_discriminant':str(disc)})
    check(s.Rational(55,36)-s.Rational(3,2)==s.Rational(1,36),'n12 is not obstructed by H')
    # Second, independent diagonal local check: exact negative definiteness,
    # rather than reproducing the author's characteristic polynomial.
    pp=edges(12);ix={e:i for i,e in enumerate(pp)};w=[V[i,i] for i in range(66)]
    constraint=s.Matrix(13,66,lambda row,col: int(row in pp[col]) if row<12 else w[col])
    tangent=s.Matrix.hstack(*constraint.nullspace())
    check(tangent.cols==53,'full diagonal sphere tangent dimension')
    K=s.diag(*[2*x-11 for x in w])
    # In f=sum w_e^3+3 sum_triangles w_ab*w_ac*w_bc, an adjacent-edge
    # Hessian entry divided by 3 is the third edge value.
    for i,j,k in combinations(range(12),3):
        es=[ix[(i,j)],ix[(i,k)],ix[(j,k)]]
        for a,b,c in [(es[0],es[1],es[2]),(es[0],es[2],es[1]),(es[1],es[2],es[0])]:
            K[a,b]=K[b,a]=w[c]
    G=tangent.T*K*tangent
    lower,diagonal=G.LDLdecomposition(hermitian=False)
    check(lower*diagonal*lower.T==G,'exact diagonal tangent LDL factorization')
    check(all(diagonal[i,i]<0 for i in range(53)),'strict negative definiteness on entire diagonal tangent')
    # Symbolic checks of the proposed endpoints and the equivalence of the apex condition.
    n,mu,c=s.symbols('n mu c',positive=True);N=n*(n-1)/2
    check(s.simplify((n*(n-1)*mu/(n-2))**2/N-4*N*mu**2/(n-2)**2)==0,'apex lower endpoint equals smooth-boundary lower endpoint')
    check(s.simplify(n/(n-2)-n**3*(n-3)/((n-2)**3*(n+1))-4*n/((n-2)**3*(n+1)))==0,'odd Ricci lower margin')
    check(s.simplify((n+1)*(n-2)/(n*(n-3))-n/(n-2)-4/(n*(n-3)*(n-2)))==0,'odd model upper margin')
    # Negative mathematical controls use independently computed quantities.
    rejected=[]
    for label,wrong in [('factor-two Q',Q(4,s.eye(6))==6*s.eye(6)),('norm 23',ip(embedded_H(4,[0,1,2,3]),embedded_H(4,[0,1,2,3]))==23),('H counterexample at n12',s.Rational(3,2)>s.Rational(55,36)),('dimension eleven feasible',s.Rational(2662,2187)<=s.Rational(40,33))]:
        if bool(wrong): raise ValueError('Accepted negative control '+label)
        rejected.append(label)
    print(json.dumps({'status':'PASS','implementation':'Independent so(n) structure constants and exterior-square minors; no author-code imports','checks':len(CHECKS),'check_labels':CHECKS,'negative_controls_rejected':rejected,'low_dimension_obstructions':lows,'pencils':pencils,'scope':'Finite exact diagnostics support the audited partial results; no global Weyl inequality or threshold proof.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
