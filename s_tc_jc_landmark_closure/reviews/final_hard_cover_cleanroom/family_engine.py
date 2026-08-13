"""Exact zero decks and strict signs for independently derived relations."""

from __future__ import annotations

import itertools
from typing import Dict, Sequence, Tuple

from derived_invariants import exact_relation_pullback, relation_poly, relation_value
from jc_exact import p_add, p_mul
from graph_model import digest
from jc_exact import quartet_values_mod, p_hash


PRIMES = (1000003, 1000033, 1000037)
_CACHE = {}
_MOD_CACHE = {}
_EXACT_PULLBACK_CACHE = {}
_POLY_CONTEXT_CACHE = {}
_SOURCE_MOD_BITS_CACHE = {}


def _cached_pullback(desc, quartet, relation):
    key = (desc.key, tuple(quartet))
    if key not in _POLY_CONTEXT_CACHE:
        from jc_exact import quartet_coordinates
        _POLY_CONTEXT_CACHE[key] = (quartet_coordinates(desc, quartet), {})
    coords, monomial_cache = _POLY_CONTEXT_CACHE[key]
    poly = {}
    for coefficient, mon in relation:
        if mon not in monomial_cache:
            value = {tuple([0] * desc.variable_count): 1}
            for coordinate in mon: value = p_mul(value, coords[coordinate])
            monomial_cache[mon] = value
        poly = p_add(poly, monomial_cache[mon], coefficient)
    return poly


def exact_family_deck(desc, port_count: int, family):
    key = (desc.key, port_count, len(family), digest(family))
    if key in _CACHE: return _CACHE[key]
    out = []
    all_indices = set(range(len(family)))
    for quartet in itertools.combinations(range(port_count), 4):
        maybe_zero = set(all_indices); nonzero = set()
        for trial, prime in enumerate(PRIMES):
            vals = quartet_values_mod(desc, quartet, port_count, prime, trial)
            for i in tuple(maybe_zero):
                if relation_value(vals, family[i], prime):
                    maybe_zero.remove(i); nonzero.add(i)
            if not maybe_zero: break
        coords = None; monomial_cache = {}
        for i in maybe_zero:
            if coords is None:
                from jc_exact import quartet_coordinates
                coords = quartet_coordinates(desc, quartet)
            poly = {}
            for coefficient, mon in family[i]:
                if mon not in monomial_cache:
                    value = {tuple([0] * desc.variable_count): 1}
                    for coordinate in mon: value = p_mul(value, coords[coordinate])
                    monomial_cache[mon] = value
                poly = p_add(poly, monomial_cache[mon], coefficient)
            if poly: nonzero.add(i)
        bits = 0
        for i in nonzero: bits |= 1 << i
        out.append((quartet, bits))
    ans = tuple(out); _CACHE[key] = ans; return ans


def bit_indices(bits: int):
    while bits:
        one = bits & -bits
        yield one.bit_length() - 1
        bits -= one


def differences(source_deck, target_deck):
    source_only = []; target_only = []
    for chunk, ((q, s), (_, t)) in enumerate(zip(source_deck, target_deck)):
        source_only.extend((chunk, q, i) for i in bit_indices(s & ~t))
        target_only.extend((chunk, q, i) for i in bit_indices(t & ~s))
    return source_only, target_only


def independent_strict_sign(desc, quartet, relation):
    """Sound exact open-cube sign proof from power coefficients.

    This sufficient test accepts no primary sign flag.  Mixed coefficients are
    returned unresolved for the later factor/Bernstein pass.
    """
    poly = exact_relation_pullback(desc, quartet, relation)
    if not poly: return None
    if all(c > 0 for c in poly.values()): sign = 1
    elif all(c < 0 for c in poly.values()): sign = -1
    else: return None
    return {"sign": sign, "term_count": len(poly), "polynomial_sha256": p_hash(poly)}


def first_independent_strict_sign(desc, quartet, family, candidate_indices):
    for i in candidate_indices:
        poly = _cached_pullback(desc, quartet, family[i])
        if not poly: continue
        if all(c > 0 for c in poly.values()): sign = 1
        elif all(c < 0 for c in poly.values()): sign = -1
        else: continue
        return {"invariant": i, "sign": sign, "term_count": len(poly), "polynomial_sha256": p_hash(poly)}
    return None


def modular_nonzero_deck(desc, port_count: int, family):
    key = (desc.key, port_count, len(family), digest(family))
    if key in _MOD_CACHE: return _MOD_CACHE[key]
    ans = []
    for quartet in itertools.combinations(range(port_count), 4):
        bits = 0
        for trial, prime in enumerate(PRIMES):
            vals = quartet_values_mod(desc, quartet, port_count, prime, trial)
            for i, rel in enumerate(family):
                if not (bits >> i & 1) and relation_value(vals, rel, prime): bits |= 1 << i
        ans.append((quartet, bits))
    out = tuple(ans); _MOD_CACHE[key] = out; return out


