#!/usr/bin/env python3
"""Adversarial re-audit of the hardened H21/fourteen-orbit clean-room gate."""
from __future__ import annotations

import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
CLEAN_ROOM = HERE.parent
PROJECT = CLEAN_ROOM.parent
VERIFIER_PATH = CLEAN_ROOM / "verify_h21_transport_and_fourteen_orbits.py"
REGRESSION_PATH = CLEAN_ROOM / "test_h21_transport_regression.py"
HISTORICAL_REPLAY = CLEAN_ROOM / "replay_historical_failure.py"
OLD_OPTIMIZED_PROBE = HERE / "optimized_bypass_probe.py"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def expect_certification_rejection(verifier, name, function, results):
    try:
        function()
    except verifier.CertificationError as error:
        results.append({
            "name": name,
            "status": "REJECTED",
            "exception": str(error)[:300],
        })
        return
    raise AssertionError(("mutation unexpectedly accepted", name))


def composite_sunlet_dependencies(assignment):
    """Independent occurrence support in the 12 composite A/B/U/V variables."""
    x_value, y_value, z_value = assignment
    if x_value == y_value == z_value == 0:
        monomials = (frozenset(),)
    elif x_value == 0:
        monomials = (
            frozenset((("A", y_value),)),
            frozenset((("V", y_value), ("B", y_value))),
        )
    elif y_value == 0:
        monomials = (
            frozenset((("U", x_value), ("V", x_value), ("A", x_value))),
            frozenset((("U", x_value), ("B", x_value))),
        )
    elif z_value == 0:
        monomials = (
            frozenset((("U", x_value), ("V", x_value))),
        )
    else:
        monomials = (
            frozenset((("U", x_value), ("V", x_value), ("A", z_value))),
            frozenset((("U", x_value), ("V", y_value), ("B", z_value))),
        )
    return set().union(*monomials)


def independent_sunlet_generator_set(verifier, certificate, upper_bound):
    omitted_port = certificate["omitted_port"]
    marginal_rows = [
        index for index, assignment in enumerate(verifier.CH4)
        if assignment[omitted_port] == 0
    ]
    for index, row in enumerate(marginal_rows):
        reduced = tuple(
            value for position, value in enumerate(verifier.CH4[row])
            if position != omitted_port
        )
        if reduced != verifier.CH3[index]:
            raise AssertionError(("CH4-to-CH3 marginal order", omitted_port,
                                  index, reduced, verifier.CH3[index]))
    port_permutation = tuple(upper_bound["canonical_port_permutation"])
    used = set()
    for row in certificate["selected_output_rows"]:
        index = marginal_rows.index(row)
        assignment = verifier.CH3[index]
        permuted = tuple(
            assignment[port_permutation[position]] for position in range(3)
        )
        used |= composite_sunlet_dependencies(permuted)
    return used


def subprocess_rejection(command, expected_text):
    completed = subprocess.run(
        command,
        cwd=PROJECT,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
    )
    combined = completed.stdout + completed.stderr
    if completed.returncode == 0:
        raise AssertionError(("subprocess unexpectedly passed", command, combined))
    if expected_text not in combined:
        raise AssertionError(("missing rejection text", command, combined))
    if "CLEANROOM_K3P_H21_TRANSPORT_AND_FOURTEEN_ORBITS_PASS" in combined:
        raise AssertionError(("rejected subprocess emitted full sentinel", command))
    return {
        "command": command,
        "returncode": completed.returncode,
        "expected_rejection_seen": True,
    }


