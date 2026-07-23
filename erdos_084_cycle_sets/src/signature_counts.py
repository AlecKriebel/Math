#!/usr/bin/env python3
"""Exact reference enumerator for the protected signature construction.

The implementation deliberately uses direct finite-set semantics and Python
integers as bitsets. It is intended as a readable reference, not as the final
high-performance discovery engine.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Mapping, MutableMapping, Set


def set_bits(mask: int) -> Iterator[int]:
    """Yield zero-based indices of set bits."""
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def value_bit(k: int, value: int) -> int:
    if not -k <= value <= k:
        raise ValueError(f"{value=} lies outside [-{k},{k}]")
    return 1 << (value + k)


def p_elements(k: int, p_mask: int) -> Iterator[int]:
    """Decode P subset [2k] from a zero-based bit mask."""
    for index in set_bits(p_mask):
        if index >= 2 * k:
            raise ValueError(f"P mask has a bit outside [2k]: {p_mask}")
        yield index + 1


def generator_mask(k: int, p_mask: int, b: int) -> int:
    """Return G_{k,P}(b) as a bit mask on [-k,k]."""
    if b == 0 or not -k <= b <= k:
        raise ValueError(f"b must lie in J_k, received {b}")

    result = value_bit(k, b) | value_bit(k, -b)
    for p in p_elements(k, p_mask):
        value = b - p
        if -k <= value <= k:
            result |= value_bit(k, value)
    return result


def signed_indices(k: int) -> List[int]:
    return list(range(-k, 0)) + list(range(1, k + 1))


def union_closure(generators: Iterable[int]) -> Set[int]:
    """All unions of a finite list of bit-mask generators."""
    family: Set[int] = {0}
    for generator in dict.fromkeys(generators):
        previous = tuple(family)
        family.update(signature | generator for signature in previous)
    return family


def signature_family(k: int, p_mask: int) -> Set[int]:
    return union_closure(
        generator_mask(k, p_mask, b) for b in signed_indices(k)
    )


def v_mask(k: int, p_mask: int, alpha: int) -> int:
    """Return V_alpha(P) on [-k,k]."""
    if alpha not in (0, 1):
        raise ValueError("alpha must be 0 or 1")
    result = 0
    for p in p_elements(k, p_mask):
        result |= value_bit(k, k + 1 - p)
    if alpha:
        result |= value_bit(k, -k)
    return result


def safe_generators(k: int, p_mask: int) -> Dict[int, int]:
    """Generators whose masks avoid -k."""
    forbidden = value_bit(k, -k)
    result: Dict[int, int] = {}
    for b in signed_indices(k):
        generator = generator_mask(k, p_mask, b)
        if not generator & forbidden:
            result[b] = generator
    return result


def restricted_witness_fibers(
    k: int, p_mask: int
) -> Mapping[int, int]:
    """Multiplicity of signatures from at most one of +/-t for each t<k."""
    safe = safe_generators(k, p_mask)
    fibers: MutableMapping[int, int] = {0: 1}

    for t in range(1, k):
        options = [0]
        if t in safe:
            options.append(safe[t])
        if -t in safe:
            options.append(safe[-t])

        next_fibers: MutableMapping[int, int] = defaultdict(int)
        for signature, multiplicity in fibers.items():
            for option in options:
                next_fibers[signature | option] += multiplicity
        fibers = next_fibers

    return dict(fibers)


@dataclass(frozen=True)
class Statistics:
    k: int
    s: int
    e: int
    trace_total: int
    restricted_witnesses: int
    restricted_collision_energy: int
    restricted_distinct_outputs: int
    restricted_max_fiber: int

    @property
    def normalized_s(self) -> float:
        return self.s / (8**self.k)

    @property
    def normalized_trace(self) -> float:
        return self.trace_total / (8**self.k)

    @property
    def size_biased_collision(self) -> float:
        if not self.restricted_witnesses:
            return 0.0
        return self.restricted_collision_energy / self.restricted_witnesses

    def to_json(self) -> dict:
        data = asdict(self)
        data.update(
            normalized_s=self.normalized_s,
            normalized_trace=self.normalized_trace,
            size_biased_collision=self.size_biased_collision,
        )
        return data


def statistics(k: int, verify_trace_equivalence: bool = False) -> Statistics:
    s_total = 0
    e_total = 0
    trace_total = 0
    witness_total = 0
    collision_total = 0
    restricted_distinct_total = 0
    max_fiber = 0

    for p_mask in range(1 << (2 * k)):
        family = signature_family(k, p_mask)
        s_total += len(family)

        for alpha in (0, 1):
            shadow = {signature | v_mask(k, p_mask, alpha) for signature in family}
            e_total += len(shadow - family)

        if p_mask & 1:  # 1 in P
            safe_family = union_closure(safe_generators(k, p_mask).values())
            trace_total += len(safe_family)

            if verify_trace_equivalence:
                forbidden = value_bit(k, -k)
                filtered = {signature for signature in family if not signature & forbidden}
                if filtered != safe_family:
                    raise AssertionError(
                        f"safe-generator trace mismatch for k={k}, P={p_mask}"
                    )

            fibers = restricted_witness_fibers(k, p_mask)
            witness_total += sum(fibers.values())
            collision_total += sum(value * value for value in fibers.values())
            restricted_distinct_total += len(fibers)
            max_fiber = max(max_fiber, max(fibers.values(), default=0))

    return Statistics(
        k=k,
        s=s_total,
        e=e_total,
        trace_total=trace_total,
        restricted_witnesses=witness_total,
        restricted_collision_energy=collision_total,
        restricted_distinct_outputs=restricted_distinct_total,
        restricted_max_fiber=max_fiber,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-k", type=int, default=4)
    parser.add_argument(
        "--verify-trace-equivalence",
        action="store_true",
        help="compare the safe-generator trace with direct filtering",
    )
    parser.add_argument("--json", type=Path, help="optional JSON output path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_k < 1:
        raise SystemExit("--max-k must be positive")

    rows = [
        statistics(k, verify_trace_equivalence=args.verify_trace_equivalence)
        for k in range(1, args.max_k + 1)
    ]
    payload = [row.to_json() for row in rows]

    print(
        "k S_k E_k trace T_k witness collision distinct max_fiber "
        "Q/W"
    )
    for row in rows:
        print(
            row.k,
            row.s,
            row.e,
            row.trace_total,
            f"{row.normalized_s:.9f}",
            row.restricted_witnesses,
            row.restricted_collision_energy,
            row.restricted_distinct_outputs,
            row.restricted_max_fiber,
            f"{row.size_biased_collision:.9f}",
        )

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
