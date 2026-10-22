#!/usr/bin/env python3
"""Exact diagnostic controls. This is not a general sheaf-cohomology solver."""
from fractions import Fraction
from itertools import combinations, product
from math import comb
import hashlib, json
from pathlib import Path

CHECKS = 0

def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ValueError(message)


def rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    if not a:
        return 0
    m, n, r = len(a), len(a[0]), 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][c]
        a[r] = [v / q for v in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [x - q * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r


def monomials(degree, variables=4):
    if variables == 1:
        yield (degree,)
    else:
        for a in range(degree + 1):
            for rest in monomials(degree - a, variables - 1):
                yield (a,) + rest


def jacobian_monomial(n, exponent):
    return any(a >= n - 1 for a in exponent)


def check_fermat_witness(n, exponent):
    require(n >= 4, 'witness requires n >= 4')
    require(sum(exponent) == n and min(exponent) >= 0, 'wrong homogeneous degree')
    require(not jacobian_monomial(n, exponent), 'Jacobian-trivial direction')


MONODROMY = {
    '13': (0,0,0,0,1), '14': (1,0,0,0,0), '23': (0,0,0,1,0),
    '24': (0,1,0,0,0), '34': (0,0,1,0,0), '12': (-1,-1,-1,-1,-1),
    '45': (-1,-1,-1,0,0), '15': (0,1,1,1,0),
    '25': (1,0,1,0,1), '35': (0,0,-1,-1,-1),
}
DIVISORS = {}
for i,j in combinations(range(1,6),2):
    d = [0]*5
    if j == 5:
        d[i] = 1
    else:
        d[0] = 1
        for h in set(range(1,5)) - {i,j}:
            d[h] = -1
    DIVISORS[str(i)+str(j)] = tuple(d)
LABELS = sorted(DIVISORS)
K = (-3,1,1,1,1)


def character_type(n, character):
    residues = {k: sum(x*y for x,y in zip(character,MONODROMY[k])) % n for k in LABELS}
    numerator = tuple(sum(residues[k]*DIVISORS[k][q] for k in LABELS) for q in range(5))
    require(all(v % n == 0 for v in numerator), 'nonintegral character divisor')
    ell = tuple(v//n for v in numerator)
    selected = tuple(k for k in LABELS if residues[k] != n-1)
    return ell, selected, residues


def reject(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    raise ValueError('negative control was accepted')


def main():
    frame = [(1,0,0),(0,1,0),(0,0,1),(1,1,1)]
    require(all(rank(triple)==3 for triple in combinations(frame,3)), 'not a dual projective frame')
    bad_frame = frame[:3]+[(1,1,0)]
    require(any(rank(triple)<3 for triple in combinations(bad_frame,3)), 'concurrent-line control missed')
    fermat = []
    for n in range(4,41):
        witness = (n-2,2,0,0)
        check_fermat_witness(n,witness)
        total = 0
        trivial = 0
        for e in monomials(n):
            total += 1
            trivial += int(jacobian_monomial(n,e))
        require(total==comb(n+3,3), 'monomial enumeration wrong')
        require(trivial==16, 'wrong degree-n Jacobian span')
        require(total-trivial==comb(n+3,3)-16, 'wrong nontrivial embedded KS dimension')
        require(n**n > 4*(n-2)**(n-2), 'unit disk smoothness bound failed')
        fermat.append({'n':n,'embedded_ks_image_dimension':total-trivial})
    require(reject(check_fermat_witness,4,(3,1,0,0)), 'trivial witness not rejected')
    require(reject(check_fermat_witness,4,(2,1,0,0)), 'wrong degree not rejected')
    require(reject(check_fermat_witness,3,(1,2,0,0)), 'wrong exponent not rejected')
    ell,selected,residues=character_type(3,(2,2,2,1,1))
    require(ell==(3,-1,-1,-1,-1), 'wrong n=3 character divisor')
    require(tuple(a+b for a,b in zip(K,ell))==(0,0,0,0,0), 'K+L not zero')
    require(selected==('12','13','23','45'), 'wrong logarithmic selection')
    require(rank([DIVISORS[k] for k in selected])==4, 'wrong residue-Chern-class rank')
    require(rank(list(DIVISORS.values()))==5, 'Picard rank control failed')
    wrong_ell,wrong_selected,_=character_type(3,(2,2,2,1,0))
    require((wrong_ell,wrong_selected)!=(ell,selected), 'mutated character not distinguished')
    bounds=tuple(sum(abs(DIVISORS[k][q]) for k in LABELS) for q in range(5))
    census=[]
    digest=hashlib.sha256()
    for n in range(2,11):
        types=set()
        count=0
        for a in product(range(n),repeat=5):
            L,J,res=character_type(n,a)
            require(all(abs(v)<=b for v,b in zip(L,bounds)), 'finite-class bound failed')
            for k in LABELS:
                linear=sum(x*y for x,y in zip(a,MONODROMY[k]))
                carry=(linear-res[k])//n
                require(linear==n*carry+res[k], 'carry identity failed')
                require(abs(carry)<=1+sum(abs(x) for x in MONODROMY[k]), 'carry bound failed')
            types.add((L,J)); count+=1
        require(count==n**5,'incomplete character enumeration')
        serialized=json.dumps(sorted(types),separators=(',',':')).encode()
        digest.update(str(n).encode()+b':'+serialized+b'\n')
        census.append({'n':n,'characters':count,'different_sheaf_types':len(types)})
    result={
        'status':'PASS_EXACT_CONTROLS', 'checks':CHECKS,
        'fermat':fermat, 'cq_exponent3':{'character':[2,2,2,1,1],'line_bundle':ell,
        'selected_divisors':selected,'residue_matrix_rank':4,'proved_selected_eigenspace_dimension':1},
        'character_census':census,'census_sha256':digest.hexdigest(),
        'negative_controls':5,
        'limits':['No general cohomology solver','No all-n proof inferred from the census',
                  'No intended-arrangement rigidity resolution','No formal proof-assistant certification']}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
