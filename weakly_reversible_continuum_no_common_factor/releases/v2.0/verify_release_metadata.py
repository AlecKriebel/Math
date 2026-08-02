#!/usr/bin/env python3
"""Verify the frozen Version 2.0.0 package metadata and byte anchors.

This check is intentionally separate from the mathematical verifiers.  It
ties the human-readable and machine-readable rate tables to one directed edge
order, checks the exact family formulas at both displayed specializations,
freezes the final manuscript and audit artifacts by SHA-256, and prevents a
Version 2 DOI from being asserted before one has actually been minted.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


release_dir = Path(__file__).resolve().parent

directed_support = (
    (0, 1), (1, 0), (0, 4), (4, 0), (0, 6), (6, 0),
    (1, 7), (7, 1), (2, 4), (4, 2), (2, 7), (7, 2),
    (2, 9), (9, 2), (3, 4), (4, 3), (5, 9), (9, 5),
    (8, 9), (9, 8),
)

frozen_rates = (
    845740, 7732494, 702464, 3920, 437290, 4380128, 1405575,
    5600, 706384, 900816, 1518755, 6873328, 3920, 896896,
    3863552, 3920, 3863552, 15680, 4346496, 658560,
)

clean_rates = (
    1160, 10296, 976, 23, 560, 5977, 1800, 25, 1629, 1237,
    1, 9152, 653, 1214, 5368, 1, 5368, 70, 6039, 915,
)

byte_anchors = {
    "output/pdf/manuscript-v2.0.0.pdf":
        "fe429cf073b30cacfe1ba75624236cda2545c44076f711d4319dcb22ff79512b",
    "audit_packet/specialist_audit_one_page.pdf":
        "b7429aed0e5edf572848cbcf856b3da89ff05447967c3dc12d9d386e0270f3d2",
    "source/MANUSCRIPT_V2.md":
        "e2ac3cf9556eb1bacf53a76dd09963a5a60ca2d47c7fe2c62a0bdfa164dd18db",
    "priority_v2/AUDIT.md":
        "2957ee7486e4a3e16c93c2c0d739ba797d14244e125ff7f58fad76757f3621ec",
    "audit_v2/audit_results.json":
        "f10a7ed2b66e3f18952bdebbaca90a35aecfaf54c17e5b31a2f1436a4ed7536e",
    "family/remainder_matrix.csv":
        "f7061a40fefd9ca2285f83ba64ce9af63cb76a45a69aca95beb5fbfb17465486",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(relative_path: str):
    with (release_dir / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def read_rate_csv(relative_path: str):
    support = []
    frozen = []
    clean = []
    with (release_dir / relative_path).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 20
    for expected_index, row in enumerate(rows):
        assert int(row["index"]) == expected_index
        support.append((int(row["source_index"]), int(row["target_index"])))
        frozen.append(int(row["frozen_v1_rate"]))
        clean.append(int(row["clean_rate"]))
    return tuple(support), tuple(frozen), tuple(clean)


def main() -> None:
    # reproduce.sh intentionally creates .venv-release before invoking this
    # verifier.  Archive omission of that generated directory is checked by
    # RELEASE_CHECKS.md and the archive listings, not here.
    assert not (release_dir / "tmp").exists()
    assert not list(release_dir.rglob("manuscript-v2-draft.pdf"))

    for relative_path, expected_hash in byte_anchors.items():
        path = release_dir / relative_path
        assert path.is_file(), relative_path
        assert sha256(path) == expected_hash, relative_path

    source_rows = read_rate_csv("source/rates.csv")
    data_rows = read_rate_csv("data/rates.csv")
    assert source_rows == data_rows
    assert source_rows == (directed_support, frozen_rates, clean_rates)

    with (release_dir / "network.csv").open(newline="", encoding="utf-8") as handle:
        network_rows = list(csv.DictReader(handle))
    assert tuple(
        (int(row["source_index"]), int(row["target_index"]))
        for row in network_rows
    ) == directed_support
    assert tuple(int(row["rate"]) for row in network_rows) == frozen_rates

    vectors = read_json("data/rate_vectors.json")
    assert tuple(map(tuple, vectors["directed_support_order"])) == directed_support
    assert tuple(vectors["frozen_v1"]["rates"]) == frozen_rates
    assert tuple(vectors["clean_integral_optimum"]["rates"]) == clean_rates
    assert max(clean_rates) == 10296 and sum(clean_rates) == 52464
    assert sp.gcd_list(clean_rates) == 1

    theorem = read_json("data/theorem.json")
    a, b, c, d = sp.symbols("a b c d")
    formulas = tuple(sp.sympify(text, locals={"a": a, "b": b, "c": c, "d": d})
                     for text in theorem["family"]["rate_formulas_in_directed_support_order"])
    assert tuple(value.subs({a: 3920, b: 3920, c: 15680, d: 658560})
                 for value in formulas) == frozen_rates
    assert tuple(value.subs({a: 653, b: 1, c: 70, d: 915})
                 for value in formulas) == clean_rates
    assert theorem["family"]["constraint_matrix_rank"] == 16
    assert theorem["family"]["dimension"] == 4
    assert theorem["minimality"]["minimum_species"] == 3
    assert theorem["minimality"]["minimum_species_attained_by_this_construction"] is True
    assert theorem["minimality"]["proved_lower_bounds"] == {
        "stoichiometric_rank_for_any_target": 2,
        "complexes_for_three_species_weakly_reversible_target": 5,
        "reversible_pairs_for_three_species_reversible_target": 3,
        "reversible_pairs_for_one_linkage_three_species_reversible_target": 4,
        "maximum_complex_degree": 2,
    }
    assert theorem["minimality"][
        "lower_bounds_other_than_species_and_one_linkage_rank_known_attained"
    ] is False
    assert theorem["minimality"]["current_support_claimed_globally_minimal"] is False

    release = read_json("data/release.json")
    assert release["version"] == "2.0.0"
    assert release["doi"] is None
    assert release["doi_status"] == "not_minted_at_release_candidate_freeze"
    citation = (release_dir / "CITATION.cff").read_text(encoding="utf-8")
    assert "version: 2.0.0" in citation
    assert "identifiers:" not in citation

    independent = read_json("audit_v2/audit_results.json")
    assert independent["status"] == "PASS"
    assert independent["family"]["rank"] == 16
    assert independent["family"]["nullity"] == 4
    assert independent["clean_rates"]["maximum_rate"] == 10296
    assert independent["clean_rates"]["rate_sum"] == 52464

    print("PASS: Version 2.0.0 package metadata and byte anchors agree")
    print("  final manuscript SHA-256: fe429cf073b30cac...ff79512b")
    print("  specialist handout SHA-256: b7429aed0e5edf57...270f3d2")
    print("  source/data rate tables and exact family formulas agree")
    print("  no Version 2 DOI is asserted before minting")


if __name__ == "__main__":
    main()
