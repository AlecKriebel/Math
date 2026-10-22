#!/usr/bin/env python3
"""Independent exact finite checks for the credited Reineke proof application.

Standard library only. Explicit exceptions remain active under -O and -OO.
This is supporting evidence, not a substitute for the universal written proof.
Default checks have no writes and no network. --mutant selects a deliberate fault.
"""
from fractions import Fraction as F
from itertools import product
import argparse
import json
import sys


class CheckFailure(Exception):
    pass


COUNTS = {}
MUTANT = 'none'


def require(condition, label, **witness):
    COUNTS[label] = COUNTS.get(label, 0) + 1
    if not condition:
        raise CheckFailure(json.dumps({'failed_check': label,
            'witness': witness}, default=str, sort_keys=True))


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def euler(a, b, arrows):
    return dot(a, b) - sum(m*a[i]*b[j] for i, j, m in arrows)


def sym(a, b, arrows):
    return euler(a, b, arrows) + euler(b, a, arrows)


def skew(a, b, arrows):
    value = euler(a, b, arrows) - euler(b, a, arrows)
    return -value if MUTANT == 'reverse_skew' else value


def determinant(mat):
    a = [[F(x) for x in row] for row in mat]
    result = F(1)
    for k in range(len(a)):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            result = -result
        x = a[k][k]
        result *= x
        for i in range(k+1, len(a)):
            t = a[i][k]/x
            for j in range(k+1, len(a)):
                a[i][j] -= t*a[k][j]
    return result


def cert_lower_bound(d, w, arrows, b):
    # Explicit basis of w-perp: e_j - (w_j/w_0)e_0.
    r = len(d)
    basis = []
    for j in range(1, r):
        x = [F(0)]*r
        x[0], x[j] = -F(w[j], w[0]), F(1)
        require(dot(w, x) == 0, 'kernel_basis')
        basis.append(x)
    gram = [[sym(x, y, arrows)-b*dot(x, y) for y in basis] for x in basis]
    minors = [determinant([row[:k] for row in gram[:k]]) for k in range(1, r)]
    require(all(x > 0 for x in minors), 'exact_restricted_sylvester', minors=minors)
    return [str(x) for x in minors]


def expansion_constant(b, M):
    term = min(b, F(0))
    if MUTANT == 'negative_sign_reversed':
        term = -term
    return F(1)+term*M


def epsilon(c, delta):
    if MUTANT == 'zero_epsilon':
        return F(0)
    if MUTANT == 'gap_ignores_cutoff':
        return c/2
    return c*(1-delta)/2


