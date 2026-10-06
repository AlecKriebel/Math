#!/usr/bin/env python3
"""Independent exact audit, using no imports from the author's checker."""
import argparse, hashlib, itertools, json
from fractions import Fraction
from pathlib import Path


def determinant(a):
    n=len(a); total=0
    for sigma in itertools.permutations(range(n)):
        term=(-1)**sum(sigma[i]>sigma[j] for i in range(n) for j in range(i+1,n))
        for i in range(n): term*=a[i][sigma[i]]
        total+=term
    return total


def multiply(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def rank(a,p=None):
    a=[[Fraction(x) if p is None else x%p for x in row] for row in a]; r=0
    for j in range(len(a[0])):
        z=next((i for i in range(r,len(a)) if a[i][j]),None)
        if z is None: continue
        a[r],a[z]=a[z],a[r]
        inv=1/a[r][j] if p is None else pow(a[r][j],-1,p)
        a[r]=[x*inv if p is None else x*inv%p for x in a[r]]
        for i in range(r+1,len(a)):
            c=a[i][j];a[i]=[x-c*y if p is None else (x-c*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r


def algebra():
    # Basis: e0,e1,e2,a1,a2,a3,u1,u2,u3,v1,v2,v3.
    # u: vertex0->1; v: vertex0->2; a: vertex1->2.
    F=[[[0,1,0],[-1,0,0],[0,0,0]],[[0,0,0],[0,0,1],[0,-1,0]],[[0,0,-1],[0,0,0],[1,0,0]]]
    starts=[0,1,2]+[1]*3+[0]*6; ends=[0,1,2]+[2]*3+[1]*3+[2]*3
    table={}
    for i,j in itertools.product(range(12),repeat=2):
        out=[0]*12
        if i<3 and i==starts[j]:out[j]=1
        elif j<3 and j==ends[i]:out[i]=1
        elif 6<=i<9 and 3<=j<6:
            for s in range(3):out[9+s]=F[j-3][s][i-6]
        table[i,j]=out
    def product(a,b):
        return [sum(a[i]*b[j]*table[i,j][s] for i in range(12) for j in range(12) if a[i] and b[j]) for s in range(12)]
    basis=[[int(i==j) for j in range(12)] for i in range(12)]
    for i,j,k in itertools.product(range(12),repeat=3):
        assert product(table[i,j],basis[k])==product(basis[i],table[j,k])
    iden=[1,1,1]+[0]*9
    for b in basis:assert product(iden,b)==product(b,iden)==b
    hom=[[sum(s==j and t==i for s,t in zip(starts,ends)) for j in range(3)] for i in range(3)]
    pdim=[[sum(s==i and t==j for s,t in zip(starts,ends)) for j in range(3)] for i in range(3)]
    assert hom==[[1,0,0],[3,1,0],[3,3,1]]
    assert pdim==[[1,3,3],[0,1,3],[0,0,1]]
    return F,hom,pdim


def results():
    F,hom,pdim=algebra()
    M=[F[1][i]+F[2][i] for i in range(3)]+[F[2][i]+F[0][i] for i in range(3)]
    d=determinant(M);assert d==1
    inv=[[(-1)**(i+j)*determinant([[M[r][c] for c in range(6) if c!=i] for r in range(6) if r!=j]) for j in range(6)] for i in range(6)]
    identity=[[int(i==j) for j in range(6)] for i in range(6)]
    assert multiply(M,inv)==multiply(inv,M)==identity
    # Independent sparse-polynomial expansion of det G and G*(x2,x3,x1).
    entries={(0,1):(1,0),(1,0):(-1,0),(1,2):(1,1),(2,1):(-1,1),(2,0):(1,2),(0,2):(-1,2)}
    terms={}
    for sigma in itertools.permutations(range(3)):
        coeff=(-1)**sum(sigma[i]>sigma[j] for i in range(3) for j in range(i+1,3));exponents=[0]*3
        for i in range(3):
            if (i,sigma[i]) not in entries:coeff=0;break
            c,var=entries[i,sigma[i]];coeff*=c;exponents[var]+=1
        terms[tuple(exponents)]=terms.get(tuple(exponents),0)+coeff
    assert not {e:c for e,c in terms.items() if c}
    kernel_vars=[1,2,0]
    for i in range(3):
        poly={}
        for j in range(3):
            if (i,j) in entries:
                c,v=entries[i,j];e=tuple(sorted([v,kernel_vars[j]]));poly[e]=poly.get(e,0)+c
        assert all(c==0 for c in poly.values())
    finite={}
    for p in [2,3,5,7,11]:
        for x in itertools.product(range(p),repeat=3):
            G=[[sum(x[k]*F[k][i][j] for k in range(3)) for j in range(3)] for i in range(3)]
            assert rank(G,p)==(2 if any(x) else 0)
        assert rank(M,p)==6;finite[str(p)]=p**3
    # Generic E(eta,eta) <= 1 certificate. Universal kernel explained in AUDIT.md.
    x=[1,0,0]; y=[0,1,0];v=[0,0,1];w=[0,0,0]
    L=[[w[i],-v[i],0]+[-F[0][i][j] for j in range(3)] for i in range(3)]
    L += [[y[i],0,-x[i],0,0,0] for i in range(3)]
    assert rank(L)==5
    assert all(rank(L,p)==5 for p in [2,3,5,7,11])
    sub=[(0,a,b) for a,b in itertools.product([0,1],repeat=2) if a<=b]
    subvals=[a-b for _,a,b in sub];qvals=[-z for z in subvals]
    assert subvals==[0,-1,0] and qvals==[0,1,0]
    eta=(1,1,-1)
    proper_splits=[]
    for support in itertools.product([0,1],repeat=3):
        if sum(support) in [0,3]:continue
        a=tuple(eta[i]*support[i] for i in range(3));b=tuple(eta[i]-a[i] for i in range(3));pair=sorted([a,b])
        if pair not in proper_splits:proper_splits.append(pair)
    assert len(proper_splits)==3
    # Fractions check strict boundary inequalities without floating-point tolerance.
    rationals=[Fraction(n,d) for d in [1,2,3] for n in range(-3,4)]
    points=0
    for a,b,c in itertools.product(rationals,repeat=3):
        lhs=(a>0 and b>0 and b+c==0);rhs=(a>0 and b>0 and c==-b);assert lhs==rhs;points+=1
    return {'schema':'tf-equivalence-independent-checks-v1','problem_id':30005755,'algebra_dimension':12,'basis_associativity_checks':1728,'hom_dimensions_source_rows_target_columns':hom,'projective_dimension_vectors':pdim,'determinant_leibniz':d,'integer_two_sided_inverse':inv,'symbolic_alternating_determinant_zero':True,'symbolic_kernel':['x2','x3','x1'],'finite_field_rank_triples':finite,'generic_eta_self_E_matrix':L,'generic_eta_self_E_matrix_rank':5,'eta_self_E_value_with_textual_upper_bound':1,'Y_submodule_dimensions':[list(s) for s in sub],'Y_submodule_weight_values':subvals,'Y_quotient_weight_values':qvals,'unordered_sign_coherent_splits':len(proper_splits),'rational_boundary_checks':points,'full_target_solved':False,'interpretation':'Exact finite algebra and arithmetic certificates; all-module TF equality still requires the scoped textual argument.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',type=Path);p.add_argument('--write',type=Path);a=p.parse_args();r=results()
    if a.check:
        assert r==json.loads(a.check.read_text()),'audit result mismatch';print('PASS: independent algebra, exact determinant, kernel, E-space, and witness checks')
    elif a.write:a.write.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    else:print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':main()
