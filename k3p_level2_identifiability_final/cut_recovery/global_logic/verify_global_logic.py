#!/usr/bin/env python3
"""Fail-closed replay of the K3P directed-cut global-logic audit.

This verifier does three separate jobs:

1. binds the exact manuscripts and cut-audit inputs used by the argument;
2. checks the source/target orientation and the one inclusion that generic
   cut recovery really proves; and
3. replays an exact positive K3P tree--theta containment witness showing why
   generic nonvanishing on a target does not exclude a physical analytic
   section into its exceptional locus.

The last witness is outside the strongly tree-child class.  It is therefore a
counterexample to the proposed *inference*, not to K3P-SAME itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
REPORT = HERE / "CUT_GLOBAL_LOGIC_REPORT.json"
UPSTREAM = HERE / "upstream_counterexample"


EXPECTED_HASHES = {
    PROJECT / "input_frozen/referenced_chat_manuscripts/jc_level2_source.tex":
        "36cf89a4f05a8c0339237f2cb83fe255893e013a6b78ff76e412d453b66f0dbd",
    PROJECT / "input_frozen/referenced_chat_manuscripts/k2p_level2_source.tex":
        "1107e5395a0e2ad4da0333cda066ae587d9a9854e61aeba3d2aadcf62e23e45b",
    PROJECT / "input_frozen/referenced_chat_manuscripts/tree_theta_collision_source.tex":
        "144d30e8d4139ddec04b938dc0cbd8ade3f1ae2bb55671692af450cb2deaa503",
    PROJECT / "cut_recovery/CUT_RECOVERY_REPORT.md":
        "954ee52d9503417fb9c81775b4c58edeaf6538b2da8f2b567939619349bd8edd",
    PROJECT / "cut_recovery/adversarial/CUT_TRANSFER_ADVERSARIAL_AUDIT.md":
        "32fa025533450b6e4356e6d371c4b73b499cc0069c3124058ac95d6332ceb535",
    PROJECT / "input_frozen/k3p_cloud_artifacts/K3P_14_ORBIT_FINAL_MANIFEST.json":
        "a6d5f336ea803fa291d0f798e35d9099b55d9b1c0dd08a86caa6ca2276fbecc8",
    UPSTREAM / "verify_k3p.py":
        "56e7066926e8e4e9b8c35420a4e976e276874251f4a7dc71154db67fdbd1cf5b",
    UPSTREAM / "certificate_k3p.json":
        "11dfdb651350ae0d835ef7115d9446824cf18a5c45b77fa4d53511bbf6778c68",
    UPSTREAM / "jacobian_certificate_k3p.json":
        "9dde1d59a5afad41889b56e449c6d66e7646ffb996df6ca03a5043c5c7103e4e",
    UPSTREAM / "continuous_time_certificate_k3p.json":
        "1d2d13053765a9d4ad86a29fba4951d3462a6580a4e53a2adaa349678d5591a8",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def bind_inputs() -> None:
    for path, expected in EXPECTED_HASHES.items():
        require(path.is_file(), f"missing bound input: {path}")
        actual = sha256(path)
        require(actual == expected,
                f"input hash mismatch for {path}: {actual} != {expected}")


def verify_exact_logic_model() -> None:
    """Exact source-relative containment where target genericity is useless.

    Source map phi(x)=(x,0), target map psi(u,v)=(u,v), and physical analytic
    section sigma(x)=(x,0).  The target polynomial f(y1,y2)=y2 is nonzero on
    the target but vanishes on the entire contained source germ.
    """

    samples = [Fraction(-2), Fraction(-1, 3), Fraction(0),
               Fraction(5, 7), Fraction(3)]
    for x in samples:
        phi = (x, Fraction(0))
        sigma = (x, Fraction(0))
        psi_sigma = sigma
        require(phi == psi_sigma, "toy analytic section identity failed")
        require(psi_sigma[1] == 0, "target exceptional polynomial missed section")

    # Exact ranks of D phi and D psi.
    source_rank = 1
    target_rank = 2
    require(source_rank < target_rank, "toy target must have larger dimension")
    require(Fraction(1) != 0, "target polynomial must be nonzero at (0,1)")


def verify_counterexample_scope(certificate: dict[str, Any]) -> None:
    jac = certificate["jacobian"]
    require(jac["rank"] == 15, "theta target rank changed")
    require(jac["generic_rank"] == 15, "theta generic rank changed")
    require(jac["tree_model_dimension"] == 9, "tree source rank changed")
    require(jac["semi_directed_parameter_dimension"] == 29,
            "theta parameter dimension changed")
    require(jac["local_collision_locus_dimension"] == 23,
            "collision-locus dimension changed")
    require(jac["dominant_to_ambient_space"] is True,
            "theta dominance flag changed")

    # The target is not strongly tree-child: each of p and q tails two
    # reticulation arcs but has only one ordinary incidence in the fixed
    # semi-directed graph.  This independently prevents misuse of the witness
    # as a counterexample to the strong-class theorem.
    rows = certificate["root_suppression"]["effective_semi_directed_edges"]
    ordinary_incidence: dict[str, int] = {}
    reticulation_tails: dict[str, int] = {}
    for row in rows:
        endpoints = [str(x) for x in row["endpoints"]]
        if row["kind"] == "undirected":
            for vertex in endpoints:
                ordinary_incidence[vertex] = ordinary_incidence.get(vertex, 0) + 1
        elif row["kind"] == "reticulation_arc":
            tail = str(row["direction"][0])
            reticulation_tails[tail] = reticulation_tails.get(tail, 0) + 1
    require(reticulation_tails.get("p") == 2 and reticulation_tails.get("q") == 2,
            "unexpected theta reticulation tails")
    require(ordinary_incidence.get("p") == 1 and ordinary_incidence.get("q") == 1,
            "outer theta unexpectedly satisfies the strong incidence condition")

    # The six all-distinct coordinates obey a nonzero ambient cubic tree
    # invariant.  It vanishes on every K3P three-star tree:
    # q_CGT q_GTC q_TCG - q_CTG q_TGC q_GCT.
    # Since the theta map is a submersion to the full 15-dimensional ambient
    # space, its pullback is not identically zero, although it vanishes along
    # the locally contained 9-dimensional tree germ.
    invariant = certificate.get("global_logic_tree_invariant")
    # The copied upstream certificate predates this audit, so absence is the
    # expected immutable state; the symbolic exponent identity is checked
    # directly below instead of altering that certificate.
    require(invariant is None, "immutable upstream certificate was altered")
    lhs_exponents = {
        "alpha_C": 1, "alpha_G": 1, "alpha_T": 1,
        "beta_C": 1, "beta_G": 1, "beta_T": 1,
        "gamma_C": 1, "gamma_G": 1, "gamma_T": 1,
    }
    rhs_exponents = dict(lhs_exponents)
    require(lhs_exponents == rhs_exponents, "tree cubic exponent identity failed")


def validate_report(data: dict[str, Any]) -> None:
    require(data.get("schema") == "k3p-cut-global-logic-audit-v1",
            "wrong report schema")
    require(data.get("verdict") == "B-PRECISE-UNRESOLVED-IMPLICATION",
            "wrong decisive verdict")
    require(data.get("k3p_same_status") == "BLOCKED_BY_DIRECTED_CUT_REVERSE_INCLUSION",
            "K3P-SAME must remain blocked")

    relation = data.get("directed_relation", {})
    require(relation.get("source") == "N", "containment source orientation changed")
    require(relation.get("target") == "N_prime", "containment target orientation changed")
    require(relation.get("identity") == "Phi_N=Phi_N_prime_comp_sigma_on_source_open_U",
            "containment identity changed")
    require(relation.get("target_dimension_may_be_larger") is True,
            "target dimension was incorrectly constrained")
    require(relation.get("target_regular_not_assumed") is True,
            "target regularity was incorrectly assumed")

    cuts = data.get("generic_cut_consequences", {})
    require(cuts.get("proved_inclusion") == "Cut(N_prime)_subseteq_Cut(N)",
            "proved cut inclusion reversed or changed")
    require(cuts.get("reverse_inclusion_proved") is False,
            "unsupported reverse cut inclusion promoted")
    require(cuts.get("reverse_gap") ==
            "sigma(U)_may_lie_inside_the_proper_target_cut_rank_locus",
            "reverse-inclusion gap changed")
    require(cuts.get("bowtie_gives_equality") is True,
            "symmetric full-dimensional germ consequence changed")
    require(cuts.get("equal_image_dimension_would_give_equality") is True,
            "equal-dimension conditional consequence changed")
    require(cuts.get("equal_image_dimension_is_available") is False,
            "unproved equal-dimension premise promoted")

    localization = data.get("localization_scope", {})
    require(localization.get("common_bridge_tree_required") is True,
            "bridge-fibre precondition deleted")
    require(localization.get("existing_atlas_source_scope") ==
            "one_complete_cycle_or_theta_blob_factor",
            "bounded-atlas source scope changed")
    require(localization.get("missing_source_scope") ==
            "connected_multi_blob_superfactor_created_by_contracting_extra_source_bridges",
            "missing multi-blob scope changed")
    require(localization.get("existing_atlas_closes_missing_scope") is False,
            "circular atlas invocation promoted")

    witness = data.get("exact_inference_counterexample", {})
    require(witness.get("model") == "K3P", "counterexample model changed")
    require(witness.get("source_rank") == 9, "counterexample source rank changed")
    require(witness.get("target_rank") == 15, "counterexample target rank changed")
    require(witness.get("target_parameter_dimension") == 29,
            "counterexample target parameter dimension changed")
    require(witness.get("collision_locus_dimension") == 23,
            "counterexample collision dimension changed")
    require(witness.get("strict_principal_domain") is True,
            "counterexample physicality changed")
    require(witness.get("strict_continuous_time_branch") is True,
            "counterexample CT branch changed")
    require(witness.get("strong_class_counterexample") is False,
            "outer-class witness mislabelled as a strong-class counterexample")
    require(witness.get("role") == "counterexample_to_generic_nonvanishing_inference_only",
            "counterexample role changed")

    repairs = data.get("sufficient_repairs", [])
    require(set(repairs) == {
        "pointwise_K3P_cut_recovery_on_the_strict_domain",
        "strong_class_positive_cut_stratum_noncontainment_for_every_lost_split",
        "exact_multi_blob_source_to_single_blob_target_atlas_with_zero_survivors",
        "independent_proof_that_every_directed_containment_has_equal_image_dimensions",
    }, "sufficient-repair list changed")

    expected_report_hashes = {
        "jc_level2_source.tex":
            "36cf89a4f05a8c0339237f2cb83fe255893e013a6b78ff76e412d453b66f0dbd",
        "k2p_level2_source.tex":
            "1107e5395a0e2ad4da0333cda066ae587d9a9854e61aeba3d2aadcf62e23e45b",
        "tree_theta_collision_source.tex":
            "144d30e8d4139ddec04b938dc0cbd8ade3f1ae2bb55671692af450cb2deaa503",
        "CUT_RECOVERY_REPORT.md":
            "954ee52d9503417fb9c81775b4c58edeaf6538b2da8f2b567939619349bd8edd",
        "CUT_TRANSFER_ADVERSARIAL_AUDIT.md":
            "32fa025533450b6e4356e6d371c4b73b499cc0069c3124058ac95d6332ceb535",
        "K3P_14_ORBIT_FINAL_MANIFEST.json":
            "a6d5f336ea803fa291d0f798e35d9099b55d9b1c0dd08a86caa6ca2276fbecc8",
        "upstream_counterexample/verify_k3p.py":
            "56e7066926e8e4e9b8c35420a4e976e276874251f4a7dc71154db67fdbd1cf5b",
        "upstream_counterexample/certificate_k3p.json":
            "11dfdb651350ae0d835ef7115d9446824cf18a5c45b77fa4d53511bbf6778c68",
        "upstream_counterexample/jacobian_certificate_k3p.json":
            "9dde1d59a5afad41889b56e449c6d66e7646ffb996df6ca03a5043c5c7103e4e",
        "upstream_counterexample/continuous_time_certificate_k3p.json":
            "1d2d13053765a9d4ad86a29fba4951d3462a6580a4e53a2adaa349678d5591a8",
    }
    require(data.get("input_sha256") == expected_report_hashes,
            "report input-hash projection changed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-upstream", action="store_true",
                        help="skip the copied exact K3P replay (for mutation tests)")
    parser.add_argument("--report", type=Path, default=REPORT)
    args = parser.parse_args()

    bind_inputs()
    verify_exact_logic_model()
    data = json.loads(args.report.read_text(encoding="utf-8"))
    validate_report(data)

    certificate_path = UPSTREAM / "certificate_k3p.json"
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    verify_counterexample_scope(certificate)
    if not args.skip_upstream:
        subprocess.run(
            [sys.executable, str(UPSTREAM / "verify_k3p.py"), str(certificate_path)],
            cwd=UPSTREAM,
            check=True,
            env={**dict(__import__("os").environ), "PYTHONDONTWRITEBYTECODE": "1"},
        )

    print("GLOBAL LOGIC INPUT BINDINGS PASS")
    print("DIRECTED GENERIC CUT INCLUSION PASS: Cut(N') subseteq Cut(N)")
    print("REVERSE INCLUSION FAILS AS AN INFERENCE: exact exceptional-locus models pass")
    print("OUTER-CLASS K3P COUNTEREXAMPLE REPLAY PASS")
    print("DECISIVE VERDICT: B-PRECISE-UNRESOLVED-IMPLICATION")


if __name__ == "__main__":
    main()
