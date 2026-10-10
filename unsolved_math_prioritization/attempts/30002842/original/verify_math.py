#!/usr/bin/env python3
"""Exact finite checks of the report's algebra; not a VOA theorem prover."""
import argparse
from fractions import Fraction as F
import json
from math import factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rank(rows, columns):
    a = [[F(x) for x in row] for row in rows]
    require(all(len(row) == columns for row in a), 'matrix row width mismatch')
    r = 0
    for c in range(columns):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = a[r][c]
        a[r] = [x/z for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                z = a[i][c]
                a[i] = [x-z*y for x,y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def derivation_dimension(c):
    """c[i][j][k] is the k coefficient in basis_i * basis_j."""
    n = len(c)
    require(n > 0 and all(len(x)==n for x in c), 'bad algebra dimensions')
    require(all(len(v)==n for x in c for v in x), 'bad structure vector')
    equations = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                row = [F(0)]*(n*n)
                # D(e_i e_j) - D(e_i)e_j - e_i D(e_j)
                for a in range(n):
                    row[k*n+a] += c[i][j][a]
                    row[a*n+i] -= c[a][j][k]
                    row[a*n+j] -= c[i][a][k]
                equations.append(row)
    return n*n-rank(equations,n*n)


def coordinate_algebra(n):
    c = [[[F(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        c[i][i][i] = F(1)
    return c


def spin_algebra(s):
    n=s+1
    c = [[[F(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        c[0][i][i] = c[i][0][i] = F(1)
    for i in range(1,n):
        c[i][i][0] = F(1)
    return c


def mul_poly(a,b):
    z=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            z[i+j]+=x*y
    return z


def evaluate(a,x):
    y=F(0)
    for t in reversed(a):
        y=y*x+t
    return y


def coefficients(N, primary_weight):
    r=N-primary_weight
    require(r>=0 and primary_weight>=1,'invalid descendant weight')
    rising=1
    for j in range(r):
        rising*=primary_weight+j
    normalization=F((-1)**r,rising)
    zero_mode_factor=(-1)**r*rising
    return normalization,zero_mode_factor


def verify(claims):
    expected_scope={
        'problem_id':30002842,
        'problem_number':'OWR-13673-012',
        'queue_rank':991,
        'status':'unsolved_partial',
        'author_approaches_completed':5,
        'full_conjecture_proved':False,
        'conjecture_disproved':False,
        'han_v5_verified_as_resolution':False,
        'affine_escape_has_weight_one_zero':False,
        'finite_checks_prove_general_voa_theorem':False,
        'novelty_claimed':False,
    }
    require(set(claims)==set(expected_scope)|{'mathematical_checks'},'claim key inventory mismatch')
    for key,value in expected_scope.items():
        require(type(claims[key]) is type(value) and claims[key]==value,'scope mismatch: '+key)
    m=claims['mathematical_checks']
    expected_keys={'cartan_charge','escape_tail_limit','hat_sign','spectral_sign',
                   'coordinate_derivation_dimensions','spin_derivation_dimensions',
                   'central_charges','tensor_automorphism_order','tested_descendant_max_weight'}
    require(set(m)==expected_keys,'mathematical claim key inventory mismatch')
    require(m['cartan_charge']==2,'Cartan/root charge must be 2')
    require(m['escape_tail_limit']==2,'escaping tail on e remains 2e, not zero')
    require(m['hat_sign']==-1,'tail lift requires the negative sign')
    require(m['spectral_sign']==-1,'double commutator has negative eigenvalue')
    require(type(m['tested_descendant_max_weight']) is int and m['tested_descendant_max_weight']==50,
            'descendant test range changed')
    for k in [1,2,3,7]:
        for N in range(k,51):
            a,z=coefficients(N,k)
            require(a*z==1,'normalized zero-mode identity failed')
    for N in range(2,51):
        a,z=coefficients(N,1)
        prev,_=coefficients(N-1,1)
        next_a,_=coefficients(N+1,1)
        require(a*F((N-1)*N)/prev==-N,'L(1) descendant coefficient failed')
        require(F(m['hat_sign'],N)*a==next_a,'displayed hat transformation failed')
        require(a*z*m['cartan_charge']==m['escape_tail_limit'],'nonvanishing tail failed')
        # N=n+2: b_n=c_N; hat b_n=c_(N+1). Every removal target is already zero.
        n=N-2
        support={N+1:next_a}
        require(N>=n+2 and 1 not in support,'sequence hypothesis failed')
        require(all(j not in support for j in range(2,N)),'low-degree removal not vacuous')
        require(next_a*coefficients(N+1,1)[1]*2==2,'hat tail action changed')
    coord=[derivation_dimension(coordinate_algebra(n)) for n in range(1,6)]
    spin=[derivation_dimension(spin_algebra(s)) for s in range(2,6)]
    require(coord==[0]*5,'coordinate algebra has unexpected derivations')
    require(coord==m['coordinate_derivation_dimensions'],'coordinate dimension claim false')
    require(spin==[s*(s-1)//2 for s in range(2,6)],'spin-factor exact rank mismatch')
    require(spin==m['spin_derivation_dimensions'],'spin dimension claim false')
    for J in [[],[2],[2,3],[3,7,11],list(range(2,15))]:
        p=[F(1)]
        for i in J:
            p=mul_poly(p,[F(1),F(1,i*(i-1))])
        require(evaluate(p,F(0))==1,'spectral filter constant term failed')
        for i in J:
            eig=m['spectral_sign']*i*(i-1)
            require(evaluate(p,F(eig))==0,'spectral filter did not annihilate a weight')
        lambdas=[F(i*(i-1)) for i in J]
        moments=[[x**r for x in lambdas] for r in range(1,len(J)+1)]
        require(rank(moments,len(J))==len(J),'nonzero weight spectral separation failed')
    charges=[F(x) for x in m['central_charges']]
    require(charges==[F(1,2),F(7,10),F(1,2)],'central-charge fixture changed')
    order=1
    for c in set(charges):
        order*=factorial(charges.count(c))
    require(order==m['tensor_automorphism_order']==2,'unequal central charges cannot be permuted')
    return {'descendant_max_weight':50,'coordinate_derivation_dimensions':coord,
            'spin_derivation_dimensions':spin,'tensor_automorphism_order':order,
            'scope':'finite exact checks only; general conjecture not proved'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--claims',type=Path,default=Path(__file__).with_name('CLAIMS.json'))
    args=parser.parse_args()
    claims=json.loads(args.claims.read_text())
    print(json.dumps({'ok':True,'results':verify(claims)},sort_keys=True))


if __name__=='__main__':
    main()
