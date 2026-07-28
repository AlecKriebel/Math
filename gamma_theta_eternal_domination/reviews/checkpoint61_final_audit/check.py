#!/usr/bin/env python3
"""Deterministic integration audit for checkpoint 061.

This checker validates the frozen claim boundary, referenced artifact
hashes, public-page scope, attribution/disclosure, and optional staged-file
exclusions.  It does not import the search implementations.
"""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
REPOSITORY = CAMPAIGN.parent
PAGE = REPOSITORY / "docs" / "research" / "gamma-theta-conjecture" / "index.html"
ACCEPTANCE = CAMPAIGN / "results" / "day3_full_response_no_full_acceptance.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def no_duplicate_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        assert key not in result, f"duplicate JSON key: {key}"
        result[key] = value
    return result


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = dict(attrs)
        if values.get("id") is not None:
            self.ids.append(str(values["id"]))
        for attribute in ("href", "src"):
            if values.get(attribute) is not None:
                self.references.append(str(values[attribute]))


EXPECTED_DIRECT_HASHES = {
    # C-085--C-089
    "math/working/full_list_terminal_hitting/NOTE.md":
        "d91fe6087283f92a6ca295f5b9a2a43e7d8ad0a34e89a811490d22bc729595ce",
    "reviews/full_list_terminal_hitting_hostile/REVIEW.md":
        "ee31aef1555dec1ff59edfcdc11a21d7579157bf979222373c7e1f50711aee1f",
    "math/working/k3_side_purity_cap_cycle/NOTE.md":
        "64312289f6d3d87a4c302692c92901caeb9788b16354493e07be01920549f11b",
    "reviews/k3_side_purity_cap_cycle_hostile/REVIEW.md":
        "094ee0e88d20bd3454e49ec8c9a82e3d6799b470d1eeba106f5a11776ffadeef",
    "math/working/k3_side_purity_cap_cycle/result.json":
        "f9dd30333986b0c984910fe3e13464c28bd64a98d85932c8e2df14f805fb1998",
    "reviews/k3_side_purity_cap_cycle_hostile/independent_result.json":
        "9f3285541225a7bd495811853cfbd5a65dce6171fd46cbac6b7fa1f6c5ff90cb",
    "math/working/separated_port_two_color_ladder/NOTE.md":
        "6b9f39e443e99894ffb7490c572149a9ae220ed1d6c445e66df7e0796eec36ff",
    "reviews/separated_port_two_color_ladder_hostile/REVIEW.md":
        "f8877823ce54fd82884541dd09ac5f96aa037d7ece3554e882b6219f3c56cce7",
    "reviews/separated_port_two_color_ladder_hostile/evidence.json":
        "0c66e111583e06404d98e001be5c081e883fe0f5afb72e4bf2b13d38a911a586",
    "math/working/full_response_disjoint_witnesses/NOTE.md":
        "b5c845cee5d887596d1c26660fe741c5ef54763d87d42033c1826f341b4fe6e4",
    # C-090--C-092
    "math/working/order13_single_full_squeeze/NOTE.md":
        "35ddcf61f32723c94b8f0d2fc66aee54331d28dc6b0a372abdac542f41609487",
    "reviews/order13_full_target_hostile/REVIEW.md":
        "d59a0b4663cbb7c4b56faaaad103dd0a2add80a0ebe3c42cc075fd3daf55a6ec",
    "math/working/separated_core_n14_attack/NOTE.md":
        "a619c7acf0dfccbc5767379f68d25f6272d3318db33e433cede39aa70b5ce279",
    "reviews/two_response_replication_hostile/REVIEW.md":
        "538dfd4182d1ca6217cd7fa20226e097270861d3124cdf976406587d18082f51",
    "math/working/separated_core_n14_attack/result.json":
        "f4b1ed7caf63d93798134353233306402202d2ff1439f7eef3f82068e8bfa489",
    "reviews/two_response_replication_hostile/independent_check.py":
        "b5eb2f7f1c1fada8e765d2799710347211ae46a864bdfb120c5bc81ca847a0fc",
}


