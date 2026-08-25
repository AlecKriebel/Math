#!/usr/bin/env python3
"""Exact convention-aware K2P displayed-quartet replay.

This verifier derives the literal Fourier pullbacks from the Klein-four
group law and the declared ``(0,C,G,T)`` / ``(1,s,g,s)`` convention. It then
checks all six separator bodies, every leaf permutation, both licensed
character transports, and every unequal pair of nonempty displayed sets.
It also binds the formulas printed in the theorem sources.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

import sympy as sp


HERE = Path(__file__).resolve().parent
DEFAULT_PROJECT = HERE.parents[1]
DEFAULT_SPEC = HERE / "QUARTET_SEMANTICS_SPEC.json"
TOPOLOGIES = ("12|34", "13|24", "14|23")
SPLIT_PARTS = {
    "12|34": ((0, 1), (2, 3)),
    "13|24": ((0, 2), (1, 3)),
    "14|23": ((0, 3), (1, 2)),
}
SPLIT_LETTERS = {"12|34": "A", "13|24": "B", "14|23": "C"}
LETTER_SPLITS = {value: key for key, value in SPLIT_LETTERS.items()}
CHARACTER_TRANSPORTS = {
    "identity": {"0": "0", "C": "C", "G": "G", "T": "T"},
    "C_T_swap": {"0": "0", "C": "T", "G": "G", "T": "C"},
}


class QuartetFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: Any = None) -> None:
    if not condition:
        suffix = "" if detail is None else f":{detail}"
        raise QuartetFailure(f"{code}{suffix}")


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_object(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_spec(path: Path) -> dict[str, Any]:
    require(path.is_file(), "QUARTET_SPEC_MISSING", path)
    spec = json.loads(path.read_text(encoding="utf-8"))
    require(spec.get("schema") == "k2p-quartet-semantics-spec-v2", "QUARTET_SPEC_SCHEMA")
    require(spec.get("character_order") == ["0", "C", "G", "T"], "CHARACTER_ORDER_CONTRACT_FAIL")
    require(spec.get("group_codes") == {"0": 0, "C": 1, "G": 2, "T": 3}, "KLEIN_CODE_CONTRACT_FAIL")
    require(spec.get("equal_nonzero_sector") == ["C", "T"], "EQUAL_SECTOR_CONTRACT_FAIL")
    require(spec.get("singleton_nonzero_sector") == ["G"], "SINGLETON_SECTOR_CONTRACT_FAIL")
    spectrum = spec.get("edge_spectrum")
    require(
        isinstance(spectrum, dict)
        and set(spectrum) == {"0", "C", "G", "T"}
        and set(spectrum.values()) <= {"1", "s", "g"}
        and spectrum["0"] == "1",
        "EDGE_SPECTRUM_SCHEMA_FAIL",
    )
    require(
        spectrum["C"] == spectrum["T"],
        "EQUAL_SECTOR_SPECTRUM_FAIL",
        spectrum,
    )
    require(
        spectrum["G"] != spectrum["C"],
        "TWO_NONZERO_SECTOR_SPECTRUM_FAIL",
        spectrum,
    )
    require(
        spec.get("canonical_coordinates")
        == {"Q0": "CCCC", "QA": "CCTT", "QB": "CTCT", "QC": "CTTC"},
        "CANONICAL_COORDINATE_CONTRACT_FAIL",
    )
    require(
        set(spec.get("canonical_formulas", {}))
        == {"F_A", "F_B", "F_C", "J_A", "J_B", "J_C"},
        "CANONICAL_FORMULA_CENSUS_FAIL",
    )
    require(
        spec.get("domain")
        == {
            "principal": "0<s<1, 0<g<1, g>2s-1",
            "strict_continuous_time": "0<s<1, s^2<g<1",
        },
        "DOMAIN_DECLARATION_CONTRACT_FAIL",
    )
    return spec


def validate_documents(project: Path, spec: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    contracts = spec.get("document_contracts")
    require(isinstance(contracts, list) and len(contracts) == 5, "DOCUMENT_CONTRACT_CENSUS_FAIL")
    for contract in contracts:
        relative = contract.get("path")
        require(isinstance(relative, str), "DOCUMENT_CONTRACT_PATH_FAIL", contract)
        path = project / relative
        require(path.is_file(), "DOCUMENT_CONTRACT_FILE_MISSING", relative)
        text = path.read_text(encoding="utf-8")
        literals = contract.get("required_unique_literals")
        require(isinstance(literals, list) and literals, "DOCUMENT_LITERAL_CENSUS_FAIL", relative)
        for literal in literals:
            require(type(literal) is str, "DOCUMENT_LITERAL_TYPE_FAIL", relative)
            count = text.count(literal)
            require(
                count == 1,
                "DOCUMENT_LITERAL_BINDING_FAIL",
                {"path": relative, "literal": literal, "count": count},
            )
        result[relative] = sha_file(path)
    return result


def xor_word(word: str, codes: dict[str, int]) -> int:
    total = 0
    for character in word:
        total ^= codes[character]
    return total


def edge_value(
    character: str,
    s_value: sp.Expr,
    g_value: sp.Expr,
    spectrum: dict[str, str],
) -> sp.Expr:
    token = spectrum[character]
    if token == "1":
        return sp.Integer(1)
    if token == "s":
        return s_value
    if token == "g":
        return g_value
    raise QuartetFailure(f"EDGE_SPECTRUM_TOKEN_FAIL:{character}:{token}")


def tree_coordinate(
    word: str,
    topology: str,
    pendant_s: tuple[sp.Expr, ...],
    pendant_g: tuple[sp.Expr, ...],
    internal_s: sp.Expr,
    internal_g: sp.Expr,
    spec: dict[str, Any],
) -> sp.Expr:
    codes = spec["group_codes"]
    require(len(word) == 4 and set(word) <= set(codes), "FOURIER_WORD_FAIL", word)
    if xor_word(word, codes) != 0:
        return sp.Integer(0)
    value = sp.Integer(1)
    for index, character in enumerate(word):
        value *= edge_value(
            character,
            pendant_s[index],
            pendant_g[index],
            spec["edge_spectrum"],
        )
    internal_code = 0
    for index in SPLIT_PARTS[topology][0]:
        internal_code ^= codes[word[index]]
    inverse_codes = {code: character for character, code in codes.items()}
    internal_character = inverse_codes[internal_code]
    value *= edge_value(
        internal_character,
        internal_s,
        internal_g,
        spec["edge_spectrum"],
    )
    return sp.factor(value)


def formula_expression(
    terms: list[list[Any]],
    topology: str,
    pendant_s: tuple[sp.Expr, ...],
    pendant_g: tuple[sp.Expr, ...],
    internal_s: sp.Expr,
    internal_g: sp.Expr,
    spec: dict[str, Any],
) -> sp.Expr:
    expression = sp.Integer(0)
    for term in terms:
        require(
            isinstance(term, list)
            and len(term) == 2
            and type(term[0]) is int
            and type(term[1]) is str,
            "FORMULA_TERM_SCHEMA_FAIL",
            term,
        )
        coefficient, word = term
        require(
            coefficient != 0 and xor_word(word, spec["group_codes"]) == 0,
            "FORMULA_TERM_CONSERVATION_FAIL",
            term,
        )
        expression += coefficient * tree_coordinate(
            word,
            topology,
            pendant_s,
            pendant_g,
            internal_s,
            internal_g,
            spec,
        )
    return sp.factor(expression)


def expected_pullback(
    formula_id: str,
    topology: str,
    pendant_product: sp.Expr,
    internal_g: sp.Expr,
) -> sp.Expr:
    family, letter = formula_id.split("_", 1)
    distinguished = LETTER_SPLITS[letter]
    if family == "F":
        return (
            sp.Integer(0)
            if topology == distinguished
            else pendant_product * (1 - internal_g)
        )
    require(family == "J", "FORMULA_FAMILY_FAIL", formula_id)
    return (
        2 * pendant_product * (1 - internal_g)
        if topology == distinguished
        else sp.Integer(0)
    )


def transported_word(
    word: str,
    permutation: tuple[int, ...],
    character_map: dict[str, str],
) -> str:
    result = [""] * 4
    for old_index, character in enumerate(word):
        result[permutation[old_index]] = character_map[character]
    require(all(result), "WORD_TRANSPORT_FAIL", {"word": word, "permutation": permutation})
    return "".join(result)


def transported_split(topology: str, permutation: tuple[int, ...]) -> str:
    mapped = {
        frozenset(permutation[index] for index in part)
        for part in SPLIT_PARTS[topology]
    }
    for candidate, parts in SPLIT_PARTS.items():
        if mapped == {frozenset(part) for part in parts}:
            return candidate
    raise QuartetFailure(f"SPLIT_TRANSPORT_FAIL:{topology}:{permutation}")


def derive_formula_layer(
    spec: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, str]]:
    pendant_s = sp.symbols("s1:5", positive=True)
    pendant_g = sp.symbols("g1:5", positive=True)
    internal_s, internal_g = sp.symbols("sI gI", positive=True)
    pendant_product = sp.prod(pendant_s)
    formulas = spec["canonical_formulas"]

    canonical_rows: dict[str, Any] = {}
    formula_digests: dict[str, str] = {}
    for formula_id in sorted(formulas):
        terms = formulas[formula_id]
        pullbacks: dict[str, str] = {}
        for topology in TOPOLOGIES:
            observed = formula_expression(
                terms,
                topology,
                pendant_s,
                pendant_g,
                internal_s,
                internal_g,
                spec,
            )
            expected = sp.factor(
                expected_pullback(formula_id, topology, pendant_product, internal_g)
            )
            require(
                sp.simplify(observed - expected) == 0,
                "CANONICAL_PULLBACK_FAIL",
                {
                    "formula": formula_id,
                    "topology": topology,
                    "observed": str(observed),
                    "expected": str(expected),
                },
            )
            pullbacks[topology] = str(observed)
        formula_payload = {
            "formula_id": formula_id,
            "terms": terms,
            "pullbacks": pullbacks,
        }
        formula_digests[formula_id] = sha_object(formula_payload)
        canonical_rows[formula_id] = {
            **formula_payload,
            "formula_sha256": formula_digests[formula_id],
        }

    transport_rows: list[dict[str, Any]] = []
    for permutation in itertools.permutations(range(4)):
        for character_transport, character_map in CHARACTER_TRANSPORTS.items():
            for formula_id in sorted(formulas):
                family, letter = formula_id.split("_", 1)
                source_split = LETTER_SPLITS[letter]
                target_split = transported_split(source_split, permutation)
                target_id = f"{family}_{SPLIT_LETTERS[target_split]}"
                terms = [
                    [coefficient, transported_word(word, permutation, character_map)]
                    for coefficient, word in formulas[formula_id]
                ]
                pullbacks: dict[str, str] = {}
                for topology in TOPOLOGIES:
                    observed = formula_expression(
                        terms,
                        topology,
                        pendant_s,
                        pendant_g,
                        internal_s,
                        internal_g,
                        spec,
                    )
                    expected = sp.factor(
                        expected_pullback(target_id, topology, pendant_product, internal_g)
                    )
                    require(
                        sp.simplify(observed - expected) == 0,
                        "TRANSPORTED_PULLBACK_FAIL",
                        {
                            "source_formula": formula_id,
                            "target_formula": target_id,
                            "permutation": permutation,
                            "character_transport": character_transport,
                            "topology": topology,
                        },
                    )
                    pullbacks[topology] = str(observed)
                row = {
                    "source_formula": formula_id,
                    "target_formula": target_id,
                    "leaf_permutation_old_to_new": list(permutation),
                    "character_transport": character_transport,
                    "terms": terms,
                    "pullbacks": pullbacks,
                }
                row["transport_sha256"] = sha_object(row)
                transport_rows.append(row)
    require(
        len(transport_rows) == 288,
        "FORMULA_TRANSPORT_CENSUS_FAIL",
        len(transport_rows),
    )
    return canonical_rows, transport_rows, formula_digests


def separating_witness(
    left: frozenset[str], right: frozenset[str]
) -> dict[str, Any]:
    require(left and right and left != right, "DISPLAYED_SET_PAIR_FAIL")
    if len(left) == 1 and bool(right - left):
        split = next(iter(left))
        return {
            "orientation": "left_zero_right_positive",
            "formula_id": f"F_{SPLIT_LETTERS[split]}",
        }
    if len(right) == 1 and bool(left - right):
        split = next(iter(right))
        return {
            "orientation": "right_zero_left_positive",
            "formula_id": f"F_{SPLIT_LETTERS[split]}",
        }
    only_right = sorted(right - left)
    if only_right:
        split = only_right[0]
        return {
            "orientation": "left_zero_right_positive",
            "formula_id": f"J_{SPLIT_LETTERS[split]}",
        }
    split = sorted(left - right)[0]
    return {
        "orientation": "right_zero_left_positive",
        "formula_id": f"J_{SPLIT_LETTERS[split]}",
    }


def derive_displayed_set_layer(
    formula_rows: dict[str, Any], formula_digests: dict[str, str]
) -> list[dict[str, Any]]:
    displayed_sets = [
        frozenset(
            TOPOLOGIES[index] for index in range(3) if mask >> index & 1
        )
        for mask in range(1, 8)
    ]
    rows: list[dict[str, Any]] = []
    for left, right in itertools.combinations(displayed_sets, 2):
        witness = separating_witness(left, right)
        formula_id = witness["formula_id"]
        family, letter = formula_id.split("_", 1)
        split = LETTER_SPLITS[letter]
        zero_topologies = (
            {split} if family == "F" else set(TOPOLOGIES) - {split}
        )
        if witness["orientation"] == "left_zero_right_positive":
            valid = left <= zero_topologies and bool(right - zero_topologies)
        else:
            valid = right <= zero_topologies and bool(left - zero_topologies)
        require(
            valid,
            "DISPLAYED_WITNESS_SEMANTICS_FAIL",
            {"left": sorted(left), "right": sorted(right), **witness},
        )
        rows.append(
            {
                "left": sorted(left),
                "right": sorted(right),
                **witness,
                "literal_terms": formula_rows[formula_id]["terms"],
                "formula_sha256": formula_digests[formula_id],
            }
        )
    require(len(rows) == 21, "DISPLAYED_PAIR_CENSUS_FAIL", len(rows))
    return rows


def main() -> None:
    if not __debug__:
        raise SystemExit("QUARTET_LOGIC_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--skip-document-binding", action="store_true")
    args = parser.parse_args()

    project = args.project.resolve()
    spec_path = args.spec.resolve()
    output = (
        args.output.resolve()
        if args.output
        else HERE / "quartet_logic_certificate.json"
    )
    spec = load_spec(spec_path)
    documents = (
        {} if args.skip_document_binding else validate_documents(project, spec)
    )
    canonical_rows, transport_rows, formula_digests = derive_formula_layer(spec)
    displayed_rows = derive_displayed_set_layer(canonical_rows, formula_digests)

    payload = {
        "schema": "k2p-displayed-quartet-semantics-v2",
        "status": "PASS",
        "character_order": spec["character_order"],
        "edge_spectrum": [
            spec["edge_spectrum"][character]
            for character in spec["character_order"]
        ],
        "equal_nonzero_sector": spec["equal_nonzero_sector"],
        "singleton_nonzero_sector": spec["singleton_nonzero_sector"],
        "domain": spec["domain"],
        "spec_path": (
            str(spec_path.relative_to(project))
            if spec_path.is_relative_to(project)
            else str(spec_path)
        ),
        "spec_sha256": sha_file(spec_path),
        "document_sha256": documents,
        "canonical_formula_count": len(canonical_rows),
        "formula_transport_count": len(transport_rows),
        "displayed_set_count": 7,
        "unequal_pair_count": len(displayed_rows),
        "strict_sign_reason": (
            "every nonzero pullback is a positive integer times "
            "prod_i(s_i)*(1-g_I), with s_i>0 and 0<g_I<1; serial "
            "internal paths replace g_I by a nonempty product in (0,1)"
        ),
        "canonical_formulas": canonical_rows,
        "formula_transports": transport_rows,
        "displayed_set_witnesses": displayed_rows,
    }
    certificate = dict(payload)
    certificate["payload_sha256"] = sha_object(payload)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("K2P_QUARTET_SIGN_LOGIC_PASS")
    print(
        json.dumps(
            {
                "payload_sha256": certificate["payload_sha256"],
                "canonical_formulas": len(canonical_rows),
                "formula_transports": len(transport_rows),
                "displayed_pairs": len(displayed_rows),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
