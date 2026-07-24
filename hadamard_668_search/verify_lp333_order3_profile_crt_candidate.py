#!/usr/bin/env python3
"""Dependency-free exact replay for an LP(333) profile-CRT candidate.

The search model uses CP-SAT, but a candidate is not trusted through the
solver.  This module uses only the Python standard library and the exact
integer routines in this directory.  It reconstructs all 37 physical
Eisenstein correlations, checks the aggregate/energy/local conditions,
checks the primitive-nine ideal and all thirteen characteristic-37
transfer coefficients, and finally checks ``D_t=0`` coefficient by
coefficient.  A third reconstruction through the prime-167 physical-word
arithmetic is also required.  No CP-SAT result or serialized integer is
trusted.

Passing this verifier certifies only the 24-profile zero gate.  It is not a
labelled nine-row lift, an LP(333), or a Hadamard matrix of order 668.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, NoReturn, Sequence

from verify_lp333_order3_char37_transfer import (
    PROFILES,
    pair_signature,
    profile_norm,
    row_sum_targets,
    signed_profile_integer,
)
from verify_lp333_order3_profile9 import (
    audit_profile_table,
    profile_column_values,
    profile_correlation_table,
)
from verify_lp333_order3_profile_crt import (
    characteristic37_residual_transfer,
    exact_profile_residuals,
    invariant_parts,
)
from verify_lp333_order3_prime167_split import (
    P as PRIME167,
    exact_correlations as prime167_exact_correlations,
)


Target = tuple[int, int, int, int]
Identifiers = tuple[int, ...]


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def require_exact_int(value: object, label: str) -> int:
    """Accept a JSON/Python integer, but never a bool, float, or string."""

    if type(value) is not int:
        raise ValueError(f"{label} must be an exact integer")
    return value


def _reject_json_constant(value: str) -> NoReturn:
    raise ValueError(f"non-finite JSON number {value!r} is forbidden")


def _strict_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def strict_json_loads(text: str) -> object:
    """Load RFC-style JSON while rejecting duplicate keys and NaN tokens."""

    return json.loads(
        text,
        object_pairs_hook=_strict_json_object,
        parse_constant=_reject_json_constant,
    )


def _require_sequence(value: object, label: str) -> Sequence[object]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{label} must be a JSON array")
    return value


def _normalize_target(target: Sequence[int]) -> Target:
    result = tuple(
        require_exact_int(value, f"target[{index}]")
        for index, value in enumerate(_require_sequence(target, "target"))
    )
    if len(result) != 4:
        raise ValueError("the aggregate target must have four coordinates")
    return result  # type: ignore[return-value]


def _normalize_identifiers(identifiers: Sequence[int]) -> Identifiers:
    values = _require_sequence(identifiers, "profile identifiers")
    result = tuple(
        require_exact_int(value, f"profile_identifiers[{index}]")
        for index, value in enumerate(values)
    )
    if len(result) != 12:
        raise ValueError("each channel must contain twelve profile IDs")
    if any(not 0 <= value < len(PROFILES) for value in result):
        raise ValueError("a profile ID lies outside the ten-state catalog")
    return result


def aggregate_target(
    identifiers_a: Sequence[int], identifiers_b: Sequence[int]
) -> Target:
    result: list[int] = []
    for channel, identifiers in enumerate((identifiers_a, identifiers_b)):
        total = [0, 0]
        for class_index, profile_id in enumerate(identifiers):
            value = signed_profile_integer(
                channel, class_index, int(profile_id)
            )
            total[0] += value[0]
            total[1] += value[1]
        result.extend(total)
    return tuple(result)  # type: ignore[return-value]


def prime167_profile_replay(
    identifiers_a: Sequence[int], identifiers_b: Sequence[int]
) -> tuple[
    tuple[tuple[int, int], ...],
    tuple[tuple[int, int], ...],
]:
    """Return unadjusted and origin-adjusted prime-167 reconstructions."""

    a_ids = _normalize_identifiers(identifiers_a)
    b_ids = _normalize_identifiers(identifiers_b)
    correlations = prime167_exact_correlations(
        profile_column_values(0, a_ids),
        profile_column_values(1, b_ids),
    )
    adjusted = (
        (
            correlations[0][0] - PRIME167,
            correlations[0][1],
        ),
    ) + correlations[1:]
    return correlations, adjusted


def audit_profile_crt_candidate(
    target: Sequence[int],
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> dict[str, Any]:
    """Replay one purported profile-CRT survivor with exact arithmetic."""

    normalized_target = _normalize_target(target)
    a_ids = _normalize_identifiers(identifiers_a)
    b_ids = _normalize_identifiers(identifiers_b)
    if normalized_target not in set(row_sum_targets()):
        raise ValueError("the aggregate target is not one of the 22 shards")

    actual_target = aggregate_target(a_ids, b_ids)
    if actual_target != normalized_target:
        raise ValueError(
            f"aggregate mismatch: {actual_target} != {normalized_target}"
        )

    energy = sum(
        profile_norm(profile_id)
        for identifiers in (a_ids, b_ids)
        for profile_id in identifiers
    )
    if energy != 54:
        raise ValueError(f"profile energy is {energy}, not 54")

    local_signatures = []
    for pair_index in range(6):
        signature_a = pair_signature(
            a_ids[pair_index], a_ids[pair_index + 6]
        )
        signature_b = pair_signature(
            b_ids[pair_index], b_ids[pair_index + 6]
        )
        if signature_a != signature_b:
            raise ValueError(
                f"opposite-pair signature {pair_index} does not match"
            )
        local_signatures.append(signature_a)

    # Reconstruct the full physical word independently of CP-SAT.
    physical = exact_profile_residuals(a_ids, b_ids)
    parts = invariant_parts(physical)
    table = profile_correlation_table(a_ids, b_ids)
    if parts != table:
        raise AssertionError(
            "the two exact correlation reconstructions disagree"
        )

    ideal_audit = audit_profile_table(a_ids, b_ids)
    if ideal_audit["failing_nonzero_classes"]:
        raise ValueError("the primitive-nine profile ideal fails")
    if table[0] != (0, 0):
        raise ValueError("the energy/origin coefficient is nonzero")

    transfer = characteristic37_residual_transfer(a_ids, b_ids)
    if any(value != (0, 0) for value in transfer):
        raise ValueError(
            "at least one characteristic-37 transfer coefficient is nonzero"
        )

    nonzero_parts = tuple(
        (part_index, value)
        for part_index, value in enumerate(table)
        if value != (0, 0)
    )
    if nonzero_parts:
        raise ValueError(
            "the CRT layers passed but exact D_t=0 replay failed: "
            f"{nonzero_parts}"
        )

    # Third, independently routed replay.  This implementation reconstructs
    # the two length-37 words and their 37 correlations in the prime-167
    # module, rather than consuming either correlation table above.
    prime167_correlations, prime167_adjusted = prime167_profile_replay(
        a_ids, b_ids
    )
    if prime167_correlations[0] != (PRIME167, 0):
        raise ValueError("the prime-167 replay has the wrong origin energy")
    if any(
        value[0] % PRIME167 or value[1] % PRIME167
        for value in prime167_correlations
    ):
        raise ValueError("the prime-167 correlation replay is nonzero modulo 167")
    if any(value != (0, 0) for value in prime167_correlations[1:]):
        raise ValueError("the prime-167 exactness replay has a nonzero lag")
    if prime167_adjusted != physical:
        raise AssertionError(
            "the prime-167 and integer physical reconstructions disagree"
        )

    certificate = {
        "target": normalized_target,
        "profiles_a": a_ids,
        "profiles_b": b_ids,
        "energy": energy,
        "local_signatures": tuple(local_signatures),
        "correlation_parts": table,
        "characteristic37_transfer": transfer,
        "prime167_correlations": prime167_correlations,
    }
    return {
        **certificate,
        "physical_coefficients_checked": len(physical),
        "invariant_parts_checked": len(parts),
        "primitive9_nonzero_parts_checked": 12,
        "characteristic37_coefficients_checked": len(transfer),
        "prime167_physical_coefficients_checked": len(prime167_correlations),
        "prime167_modular_zero": True,
        "exact_zero_parts": all(value == (0, 0) for value in table),
        "certificate_sha256": compact_hash(certificate),
        "status": "profile_zero_gate_only",
    }


def load_candidate(path: Path) -> tuple[Target, Identifiers, Identifiers]:
    candidates = load_candidates(path)
    if not candidates:
        raise ValueError("candidate JSON contains no survivors")
    return candidates[0]


def _candidate_tuple(candidate: object, label: str) -> tuple[
    Target, Identifiers, Identifiers
]:
    if not isinstance(candidate, dict):
        raise ValueError(f"{label} must be an object")
    for key in ("target", "profiles_a", "profiles_b"):
        if key not in candidate:
            raise ValueError(f"{label} is missing {key!r}")
    return (
        _normalize_target(candidate["target"]),  # type: ignore[arg-type]
        _normalize_identifiers(candidate["profiles_a"]),  # type: ignore[arg-type]
        _normalize_identifiers(candidate["profiles_b"]),  # type: ignore[arg-type]
    )


def load_candidates(
    path: Path,
) -> tuple[tuple[Target, Identifiers, Identifiers], ...]:
    """Load either one legacy candidate or a v2 survivor catalog strictly."""

    payload = strict_json_loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("candidate JSON must be an object")
    if "survivors" in payload:
        survivors = _require_sequence(payload["survivors"], "survivors")
        if not survivors:
            raise ValueError("survivor catalog is empty")
        return tuple(
            _candidate_tuple(candidate, f"survivors[{index}]")
            for index, candidate in enumerate(survivors)
        )
    if "candidates" in payload:
        survivors = _require_sequence(payload["candidates"], "candidates")
        if not survivors:
            raise ValueError("candidate catalog is empty")
        return tuple(
            _candidate_tuple(candidate, f"candidates[{index}]")
            for index, candidate in enumerate(survivors)
        )
    return (_candidate_tuple(payload.get("candidate", payload), "candidate"),)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    candidates = load_candidates(args.candidate)
    results = tuple(
        audit_profile_crt_candidate(target, a_ids, b_ids)
        for target, a_ids, b_ids in candidates
    )
    print(f"survivors_replayed={len(results)}")
    for index, result in enumerate(results):
        print(
            f"survivor[{index}] target={result['target']} "
            f"certificate_sha256={result['certificate_sha256']}"
        )
    print("prime167_physical_coefficients_checked=37")
    print("PASS: exact dependency-free profile-CRT replay")
    print("STATUS: profile zero gate only; no labelled lift or H(668)")


if __name__ == "__main__":
    main()