def run_case(name, d, arrows, b, max_n):
    r = len(d)
    units = [tuple(int(i == j) for i in range(r)) for j in range(r)]
    w = tuple(-sym(d, z, arrows) for z in units)
    require(all(z > 0 for z in w), 'positive_denominator', w=w)
    B = dot(d, w)
    require(B == -sym(d, d, arrows) > 0, 'B_identity')
    minors = cert_lower_bound(d, w, arrows, b)
    ratios = [F(di, wi) for di, wi in zip(d, w)]
    M = min(ratios) if MUTANT == 'minimum_instead_of_maximum' else max(ratios)
    c = expansion_constant(b, M)
    require(c > 0, 'positive_constant', c=c)
    require(skew(d, d, arrows) == 0, 'central_slope_zero')
    enumerated = eligible = negative_euler = negative_rayleigh = strict = 0
    min_slack = None
    for n in range(1, max_n+1):
        D = tuple(n*z for z in d)
        repr_dim = sum(m*D[i]*D[j] for i, j, m in arrows)
        for e in product(*(range(x+1) for x in D)):
            enumerated += 1
            complement = tuple(Di-ei for Di, ei in zip(D, e))
            E = euler(e, complement, arrows)
            # Compute both independently before filtering by the Euler sign.
            grass = sum(ei*(Di-ei) for Di, ei in zip(D, e))
            codim = sum(m*e[i]*(D[j]-e[j]) for i, j, m in arrows)
            if MUTANT == 'transpose_incidence':
                codim = sum(m*e[j]*(D[i]-e[i]) for i, j, m in arrows)
            require(repr_dim+grass-codim == repr_dim+E,
                    'incidence_dimension', d=d, n=n, e=e)
            if E < 0:
                negative_euler += 1
                exclude = E > 0 if MUTANT == 'reverse_avoidance' else E < 0
                require(exclude, 'negative_euler_locus_excluded', E=E, e=e)
                require(repr_dim+E < repr_dim, 'proper_incidence_dimension')
            if e == (0,)*r or e == D:
                continue
            denominator = B if MUTANT == 'missing_n_normalization' else n*B
            eta = F(dot(w, e), denominator)
            require(0 < eta < 1, 'eta_in_open_interval', d=d, n=n, e=e, eta=eta)
            f = tuple(F(z, n) for z in e)
            if MUTANT == 'missing_f_normalization':
                f = tuple(F(z) for z in e)
            require(euler(f, tuple(di-fi for di, fi in zip(d, f)), arrows) == F(E,n*n),
                    'Euler_homogeneity', n=n, e=e)
            x = tuple(fi-eta*di for fi, di in zip(f, d))
            require(dot(w, x) == 0, 'weighted_orthogonality', n=n, e=e)
            for xi, di in zip(x, d):
                require(-eta*di <= xi <= (1-eta)*di, 'coordinate_box')
                linear = (1-2*eta)*di*xi
                if MUTANT == 'wrong_coordinate_sign':
                    linear = -linear
                require(xi*xi <= eta*(1-eta)*di*di+linear,
                        'coordinate_square', xi=xi, di=di, eta=eta)
            bound = eta*(1-eta)*B
            weighted = sum(F(wi,di)*xi*xi for wi,di,xi in zip(w,d,x))
            require(weighted <= bound, 'weighted_box')
            require(dot(x,x) <= M*bound, 'unweighted_box', d=d, n=n, e=e, M=M)
            q = sym(x,x,arrows)
            if q < 0:
                negative_rayleigh += 1
            require(q >= b*dot(x,x), 'restricted_Rayleigh')
            require(q >= min(b,F(0))*M*bound, 'uniform_Rayleigh_box')
            require(2*euler(f,tuple(di-fi for di,fi in zip(d,f)),arrows) ==
                    sym(d,f,arrows)-skew(d,f,arrows)-sym(f,f,arrows),
                    'Euler_skew_identity', d=d,n=n,e=e)
            if E < 0:
                continue
            eligible += 1
            require(skew(d,f,arrows) <= -c*bound,
                    'uniform_numerical_estimate',d=d,n=n,e=e,c=c)
            gap = -skew(d,e,arrows)/F(dot(w,e))
            require(gap == -skew(d,f,arrows)/F(dot(w,f)), 'slope_homogeneity')
            slack = gap-c*(1-eta)
            require(slack >= 0, 'uniform_slope_gap',d=d,n=n,e=e,gap=gap)
            min_slack = slack if min_slack is None else min(min_slack,slack)
            for delta in (eta,(1+eta)/2,F(1,4),F(1,2),F(3,4),F(9,10),F(99,100)):
                if eta <= delta < 1:
                    eps = epsilon(c,delta)
                    require(eps > 0, 'strict_epsilon_positive',eps=eps)
                    require(gap > eps,'strict_expansion_gap',d=d,n=n,e=e,
                            gap=gap,delta=delta,epsilon=eps)
                    strict += 1
    return {'name':name,'d':d,'arrows':arrows,'scales':[1,max_n],
            'w':w,'B':B,'M':str(M),'certified_lower_bound':str(b),'c':str(c),
            'restricted_shift_minors':minors,'enumerated':enumerated,
            'eligible':eligible,'negative_euler':negative_euler,
            'negative_Rayleigh_vectors':negative_rayleigh,
            'strict_cutoffs':strict,'minimum_gap_slack':str(min_slack)}


