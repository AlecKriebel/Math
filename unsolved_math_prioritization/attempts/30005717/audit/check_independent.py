#!/usr/bin/env python3
"""Independent exact audit. Python 3 + SymPy; no network or private inputs.
Usage: python check_independent.py [path/to/public]
Writes only independent_results.json beside this script. Frozen input stays unchanged.
The stress solver uses original-coordinate monomials, not a Gale parametrization.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter, deque
from math import factorial
import hashlib, json, sys
import sympy as s
from sympy.polys.matrices import DomainMatrix

HASHES = {
 'README.md':'416539fee8d44fc749b50bbd0301077e13151cef0080e6635f06d021a853cacc',
 'RESEARCH.md':'a12e62ffb15c55e5a2eaa9001b8579bcfa32dbae8926eb2f30cd2e670bd7c8d6',
 'check_exact.py':'dde6135f60985df7a84467544bd08ef1386180e9dbbd0ff3ab2657e355bc846d',
 'exact_results.json':'ca25d8ee3df231057c556bef13f204961c053ca016990547247c7a78115fce63',
 'sources.json':'671489068c0bf8038e07cb5e8a728a02ca1a5b6a7194da722ed40efc014f9ab1',
 'status.json':'48e95508e19f111972371d232d87cea19fd9a0a09a7b9d2eaec3e9755a416660'}

def exps(n,k):
    # Alternate enumeration: weakly increasing variable-index words.
    from itertools import combinations_with_replacement
    ans=[]
    for word in combinations_with_replacement(range(n),k):
        c=Counter(word);ans.append(tuple(c[i] for i in range(n)))
    return ans

def rank(m):
    return DomainMatrix.from_Matrix(m).to_field().rank()

def cross(d):
    p=[[sign*int(i==j) for j in range(d)] for i in range(d) for sign in [-1,1]]
    f=[frozenset(2*i+z[i] for i in range(d)) for z in product(range(2),repeat=d)]
    return p,f

def cyclic(d,n):
    p=[[t**j for j in range(1,d+1)] for t in range(1,n+1)]
    facets=[]
    for f in combinations(range(n),d):
        outside=set(range(n))-set(f)
        if all(sum(a<v<b for v in f)%2==0 for a,b in combinations(sorted(outside),2)):
            facets.append(frozenset(f))
    return p,facets

def polygon_join(polys):
    total=2*len(polys)
    p=[];f=[frozenset()];offset=0
    for block,poly in enumerate(polys):
        p += [[0]*(2*block)+list(v)+[0]*(total-2*block-2) for v in poly]
        edges=[frozenset((offset+i,offset+(i+1)%len(poly))) for i in range(len(poly))]
        f=[a|b for a in f for b in edges];offset+=len(poly)
    return p,f

def support_cert(p,facets):
    n,d=len(p),len(p[0]); C=s.Matrix([[1]+list(v) for v in p])
    assert rank(C)==d+1
    assert set().union(*facets)==set(range(n))
    ridges={}
    for fi,f in enumerate(facets):
        A=C[sorted(f),:]
        # Cofactor vector rather than author nullspace supporting-plane solver.
        h=s.Matrix([(-1)**j*A[:,[q for q in range(d+1) if q!=j]].det() for j in range(d+1)])
        assert h != s.zeros(d+1,1)
        signs=[s.sign((C[i,:]*h)[0]) for i in range(n) if i not in f]
        assert signs and (all(v==1 for v in signs) or all(v==-1 for v in signs))
        for r in combinations(sorted(f),d-1): ridges.setdefault(r,[]).append(fi)
    assert all(len(v)==2 for v in ridges.values())
    adj=[set() for f in facets]
    for a,b in ridges.values():adj[a].add(b);adj[b].add(a)
    seen={0};todo=[0]
    while todo:
        for j in adj[todo.pop()]-seen:seen.add(j);todo.append(j)
    assert len(seen)==len(facets)
    faces={frozenset()}
    for f in facets:
        for j in range(1,d+1):faces.update(map(frozenset,combinations(sorted(f),j)))
    # Supporting facets, two incidences per ridge and connected polytope dual graph
    # certify exhaustiveness, including for the specified rational perturbation.
    return C.T,faces

def stress(C,faces,k):
    n=C.cols; lower=exps(n,k-1);ri={a:i for i,a in enumerate(lower)}
    mon=[a for a in exps(n,k) if frozenset(i for i,v in enumerate(a) if v) in faces]
    ent={}
    for j,a in enumerate(mon):
        for i,v in enumerate(a):
            if v:
                b=list(a);b[i]-=1;b=tuple(b)
                for row in range(C.rows):
                    val=v*C[row,i]
                    if val:ent[row*len(lower)+ri[b],j]=val
    M=s.MutableSparseMatrix(C.rows*len(lower),len(mon),ent)
    kernel=DomainMatrix.from_Matrix(M).to_field().nullspace().to_Matrix()
    assert M*kernel.T==s.zeros(M.rows,kernel.rows)
    return mon,kernel

def dranks(mon,K,k,n):
    ans=[]
    for order in (1,k-1):
        target=exps(n,k-order); ti={a:i for i,a in enumerate(target)};rows=[]
        for coeff in K.tolist():
            for alpha in exps(n,order):
                out=[0]*len(target)
                for a,c in zip(mon,coeff):
                    if c and all(u>=v for u,v in zip(a,alpha)):
                        beta=tuple(u-v for u,v in zip(a,alpha))
                        fac=1
                        for u,v in zip(a,alpha):fac*=factorial(u)//factorial(u-v)
                        out[ti[beta]]+=c*fac
                if any(out):rows.append(out)
        ans.append(rank(s.Matrix(rows)) if rows else 0)
    return ans

def check(name,p,f,k,expected):
    C,faces=support_cert(p,f);mon,K=stress(C,faces,k);n=len(p)
    ranks=dranks(mon,K,k,n)
    assert K.rows==expected['stress_dimension'],name
    assert ranks==[expected['first_derivative_rank'],expected['degree_one_derivative_rank']],name
    assert len(f)==expected['facets'],name
    missing=[]
    for size in range(2,min(n,len(p[0])+1)+1):
        for word in combinations(range(n),size):
            t=frozenset(word)
            if t not in faces and all(t-{i} in faces for i in t):missing.append(size-1)
    assert sorted(missing)==expected['missing_dimensions'],name
    if name=='three_triangles_6d':
        x=s.symbols('x:9');a,b,c=[sum(x[3*j:3*j+3]) for j in range(3)]
        F=s.Poly((a-c)*(b-c)*(a-b),*x)
        coeff=s.Matrix([[F.coeff_monomial(s.prod(x[i]**e for i,e in enumerate(m))) for m in mon]])
        assert rank(K.col_join(coeff))==1
        assert all(sum(C[r,i]*s.diff(F.as_expr(),x[i]) for i in range(n)).expand()==0 for r in range(C.rows))
        absent=[t for t in faces if len(t)==3 and F.coeff_monomial(s.prod(x[i] for i in t))==0]
        assert len(absent)==27 and sum(len(t)==3 for t in faces)==81
        assert all(len(t&frozenset(range(3*j,3*j+3)))==1 for t in absent for j in range(3))
    print(name,'PASS',flush=True)
    return dict(name=name,stress_dimension=K.rows,first_derivative_rank=ranks[0],degree_one_derivative_rank=ranks[1],facets=len(f)),C,faces

def main():
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'public'
    for f,h in HASHES.items():assert hashlib.sha256((root/f).read_bytes()).hexdigest()==h,f
    expected={c['name']:c for c in json.loads((root/'exact_results.json').read_text())['cases']}
    cases=[]
    p,f=cross(4);cases.append(('cross_4d',p,f,2))
    pert=[[100*a+s.Rational(((i+2)*(j+3))%7-3,10) for j,a in enumerate(v)] for i,v in enumerate(p)]
    cases.append(('perturbed_cross_4d',pert,f,2))
    for d,n in ((4,6),(4,8),(6,8),(6,9)):
        p,f=cyclic(d,n);cases.append((f'cyclic_{d}d_{n}',p,f,d//2))
    tri=[[1,0],[0,1],[-1,-1]]
    # Reorder square polygon cyclically, then restore author's vertex labels.
    sq=[[-1,0],[0,-1],[1,0],[0,1]]
    p,f=polygon_join([tri,sq]); perm=[0,1,2,3,5,4,6]
    # old cyclic square offsets 3,4,5,6 correspond author 3,5,4,6.
    new=[None]*7
    for i,j in enumerate(perm):new[j]=p[i]
    f=[frozenset(perm[i] for i in t) for t in f]
    cases.append(('triangle_square_4d',new,f,2))
    p,f=polygon_join([tri,[[-1,-1],[1,-1],[2,0],[1,1],[-1,1]]]);cases.append(('triangle_pentagon_4d',p,f,2))
    p,f=polygon_join([tri,tri,tri]);cases.append(('three_triangles_6d',p,f,3))
    p,f=cross(6);cases.append(('cross_6d',p,f,3))
    p,f=cross(5);cases.append(('bipyramid_cross4',p,f,2))
    p=[[0]*4]+[[int(i==j) for j in range(4)] for i in range(4)]+[[s.Rational(3,10)]*4]
    f=[frozenset(t) for t in combinations(range(5),4) if set(t)!={1,2,3,4}]
    f += [frozenset(t+(5,)) for t in combinations(range(1,5),3)]
    cases.append(('stacked_simplex_negative_control',p,f,2))
    out=[]
    for name,p,f,k in cases:out.append(check(name,p,f,k,expected[name])[0])
    p0=p;C0,_=support_cert(p0,f);p1=[v[:] for v in p0];p1[-1][0]+=s.Rational(1,100)
    C1,faces1=support_cert(p1,f);M,K=stress(C1,faces1,2);assert K.rows==0
    assert rank(C0.col_join(C1))==6
    v0=C0.nullspace()[0];v1=C1.nullspace()[0]
    a0=sorted(abs(q)/max(map(abs,v0)) for q in v0)
    a1=sorted(abs(q)/max(map(abs,v1)) for q in v1)
    assert a0!=a1 # rules out every permutation and nonzero scalar of the unique Gale vector
    # Exact quotient multiplication in basis [u^2*v], with u*v^2=-u^2*v.
    soclemat=s.Matrix([[0,1,-1],[1,-1,0]])
    assert soclemat.nullspace()==[s.ones(3,1)]
    firstfactor=s.Matrix([[0,1],[1,-1],[-1,0]])
    assert rank(firstfactor)==2
    for fn,h in HASHES.items():assert hashlib.sha256((root/fn).read_bytes()).hexdigest()==h
    result=dict(verdict='PASS: partial research only',sympy_version=s.__version__,frozen_hashes_verified=HASHES,
                independent_method='Original-coordinate face-supported monomial differential kernel; exact rational DomainMatrix',
                cases=out,three_triangle_checks=dict(top_cubic_membership=True,triangular_faces=81,inactive_triangles=27,quadratic_socle_dimension=1,degree_one_multiplication_rank=2),
                excluded_stacked_perturbation=dict(same_facets=True,both_top_stress_dimensions=0,augmented_rowspace_union_rank=6,unlabeled_affine_equivalence=False),
                limitations=['Finite examples only','No proof of unrestricted even-dimensional conjecture','No historical novelty assertion'])
    Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: 12 independent original-coordinate checks; quotient and unlabeled perturbation controls')

if __name__=='__main__':main()
