#!/usr/bin/env python3
"""Independent finite diagnostics for PR 872, not an asymptotic proof.

Standard library only. No candidate checker or inherited audit code is imported.
"""
from collections import Counter, defaultdict
from fractions import Fraction
import argparse
import hashlib
import json
import math
from pathlib import Path


def require(value, message):
    if not value:
        raise RuntimeError(message)


def reduced_words(factors, length):
    if length == 0:
        yield ()
        return
    alphabet = range(len(factors))
    def extend(prefix):
        if len(prefix) == length:
            yield tuple(prefix)
        else:
            for a in alphabet:
                if not prefix or factors[a] != factors[prefix[-1]]:
                    prefix.append(a)
                    yield from extend(prefix)
                    prefix.pop()
    yield from extend([])


def inverse(word, inv):
    return tuple(inv[a] for a in reversed(word))


def multiply(left, right):
    size = len(left)
    return [[sum(left[i][k] * right[k][j] for k in range(size))
             for j in range(size)] for i in range(size)]


def matrix_power(matrix, exponent):
    size = len(matrix)
    result = [[int(i == j) for j in range(size)] for i in range(size)]
    while exponent:
        if exponent & 1:
            result = multiply(result, matrix)
        matrix = multiply(matrix, matrix)
        exponent //= 2
    return result


def jacobi_symmetric(matrix, tolerance=2e-13):
    """Finite diagnostic eigensolver. Residual checked against reconstructed A."""
    original = [list(map(float, row)) for row in matrix]
    a = [row[:] for row in original]
    n = len(a)
    vectors = [[float(i == j) for j in range(n)] for i in range(n)]
    iterations = 0
    for iterations in range(max(1, n * n * 100)):
        if n < 2:
            break
        p, q = max(((i, j) for i in range(n) for j in range(i+1, n)),
                   key=lambda ij: abs(a[ij[0]][ij[1]]))
        if abs(a[p][q]) < tolerance:
            break
        tau = (a[q][q] - a[p][p]) / (2 * a[p][q])
        t = math.copysign(1.0, tau) / (abs(tau) + math.sqrt(1 + tau*tau))
        c = 1 / math.sqrt(1 + t*t)
        s = t * c
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        a[p][p] = app - t * apq
        a[q][q] = aqq + t * apq
        a[p][q] = a[q][p] = 0.0
        for k in range(n):
            if k not in (p, q):
                akp, akq = a[k][p], a[k][q]
                a[k][p] = a[p][k] = c*akp - s*akq
                a[k][q] = a[q][k] = s*akp + c*akq
            vkp, vkq = vectors[k][p], vectors[k][q]
            vectors[k][p] = c*vkp - s*vkq
            vectors[k][q] = s*vkp + c*vkq
    residual = max((abs(sum(original[i][k]*vectors[k][j] for k in range(n))
                        - a[j][j]*vectors[i][j])
                    for i in range(n) for j in range(n)), default=0.0)
    require(residual < 1e-8, 'numerical eigensolver residual too large')
    return [a[j][j] for j in range(n)], vectors, residual


