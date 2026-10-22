#!/usr/bin/env python3
"""Independent exact audit: generic associativity, cyclic trace, and balance kernels.
Requires Python 3 and SymPy. Does not import any author or previous-audit code.
"""
import json
from itertools import product, combinations
from math import comb
from collections import Counter
from fractions import Fraction
import sympy as S

def algebra_check():
    alpha,beta=S.symbols('alpha beta',nonzero=True)
    names='c_x c_y d_p d_q s_x s_y r_p r_q gamma delta'
    unknown=S.symbols(names)
    cx,cy,dp,dq,sx,sy,rp,rq,gamma,delta=unknown
    # eA,x,y,a,eB,p,q,b,u,w,v,z; corner labels target,source.
    corners=['AA']*4+['BB']*4+['AB']*2+['BA']*2
    degrees=[0,2,2,4,0,2,2,4,1,3,1,3]
    table={}
    def put(i,j,value): table[i,j]={k:S.sympify(v) for k,v in value.items()}
    for i,corner in enumerate(corners):
        put(0 if corner[0]=='A' else 4,i,{i:1})
        put(i,0 if corner[1]=='A' else 4,{i:1})
    for i,j,k in [(1,2,3),(2,1,3),(5,6,7),(6,5,7)]: put(i,j,{k:1})
    for i in [1,2]: put(i,8,{9:1})
    for j in [5,6]: put(8,j,{9:1})
    for i,j,c in [(10,1,sx),(10,2,sy),(5,10,rp),(6,10,rq)]: put(i,j,{11:c})
    put(8,10,{1:cx,2:cy}); put(10,8,{5:dp,6:dq})
    for i,j,k,c in [(8,11,3,alpha),(9,10,3,beta),(10,9,7,gamma),(11,8,7,delta)]: put(i,j,{k:c})
    def mult(a,b,T=table):
        result={}
        for i,x in a.items():
            for j,y in b.items():
                for k,z in T.get((i,j),{}).items(): result[k]=result.get(k,0)+x*y*z
        return {k:S.expand(v) for k,v in result.items() if S.expand(v)!=0}
    units=[{i:S.Integer(1)} for i in range(12)]
    constraints=set()
    for i,j,k in product(range(12),repeat=3):
        lhs=mult(mult(units[i],units[j]),units[k])
        rhs=mult(units[i],mult(units[j],units[k]))
        for key in set(lhs)|set(rhs):
            e=S.expand(lhs.get(key,0)-rhs.get(key,0))
            if e!=0: constraints.add(e)
    # Invert alpha,beta in the coefficient field, as allowed by Serre nondegeneracy.
    G=S.groebner(sorted(constraints,key=str),*unknown,domain=S.QQ.frac_field(alpha,beta))
    expected=dict(zip(unknown,[beta,beta,beta,beta,beta/alpha,beta/alpha,beta/alpha,beta/alpha,beta,alpha]))
    assert len(G.polys)==len(unknown)
    inv_a,inv_b=S.symbols('inv_alpha inv_beta')
    localized=S.groebner(list(constraints)+[alpha*inv_a-1,beta*inv_b-1],
                         *unknown,inv_a,inv_b,alpha,beta,domain=S.QQ)
    for v in unknown:
        numerator=S.cancel(v-expected[v]).as_numer_denom()[0]
        assert localized.reduce(numerator)[1]==0
    for v in unknown: assert G.reduce(v-expected[v])[1]==0
    for f in G.polys: assert S.cancel(f.as_expr().subs(expected))==0
    normal={pair:{k:S.cancel(v.subs(expected)) for k,v in row.items()} for pair,row in table.items()}
    standard={pair:{k:v.subs({alpha:1,beta:1}) for k,v in row.items()} for pair,row in normal.items()}
    for i,j,k in product(range(12),repeat=3):
        lhs=mult(mult(units[i],units[j],normal),units[k],normal)
        rhs=mult(units[i],mult(units[j],units[k],normal),normal)
        assert all(S.cancel(lhs.get(q,0)-rhs.get(q,0))==0 for q in set(lhs)|set(rhs))
    # Map the parameterized basis to beta*v_std, alpha*z_std and other bases unchanged.
    factors=[S.Integer(1)]*10+[beta,alpha]
    for i,j in product(range(12),repeat=2):
        l=normal.get((i,j),{}); r=standard.get((i,j),{})
        for k in set(l)|set(r): assert S.cancel(l.get(k,0)*factors[k]-factors[i]*factors[j]*r.get(k,0))==0
        for k in l:
            assert degrees[k]==degrees[i]+degrees[j]
            assert corners[i][1]==corners[j][0]
            assert corners[k]==corners[i][0]+corners[j][1]
    # The graded Serre trace is tr(a)=1, tr(b)=-1, zero elsewhere.
    def trace(row):return row.get(3,0)-row.get(7,0)
    for i,j in product(range(12),repeat=2):
        assert S.cancel(trace(normal.get((i,j),{}))-(-1)**(degrees[i]*degrees[j])*trace(normal.get((j,i),{})))==0
    gram=S.Matrix(12,12,lambda i,j:trace(normal.get((i,j),{})))
    assert S.factor(gram.det())!=0
    # Graded automorphisms preserve the two isotropic lines: (a*x+b*y)^2=2*a*b*x*y.
    return {'generic_associativity_triples':1728,'distinct_generic_equations':len(constraints),
            'fraction_field_groebner_basis_size':len(G.polys),
            'localized_polynomial_groebner_basis_size':len(localized.polys),
            'necessity_has_no_extra_parameter_exclusions':True,
            'unique_structure_coefficients':{str(k):str(v) for k,v in expected.items()},
            'normal_form_symbolic_associativity_triples':1728,
            'symbolic_basis_change_products':144,'graded_cyclic_trace_checks':144,
            'trace_gram_determinant':str(S.factor(gram.det())),
            'trace_normalization':'tr(a)=1, tr(b)=-1',
            'grading_and_corner_compatibility':True}

