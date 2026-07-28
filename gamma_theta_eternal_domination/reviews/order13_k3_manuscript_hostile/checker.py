#!/usr/bin/env python3
"""Independent, lightweight audit of the tagged order-13 k=3 paper package."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import re
import shutil
import subprocess


CAMPAIGN = Path(__file__).resolve().parents[2]
REPO = CAMPAIGN.parent
PAPER = CAMPAIGN / "paper/order13_k3_complete"
TAG = "gamma-theta-order13-k3-v1.0.0"

EXPECTED_HASHES = {
    "paper/order13_k3_complete/main.tex":
        "56afff0796fb602589d38714793e42b6864a5454d71d8da51b559daa3daea8f2",
    "paper/order13_k3_complete/references.bib":
        "79600fcc86edce90e6cedf1eb1ee07ff3544ac7e0eb62bef4d9904fa59f0615b",
    "paper/order13_k3_complete/main.pdf":
        "6768cecf0d46672f7d56cbda2715b49ef18470e5d60b3c7912fc9999843ae5a4",
    "math/working/order13_single_full_squeeze/minimal-instance.cnf":
        "d5a2f17ad6e61cb7ca5cb9d2930b6a0738fec32ee1d9956207dc67bb297dcb13",
    "math/working/order13_single_full_squeeze/minimal-proof.drat":
        "653b01e904b97c01bfa25fbbea29fbadee603918dbaff0ea41b7ad09460fb910",
    "math/working/order13_no_full_tight_five_five/micro-instance.cnf":
        "3d1a1379eb2a90ffd399e5a830b1a81881ed527c6e9db06574a390085cb5c1e0",
    "math/working/order13_no_full_tight_five_five/micro-proof.additions.drat":
        "c4f1989ac80474a86b75ba939e494bde5928b2727fd61297eb695f3937222eee",
    "math/working/order13_no_full_a7_structured/instance.cnf":
        "76ff2768c7afd95ee535f8684515b0b15319b1f5ca69085447a1f7eba66393e1",
    "math/working/order13_no_full_a7_structured/proof.additions.drat":
        "c985ce0a602a91a0d323594e3aeecf210fa5131027ef4b6c9b6e4d4b628f1848",
}

EXPECTED_CNFS = {
    "math/working/order13_single_full_squeeze/minimal-instance.cnf":
        (9802, 85409, 4_808_845),
    "math/working/order13_no_full_tight_five_five/micro-instance.cnf":
        (1222, 24694, 447_906),
    "math/working/order13_no_full_a7_structured/instance.cnf":
        (9802, 84614, 4_784_714),
}

EXPECTED_ADDITION_PROOFS = {
    "math/working/order13_no_full_tight_five_five/micro-proof.additions.drat":
        (78_697, 5_426_898),
    "math/working/order13_no_full_a7_structured/proof.additions.drat":
        (156_205, 8_878_465),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def check_cnf(rel: str, expected: tuple[int, int, int]) -> None:
    path = CAMPAIGN / rel
    variables, clauses, size = expected
    assert path.stat().st_size == size
    with path.open("rt", encoding="ascii") as stream:
        header = stream.readline().split()
        assert header == ["p", "cnf", str(variables), str(clauses)]
        seen = 0
        for line in stream:
            literals = [int(token) for token in line.split()]
            assert literals and literals[-1] == 0
            assert all(1 <= abs(literal) <= variables for literal in literals[:-1])
            seen += 1
    assert seen == clauses


def check_addition_proof(rel: str, expected: tuple[int, int]) -> None:
    path = CAMPAIGN / rel
    additions, size = expected
    assert path.stat().st_size == size
    count = 0
    last = None
    with path.open("rt", encoding="ascii") as stream:
        for line in stream:
            assert not line.startswith("d ")
            values = [int(token) for token in line.split()]
            assert values and values[-1] == 0
            last = values
            count += 1
    assert count == additions
    assert last == [0]


def decode_graph6(record: str) -> list[int]:
    assert record and 0 <= ord(record[0]) - 63 <= 62
    n = ord(record[0]) - 63
    bits: list[int] = []
    for char in record[1:]:
        value = ord(char) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    assert len(bits) >= n * (n - 1) // 2
    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if bits[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return adjacency


def graph_stats(record: str) -> dict[str, int]:
    adjacency = decode_graph6(record)
    n = len(adjacency)
    universe = (1 << n) - 1
    closed = [adjacency[v] | (1 << v) for v in range(n)]

    def dominates(mask: int) -> bool:
        reached = 0
        for vertex in range(n):
            if mask & (1 << vertex):
                reached |= closed[vertex]
        return reached == universe

    def independent(mask: int) -> bool:
        return all(
            not (adjacency[vertex] & mask)
            for vertex in range(n)
            if mask & (1 << vertex)
        )

    gamma = next(
        size
        for size in range(1, n + 1)
        if any(
            dominates(sum(1 << vertex for vertex in choice))
            for choice in itertools.combinations(range(n), size)
        )
    )
    alpha = max(mask.bit_count() for mask in range(1 << n) if independent(mask))
    independent_domination = min(
        mask.bit_count()
        for mask in range(1, 1 << n)
        if independent(mask) and dominates(mask)
    )

    def eternal_kernel(size: int) -> set[int]:
        family = {
            sum(1 << vertex for vertex in choice)
            for choice in itertools.combinations(range(n), size)
            if dominates(sum(1 << vertex for vertex in choice))
        }
        while True:
            deleted: list[int] = []
            for state in family:
                for attacked in range(n):
                    if state & (1 << attacked):
                        continue
                    responses = (
                        state & adjacency[attacked]
                    )
                    if not any(
                        ((state ^ (1 << guard)) | (1 << attacked)) in family
                        for guard in range(n)
                        if responses & (1 << guard)
                    ):
                        deleted.append(state)
                        break
            if not deleted:
                return family
            family.difference_update(deleted)

    gamma_infinity = next(
        size for size in range(gamma, n + 1) if eternal_kernel(size)
    )

    # Since alpha=3 in both controls, a proper 3-coloring of the complement
    # proves theta=3.  The search below independently finds such a coloring.
    complement = [universe ^ (1 << v) ^ adjacency[v] for v in range(n)]
    colors = [-1] * n

    def colorable(done: int) -> bool:
        if done == universe:
            return True
        vertex = -1
        options: list[int] | None = None
        for candidate in range(n):
            if done & (1 << candidate):
                continue
            forbidden = {
                colors[other]
                for other in range(n)
                if colors[other] >= 0 and complement[candidate] & (1 << other)
            }
            available = [color for color in range(3) if color not in forbidden]
            if options is None or len(available) < len(options):
                vertex, options = candidate, available
        assert options is not None
        for color in options:
            colors[vertex] = color
            if colorable(done | (1 << vertex)):
                return True
        colors[vertex] = -1
        return False

    assert colorable(0)
    theta = 3
    kernel = eternal_kernel(3)
    return {
        "n": n,
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
        "gamma_infinity": gamma_infinity,
        "theta": theta,
        "greatest_family_size": len(kernel),
    }


def main() -> None:
    for rel, expected in EXPECTED_HASHES.items():
        assert sha256(CAMPAIGN / rel) == expected
    for rel, expected in EXPECTED_CNFS.items():
        check_cnf(rel, expected)
    for rel, expected in EXPECTED_ADDITION_PROOFS.items():
        check_addition_proof(rel, expected)

    tex = (PAPER / "main.tex").read_text(encoding="utf-8")
    required_fragments = [
        r"\author{Alec Kriebel}",
        r"\gamma(G)=\gaminf(G)=3<\theta(G)",
        "unconditional on lower-order enumeration",
        "does not exclude order-13 parameters four or five",
        "does not resolve",
        "the universal conjecture",
        "exactly one adjacent guard moves",
        "attacks are made only at",
        "identified a gap in that argument",
        "reopened the implication as an",
        "explicit question",
        "heavy assistance from ChatGPT 5.6 Sol",
        "No outside",
        "individual was contacted",
    ]
    assert all(fragment in tex for fragment in required_fragments)
    assert r"\verb!LF\|ul\XzVsaqJ!" in tex
    assert r"\verb!LDZZa^g|fkw[iH!" in tex

    log = (PAPER / "main.log").read_text(encoding="utf-8", errors="replace")
    forbidden_log_patterns = [
        r"LaTeX Warning:",
        r"Package .* Warning:",
        r"Overfull \\\\hbox",
        r"Underfull \\\\hbox",
        r"undefined references",
        r"Emergency stop",
        r"Fatal error",
    ]
    assert not any(
        re.search(pattern, log, flags=re.IGNORECASE)
        for pattern in forbidden_log_patterns
    )

    replay = json.loads((CAMPAIGN / "repro/c097/replay-result.json").read_text())
    assert replay["verdict"] == "PASS"
    assert replay["universal_conjecture_status"] == "UNRESOLVED"
    assert all(replay["hash_checks"].values())
    assert replay["four_neutral_replay"]["strict_rup"] is True
    assert replay["residual_replay"]["addition_only_rup"] is True
    assert replay["residual_replay"]["coverage"] == {
        "anchor_permutations": 6,
        "every_type_pair_normalizes_to_0_and_2": True,
        "label10_nonzero_exactly_at_most_three_neutral": True,
        "ordered_distinct_type_pairs": 6,
        "sorted_residual_signature_sequences": 1716,
    }

    full = json.loads(
        (CAMPAIGN / "reviews/order13_full_target_hostile/result.json").read_text()
    )
    assert full["verdict"] == "PASS"
    assert full["clean_room_formula"]["byte_identical_to_frozen"] is True
    assert full["clean_room_formula"]["variables"] == 9802
    assert full["clean_room_formula"]["clauses"] == 85409
    assert full["positive_control"]["greatest_eternal_family_states"] == 157

    controls = {
        r"LF\|ul\XzVsaqJ": graph_stats(r"LF\|ul\XzVsaqJ"),
        "LDZZa^g|fkw[iH": graph_stats("LDZZa^g|fkw[iH"),
    }
    assert controls[r"LF\|ul\XzVsaqJ"] == {
        "n": 13, "gamma": 3, "i": 3, "alpha": 3,
        "gamma_infinity": 3, "theta": 3, "greatest_family_size": 157,
    }
    assert controls["LDZZa^g|fkw[iH"] == {
        "n": 13, "gamma": 3, "i": 3, "alpha": 3,
        "gamma_infinity": 3, "theta": 3, "greatest_family_size": 139,
    }

    tag_commit = subprocess.check_output(
        ["git", "rev-parse", f"{TAG}^{{}}"], cwd=REPO, text=True
    ).strip()
    assert tag_commit == "883e796cb163f360d8052e94ae507d3cbb3e6599"
    for rel in (
        "paper/order13_k3_complete/main.tex",
        "paper/order13_k3_complete/references.bib",
        "paper/order13_k3_complete/main.pdf",
    ):
        tagged = subprocess.check_output(
            ["git", "show", f"{TAG}:gamma_theta_eternal_domination/{rel}"],
            cwd=REPO,
        )
        assert hashlib.sha256(tagged).hexdigest() == EXPECTED_HASHES[rel]

    pdfinfo = shutil.which("pdfinfo")
    assert pdfinfo is not None
    metadata = subprocess.check_output(
        [pdfinfo, str(PAPER / "main.pdf")], text=True
    )
    assert "Author:          Alec Kriebel" in metadata
    assert "Pages:           10" in metadata
    assert "Encrypted:       no" in metadata
    assert "Form:            none" in metadata

    result = {
        "verdict": "PASS",
        "tag": TAG,
        "tag_commit": tag_commit,
        "paper_hashes": {
            "main.tex": EXPECTED_HASHES["paper/order13_k3_complete/main.tex"],
            "references.bib":
                EXPECTED_HASHES["paper/order13_k3_complete/references.bib"],
            "main.pdf": EXPECTED_HASHES["paper/order13_k3_complete/main.pdf"],
        },
        "formula_and_proof_hashes": {
            rel: EXPECTED_HASHES[rel]
            for rel in EXPECTED_HASHES
            if rel.endswith((".cnf", ".drat"))
        },
        "controls": controls,
        "pdf": {
            "author": "Alec Kriebel",
            "pages": 10,
            "encrypted": False,
            "forms": False,
            "build_log_clean": True,
        },
        "scope": {
            "main_theorem": "complete order-13 parameter-three exclusion",
            "lower_order_dependency": False,
            "order13_remaining_parameters": [4, 5],
            "universal_conjecture": "UNRESOLVED",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
