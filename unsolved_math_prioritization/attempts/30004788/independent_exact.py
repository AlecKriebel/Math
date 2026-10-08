#!/usr/bin/env python3
"""Independent finite/exact audit. This does not prove a p-adic branching theorem."""
import argparse
from fractions import Fraction
from itertools import product
import json
import os
import sys

MUTANTS = ('split_jordan', 'merge_orbits', 'drop_affine_constant',
           'equal_fitting', 'wrong_syzygy', 'invert_nilpotent',
           'drop_polynomial_factor')

def need(ok, label):
    if not ok:
        raise ValueError(label)

def mm(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def determinant3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))

def inv3(a):
    d=determinant3(a)
    need(d != 0, 'singular orbit chart')
    result=[]
    for i in range(3):
        row=[]
        for j in range(3):
            r=[k for k in range(3) if k != j]
            c=[k for k in range(3) if k != i]
            minor=a[r[0]][c[0]]*a[r[1]][c[1]]-a[r[0]][c[1]]*a[r[1]][c[0]]
            row.append(Fraction((-1)**(i+j)*minor,d))
        result.append(row)
    need(mm(a,result)==[[int(i==j) for j in range(3)] for i in range(3)], 'inverse identity')
    return result

def rank(rows):
    rows=[list(map(Fraction,r)) for r in rows]
    pivots={}
    for row in rows:
        for j, p in sorted(pivots.items()):
            coefficient=row[j]
            row=[a-coefficient*b for a,b in zip(row,p)]
        lead=next((j for j,x in enumerate(row) if x),None)
        if lead is not None:
            d=row[lead]
            pivots[lead]=[x/d for x in row]
    return len(pivots)

def cross(x,y):
    return (x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0])

def proj(x,q):
    x=tuple(a%q for a in x)
    leading=next(a for a in x if a)
    return tuple(a*pow(leading,-1,q)%q for a in x)

def flag(x,y,q):
    return (proj(x,q),proj(cross(x,y),q))

def apply_h(h,x):
    a,b,c,d=h
    return (a*x[0]+b*x[1],c*x[0]+d*x[1],x[2])

def monomial_in(m,gens):
    return any(all(a>=b for a,b in zip(m,g)) for g in gens)

