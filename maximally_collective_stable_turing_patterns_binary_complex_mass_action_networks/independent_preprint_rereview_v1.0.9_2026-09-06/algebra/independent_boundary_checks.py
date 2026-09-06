#!/usr/bin/env python3
"""Independent v1.0.9 algebra boundary checks; imports no project modules."""
from __future__ import annotations
import itertools
import json
from pathlib import Path
import sympy as S

def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)

def reactions(m):
    n=m+1
    def vec(*pairs):
        v=S.zeros(n,1)
        for i,c in pairs: v[i]=c
        return v
    rows=[(vec(),vec((0,1)))]
    rows += [(vec((0,1),(i,1)),vec((0,1),(i+1,1))) for i in range(1,m-2)]
    rows += [(vec((0,1),(m-2,1)),vec((m-1,2))),
             (vec((m-1,2)),vec((1,1))),
             (vec((m,2)),vec((0,1),(m-1,1))),
             (vec((0,1),(m-1,1)),vec((m,2)))]
    return rows

def construct(m,a,b,h=None):
    rows=reactions(m)
    Y=S.Matrix.hstack(*(x for x,y in rows))
    G=S.Matrix.hstack(*(y-x for x,y in rows))
    flux=S.diag(*([a]*m+[b,b]))
    return G,Y,G*flux*Y.T*(S.diag(*h) if h is not None else S.eye(m+1))

def components(M,I):
    # Reachability-based SCCs, separately implemented from manuscript verifier.
    I=set(I)
    reach={j:{j} for j in I}
    for j in I:
        todo=[j]
        while todo:
            k=todo.pop()
            for i in I-reach[j]:
                if M[i,k]!=0: reach[j].add(i); todo.append(i)
    remain=set(I); out=[]
    while remain:
        j=min(remain)
        C={i for i in remain if i in reach[j] and j in reach[i]}
        out.append(C);remain-=C
    return out

def hurwitz(poly):
    c=poly.all_coeffs();n=len(c)-1
    H=S.zeros(n,n)
    for i in range(n):
        for j in range(n):
            k=2*j-i+1
            H[i,j]=c[k] if 0<=k<=n else 0
    return all(H[:k,:k].det()>0 for k in range(1,n+1))

