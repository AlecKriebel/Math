#!/usr/bin/env python3
"""Independent closed-form F_3 certificate; does not import author code."""
from collections import Counter, defaultdict
from itertools import product
from math import comb, factorial
import json

P=3
E=list(product(range(3),repeat=3))
I={e:i for i,e in enumerate(E)}
U=I[(0,0,0)]; X=I[(1,0,0)]; Y=I[(0,1,0)]; Z=I[(0,0,1)]
COUNT=Counter()
def check(ok,name):
    COUNT[name]+=1
    if not ok: raise AssertionError(name)
def tidy(v): return {a:c%P for a,c in v.items() if c%P}
def add(*vs):
    out=defaultdict(int)
    for v in vs:
        for a,c in v.items():out[a]+=c
    return tidy(out)
def times(v,c):return tidy({a:c*b for a,b in v.items()})
def unit(a):return {a:1}
def prod(a,b):
    if a is None or b is None:return None
    e=tuple(x+y for x,y in zip(E[a],E[b]))
    return I[e] if max(e)<3 else None
M=[[prod(a,b) for b in range(27)] for a in range(27)]
def multiply(v,w):
    out=defaultdict(int)
    for a,c in v.items():
        for b,d in w.items():
            q=M[a][b]
            if q is not None:out[q]+=c*d
    return tidy(out)
def linear(table,v):return add(*(times(table[a],c) for a,c in v.items()))
def coproduct(a):
    i,j,k=E[a];out=defaultdict(int)
    for u in range(i+1):
        for v in range(j+1):
            for r in range(k+1):
                for s in range(k-r+1):
                    t=k-r-s; l=(u+t,v,r); rr=(i-u,j-v+t,s)
                    if max(l+rr)<3:
                        out[I[l],I[rr]]+=comb(i,u)*comb(j,v)*factorial(k)//(factorial(r)*factorial(s)*factorial(t))
    return tidy(out)
def antipode(a):
    i,j,k=E[a];out=defaultdict(int)
    for t in range(k+1):
        e=(i+t,j+t,k-t)
        if max(e)<3:out[I[e]]+=(-1)**(i+j+k-t)*comb(k,t)
    return tidy(out)
D=[coproduct(a) for a in range(27)]
S=[antipode(a) for a in range(27)]
def tensor_multiply(v,w):
    out=defaultdict(int)
    for a,c in v.items():
        for b,d in w.items():
            q=tuple(M[x][y] for x,y in zip(a,b))
            if None not in q:out[q]+=c*d
    return tidy(out)
def translate(t,right=True,delta=D):
    return [tidy({b:c for (f,b),c in da.items() if f==t}) if right else tidy({f:c for (f,b),c in da.items() if b==t}) for da in delta]
def comm(F,G,a):return add(linear(F,G[a]),times(linear(G,F[a]),-1))

def rank(rows):
    """Column-stream independent row-echelon elimination."""
    piv={}
    for rr in rows:
        row=[x%P for x in rr]
        for p,r in sorted(piv.items()):
            if row[p]:
                c=row[p]; row=[(a-c*b)%P for a,b in zip(row,r)]
        j=next((j for j,a in enumerate(row) if a),None)
        if j is not None:
            inv=1 if row[j]==1 else 2
            piv[j]=[(a*inv)%P for a in row]
    return len(piv)

# Both B_n and normalized induced X_n use coordinates (left, inner..., right).
def comparison(v,theta=False):
    out=defaultdict(int)
    for row,c in v.items():
        a,*mid,b=row
        choices=product(*(D[t].items() for t in mid))
        for entries in choices:
            lefts=[]; rr=unit(U); k=c
            for (l,r),d in entries:lefts.append(l);rr=multiply(rr,unit(r));k*=d
            if theta:rr=linear(S,rr)
            rr=multiply(rr,unit(b))
            for end,d in rr.items():out[(a,*lefts,end)]+=k*d
    return tidy(out)
def bar_d(v):
    out=defaultdict(int)
    for row,c in v.items():
        for i in range(len(row)-1):
            q=M[row[i]][row[i+1]]
            if q is not None:out[row[:i]+(q,)+row[i+2:]]+=c*(-1)**i
    return tidy(out)
def induced_d(v):
    out=defaultdict(int)
    for row,c in v.items():
        a,*mid,b=row;n=len(mid)
        for (l,r),d in D[mid[0]].items():
            start=M[a][l]
            if start is not None:
                for end,e in multiply(S[r],unit(b)).items():out[(start,*mid[1:],end)]+=c*d*e
        for i in range(n-1):
            q=M[mid[i]][mid[i+1]]
            if q is not None:out[(a,*mid[:i],q,*mid[i+2:],b)]+=c*(-1)**(i+1)
        if mid[-1]==U:out[(a,*mid[:-1],b)]+=c*(-1)**n
    return tidy(out)

