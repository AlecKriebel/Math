#!/usr/bin/env python3
"""Read-only exact finite validation of authored theta partial results.

The oracle enumerates ordered heat-operator words with coefficient 1/d!,
independently of the original multiset/factorial implementation. All comparisons
remain active under -O and -OO. It prints JSON and never writes files.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import product
from math import factorial
import argparse
import json
import os
import sympy as s


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def jets(g, mutation=None):
    a, b, c = s.symbols('a b c')
    y = s.symbols('y4:' + str(g + 1))
    alpha = s.symbols('alpha1:4')
    beta = s.symbols('beta4:' + str(g + 1))
    gamma = s.symbols('gamma4:' + str(g + 1))
    variables = (a, b, c) + y
    edges = [(0,1,0), (0,2,1), (1,2,2)]
    edges += [(i,j,j) for j in range(3,g) for i in range(3)]
    entries = [defaultdict(Fraction) for _ in range(g)]
    for d in range(4):
        for word in product(range(len(edges)), repeat=d):
            orders0 = [0]*g
            exponents = [0]*len(variables)
            for e in word:
                u,v,k = edges[e]
                orders0[u] += 1
                orders0[v] += 1
                exponents[k] += 1
            # Ordered D^d expansion uses 1/d!. Multiplying by the factorials
            # of repeated edges exactly emulates removing multiset factorials.
            weight = Fraction(1,factorial(d))
            if mutation == 'remove_factorials':
                for e in set(word):
                    weight *= factorial(word.count(e))
            if mutation == 'wrong_heat_scale':
                weight *= 2**d
            for out in range(g):
                orders = orders0.copy()
                orders[out] += 1
                if any(n % 2 != int(i < 3) for i,n in enumerate(orders)):
                    continue
                moments = [0]*(3+2*(g-3))
                for i,n in enumerate(orders):
                    if i < 3:
                        require(n in (1,3), 'Odd moment range')
                        if n == 3:
                            moments[i] += 1
                    else:
                        require(n in (0,2,4), 'Even moment range')
                        if n == 2:
                            moments[i] += 1
                        elif n == 4:
                            moments[g+i-3] += 1
                entries[out][tuple(exponents)+tuple(moments)] += weight
    symbols = variables + alpha + beta + gamma
    F = []
    for entry in entries:
        F.append(s.Add(*(s.Rational(v.numerator,v.denominator)*s.prod(x**n for x,n in zip(symbols,k)) for k,v in entry.items())))
    return F, variables, alpha, beta, gamma


def truncate(expr, variables, degree):
    return s.Add(*(coeff*s.prod(v**n for v,n in zip(variables,powers))
                   for powers,coeff in s.Poly(s.expand(expr),*variables).terms()
                   if sum(powers) <= degree))


def check_genus(g, mutation):
    F, variables, alpha, beta, gamma = jets(g,mutation)
    a,b,c,*ys = variables
    y = tuple(ys)
    S = sum(t*v*v for t,v in zip(beta,y))
    A,B,C = alpha
    total = A+B+C
    E = [c+A*a*b+S+B*C*c**3/6+A*B*a*a*c/2+A*C*b*b*c/2+S*(A*(a+b)+total*c/2),
         b+B*a*c+S+A*C*b**3/6+A*B*a*a*b/2+B*C*c*c*b/2+S*(B*(a+c)+total*b/2),
         a+C*b*c+S+A*B*a**3/6+A*C*a*b*b/2+B*C*a*c*c/2+S*(C*(b+c)+total*a/2)]
    for j,v in enumerate(y):
        cross = sum(beta[k]*y[k]**2 for k in range(len(y)) if k != j)
        multiplier = 2 if mutation == 'wrong_cross_multiplicity' else 3
        E.append(beta[j]*v*(a+b+c+A*a*b+B*a*c+C*b*c)+gamma[j]*v**3+multiplier*beta[j]*v*cross)
    for i in range(g):
        require(s.expand(F[i]-E[i]) == 0, f'g={g}: full cubic jet {i+1}')
    for j,v in enumerate(y):
        sign = 1 if mutation == 'wrong_elimination_sign' else -1
        reduced = truncate(F[j+3].subs({a:sign*S,b:sign*S,c:sign*S}),y,3)
        coefficient = 2 if mutation == 'wrong_residual_coefficient' else 3
        require(s.expand(reduced-(gamma[j]-coefficient*beta[j]**2)*v**3)==0,
                f'g={g}: reduced jet {j+4}')
    return {'g':g,'full_cubic_equations':g,'reduced_equations':g-3,'status':'PASS'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mutation',choices=['remove_factorials','wrong_heat_scale','wrong_cross_multiplicity','wrong_elimination_sign','wrong_residual_coefficient','wrong_fourier_lead'])
    args = parser.parse_args()
    cases = [check_genus(g,args.mutation) for g in range(3,9)]
    q = s.symbols('q')
    T0 = 1 + sum(2*q**(n*n) for n in range(1,4))
    T2 = sum(-8*s.pi**2*n*n*q**(n*n) for n in range(1,4))
    T4 = sum(32*s.pi**4*n**4*q**(n*n) for n in range(1,4))
    cj = s.series(T4/T0-3*(T2/T0)**2,q,0,3).removeO()
    lead = 16 if args.mutation == 'wrong_fourier_lead' else 32
    require(s.expand(cj-(lead*q-256*q*q)*s.pi**4)==0,'Elliptic Fourier coefficient')
    g=s.symbols('g',integer=True)
    r=(g-3)*(g-4)/2+2*(g-3)
    require(s.simplify(g+r-(g*(g+1)/2-g))==0,'Slice dimension identity')
    require(s.simplify(g*(g+1)/2-(3*g-6)-g-(g-3)*(g-4)/2)==0,'Spin dimension identity')
    u,v=s.symbols('u v')
    J=s.Matrix([[s.diff(p,w) for w in (u,v)] for p in (u,u*v)])
    require(J.det()==u,'Algebraic-independence counterexample Jacobian')
    G=s.groebner([u,u*v],u,v)
    require([p.as_expr() for p in G.polys]==[u],'Counterexample ideal has height one')
    # The points in question have cubic z1*z2*z3; the flattening has rank 3.
    ranks=[]
    for n in range(3,9):
        z=s.symbols('z0:'+str(n))
        for polynomial,expected,label in [(z[0]*z[1]*z[2],3,'diagonal'),(z[0]*sum(w*w for w in z[1:]),n,'product')]:
            M=s.Matrix([[s.diff(polynomial,z[i],z[j],z[k]) for j in range(n) for k in range(j,n)] for i in range(n)])
            require(M.rank()==expected,f'{label} cubic rank g={n}')
        ranks.append({'g':n,'diagonal':3,'nondegenerate_product':n})
    print(json.dumps({'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),
                      'jet_cases':cases,'fourier_coefficient':'32*pi^4*q - 256*pi^4*q^2 + O(q^3)',
                      'full_cubic_includes_repeated_edge_factorials':True,'cubic_ranks':ranks,
                      'counterexample_ideal':'(u,uv)=(u)','scope':'Finite exact sanity checks, not a global proof.'},indent=2))


if __name__=='__main__':
    main()