def structural_controls():
    # A false statement in the source's compressed spectral paragraph must not
    # be used: on v-perp individual Rayleigh quotients need not equal lambda_2.
    # Even in the source's negative-quotient branch the quotients need not
    # approach the least restricted eigenvalue individually. This regular
    # weighted graph has eigenvalues -5,-1,7,7 and Perron vector (1,1,1,1).
    # Both following w-perpendicular vectors have negative, distinct quotients.
    arrows = [(0,1,5),(0,2,1),(0,3,1),(1,2,1),(1,3,1),(2,3,5)]
    a,b = (1,1,-1,-1),(F(5,4),F(3,4),-1,-1)
    w = (5,5,5,5)
    require(dot(w,a)==dot(w,b)==0,'Rayleigh_control_orthogonal')
    qa,qb = F(sym(a,a,arrows),dot(a,a)),F(sym(b,b,arrows),dot(b,b))
    if MUTANT == 'all_Rayleigh_quotients_equal':
        require(qa == qb,'Rayleigh_quotient_variation',qa=qa,qb=qb)
    else:
        require(qa != qb and qa < 0 and qb < 0,'Rayleigh_quotient_variation',qa=qa,qb=qb)
    # Exact PF example away from the all-ones ray: 3-vertex transitive triangle
    # with edge multiplicities 6,1,6 has v=(3,4,3), lambda_1=-7.
    # C has remaining eigenvalues 3 and 10, so b(v)=3 and c=1.
    arrows_pf=[(0,1,6),(0,2,1),(1,2,6)]
    v=(3,4,3)
    require(tuple(sym(v,tuple(int(i==j) for i in range(3)),arrows_pf)
                  for j in range(3)) == tuple(-7*z for z in v),'exact_PF_eigenvector')
    # Disconnected zero extension preserves all relevant ratios, but positivity
    # on the unused component still needs an added positive denominator weight.
    d=(3,4); ar=[(0,1,3)]; e=(1,2)
    k=(6,1)
    extended_k=k+((0,) if MUTANT=='zero_offcomponent_kappa' else (7,))
    require(all(x>0 for x in extended_k),'disconnected_full_cone_positivity')
    ee=e+(0,)
    require(dot(extended_k,ee)==dot(k,e),'zero_extension_denominator')
    require(skew(d+(0,),ee,ar)==skew(d,e,ar),'zero_extension_numerator')
    # Strict vs weak distinction: a gap exactly g permits epsilon=g only for
    # <=, whereas halving a positive lower bound always supplies strictness.
    g=F(1,3)
    require(not g>g and g>g/2,'strict_boundary_control')


MUTATIONS = ['reverse_skew','negative_sign_reversed','minimum_instead_of_maximum',
    'zero_epsilon','gap_ignores_cutoff','transpose_incidence','reverse_avoidance',
    'missing_n_normalization','missing_f_normalization','wrong_coordinate_sign',
    'all_Rayleigh_quotients_equal','zero_offcomponent_kappa']


def main():
    global MUTANT
    parser=argparse.ArgumentParser()
    parser.add_argument('--mutant',choices=['none']+MUTATIONS,default='none')
    args=parser.parse_args()
    MUTANT=args.mutant
    try:
        structural_controls()
        cases=[run_case('unequal Kronecker dimension', (3,4), [(0,1,3)],F(0),6),
               run_case('negative restricted branch', (1,1,1,1),
                        [(0,1,3),(1,2,1),(2,3,3)],F(-3,4),6),
               run_case('unequal negative branch', (2,3,3,2),
                        [(0,1,3),(1,2,1),(2,3,3)],F(-3,4),3),
               run_case('nonconstant integral PF vector', (3,4,3),
                        [(0,1,6),(0,2,1),(1,2,6)],F(0),4)]
    except CheckFailure as exc:
        print(json.dumps({'status':'REJECT','mutant':MUTANT,'failure':json.loads(str(exc)),
                          'checks_before_rejection':sum(COUNTS.values())},sort_keys=True))
        return 1
    print(json.dumps({'status':'PASS','mutant':MUTANT,'method':'exact Fraction arithmetic; explicit failures',
                      'cases':cases,'checks':COUNTS,'total_checks':sum(COUNTS.values()),
                      'scope':'finite support checks; universal proof separately audited'},indent=2,sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
