"""Independent exact JC Fourier tensors and graph-derived quartet invariants."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import itertools
import json
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from graph_model import RootedGraph, digest, stable_json, topological_order


Monomial = Tuple[int, ...]
Polynomial = Dict[Monomial, int]


def p_add(a: Polynomial, b: Polynomial, scale: int = 1) -> Polynomial:
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, 0) + scale * c
        if out[m] == 0: del out[m]
    return out


def p_mul(a: Polynomial, b: Polynomial) -> Polynomial:
    if not a or not b: return {}
    out = defaultdict(int)
    for x, c in a.items():
        for y, d in b.items(): out[tuple(i + j for i, j in zip(x, y))] += c * d
    return {m: c for m, c in out.items() if c}


def p_key(p: Polynomial):
    return tuple(sorted((m, c) for m, c in p.items()))


def p_hash(p: Polynomial):
    return digest([[list(m), c] for m, c in p_key(p)])


def jc_orbits4():
    reps = set()
    for g in itertools.product(range(4), repeat=4):
        if g[0] ^ g[1] ^ g[2] ^ g[3]: continue
        images = []
        for p in itertools.permutations((1, 2, 3)):
            mp = {0: 0, 1: p[0], 2: p[1], 3: p[2]}
            images.append(tuple(mp[x] for x in g))
        reps.add(min(images))
    out = tuple(sorted(reps))
    if len(out) != 15: raise AssertionError(len(out))
    return out


ORBITS4 = jc_orbits4()


def derive_quadratic_invariants():
    """All arm-multihomogeneous quadratic JC-orbit binomials.

    This family is derived from the character orbits and is deliberately
    independent of the project's historical 84-template family.
    """
    products = defaultdict(list)
    for i in range(15):
        for j in range(i, 15):
            degree = tuple(int(ORBITS4[i][k] != 0) + int(ORBITS4[j][k] != 0) for k in range(4))
            products[degree].append((i, j))
    inv = set()
    for degree, vals in products.items():
        for a, b in itertools.combinations(vals, 2):
            x, y = sorted((a, b))
            inv.add((x, y))
    out = tuple(sorted(inv))
    if len(out) != 162: raise AssertionError(len(out))
    for (a, b) in out:
        da = tuple(int(ORBITS4[a[0]][k] != 0) + int(ORBITS4[a[1]][k] != 0) for k in range(4))
        db = tuple(int(ORBITS4[b[0]][k] != 0) + int(ORBITS4[b[1]][k] != 0) for k in range(4))
        if da != db: raise AssertionError("non-multihomogeneous invariant")
    return out


INVARIANTS = derive_quadratic_invariants()


@dataclass(frozen=True)
class Descriptor:
    reticulation_count: int
    # One row per effective edge variable.  Entry is -1 when absent and a
    # selected-boundary bit mask when present in that switching.
    rows: Tuple[Tuple[int, ...], ...]

    @property
    def choice_count(self): return 1 << self.reticulation_count

    @property
    def variable_count(self): return len(self.rows) + self.reticulation_count

    @property
    def key(self): return (self.reticulation_count, self.rows)


def normalize_zero_sum_split_mask(mask: int, port_count: int,
                                  mode: str = "minimum") -> int:
    """Normalize an edge side on the zero-sum Fourier slice.

    For a zero-sum character assignment, the XOR on ``S`` equals the XOR on
    its complement.  The physical JC coordinate therefore sees an unordered
    split, not a rooted descendant side.  ``minimum`` is the locked canonical
    representative.  The other modes exist only for adversarial mutation
    tests and must never be used by an accepted audit.
    """
    if mask < 0:
        return -1
    full = (1 << port_count) - 1
    complement = full ^ mask
    if mode == "minimum":
        return min(mask, complement)
    if mode == "none":
        return mask
    if mode == "maximum":
        return max(mask, complement)
    if mode == "wrong_four_port_universe":
        # Deliberately invalid mutation: it complements only the first four
        # positions even when the descriptor has more selected ports.
        wrong_full = (1 << min(port_count, 4)) - 1
        return min(mask, wrong_full ^ mask)
    raise ValueError(("unknown split-complement normalization", mode))


def permute_descriptor(desc: Descriptor, old_to_new: Sequence[int]) -> Descriptor:
    def pmask(mask):
        if mask < 0: return -1
        out = 0
        for old, new in enumerate(old_to_new):
            if mask >> old & 1: out |= 1 << new
        return normalize_zero_sum_split_mask(out, len(old_to_new), "minimum")
    return Descriptor(desc.reticulation_count, tuple(sorted(tuple(pmask(x) for x in row) for row in desc.rows)))


def canonical_descriptor_key(desc: Descriptor):
    """Quotient harmless reticulation ordering and parent-choice flips."""
    r = desc.reticulation_count
    best = None
    for permutation in itertools.permutations(range(r)):
        for flips in itertools.product((0, 1), repeat=r):
            old_column_for_new = []
            for new_bits in itertools.product((0, 1), repeat=r):
                old_bits = [0] * r
                for new_axis, old_axis in enumerate(permutation):
                    old_bits[old_axis] = new_bits[new_axis] ^ flips[old_axis]
                column = 0
                for bit in old_bits:
                    column = (column << 1) | bit
                old_column_for_new.append(column)
            rows = tuple(sorted(
                tuple(row[column] for column in old_column_for_new)
                for row in desc.rows
            ))
            key = (r, rows)
            if best is None or key < best:
                best = key
    return best


def descriptor_from_graph(g: RootedGraph,
                          split_complement_mode: str = "minimum") -> Descriptor:
    lm = g.label_map
    selected = sorted((int(c.split("_")[1]), v) for v, c in lm.items() if c.startswith("L_"))
    if [i for i, _ in selected] != list(range(len(selected))): raise ValueError("nonconsecutive selected labels")
    selected_index = {v: i for i, v in selected}
    indeg, outdeg, children0, parents0 = g.degrees()
    retics = sorted(v for v in g.vertices if (indeg[v], outdeg[v]) == (2, 1))
    parent_order = {r: tuple(sorted(parents0[r])) for r in retics}
    all_arcs = tuple(sorted(g.arcs)); rows = []
    for choice in itertools.product((0, 1), repeat=len(retics)):
        kept = set(all_arcs)
        for r, bit in zip(retics, choice):
            ps = parent_order[r]
            kept.discard((ps[1 - bit], r))
        children = defaultdict(list)
        for u, v in kept: children[u].append(v)
        topo = topological_order(RootedGraph.make(kept, g.root, lm))
        masks = {v: (1 << selected_index[v] if v in selected_index else 0) for v in g.vertices}
        for v in reversed(topo):
            for c in children[v]: masks[v] |= masks[c]
        rows.append({e: masks[e[1]] for e in kept})
    edge_rows = []
    for e in all_arcs:
        row = tuple(
            normalize_zero_sum_split_mask(
                rows[c].get(e, -1), len(selected), split_complement_mode,
            )
            for c in range(len(rows))
        )
        # A retained zero-mask edge and an absent edge are both invisible to
        # every selected Fourier coordinate.  Entirely invisible rows vanish.
        if all(x in (-1, 0) for x in row): continue
        edge_rows.append(row)
    # Edges with the same complete switching-mask row enter only through their
    # product.  This exact zipping is an open-cube submersion.
    return Descriptor(len(retics), tuple(sorted(set(edge_rows))))


def assignment_xor(mask: int, assignment: Sequence[int]) -> int:
    x = 0; i = 0
    while mask:
        if mask & 1: x ^= assignment[i]
        mask >>= 1; i += 1
    return x


def coordinate_poly(desc: Descriptor, assignment: Sequence[int]) -> Polynomial:
    E, R = len(desc.rows), desc.reticulation_count
    nvar = E + R; out = {}
    for ci, bits in enumerate(itertools.product((0, 1), repeat=R)):
        exp = [0] * nvar
        for ei, row in enumerate(desc.rows):
            mask = row[ci]
            if mask >= 0 and assignment_xor(mask, assignment) != 0: exp[ei] = 1
        weight = {tuple(exp): 1}
        for ri, bit in enumerate(bits):
            idx = E + ri
            if bit == 0:  # lambda
                nxt = {}
                for m, c in weight.items():
                    z = list(m); z[idx] += 1; nxt[tuple(z)] = nxt.get(tuple(z), 0) + c
                weight = nxt
            else:  # 1-lambda
                nxt = {}
                for m, c in weight.items():
                    nxt[m] = nxt.get(m, 0) + c
                    z = list(m); z[idx] += 1; z = tuple(z); nxt[z] = nxt.get(z, 0) - c
                weight = {m: c for m, c in nxt.items() if c}
        out = p_add(out, weight)
    return out


def quartet_coordinates(desc: Descriptor, quartet: Sequence[int]) -> Tuple[Polynomial, ...]:
    m = max((max(quartet) + 1), max((max(x for x in row if x >= 0).bit_length() for row in desc.rows), default=0))
    ans = []
    for q in ORBITS4:
        a = [0] * m
        for leaf, val in zip(quartet, q): a[leaf] = val
        ans.append(coordinate_poly(desc, a))
    return tuple(ans)


def invariant_poly(coords: Sequence[Polynomial], invariant_index: int) -> Polynomial:
    a, b = INVARIANTS[invariant_index]
    return p_add(p_mul(coords[a[0]], coords[a[1]]), p_mul(coords[b[0]], coords[b[1]]), -1)


def _eval_coordinate_mod(desc: Descriptor, assignment: Sequence[int], prime: int, seed: int, trial: int):
    h = hashlib.sha256(stable_json([desc.key, seed, trial]).encode()).digest()
    vals = []
    for i in range(desc.variable_count):
        off = (2 * i) % 30
        vals.append(2 + int.from_bytes(h[off:off + 2], "big") % (prime - 3))
    E, R = len(desc.rows), desc.reticulation_count; total = 0
    for ci, bits in enumerate(itertools.product((0, 1), repeat=R)):
        z = 1
        for ei, row in enumerate(desc.rows):
            mask = row[ci]
            if mask >= 0 and assignment_xor(mask, assignment) != 0: z = (z * vals[ei]) % prime
        for ri, bit in enumerate(bits):
            lam = vals[E + ri]
            z = z * (lam if bit == 0 else (1 - lam)) % prime
        total = (total + z) % prime
    return total


def quartet_values_mod(desc: Descriptor, quartet: Sequence[int], port_count: int,
                        prime: int, trial: int, seed: int = 9173):
    vals = []
    for q in ORBITS4:
        a = [0] * port_count
        for leaf, val in zip(quartet, q): a[leaf] = val
        vals.append(_eval_coordinate_mod(desc, a, prime, seed, trial))
    return tuple(vals)


_DECK_CACHE = {}


def exact_deck(desc: Descriptor, port_count: int):
    """Exact zero/nonzero deck over every unordered physical quartet."""
    key = (desc.key, port_count)
    if key in _DECK_CACHE: return _DECK_CACHE[key]
    primes = (1000003, 1000033, 1000037)
    deck = []
    for quartet in itertools.combinations(range(port_count), 4):
        maybe_zero = set(range(len(INVARIANTS)))
        for trial, prime in enumerate(primes):
            vals = []
            for q in ORBITS4:
                a = [0] * port_count
                for leaf, val in zip(quartet, q): a[leaf] = val
                vals.append(_eval_coordinate_mod(desc, a, prime, 9173, trial))
            nonzero = set()
            for ii, (a, b) in enumerate(INVARIANTS):
                v = (vals[a[0]] * vals[a[1]] - vals[b[0]] * vals[b[1]]) % prime
                if v: nonzero.add(ii)
            maybe_zero -= nonzero
            if not maybe_zero: break
        bits = (1 << len(INVARIANTS)) - 1
        if maybe_zero:
            coords = quartet_coordinates(desc, quartet)
            for ii in maybe_zero:
                if not invariant_poly(coords, ii): bits &= ~(1 << ii)
        deck.append((quartet, bits))
    out = tuple(deck); _DECK_CACHE[key] = out; return out


def deck_hash(deck):
    return digest([[list(q), format(bits, "x")] for q, bits in deck])


def first_difference(source_deck, target_deck):
    if tuple(q for q, _ in source_deck) != tuple(q for q, _ in target_deck): raise ValueError("quartet key mismatch")
    for chunk, ((q, s), (_, t)) in enumerate(zip(source_deck, target_deck)):
        source_only = s & ~t
        if source_only:
            ii = (source_only & -source_only).bit_length() - 1
            return "source_only", q, ii, chunk
    for chunk, ((q, s), (_, t)) in enumerate(zip(source_deck, target_deck)):
        target_only = t & ~s
        if target_only:
            return "target_only", q, tuple(i for i in range(len(INVARIANTS)) if target_only >> i & 1), chunk
    return "equal", None, None, None


def quick_strict_sign(poly: Polynomial):
    if not poly: return None
    vals = set(poly.values())
    if all(c > 0 for c in vals): return 1
    if all(c < 0 for c in vals): return -1
    return None


def strict_target_witness(desc: Descriptor, quartet, candidates):
    coords = quartet_coordinates(desc, quartet)
    for ii in candidates:
        poly = invariant_poly(coords, ii)
        sign = quick_strict_sign(poly)
        if sign:
            return {"invariant": ii, "sign": sign, "polynomial_sha256": p_hash(poly), "term_count": len(poly)}
    return None
