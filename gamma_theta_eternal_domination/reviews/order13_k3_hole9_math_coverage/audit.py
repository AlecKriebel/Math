#!/usr/bin/env python3
"""Read-only clean-room audit of the hole9 UNSAT-to-graph implication.

This audit deliberately imports no campaign Python module and launches no
solver or proof checker.  It independently reconstructs the exact hole9 CNF,
checks the full coloring bank by enumerating all named colorings, binds the
accepted mathematical and certificate-verifier artifacts, and records the
precise graph-theoretic conclusion supported by their composition.
"""

from __future__ import annotations

from collections import Counter, OrderedDict
import hashlib
from itertools import combinations, product
import json
import math
import os
from pathlib import Path, PurePosixPath
import stat
from typing import Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
N = 13
HOLE = 9
EXPECTED_VARIABLES = 9_802
EXPECTED_CLAUSES = 32_108
EXPECTED_LITERALS = 281_028
EXPECTED_FORMULA_SHA256 = (
    "3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea"
)


class AuditFailure(RuntimeError):
    """A frozen binding or independent reconstruction failed closed."""


FROZEN: Mapping[str, tuple[int, str, str]] = {
    "math/lemmas/order13_k3_hole9_certificate_exclusion.md": (
        7_351,
        "372f1595dc224232095eb9cf9523eb1d1d992502391d6fc58f3e818d41769937",
        "integration theorem under review",
    ),
    "math/lemmas/order13_k3_synthesis_target.md": (
        26_303,
        "7bec13620961adeaf61c60e88c8bc9366beecab7387e40c80083fe702484ab39",
        "C-055 graph-to-CNF equivalence and template coverage",
    ),
    "math/lemmas/order13_k3_hole11_exclusion.md": (
        16_330,
        "511432d00f43f602fd906b3b5e37ae0e5c85cbc1523bcd63c5b668a00f0d53f8",
        "C-053 near-spanning-hole theorem",
    ),
    "math/lemmas/k3_structural_day1.md": (
        6_848,
        "00d6fb851a3cb50ed907a593b0379376571251f8604974b5b67e05e2b0705d6e",
        "C-014 odd-wheel obstruction",
    ),
    "reviews/k3_structural_hostile_review.md": (
        9_565,
        "f2b0ce3d551576d5050bb03c7e8699bdffdb3ae35fbf5d3cf4b28c4e4ab270bc",
        "hostile acceptance of C-014",
    ),
    "math/lemmas/k3_antihole_elimination.md": (
        3_686,
        "9e572203c09e082c3cbdfc0cdae8e4166007af3f909b73f7d8d2e196f04ddc4f",
        "C-017 odd-antihole elimination",
    ),
    "reviews/k3_antihole_hostile_review.md": (
        5_964,
        "7837fb360328533ea58a31d1a0eb60ef279a67d1e610144eb5206661ef38f5e3",
        "hostile acceptance of C-017",
    ),
    "math/lemmas/maximum_independent_states.md": (
        4_211,
        "08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e",
        "maximum-independent-state lemma",
    ),
    "math/reductions.md": (
        16_385,
        "d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13",
        "parameter chain and component additivity",
    ),
    "math/lemmas/order12_frontier.md": (
        8_120,
        "adb27204d33feb47933f2a4b1e381485b2e1b80c22b56a67b18586c4933c2b75",
        "C-050 lower-order frontier theorem",
    ),
    "results/order12_frontier_acceptance.json": (
        7_726,
        "e3b093085bafd124c228a29ef98c86341a45316dc02e11b565a138afe983d57a",
        "C-050 acceptance with published through-order-11 premise",
    ),
    "reviews/c050_acceptance_wrapper_hostile/REVIEW.md": (
        8_326,
        "b7a0bba8fd82fd0716e7f38dbb2e14c5a2e9d34046a6ee1684d066f818af2b5c",
        "hostile acceptance of the frozen C-050 wrapper",
    ),
    "reviews/order13_k3_math_hostile/REVIEW.md": (
        15_021,
        "284ec751a215e499de2adfa2f2b377d1a700a27a8b3e96964067c53f652698d8",
        "hostile audit of C-053 and C-055 mathematics",
    ),
    "reviews/order13_k3_math_hostile/ADDENDUM.md": (
        2_415,
        "42fbc74ad916757a35df8bf5cbc6c4ab5205ae5f5d34abf915cff6bbb2203bd7",
        "revised-byte mathematical acceptance",
    ),
    "reviews/order13_k3_math_hostile/evidence.json": (
        20_660,
        "8c1f5b3fe4511a4d19efdc224a7ea6b10b38eac06275ddce615bd73949d22af1",
        "clean-room mathematical audit evidence",
    ),
    "reviews/order13_k3_math_hostile/addendum_evidence.json": (
        3_456,
        "e45d99d880af6350034d7ee9a4b83acb30cc4706c9aa4445d97a07a272d3dc14",
        "revised-byte mathematical evidence",
    ),
    "reviews/order13_k3_constructor_independent/REVIEW.md": (
        6_803,
        "df128b29dd5464ec55465333d4672bc7dfbbe76538024325ab880a2a60d5bda4",
        "independent constructor review",
    ),
    "reviews/order13_k3_constructor_independent/evidence.json": (
        5_559,
        "784839ee925675b49a3636ab1625ef35389da2a6d418e629164c2ca5bb053e09",
        "independent constructor evidence",
    ),
    "reviews/order13_k3_constructor_acceptance/REVIEW.md": (
        6_905,
        "7d05355fdc92db4ccbb4a6254934015ddc89f216392fad341cff0bdb82f5e428",
        "constructor integration acceptance",
    ),
    "reviews/order13_k3_constructor_acceptance/evidence.json": (
        7_248,
        "8318d036867da89c2b2b7b9599bde17f50e160731d21243584609d34a515ec74",
        "constructor integration evidence",
    ),
    "reviews/order13_k3_hole9_preflight_constructor/REVIEW.md": (
        4_352,
        "70e870564eca1c2ccb53f4db8607c52218e237637ec54ad183f442f5fc8e2548",
        "live-package preflight review",
    ),
    "reviews/order13_k3_hole9_preflight_constructor/evidence.json": (
        2_183,
        "2687e1f893f85b64c83fdfe86cfcbd2eb7670a3307cc23f0cc999c999a422de9",
        "live-package preflight evidence",
    ),
    "instances/order13_k3_hole9/instance.cnf": (
        1_168_197,
        EXPECTED_FORMULA_SHA256,
        "accepted live hole9 DIMACS",
    ),
    "instances/order13_k3_hole9/coloring-bank.json": (
        227_208,
        "a0f47a0aaa3be4659ce483f27a963d351f3a13424cac6a6a99ef6ac9e0c872f1",
        "accepted complete coloring bank",
    ),
    "instances/order13_k3_hole9/constructor-manifest.json": (
        5_408,
        "8f55019121df7280368528c1b7c0808d3cc06e7bd0f871be516057763c87ad5b",
        "accepted constructor manifest",
    ),
    "certificates/order13_k3_hole9_attempt000001_lrat/instance.cnf": (
        1_168_197,
        EXPECTED_FORMULA_SHA256,
        "certificate copy of exact DIMACS",
    ),
    "certificates/order13_k3_hole9_attempt000001_lrat/proof.normalized.bdrat": (
        742_337,
        "af216ef2d7698db2b1d1c55411bc05025bfe25f10c16f2e85c5301f7a88bdd5f",
        "addition-only binary RUP proof",
    ),
    "certificates/order13_k3_hole9_attempt000001_lrat/proof.lrat": (
        8_546_664,
        "f6ef614f2acee4cf43aa3b75372b354912c50248a13c3f863479cdc49b061805",
        "LRAT proof",
    ),
    "certificates/order13_k3_hole9_attempt000001_lrat/candidate-manifest.json": (
        6_953,
        "2c27a98e6a3a4ca66fdfedac4c3ae6839b11d0008ed63a1d8999b24c3f917fa1",
        "candidate provenance; no claims imported",
    ),
    "src/verifier_b/order13_k3_hole9_certificate.py": (
        39_193,
        "4adf3691f438c03b230ff323ea5f7c180db9b5c8cd895b6f31327f5e154a97ee",
        "independent proof verifier B",
    ),
    "tests/test_order13_k3_hole9_certificate_verifier_b.py": (
        3_826,
        "2ca00e46efee4597fcc532ffe9e8d9fc61c73631def42011d26ab7a3cf516fc5",
        "focused verifier-B tests",
    ),
    "reviews/order13_k3_hole9_certificate_verifier_b/REVIEW.md": (
        4_848,
        "d5658d94d7826864cc001c20ebf1e725196c25902d817cdb7a96a18bc9c96dd4",
        "verifier-B review",
    ),
    "reviews/order13_k3_hole9_certificate_verifier_b/evidence.json": (
        15_105,
        "3de45d16b906e52c3960e4b2e75604908c8cacf356b84d7337db721f4fa49af8",
        "canonical fresh RUP/LRAT replay evidence",
    ),
    "reviews/order13_k3_hole9_certificate_verifier_b/tool-source-provenance.json": (
        2_518,
        "95702f678c8fbbde5f733e121105d59b2c3890821b1195300d7ec5f03cefa275",
        "corrected checker source/build provenance",
    ),
    "reviews/order13_k3_hole9_certificate_verifier_b/external_code_audit/REVIEW.md": (
        9_578,
        "aef1543f799666fd32842dd2aaa454d7ae65c9556374cbf6d5d4f5f6bbb18c4a",
        "external exact-byte verifier-code acceptance",
    ),
    "reviews/order13_k3_hole9_certificate_verifier_b/external_code_audit/evidence.json": (
        8_482,
        "97aad1ec54552aca510d511063ccca74de702dc4f9f1796dbbc2333f4c42ecd9",
        "external verifier-code audit evidence",
    ),
    "reviews/order13_k3_hole9_certificate_verifier_b/external_code_audit/replay.py": (
        21_785,
        "e7627c21fa588ec4b1efd2438d6666acf6f437bbed6dcff7ebe5b592fe38e66f",
        "read-only external verifier-code replay",
    ),
}


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _relative_path(relative: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or not pure.parts or any(
        part in ("", ".", "..") for part in pure.parts
    ):
        raise AuditFailure(f"unsafe relative path: {relative!r}")
    current = ROOT
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise AuditFailure(f"symlink component rejected: {relative}")
    return current


def read_regular(relative: str) -> bytes:
    path = _relative_path(relative)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise AuditFailure(f"cannot open {relative}: {exc}") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise AuditFailure(f"not a regular file: {relative}")
        chunks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity_before = (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    )
    identity_after = (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    )
    if identity_before != identity_after:
        raise AuditFailure(f"file changed during read: {relative}")
    return b"".join(chunks)


def bind_frozen() -> tuple[dict[str, bytes], list[dict[str, object]]]:
    payloads: dict[str, bytes] = {}
    records: list[dict[str, object]] = []
    for relative in sorted(FROZEN):
        expected_size, expected_sha, role = FROZEN[relative]
        payload = read_regular(relative)
        if len(payload) != expected_size:
            raise AuditFailure(
                f"size mismatch for {relative}: {len(payload)} != {expected_size}"
            )
        actual_sha = sha256(payload)
        if actual_sha != expected_sha:
            raise AuditFailure(
                f"SHA-256 mismatch for {relative}: {actual_sha} != {expected_sha}"
            )
        payloads[relative] = payload
        records.append(
            {
                "path": relative,
                "role": role,
                "sha256": actual_sha,
                "size_bytes": len(payload),
            }
        )
    return payloads, records


def strict_json(payload: bytes, label: str) -> object:
    def object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise AuditFailure(f"duplicate JSON key {key!r} in {label}")
            result[key] = value
        return result

    def reject_constant(token: str) -> object:
        raise AuditFailure(f"nonfinite JSON token {token!r} in {label}")

    try:
        return json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=object_pairs,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuditFailure(f"malformed JSON in {label}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


class Formula:
    """Independent variable allocator and tagged clause stream."""

    def __init__(self) -> None:
        self.next_variable = 1
        self.edge: dict[tuple[int, int], int] = {}
        self.witness: dict[tuple[int, int, int], int] = {}
        self.family: dict[tuple[int, int, int], int] = {}
        self.move: dict[tuple[tuple[int, int, int], int, int], int] = {}
        self.clauses: list[tuple[int, ...]] = []
        self.tags: list[str] = []

    def allocate(self) -> int:
        result = self.next_variable
        self.next_variable += 1
        return result

    @property
    def variables(self) -> int:
        return self.next_variable - 1

    def add(self, tag: str, literals: Iterable[int]) -> None:
        clause = tuple(literals)
        require(bool(clause), f"unexpected empty formula clause in {tag}")
        require(0 not in clause, f"zero literal in {tag}")
        require(
            all(abs(literal) <= self.variables for literal in clause),
            f"unallocated literal in {tag}",
        )
        require(len(set(clause)) == len(clause), f"duplicate literal in {tag}")
        require(
            not any(-literal in clause for literal in clause),
            f"tautology in {tag}",
        )
        self.tags.append(tag)
        self.clauses.append(clause)

    def h_edge(self, first: int, second: int) -> int:
        require(first != second, "loop requested")
        pair = tuple(sorted((first, second)))
        return self.edge[pair]


def canonicalize(row: Sequence[int]) -> tuple[int, ...]:
    names: dict[int, int] = {}
    answer: list[int] = []
    for color in row:
        if color not in names:
            names[color] = len(names)
        answer.append(names[color])
    return tuple(answer)


def independent_coloring_bank() -> tuple[tuple[tuple[int, ...], ...], int]:
    """Enumerate all 3^13 named rows, then quotient color names."""

    positive = {
        tuple(sorted((vertex, (vertex + 1) % HOLE)))
        for vertex in range(HOLE)
    }
    positive.update({(0, HOLE), (1, HOLE)})
    canonical_rows: set[tuple[int, ...]] = set()
    labeled_count = 0
    for row in product(range(3), repeat=N):
        if any(row[first] == row[second] for first, second in positive):
            continue
        labeled_count += 1
        canonical_rows.add(canonicalize(row))
    return tuple(sorted(canonical_rows)), labeled_count


def build_formula(
    coloring_rows: Sequence[Sequence[int]],
) -> Formula:
    formula = Formula()
    vertices = tuple(range(N))
    triples = tuple(combinations(vertices, 3))
    for pair in combinations(vertices, 2):
        formula.edge[pair] = formula.allocate()
    for first, second in combinations(vertices, 2):
        for witness in vertices:
            if witness not in (first, second):
                formula.witness[(first, second, witness)] = formula.allocate()
    for triple in triples:
        formula.family[triple] = formula.allocate()
    for triple in triples:
        for attacked in vertices:
            if attacked in triple:
                continue
            for guard in triple:
                formula.move[(triple, attacked, guard)] = formula.allocate()
    require(formula.variables == EXPECTED_VARIABLES, "variable census mismatch")

    for four_set in combinations(vertices, 4):
        formula.add(
            "no_h_k4",
            (
                -formula.h_edge(first, second)
                for first, second in combinations(four_set, 2)
            ),
        )
    for first, second in combinations(vertices, 2):
        candidates = tuple(
            witness for witness in vertices if witness not in (first, second)
        )
        formula.add(
            "pair_common_neighbor_choice",
            (
                formula.witness[(first, second, witness)]
                for witness in candidates
            ),
        )
        for witness in candidates:
            variable = formula.witness[(first, second, witness)]
            formula.add(
                "pair_common_neighbor_implication",
                (-variable, formula.h_edge(first, witness)),
            )
            formula.add(
                "pair_common_neighbor_implication",
                (-variable, formula.h_edge(second, witness)),
            )

    rim_edges = {
        tuple(sorted((vertex, (vertex + 1) % HOLE)))
        for vertex in range(HOLE)
    }
    for first, second in combinations(range(HOLE), 2):
        edge = formula.h_edge(first, second)
        formula.add(
            "induced_hole",
            (edge if (first, second) in rim_edges else -edge,),
        )
    for outside in range(HOLE, N):
        formula.add(
            "hole_hub_free",
            (-formula.h_edge(outside, rim) for rim in range(HOLE)),
        )
    formula.add("named_rim_edge_common_neighbor", (formula.h_edge(0, HOLE),))
    formula.add("named_rim_edge_common_neighbor", (formula.h_edge(1, HOLE),))

    full_mask = (1 << N) - 1
    for mask in range(1, full_mask):
        if not (mask & 1):
            continue
        formula.add(
            "g_connected_cut",
            (
                -formula.h_edge(first, second)
                for first in vertices
                if mask >> first & 1
                for second in vertices
                if not (mask >> second & 1)
            ),
        )

    for triple in triples:
        selected = formula.family[triple]
        for outside in vertices:
            if outside in triple:
                continue
            formula.add(
                "selected_state_dominates",
                (-selected, *(-formula.h_edge(outside, guard) for guard in triple)),
            )
    formula.add("eternal_family_nonempty", formula.family.values())

    for triple in triples:
        selected = formula.family[triple]
        for attacked in vertices:
            if attacked in triple:
                continue
            responses: list[int] = []
            for guard in triple:
                move = formula.move[(triple, attacked, guard)]
                successor = tuple(
                    sorted((set(triple) - {guard}) | {attacked})
                )
                responses.append(move)
                formula.add(
                    "move_guard_adjacent_in_g",
                    (-move, -formula.h_edge(guard, attacked)),
                )
                formula.add(
                    "move_successor_in_family",
                    (-move, formula.family[successor]),
                )
            formula.add(
                "selected_attack_has_response",
                (-selected, *responses),
            )

    for triple in triples:
        formula.add(
            "h_triangle_forced_into_family",
            (
                -formula.h_edge(triple[0], triple[1]),
                -formula.h_edge(triple[0], triple[2]),
                -formula.h_edge(triple[1], triple[2]),
                formula.family[triple],
            ),
        )

    for row in coloring_rows:
        require(len(row) == N, "malformed coloring row")
        formula.add(
            "complete_coloring_obstruction",
            (
                formula.h_edge(first, second)
                for first, second in combinations(vertices, 2)
                if row[first] == row[second]
            ),
        )
    return formula


def dimacs_bytes(formula: Formula) -> bytes:
    lines = [f"p cnf {formula.variables} {len(formula.clauses)}"]
    lines.extend(
        " ".join(map(str, clause)) + " 0" for clause in formula.clauses
    )
    return ("\n".join(lines) + "\n").encode("ascii")


def clause_family_evidence(formula: Formula) -> OrderedDict[str, object]:
    counts: OrderedDict[str, dict[str, object]] = OrderedDict()
    digests: dict[str, object] = {}
    for tag, clause in zip(formula.tags, formula.clauses):
        if tag not in counts:
            counts[tag] = {"clauses": 0, "literals": 0}
            digests[tag] = hashlib.sha256()
        counts[tag]["clauses"] = int(counts[tag]["clauses"]) + 1
        counts[tag]["literals"] = int(counts[tag]["literals"]) + len(clause)
        digests[tag].update(
            (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        )
    for tag in counts:
        counts[tag]["clause_stream_sha256"] = digests[tag].hexdigest()
    return counts


def parse_binary_proof(payload: bytes) -> dict[str, int]:
    offset = 0
    additions = 0
    literals = 0
    maximum_variable = 0
    maximum_clause = 0
    empty_records: list[int] = []
    while offset < len(payload):
        prefix = payload[offset]
        offset += 1
        require(prefix == ord("a"), "binary proof contains a non-addition record")
        additions += 1
        clause_size = 0
        while True:
            value = 0
            shift = 0
            encoded_start = offset
            while True:
                require(offset < len(payload), "truncated binary proof varint")
                byte = payload[offset]
                offset += 1
                value |= (byte & 0x7F) << shift
                if not (byte & 0x80):
                    break
                shift += 7
                require(shift <= 63, "oversized binary proof varint")
            canonical = bytearray()
            residue = value
            while residue & ~0x7F:
                canonical.append((residue & 0x7F) | 0x80)
                residue >>= 7
            canonical.append(residue)
            require(
                payload[encoded_start:offset] == bytes(canonical),
                "noncanonical binary proof varint",
            )
            if value == 0:
                break
            variable = value >> 1
            require(1 <= variable <= EXPECTED_VARIABLES, "proof variable out of range")
            clause_size += 1
            literals += 1
            maximum_variable = max(maximum_variable, variable)
        maximum_clause = max(maximum_clause, clause_size)
        if clause_size == 0:
            empty_records.append(additions)
            require(offset == len(payload), "binary proof has post-empty data")
    require(len(empty_records) == 1, "binary proof lacks a unique empty addition")
    require(empty_records[0] == additions, "binary proof empty addition is not final")
    return {
        "addition_records": additions,
        "deletion_records": 0,
        "empty_addition_record": empty_records[0],
        "empty_additions": 1,
        "literals": literals,
        "maximum_clause_size": maximum_clause,
        "maximum_variable_observed": maximum_variable,
        "nonempty_additions": additions - 1,
        "post_empty_records": 0,
    }


def main() -> None:
    payloads, frozen_records = bind_frozen()

    package_directory = _relative_path("instances/order13_k3_hole9")
    package_entries = sorted(path.name for path in package_directory.iterdir())
    require(
        package_entries
        == ["coloring-bank.json", "constructor-manifest.json", "instance.cnf"],
        f"unexpected live package entries: {package_entries}",
    )
    require(
        all(
            path.is_file() and not path.is_symlink()
            for path in package_directory.iterdir()
        ),
        "live package contains a nonregular or symlink entry",
    )

    live_formula = payloads["instances/order13_k3_hole9/instance.cnf"]
    certificate_formula = payloads[
        "certificates/order13_k3_hole9_attempt000001_lrat/instance.cnf"
    ]
    require(live_formula == certificate_formula, "formula copies are not identical")

    bank_value = strict_json(
        payloads["instances/order13_k3_hole9/coloring-bank.json"],
        "live coloring bank",
    )
    require(isinstance(bank_value, list), "coloring bank is not a list")
    retained_bank = tuple(tuple(row) for row in bank_value)
    require(
        all(
            len(row) == N
            and all(type(color) is int and color in (0, 1, 2) for color in row)
            for row in retained_bank
        ),
        "malformed coloring-bank row",
    )
    reconstructed_bank, labeled_colorings = independent_coloring_bank()
    require(
        retained_bank == reconstructed_bank,
        "retained coloring bank differs from exhaustive named-coloring quotient",
    )
    require(len(retained_bank) == 2_295, "coloring bank row count mismatch")
    require(labeled_colorings == 13_770, "labeled coloring count mismatch")
    require(
        labeled_colorings == 6 * len(retained_bank),
        "color-name orbit quotient is not free and complete",
    )
    theoretical_labeled = (2**HOLE - 2) * 3 ** (12 - HOLE)
    require(labeled_colorings == theoretical_labeled, "chromatic count mismatch")

    formula = build_formula(reconstructed_bank)
    reconstructed_dimacs = dimacs_bytes(formula)
    require(
        reconstructed_dimacs == live_formula,
        "clean-room semantic reconstruction differs from exact DIMACS bytes",
    )
    require(formula.variables == EXPECTED_VARIABLES, "wrong variable count")
    require(len(formula.clauses) == EXPECTED_CLAUSES, "wrong clause count")
    literal_count = sum(map(len, formula.clauses))
    require(literal_count == EXPECTED_LITERALS, "wrong literal count")
    require(sha256(reconstructed_dimacs) == EXPECTED_FORMULA_SHA256, "wrong hash")

    family_evidence = clause_family_evidence(formula)
    manifest = strict_json(
        payloads["instances/order13_k3_hole9/constructor-manifest.json"],
        "constructor manifest",
    )
    require(isinstance(manifest, dict), "constructor manifest is not an object")
    require(manifest["template"] == "hole9", "wrong manifest template")
    require(manifest["order"] == 13, "wrong manifest order")
    require(manifest["parameter"] == 3, "wrong manifest parameter")
    require(manifest["variable_count"] == EXPECTED_VARIABLES, "wrong manifest vars")
    require(manifest["clause_count"] == EXPECTED_CLAUSES, "wrong manifest clauses")
    require(manifest["literal_count"] == EXPECTED_LITERALS, "wrong manifest literals")
    require(manifest["coloring_row_count"] == 2_295, "wrong manifest bank count")
    require(
        manifest["fixed_independent_triple_in_g"] == [0, 1, 9],
        "wrong fixed independent triple",
    )
    require(manifest["heuristic_symmetry_breakers"] == [], "unsafe breaker listed")
    require(
        manifest["graph_variable_semantics"] == "edge variables encode H=complement(G)",
        "wrong graph-variable semantics",
    )
    require(
        manifest["clause_families"] == family_evidence,
        "manifest clause-family census/hash mismatch",
    )

    verifier_evidence = strict_json(
        payloads[
            "reviews/order13_k3_hole9_certificate_verifier_b/evidence.json"
        ],
        "verifier-B evidence",
    )
    require(isinstance(verifier_evidence, dict), "verifier evidence is not an object")
    require(
        verifier_evidence["verdict"]
        == "VERIFIED_EXACT_HOLE9_CNF_UNSAT_CANDIDATE_ONLY_PENDING_HOSTILE_ACCEPTANCE",
        "unexpected verifier-B verdict",
    )
    require(
        verifier_evidence["formula"]["sha256"] == EXPECTED_FORMULA_SHA256,
        "verifier evidence names a different formula",
    )
    require(
        verifier_evidence["formula"]["certificate_equals_constructor_byte_for_byte"]
        is True,
        "verifier evidence lacks formula equality",
    )
    require(
        verifier_evidence["checkers"]["drat_trim"]["marker"] == "s VERIFIED"
        and verifier_evidence["checkers"]["drat_trim"]["exit_code"] == 0
        and verifier_evidence["checkers"]["drat_trim"]["stderr_empty"] is True
        and verifier_evidence["checkers"]["drat_trim"]["rat_lemmas_in_core"] == 0,
        "RUP checker acceptance fields are incomplete",
    )
    require(
        verifier_evidence["checkers"]["lrat_check"]["marker"] == "c VERIFIED"
        and verifier_evidence["checkers"]["lrat_check"]["exit_code"] == 0
        and verifier_evidence["checkers"]["lrat_check"]["stderr_empty"] is True,
        "LRAT checker acceptance fields are incomplete",
    )
    require(
        verifier_evidence["hostile_mutations"] == {
            **verifier_evidence["hostile_mutations"],
            "all_rejected": True,
            "count": 24,
        },
        "verifier mutation verdict mismatch",
    )
    external_code_evidence = strict_json(
        payloads[
            "reviews/order13_k3_hole9_certificate_verifier_b/"
            "external_code_audit/evidence.json"
        ],
        "external verifier-code audit evidence",
    )
    require(
        isinstance(external_code_evidence, dict)
        and external_code_evidence["verdict"]
        == "ACCEPT_WITH_CAVEATS_NO_SOUNDNESS_BLOCKER"
        and external_code_evidence["no_soundness_blocker"] is True
        and external_code_evidence["retained_verifier_evidence"][
            "byte_identical_fresh_replay"
        ]
        is True
        and external_code_evidence["retained_verifier_evidence"][
            "hostile_mutations_count"
        ]
        == 24
        and external_code_evidence["provenance_repair"][
            "corrected_final_sha256"
        ]
        == "95702f678c8fbbde5f733e121105d59b2c3890821b1195300d7ec5f03cefa275"
        and all(
            caveat["blocking"] is False
            for caveat in external_code_evidence["caveats"]
        ),
        "external verifier-code acceptance fields are incomplete",
    )

    proof_stats = parse_binary_proof(
        payloads[
            "certificates/order13_k3_hole9_attempt000001_lrat/"
            "proof.normalized.bdrat"
        ]
    )
    for key, value in proof_stats.items():
        require(
            verifier_evidence["normalized_binary_proof"][key] == value,
            f"proof census mismatch for {key}",
        )
    require(
        proof_stats
        == {
            "addition_records": 45_281,
            "deletion_records": 0,
            "empty_addition_record": 45_281,
            "empty_additions": 1,
            "literals": 410_400,
            "maximum_clause_size": 284,
            "maximum_variable_observed": 9_802,
            "nonempty_additions": 45_280,
            "post_empty_records": 0,
        },
        "independent binary-proof census mismatch",
    )

    constructor_acceptance = strict_json(
        payloads["reviews/order13_k3_constructor_acceptance/evidence.json"],
        "constructor acceptance",
    )
    require(
        constructor_acceptance["verdict"]
        == "ACCEPT_CONSTRUCTOR_A_FOR_PROOF_PRODUCTION_INPUTS",
        "constructor acceptance verdict mismatch",
    )
    preflight = strict_json(
        payloads["reviews/order13_k3_hole9_preflight_constructor/evidence.json"],
        "hole9 preflight",
    )
    require(
        preflight["verdict"] == "ACCEPT_LIVE_HOLE9_PACKAGE_PREFLIGHT",
        "preflight verdict mismatch",
    )
    math_addendum = strict_json(
        payloads["reviews/order13_k3_math_hostile/addendum_evidence.json"],
        "mathematical addendum evidence",
    )
    require(
        math_addendum["verdict"] == "ACCEPT_REVISED_BYTES_MATHEMATICS_UNCHANGED",
        "mathematical addendum verdict mismatch",
    )
    frontier = strict_json(
        payloads["results/order12_frontier_acceptance.json"],
        "C-050 acceptance",
    )
    require(
        frontier["status"]
        == "ACCEPTED_WITH_EXPLICIT_PUBLISHED_THROUGH_ORDER_11_PREMISE",
        "C-050 published-premise boundary mismatch",
    )

    integration_text = payloads[
        "math/lemmas/order13_k3_hole9_certificate_exclusion.md"
    ].decode("utf-8")
    integration_flat = " ".join(integration_text.split())
    required_phrases = (
        "Relative to C-050",
        "hub-free induced \\(C_9\\)",
        "only a relabeling of the whole graph",
        "complete first-use-canonical coloring bank",
        "one template exclusion, not a complete parameter-three slice",
        "does not raise the global lower bound",
    )
    for phrase in required_phrases:
        require(phrase in integration_flat, f"integration note lacks {phrase!r}")

    formula_family_counts = Counter(formula.tags)
    output = {
        "schema": "gamma-theta-order13-k3-hole9-math-coverage-audit-v1",
        "schema_version": 1,
        "verdict": "ACCEPT_EXACT_HOLE9_TEMPLATE_EXCLUSION_AND_C5_C7_REDUCTION",
        "frozen_bindings": frozen_records,
        "exact_boolean_object": {
            "clauses": len(formula.clauses),
            "clean_room_reconstruction_byte_identical": True,
            "literals": literal_count,
            "sha256": sha256(reconstructed_dimacs),
            "size_bytes": len(reconstructed_dimacs),
            "variables": formula.variables,
        },
        "coloring_bank": {
            "canonical_rows": len(retained_bank),
            "complete": True,
            "expected_formula": "(2^9-2)*3^3",
            "first_use_rows_equal_retained_bytes_semantically": True,
            "free_color_name_orbit_size": 6,
            "labeled_rows": labeled_colorings,
            "named_rows_exhaustively_enumerated": 3**N,
            "unsafe_vertex_symmetry_used": False,
        },
        "formula_semantics": {
            "clause_family_counts": dict(formula_family_counts),
            "complement_sign": "e_uv is an H=complement(G) edge; every encoded G-edge is a negative e literal",
            "connected_graph": "every proper cut has a negative H-edge, hence a crossing G-edge",
            "domination_lower_bound": "every H-pair has an external common H-neighbor, equivalently no G-pair dominates",
            "eternal_family_nonempty": True,
            "fixed_triple": [0, 1, 9],
            "fixed_triple_origin": "rim edge 01 plus a guaranteed external common H-neighbor; no unrelated anchor",
            "graph_symmetry_breakers": [],
            "hub_free_induced_hole": 9,
            "one_guard": "each response variable names one guard u and successor D-u+r",
            "resulting_state_dominates": "every selected successor is subject to selected-state domination clauses",
            "theta_gap": "the complete bank forbids every 3-coloring of H, so theta(G)=chi(H)>3",
            "unoccupied_attacks_only": "move variables and response clauses exist only for r not in D",
        },
        "certificate_acceptance": {
            "external_code_audit_no_soundness_blocker": True,
            "external_code_audit_verdict": (
                "ACCEPT_WITH_CAVEATS_NO_SOUNDNESS_BLOCKER"
            ),
            "formula_unsat": True,
            "independent_binary_proof_census": proof_stats,
            "independent_verifier_evidence_sha256": FROZEN[
                "reviews/order13_k3_hole9_certificate_verifier_b/evidence.json"
            ][1],
            "lrat_marker": "c VERIFIED",
            "rup_marker": "s VERIFIED",
            "verifier_scope": "exact SHA-256-bound hole9 CNF only",
        },
        "mathematical_implication": {
            "branch_exclusion": (
                "Relative to C-050 and the accepted C-055 inputs, no "
                "order-13 counterexample with common parameter 3 has a "
                "hub-free induced C9 in its complement."
            ),
            "coverage_after_C053": [
                "hub-free induced C5 in complement",
                "hub-free induced C7 in complement",
            ],
            "coverage_logic": (
                "Any selected C9, either orientation, any named rim edge, "
                "and any guaranteed external common H-neighbor can be "
                "relabelled to the exact template. Overlap among holes or "
                "branches causes no omission."
            ),
            "relative_inputs": [
                "parameter chain",
                "component additivity",
                "C-050 relative to the published through-order-11 premise",
                "Strong Perfect Graph Theorem",
                "C-014 odd-wheel obstruction",
                "C-017 odd-antihole elimination",
                "maximum-independent-state lemma",
                "C-053 near-spanning-hole theorem",
                "C-055 exact graph-to-CNF and template-cover theorem",
            ],
            "remaining_live_formula_templates": ["hole5", "hole7"],
        },
        "scope_exclusions": [
            "no complete order-13 parameter-three exclusion",
            "no exclusion of hole5",
            "no exclusion of hole7",
            "no order-13 parameter-four exclusion",
            "no order-13 parameter-five exclusion",
            "no all-order-13 exclusion",
            "no counterexample lower bound of 14",
            "no universal gamma-theta resolution",
            "no novelty or priority claim",
        ],
    }
    print(
        json.dumps(
            output,
            allow_nan=False,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