def all_pairings(vertices):
    if not vertices: yield (); return
    a=vertices[0]
    for b in vertices[1:]:
        rest=tuple(v for v in vertices if v not in [a,b])
        for tail in all_pairings(rest): yield tuple(sorted(((a,b),)+tail))

def noncrossing(pairs):
    return all(not (a<c<b<d or c<a<d<b) for (a,b),(c,d) in combinations(pairs,2))

def components(n,*pairings):
    adjacent={i:set() for i in range(n)}
    for p in pairings:
        for a,b in p:adjacent[a].add(b);adjacent[b].add(a)
    unvisited=set(range(n)); out=[]
    while unvisited:
        work=[min(unvisited)]; seen=set()
        while work:
            a=work.pop()
            if a not in seen:seen.add(a);work.extend(adjacent[a]-seen)
        unvisited-=seen;out.append(tuple(sorted(seen)))
    return out

def rational_rank(rows):
    pivots={}
    for raw in rows:
        row={j:Fraction(c) for j,c in enumerate(raw) if c}
        while row:
            p=min(row)
            if p not in pivots:
                f=row[p];pivots[p]={j:v/f for j,v in row.items()};break
            f=row[p]
            for j,c in pivots[p].items():
                v=row.get(j,0)-f*c
                if v:row[j]=v
                else:row.pop(j,None)
    return len(pivots)

def balance_dimension(n,A,B,C):
    groups=components(n,A,C); r=len(groups)
    ca=len(components(n,A,B));cb=len(components(n,B,C));s=len(components(n,A,B,C))
    twice_m=n//2-ca-cb+r; assert twice_m%2==0
    m=twice_m//2
    basis=list(combinations(range(r),m)) if 0<=m<=r else []
    targets=list(combinations(range(r),m+1)) if 0<=m+1<=r else []
    index={v:i for i,g in enumerate(groups) for v in g}
    rows=[]
    for a,b in B:
        i,j=index[a],index[b]
        for target in targets:
            T=set(target);row=[]
            for monomial in basis:
                M=set(monomial)
                row.append(int(i not in M and M|{i}==T)-int(j not in M and M|{j}==T))
            rows.append(row)
    dim=len(basis)-rational_rank(rows)
    q=m-r+s; predicted=comb(s,q) if 0<=q<=s else 0
    assert dim==predicted
    return dim

def balance_check():
    rows=[];total=0
    for k in range(1,5):
        matches=sorted(set(p for p in all_pairings(tuple(range(2*k))) if noncrossing(p)))
        hist=Counter(balance_dimension(2*k,A,B,C) for A,B,C in product(matches,repeat=3))
        rows.append({'k':k,'matchings':len(matches),'triples':len(matches)**3,'dimension_histogram':dict(sorted(hist.items()))})
        total+=len(matches)**3
    A=((0,1),(2,5),(3,4),(6,7));B=((0,3),(1,2),(4,5),(6,7));C=((0,5),(1,4),(2,3),(6,7))
    assert balance_dimension(8,A,B,C)==2
    # For the six-point factor, input/output each one circle; three cup surgeries give chi=-3.
    # With three boundary circles, this connected surface has genus 1: 2-2*g-3=-3.
    # Standard TQFT sends 1 tensor 1 to m Delta(1)=2*u, untouched factor stays 1.
    return {'all_triples_checked':total,'enumeration':rows,'k4_example_dimension':2,
            'standard_tqft_k4_example_image':'2*u (common-cup factor is the unit)'}

def koszul_check():
    w,x,y=S.symbols('w x y')
    da1=S.Matrix([[w,y]]);da2=S.Matrix([-y,w]);db1=S.Matrix([[w,x]]);db2=S.Matrix([-x,w])
    f1=S.Matrix([[0,1]]);f2=S.Matrix([-1,0]);g1=f1;g2=f2
    expressions=[da1*da2,db1*db2,db1*f2+f1*da2,da1*g2+g1*db2,g1*f2,f1*g2]
    assert all(e==S.zeros(*e.shape) for e in expressions)
    return {'exact_polynomial_matrix_identities':len(expressions),'scope':'Local model only'}

def main():
    result={'status':'PASS','coefficient_field':'QQ(alpha,beta)','algebra':algebra_check(),
            'higher_rank':balance_check(),'local_koszul':koszul_check()}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