EXPECTED_STATUSES = {
    "C-085": "PROVED",
    "C-086": "PROVED",
    "C-087": "REFUTED",
    "C-088": "PROVED",
    "C-089": "PROVED",
    "C-090": "CERTIFIED-FINITE",
    "C-091": "PROVED",
    "C-092": "CERTIFIED-FINITE",
    "C-093": "PROVED",
    "C-094": "PROVED",
    "C-095": "REFUTED",
}


REQUIRED_STAGED = {
    "docs/research/gamma-theta-conjecture/index.html",
    "gamma_theta_eternal_domination/CLAIMS.md",
    "gamma_theta_eternal_domination/README.md",
    "gamma_theta_eternal_domination/RESEARCH_LOG.md",
    "gamma_theta_eternal_domination/STATE.md",
    "gamma_theta_eternal_domination/results/day3_full_response_no_full_acceptance.json",
    "gamma_theta_eternal_domination/results/logs/checkpoint61-full-suite.log",
    "gamma_theta_eternal_domination/math/working/order13_no_full_decomposition/NOTE.md",
    "gamma_theta_eternal_domination/math/working/order13_no_full_decomposition/decompose.py",
    "gamma_theta_eternal_domination/reviews/order13_no_full_decomposition_hostile/REVIEW.md",
    "gamma_theta_eternal_domination/reviews/order13_no_full_decomposition_hostile/checker.py",
    "gamma_theta_eternal_domination/reviews/order13_no_full_decomposition_hostile/result.json",
    "gamma_theta_eternal_domination/math/working/physicalized_twosat_endgame/NOTE.md",
    "gamma_theta_eternal_domination/math/working/physicalized_twosat_endgame/verify.py",
    "gamma_theta_eternal_domination/math/working/physicalized_twosat_endgame/result.json",
    "gamma_theta_eternal_domination/reviews/physicalized_twosat_endgame_hostile/REVIEW.md",
    "gamma_theta_eternal_domination/reviews/physicalized_twosat_endgame_hostile/independent_check.py",
    "gamma_theta_eternal_domination/reviews/physicalized_twosat_endgame_hostile/independent_result.json",
}

ALLOWED_STAGED_EXACT = {
    "docs/research/gamma-theta-conjecture/index.html",
    "gamma_theta_eternal_domination/CLAIMS.md",
    "gamma_theta_eternal_domination/README.md",
    "gamma_theta_eternal_domination/RESEARCH_LOG.md",
    "gamma_theta_eternal_domination/STATE.md",
    "gamma_theta_eternal_domination/results/day3_full_response_no_full_acceptance.json",
    "gamma_theta_eternal_domination/results/logs/checkpoint61-full-suite.log",
    "gamma_theta_eternal_domination/math/working/order13_no_full_decomposition/NOTE.md",
    "gamma_theta_eternal_domination/math/working/order13_no_full_decomposition/decompose.py",
}

ALLOWED_STAGED_PREFIXES = (
    "gamma_theta_eternal_domination/math/working/full_list_terminal_hitting/",
    "gamma_theta_eternal_domination/math/working/full_response_disjoint_witnesses/",
    "gamma_theta_eternal_domination/math/working/full_response_witness_bound/",
    "gamma_theta_eternal_domination/math/working/k3_side_purity_cap_cycle/",
    "gamma_theta_eternal_domination/math/working/order13_no_full_probe/",
    "gamma_theta_eternal_domination/math/working/order13_single_full_squeeze/",
    "gamma_theta_eternal_domination/math/working/physicalized_twosat_endgame/",
    "gamma_theta_eternal_domination/math/working/separated_core_n14_attack/",
    "gamma_theta_eternal_domination/reviews/checkpoint61_adversary/",
    "gamma_theta_eternal_domination/reviews/checkpoint61_final_audit/",
    "gamma_theta_eternal_domination/reviews/full_list_terminal_hitting_hostile/",
    "gamma_theta_eternal_domination/reviews/full_response_witness_bound_hostile/",
    "gamma_theta_eternal_domination/reviews/k3_side_purity_cap_cycle_hostile/",
    "gamma_theta_eternal_domination/reviews/order13_full_target_hostile/",
    "gamma_theta_eternal_domination/reviews/order13_no_full_decomposition_hostile/",
    "gamma_theta_eternal_domination/reviews/physicalized_twosat_endgame_hostile/",
    "gamma_theta_eternal_domination/reviews/separated_port_two_color_ladder_hostile/",
    "gamma_theta_eternal_domination/reviews/two_response_replication_hostile/",
)


