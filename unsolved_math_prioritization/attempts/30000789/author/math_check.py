#!/usr/bin/env python3
"""Exact, fail-closed diagnostics for the accompanying scoped mathematical proofs."""
import json
from itertools import combinations, product
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parent
COUNT = 0
NEGATIVE = 0

def require(ok, message):
    global COUNT
    COUNT += 1
    if not bool(ok):
        raise ValueError(message)

def zero(x):
    return s.cancel(s.expand(x)) == 0

def reject(call, message):
    global NEGATIVE
    try:
        call()
    except (ValueError, TypeError):
        NEGATIVE += 1
    else:
        raise ValueError('Negative control accepted: ' + message)

def pairs(n):
    return list(combinations(range(n), 2))

def tensor(n, M):
    pp = pairs(n); ix = {p:i for i,p in enumerate(pp)}
    def t(i,j,k,l):
        if i == j or k == l:
            return s.S.Zero
        a,b = sorted((i,j)); c,d = sorted((k,l))
        sign = (1 if i<j else -1)*(1 if k<l else -1)
        return sign*M[ix[a,b],ix[c,d]]
    return t

def wedge(A):
    n=A.rows; pp=pairs(n)
    return s.Matrix([[A[i,k]*A[j,l]-A[i,l]*A[j,k] for k,l in pp] for i,j in pp])

def ricci(n,M):
    t=tensor(n,M)
    return s.Matrix(n,n,lambda i,j:sum(t(i,k,j,k) for k in range(n)))

def E(n,S):
    pp=pairs(n); delta=lambda a,b:s.Integer(a==b)
    return s.Matrix([[s.Rational(1,n-2)*(S[i,k]*delta(j,l)+S[j,l]*delta(i,k)-S[i,l]*delta(j,k)-S[j,k]*delta(i,l)) for k,l in pp] for i,j in pp])

