#!/usr/bin/env python3
"""Search universal wrong-split K3P cut-minor sign certificates.

For each graph-derived one-active target direction, compile all 144 two-by-two
minors of the four 4x4 Fourier character blocks for the normalized split
01|23.  A coefficientwise strict sign in positive edge-spectrum and
inheritance variables proves the target minor cannot vanish anywhere in the
strict positive domain.  This is a discovery pass; a promoted certificate
requires independent graph, polynomial, and domain replay.
"""

from __future__ import annotations

import collections
import fractions
import hashlib
import itertools
import json
import math
from pathlib import Path

import explore_crossbridge_atlas as cross
import numpy as np


HERE = Path(__file__).resolve().parent
RECORD_DIRECTORY = HERE / "cut_minor_sign_records"
atlas = cross.atlas


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def minor_polynomial(outputs, index, character_sum, rows, columns):
    r0, r1 = rows
    c0, c1 = columns
    a = index[(r0, character_sum ^ r0, c0, character_sum ^ c0)]
    b = index[(r1, character_sum ^ r1, c1, character_sum ^ c1)]
    c = index[(r0, character_sum ^ r0, c1, character_sum ^ c1)]
    d = index[(r1, character_sum ^ r1, c0, character_sum ^ c0)]
    return atlas.sparse_lincomb(
        [atlas.sparse_mul(outputs[a], outputs[b]), atlas.sparse_mul(outputs[c], outputs[d])],
        [1, -1],
    ), (a, b, c, d)


def coefficient_sign(polynomial):
    coefficients = [value for value in polynomial.values() if value]
    if coefficients and all(value > 0 for value in coefficients):
        return 1
    if coefficients and all(value < 0 for value in coefficients):
        return -1
    return 0


def inheritance_bernstein_sign(polynomial, edge_width, inheritance_count):
    """Certify one global sign after Bernstein conversion only in lambdas."""
    if inheritance_count == 0:
        sign = coefficient_sign(polynomial)
        return None if not sign else {
            "sign": sign,
            "degrees": [],
            "coefficient_count": len(polynomial),
            "minimum": str(min(polynomial.values())),
            "maximum": str(max(polynomial.values())),
        }
    degrees = tuple(
        max(exponent[edge_width + axis] for exponent in polynomial)
        for axis in range(inheritance_count)
    )
    grouped = collections.defaultdict(lambda: collections.defaultdict(fractions.Fraction))
    for exponent, coefficient in polynomial.items():
        edge_exponent = exponent[:edge_width]
        inheritance_exponent = exponent[edge_width:]
        grouped[edge_exponent][inheritance_exponent] += coefficient
    bernstein = []
    for edge_exponent, power in grouped.items():
        for beta in itertools.product(*(range(degree + 1) for degree in degrees)):
            value = fractions.Fraction(0)
            for alpha, coefficient in power.items():
                if all(alpha[axis] <= beta[axis] for axis in range(inheritance_count)):
                    multiplier = fractions.Fraction(1)
                    for axis, degree in enumerate(degrees):
                        multiplier *= fractions.Fraction(
                            math.comb(beta[axis], alpha[axis]),
                            math.comb(degree, alpha[axis]),
                        )
                    value += coefficient * multiplier
            bernstein.append((edge_exponent, beta, value))
    values = [value for _, _, value in bernstein]
    sign = 1 if values and all(value >= 0 for value in values) and any(value > 0 for value in values) else 0
    if not sign and values and all(value <= 0 for value in values) and any(value < 0 for value in values):
        sign = -1
    if not sign:
        return None
    return {
        "sign": sign,
        "degrees": list(degrees),
        "coefficient_count": len(values),
        "negative": sum(value < 0 for value in values),
        "zero": sum(value == 0 for value in values),
        "positive": sum(value > 0 for value in values),
        "minimum": str(min(values)),
        "maximum": str(max(values)),
        "ordered_coefficients_sha256": digest(
            [[list(edge), list(beta), str(value)] for edge, beta, value in bernstein]
        ),
    }


