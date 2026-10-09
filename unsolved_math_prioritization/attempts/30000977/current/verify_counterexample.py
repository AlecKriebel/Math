#!/usr/bin/env python3
"""Exact finite checks for the GPR canonical-degree-12 example.

This checks its finite algebra, NOT existence, singularity classification,
finite duality, ampleness, or the geometric proof. See PROOF_AUDIT.md.
No third-party program or source file is read.
"""
from fractions import Fraction
from itertools import product
import argparse
import json

E = [(1,1,2),(2,2,0),(1,2,1),(2,1,0)]
F = [(2,1,1),(0,1,2),(1,2,1),(0,2,2)]
ACTIVE = [(0,1,0),(1,0,1),(0,2,0),(2,2,2)]
DIVISORS = [
    (1,0,0,1,1,1,0,0),
    (2,0,0,0,2,0,0,0),
    (0,1,1,0,0,0,1,1),
    (0,0,0,2,0,2,0,0),
]
EXPECTED_DEGREES = [
    (0,0),(1,2),(1,2),(2,2),(1,1),(2,1),(2,2),(2,1),(1,1),
    (2,1),(2,2),(2,1),(1,1),(1,1),(1,2),(1,2),(1,1),(1,1),
    (2,1),(1,2),(1,1),(1,2),(2,1),(1,1),(1,1),(1,1),(2,2),
]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def dot(a,b):
    return sum(x*y for x,y in zip(a,b)) % 3

def span(vectors):
    return {tuple(sum(c*v[j] for c,v in zip(coeff,vectors)) % 3
                  for j in range(3))
            for coeff in product(range(3), repeat=len(vectors))}

def verify(mutation=None):
    e, f = list(E), list(F)
    group_rank, characteristic = 3, 0
    relation = (1,3)
    canonical_characters = list(ACTIVE)
    if mutation == 'bad_group': group_rank = 2
    if mutation == 'bad_relation': relation = (1,2)
    if mutation == 'missing_section': canonical_characters.remove((0,2,0))
    if mutation == 'bad_branch': f[2] = (2,1,2)
    if mutation == 'bad_characteristic': characteristic = 3
    require(characteristic == 0, 'The audited statement is characteristic zero.')
    require(group_rank == 3, 'The given monodromies require rank-three G, of order 27.')
    for label, vectors in [('E',e),('F',f)]:
        require(len(vectors)==4 and all(len(v)==3 for v in vectors), 'Bad branch dimensions.')
        require(all(all(isinstance(a,int) and a in range(3) for a in v) for v in vectors), 'Bad residues.')
        require(all(sum(v[j] for v in vectors)%3==0 for j in range(3)), label+' tuple is not spherical.')
        require(len(span(vectors))==27, label+' monodromies do not span G.')
    dependent = [(i,j,k) for i,a in enumerate(e) for j,b in enumerate(f)
                 for k in (1,2) if tuple(k*x%3 for x in a)==b]
    require(dependent==[(2,2,1)], 'Unexpected common inertia or tangent character.')
    rows=[]
    actual_active={}
    for c in product(range(3),repeat=3):
        er,fr = [dot(c,v) for v in e],[dot(c,v) for v in f]
        require(sum(er)%3==sum(fr)%3==0, 'Non-integral eigenbundle degree.')
        de,df=sum(er)//3,sum(fr)//3
        h=max(de-1,0)*max(df-1,0)
        rows.append((de,df))
        if h:
            actual_active[c]=(h,tuple(2-a for a in er+fr))
    require(rows==EXPECTED_DEGREES, 'The 27-character table changed.')
    require(set(actual_active)==set(canonical_characters), 'The chosen sections are not the complete canonical basis.')
    require(sum(h for h,d in actual_active.values())==4, 'Geometric genus is not four.')
    require(all(actual_active[c]==(1,d) for c,d in zip(ACTIVE,DIVISORS)), 'Canonical divisors differ.')
    for i,j in product(range(-1,4),repeat=2):
        zeros=[(i>=0 and d[i]>0) or (j>=0 and d[4+j]>0) for d in DIVISORS]
        require(not all(zeros), 'Canonical base point at a branch stratum.')
    left=tuple(2*x for x in DIVISORS[0])
    right=tuple(x+y for x,y in zip(DIVISORS[relation[0]],DIVISORS[relation[1]]))
    require(left==right, 'The proposed quadric relation has unequal divisors.')
    require(left!=tuple(x+y for x,y in zip(DIVISORS[1],DIVISORS[2])), 'Wrong printed relation was not detected.')
    degree=3**group_rank
    twice_genus_minus_two=degree*(-2+4*Fraction(2,3))
    genus=1+twice_genus_minus_two/2
    k2=degree*2*Fraction(2,3)**2
    require(genus==10 and k2==24 and k2/2==12, 'Unexpected invariants.')
    singularities=(degree//3)**2//(degree//3)
    require(singularities==9, 'Unexpected singular point orbit count.')
    return {'status':'PASS_FINITE_CHECKS_ONLY','cover_degree':degree,'curve_genus':int(genus),
            'canonical_degree':int(k2/2),'K_squared':int(k2),'p_g':4,
            'A2_points':singularities,'character_rows':27,'branch_strata_checked':25,
            'correct_relation':'2A=B+D; x0^2=x1*x3',
            'geometric_dependencies':'See PROOF_AUDIT.md; not established by this program.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--mutate', choices=['bad_group','bad_relation','missing_section','bad_branch','bad_characteristic'])
    args=parser.parse_args()
    try:
        print(json.dumps(verify(args.mutate),sort_keys=True))
    except ValueError as exc:
        print('GUARD_FAILURE: '+str(exc))
        raise SystemExit(2)
