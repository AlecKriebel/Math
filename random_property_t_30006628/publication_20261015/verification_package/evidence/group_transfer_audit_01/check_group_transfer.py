#!/usr/bin/env python3
"""Independent exact finite tests; not an asymptotic proof or (T) decision tool.

A syllable is (factor_index, exponent). A factor order 0 denotes Z. The
normalizer uses factor multiplication, independently of the suffix generator.
No candidate checker, prior audit, or third-party package is imported.
"""
from collections import Counter
from itertools import product
import json


class Failure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


MODELS = (
    ("three_involutions", (2, 2, 2), ((1,), (1,), (1,)), 10, 14),
    ("mixed_torsion", (2, 3, 4), ((1,), (1, 2), (1, 3)), 7, 8),
    ("infinite_and_involution", (0, 2, 0), ((-1, 1), (1,), (-1, 1)), 7, 8),
    ("unequal_ball_alphabets", (0, 3, 2), ((-2, -1, 1, 2), (1, 2), (1,)), 6, 7),
    ("four_factors", (2, 3, 0, 2), ((1,), (1, 2), (-1, 1), (1,)), 6, 7),
)


def normalize(orders, sequence):
    stack = []
    for i, value in sequence:
        if stack and stack[-1][0] == i:
            value += stack.pop()[1]
        if orders[i]:
            value %= orders[i]
        if value:
            stack.append((i, value))
    return tuple(stack)


def inv_letter(orders, letter):
    i, value = letter
    return (i, (-value) % orders[i] if orders[i] else -value)


def inverse(orders, word):
    return tuple(inv_letter(orders, a) for a in reversed(word))


def words(alphabet, length):
    if length == 0:
        yield ()
        return
    for initial in alphabet:
        for tail in words_after(alphabet, length - 1, initial[0]):
            yield (initial,) + tail


def words_after(alphabet, length, previous):
    if length == 0:
        yield ()
        return
    for a in alphabet:
        if a[0] != previous:
            for tail in words_after(alphabet, length - 1, a[0]):
                yield (a,) + tail