def full_bernstein_sign(polynomial, cap=2_000_000):
    """Exact tensor Bernstein sign on the open unit cube."""
    width = len(next(iter(polynomial)))
    active = tuple(
        axis
        for axis in range(width)
        if len({exponent[axis] for exponent in polynomial}) > 1
    )
    if not active:
        sign = coefficient_sign(polynomial)
        if not sign:
            return None
        value = next(iter(polynomial.values()))
        return {
            "sign": sign,
            "active_parameter_indices": [],
            "degrees": [],
            "coefficient_count": 1,
            "negative": int(value < 0),
            "zero": 0,
            "positive": int(value > 0),
            "minimum": str(value),
            "maximum": str(value),
            "ordered_coefficients_sha256": digest([str(value)]),
        }
    reduced = collections.defaultdict(int)
    for exponent, coefficient in polynomial.items():
        reduced[tuple(exponent[axis] for axis in active)] += coefficient
    reduced = {exponent: coefficient for exponent, coefficient in reduced.items() if coefficient}
    degrees = tuple(max(exponent[axis] for exponent in reduced) for axis in range(len(active)))
    count = math.prod(degree + 1 for degree in degrees)
    if count > cap:
        return None
    # Every present degree is one or two.  Apply the power-to-Bernstein
    # transform axis by axis with one common power-of-two denominator.  This
    # is exact integer arithmetic and avoids millions of Fraction objects.
    if any(degree not in (1, 2) for degree in degrees):
        return None
    values = np.zeros(tuple(degree + 1 for degree in degrees), dtype=np.int64)
    for exponent, coefficient in reduced.items():
        values[exponent] += int(coefficient)
    denominator_power = 0
    for axis, degree in enumerate(degrees):
        moved = np.moveaxis(values, axis, 0)
        old = moved.copy()
        if degree == 1:
            moved[0] = old[0]
            moved[1] = old[0] + old[1]
        else:
            moved[0] = 2 * old[0]
            moved[1] = 2 * old[0] + old[1]
            moved[2] = 2 * (old[0] + old[1] + old[2])
            denominator_power += 1
        values = np.moveaxis(moved, 0, axis)
        if np.max(np.abs(values)) >= 2**61:
            return None
    flat = values.reshape(-1)
    sign = 1 if np.all(flat >= 0) and np.any(flat > 0) else 0
    if not sign and np.all(flat <= 0) and np.any(flat < 0):
        sign = -1
    if not sign:
        return None
    coefficient_hash = hashlib.sha256()
    coefficient_hash.update(flat.astype("<i8", copy=False).tobytes())
    coefficient_hash.update(str(denominator_power).encode())
    return {
        "sign": sign,
        "active_parameter_indices": list(active),
        "degrees": list(degrees),
        "coefficient_count": int(flat.size),
        "common_denominator": f"2^{denominator_power}",
        "negative": int(np.count_nonzero(flat < 0)),
        "zero": int(np.count_nonzero(flat == 0)),
        "positive": int(np.count_nonzero(flat > 0)),
        "minimum_numerator": str(int(np.min(flat))),
        "maximum_numerator": str(int(np.max(flat))),
        "ordered_numerators_sha256": coefficient_hash.hexdigest(),
    }


def atomic_write_json(path: Path, value) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def factor_positive_monomial(polynomial):
    width = len(next(iter(polynomial)))
    common = tuple(min(exponent[i] for exponent in polynomial) for i in range(width))
    reduced = collections.defaultdict(int)
    for exponent, coefficient in polynomial.items():
        reduced[tuple(value - common[i] for i, value in enumerate(exponent))] += coefficient
    return common, {exponent: coefficient for exponent, coefficient in reduced.items() if coefficient}


