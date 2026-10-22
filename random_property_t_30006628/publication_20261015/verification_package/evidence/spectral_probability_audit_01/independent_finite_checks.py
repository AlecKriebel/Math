#!/usr/bin/env python3
"""Independent finite evidence for PR872; no asymptotic theorem certificate.

Standard library only. Does not read or execute the author's checker.
Uses explicit guards so optimized Python performs the same checks.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from itertools import product


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def inverse(word, inv):
    return tuple(inv[a] for a in reversed(word))


def words(length, parts):
    if length == 1:
        yield from ((a,) for a in range(len(parts)))
        return
    for pre in words(length - 1, parts):
        for a in range(len(parts)):
            if parts[a] != parts[pre[-1]]:
                yield pre + (a,)


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def ident(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def power(a, exponent):
    result = ident(len(a))
    for _ in range(exponent):
        result = matmul(result, a)
    return result


def endpoint_counts(t, parts, inv):
    k = len(parts)
    a = [[int(parts[i] != parts[j]) for j in range(k)] for i in range(k)]
    v = power(a, t - 1)
    if t % 2:
        half = power(a, t // 2)
        for x in range(k):
            removed = sum(half[x][mid] for mid in range(k) if inv[mid] == mid)
            v[x][inv[x]] -= removed
    return v


def c_matrix(lengths):
    result = Counter()
    for i in range(3):
        t, u = lengths[i], lengths[(i + 1) % 3]
        result[t, u] += 1
        result[u, t] += 1
    return result


def exhaustive_case(name, parts, inv, L):
    k = len(parts)
    a = [[int(parts[i] != parts[j]) for j in range(k)] for i in range(k)]
    cached = {t: list(words(t, parts)) for t in (L, L + 1)}
    valid = {t: [w for w in ws if inverse(w, inv) != w] for t, ws in cached.items()}
    for t, ws in valid.items():
        actual = Counter((w[0], w[-1]) for w in ws)
        v = endpoint_counts(t, parts, inv)
        need(all(actual[x, y] == v[x][y] for x in range(k) for y in range(k)),
             'independent palindrome-deletion formula failed')
    rows = []
    negative = set()
    for e in range(3):
        lengths = (L, L, L) if e == 0 else ((L, L, L + 1) if e == 1 else (L, L + 1, L + 1))
        ell = sum(lengths)
        vset = set(valid[lengths[0]]) | set(valid[lengths[1]]) | set(valid[lengths[2]])
        vertices = sorted(vset)
        edge_counts = Counter()
        inv_convention_counts = Counter()
        sampled = retained = max_degree = 0
        max_degree_witness = None
        for r in words(ell, parts):
            if parts[r[0]] == parts[r[-1]]:
                continue
            sampled += 1
            b0, b1 = lengths[0], lengths[0] + lengths[1]
            bs = (r[:b0], r[b0:b1], r[b1:])
            if any(inverse(w, inv) == w for w in bs):
                continue
            retained += 1
            degrees = Counter()
            for i in range(3):
                x, y = inverse(bs[i], inv), bs[(i + 1) % 3]
                need(x != y, 'loop in retained triangular link')
                edge_counts[x, y] += 1
                edge_counts[y, x] += 1
                degrees[x] += 1
                degrees[y] += 1
                # Deliberately wrong convention, without the global inverse relabeling.
                z = bs[i]
                inv_convention_counts[z, y] += 1
                inv_convention_counts[y, z] += 1
            need(sum(degrees.values()) == 6 and max(degrees.values()) <= 3,
                 'degree/sample count failed')
            if max(degrees.values()) > max_degree:
                max_degree = max(degrees.values())
                max_degree_witness = [list(w) for w in bs]
        trace = sum(power(a, ell)[x][x] for x in range(k))
        need(sampled == trace, 'trace cyclic-count identity failed')
        cs = c_matrix(lengths)
        completions = {}
        raw_completions = {}
        for h in set(lengths):
            raw_completions[h] = power(a, h + 1)
            completions[h] = [[sum(a[p][w[0]] * a[w[-1]][q] for w in valid[h])
                               for q in range(k)] for p in range(k)]
        comparisons = mismatches_without_torsion = mismatches_wrong_type = 0
        for x, y in product(vertices, repeat=2):
            t, u = len(x), len(y)
            c = cs[t, u]
            h = ell - t - u
            expected = c * a[x[0]][y[0]] * completions[h][x[-1]][y[-1]] if c else 0
            need(edge_counts[x, y] == expected, 'corner kernel mismatch')
            comparisons += 1
            if c:
                wrong_torsion = c * a[x[0]][y[0]] * raw_completions[h][x[-1]][y[-1]]
                mismatches_without_torsion += (wrong_torsion != edge_counts[x, y])
                wrong_c = c - 1
                wrong_type = wrong_c * a[x[0]][y[0]] * completions[h][x[-1]][y[-1]]
                mismatches_wrong_type += (wrong_type != edge_counts[x, y])
        if mismatches_without_torsion:
            negative.add('omit_inverse_fixed_completion_deletion')
        if mismatches_wrong_type:
            negative.add('change_oriented_type_multiplicity')
        if inv_convention_counts != edge_counts:
            negative.add('drop_link_inverse_without_relabeling')
        if max_degree == 3:
            negative.add('bound_single_sample_degree_by_two')
        digest_rows = [(list(x), list(y), c) for (x, y), c in sorted(edge_counts.items())]
        rows.append({'name': name, 'lengths': lengths, 'cyclic_words': sampled,
                     'retained_words': retained, 'vertices': len(vertices),
                     'ordered_vertex_pair_checks': comparisons, 'max_single_sample_degree': max_degree,
                     'degree_three_witness': max_degree_witness,
                     'wrong_torsion_mismatch_pairs': mismatches_without_torsion,
                     'wrong_type_mismatch_pairs': mismatches_wrong_type,
                     'adjacency_counts_sha256': hashlib.sha256(json.dumps(digest_rows,separators=(',',':')).encode()).hexdigest()})
    return rows, negative


def characteristic(a):
    n = len(a)
    b = ident(n)
    coeff = [F(1)]
    for j in range(1, n + 1):
        b = matmul(a, b)
        c = -sum(b[i][i] for i in range(n)) / j
        coeff.append(c)
        for i in range(n):
            b[i][i] += c
    return coeff


def polynomial_roots(roots):
    p = [F(1)]
    for root in roots:
        q = [F(0)] * (len(p) + 1)
        for i, c in enumerate(p):
            q[i] += c
            q[i + 1] -= c * root
        p = q
    return p


def rational_limit_checks():
    # Three factors, sizes 1,1,3: lambda=3, Perron coordinates proportional to 3,3,2,2,2.
    parts = [0, 1, 2, 2, 2]
    inv = [0, 1, 4, 3, 2]
    r = [3, 3, 2, 2, 2]
    a = [[int(parts[i] != parts[j]) for j in range(5)] for i in range(5)]
    need([sum(a[i][j] * r[j] for j in range(5)) for i in range(5)] == [3*x for x in r], 'Perron witness')
    pi = [F(x*x, 30) for x in r]
    p = [[F(a[i][j]*r[j], 3*r[i]) for j in range(5)] for i in range(5)]
    need(characteristic(p) == polynomial_roots([F(1), F(-2,3), F(-1,3), F(0), F(0)]), 'exact P spectrum')
    qs = [[[F(1)]], [[F(1,2),F(1,2)],[F(1),F(0)]], [[F(0),F(1)],[F(1,2),F(1,2)]]]
    spectra = []
    for e, q in enumerate(qs):
        qp = [[q[t][u]*p[a0][c] for u in range(len(q)) for c in range(5)]
              for t in range(len(q)) for a0 in range(5)]
        roots = [F(1), F(-2,3), F(-1,3), F(0), F(0)]
        if e:
            roots += [F(-1,2), F(1,3), F(1,6), F(0), F(0)]
        need(characteristic(qp) == polynomial_roots(roots), 'type/P tensor spectrum')
        spectra.append({'residue': e, 'nonzero_eigenvalues': [str(x) for x in roots if x],
                        'second_largest_walk_eigenvalue': str(sorted(roots, reverse=True)[1])})
    # Characteristic polynomial, not floating-point approximate eigenvalues.
    negative = {'assume_nonprincipal_tensor_eigenvalues_nonpositive',
                'replace_Perron_endpoint_weights_by_uniform'}
    need(pi != [F(1,5)]*5, 'uneven endpoint weights control')
    convergence = []
    for L in (8, 16, 32):
        for e in range(3):
            ls = (L,L,L) if e == 0 else ((L,L,L+1) if e == 1 else (L,L+1,L+1))
            cs = c_matrix(ls)
            ts = sorted(set(ls))
            vs = {t: endpoint_counts(t,parts,inv) for t in ts}
            need(all(vs[t][a0][b] > 0 for t in ts for a0 in range(5) for b in range(5)), 'all endpoint classes exist')
            tc = {h: matmul(matmul(a,vs[h]),a) for h in ts}
            maxerr=F(0)
            missing_multiplicity_detected=False
            for ti,t in enumerate(ts):
                ht=sum(cs[t,u] for u in ts)
                for a0,b in product(range(5), repeat=2):
                    weights=[]
                    wrong=[]
                    limits=[]
                    for u,c,f in product(ts,range(5),range(5)):
                        raw=cs[t,u]*a[a0][c]*tc[sum(ls)-t-u][b][f] if cs[t,u] else 0
                        weights.append(vs[u][c][f]*raw)
                        wrong.append(raw)
                        limits.append(F(cs[t,u],ht)*p[a0][c]*pi[f])
                    denom=sum(weights)
                    need(denom>0, 'mean row degree positive')
                    row=[F(w,denom) for w in weights]
                    need(sum(row)==1, 'compressed stochastic row')
                    maxerr=max(maxerr,max(abs(x-y) for x,y in zip(row,limits)))
                    if sum(wrong) and row != [F(w,sum(wrong)) for w in wrong]:
                        missing_multiplicity_detected=True
            need(missing_multiplicity_detected, 'missing class multiplicity mutation not detected')
            convergence.append({'L':L, 'residue':e, 'max_entry_error_exact':str(maxerr),
                                'max_entry_error_float':float(maxerr)})
    negative.add('omit_destination_endpoint_class_multiplicity')
    for e in range(3):
        es=[x['max_entry_error_float'] for x in convergence if x['residue']==e]
        need(es[2] < es[1] < es[0], 'observed convergence decreasing')
    gamma=F(7,12)
    eps=F(1,26)
    bound=(1-eps)*gamma/(1+eps)
    need(bound>F(1,2), 'strict actual-gap margin')
    return {'spectra':spectra,'endpoint_weights':[str(x) for x in pi],
            'compression_convergence':convergence,'gamma':str(gamma),'epsilon':str(eps),
            'actual_gap_bound':str(bound)},negative


def main():
    allrows=[]
    negatives=set()
    for case in [('three_involutions',[0,1,2],[0,1,2],3),
                 ('uneven_C2_C2_C4',[0,1,2,2,2],[0,1,4,3,2],3),
                 ('mixed_C2_C3_C3',[0,1,1,2,2],[0,2,1,4,3],2)]:
        rows,neg=exhaustive_case(*case)
        allrows.extend(rows)
        negatives.update(neg)
    limits,neg=rational_limit_checks()
    negatives.update(neg)
    need(len(negatives)==7, 'expected seven distinct deliberate bad models rejected')
    print(json.dumps({'status':'PASS', 'scope':'Finite exact evidence only; not an asymptotic proof or property-(T) certificate.',
                      'exhaustive_cases':allrows,'rational_limit_checks':limits,
                      'deliberately_wrong_models_rejected':sorted(negatives)},indent=2))


if __name__=='__main__':
    main()
