"""Research candidate: sparse numerator/dense denominator Cartier reduction.

This is a reference reduction, using the existing bounded exhaustive prime oracle
for feasible examples. It does NOT implement the large-prime input theorem or
establish novelty. Exponents and multiplicities stay as binary Python integers.
No loop enumerates the degree of the sparse input or the characteristic.
"""

from __future__ import annotations

import finite_fields as ff


def normalized_sparse(K, terms):
    answer = {}
    for n, a in terms:
        if not isinstance(n, int) or n < 0:
            raise ValueError("exponents must be nonnegative integers")
        answer[n] = K.add(answer.get(n, K.zero), K.element(a))
    return {n: a for n, a in sorted(answer.items()) if a != K.zero}


def sparse_dense_product(K, sparse, dense):
    out = {}
    for n, a in sparse.items():
        for j, b in enumerate(dense):
            if b != K.zero:
                out[n + j] = K.add(out.get(n + j, K.zero), K.mul(a, b))
    return {n: a for n, a in out.items() if a != K.zero}


def sparse_derivative(K, sparse):
    return {n - 1: K.mul(a, K.element(n % K.p))
            for n, a in sparse.items() if n and n % K.p}


def logarithmic_denominator(K, sparse, audit):
    """Adaptive exact Pade recovery of the reduced denominator of U'/U.

    Classical rational reconstruction, with a sparse exact identity certificate.
    2B coefficients, a B by (B+1) augmented matrix, no degree-N expansion.
    """
    if 0 not in sparse:
        raise ValueError("the constant coefficient must be nonzero")
    B = 1
    derivative = sparse_derivative(K, sparse)
    inv0 = K.inv(sparse[0])
    while True:
        coeff = [sparse.get(i, K.zero) for i in range(2 * B + 1)]
        series = []
        for k in range(2 * B):
            v = K.mul(coeff[k + 1], K.element((k + 1) % K.p))
            for i in range(1, k + 1):
                v = K.sub(v, K.mul(coeff[i], series[k - i]))
            series.append(K.mul(v, inv0))
        columns = [[series[j - i] for j in range(B, 2 * B)]
                   for i in range(1, B + 1)]
        sol = ff.solve_columns(K, columns, [K.neg(series[j]) for j in range(B, 2 * B)])
        accepted = False
        if sol is not None:
            Q = ff.trim(K, [K.one] + sol)
            P = ff.trim(K, [sum_field(K, (K.mul(Q[i], series[k - i])
                                        for i in range(min(k, len(Q) - 1) + 1)))
                            for k in range(B)])
            accepted = (sparse_dense_product(K, derivative, Q)
                        == sparse_dense_product(K, sparse, P))
            if accepted:
                common = ff.gcd(K, P, Q)
                denominator = ff.monic(K, ff.exact_div(K, Q, common))
                audit.append({"B": B, "matrix_rows": B, "matrix_columns": B + 1,
                              "accepted": True, "denominator_degree": len(denominator) - 1})
                return denominator
        audit.append({"B": B, "matrix_rows": B, "matrix_columns": B + 1,
                      "accepted": False})
        B *= 2


def sum_field(K, terms):
    answer = K.zero
    for a in terms:
        answer = K.add(answer, a)
    return answer


def quotient_multiplicity(K, sparse, g, audit=None):
    """Exact multiplicity of a known monic irreducible, using exponent digits.

    Constructive residue argument related to Mattarei (2005/2006), Theorem 2.
    Uses an iterative postorder tree, never a recursion-depth or p-sized scan.
    """
    if len(g) == 2 and g[0] == K.zero:
        return min(sparse)
    alpha = ff.divmod_poly(K, (K.zero, K.one), g)[1]
    one, zero = (K.one,), ()

    def emul(a, b):
        return ff.divmod_poly(K, ff.mul(K, a, b), g)[1]

    def epow(a, n):
        v = one
        while n:
            if n & 1:
                v = emul(v, a)
            n >>= 1
            if n:
                a = emul(a, a)
        return v

    terms = [(n, emul((a,), epow(alpha, n))) for n, a in sparse.items()]
    stack, results, next_id = [(0, terms, None)], {}, 1
    nodes = coefficient_checks = 0
    while stack:
        ident, terms, children = stack.pop()
        if children is None:
            nodes += 1
            if len(terms) == 1:
                results[ident] = (0, terms[0][1])
                continue
            buckets = {}
            for n, a in terms:
                q, r = divmod(n, K.p)
                buckets.setdefault(r, []).append((q, a))
            children = []
            for r, child_terms in sorted(buckets.items()):
                children.append((r, next_id, child_terms))
                next_id += 1
            stack.append((ident, terms, children))
            stack.extend((child_id, child_terms, None) for _, child_id, child_terms in children)
            continue
        v = min(results[child_id][0] for _, child_id, _ in children)
        active = [(r, results[child_id][1]) for r, child_id, _ in children
                  if results[child_id][0] == v]
        binomials = [1] * len(active)
        for j in range(len(active)):
            c = sum_poly(K, (ff.scale(K, a, K.element(b))
                             for (_, a), b in zip(active, binomials)))
            coefficient_checks += 1
            if c != zero:
                results[ident] = (K.p * v + j, c)
                break
            if j + 1 == len(active):
                raise ArithmeticError("distinct-residue Vandermonde guarantee failed")
            inv = pow(j + 1, -1, K.p)
            binomials = [b * (r - j) * inv % K.p for (r, _), b in zip(active, binomials)]
    if audit is not None:
        audit.append({"factor_degree": len(g) - 1, "terms": len(sparse),
                      "max_exponent_bits": max(sparse).bit_length(), "nodes": nodes,
                      "coefficient_checks": coefficient_checks})
    return results[0][0]