def main():
    out={"source":"literal reaction construction, no project imports", "checks":{}}
    a,b=S.symbols('a b',positive=True)
    omission_count=0
    for m in range(3,10):
        G,Y,A=construct(m,a,b)
        c=S.Matrix([0]+[4]*(m-2)+[2,1])
        require(G.shape==(m+1,m+2),f"shape {m}")
        require(G.rank()==m and c.T*G==S.zeros(1,m+2),f"rank/conservation {m}")
        require(G*S.Matrix([a]*m+[b,b])==S.zeros(m+1,1),f"flux {m}")
        require(all(sum(x)<=2 and sum(y)<=2 for x,y in reactions(m)),f"binary {m}")
        r=S.Matrix([2]+[-2]*(m-2)+[0,1])
        require(A*r==S.zeros(m+1,1),f"kernel {m}")
        for omit in range(m+1):
            coeff=S.factor((-1)**m*A.minor_submatrix(omit,omit).det(method='domain-ge'))
            expected=0 if omit in (0,m-1) else (-2 if omit==m else 16)*a**(m-1)*b
            require(S.expand(coeff-expected)==0,f"omission {m} {omit}")
            omission_count+=1
    out['checks']['symbolic_reaction_and_omission_identities']=omission_count
    print('Symbolic reaction and omission identities PASS',flush=True)

    # Re-derive arbitrary-scaling boundary stability from reactions.
    h1,hm,hz=S.symbols('h1 hm hz',positive=True)
    A=construct(4,a,b)[2]
    triad=A.extract([0,3,4],[0,3,4])*S.diag(h1,hm,hz)
    cc=triad.charpoly().all_coeffs()
    require(S.expand(cc[1]-(a*h1+4*a*hm+b*h1+b*hm+4*b*hz))==0,'triad c1')
    require(S.expand(cc[2]-a*(4*a*h1*hm+7*b*h1*hm+4*b*h1*hz+16*b*hm*hz))==0,'triad c2')
    require(S.expand(cc[3]-16*a*a*b*h1*hm*hz)==0,'triad c3')
    gap=S.Poly(S.expand((cc[1]*cc[2]-cc[3])/a),a,b,h1,hm,hz)
    require(len(gap.terms())==14 and all(c>0 for c in gap.coeffs()),'triad fourteen-term Routh gap')
    for I in itertools.combinations(range(3),2):
        q=triad.extract(I,I).charpoly()
        require(all(all(v>0 for v in S.Poly(c,a,b,h1,hm,hz).coeffs()) for c in q.all_coeffs()),'triad pair Hurwitz')
    out['checks']['triad_Routh_positive_monomials']=14

    # The sole graph cancellation occurs at b=2a; scaling H cannot affect zero entries.
    scc_sets=0;corrected_orders=0
    for m in range(3,12):
        for rate in (1,2,3):
            A=construct(m,S.Integer(1),S.Integer(rate))[2]
            allowed=[set(range(m-1)),set(range(1,m))]
            boundary={0,m-1,m}
            for k in range(1,m):
                for I in itertools.combinations(range(m+1),k):
                    for C in components(A,I):
                        require(len(C)==1 or C in allowed or C<=boundary,f"SCC {m} {rate} {I} {C}")
                    scc_sets+=1
            for j in range(1,m-1):
                blocks=[[i] for i in range(j+1,m-1)]+[[0,m-1,m]]+[[i] for i in range(1,j)]
                for u,block in enumerate(blocks):
                    for later in blocks[u+1:]:
                        require(all(A[i,k]==0 for i in block for k in later),f"Frobenius order {m},{rate},{j}")
                corrected_orders+=1
    out['checks']['all_retained_sets_SCC']=scc_sets
    out['checks']['corrected_Frobenius_orders']=corrected_orders
    print('SCC exhaustion and corrected Frobenius orders PASS',flush=True)

    # T=1 is a genuine nonsemisimple conservation boundary, not a stable endpoint.
    degeneracy=[]
    for m in range(3,10):
        for hz in (S.Rational(1,16*(m-2)),S.Rational(1,8*(m-2)),S.Rational(1,4*(m-2))):
            h=[S.Integer(1)]*m+[hz]
            J=construct(m,S.Integer(1),S.Integer(1),h)[2]
            coeff=J.charpoly().all_coeffs()
            T=8*(m-2)*hz
            require(J.rank()==m,f"rank at T={T},m={m}")
            require(coeff[-1]==0,f"conservation at T={T}")
            require(S.sign(coeff[-2])==S.sign(T-1),f"zero coefficient T={T}")
            require(all(x>0 for x in coeff[:-2]),f"lower minors char coefficients m={m},T={T}")
            if T==1:
                require(coeff[-2]==0 and coeff[-3]>0,f"exact double zero m={m}")
                require((J**2).rank()==m-1,f"one Jordan block of size two m={m}")
            degeneracy.append({'m':m,'T':str(T),'rank_J':J.rank(),'zero_multiplicity':2 if T==1 else 1,'linear_coefficient':str(coeff[-2])})
    out['checks']['conservation_boundary_cases']=degeneracy
    print('Conservation-zero boundary checks PASS',flush=True)

    # Exact n=2 eligible ray, equality ray, and absent sum-hypothesis diagnostic.
    s,l=S.symbols('s lambda',real=True)
    J=S.Matrix([[1,1],[-2,-2]])
    chi=S.factor((l*S.eye(2)+s*S.diag(1,3)-J).det())
    require(S.expand(chi-(l*l+(1+4*s)*l+s*(3*s-1)))==0,'n2 characteristic')
    equality=S.factor((s*S.diag(1,2)-J).det())
    require(equality==2*s*s,'n2 beta1 equality')
    outside=S.Matrix([[2,2],[-1,-1]])-S.Rational(1,100)*S.diag(3,1)
    ev=list(outside.eigenvals())
    require(all(x.is_positive for x in ev),'omitted sum hypothesis positive roots')
    out['checks']['n2']={'eligible_characteristic':str(chi),'threshold':'1/3','equality_determinant':str(equality),'without_sum_hypothesis_J':[[2,2],[-1,-1]],'without_sum_hypothesis_D':[3,1],'eigenvalues_at_s_1_100':[str(x) for x in ev]}

    # Exact contrast comparisons at algebraic endpoints and rational interior points.
    # The report gives the dimension-independent inequalities, not an extrapolation.
    endpoint_cases=0
    for nu in list(range(1,13))+[63,127,997]:
        m=nu+2
        L0=1/S.sqrt(3) if nu==1 else S.sqrt(S.Rational(5,4*nu))
        L1=S.Rational(90*nu,90*nu+1)
        for L in [L0,L1,(L0+L1)/2]:
            h=[S.Integer(1)]+[S.Rational(91*m-181-i,91*m-180-i)/L for i in range(2,m)]+[S.Integer(1),S.Integer(1)]
            d=[S.Rational(23,63)]+[1/((91*m-180-i)*L) for i in range(2,m)]+[S.Rational(1,7),S.Rational(16,45)]
            # Interior h_i decreases and d_i increases with i, since K_i
            # decreases by one. It suffices to check their two endpoints
            # against the three boundary species (proved in the report).
            extremal_indices={0,1,m-2,m-1,m}
            require(all(S.simplify(h[i]-1)>=0 for i in extremal_indices),'h minimum')
            require(all(S.simplify(h[1]-h[i])>=0 for i in extremal_indices),'h maximum')
            require(all(S.simplify(d[i]-d[1])>=0 for i in extremal_indices),'d minimum')
            require(all(S.simplify(d[0]-d[i])>=0 for i in extremal_indices),'d maximum')
            chiD=S.simplify(d[0]/d[1]); chiH=h[1]
            require(S.simplify(chiD-S.Rational(23,63)*91*nu*L)==0,'contrast D')
            require(S.simplify(chiH-S.Rational(91*nu-1,91*nu)/L)==0,'contrast H')
            require(S.simplify(chiD/chiH)>1,'within-family minimax ordering')
            endpoint_cases+=1
    out['checks']['contrast_endpoint_and_interior_cases']=endpoint_cases
    out['status']='PASS'
    path=Path(__file__).with_name('independent_boundary_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','omission_identities':omission_count,'SCC_sets':scc_sets,'Frobenius_orders':corrected_orders,'conservation_cases':len(degeneracy),'contrast_cases':endpoint_cases}))

if __name__=='__main__':main()