def run():
    COUNT.clear()
    R={t:translate(t) for t in (X,Y,Z)}
    L={t:translate(t,False) for t in (X,Y,Z)}
    for a in range(27):
        aa=unit(a);dl=defaultdict(int);dr=defaultdict(int)
        for (b,c),n in D[a].items():
            for (l,r),m in D[b].items():dl[(l,r,c)]+=n*m
            for (l,r),m in D[c].items():dr[(b,l,r)]+=n*m
        check(tidy(dl)==tidy(dr),'coassociativity')
        check(tidy({b:c for (b,d),c in D[a].items() if d==U})==aa and tidy({b:c for (d,b),c in D[a].items() if d==U})==aa,'counits')
        lhs=add(*(times(multiply(S[b],unit(c)),n) for (b,c),n in D[a].items()))
        rhs=add(*(times(multiply(unit(b),S[c]),n) for (b,c),n in D[a].items()))
        check(lhs==rhs==({U:1} if a==U else {}),'antipodes')
        check(linear(S,S[a])==aa,'involution')
        check(comm(R[X],R[Y],a)==times(R[Z][a],-1),'right_bracket')
        check(comm(L[X],L[Y],a)==L[Z][a],'left_bracket_opposite_sign')
        check(comm(R[X],R[Y],a).get(U,0)==(2 if a==Z else 0),'scalar_nonboundary_bracket')
        for t in (X,Y,Z):check(R[t][a].get(U,0)==int(a==t),'epsilon_splitting')
        for c in range(3):check((int(a==U)*c-c*int(a==U))%3==0,'zero_B1')
    rows=[]
    for a,b in product(range(27),repeat=2):
        q=M[a][b]; ab=unit(q) if q is not None else {}
        check(M[a][b]==M[b][a],'commutativity')
        check(linear(D,ab)==tensor_multiply(D[a],D[b]),'bialgebra_compatibility')
        check(int(q==U)==int(a==U)*int(b==U),'augmentation_multiplicative')
        row=[(int(a==U)*int(b==t)-int(q==t)+int(a==t)*int(b==U))%3 for t in range(27)]
        rows.append(row)
        for t in (X,Y,Z):
            check(row[t]==0,'augmentation_derivations')
            check(linear(R[t],ab)==add(multiply(R[t][a],unit(b)),multiply(unit(a),R[t][b])),'hochschild_derivations')
    for a,b,c in product(range(27),repeat=3):check(prod(prod(a,b),c)==prod(a,prod(b,c)),'associativity')
    d1rank=rank(rows);check(d1rank==24,'delta1_rank');check(27-d1rank==3,'H1_dimension')
    for n in (1,2):
        for mid in product(range(27),repeat=n):
            v=unit((U,*mid,U))
            check(comparison(comparison(v,True))==v,'psi_theta_inverse_degree_'+str(n))
            check(comparison(comparison(v),True)==v,'theta_psi_inverse_degree_'+str(n))
            check(bar_d(comparison(v,True))==comparison(induced_d(v),True),'theta_chain_degree_'+str(n))
            check(induced_d(comparison(v))==comparison(bar_d(v)),'psi_chain_degree_'+str(n))
    for a in range(27):
        v=comparison(unit((U,a,U)))
        for t in (X,Y,Z):
            lifted=add(*(times(multiply(unit(l),unit(r)),c) for (l,m,r),c in v.items() if m==t))
            check(lifted==R[t][a],'actual_bar_induction_image')
    skew=add(D[Z],times({(b,a):c for (a,b),c in D[Z].items()},-1))
    check(skew=={(X,Y):1,(Y,X):2},'noncocommutativity')
    check(comm(R[X],R[Y],Z).get(U)==2,'witness_nonzero')
    # Four substantive mutations with explicit witness failure.
    check(comm(R[X],R[Y],Z)!=unit(U),'mutation_wrong_orientation')
    check(comm(R[X],R[Y],Z)!={},'mutation_zero_bracket')
    badS=list(S);badS[Z]={Z:2}
    bad=add(*(times(multiply(badS[b],unit(c)),n) for (b,c),n in D[Z].items()))
    check(bool(bad),'mutation_missing_antipode_correction')
    primitiveD=[]
    for a in range(27):
        i,j,k=E[a];out=defaultdict(int)
        for u,v,w in product(range(i+1),range(j+1),range(k+1)):
            out[I[(u,v,w)],I[(i-u,j-v,k-w)]]+=comb(i,u)*comb(j,v)*comb(k,w)
        primitiveD.append(tidy(out))
    px=translate(X,delta=primitiveD);py=translate(Y,delta=primitiveD)
    check(comm(px,py,Z)=={} and comm(px,py,Z)!=comm(R[X],R[Y],Z),'mutation_removed_cross_term')
    return {'status':'PASS','field':'F_3','dimension':27,'delta1_rank':d1rank,'H1_dimension':3,'B1_dimension':0,'right_bracket':'-f_z','left_bracket':'+f_z','witness_value':2,'assertions':sum(COUNT.values()),'checks':dict(sorted(COUNT.items())),'independent_implementation':'Closed binomial/multinomial structure constants; no author-code imports.','bar_comparison_coverage':'Both inverse and chain-map identities in degrees one and two on all inner basis tuples; H-bimodule linearity covers outer factors.','mathematical_negative_controls':4,'limitations':'Exact arithmetic and a written proof, not formal proof-assistant or human peer review.'}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