def audit_acceptance() -> dict[str, object]:
    acceptance = json.loads(
        ACCEPTANCE.read_text(encoding="utf-8"),
        object_pairs_hook=no_duplicate_object,
    )
    boundary = acceptance["claim_boundary"]
    assert boundary == {
        "universal_conjecture_resolved": False,
        "counterexample_found": False,
        "complete_k3_theorem": False,
        "complete_order13_exclusion": False,
        "order13_parameter3_full_response_branch_excluded": True,
        "order13_parameter3_no_full_branch_excluded": False,
        "finite_frontier": 13,
        "finite_frontier_raised_in_this_checkpoint": False,
        "general_order14_search_started": False,
        "second_paper_issued": False,
        "novelty_priority_claimed": False,
    }

    accepted = acceptance["accepted_claims"]
    assert {key: value["status"] for key, value in accepted.items()} == (
        EXPECTED_STATUSES
    )
    assert "no-full branch remains open" in accepted["C-090"]["scope_warning"]
    assert "structural reduction only" in accepted["C-093"]["scope_warning"]
    assert "literal-level identity only" in accepted["C-094"]["scope_warning"]
    assert "supporting cross-clauses" in accepted["C-095"]["summary"]
    assert acceptance["no_full_probe"]["outcome"] == "TIMEOUT_NONCLAIM"
    assert acceptance["no_full_probe"]["interpretation"] == (
        "No SAT or UNSAT inference is accepted."
    )
    assert acceptance["retracted_or_rejected"]["false_order13_count"][
        "status"
    ] == "RETRACTED_BEFORE_PROMOTION"
    assert acceptance["retracted_or_rejected"]["automatic_clause_edge_transport"][
        "status"
    ] == "REFUTED_BY_C095"

    certificate = acceptance["order13_full_response_certificate"]
    artifact_rows = {
        certificate["formula"]["path"]: certificate["formula"],
        certificate["proof"]["path"]: certificate["proof"],
        "math/working/order13_single_full_squeeze/minimal-core.cnf": {
            "sha256": certificate["reduced_core"]["cnf_sha256"]
        },
        "math/working/order13_single_full_squeeze/minimal-core.drat": {
            "sha256": certificate["reduced_core"]["proof_sha256"]
        },
        "reviews/order13_full_target_hostile/checker.py": {
            "sha256": certificate["clean_room_reconstruction"]["checker_sha256"]
        },
        "reviews/order13_full_target_hostile/result.json": {
            "sha256": certificate["clean_room_reconstruction"]["result_sha256"]
        },
        "reviews/order13_full_target_hostile/REVIEW.md": {
            "sha256": certificate["clean_room_reconstruction"]["review_sha256"]
        },
    }
    no_full = acceptance["no_full_structural_audit"]
    artifact_rows.update(
        {
            "math/working/order13_no_full_decomposition/NOTE.md": {
                "sha256": no_full["source_note_sha256"]
            },
            "math/working/order13_no_full_decomposition/decompose.py": {
                "sha256": no_full["splitter_sha256"]
            },
            "reviews/order13_no_full_decomposition_hostile/REVIEW.md": {
                "sha256": no_full["hostile_review_sha256"]
            },
            "reviews/order13_no_full_decomposition_hostile/checker.py": {
                "sha256": no_full["independent_checker_sha256"]
            },
            "reviews/order13_no_full_decomposition_hostile/result.json": {
                "sha256": no_full["independent_result_sha256"]
            },
        }
    )
    physical = acceptance["physical_clause_transport_control"]
    artifact_rows.update(
        {
            "math/working/physicalized_twosat_endgame/NOTE.md": {
                "sha256": physical["source_note_sha256"]
            },
            "math/working/physicalized_twosat_endgame/verify.py": {
                "sha256": physical["source_verifier_sha256"]
            },
            "math/working/physicalized_twosat_endgame/result.json": {
                "sha256": physical["source_result_sha256"]
            },
            "reviews/physicalized_twosat_endgame_hostile/independent_check.py": {
                "sha256": physical["independent_checker_sha256"]
            },
            "reviews/physicalized_twosat_endgame_hostile/independent_result.json": {
                "sha256": physical["independent_result_sha256"]
            },
            "reviews/physicalized_twosat_endgame_hostile/REVIEW.md": {
                "sha256": physical["hostile_review_sha256"]
            },
        }
    )
    for relative, row in artifact_rows.items():
        path = CAMPAIGN / relative
        assert sha256(path) == row["sha256"], relative
        if "bytes" in row:
            assert path.stat().st_size == row["bytes"], relative

    old_review = (
        CAMPAIGN / "reviews" / "checkpoint61_adversary" / "REVIEW.md"
    )
    assert sha256(old_review) == acceptance["verification"][
        "pre_final_c085_c092_integration_review_sha256"
    ]
    assert sha256(
        CAMPAIGN / "math" / "working" / "order13_no_full_probe" / "instance.cnf"
    ) == acceptance["no_full_probe"]["instance_sha256"]

    for relative, expected in EXPECTED_DIRECT_HASHES.items():
        assert sha256(CAMPAIGN / relative) == expected, relative
    return acceptance


