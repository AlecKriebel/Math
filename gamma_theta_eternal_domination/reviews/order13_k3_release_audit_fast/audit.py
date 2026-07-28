#!/usr/bin/env python3
"""Read-only release audit for the order-13, parameter-three manuscript."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess


CAMPAIGN = Path(__file__).resolve().parents[2]
TEX = CAMPAIGN / "paper/order13_k3_complete/main.tex"
PDF = CAMPAIGN / "paper/order13_k3_complete/main.pdf"
CLAIMS = CAMPAIGN / "CLAIMS.md"
ACCEPTANCE = CAMPAIGN / "results/order13_k3_complete_acceptance.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cnf_header(path: Path) -> tuple[int, int]:
    with path.open("rt", encoding="ascii") as stream:
        line = stream.readline().strip()
    match = re.fullmatch(r"p cnf ([0-9]+) ([0-9]+)", line)
    assert match
    return int(match.group(1)), int(match.group(2))


def proof_shape(path: Path) -> dict[str, object]:
    additions = 0
    deletions = 0
    terminal = None
    with path.open("rb") as stream:
        for raw in stream:
            line = raw.strip()
            if not line:
                continue
            terminal = line
            if line.startswith(b"d "):
                deletions += 1
            else:
                additions += 1
    return {
        "additions": additions,
        "deletions": deletions,
        "terminal_empty_clause": terminal == b"0",
    }


def decode_graph6(record: str) -> list[int]:
    assert record and record[0] != ">"
    n = ord(record[0]) - 63
    assert 0 <= n <= 62
    bits: list[int] = []
    for char in record[1:]:
        value = ord(char) - 63
        assert 0 <= value <= 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    assert len(bits) >= n * (n - 1) // 2
    adjacency = [0] * n
    position = 0
    for high in range(1, n):
        for low in range(high):
            if bits[position]:
                adjacency[high] |= 1 << low
                adjacency[low] |= 1 << high
            position += 1
    return adjacency


def dominates(adjacency: list[int], vertices: tuple[int, ...]) -> bool:
    covered = 0
    for vertex in vertices:
        covered |= adjacency[vertex] | (1 << vertex)
    return covered == (1 << len(adjacency)) - 1


def gamma(adjacency: list[int]) -> int:
    for size in range(1, len(adjacency) + 1):
        if any(
            dominates(adjacency, vertices)
            for vertices in itertools.combinations(range(len(adjacency)), size)
        ):
            return size
    raise AssertionError


def alpha(adjacency: list[int]) -> int:
    n = len(adjacency)
    for size in range(n, 0, -1):
        for vertices in itertools.combinations(range(n), size):
            mask = sum(1 << vertex for vertex in vertices)
            if all(adjacency[vertex] & mask == 0 for vertex in vertices):
                return size
    return 0


def independent_domination(adjacency: list[int]) -> int:
    n = len(adjacency)
    for size in range(1, n + 1):
        for vertices in itertools.combinations(range(n), size):
            mask = sum(1 << vertex for vertex in vertices)
            if all(adjacency[vertex] & mask == 0 for vertex in vertices):
                if dominates(adjacency, vertices):
                    return size
    raise AssertionError


def colorable(adjacency: list[int], colors: int) -> bool:
    n = len(adjacency)
    order = sorted(range(n), key=lambda vertex: adjacency[vertex].bit_count(), reverse=True)
    assigned = [-1] * n

    def visit(position: int) -> bool:
        if position == n:
            return True
        vertex = order[position]
        forbidden = {
            assigned[neighbor]
            for neighbor in range(n)
            if (adjacency[vertex] >> neighbor) & 1 and assigned[neighbor] >= 0
        }
        for color in range(colors):
            if color not in forbidden:
                assigned[vertex] = color
                if visit(position + 1):
                    return True
                assigned[vertex] = -1
        return False

    return visit(0)


def theta(adjacency: list[int]) -> int:
    n = len(adjacency)
    full = (1 << n) - 1
    complement = [
        full ^ (1 << vertex) ^ adjacency[vertex] for vertex in range(n)
    ]
    for colors in range(1, n + 1):
        if colorable(complement, colors):
            return colors
    raise AssertionError


def greatest_eternal_family(adjacency: list[int], size: int) -> set[tuple[int, ...]]:
    n = len(adjacency)
    family = {
        state
        for state in itertools.combinations(range(n), size)
        if dominates(adjacency, state)
    }
    changed = True
    while changed:
        changed = False
        remove: set[tuple[int, ...]] = set()
        for state in family:
            occupied = set(state)
            for attack in range(n):
                if attack in occupied:
                    continue
                legal = False
                for guard in state:
                    if (adjacency[guard] >> attack) & 1:
                        successor = tuple(
                            sorted((occupied - {guard}) | {attack})
                        )
                        if successor in family:
                            legal = True
                            break
                if not legal:
                    remove.add(state)
                    break
        if remove:
            family.difference_update(remove)
            changed = True
    return family


def control_profile(record: str) -> dict[str, object]:
    adjacency = decode_graph6(record)
    family = greatest_eternal_family(adjacency, 3)
    return {
        "order": len(adjacency),
        "gamma": gamma(adjacency),
        "i": independent_domination(adjacency),
        "alpha": alpha(adjacency),
        "gamma_infinity_is_3": bool(family),
        "theta": theta(adjacency),
        "greatest_eternal_triple_family": len(family),
        "dominating_triples": sum(
            dominates(adjacency, state)
            for state in itertools.combinations(range(len(adjacency)), 3)
        ),
    }


def canonical_graph6(record: str) -> str:
    labelg = CAMPAIGN / "tools/nauty2_9_3/labelg"
    completed = subprocess.run(
        [str(labelg), "-q"],
        input=record + "\n",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return completed.stdout.strip()


def main() -> None:
    tex = TEX.read_text(encoding="utf-8")
    claims = CLAIMS.read_text(encoding="utf-8")
    acceptance = json.loads(ACCEPTANCE.read_text(encoding="utf-8"))
    c096 = acceptance["accepted_claims"]["C-096"]
    c097 = acceptance["accepted_claims"]["C-097"]

    artifacts = {
        "C-090 instance": (
            CAMPAIGN
            / "math/working/order13_single_full_squeeze/minimal-instance.cnf",
            4_808_845,
            "d5a2f17ad6e61cb7ca5cb9d2930b6a0738fec32ee1d9956207dc67bb297dcb13",
            (9802, 85409),
        ),
        "C-090 proof": (
            CAMPAIGN
            / "math/working/order13_single_full_squeeze/minimal-proof.drat",
            19_874_489,
            "653b01e904b97c01bfa25fbbea29fbadee603918dbaff0ea41b7ad09460fb910",
            None,
        ),
        "C-096 instance": (
            CAMPAIGN / c096["instance"]["path"],
            c096["instance"]["bytes"],
            c096["instance"]["sha256"],
            (c096["instance"]["variables"], c096["instance"]["clauses"]),
        ),
        "C-096 proof": (
            CAMPAIGN / c096["proof"]["path"],
            c096["proof"]["bytes"],
            c096["proof"]["sha256"],
            None,
        ),
        "C-097 instance": (
            CAMPAIGN / c097["instance"]["path"],
            c097["instance"]["bytes"],
            c097["instance"]["sha256"],
            (c097["instance"]["variables"], c097["instance"]["clauses"]),
        ),
        "C-097 proof": (
            CAMPAIGN / c097["proof"]["path"],
            c097["proof"]["bytes"],
            c097["proof"]["sha256"],
            None,
        ),
    }
    artifact_checks = {}
    for name, (path, expected_bytes, expected_hash, expected_header) in artifacts.items():
        observed = {
            "path": str(path.relative_to(CAMPAIGN)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        if expected_header:
            observed["cnf_header"] = list(cnf_header(path))
        observed["pass"] = (
            observed["bytes"] == expected_bytes
            and observed["sha256"] == expected_hash
            and (
                expected_header is None
                or observed["cnf_header"] == list(expected_header)
            )
        )
        artifact_checks[name] = observed

    c096_proof = proof_shape(artifacts["C-096 proof"][0])
    c097_proof = proof_shape(artifacts["C-097 proof"][0])
    proof_shapes = {
        "C-096": c096_proof,
        "C-097": c097_proof,
    }
    assert c096_proof == {
        "additions": 78697,
        "deletions": 0,
        "terminal_empty_clause": True,
    }
    assert c097_proof == {
        "additions": 156205,
        "deletions": 0,
        "terminal_empty_clause": True,
    }

    full_control = control_profile(r"LF\|ul\XzVsaqJ")
    neutral_control = control_profile("LDZZa^g|fkw[iH")
    assert full_control == {
        "order": 13,
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity_is_3": True,
        "theta": 3,
        "greatest_eternal_triple_family": 157,
        "dominating_triples": 157,
    }
    assert neutral_control == {
        "order": 13,
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity_is_3": True,
        "theta": 3,
        "greatest_eternal_triple_family": 139,
        "dominating_triples": 139,
    }
    neutral_canonical = canonical_graph6("LDZZa^g|fkw[iH")
    assert neutral_canonical == c096["sharp_control"]["graph6"]

    replay_paths = [
        "repro/c097/replay.py",
        "reviews/order13_full_target_hostile/checker.py",
        "reviews/tight_micro_hostile_review/checker.py",
        "reviews/order13_no_full_a7_hostile/checker.py",
    ]
    assert all((CAMPAIGN / path).is_file() for path in replay_paths)

    theorem_scope = {
        "exact_main_statement_present": (
            r"\gamma(G)=\gaminf(G)=3<\theta(G)" in tex
            and "does not exclude parameters four or five at order 13" in tex
            and "universal conjecture" in tex
            and "parameter three at arbitrary order" in tex
        ),
        "conditional_frontier_wording_present": (
            "Relative to the published through-order-11 result and the separately"
            in tex
        ),
        "full_no_full_exhaustive_split_present": (
            "The two\nbranches exhaust all possibilities." in tex
        ),
        "lower_order_not_used_in_main_assembly": (
            "published through-order-11" not in tex[
                tex.index(r"\begin{proof}[Proof of Theorem"):tex.index(
                    r"\begin{corollary}\label{cor:frontier}"
                )
            ]
        ),
        "unoccupied_exactly_one_model_present": (
            "After an attack at an unoccupied vertex, exactly one" in tex
            and "adjacent guard moves to the attacked vertex" in tex
        ),
    }
    assert all(theorem_scope.values())

    claims_alignment = {
        "C-090 row_has_stats_and_hashes": all(
            token in claims
            for token in (
                "9,802-variable, 85,409-clause",
                "d5a2f17ad6e61cb7ca5cb9d2930b6a0738fec32ee1d9956207dc67bb297dcb13",
                "653b01e904b97c01bfa25fbbea29fbadee603918dbaff0ea41b7ad09460fb910",
            )
        ),
        "C-096 row_has_stats_and_hashes": all(
            token in claims
            for token in (
                "1,222-variable, 24,694-clause",
                c096["instance"]["sha256"],
                c096["proof"]["sha256"],
            )
        ),
        "C-097 row_has_stats_and_hashes": all(
            token in claims
            for token in (
                "9,802-variable, 84,614-clause",
                c097["instance"]["sha256"],
                c097["proof"]["sha256"],
            )
        ),
        "residual_census_sums_to_84614": sum(
            (3, 1, 715, 78, 1716, 2860, 2860, 8580, 8580,
             59049, 10, 6, 12, 2, 140, 1, 1)
        ) == 84614,
        "signature_multisets_1716": (
            len(list(itertools.combinations_with_replacement(range(8), 6)))
            == 1716
        ),
    }
    assert all(claims_alignment.values())

    primary_2015 = (
        CAMPAIGN
        / "literature/sources/km2015_src/gamma_theta_Revised_July_11.tex"
    ).read_text(encoding="utf-8")
    attribution = {
        "paper_says_2015_identified_gap_and_reopened_question": (
            "identified a gap in that argument and reopened the implication as an"
            in tex
            and "explicit question \\cite{KlostermeyerMynhardt2015}" in tex
        ),
        "paper_attributes_later_name_to_subsequent_literature": (
            "Subsequent literature" in tex
            and "refers to their conjectural formulation as the" in tex
            and "\\cite{MacGillivrayMynhardtVirgile2022}" in tex
        ),
        "2015_source_identifies_2009_error": (
            "The proof given in\n\\cite{KM2} is incorrect" in primary_2015
        ),
        "2015_source_states_explicit_open_question": (
            "Does there exist a graph $G$ such that $\\gamma(G)=\\gamma"
            in primary_2015
            and "^{\\infty}(G)$ and $\\gamma(G)<\\theta(G)$?" in primary_2015
        ),
        "2015_source_uses_gamma_theta_name": bool(
            re.search(r"gamma.?theta conjecture", primary_2015, re.IGNORECASE)
        ),
        "verdict": "PASS",
    }
    assert attribution["paper_says_2015_identified_gap_and_reopened_question"]
    assert attribution["paper_attributes_later_name_to_subsequent_literature"]
    assert attribution["2015_source_identifies_2009_error"]
    assert attribution["2015_source_states_explicit_open_question"]
    assert not attribution["2015_source_uses_gamma_theta_name"]

    release_tag = subprocess.run(
        [
            "git",
            "ls-remote",
            "--tags",
            "origin",
            "refs/tags/gamma-theta-order13-k3-v1.0.0",
        ],
        cwd=CAMPAIGN.parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    ).stdout.strip()

    result = {
        "schema": "order13-k3-release-audit-fast-v1",
        "verdict": "PASS",
        "publication_blockers": [],
        "artifact_checks": artifact_checks,
        "proof_shapes": proof_shapes,
        "control_profiles": {
            "full_response_theta_ablation": full_control,
            "three_neutral_sharp_control": neutral_control,
            "three_neutral_canonical_graph6": neutral_canonical,
        },
        "theorem_scope": theorem_scope,
        "claims_alignment": claims_alignment,
        "replay_paths": {path: (CAMPAIGN / path).is_file() for path in replay_paths},
        "attribution_audit": attribution,
        "release_tag": {
            "remote_exists_at_audit_time": bool(release_tag),
            "note": (
                "Expected to be absent before release; public PDF must not be "
                "published until the tag exists and binds the audited files."
            ),
        },
        "file_hashes": {
            "main.tex": sha256(TEX),
            "main.pdf": sha256(PDF),
            "CLAIMS.md": sha256(CLAIMS),
            "acceptance.json": sha256(ACCEPTANCE),
        },
    }
    assert all(item["pass"] for item in artifact_checks.values())
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