def sum_poly(K, terms):
    answer = ()
    for a in terms:
        answer = ff.add(K, answer, a)
    return answer


def dense_power(K, g, e):
    answer = (K.one,)
    while e:
        if e & 1:
            answer = ff.mul(K, answer, g)
        e >>= 1
        if e:
            g = ff.mul(K, g, g)
    return answer


def coefficient_root(K, a):
    return K.pow(a, K.p ** (K.m - 1))


def factor_sparse(K, terms, prime_oracle=ff.exhaustive_prime_split_oracle, verify=True):
    """Full research-candidate reduction with all multiplicities, plus audit.

    Verification uses exact valuations and a degree sum, never dense expansion of
    a power with a binary-encoded enormous multiplicity.
    """
    original = normalized_sparse(K, terms)
    if not original:
        raise ValueError("zero polynomial is excluded")
    shift = min(original)
    U = {n - shift: a for n, a in original.items()}
    V = (K.one,)
    collected = {(K.zero, K.one): shift} if shift else {}
    weight = 1
    audit = {"levels": [], "pade": [], "valuations": []}
    while max(U) > 0:
        G = logarithmic_denominator(K, U, audit["pade"])
        visible = ff.factor(K, G, prime_oracle).factors
        A = (K.one,)
        signed = {}
        for g, squarefree_e in visible:
            if squarefree_e != 1:
                raise ArithmeticError("logarithmic denominator must be squarefree")
            mu = quotient_multiplicity(K, U, g, audit["valuations"])
            r = mu % K.p
            if not (0 < r <= len(U) - 1):
                raise ArithmeticError("sparse residue-multiplicity bound failed")
            A = ff.mul(K, A, dense_power(K, g, r))
            signed[g] = r
        Vfactors = ff.factor(K, V, prime_oracle).factors
        AV = (K.one,)
        for g, e in Vfactors:
            r = e % K.p
            if r:
                AV = ff.mul(K, AV, dense_power(K, g, r))
                signed[g] = signed.get(g, 0) - r
        HV = ff.polynomial_pth_root(K, ff.exact_div(K, V, AV))
        # Constant section suffices because U(0), A(0) are nonzero.
        Unew = {n // K.p: coefficient_root(K, a) for n, a in U.items() if n % K.p == 0}
        W = ff.trim(K, [coefficient_root(K, A[j]) for j in range(0, len(A), K.p)])
        Vnew = ff.mul(K, W, HV)
        audit["levels"].append({"sparse_terms": len(U), "numerator_degree_bits": max(U).bit_length(),
                                "denominator_degree": len(V) - 1,
                                "visible_degree": len(G) - 1, "residue_product_degree": len(A) - 1,
                                "new_denominator_degree": len(Vnew) - 1,
                                "signed_factor_count": len(signed),
                                "negative_signed_residues": sum(r < 0 for r in signed.values()),
                                "weight_bits": weight.bit_length()})
        for g, r in signed.items():
            collected[g] = collected.get(g, 0) + weight * r
        U, V, weight = Unew, Vnew, weight * K.p
    if len(V) != 1:
        raise ArithmeticError("terminal sparse numerator has a nonconstant denominator")
    if any(e < 0 for e in collected.values()):
        raise ArithmeticError("negative final multiplicity")
    factors = tuple(sorted((g, e) for g, e in collected.items() if e))
    result = ff.Factorization(original[max(original)], factors)
    if verify:
        if sum((len(g) - 1) * e for g, e in factors) != max(original):
            raise ArithmeticError("final weighted degree mismatch")
        if any(not ff.irreducible(K, g) or quotient_multiplicity(K, original, g) != e
               for g, e in factors):
            raise ArithmeticError("final independent irreducibility/valuation check failed")
    return result, audit
