#!/usr/bin/env python3
"""Fail-closed mutation suite for the printed certificate appendix."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
SUBMISSION = HERE.parent
APPENDIX = HERE / "PRINTED_CERTIFICATE_APPENDIX.json"
TEX = SUBMISSION / "supplement" / "certificate_appendix.tex"
VERIFIER = HERE / "verify_printed_certificate_appendix.py"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def reseal(value: dict[str, Any]) -> str:
    value.pop("payload_sha256", None)
    digest = hashlib.sha256(canonical_bytes(value)).hexdigest()
    value["payload_sha256"] = digest
    return digest


def run_verifier(appendix: Path, tex: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(VERIFIER),
            "--appendix",
            str(appendix),
            "--tex",
            str(tex),
        ],
        cwd=SUBMISSION.parent,
        text=True,
        capture_output=True,
        check=False,
    )


def mutate_omit_quadratic(value: dict[str, Any]) -> None:
    value["quadratic_templates"].pop(0)
    value["quadratic_template_count"] -= 1


def mutate_quadratic_coefficient(value: dict[str, Any]) -> None:
    value["quadratic_templates"][0]["terms"][0]["coefficient"] = 2


def mutate_quadratic_multidegree(value: dict[str, Any]) -> None:
    row = value["quadratic_templates"][2]
    row["multidegree"][0], row["multidegree"][1] = row["multidegree"][1], row["multidegree"][0]


def mutate_quadratic_count(value: dict[str, Any]) -> None:
    value["quadratic_templates"][2]["raw_presentation_count"] += 1


def mutate_unauthorized_transport(value: dict[str, Any]) -> None:
    row = copy.deepcopy(value["certified_high_degree_transports"]["theta0_quintic"][0])
    row["canonical_class_id"] = 999
    value["certified_high_degree_transports"]["theta0_quintic"].append(row)
    value["certified_high_degree_transports"]["covered_directional_records"] += 1


def mutate_quintic_formula(value: dict[str, Any]) -> None:
    value["high_degree_bases"][0]["terms"][0]["coefficient"] *= -1


def mutate_quartic_formula(value: dict[str, Any]) -> None:
    value["high_degree_bases"][1]["terms"][0]["indices"][0] = 1


def mutate_cubic_formula(value: dict[str, Any]) -> None:
    value["high_degree_bases"][4]["multidegree"][0] += 1


def mutate_quartic_parent(value: dict[str, Any]) -> None:
    value["certified_high_degree_transports"]["lower_theta_quartic"][0]["base_id"] = "HDQ-03"


def mutate_coordinate(value: dict[str, Any]) -> None:
    value["coordinate_dictionaries"]["five_port_displayed"][0]["character_tuple"] = "000TT"


def mutate_omit_restoration_child(value: dict[str, Any]) -> None:
    value["worked_examples"]["restoration_root_s1_c658_t2792_p1032"]["first_children"].pop()


def mutate_restoration_parent(value: dict[str, Any]) -> None:
    value["worked_examples"]["restoration_root_s1_c658_t2792_p1032"]["second_children"][0][
        "parent_first_coverage_index"
    ] += 1


def mutate_restoration_terminal(value: dict[str, Any]) -> None:
    example = value["worked_examples"]["restoration_root_s1_c658_t2792_p1032"]
    example["second_children"][0]["status"] = "unresolved"
    example["termination"]["unresolved"] = 1


def mutate_one_port_transport(value: dict[str, Any]) -> None:
    value["worked_examples"]["probe_tree_k3_identity"]["selected_one_port_transport"][
        "transport_id"
    ] = "0" * 64


def mutate_two_port_parent(value: dict[str, Any]) -> None:
    value["worked_examples"]["probe_tree_k3_identity"]["selected_two_port_transport"][
        "parent_transport_id"
    ] = "1" * 64


def mutate_input_hash(value: dict[str, Any]) -> None:
    value["input_bindings"][0]["sha256"] = "f" * 64


MUTATIONS: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
    ("omitted_quadratic_template", mutate_omit_quadratic),
    ("false_quadratic_coefficient", mutate_quadratic_coefficient),
    ("reassigned_quadratic_multidegree", mutate_quadratic_multidegree),
    ("false_quadratic_count", mutate_quadratic_count),
    ("unauthorized_high_degree_transport", mutate_unauthorized_transport),
    ("reassigned_quintic_formula", mutate_quintic_formula),
    ("reassigned_quartic_formula", mutate_quartic_formula),
    ("reassigned_cubic_formula", mutate_cubic_formula),
    ("wrong_quartic_parent", mutate_quartic_parent),
    ("wrong_coordinate_dictionary", mutate_coordinate),
    ("omitted_restoration_child", mutate_omit_restoration_child),
    ("wrong_restoration_parent", mutate_restoration_parent),
    ("unterminated_restoration_child", mutate_restoration_terminal),
    ("broken_one_port_transport", mutate_one_port_transport),
    ("broken_two_port_parent_transport", mutate_two_port_parent),
    ("wrong_input_file_hash", mutate_input_hash),
)


def main() -> None:
    if not __debug__:
        raise RuntimeError("OPTIMIZED_PYTHON_FORBIDDEN")
    original = json.loads(APPENDIX.read_text(encoding="utf-8"))
    original_tex = TEX.read_text(encoding="utf-8")
    baseline = run_verifier(APPENDIX, TEX)
    if baseline.returncode != 0:
        raise RuntimeError("BASELINE_REPLAY_FAILED\n" + baseline.stderr)

    results = []
    with tempfile.TemporaryDirectory(prefix="k2p-printed-appendix-mutations-") as temporary:
        root = Path(temporary)
        for name, mutation in MUTATIONS:
            value = copy.deepcopy(original)
            mutation(value)
            old_digest = original["payload_sha256"]
            new_digest = reseal(value)
            mutated_tex = original_tex.replace(old_digest, new_digest)
            appendix_path = root / f"{name}.json"
            tex_path = root / f"{name}.tex"
            appendix_path.write_text(
                json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            tex_path.write_text(mutated_tex, encoding="utf-8")
            replay = run_verifier(appendix_path, tex_path)
            detected = replay.returncode != 0
            results.append({"mutation": name, "detected": detected})
            if not detected:
                raise RuntimeError(f"MUTATION_SURVIVED:{name}")

        stale = copy.deepcopy(original)
        stale["quadratic_templates"][0]["canonical_class_count"] += 1
        stale_path = root / "stale_seal.json"
        stale_path.write_text(json.dumps(stale, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        stale_replay = run_verifier(stale_path, TEX)
        stale_detected = stale_replay.returncode != 0
        results.append({"mutation": "stale_payload_seal", "detected": stale_detected})
        if not stale_detected:
            raise RuntimeError("MUTATION_SURVIVED:stale_payload_seal")

        tex_mutation = root / "missing_tex_template.tex"
        tex_mutation.write_text(original_tex.replace("R4Q-03", "R4Q-XX"), encoding="utf-8")
        tex_replay = run_verifier(APPENDIX, tex_mutation)
        tex_detected = tex_replay.returncode != 0
        results.append({"mutation": "missing_printed_template", "detected": tex_detected})
        if not tex_detected:
            raise RuntimeError("MUTATION_SURVIVED:missing_printed_template")

    print(
        json.dumps(
            {
                "status": "PASS",
                "baseline": "PASS",
                "mutation_count": len(results),
                "detected": sum(row["detected"] for row in results),
                "mutations": results,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
