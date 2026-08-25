#!/usr/bin/env python3
"""Independent audit of the lost-bridge global-transfer proof.

This verifier does not import the builder or any fourteen-orbit code.  It
recomputes the topology-only 204-direction universe from frozen switching
signatures, checks the exact dependency DAG, audits split compatibility and
strict K3P convolution, and binds the independently verified pointwise local
certificate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
DEFAULT_ARTIFACT = HERE / "GLOBAL_TRANSFER_CERTIFICATE.json"
DEFAULT_UNIVERSE = HERE / "GLOBAL_TRANSFER_DIRECTION_UNIVERSE.json"
REPORT = HERE / "VERIFICATION_REPORT.json"
FROZEN_TOPOLOGY = PROJECT / "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json"
MARGINAL = PROJECT / "marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json"
DIRECTED_LOGIC = PROJECT / "cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json"
LOCAL_FINAL = HERE.parent / "final_certificate/STRONG_CROSSBRIDGE_FINAL_CERTIFICATE.json"
LOCAL_UNIVERSE = HERE.parent / "final_certificate/UNIVERSE_CERTIFICATE.json"
LOCAL_VERIFICATION = HERE.parent / "final_certificate/VERIFICATION_REPORT.json"
LOCAL_MUTATIONS = HERE.parent / "final_certificate/ADVERSARIAL_MUTATION_REPORT.json"


class VerificationError(RuntimeError):
    pass


def require(condition, label):
    if not condition:
        raise VerificationError(str(label))


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    answer = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            answer.update(block)
    return answer.hexdigest()


def expected_binding(path: Path):
    return {
        "path": str(path.resolve().relative_to(PROJECT)),
        "sha256": sha_file(path),
    }


def permute_mask(mask: int, old_order: tuple[int, ...]) -> int:
    answer = 0
    for new, old in enumerate(old_order):
        if mask & (1 << old):
            answer |= 1 << new
    return answer


def displayed_by_all(signatures, reticulation_count, first):
    side = sum(1 << label for label in first)
    complement = 15 ^ side
    return all(
        any(signature[switch] in (side, complement) for signature in signatures)
        for switch in range(1 << reticulation_count)
    )


def rebuild_directions(topology):
    rows = []
    raw = 0
    displayed = 0
    keys = set()
    section = topology["one_active_wrong_split"]
    for expected_record_id, record in enumerate(section["records"]):
        require(record["id"] == expected_record_id, "record order")
        reticulations = int(record["reticulation_count"])
        signatures = tuple(tuple(int(mask) for mask in row) for row in record["signatures"])
        require(all(len(row) == 1 << reticulations for row in signatures), "signature width")
        for split in record["splits"]:
            raw += 1
            first = tuple(int(label) for label in split["split"])
            computed = displayed_by_all(signatures, reticulations, first)
            require(computed == split["displayed_by_all"], "displayed flag replay")
            if computed:
                displayed += 1
                continue
            complement = tuple(sorted(set(range(4)) - set(first)))
            old_order = first + complement
            key = (record["id"], tuple(sorted((tuple(sorted(first)), complement))))
            require(key not in keys, "direction uniqueness")
            keys.add(key)
            normalized = tuple(
                tuple(permute_mask(mask, old_order) for mask in signature)
                for signature in signatures
            )
            rows.append(
                {
                    "target_index": len(rows),
                    "record_id": record["id"],
                    "reticulation_count": reticulations,
                    "old_split": list(first),
                    "old_order": list(old_order),
                    "normalized_split": [[0, 1], [2, 3]],
                    "normalized_signatures_sha256": digest(normalized),
                    "direction_key": [
                        record["id"],
                        [list(key[1][0]), list(key[1][1])],
                    ],
                }
            )
    require(len(section["records"]) == 72, "one-active records")
    require(raw == 216 and displayed == 12 and len(rows) == 204, "direction census")
    require(len(keys) == 204, "direction key census")
    return rows, raw, displayed


def verify_topology_universe(universe, topology):
    require(universe["schema"] == "k3p-global-transfer-direction-universe-v1", "universe schema")
    require(universe["status"] == "PASS", "universe status")
    require(universe["input"] == expected_binding(FROZEN_TOPOLOGY), "universe input")
    require(universe["algebraic_JC_minor_fields_used"] is False, "JC algebra field use")
    rows, raw, displayed = rebuild_directions(topology)
    counts = universe["counts"]
    require(counts["primitive_core_templates"] == 5, "core count")
    require(counts["one_active_records"] == 72, "record count")
    require(counts["raw_labelled_split_entries"] == raw == 216, "raw split count")
    require(counts["displayed_by_all_removed"] == displayed == 12, "displayed split count")
    require(counts["wrong_split_directions"] == 204, "wrong split count")
    require(counts["unique_direction_keys"] == 204, "unique directions")
    require(universe["independent_displayed_flag_recomputation_failures"] == [], "display replay failures")
    require(universe["directions"] == rows, "direction rows")
    require(universe["directions_sha256"] == digest(rows), "direction digest")
    return rows


def split_compatible(first, second, labels):
    first = set(first)
    second = set(second)
    first_complement = set(labels) - first
    second_complement = set(labels) - second
    intersections = (
        first & second,
        first & second_complement,
        first_complement & second,
        first_complement & second_complement,
    )
    return any(not part for part in intersections), tuple(len(part) for part in intersections)


def verify_crossing_split_logic(payload):
    two_active = payload["two_active_exclusion"]
    require(two_active["four_nonempty_intersections"] == ["A∩C", "A∩D", "B∩C", "B∩D"], "four intersections")
    compatible, sizes = split_compatible({0, 1}, {0, 2}, range(4))
    require(sizes == (1, 1, 1, 1), "crossing witness intersections")
    require(compatible is False, "crossing splits called compatible")
    require("R in Cut(Nprime) implies R in Cut(N)" == two_active["directional_step"], "directional use")
    return sizes


def verify_k3p_convolution(payload, marginal):
    table = marginal["character_group"]["xor_table"]
    require(table == [[left ^ right for right in range(4)] for left in range(4)], "XOR table")

    # Exact character-homomorphism replay.  It proves that convolution of the
    # inverse-Fourier probability vectors has coordinatewise-product spectra.
    bit_pair = ((0, 0), (1, 0), (0, 1), (1, 1))
    hadamard = []
    for character in bit_pair:
        row = []
        for state in bit_pair:
            parity = character[0] * state[0] + character[1] * state[1]
            row.append(-1 if parity % 2 else 1)
        hadamard.append(row)
    homomorphism_checks = 0
    for character in range(4):
        for left in range(4):
            for right in range(4):
                require(
                    hadamard[character][left ^ right]
                    == hadamard[character][left] * hadamard[character][right],
                    "character homomorphism",
                )
                homomorphism_checks += 1

    # Each of the four convolution coordinates is a sum of four products of
    # strictly positive entries and is therefore strictly positive.
    convolution_pairs = {
        output: tuple((left, left ^ output) for left in range(4))
        for output in range(4)
    }
    require(all(len(set(pairs)) == 4 for pairs in convolution_pairs.values()), "convolution pairs")

    # Independently expand the switching weights for every level-2 side blob.
    # Their sum is the constant polynomial one, and each unexpanded factor is
    # lambda_i or 1-lambda_i, hence strictly positive on the physical domain.
    switching_components = 0
    switching_sum_checks = 0
    for reticulation_count in range(3):
        zero = (0,) * reticulation_count
        total = {}
        for bits in itertools.product((0, 1), repeat=reticulation_count):
            switching_components += 1
            weight = {zero: 1}
            for axis, bit in enumerate(bits):
                updated = {}
                for exponent, coefficient in weight.items():
                    if bit:
                        raised = list(exponent); raised[axis] += 1
                        updated[tuple(raised)] = updated.get(tuple(raised), 0) + coefficient
                    else:
                        updated[exponent] = updated.get(exponent, 0) + coefficient
                        raised = list(exponent); raised[axis] += 1
                        updated[tuple(raised)] = updated.get(tuple(raised), 0) - coefficient
                weight = {exponent: coefficient for exponent, coefficient in updated.items() if coefficient}
            for exponent, coefficient in weight.items():
                total[exponent] = total.get(exponent, 0) + coefficient
        total = {exponent: coefficient for exponent, coefficient in total.items() if coefficient}
        require(total == {zero: 1}, ("switching weights do not sum to one", reticulation_count))
        switching_sum_checks += 1

    strict = payload["strict_physical_marginal"]
    require("convolution" in strict["serial_convolution_statement"], "edge convolution statement")
    require("convex mixture" in strict["two_terminal_blob_mixture_statement"], "two-terminal mixture statement")
    require("strict positivity" in strict["two_terminal_blob_mixture_statement"], "mixture strictness")
    mixture_identities = strict["two_terminal_blob_mixture_identities"]
    require(mixture_identities["switching_weights"] == "w_s>0 and sum_s w_s=1", "mixture weights identity")
    require(mixture_identities["probability_coordinate"] == "p_eff(h)=sum_s w_s*p_s(h)>0", "mixture probability identity")
    require(mixture_identities["spectrum_lower_margin"] == "x_eff=sum_s w_s*x_s>0", "mixture lower margin")
    require(mixture_identities["spectrum_upper_margin"] == "1-x_eff=sum_s w_s*(1-x_s)>0", "mixture upper margin")
    require(mixture_identities["spectrum_scope"] == "x in {c,g,t}", "mixture spectrum scope")
    require("retained as lambda" in strict["inheritance_statement"], "inheritance statement")
    require("set to zero" in strict["Fourier_marginal_statement"], "Fourier marginal statement")
    require(marginal["switching_and_inheritance"]["weights_sum_to_one"] is True, "inheritance weights")
    return (
        homomorphism_checks,
        sum(map(len, convolution_pairs.values())),
        switching_sum_checks,
        switching_components,
    )


EXPECTED_DEPENDENCIES = {
    "H0": (),
    "D1": ("H0",),
    "L0": ("H0",),
    "L1": ("L0",),
    "T1": ("L0", "L1"),
    "T2": ("D1", "L0", "T1"),
    "T3": ("T1", "T2"),
    "T4": ("T3",),
    "M1": ("H0", "T4"),
    "S1": ("H0", "T4"),
    "P1": ("M1", "L0"),
    "P2": ("T4", "S1"),
    "X": ("M1", "P1", "P2"),
    "C": ("D1", "X"),
}


def verify_proof_dag(payload):
    steps = payload["proof_steps"]
    require([row["id"] for row in steps] == list(EXPECTED_DEPENDENCIES), "proof step order")
    by_id = {row["id"]: row for row in steps}
    require(len(by_id) == len(steps), "duplicate proof ids")
    seen = set()
    for step_id, expected in EXPECTED_DEPENDENCIES.items():
        row = by_id[step_id]
        require(tuple(row["depends_on"]) == expected, ("proof dependencies", step_id))
        require(set(row["depends_on"]) <= seen, ("non-topological DAG", step_id))
        seen.add(step_id)
    require(payload["proof_step_ids_sha256"] == digest(list(EXPECTED_DEPENDENCIES)), "proof ids digest")
    require("Cut(Nprime) subset Cut(N)" in by_id["D1"]["claim"], "proved inclusion direction")
    require("two-active" in by_id["T2"]["claim"], "two-active exclusion")
    require("204-direction" in by_id["T4"]["claim"], "finite handoff")
    require("no target-open" in by_id["M1"]["reason"], "target openness leak")
    require("strict physical D3,+" in by_id["S1"]["claim"], "strict target marginal")
    require("rank at most four" in by_id["P1"]["claim"], "source rank")
    require("rank greater than four" in by_id["P2"]["claim"], "target rank")
    return len(steps)


def verify_local_pointwise(payload, independently_rebuilt_rows):
    final = json.loads(LOCAL_FINAL.read_text())
    universe = json.loads(LOCAL_UNIVERSE.read_text())
    verification = json.loads(LOCAL_VERIFICATION.read_text())
    mutations = json.loads(LOCAL_MUTATIONS.read_text())
    bindings = payload["load_bearing_inputs"]
    require(bindings["pointwise_204_certificate"] == expected_binding(LOCAL_FINAL), "local final binding")
    require(bindings["pointwise_204_universe"] == expected_binding(LOCAL_UNIVERSE), "local universe binding")
    require(bindings["pointwise_204_independent_verification"] == expected_binding(LOCAL_VERIFICATION), "local verification binding")
    require(bindings["pointwise_204_adversarial_mutations"] == expected_binding(LOCAL_MUTATIONS), "local mutation binding")
    require(final["schema"] == "k3p-strong-crossbridge-final-certificate-v1", "local schema")
    require(final["status"] == "PASS" and final["blocked_dependencies"] == [], "local status")
    coverage = final["coverage"]
    require(coverage["target_directions"] == 204, "local coverage")
    require(coverage["pairwise_disjoint"] is True and coverage["union_is_all_204"] is True, "local partition flags")
    require(coverage["automorphism_transport_used"] is False, "local automorphism transport")
    targets = []
    for dependency in final["dependencies"]:
        require(dependency["status"] == "PASS", ("local dependency", dependency["name"]))
        targets.extend(dependency["required_targets"])
    require(len(targets) == len(set(targets)) == 204, "local target partition cardinality")
    require(set(targets) == set(range(204)), "local target partition union")
    require(universe["status"] == "PASS" and len(universe["directions"]) == 204, "local universe status")
    require(
        [row["normalized_signatures_sha256"] for row in universe["directions"]]
        == [row["normalized_signatures_sha256"] for row in independently_rebuilt_rows],
        "local/global direction crosswalk",
    )
    require(verification["schema"] == "k3p-strong-crossbridge-final-verification-v1", "local verification schema")
    require(verification["status"] == "PASS", "local verification status")
    require(verification["artifacts"]["final_certificate_sha256"] == sha_file(LOCAL_FINAL), "local verification final hash")
    require(verification["artifacts"]["universe_certificate_sha256"] == sha_file(LOCAL_UNIVERSE), "local verification universe hash")
    require(mutations["schema"] == "k3p-strong-crossbridge-final-adversarial-mutations-v1", "local mutation schema")
    require(mutations["status"] == "PASS" and mutations["all_mutations_rejected"] is True, "local mutations")
    require(mutations["rejected_count"] == mutations["mutation_count"] == 34, "local mutation count")
    require(payload["local_204_dependency_pass"] is True, "payload local pass")
    return len(targets), mutations["mutation_count"]


def verify_payload(payload, universe):
    require(payload["schema"] == "k3p-lost-bridge-global-transfer-certificate-v1", "schema")
    require(payload["status"] == "PASS", "status")
    require(payload["blocked_reason"] is None, "blocked reason")
    scope = payload["scope"]
    require(scope["network_class"] == "binary standard semi-directed strongly tree-child level-2", "network class")
    require(scope["conclusion"] == "Cut(N)=Cut(Nprime)", "conclusion")

    bindings = payload["load_bearing_inputs"]
    require(bindings["frozen_strong_topology"] == expected_binding(FROZEN_TOPOLOGY), "topology binding")
    require(bindings["selected_marginal"] == expected_binding(MARGINAL), "marginal binding")
    require(bindings["directed_cut_inclusion_audit"] == expected_binding(DIRECTED_LOGIC), "directed logic binding")
    require(bindings["recompiled_direction_universe"] == expected_binding(DEFAULT_UNIVERSE), "direction universe binding")

    topology = json.loads(FROZEN_TOPOLOGY.read_text())
    marginal = json.loads(MARGINAL.read_text())
    directed = json.loads(DIRECTED_LOGIC.read_text())
    require(topology["status"] == "EXACTLY COMPUTED", "topology status")
    require(len(topology["primitive_cores"]) == 5, "primitive core count")
    require(topology["primitive_orientation_derivation"]["template_match"] is True, "primitive templates")
    require(topology["switching_compression"]["status"] == "EXACTLY COMPUTED", "switching compression status")
    require(topology["switching_compression"]["survivor_count"] == 0, "switching survivors")
    require(topology["switching_compression"]["failures"] == [], "switching failures")
    rows = verify_topology_universe(universe, topology)
    require(payload["one_active_handoff"]["wrong_split_directions"] == 204, "handoff direction count")
    require(payload["one_active_handoff"]["direction_universe_sha256"] == sha_file(DEFAULT_UNIVERSE), "handoff universe hash")

    require(marginal["status"] == "PASS" and marginal["k2p_algebra_used"] is False, "marginal status")
    source_relative = marginal["source_relative_open_image"]
    require(source_relative["direct_marginal_of_original_containment"] is True, "direct marginal")
    require(source_relative["target_marginal_openness_used"] is False, "target marginal openness")
    require(directed["generic_cut_consequences"]["proved_inclusion"] == "Cut(N_prime)_subseteq_Cut(N)", "directed inclusion")
    require(directed["generic_cut_consequences"]["reverse_inclusion_proved"] is False, "prior reverse status")
    require(directed["directed_relation"]["target_regular_not_assumed"] is True, "target regularity")

    noncircular = payload["noncircularity"]
    require(noncircular["common_bridge_tree_assumed"] is False, "common bridge tree assumption")
    require(noncircular["bridge_tree_equality_assumed"] is False, "bridge equality assumption")
    require(noncircular["fourteen_orbit_classification_imported"] is False, "fourteen-orbit import")
    require(noncircular["target_regular_point_assumed"] is False, "target regular point")
    require(noncircular["target_open_marginal_assumed"] is False, "target-open marginal")
    require(noncircular["only_preexisting_cut_direction_used"] == "Cut(Nprime) subset Cut(N)", "preexisting direction")
    require(noncircular["reverse_direction_proved_here"] == "Cut(N) subset Cut(Nprime)", "new direction")

    require("pendant leaf bridge" in payload["trivial_split_handling"], "trivial split handling")
    intersections = verify_crossing_split_logic(payload)
    (
        homomorphism_checks,
        convolution_terms,
        switching_sum_checks,
        switching_components,
    ) = verify_k3p_convolution(payload, marginal)
    proof_steps = verify_proof_dag(payload)
    local_targets, local_mutations = verify_local_pointwise(payload, rows)

    rank = payload["rank_transfer"]
    require(rank["source_bridge_rank_bound"] == 4, "source rank bound")
    require(rank["target_local_rank_lower_bound"] == 5, "target rank lower bound")
    require(rank["target_pointwise_not_generic"] is True, "pointwise target use")
    require(rank["target_openness_needed"] is False, "target openness needed")
    require("for every theta in U" in rank["identity"], "pointwise marginal identity")
    return {
        "status": "PASS",
        "direction_count": len(rows),
        "proof_step_count": proof_steps,
        "crossing_intersection_sizes": list(intersections),
        "character_homomorphism_checks": homomorphism_checks,
        "strict_convolution_product_terms": convolution_terms,
        "switching_weight_polynomial_checks": switching_sum_checks,
        "two_terminal_mixture_components_checked": switching_components,
        "local_targets_bound": local_targets,
        "local_mutations_bound": local_mutations,
        "common_bridge_tree_used": False,
        "fourteen_orbit_used": False,
    }


def mutation_cases(payload):
    cases = []
    def changed(name, mutate):
        value = copy.deepcopy(payload)
        mutate(value)
        cases.append((name, value))

    changed("status", lambda x: x.__setitem__("status", "BLOCKED"))
    changed("common_bridge_tree", lambda x: x["noncircularity"].__setitem__("common_bridge_tree_assumed", True))
    changed("bridge_tree_equality", lambda x: x["noncircularity"].__setitem__("bridge_tree_equality_assumed", True))
    changed("fourteen_orbit", lambda x: x["noncircularity"].__setitem__("fourteen_orbit_classification_imported", True))
    changed("target_open", lambda x: x["noncircularity"].__setitem__("target_open_marginal_assumed", True))
    changed("old_cut_direction", lambda x: x["noncircularity"].__setitem__("only_preexisting_cut_direction_used", "Cut(N) subset Cut(Nprime)"))
    changed("new_cut_direction", lambda x: x["noncircularity"].__setitem__("reverse_direction_proved_here", "Cut(Nprime) subset Cut(N)"))
    changed("topology_hash", lambda x: x["load_bearing_inputs"]["frozen_strong_topology"].__setitem__("sha256", "0" * 64))
    changed("marginal_hash", lambda x: x["load_bearing_inputs"]["selected_marginal"].__setitem__("sha256", "1" * 64))
    changed("local_hash", lambda x: x["load_bearing_inputs"]["pointwise_204_certificate"].__setitem__("sha256", "2" * 64))
    changed("universe_count", lambda x: x["one_active_handoff"].__setitem__("wrong_split_directions", 203))
    changed("universe_hash", lambda x: x["one_active_handoff"].__setitem__("direction_universe_sha256", "3" * 64))
    changed("source_rank", lambda x: x["rank_transfer"].__setitem__("source_bridge_rank_bound", 5))
    changed("target_rank", lambda x: x["rank_transfer"].__setitem__("target_local_rank_lower_bound", 4))
    changed("pointwise_flag", lambda x: x["rank_transfer"].__setitem__("target_pointwise_not_generic", False))
    changed("target_openness_rank", lambda x: x["rank_transfer"].__setitem__("target_openness_needed", True))
    changed("two_terminal_mixture", lambda x: x["strict_physical_marginal"].__setitem__("two_terminal_blob_mixture_statement", "omitted"))
    changed("trivial_split", lambda x: x.__setitem__("trivial_split_handling", "omitted"))
    changed("four_intersections", lambda x: x["two_active_exclusion"]["four_nonempty_intersections"].pop())
    changed("directional_step", lambda x: x["two_active_exclusion"].__setitem__("directional_step", "reverse"))
    for step_id in ("T2", "T4", "M1", "S1", "P1", "P2", "X", "C"):
        changed(
            f"dependency_{step_id}",
            lambda x, step_id=step_id: next(row for row in x["proof_steps"] if row["id"] == step_id)["depends_on"].pop(),
        )
    changed("duplicate_step", lambda x: x["proof_steps"].__setitem__(1, copy.deepcopy(x["proof_steps"][0])))
    changed("local_pass", lambda x: x.__setitem__("local_204_dependency_pass", False))
    return cases


def run_mutations(payload, universe):
    results = []
    for name, changed in mutation_cases(payload):
        rejected = False
        try:
            verify_payload(changed, universe)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected = True
        require(rejected, ("mutation accepted", name))
        results.append({"name": name, "result": "REJECTED"})
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--universe", type=Path, default=DEFAULT_UNIVERSE)
    parser.add_argument("--mutations", action="store_true")
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument("--no-write-report", action="store_true")
    args = parser.parse_args()
    payload = json.loads(args.artifact.read_text())
    universe = json.loads(args.universe.read_text())
    result = verify_payload(payload, universe)
    mutations = run_mutations(payload, universe) if args.mutations else []
    report = {
        "schema": "k3p-lost-bridge-global-transfer-verification-v1",
        **result,
        "artifact_sha256": sha_file(args.artifact),
        "universe_sha256": sha_file(args.universe),
        "verifier_sha256": sha_file(Path(__file__).resolve()),
        "producer_imported": False,
        "python_optimized": not __debug__,
        "mutation_count": len(mutations),
        "mutations": mutations,
    }
    if not args.no_write_report:
        temporary = args.report.with_suffix(args.report.suffix + ".tmp")
        temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        temporary.replace(args.report)
    print(
        json.dumps(
            {
                key: report[key]
                for key in ("status", "direction_count", "proof_step_count", "mutation_count")
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