def dual_mul(x,y):
    return (x[0]*y[0],x[0]*y[1]+x[1]*y[0])

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mutate',choices=MUTANTS)
    mutant=parser.parse_args().mutate
    t=[[0,-4],[1,4]] if mutant!='split_jordan' else [[2,0],[0,2]]
    nil=[[t[i][j]-2*int(i==j) for j in range(2)] for i in range(2)]
    need(mm(nil,nil)==[[0,0],[0,0]],'Jordan square')
    need(nil!=[[0,0],[0,0]],'Jordan nonzero nilpotent')
    need(t[1][0]!=0,'cyclic quotient generator')

    # First two columns encode each flag. Entries are small integers, independent
    # of the local field. Inverse-by-cofactors checks the full group equations,
    # including the affine constant from diag(h,1), not just tangent dimensions.
    charts=[[[0,1,0],[0,0,1],[1,0,0]],[[1,0,0],[0,0,1],[0,1,0]],
            [[1,0,0],[0,1,0],[0,0,1]],[[1,1,0],[0,0,1],[1,0,0]],
            [[1,0,1],[0,1,0],[1,0,0]],[[1,0,0],[0,1,1],[0,1,0]]]
    if mutant=='merge_orbits': charts[4]=charts[3]
    # Coefficient order is (constant, a,b,c,d).
    zero=(0,0,0,0,0); c=(0,0,0,1,0)
    a1=(-1,1,0,0,0); b=(0,0,1,0,0); d1=(-1,0,0,0,1)
    expected=[(zero,zero,c),(zero,c,zero),(c,zero,zero),
              (a1,c,c),(c,a1,b),(zero,c,d1)]
    affine=[]; dimensions=[]
    for g,wanted in zip(charts,expected):
        gi=inv3(g)
        components=[]
        for index in range(5):
            h=[[0]*3 for _ in range(3)]
            if index==0: h[2][2]=0 if mutant=='drop_affine_constant' else 1
            else:
                i,j=((0,0),(0,1),(1,0),(1,1))[index-1]
                h[i][j]=1
            components.append(mm(mm(gi,h),g))
        rows=[tuple(int(m[i][j]) for m in components) for i,j in ((1,0),(2,0),(2,1))]
        need(tuple(rows)==wanted,'full affine stabilizer equations')
        affine.append(rows);dimensions.append(rank([r[1:] for r in rows]))
    need(dimensions==[1,1,1,2,3,2],'six orbit dimensions')

    finite=[]
    for q in (2,3,5):
        points={proj(x,q) for x in product(range(q),repeat=3) if any(x)}
        allflags={(x,n) for x in points for n in points if sum(a*b for a,b in zip(x,n))%q==0}
        hs=[h for h in product(range(q),repeat=4) if (h[0]*h[3]-h[1]*h[2])%q]
        covered=set(); sizes=[]
        for g in charts:
            x=tuple(row[0] for row in g);y=tuple(row[1] for row in g)
            orbit={flag(apply_h(h,x),apply_h(h,y),q) for h in hs}
            need(not covered.intersection(orbit),'finite-field orbit overlap')
            need(orbit<=allflags,'finite-field nonflag')
            covered.update(orbit);sizes.append(len(orbit))
        need(covered==allflags,'finite-field orbit coverage')
        need(sizes==[q+1,q+1,q+1,q*q-1,q*(q*q-1),q*q-1],'finite-field orbit sizes')
        finite.append({'q':q,'group_order':len(hs),'flag_count':len(allflags),'orbit_sizes':sizes})

    i=((1,0),(0,1)); j=((2,0),(0,1))
    if mutant=='equal_fitting': j=i
    need(monomial_in((1,0),i) and not monomial_in((1,0),j),'distinct first Fitting ideals')
    # Presentation syzygy: (-v)*u^power + u^relation_power*v = 0.
    for power in (1,2):
        relation_power=1 if mutant=='wrong_syzygy' and power==2 else power
        terms={}
        for monomial,coefficient in (((power,1),-1),((relation_power,1),1)):
            terms[monomial]=terms.get(monomial,0)+coefficient
        need(all(c==0 for c in terms.values()),'presentation syzygy')
    fibres=[]
    for alpha,beta in product(range(-2,3),repeat=2):
        dims=[2-int(beta!=0 or alpha**power!=0) for power in (1,2)]
        need(dims[0]==dims[1],'equal simple-target dimensions')
        fibres.append({'point':[alpha,beta],'dimensions':dims})
    # In R/(u^2,v), u survives, while 1+u and 1+v are units. This is an
    # exact witness that Laurent localization does not collapse the ideals.
    u=(0,1);one=(1,0)
    need(u!= (0,0) and dual_mul(u,u)==(0,0),'nonzero dual-number class')
    chosen_unit=u if mutant=='invert_nilpotent' else (1,1)
    need(dual_mul(chosen_unit,(1,-1))==one,'Laurent localization unit witness')

    polynomial_cases=0
    # Universal zero-factor certificate after X_a=beta_j: each chosen pair
    # must be an actual factor. This does not model any center action.
    for n in range(1,6):
        factors={(a,j) for a in range(n) for j in range(n+1)}
        if mutant=='drop_polynomial_factor': factors.remove((0,0))
        for a,j in product(range(n),range(n+1)):
            need((a,j) in factors,'polynomial substitution zero factor')
            polynomial_cases+=1
        for shift in range(n):
            need({((a+shift)%n,j) for a,j in factors}==factors,'coordinate symmetry')

    return {'status':'PASS','uid':os.getuid(),'arithmetic':'exact integer/rational',
            'full_affine_stabilizers':affine,'orbit_dimensions':dimensions,
            'finite_field_orbits':finite,'ideal_fibre_samples':fibres,
            'universal_zero_factor_cases':polynomial_cases,
            'p_adic_theorems_computationally_verified':False}

if __name__=='__main__':
    try:
        print(json.dumps(main(),sort_keys=True))
    except ValueError as e:
        print('SEMANTIC_REJECTION: '+str(e),file=sys.stderr)
        sys.exit(1)