def main() -> None:
    _, _, _, targets = cross.build_universes()
    assignments = atlas.k3p_assignments(4)
    index = {assignment: position for position, assignment in enumerate(assignments)}
    pairs = tuple((left, right) for left in range(4) for right in range(left + 1, 4))
    RECORD_DIRECTORY.mkdir(exist_ok=True)
    records = []
    unsolved = []
    for target_index, row in enumerate(targets):
        record_path = RECORD_DIRECTORY / f"{target_index:03d}.json"
        if record_path.exists():
            public = json.loads(record_path.read_text())
            records.append(public)
            if public["certificate"] is None:
                unsolved.append(target_index)
            print(
                json.dumps(
                    {
                        "target": target_index,
                        "record_id": public["record_id"],
                        "certificates": public["certificate_count"],
                        "resumed": True,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            continue
        descriptor = row["descriptor"]
        outputs = atlas.output_sparse_polynomials(descriptor)
        candidates = []
        pending = []
        for character_sum in range(4):
            for rows in pairs:
                for columns in pairs:
                    polynomial, coordinates = minor_polynomial(
                        outputs, index, character_sum, rows, columns
                    )
                    if not polynomial:
                        continue
                    common, reduced = factor_positive_monomial(polynomial)
                    varying = tuple(
                        axis
                        for axis in range(len(next(iter(reduced))))
                        if len({exponent[axis] for exponent in reduced}) > 1
                    )
                    degrees = tuple(
                        max(exponent[axis] for exponent in reduced)
                        for axis in varying
                    )
                    bernstein_count = math.prod(degree + 1 for degree in degrees)
                    sign = coefficient_sign(reduced)
                    bernstein = inheritance_bernstein_sign(
                        reduced,
                        3 * descriptor.edge_class_count,
                        descriptor.retic_count,
                    )
                    if sign or bernstein is not None:
                        certified_sign = sign if sign else bernstein["sign"]
                        candidates.append(
                            {
                                "character_sum": character_sum,
                                "rows": list(rows),
                                "columns": list(columns),
                                "coordinate_indices": list(coordinates),
                                "sign": certified_sign,
                                "method": (
                                    "coefficientwise"
                                    if sign
                                    else "edge-monomial coefficientwise plus inheritance Bernstein"
                                ),
                                "term_count": len(reduced),
                                "positive_monomial_exponent": list(common),
                                "reduced_polynomial_sha256": digest(
                                    [[list(exponent), str(coefficient)] for exponent, coefficient in sorted(reduced.items())]
                                ),
                                "inheritance_bernstein": bernstein,
                                "full_bernstein": None,
                            }
                        )
                    else:
                        pending.append(
                            (
                                bernstein_count,
                                character_sum,
                                rows,
                                columns,
                                coordinates,
                                common,
                                reduced,
                            )
                        )
        if not candidates:
            pending.sort(key=lambda item: (item[0], item[1], item[2], item[3]))
            for (
                bernstein_count,
                character_sum,
                rows,
                columns,
                coordinates,
                common,
                reduced,
            ) in pending:
                if bernstein_count > 2_000_000:
                    break
                full_bernstein = full_bernstein_sign(reduced)
                if full_bernstein is None:
                    continue
                candidates.append(
                    {
                        "character_sum": character_sum,
                        "rows": list(rows),
                        "columns": list(columns),
                        "coordinate_indices": list(coordinates),
                        "sign": full_bernstein["sign"],
                        "method": "exact full tensor Bernstein on the open unit cube",
                        "term_count": len(reduced),
                        "positive_monomial_exponent": list(common),
                        "reduced_polynomial_sha256": digest(
                            [[list(exponent), str(coefficient)] for exponent, coefficient in sorted(reduced.items())]
                        ),
                        "inheritance_bernstein": None,
                        "full_bernstein": full_bernstein,
                    }
                )
                break
        candidates.sort(
            key=lambda item: (
                item["term_count"],
                item["character_sum"],
                item["rows"],
                item["columns"],
            )
        )
        public = {
            "target_index": target_index,
            "record_id": row["record_id"],
            "old_split": row["old_split"],
            "old_order": row["old_order"],
            "reticulation_count": row["reticulation_count"],
            "descriptor_sha256": cross.digest(cross.descriptor_payload(descriptor)),
            "certificate": None if not candidates else candidates[0],
            "certificate_count": len(candidates),
        }
        records.append(public)
        if not candidates:
            unsolved.append(target_index)
        atomic_write_json(record_path, public)
        print(
            json.dumps(
                {
                    "target": target_index,
                    "record_id": row["record_id"],
                    "certificates": len(candidates),
                    "best_terms": None if not candidates else candidates[0]["term_count"],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    payload = {
        "schema": "k3p-one-active-cut-minor-sign-search-v1",
        "status": "DISCOVERY_COMPLETE" if not unsolved else "PARTIAL_DISCOVERY",
        "method": (
            "coefficientwise or exact tensor Bernstein on the open unit cube, "
            "after a positive monomial factor"
        ),
        "domain": "independent positive edge spectra and positive inheritance variables; hence D3+",
        "target_directions": len(targets),
        "solved": len(targets) - len(unsolved),
        "unsolved_target_indices": unsolved,
        "records": records,
    }
    atomic_write_json(HERE / "CUT_MINOR_SIGN_SEARCH.json", payload)
    print(json.dumps({key: payload[key] for key in ("status", "target_directions", "solved", "unsolved_target_indices")}, sort_keys=True))


if __name__ == "__main__":
    main()
