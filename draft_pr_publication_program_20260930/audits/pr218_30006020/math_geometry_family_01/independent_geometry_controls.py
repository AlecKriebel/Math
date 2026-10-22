#!/usr/bin/env python3
"""Finite independent exact controls; no frozen verifier imported or executed.

The direct genus-zero vertex construction uses <tau_d>_{0,N}=(N-3)!/prod d!.
It does not use the manuscript's F expansion. All arithmetic below is rational.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import comb, factorial, floor, log
from pathlib import Path
import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def weak(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in weak(total-first, length-1):
                yield (first,)+rest


def positive(total, length):
    for v in weak(total-length, length):
        yield tuple(x+1 for x in v)


def raw_vertex(k):
    """F for the one-vertex graph of global genus g=k, vertex genus zero."""
    degree = 2*k-3
    coefficients = defaultdict(Q)
    terms = 0
    for d in weak(degree, 2*k):
        # Independent direct V_{0,2k}, with each loop variable at two half-edges.
        dfact = 1
        for x in d:
            dfact *= factorial(x)
        intersection = Q(factorial(degree), dfact)
        coefficient = intersection / (2**degree * dfact)
        j = tuple(d[2*i]+d[2*i+1]+1 for i in range(k))
        coefficients[j] += coefficient
        terms += 1
    return dict(coefficients), terms


def claimed_ctilde_zero(k, j):
    # DL c_{0,k}, reduced with Vandermonde, independently from half-edge enumeration.
    v = Q(factorial(2*k-3)**2, factorial(4*k-5)*2**(5*k-6))
    for x in j:
        d = x-1
        v *= factorial(2*x)*Q(comb(2*d,d), factorial(d)**2)
    return v


def beta_integral(j):
    v = Q(1, factorial(2*sum(j)-1))
    for x in j:
        v *= factorial(2*x-1)
    return v


def simplex_integral(exponents):
    v = Q(1, factorial(sum(exponents)+len(exponents)-1))
    for e in exponents:
        v *= factorial(e)
    return v


def integrated_height_mass(F, heights):
    mass = Q(0)
    for j, coefficient in F.items():
        term = coefficient*beta_integral(j)
        for x, m in zip(j, heights):
            term /= m**(2*x)
        mass += term
    return mass


def checks():
    rows = []
    for k in range(2,6):
        n = 3*k-3
        F, terms = raw_vertex(k)
        assert set(F) == set(positive(n,k))
        A = Q(factorial(4*k-5)*2**(3*k-3), factorial(2*k-3))
        for j, actual in F.items():
            rhs = A*claimed_ctilde_zero(k,j)
            for x in j:
                rhs /= factorial(2*x)
            assert rhs == actual
            # Exact conditional Dirichlet normalizer and first/second identities.
            integrated = beta_integral(j)
            assert integrated > 0
            base = tuple(2*x-1 for x in j)
            assert simplex_integral(base) == integrated
            def moment(selected):
                exponent = list(base)
                for i in selected:
                    exponent[i] += 1
                return simplex_integral(exponent)/integrated
            expected_sum = sum(moment((i,)) for i in range(k))
            for i in range(k):
                assert moment((i,)) == Q(j[i],n)
                assert moment((i,i)) == Q(2*j[i]*(2*j[i]+1),2*n*(2*n+1))
            expected_square_sum = sum(moment((i,i)) for i in range(k))
            expected_cross = sum(moment((i,l))
                                 for i in range(k) for l in range(k) if i != l)
            assert expected_sum == 1
            assert expected_square_sum+expected_cross == 1
        row = {'global_genus':k, 'vertex_genus':0, 'loops':k,
               'half_edge_monomials':terms, 'paired_monomials':len(F),
               'F_expansion_exact':True, 'gamma_total_parameter':2*n,
               'Dirichlet_first_second_total_area_exact':True}
        if k <= 4:
            M = 3
            labelled = sum((integrated_height_mass(F,m) for m in product(range(1,M+1),repeat=k)), Q(0))
            labelled /= 2**k*factorial(k)
            orbit = Q(0)
            for m in combinations_with_replacement(range(1,M+1),k):
                stabilizer = 2**k
                for count in Counter(m).values():
                    stabilizer *= factorial(count)
                orbit += integrated_height_mass(F,m)/stabilizer
            assert labelled == orbit
            row.update({'height_cap':M, 'labelled_heights':M**k,
                        'height_orbits':comb(M+k-1,k),
                        'orbit_stabilizer_mass_exact':True,
                        'integrated_mass':str(orbit)})
        rows.append(row)
    prefactors = []
    for g in (100,1000,10000,100000,1000000):
        cutoff = floor(Q(3,5)*log(6*g-6))
        D_over_D1 = Q(1)
        max_error = Q(0)
        for k in range(1,cutoff):
            ratio = Q(12*(g-k)*(3*g-3-k),(6*g-5-2*k)*(6*g-6-2*k))
            # Derive by factorials at small enough genus rather than reusing ratio.
            if g <= 1000:
                def D(g,k):
                    return Q(factorial(6*g-5-2*k)*2**(2*k),
                             factorial(g-k)*factorial(3*g-3-k)*3**(g-k))
                assert D(g,k+1)/D(g,k) == ratio
            D_over_D1 *= ratio
            max_error = max(max_error,abs(D_over_D1-1))
        prefactors.append({'g':g,'cutoff':cutoff,'max_relative_error':float(max_error),
                           'scaled_by_g_over_log_squared':float(max_error*g/log(g)**2)})
    eta = 0.6*log(1.1)-0.05
    assert eta > 1/220
    return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'method':'Independent direct genus-zero half-edge construction, rational orbit/stabilizer summation, beta integrals; no imported manuscript verifier.',
            'genus_zero_graph_controls':rows, 'prefactor_controls':prefactors,
            'eta_numeric':eta,'eta_greater_than_1_over_220':True,
            'limitation':'Finite exact controls validate algebra and conventions; asymptotic claims require the analytic proof and cited geometric theorems.'}


if __name__ == '__main__':
    result = checks()
    result['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (ROOT/'INDEPENDENT_GEOMETRY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
