#!/usr/bin/env python3
"""Apply the norm-preserving BS-quad switch to a variable-q checkpoint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from alternate_variable_q_candidate import load_sequences, rewrite_payload
from variable_q_base import canonical_margin_transform, switch_short_quads


def switch_payload(payload: object, source: str) -> dict[str, object]:
    a, b, c, d = load_sequences(payload)
    switched_c, switched_d = switch_short_quads(c, d)
    sequences = canonical_margin_transform(a, b, switched_c, switched_d)
    result = rewrite_payload(payload, sequences, "quad_switch_source", source)
    search = result.get("search")
    if isinstance(search, dict):
        result["search"] = {**search, "short_quad_switched": True}
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    transformed = switch_payload(payload, str(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(transformed, indent=2) + "\n", encoding="utf-8")
    print(f"source_shard={payload.get('shard') if isinstance(payload, dict) else 'unknown'}")
    print(f"target_shard={transformed['shard']}")
    print(f"energy_half={transformed['energy_half_base']}")
    print(f"wrote={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