def case(factors, inv, ell, name, mutation=None):
    require(all(inv[inv[a]] == a and factors[a] == factors[inv[a]]
                for a in range(len(factors))), 'invalid inversion')
    length = ell // 3
    residue = ell % 3
    pattern = ((length, length, length), (length, length, length+1),
               (length, length+1, length+1))[residue]
    types = sorted(set(pattern))
    words = {t: list(reduced_words(factors, t)) for t in types}
    vertices_by_type = {t: [w for w in words[t] if w != inverse(w, inv)] for t in types}
    vertices = [(t, w) for t in types for w in vertices_by_type[t]]
    raw = Counter()
    cyclic_count = retained_count = 0
    for word in reduced_words(factors, ell):
        if factors[word[-1]] == factors[word[0]]:
            continue
        cyclic_count += 1
        i, j = pattern[0], pattern[0]+pattern[1]
        blocks = (word[:i], word[i:j], word[j:])
        if any(w == inverse(w, inv) for w in blocks):
            continue
        retained_count += 1
        sample_degrees = Counter()
        for index in range(3):
            first = (pattern[index], inverse(blocks[index], inv))
            second = (pattern[(index+1)%3], blocks[(index+1)%3])
            require(first != second, 'direct enumeration produced a loop')
            raw[first, second] += 1
            raw[second, first] += 1
            sample_degrees[first] += 1
            sample_degrees[second] += 1
        require(max(sample_degrees.values()) <= 3, 'per-sample vertex degree exceeds three')
    coefficients = ({(length,length):6} if residue == 0 else
                    {(length,length):2,(length,length+1):2,(length+1,length):2}
                    if residue == 1 else
                    {(length,length+1):2,(length+1,length):2,(length+1,length+1):2})
    A = [[int(factors[a] != factors[b]) for b in range(len(factors))]
         for a in range(len(factors))]
    require(cyclic_count == sum(matrix_power(A,ell)[i][i] for i in range(len(factors))),
            'trace cyclic count mismatch')
    require(sum(raw.values()) == 6*retained_count, 'total adjacency weight mismatch')
    completion = {}
    for t in types:
        for u in types:
            if coefficients.get((t,u),0):
                h = ell-t-u
                key = (t,u)
                completion[key] = [[sum(factors[p] != factors[w[0]] and factors[w[-1]] != factors[q]
                                            for w in vertices_by_type[h])
                                     for q in range(len(factors))] for p in range(len(factors))]
    row_degree = {}
    checks = 0
    wrong_single_orientation_mismatches = 0
    wrong_no_deletion_mismatches = 0
    for x in vertices:
        row_degree[x] = sum(raw[x,y] for y in vertices)
        for y in vertices:
            t, wx = x
            u, wy = y
            coefficient = coefficients.get((t,u),0)
            count = 0
            if coefficient:
                count = coefficient * A[wx[0]][wy[0]] * completion[t,u][wx[-1]][wy[-1]]
                require(completion[t,u][wx[-1]][wy[-1]] == completion[t,u][wy[-1]][wx[-1]],
                        'completion symmetry failed')
            if mutation == 'single-orientation':
                count //= 2
            elif mutation == 'omit-fixed-completion' and coefficient:
                count = coefficient * A[wx[0]][wy[0]] * matrix_power(A,ell-t-u+1)[wx[-1]][wy[-1]]
            require(count == raw[x,y], 'expected-link kernel (4.1) mismatch')
            if count:
                wrong_single_orientation_mismatches += int(count//2 != raw[x,y])
            if coefficient:
                h = ell-t-u
                undeleted = matrix_power(A,h+1)[wx[-1]][wy[-1]]
                wrong_count = coefficient * A[wx[0]][wy[0]] * undeleted
                wrong_no_deletion_mismatches += int(wrong_count != raw[x,y])
            checks += 1
    endpoint_groups = defaultdict(list)
    for vertex in vertices:
        t,w = vertex
        endpoint_groups[t,w[0],w[-1]].append(vertex)
    labels = sorted(endpoint_groups)
    compression_checks = 0
    compressed = []
    positive_degree = all(row_degree[x] > 0 for x in vertices)
    if vertices and positive_degree:
        for alpha in labels:
            members = endpoint_groups[alpha]
            reference = members[0]
            row = []
            for beta in labels:
                destination = endpoint_groups[beta]
                masses = [Fraction(sum(raw[x,y] for y in destination),row_degree[x]) for x in members]
                require(len(set(masses)) == 1, 'endpoint compression not constant')
                entries = {raw[x,y] for x in members for y in destination}
                require(len(entries) == 1, 'adjacency is not class-constant')
                row.append(masses[0])
                compression_checks += len(masses)
            require(sum(row) == 1,'compressed walk not stochastic')
            compressed.append(row)
        weights = [len(endpoint_groups[alpha])*row_degree[endpoint_groups[alpha][0]] for alpha in labels]
        for i in range(len(labels)):
            for j in range(len(labels)):
                require(weights[i]*compressed[i][j] == weights[j]*compressed[j][i],
                        'compressed detailed balance mismatch')
        symmetric = [[float(compressed[i][j])*math.sqrt(weights[i]/weights[j])
                      for j in range(len(labels))] for i in range(len(labels))]
        eigenvalues,_,residual_error = jacobi_symmetric(symmetric)
        eigenvalues.sort(reverse=True)
        if len(vertices) <= 32:
            full_symmetric = [[raw[x,y]/math.sqrt(row_degree[x]*row_degree[y]) for y in vertices] for x in vertices]
            full_eigenvalues,_,full_residual = jacobi_symmetric(full_symmetric)
            expected = sorted(eigenvalues + [0.0]*(len(vertices)-len(labels)),reverse=True)
            full_eigenvalues.sort(reverse=True)
            require(max(abs(x-y) for x,y in zip(full_eigenvalues,expected)) < 1e-8,
                    'full walk spectrum differs from endpoint compression plus zeros')
            full_spectrum_checked = True
        else:
            full_spectrum_checked = False
    else:
        eigenvalues,residual_error = [],None
        full_spectrum_checked = False
    deleted = {}
    for t in types:
        removed = [w for w in words[t] if w == inverse(w, inv)]
        require(not removed or t%2 == 1,'even inverse-fixed word')
        require(all(factors[w[0]] == factors[w[-1]] for w in removed),'bad fixed-word endpoints')
        power = matrix_power(A,t-1)
        for a in range(len(factors)):
            for b in range(len(factors)):
                full = sum(w[0] == a and w[-1] == b for w in words[t])
                require(full == power[a][b], 'endpoint matrix-power mismatch')
        if t%2:
            s = t//2
            prefix_count = len(list(reduced_words(factors,s)))
            middle_self_inverse = sum(inv[a] == a for a in range(len(factors)))
            require(len(removed) <= prefix_count*middle_self_inverse, 'odd deletion bound failed')
        deleted[str(t)] = {'full':len(words[t]),'removed':len(removed),'kept':len(vertices_by_type[t])}
    return {'name':name,'factors':factors,'inverse':inv,'ell':ell,'pattern':pattern,
            'cyclic_words':cyclic_count,'retained_relators':retained_count,
            'vertices':len(vertices),'endpoint_classes':len(labels),'kernel_entries_checked':checks,
            'compression_row_class_checks':compression_checks,'positive_degrees':positive_degree,
            'finite_mean_second_walk_eigenvalue_diagnostic':eigenvalues[1] if len(eigenvalues)>1 else None,
            'eigensolver_max_residual':residual_error,'full_spectrum_compression_checked':full_spectrum_checked,
            'inverse_fixed_deletion':deleted,
            'negative_controls':{'single_orientation_entry_mismatches':wrong_single_orientation_mismatches,
                                 'omitting_inverse_fixed_completion_entry_mismatches':wrong_no_deletion_mismatches}}


def spectral_diagnostics(sizes):
    factors = [i for i,size in enumerate(sizes) for _ in range(size)]
    A = [[int(factors[a] != factors[b]) for b in range(len(factors))] for a in range(len(factors))]
    eigenvalues,vectors,residual = jacobi_symmetric(A)
    order = sorted(range(len(eigenvalues)), key=lambda j:eigenvalues[j],reverse=True)
    lam = eigenvalues[order[0]]
    r = [abs(vectors[i][order[0]]) for i in range(len(factors))]
    require(all(x>0 for x in r),'Perron vector lacks positive entries')
    rho = -min(eigenvalues)/lam
    products = sorted((q*e/lam*rr for q in (1.0,-0.5) for e in eigenvalues
                       for rr in (1.0,0.0)),reverse=True)
    require(abs(products[0]-1.0)<1e-10,'principal product mismatch')
    require(products[1] <= rho/2+1e-10 and products[1]<0.5,'tensor upper bound failed')
    # Explicit endpoint asymptotic diagnostics on counts before and after exact deletion.
    endpoint_errors = []
    for t in (4,5,8,9,12,13,20,21):
        full = matrix_power(A,t-1)
        relative_error = max(abs(full[a][b]/(lam**(t-1)*r[a]*r[b])-1)
                             for a in range(len(factors)) for b in range(len(factors)))
        endpoint_errors.append({'t':t,'max_full_endpoint_relative_error':relative_error})
    return {'sizes':sizes,'lambda_diagnostic':lam,'rho_diagnostic':rho,
            'unequal_residue_largest_nonprincipal_product_diagnostic':products[1],
            'spectral_margin_above_half_diagnostic':(1-rho)/2,
            'A_eigensolver_residual':residual,'full_endpoint_relative_errors':endpoint_errors}


def endpoint_diagnostics(factors, inv, label):
    k = len(factors)
    A = [[int(factors[a] != factors[b]) for b in range(k)] for a in range(k)]
    eigenvalues, vectors, residual = jacobi_symmetric(A)
    index = max(range(k), key=lambda j:eigenvalues[j])
    lam = eigenvalues[index]
    r = [abs(vectors[a][index]) for a in range(k)]
    cache = {}
    def endpoint_counts(t):
        if t in cache:
            return cache[t]
        counts = matrix_power(A,t-1)
        removed = [[0]*k for _ in range(k)]
        if t == 1:
            for a in range(k):
                removed[a][a] = int(inv[a] == a)
        elif t%2:
            s = t//2
            prefix = matrix_power(A,s-1)
            center_choices = [sum(inv[c] == c and factors[c] != factors[d] for c in range(k))
                              for d in range(k)]
            for a in range(k):
                removed[a][inv[a]] = sum(prefix[a][d]*center_choices[d] for d in range(k))
        kept = [[counts[a][b]-removed[a][b] for b in range(k)] for a in range(k)]
        require(all(x>=0 for row in kept for x in row), 'negative endpoint count')
        if t <= 4:
            direct = Counter((w[0],w[-1]) for w in reduced_words(factors,t) if w != inverse(w,inv))
            require(all(kept[a][b] == direct[a,b] for a in range(k) for b in range(k)),
                    'closed endpoint-deletion formula disagrees with direct enumeration')
        cache[t] = kept
        return kept
    for t in range(1,5):
        endpoint_counts(t)
    rows = []
    for L in (4,5,8,9,16,17,24,25):
        for residue in range(3):
            ell = 3*L+residue
            types = [L] if residue == 0 else [L,L+1]
            C = [[6]] if residue == 0 else [[2,2],[2,0]] if residue == 1 else [[0,2],[2,2]]
            degrees = {}
            T = {}
            V = {t:endpoint_counts(t) for t in types}
            max_endpoint_relative_error = max(abs(V[t][a][b]/(lam**(t-1)*r[a]*r[b])-1)
                                              for t in types for a in range(k) for b in range(k))
            for ti,t in enumerate(types):
                for ui,u in enumerate(types):
                    if C[ti][ui]:
                        T[t,u] = multiply(multiply(A,endpoint_counts(ell-t-u)),A)
                for a in range(k):
                    for b in range(k):
                        degrees[t,a,b] = sum(C[ti][ui] * A[a][c] * V[u][c][f] * T[t,u][b][f]
                                             for ui,u in enumerate(types) if C[ti][ui]
                                             for c in range(k) for f in range(k))
            max_degree_relative_error = max(abs(degrees[t,a,b]/(lam**(ell-t+1)*r[a]*r[b]*sum(C[ti]))-1)
                                             for ti,t in enumerate(types) for a in range(k) for b in range(k))
            max_walk_entry_error = 0.0
            stationary_total = sum(V[t][a][b]*degrees[t,a,b]
                                   for t in types for a in range(k) for b in range(k))
            max_stationary_entry_error = 0.0
            for ti,t in enumerate(types):
                for a in range(k):
                    for b in range(k):
                        exact_stationary = V[t][a][b]*degrees[t,a,b]/stationary_total
                        limit_stationary = (sum(C[ti])/6)*r[a]**2*r[b]**2
                        max_stationary_entry_error = max(max_stationary_entry_error,
                                                         abs(exact_stationary-limit_stationary))
                        for ui,u in enumerate(types):
                            if not C[ti][ui]:
                                continue
                            for c in range(k):
                                for f in range(k):
                                    exact = Fraction(V[u][c][f]*C[ti][ui]*A[a][c]*T[t,u][b][f],
                                                     degrees[t,a,b])
                                    limit = (C[ti][ui]/sum(C[ti]))*A[a][c]*r[c]/(lam*r[a])*r[f]**2
                                    max_walk_entry_error = max(max_walk_entry_error,abs(float(exact)-limit))
            rows.append({'L':L,'ell':ell,'residue':residue,
                         'max_kept_endpoint_relative_error_diagnostic':max_endpoint_relative_error,
                         'max_degree_relative_error_diagnostic':max_degree_relative_error,
                         'max_compressed_walk_entry_error_diagnostic':max_walk_entry_error,
                         'max_stationary_probability_error_diagnostic':max_stationary_entry_error})
    return {'name':label,'factors':factors,'inverse':inv,'rows':rows,
            'counting':'Exact integer endpoints and deletion; floating Perron limits are diagnostics only.'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    parser.add_argument('--mutation',choices=('single-orientation','omit-fixed-completion'))
    args = parser.parse_args()
    cases = []
    configurations = [('three_involutions',[0,1,2],[0,1,2],range(6,12)),
                      ('one_inverse_pair_two_involutions',[0,0,1,2],[1,0,2,3],range(6,12)),
                      ('mixed_pair_and_involution',[0,0,0,1,2],[1,0,2,3,4],range(6,9)),
                      ('all_involutions_unequal',[0,0,0,1,2],[0,1,2,3,4],range(6,9)),
                      ('three_unequal_parts',[0,1,1,2,2,2],[0,2,1,4,3,5],range(6,9))]
    for name,factors,inv,lengths in configurations:
        for ell in lengths:
            cases.append(case(factors,inv,ell,name,args.mutation))
    spectral = [spectral_diagnostics(sizes) for sizes in ([1,1,1],[2,1,1],[3,1,1],[1,2,3],[1,1,32])]
    endpoint_results = [endpoint_diagnostics(factors,inv,name) for name,factors,inv,_ in configurations]
    require(any(c['negative_controls']['omitting_inverse_fixed_completion_entry_mismatches'] for c in cases),
            'no deletion-sensitive case tested')
    require(all(c['negative_controls']['single_orientation_entry_mismatches'] for c in cases),
            'single-orientation negative control not triggered')
    result = {'status':'PASS','diagnostics_only':True,'independent_of_candidate_checker':True,
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'case_count':len(cases),'kernel_entries_checked':sum(c['kernel_entries_checked'] for c in cases),
              'cyclic_relators_enumerated':sum(c['cyclic_words'] for c in cases),
              'retained_relators_enumerated':sum(c['retained_relators'] for c in cases),
              'cases':cases,'spectral_diagnostics':spectral,'endpoint_asymptotic_diagnostics':endpoint_results}
    encoded = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(encoded)
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','spectral_diagnostics','endpoint_asymptotic_diagnostics')},sort_keys=True))

if __name__ == '__main__':
    main()