def _modular_bits_for_quartet(desc, quartet, port_count, family):
    key = (desc.key, tuple(quartet), port_count, len(family), digest(family))
    if key in _SOURCE_MOD_BITS_CACHE: return _SOURCE_MOD_BITS_CACHE[key]
    bits = 0
    for trial, prime in enumerate(PRIMES):
        vals = quartet_values_mod(desc, quartet, port_count, prime, trial)
        for i, rel in enumerate(family):
            if not (bits >> i & 1) and relation_value(vals, rel, prime): bits |= 1 << i
    _SOURCE_MOD_BITS_CACHE[key] = bits
    return bits


def find_generic_identity_separator(source_desc, target_desc, port_count: int, family):
    """Find target-zero/source-nonzero without expanding a full source deck."""
    target_mod = modular_nonzero_deck(target_desc, port_count, family)
    all_bits = (1 << len(family)) - 1
    for quartet, target_nonzero in target_mod:
        possible_target_zeros = all_bits & ~target_nonzero
        if not possible_target_zeros: continue
        source_nonzero = _modular_bits_for_quartet(
            source_desc, quartet, port_count, family,
        )
        candidates = possible_target_zeros & source_nonzero
        for invariant in bit_indices(candidates):
            target_poly = _cached_pullback(target_desc, quartet, family[invariant])
            if target_poly: continue
            source_poly = _cached_pullback(source_desc, quartet, family[invariant])
            if not source_poly:
                # A modular nonzero evaluation made this branch impossible;
                # retain the assertion rather than silently continuing.
                raise AssertionError("modular source witness expanded to zero")
            return {
                "classification": "generic_identity_separation",
                "quartet": quartet,
                "invariant": invariant,
                "source_polynomial_sha256": p_hash(source_poly),
                "target_zero": True,
            }
    return None


def find_generic_identity_separator_on_quartet(source_desc, target_desc,
                                                quartet, port_count: int,
                                                family):
    """Exact target-zero/source-nonzero witness on one prescribed quartet."""
    quartet = tuple(quartet)
    target_nonzero = _modular_bits_for_quartet(
        target_desc, quartet, port_count, family,
    )
    source_nonzero = _modular_bits_for_quartet(
        source_desc, quartet, port_count, family,
    )
    candidates = source_nonzero & ~target_nonzero
    for invariant in bit_indices(candidates):
        target_poly = _cached_pullback(
            target_desc, quartet, family[invariant],
        )
        if target_poly:
            continue
        source_poly = _cached_pullback(
            source_desc, quartet, family[invariant],
        )
        if not source_poly:
            raise AssertionError("modular source witness expanded to zero")
        return {
            "classification": "generic_identity_separation",
            "quartet": quartet,
            "invariant": invariant,
            "source_polynomial_sha256": p_hash(source_poly),
            "target_zero": True,
        }
    return None


def _exact_nonzero(desc, quartet, family, i):
    key = (desc.key, tuple(quartet), i, len(family), digest(family))
    if key not in _EXACT_PULLBACK_CACHE:
        _EXACT_PULLBACK_CACHE[key] = bool(_cached_pullback(desc, quartet, family[i]))
    return _EXACT_PULLBACK_CACHE[key]


def classify_containment_pair(source_deck, target_desc, port_count: int, family):
    """Fail-closed directed screen optimized for early exact identities."""
    mod = modular_nonzero_deck(target_desc, port_count, family)
    # A modularly nonzero value is an exact certificate of nonidentity.  Only
    # modular zeros that could be target identities are expanded.
    for chunk, ((q, sbits), (_, mbits)) in enumerate(zip(source_deck, mod)):
        possible = sbits & ~mbits
        for i in bit_indices(possible):
            if not _exact_nonzero(target_desc, q, family, i):
                poly = exact_relation_pullback(target_desc, q, family[i])
                return {"classification": "generic_identity_separation", "quartet": q, "invariant": i, "target_zero": not bool(poly)}
    # Try independently proved strict signs among already certified target-only
    # relations before paying for the complete exact target deck.
    for chunk, ((q, sbits), (_, mbits)) in enumerate(zip(source_deck, mod)):
        candidates = tuple(bit_indices(mbits & ~sbits))
        if candidates:
            witness = first_independent_strict_sign(target_desc, q, family, candidates)
            if witness:
                witness.update({"classification": "strict_sign_separation", "quartet": q})
                return witness
    target_deck = exact_family_deck(target_desc, port_count, family)
    source_only, target_only = differences(source_deck, target_deck)
    if source_only:
        chunk, q, i = source_only[0]
        return {"classification": "generic_identity_separation", "quartet": q, "invariant": i, "target_zero": True}
    by_quartet = {}
    for _, q, i in target_only: by_quartet.setdefault(tuple(q), []).append(i)
    for q, candidates in by_quartet.items():
        witness = first_independent_strict_sign(target_desc, q, family, candidates)
        if witness:
            witness.update({"classification": "strict_sign_separation", "quartet": q})
            return witness
    return {
        "classification": "equal_deck" if not target_only else "unequal_necessary",
        "target_only_unsigned_count": len(target_only),
        "target_deck": target_deck,
    }