def run():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError("the hardened re-audit itself refuses optimized Python")

    verifier = load_module("hardened_cleanroom_verifier_reaudit", VERIFIER_PATH)
    mutation_results = []
    control_results = []

    # Full baseline with a call counter proving that every raw-member Fourier
    # transport (38) plus every representative repeat (14) is reached.
    transport_calls = []
    original_transport = verifier.verify_fourier_transport

    def counted_transport(base_graph, relabelled_graph, perm):
        transport_calls.append(tuple(perm))
        return original_transport(base_graph, relabelled_graph, perm)

    verifier.verify_fourier_transport = counted_transport
    baseline_stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(baseline_stdout):
            diagnostics = verifier.verify_all(run_certificates=True)
    finally:
        verifier.verify_fourier_transport = original_transport
    baseline_text = baseline_stdout.getvalue()
    full_sentinel = "CLEANROOM_K3P_H21_TRANSPORT_AND_FOURTEEN_ORBITS_PASS"
    if full_sentinel not in baseline_text:
        raise AssertionError("full baseline omitted terminal sentinel")
    if "PASS five independently reconstructed directed-rank upper bounds" not in baseline_text:
        raise AssertionError("full baseline omitted rank-upper-bound sentinel")
    expected_transport_calls = 38 + 14
    if len(transport_calls) != expected_transport_calls:
        raise AssertionError(("raw Fourier transport call census",
                              len(transport_calls), expected_transport_calls))
    if len(diagnostics.get("rank_upper_bounds", ())) != 5:
        raise AssertionError("full baseline returned incomplete rank evidence")

    # The former skip control must now fail before emitting any full sentinel.
    skipped_stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(skipped_stdout):
            verifier.verify_all(run_certificates=False)
    except verifier.CertificationError as error:
        if "cannot skip algebraic certificates" not in str(error):
            raise
    else:
        raise AssertionError("run_certificates=False unexpectedly passed")
    if full_sentinel in skipped_stdout.getvalue():
        raise AssertionError("certificate-skip control emitted full sentinel")
    control_results.append({
        "name": "run_certificates_false",
        "status": "REJECTED_WITHOUT_FULL_SENTINEL",
    })

    # Optimized Python and the old optimized bypass must both fail at import.
    optimized_results = []
    optimized_results.append(subprocess_rejection(
        [sys.executable, "-O", str(VERIFIER_PATH)],
        "certification verifier refuses optimized Python",
    ))
    optimized_results.append(subprocess_rejection(
        [sys.executable, "-O", str(OLD_OPTIMIZED_PROBE)],
        "certification verifier refuses optimized Python",
    ))
    optimize_environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
                            "PYTHONOPTIMIZE": "1"}
    environment_run = subprocess.run(
        [sys.executable, str(VERIFIER_PATH)], cwd=PROJECT,
        env=optimize_environment, text=True, capture_output=True,
    )
    environment_text = environment_run.stdout + environment_run.stderr
    if (environment_run.returncode == 0 or
            "certification verifier refuses optimized Python" not in environment_text or
            full_sentinel in environment_text):
        raise AssertionError(("PYTHONOPTIMIZE control", environment_run.returncode,
                              environment_text))
    optimized_results.append({
        "command": ["PYTHONOPTIMIZE=1", sys.executable, str(VERIFIER_PATH)],
        "returncode": environment_run.returncode,
        "expected_rejection_seen": True,
    })

    # Every active JSON input must be registered, byte-bound, and reject a
    # one-byte alteration before JSON parsing.
    expected_active_inputs = {
        "K3P_14_ORBIT_LOCK.json",
        "k3p_prelock_source5_quartic.json",
        "k3p_h14_marginal_orbit_certificates.json",
        "k3p_remaining_quartic_separators.json",
        "k3p_directed_rank_obstructions.json",
    }
    if set(verifier.EXPECTED_INPUT_SHA256) != expected_active_inputs:
        raise AssertionError(("active input registry", verifier.EXPECTED_INPUT_SHA256))
    active_hash_results = []
    original_read_bytes = Path.read_bytes
    for filename in sorted(expected_active_inputs):
        path = (verifier.ARTIFACTS / filename).resolve()
        observed = digest(path)
        expected = verifier.EXPECTED_INPUT_SHA256[filename]
        if observed != expected:
            raise AssertionError(("baseline active hash mismatch", filename,
                                  observed, expected))

        def altered_read_bytes(self, _target=path):
            payload = original_read_bytes(self)
            if self.resolve() == _target:
                return payload + b"\n"
            return payload

        with mock.patch.object(Path, "read_bytes", altered_read_bytes):
            expect_certification_rejection(
                verifier,
                f"active_hash_one_byte_mutation:{filename}",
                lambda _filename=filename: verifier.load_bound_json(_filename),
                mutation_results,
            )
        active_hash_results.append({
            "filename": filename,
            "sha256": observed,
            "one_byte_mutation": "REJECTED_BEFORE_PARSE",
        })

    # Reconstruct canonical records once for direct certificate mutation tests.
    reconstructions = {
        orbit_id: verifier.reconstruct_record(record)
        for orbit_id, record in verifier.RECORDS.items()
    }
    h21_record = verifier.RECORDS["H21-01"]

    def reject_record_mutation(name, mutate):
        record = copy.deepcopy(h21_record)
        mutate(record)
        expect_certification_rejection(
            verifier, name, lambda: verifier.reconstruct_record(record),
            mutation_results,
        )

    reject_record_mutation(
        "port_permutation_mismatch",
        lambda record: record.__setitem__("port_permutation", [0, 1, 2, 3]),
    )
    reject_record_mutation(
        "source_incoming_role_mismatch",
        lambda record: record.__setitem__("source_incoming_role", "selected-port-3"),
    )
    reject_record_mutation(
        "target_incoming_role_mismatch",
        lambda record: record.__setitem__("target_incoming_role", "selected-port-3"),
    )
    reject_record_mutation(
        "source_repair_tag_mismatch",
        lambda record: record.__setitem__("source_repair", 0),
    )
    reject_record_mutation(
        "target_repair_tag_mismatch",
        lambda record: record.__setitem__("target_repair", 0),
    )
    reject_record_mutation(
        "raw_member_omission",
        lambda record: (
            record.__setitem__("raw_members", record["raw_members"][:-1]),
            record.__setitem__("raw_member_transports",
                               record["raw_member_transports"][:-1]),
        ),
    )
    reject_record_mutation(
        "raw_member_duplicate_insertion",
        lambda record: record["raw_members"].append(record["raw_members"][0]),
    )
    reject_record_mutation(
        "raw_witness_omission",
        lambda record: record.__setitem__(
            "raw_member_transports", record["raw_member_transports"][:-1]
        ),
    )
    reject_record_mutation(
        "raw_witness_base_displayed_frame_confusion",
        lambda record: record["raw_member_transports"][2].__setitem__(
            "target_automorphism", [3, 1, 2, 0]
        ),
    )

    # A bad coordinate action must still be rejected by exact physical-edge
    # symbolic transport, independently of raw membership accounting.
    original_coordinate_transport = verifier.coordinate_transport
    verifier.coordinate_transport = lambda perm: tuple(range(64))
    try:
        reconstruction = reconstructions["H21-01"]
        expect_certification_rejection(
            verifier,
            "identity_coordinate_transport_for_nonidentity_relabelling",
            lambda: verifier.verify_fourier_transport(
                reconstruction["target_base"],
                reconstruction["target_displayed"],
                tuple(h21_record["representative_permutation"]),
            ),
            mutation_results,
        )
    finally:
        verifier.coordinate_transport = original_coordinate_transport

    rank_certificates = verifier.load_bound_json(
        "k3p_directed_rank_obstructions.json"
    )["records"]
    rank_evidence = [
        verifier.verify_rank_obstruction_certificate(certificate, reconstructions)
        for certificate in rank_certificates
    ]
    expected_rank_inequalities = {
        "H21-02": (11, 10),
        "L20-02": (14, 12),
        "L21a-02": (11, 10),
        "L21b-02": (11, 10),
        "L23-01": (14, 12),
    }
    for evidence in rank_evidence:
        expected = expected_rank_inequalities[evidence["orbit_id"]]
        actual = (evidence["source_minor"]["rank"],
                  evidence["target_upper_bound"]["generator_count"])
        if actual != expected or evidence["target_minor"]["rank"] != expected[1]:
            raise AssertionError(("rank inequality", evidence["orbit_id"],
                                  actual, expected))

    def reject_rank_mutation(name, orbit_id, mutate):
        certificate = copy.deepcopy(next(
            entry for entry in rank_certificates if entry["orbit_id"] == orbit_id
        ))
        mutate(certificate)
        expect_certification_rejection(
            verifier, name,
            lambda: verifier.verify_rank_obstruction_certificate(
                certificate, reconstructions
            ),
            mutation_results,
        )

    reject_rank_mutation(
        "rank_labels_101_over_100",
        "H21-02",
        lambda certificate: (
            certificate["source_rank_certificate"].__setitem__("rank", 101),
            certificate.__setitem__("target_dimension_upper_bound", 100),
            certificate["target_rank_certificate"].__setitem__("rank", 100),
        ),
    )
    reject_rank_mutation(
        "source_minor_column_count_mismatch",
        "H21-02",
        lambda certificate: certificate["source_rank_certificate"].__setitem__(
            "parameter_columns",
            certificate["source_rank_certificate"]["parameter_columns"][:-1],
        ),
    )
    reject_rank_mutation(
        "target_minor_row_count_mismatch",
        "H21-02",
        lambda certificate: certificate["target_rank_certificate"].__setitem__(
            "output_rows",
            certificate["target_rank_certificate"]["output_rows"][:-1],
        ),
    )
    reject_rank_mutation(
        "target_upper_bound_integer_mismatch",
        "H21-02",
        lambda certificate: certificate.__setitem__(
            "target_dimension_upper_bound", 11
        ),
    )
    reject_rank_mutation(
        "H21_generator_name_mutation",
        "H21-02",
        lambda certificate: certificate["rational_generators"].__setitem__(0, "BAD"),
    )
    reject_rank_mutation(
        "H21_saturation_factor_mutation",
        "H21-02",
        lambda certificate: certificate["saturation_factors"].__setitem__(0, "BAD"),
    )
    reject_rank_mutation(
        "rank_source_map_hash_direction_mutation",
        "H21-02",
        lambda certificate: certificate.__setitem__(
            "source_map_hash", certificate["target_map_hash"]
        ),
    )
    reject_rank_mutation(
        "sunlet_absent_generator_mutation",
        "L21a-02",
        lambda certificate: certificate["absent_generators"].__setitem__(0, "BAD"),
    )
    reject_rank_mutation(
        "sunlet_omitted_port_out_of_range",
        "L20-02",
        lambda certificate: certificate.__setitem__("omitted_port", 4),
    )
    reject_rank_mutation(
        "unknown_upper_bound_mechanism",
        "H21-02",
        lambda certificate: certificate.__setitem__("obstruction_type", "UNKNOWN"),
    )

    # Circularity audit: remove/poison every rank conclusion passed to the
    # target-factorization routines.  Their independently reconstructed counts
    # must remain 10/12 and must match independently derived dependency support.
    circularity_results = []
    for certificate in rank_certificates:
        orbit_id = certificate["orbit_id"]
        poisoned = copy.deepcopy(certificate)
        poisoned["source_rank_certificate"] = {"rank": 999}
        poisoned["target_rank_certificate"] = {"rank": 998}
        poisoned["target_dimension_upper_bound"] = 997
        descriptor = reconstructions[orbit_id]["target_descriptor"]
        if orbit_id == "H21-02":
            upper = verifier.verify_h21_target_upper_bound(descriptor, poisoned)
            if upper["generator_count"] != 10 or upper["identity_count"] != 11:
                raise AssertionError(("H21 poisoned conclusion dependency", upper))
            point = verifier.exact_point(verifier.RECORDS[orbit_id], "target")
            edges, _ = point
            saturation_values = (
                edges[2][0], edges[2][1],
                edges[3][2] * edges[6][2], edges[6][2],
            )
            if min(saturation_values) <= 0:
                raise AssertionError(("H21 saturation point", saturation_values))
            circularity_results.append({
                "orbit_id": orbit_id,
                "rank_fields_poisoned": True,
                "reconstructed_generator_count": 10,
                "exact_identity_count": 11,
                "strict_point_saturation_minimum": str(min(saturation_values)),
            })
        else:
            upper = verifier.verify_sunlet_target_upper_bound(descriptor, poisoned)
            independent_used = independent_sunlet_generator_set(
                verifier, certificate, upper
            )
            if len(independent_used) != upper["generator_count"]:
                raise AssertionError(("sunlet dependency undercount", orbit_id,
                                      independent_used, upper))
            expected_names = {
                f"{prefix}_{verifier.LETTER[character]}"
                for prefix, character in independent_used
            }
            if expected_names != set(upper["generators"]):
                raise AssertionError(("sunlet generator-name mismatch", orbit_id,
                                      expected_names, upper["generators"]))
            circularity_results.append({
                "orbit_id": orbit_id,
                "rank_fields_poisoned": True,
                "reconstructed_generator_count": upper["generator_count"],
                "independent_composite_support_count": len(independent_used),
                "exact_canonical_sunlet_match": True,
            })

    # Auxiliary independent implementation must agree on all five bounds.
    exact_four_port_path = PROJECT / "reproducibility" / "exact_four_port.py"
    exact_four_port = load_module(
        "auxiliary_exact_four_port_reaudit", exact_four_port_path
    )
    auxiliary = exact_four_port.verify_four_port(verifier.ARTIFACTS)
    auxiliary_ranks = {
        entry["orbit_id"]: (
            entry["source"]["rank_lower_bound"],
            entry["target_factorization"]["generator_count"],
        )
        for entry in auxiliary["directed_rank_separators"]
    }
    if auxiliary_ranks != expected_rank_inequalities:
        raise AssertionError(("auxiliary rank disagreement", auxiliary_ranks,
                              expected_rank_inequalities))

    # Historical failure must remain preserved after hardening.
    historical = subprocess.run(
        [sys.executable, str(HISTORICAL_REPLAY)], cwd=PROJECT,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True, capture_output=True,
    )
    historical_text = historical.stdout + historical.stderr
    if (historical.returncode != 0 or
            "HISTORICAL_H21_01_FAILURE_REPRODUCED_EXACTLY" not in historical_text):
        raise AssertionError(("historical failure replay", historical.returncode,
                              historical_text))

    result = {
        "status": "PASS_ZERO_REMAINING_HARDENING_GAPS",
        "hashes": {
            "hardened_verifier": digest(VERIFIER_PATH),
            "regression": digest(REGRESSION_PATH),
            "historical_replay": digest(HISTORICAL_REPLAY),
            "auxiliary_exact_four_port": digest(exact_four_port_path),
        },
        "baseline": {
            "full_terminal_sentinel": True,
            "rank_upper_bound_sentinel": True,
            "raw_plus_representative_Fourier_transport_calls": len(transport_calls),
            "rank_upper_bound_records": len(diagnostics["rank_upper_bounds"]),
        },
        "controls": control_results,
        "optimized_mode_rejections": optimized_results,
        "active_hashes": active_hash_results,
        "mutation_results": mutation_results,
        "rank_inequalities": {
            orbit_id: {"source": source, "target_upper_bound": target}
            for orbit_id, (source, target) in expected_rank_inequalities.items()
        },
        "circularity_audit": circularity_results,
        "auxiliary_rank_agreement": auxiliary_ranks,
        "historical_failure_preserved": True,
    }
    print(json.dumps(result, indent=2, default=list))
    print("HARDENED_CLEANROOM_ADVERSARIAL_REAUDIT_PASS")
    return result


if __name__ == "__main__":
    run()