def audit_claims_and_summaries() -> None:
    claims = (CAMPAIGN / "CLAIMS.md").read_text(encoding="utf-8")
    rows = {
        match.group(1): (match.group(2), match.group(3))
        for match in re.finditer(
            r"^\| (C-\d{3}) \| ([A-Z-]+) \| (.*)$", claims, re.MULTILINE
        )
    }
    for claim, status in EXPECTED_STATUSES.items():
        assert rows[claim][0] == status

    c090 = rows["C-090"][1]
    assert "only the order-13 parameter-three full-response branch" in c090
    assert "no-full-list branch remains open" in c090
    assert "global frontier remains 13" in c090
    assert "connectivity is not assumed" in c090
    assert "full target need not be unique" in c090
    assert "structural reduction, not an exclusion" in rows["C-093"][1]
    assert "cannot be substituted into a graph attack" in rows["C-095"][1]
    assert "not a counterexample" in rows["C-095"][1]
    assert "No claim above resolves" in claims
    assert "No complete" in claims and "universal resolution is" in claims

    sources = {
        "CLAIMS.md": claims,
        "README.md": (CAMPAIGN / "README.md").read_text(encoding="utf-8"),
        "STATE.md": (CAMPAIGN / "STATE.md").read_text(encoding="utf-8"),
        "RESEARCH_LOG.md": (CAMPAIGN / "RESEARCH_LOG.md").read_text(
            encoding="utf-8"
        ),
    }
    assert "|A|\\ge7" not in sources["CLAIMS.md"]
    assert "|A|\\ge7" not in sources["README.md"]
    assert sources["STATE.md"].count("|A|\\ge7,|Q|\\le3") == 1
    assert sources["RESEARCH_LOG.md"].count("|A|\\ge7,|Q|\\le3") == 1
    for name in ("STATE.md", "RESEARCH_LOG.md"):
        position = sources[name].index("|A|\\ge7,|Q|\\le3")
        context = sources[name][max(0, position - 180) : position + 180].lower()
        assert "false" in context and "retract" in context

    normalized = {
        name: " ".join(text.lower().split()) for name, text in sources.items()
    }
    assert "no claim above resolves" in normalized["CLAIMS.md"]
    for name in sources:
        assert "universal conjecture remains unresolved" in normalized[name]
    assert "complete order-13 exclusion" in sources["README.md"]
    assert "not a complete order-13 exclusion" in sources["README.md"]
    assert "No general\norder-14 search has begun" in sources["README.md"]
    assert "sole current paper" in sources["STATE.md"]