def decomposition(n,M):
    Ric=ricci(n,M); scal=s.trace(Ric); a=scal/(n*(n-1)); S=Ric-scal/n*s.eye(n)
    return a,S,M-a*s.eye(n*(n-1)//2)-E(n,S)

def inner(A,B):
    return s.trace(A.T*B)

def Q(n,M):
    t=tensor(n,M); pp=pairs(n)
    return s.Matrix([[sum(t(i,j,a,b)*t(k,l,a,b)/2+t(i,a,k,b)*t(j,a,l,b)-t(i,a,l,b)*t(j,a,k,b) for a,b in product(range(n),repeat=2)) for k,l in pp] for i,j in pp])

def algebraic(n,M,weyl=False):
    require(M == M.T,'pair symmetry')
    t=tensor(n,M)
    for i,j,k,l in product(range(n),repeat=4):
        require(t(i,j,k,l)+t(i,k,l,j)+t(i,l,j,k)==0,'first Bianchi identity')
    if weyl:
        require(ricci(n,M)==s.zeros(n),'zero Ricci')

def cp2():
    H=s.zeros(6); pp=pairs(4); ix={p:i for i,p in enumerate(pp)}
    for p,v in [((0,1),2),((0,2),-1),((0,3),-1),((1,2),-1),((1,3),-1),((2,3),2)]:H[ix[p],ix[p]]=v
    for p,q,v in [((0,1),(2,3),2),((0,2),(1,3),1),((0,3),(1,2),-1)]:H[ix[p],ix[q]]=H[ix[q],ix[p]]=v
    return H

def product_weyl(p,q):
    n=p+q
    return s.diag(*[s.Rational(q,p-1) if j<p else s.Rational(p,q-1) if i>=p else -1 for i,j in pairs(n)])

def diagonal_q(n,M):
    pp=pairs(n); a={(i,j):M[z,z] for z,(i,j) in enumerate(pp)}
    def w(i,j):return a[tuple(sorted((i,j)))] if i!=j else 0
    return s.diag(*[w(i,j)**2+sum(w(i,k)*w(j,k) for k in range(n) if k not in (i,j)) for i,j in pp])

def embed(n,H,indices):
    pp=pairs(n); ix={p:i for i,p in enumerate(pp)}; hh=pairs(4); out=s.zeros(len(pp))
    for a,(i,j) in enumerate(hh):
        for b,(k,l) in enumerate(hh):
            u,v=indices[i],indices[j]; x,y=indices[k],indices[l]
            out[ix[tuple(sorted((u,v)))],ix[tuple(sorted((x,y)))]]=(1 if u<v else -1)*(1 if x<y else -1)*H[a,b]
    return out

def main():
    cert=json.loads((ROOT/'certificates.json').read_text())
    H=cp2(); algebraic(4,H,True)
    require(inner(H,H)==24,'CP2 norm'); require(Q(4,H)==6*H,'CP2 Q identity'); require(inner(Q(4,H),H)==144,'CP2 cubic')
    require(s.Rational(144**2,24**3)==s.Rational(3,2),'CP2 quotient')
    bad=H.copy();bad[0,0]+=1
    reject(lambda:algebraic(4,bad,True),'non-Weyl matrix')
    bad=H.copy();bad[0,5]+=1;bad[5,0]+=1
    reject(lambda:algebraic(4,bad,True),'Bianchi failure')
    reject(lambda:require(inner(H,H)==23,'wrong norm'),'wrong norm')
    for n in (4,5):
        A=s.Matrix(n,n,lambda i,j:s.Integer((i+j+1)%4-2))
        B=s.diag(*[s.Integer(i-2) for i in range(n)])
        R=wedge(A)+2*wedge(B)+s.eye(n*(n-1)//2)
        a,S,W=decomposition(n,R); algebraic(n,R);algebraic(n,W,True)
        qr=Q(n,R); qw=Q(n,W)
        require(zero(s.trace(ricci(n,qr))-inner(ricci(n,R),ricci(n,R))),'scalar Q identity')
        require(zero(inner(qr,W)-inner(qw,W)-inner(wedge(S),W)/(n-2)),'general tangency identity')
        require(qw==decomposition(n,qw)[2],'Weyl subalgebra')
        require(zero(inner(decomposition(n,wedge(S))[2],decomposition(n,wedge(S))[2])-(s.Rational(n*n-3*n+3,2*(n-1)*(n-2))*inner(S,S)**2-s.Rational(n,2*(n-2))*s.trace(S**4))),'fourth-moment identity')
    n=s.symbols('n',positive=True); p,q=s.symbols('p q',positive=True)
    Aeven=s.Rational(1,2)*(n-2)/(n-1)
    require(zero(2*n*(n-1)*Aeven/(n-2)**2-n/(n-2)),'even lower endpoint')
    T=p*q*(p+q-1)*(p+q-2)/(2*(p-1)*(q-1))
    explicit=p*q*q/(2*(p-1))+q*p*p/(2*(q-1))+p*q
    require(zero(s.factor(T-explicit)),'two-block norm formula')
    Lodd=n**3*(n-3)/((n-2)**3*(n+1)); Uodd=(n+1)*(n-2)/(n*(n-3))
    require(zero(s.factor(n/(n-2)-Lodd-4*n/((n-2)**3*(n+1)))),'odd lower width')
    require(zero(s.factor(Uodd-n/(n-2)-4/(n*(n-3)*(n-2)))),'odd upper width')
    lower=[]
    for nn in range(4,12):
        L=s.Rational(nn,nn-2) if nn%2==0 else Lodd.subs(n,nn)
        U=s.Rational(4*(nn-1),3*nn)
        require(L>U,'no cone dimensions 4 through 11')
        lower.append({'n':nn,'necessary_lower':str(L),'necessary_upper':str(U),'gap':str(L-U)})
    require(lower==cert['low_dimension_obstructions'],'saved obstruction table')
    require(s.Rational(2662,2187)-s.Rational(40,33)==s.Rational(122,24057),'dimension eleven gap')
    reject(lambda:require(s.Rational(2662,2187)<=s.Rational(40,33),'reversed endpoint'),'reversed cone interval')
    for nn in range(4,17):
        pp=nn//2;qq=nn-pp; V=product_weyl(pp,qq)
        require(ricci(nn,V)==s.zeros(nn),'two-block Weyl')
        require(diagonal_q(nn,V)==(nn-1)*V,'two-block Q')
        require(inner(V,V)==T.subs({p:pp,q:qq}),'two-block norm')
        S=s.diag(*([qq]*pp+[-pp]*qq)); PS=decomposition(nn,wedge(S))[2]
        ratio=inner(PS,PS)/inner(S,S)**2
        expected=s.Rational(nn-2,2*(nn-1)) if nn%2==0 else s.Rational(nn**2*(nn-3),2*(nn-2)*(nn-1)*(nn+1))
        require(ratio==expected,'balanced Ricci witness')
    # Exact full diagonal-Weyl Hessian spectrum at n=12, not the full Weyl space.
    nn=12;pp=pairs(nn); N=len(pp); W=product_weyl(6,6); vals=[W[i,i] for i in range(N)]
    incidence=s.Matrix(nn,N,lambda i,z:s.Integer(i in pp[z])); basis=s.Matrix.hstack(*incidence.nullspace());require(basis.cols==54,'diagonal Weyl dimension')
    ix={e:z for z,e in enumerate(pp)}
    def ww(i,j):return vals[ix[tuple(sorted((i,j)))]]
    D=s.zeros(N)
    for z,(i,j) in enumerate(pp):
        D[z,z]=2*ww(i,j)
        for k in range(nn):
            if k not in (i,j):
                D[z,ix[tuple(sorted((j,k)))]]+=ww(i,k)
                D[z,ix[tuple(sorted((i,k)))]]+=ww(j,k)
    pivots=list(basis.T.rref()[1]); sub=basis.extract(pivots,range(basis.cols)); restricted=sub.inv()*(D*basis).extract(pivots,range(basis.cols))
    require(D*basis==basis*restricted,'diagonal subspace preserved')
    x=s.symbols('x'); target=(x-22)*x**18*(x+s.Rational(22,5))**25*(x-s.Rational(44,5))**10
    require(zero(restricted.charpoly(x).as_expr()-target),'exact diagonal Hessian spectrum')
    # Explicit coordinate CP2 pencils in dimension twelve.
    pencil=[];t=s.symbols('t'); norm0=inner(W,W); beta2=s.Rational(55,36)
    require(norm0==s.Rational(396,5),'dimension twelve norm')
    maps=[(0,1,2,3),(0,6,7,8),(0,1,6,7),(0,6,1,7)]
    for indices in maps:
        HH=embed(12,H,indices); algebraic(12,HH,True); ell=inner(W,HH)
        f=11*norm0+33*ell*t+18*ell*t*t+144*t**3
        norm=norm0+2*ell*t+24*t*t
        difference=s.factor(beta2*norm**3-f**2)
        expected=cert['pencil_differences'][str(ell)]
        require(zero(difference-s.sympify(expected,locals={'t':t})),'saved pencil polynomial')
        quart=s.Poly(s.cancel(difference/t**2),t)
        # Complete the t^4/t^3 terms to a square; residual quadratic must be positive.
        a=quart.nth(4); b=quart.nth(3)/(2*a)
        rem=s.Poly(s.expand(quart.as_expr()-a*(t*t+b*t)**2),t)
        require(a>0 and rem.degree()==2,'quartic SOS leading part')
        discr=rem.nth(1)**2-4*rem.nth(2)*rem.nth(0)
        require(rem.nth(2)>0 and discr<0,'quartic residual positive')
        pencil.append({'indices':list(indices),'inner_product':str(ell),'quartic_discriminant':str(discr)})
    reject(lambda:require(s.Rational(3,2)>beta2,'false CP2 counterexample'),'CP2 does not obstruct dimension twelve')
    require(s.Rational(55,36)-s.Rational(3,2)==s.Rational(1,36),'dimension twelve squared gap')
    output={'status':'PASS','scope':'Exact diagnostics support only the scoped written partial proofs; n0=12 remains unresolved.','checks':COUNT,'negative_controls_rejected':NEGATIVE,'low_dimension_obstructions':lower,'diagonal_tangent_dimension':53,'one_third_diagonal_constrained_hessian_eigenvalues':{'-11':18,'-77/5':25,'-11/5':10},'pencils':pencil,'weyl_dimension_n12':1638,'unresolved_beta12_squared_upper':'55/36'}
    print(json.dumps(output,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
