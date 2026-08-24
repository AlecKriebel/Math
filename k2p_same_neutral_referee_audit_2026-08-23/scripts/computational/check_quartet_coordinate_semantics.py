#!/usr/bin/env python3
"""Independent exact check of the submission's printed quartet separators.

This script owns the Klein-four tree Fourier formula.  It does not call the
submission's graph classifier.  As a separate consistency check, it imports
only the low-level ``sector_for_mask`` routine from the submitted atlas and
confirms that routine implements the declared (0,C,G,T) / (1,s,g,s) order.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


ZERO, C, G, T = 0, 1, 2, 3
CHARACTER_NAMES = {ZERO: "0", C: "C", G: "G", T: "T"}
SPLITS = {
    "12|34": (0, 1),
    "13|24": (0, 2),
    "14|23": (0, 3),
}


def xor_all(values: tuple[int, ...]) -> int:
    total = 0
    for value in values:
        total ^= value
    return total


def edge_value(character: int, s_value: Any, g_value: Any) -> Any:
    if character == ZERO:
        return 1
    if character in (C, T):
        return s_value
    if character == G:
        return g_value
    raise ValueError(character)


def tree_coordinate(
    characters: tuple[int, int, int, int],
    topology: str,
    leaf_s: tuple[Any, Any, Any, Any],
    leaf_g: tuple[Any, Any, Any, Any],
    internal_s: Any,
    internal_g: Any,
) -> Any:
    """Fourier coordinate of an unrooted quartet tree with five edges."""
    if xor_all(characters) != ZERO:
        return 0
    value = 1
    for index, character in enumerate(characters):
        value *= edge_value(character, leaf_s[index], leaf_g[index])
    left = SPLITS[topology]
    internal_character = characters[left[0]] ^ characters[left[1]]
    value *= edge_value(internal_character, internal_s, internal_g)
    return sp.expand(value) if isinstance(value, sp.Basic) else value


def polynomial_values(
    topology: str,
    leaf_s: tuple[Any, Any, Any, Any],
    leaf_g: tuple[Any, Any, Any, Any],
    internal_s: Any,
    internal_g: Any,
) -> dict[str, Any]:
    q = lambda word: tree_coordinate(
        tuple({"0": ZERO, "C": C, "G": G, "T": T}[letter] for letter in word),
        topology,
        leaf_s,
        leaf_g,
        internal_s,
        internal_g,
    )
    return {
        "q_GGGG": q("GGGG"),
        "q_GGTT": q("GGTT"),
        "q_GTTG": q("GTTG"),
        "q_GTGT": q("GTGT"),
        "printed_F": sp.expand(q("GGGG") - q("GGTT")),
        "printed_G": sp.expand(q("GGGG") - q("GGTT") - q("GTTG") + q("GTGT")),
        "q_CCCC": q("CCCC"),
        "q_CCTT": q("CCTT"),
        "q_CTTC": q("CTTC"),
        "q_CTCT": q("CTCT"),
        "corrected_F": sp.expand(q("CCCC") - q("CCTT")),
        "corrected_G": sp.expand(q("CCCC") - q("CCTT") - q("CTTC") + q("CTCT")),
    }


def fraction_string(value: Any) -> str:
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)
    return str(value)


def import_atlas(project: Path):
    atlas_path = project / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
    spec = importlib.util.spec_from_file_location("audit_coordinate_semantics_atlas", atlas_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {atlas_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module, atlas_path


def atlas_tree_coordinate(
    atlas,
    characters: tuple[int, int, int, int],
    topology: str,
    leaf_s: tuple[Fraction, Fraction, Fraction, Fraction],
    leaf_g: tuple[Fraction, Fraction, Fraction, Fraction],
    internal_s: Fraction,
    internal_g: Fraction,
) -> Fraction:
    """Use only submitted low-level sector dispatch, not its classifier."""
    masks = tuple(1 << index for index in range(4)) + (
        sum(1 << index for index in SPLITS[topology]),
    )
    spectra = tuple(zip(leaf_s, leaf_g)) + ((internal_s, internal_g),)
    value = Fraction(1)
    for mask, (s_value, g_value) in zip(masks, spectra):
        sector = atlas.sector_for_mask(mask, characters)
        value *= (Fraction(1), s_value, g_value)[sector]
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    s_symbols = sp.symbols("s1:5")
    g_symbols = sp.symbols("g1:5")
    s_internal, g_internal = sp.symbols("sI gI")
    symbolic = {
        topology: {name: str(value) for name, value in polynomial_values(
            topology, s_symbols, g_symbols, s_internal, g_internal
        ).items()}
        for topology in SPLITS
    }

    # Every edge uses the same exact point.  It lies strictly in both D_plus
    # and the continuous-time cone: s^2=9/16 < g=3/5.
    s_value, g_value = Fraction(3, 4), Fraction(3, 5)
    leaf_s = (s_value,) * 4
    leaf_g = (g_value,) * 4
    numeric_raw = {
        topology: polynomial_values(topology, leaf_s, leaf_g, s_value, g_value)
        for topology in SPLITS
    }
    numeric = {
        topology: {name: fraction_string(value) for name, value in values.items()}
        for topology, values in numeric_raw.items()
    }

    transition_entries = {
        "f(0)": (1 + 2 * s_value + g_value) / 4,
        "f(C)=f(T)": (1 - g_value) / 4,
        "f(G)": (1 - 2 * s_value + g_value) / 4,
    }
    domain = {
        "0<s<1": 0 < s_value < 1,
        "0<g<1": 0 < g_value < 1,
        "g>2s-1": g_value > 2 * s_value - 1,
        "g>s^2": g_value > s_value * s_value,
        "all_transition_entries_positive": all(value > 0 for value in transition_entries.values()),
        "transition_entries": {name: fraction_string(value) for name, value in transition_entries.items()},
    }

    atlas, atlas_path = import_atlas(args.project)
    sector_dispatch = {
        CHARACTER_NAMES[character]: atlas.sector_for_mask(1, (character, ZERO, ZERO, character))
        for character in (ZERO, C, G, T)
    }
    expected_dispatch = {"0": 0, "C": 1, "G": 2, "T": 1}
    if sector_dispatch != expected_dispatch:
        raise RuntimeError((sector_dispatch, expected_dispatch))

    atlas_agreement: dict[str, dict[str, str]] = {}
    words = ("GGGG", "GGTT", "GTTG", "GTGT", "CCCC", "CCTT", "CTTC", "CTCT")
    lookup = {"0": ZERO, "C": C, "G": G, "T": T}
    for topology in SPLITS:
        atlas_agreement[topology] = {}
        for word in words:
            chars = tuple(lookup[letter] for letter in word)
            independent = tree_coordinate(chars, topology, leaf_s, leaf_g, s_value, g_value)
            submitted_low_level = atlas_tree_coordinate(
                atlas, chars, topology, leaf_s, leaf_g, s_value, g_value
            )
            if independent != submitted_low_level:
                raise RuntimeError((topology, word, independent, submitted_low_level))
            atlas_agreement[topology][word] = fraction_string(independent)

    failures = {
        "printed_F_zero_on_12|34": bool(numeric_raw["12|34"]["printed_F"] == 0),
        "printed_G_zero_on_12|34": bool(numeric_raw["12|34"]["printed_G"] == 0),
        "printed_F_positive_on_13|24": bool(numeric_raw["13|24"]["printed_F"] > 0),
        "printed_G_positive_on_13|24": bool(numeric_raw["13|24"]["printed_G"] > 0),
    }
    corrected_checks = {
        "corrected_F_zero_on_12|34": bool(numeric_raw["12|34"]["corrected_F"] == 0),
        "corrected_F_positive_on_13|24": bool(numeric_raw["13|24"]["corrected_F"] > 0),
        "corrected_F_positive_on_14|23": bool(numeric_raw["14|23"]["corrected_F"] > 0),
        "corrected_G_zero_on_12|34": bool(numeric_raw["12|34"]["corrected_G"] == 0),
        "corrected_G_positive_on_13|24": bool(numeric_raw["13|24"]["corrected_G"] > 0),
        "corrected_G_zero_on_14|23": bool(numeric_raw["14|23"]["corrected_G"] == 0),
    }
    if all(failures.values()):
        raise RuntimeError("printed identities unexpectedly passed")
    if not all(corrected_checks.values()):
        raise RuntimeError(corrected_checks)

    result = {
        "schema": "independent-k2p-quartet-coordinate-audit-v1",
        "declared_order": ["0", "C", "G", "T"],
        "declared_spectrum": ["1", "s", "g", "s"],
        "submitted_atlas_path": str(atlas_path),
        "submitted_sector_dispatch": sector_dispatch,
        "symbolic_tree_pullbacks": symbolic,
        "exact_test_point": {"s": "3/4", "g": "3/5", "all_five_edges_equal": True},
        "domain_checks": domain,
        "numeric_tree_pullbacks": numeric,
        "submitted_low_level_map_agreement": atlas_agreement,
        "printed_claim_checks": failures,
        "corrected_coordinate_checks": corrected_checks,
        "conclusion": (
            "FAIL: the printed G/T quartet polynomials do not have their claimed zero/sign "
            "sets under the declared and implemented (1,s,g,s) convention; replacing the "
            "leading G symbols by C gives the expected C/T-sector separators."
        ),
    }
    encoded_without_hash = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(encoded_without_hash).hexdigest()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