def audit_page() -> dict[str, object]:
    text = PAGE.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    parser.close()
    assert len(parser.ids) == len(set(parser.ids))
    for reference in parser.references:
        if reference.startswith("#"):
            assert reference[1:] in parser.ids, reference
        elif not re.match(r"^(?:[a-z]+:)?//", reference):
            local = (PAGE.parent / reference.split("#", 1)[0]).resolve()
            if reference.split("#", 1)[0].endswith("/"):
                local /= "index.html"
            assert local.exists(), reference

    required = (
        'meta name="author" content="Alec Kriebel, with heavy assistance '
        'from ChatGPT 5.6 Sol"',
        '"name": "Alec Kriebel"',
        "A research program led by Alec Kriebel, with heavy assistance "
        "from ChatGPT 5.6 Sol",
        "The conjecture has not been resolved.",
        "no lower bound of 14 is claimed",
        "The complete order-13 search has <strong>not</strong> been finished",
        "Parameter-three full-response branch — certified impossible.",
        "No-full-list \\(C_5\\) and \\(C_7\\) branches — still live.",
        "Parameters \\(4\\) and \\(5\\) — still live.",
        "The no-full-list branch remains open, so the global frontier is still 13.",
        "The no-full order-13 census is narrower.",
        "at least five nonneutral vertices and at most five neutral vertices",
        "supporting cross-edges do not transport",
        "not a second paper",
        "heavy assistance from ChatGPT 5.6 Sol under Alec Kriebel's direction",
    )
    for phrase in required:
        assert phrase in text, phrase
    assert "|A|\\ge7" not in text

    paper_links = set(
        re.findall(r'href="([^"]*papers/[^"]*)"', text, flags=re.IGNORECASE)
    )
    assert paper_links == {"../../papers/gamma-theta-order-12-frontier/"}
    return {
        "sha256": sha256(PAGE),
        "bytes": PAGE.stat().st_size,
        "ids": len(parser.ids),
        "references": len(parser.references),
    }


def staged_paths() -> list[str]:
    completed = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "-z"],
        cwd=REPOSITORY,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [
        item.decode("utf-8")
        for item in completed.stdout.split(b"\0")
        if item
    ]


def audit_staging(require_staged: bool) -> dict[str, object]:
    staged = staged_paths()
    if require_staged:
        assert staged, "the index is empty"
        missing = sorted(REQUIRED_STAGED - set(staged))
        assert not missing, f"required checkpoint files not staged: {missing}"

    forbidden_exact = {
        "gamma_theta_eternal_domination/results/synthesis_k3_template_bank_runs/"
        "hole5_seed0_600s/proof.drat",
    }
    forbidden_prefixes = (
        "dimension_three_keller_degree/",
        "gamma_theta_eternal_domination/certificates/"
        "order12_k4_v3_case0111_recovery_attempt000001/",
        "gamma_theta_eternal_domination/certificates/"
        "synthesis_k3_hole5_signature_seed0_lrat_c033/",
        "gamma_theta_eternal_domination/certificates/"
        "synthesis_k3_hole7_full_bank_seed0_addition_only/",
        "gamma_theta_eternal_domination/math/working/terminal_cube_patterns/",
    )
    bad: list[str] = []
    for path in staged:
        if path not in ALLOWED_STAGED_EXACT and not path.startswith(
            ALLOWED_STAGED_PREFIXES
        ):
            bad.append(path)
        if path in forbidden_exact or path.startswith(forbidden_prefixes):
            bad.append(path)
        if path.endswith("replay.lock") or "__pycache__/" in path or path.endswith(
            ".pyc"
        ):
            bad.append(path)
        prefix = (
            "gamma_theta_eternal_domination/math/working/"
            "order13_no_full_decomposition/"
        )
        if path.startswith(prefix) and path not in {
            prefix + "NOTE.md",
            prefix + "decompose.py",
        }:
            bad.append(path)
    assert not sorted(set(bad)), f"forbidden staged paths: {sorted(set(bad))}"
    return {"files": len(staged), "checked": bool(staged) or require_staged}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-staged",
        action="store_true",
        help="also require the checkpoint's essential files in the Git index",
    )
    args = parser.parse_args()

    acceptance = audit_acceptance()
    audit_claims_and_summaries()
    page = audit_page()
    staging = audit_staging(args.require_staged)
    subprocess.run(
        ["git", "diff", "--check"],
        cwd=REPOSITORY,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = {
        "acceptance_sha256": sha256(ACCEPTANCE),
        "claim_boundary": acceptance["claim_boundary"],
        "direct_hashes_checked": len(EXPECTED_DIRECT_HASHES),
        "page": page,
        "staging": staging,
        "status": "PASS",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