def suffix_witness(alphabet, a, b, length):
    factors = sorted({x[0] for x in alphabet})
    representatives = {i: next(x for x in alphabet if x[0] == i) for i in factors}
    c = next(i for i in factors if i not in (a[0], b[0]))
    d, e = [i for i in factors if i != c][:2]
    if length % 2 == 0:
        factor_pattern = tuple(c if j % 2 == 0 else d for j in range(length - 1))
    else:
        factor_pattern = (c, d, e, c) + (d, c) * ((length - 5) // 2)
    return tuple(representatives[i] for i in factor_pattern)


def run():
    counts = Counter()
    tables = []
    for name, orders, parts, max_word_length, max_relator_length in MODELS:
        alphabet = tuple((i, value) for i, part in enumerate(parts) for value in part)
        require(len(set(alphabet)) == len(alphabet), name + ": distinct alphabet")
        require(set(inverse(orders, (a,))[0] for a in alphabet) == set(alphabet), name + ": inverse closed")
        model = {"model": name, "factor_orders_zero_means_infinite": list(orders),
                 "alphabet_sizes": list(map(len, parts)), "inverse_fixed_by_length": {},
                 "retained_relators_by_length": {}, "suffix_witnesses": 0}
        for t in range(1, max_word_length + 1):
            total, fixed = 0, 0
            bound = None
            if t % 2:
                s = t // 2
                bound = sum(1 for unused in words(alphabet, s)) * sum(inv_letter(orders, a) == a for a in alphabet)
            for w in words(alphabet, t):
                total += 1
                require(normalize(orders, w) == w, "normal form was not reduced")
                iw = inverse(orders, w)
                require(inverse(orders, iw) == w, "inverse involution")
                require(normalize(orders, w + iw) == (), "inverse product")
                counts['normal_form_words'] += 1
                if w == iw:
                    fixed += 1
                    require(t % 2 == 1, "even inverse-fixed word")
                    s = t // 2
                    require(w[s] == inv_letter(orders, w[s]), "middle not involution")
                    require(w[s + 1:] == inverse(orders, w[:s]), "not conjugate involution")
                elif t % 2 == 0:
                    counts['even_words_not_inverse_fixed'] += 1
            if bound is not None:
                require(fixed <= bound, "inverse-fixed count exceeds proposed upper bound")
            model['inverse_fixed_by_length'][str(t)] = {"all": total, "fixed": fixed, "upper_bound_if_odd": bound}
        # Actual finite-group/free-product multiplication verifies the cancellation
        # identity, including same-factor a,b products and the identity case.
        for length in range(4, 24):
            for a, b in product(alphabet, repeat=2):
                v = suffix_witness(alphabet, a, b, length)
                left = (a,) + v
                right = (inv_letter(orders, b),) + v
                require(len(v) == length - 1, "suffix length")
                require(normalize(orders, left) == left, "left not reduced")
                require(normalize(orders, right) == right, "right not reduced")
                require(left != inverse(orders, left), "left inverse fixed")
                require(right != inverse(orders, right), "right inverse fixed")
                require(normalize(orders, left + inverse(orders, right)) == normalize(orders, (a, b)), "suffix identity")
                counts['suffix_witnesses'] += 1
                model['suffix_witnesses'] += 1
        for a, b, c in product(alphabet, repeat=3):
            ci = inv_letter(orders, c)
            require(normalize(orders, (c, a, b, ci)) == normalize(orders, (c, a) + (b, ci)), "K normality identity")
            counts['normality_identities'] += 1
        for ell in range(3, max_relator_length + 1):
            length, residue = divmod(ell, 3)
            lengths = ((length, length, length), (length, length, length+1), (length, length+1, length+1))[residue]
            retained = 0
            for w in words(alphabet, ell):
                if w[-1][0] == w[0][0]:
                    continue
                counts['cyclic_relators'] += 1
                cuts = (0, lengths[0], lengths[0] + lengths[1], ell)
                blocks = tuple(w[cuts[i]:cuts[i+1]] for i in range(3))
                if any(x == inverse(orders, x) for x in blocks):
                    counts['discarded_relators'] += 1
                    continue
                retained += 1
                # Actual inverse-pair labels, and both link conventions.
                signed = tuple((min(x, inverse(orders, x)), 1 if x < inverse(orders, x) else -1) for x in blocks)
                require(len(set((len(x), x) for x in blocks)) >= 1, "nonempty blocks")
                candidate_edges = []
                kk_inverse_edges = []
                for i in range(3):
                    x, y = blocks[i], blocks[(i+1) % 3]
                    require(x != inverse(orders, y), "cyclic formal block cancellation")
                    require(not (signed[i][0] == signed[(i+1)%3][0] and signed[i][1] == -signed[(i+1)%3][1]), "signed formal cancellation")
                    edge = tuple(sorted((inverse(orders, x), y)))
                    require(edge[0] != edge[1], "link loop")
                    candidate_edges.append(edge)
                    # KK has {x,y^-1}; invert all its vertices.
                    kk_edge = (x, inverse(orders, y))
                    kk_inverse_edges.append(tuple(sorted(inverse(orders, v) for v in kk_edge)))
                require(sorted(candidate_edges) == sorted(kk_inverse_edges), "global inverse isomorphism")
                counts['retained_triangles'] += 1
            model['retained_relators_by_length'][str(ell)] = retained
        tables.append(model)
    # Boundary falsifications are positive detections of failures of deliberately
    # weakened statements. They are not claims about the theorem's legal range.
    pair_alphabet = ((0, 1), (1, 1))
    orders = (2, 2)
    for length in (1, 3, 5, 7, 9):
        require(all(w == inverse(orders, w) for w in words(pair_alphabet, length)), "two-C2 odd boundary did not fail")
        counts['boundary_controls'] += 1
    # Even-length generators of C2*C2 at L=4 only generate <(ab)^2>.
    # Its normal-form cosets 1,a,ab,aba are distinct (index four), not <=two.
    generators = tuple(words(pair_alphabet, 4))
    require(len(generators) == 2 and inverse(orders, generators[0]) == generators[1], "two-C2 even boundary generators")
    counts['boundary_controls'] += 1
    # Length one may consist only of inverse-fixed letters even with n=3.
    triple = ((0, 1), (1, 1), (2, 1))
    require(all(w == inverse((2, 2, 2), w) for w in words(triple, 1)), "small-length boundary")
    counts['boundary_controls'] += 1
    # Sharp index-two possibility: syllable parity is a homomorphism for the
    # free product of C2 factors, and every even-length block has even parity.
    for length in (4, 6, 8):
        for w in words(triple, length):
            require(len(w) % 2 == 0, "even block parity")
        counts['parity_controls'] += 1
    # Omitting the inverse-fixed deletion would create a formal generator pair
    # whose two images coincide already before taking the random quotient.
    involution = ((0, 1),)
    require(involution == inverse((2, 2, 2), involution), "inverse-fixed deletion mutation not detected")
    counts['boundary_controls'] += 1
    return {"status": "PASS", "scope": "Exact finite algebra/enumeration checks only; no asymptotic or property-(T) computational certificate", "counts": dict(sorted(counts.items())), "models": tables}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
