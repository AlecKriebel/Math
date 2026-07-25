#!/usr/bin/env python3
"""Shared exact machinery for the shell-two structured action closure.

This module deliberately calls the frozen v1 family auditors rather than
copying their mathematics.  It adds the missing action closure, strict input
and manifest pinning, survivor replay at the following lambda digit, and
resumable per-image records.
"""

from __future__ import annotations

from collections import Counter
import ast
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import sys
import time
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
SHELL_TWO = SEARCH / "shell_two_exact"
STRUCTURED = SEARCH / "structured_phase_families"
SECOND = SEARCH / "phase_second_digit"
sys.path[:0] = [
    str(STRUCTURED),
    str(SHELL_TWO),
    str(SECOND),
    str(SEARCH),
]

import verify_shell_two_exact_orbits as shell  # noqa: E402
import verify_structured_phase_families as structured  # noqa: E402
import verify_f27_submodule_families as f27  # noqa: E402
from verify_lp333_order3_phase_hensel import masks_from_trits  # noqa: E402
from verify_lp333_order3_trit_lift import trits_from_masks  # noqa: E402


MODULUS = 3
RESULT_SCHEMA = "h668-shell-two-structured-action-image-v2"
CERTIFICATE_SCHEMA = "h668-shell-two-structured-action-closure-v2"
EXPECTED_IMAGE_COUNT = 84
FAMILY_NAMES = (
    "opposite_planar_c3_envelope",
    "opposite_twisted_c6",
    "opposite_helical_c4",
)
F27_FAMILY_NAME = "f27_minimal_submodules"
ALL_FAMILY_NAMES = FAMILY_NAMES + (F27_FAMILY_NAME,)

SOURCE_SEEDS = (
    SHELL_TWO / "verify_shell_two_exact_orbits.py",
    STRUCTURED / "verify_structured_phase_families.py",
    STRUCTURED / "verify_f27_submodule_families.py",
)
LOCAL_CERTIFICATE_SOURCES = (
    HERE / "action_closure_common.py",
    HERE / "run_action_closure.py",
    HERE / "verify_action_closure.py",
)
MODULE_SEARCH_PATHS = (STRUCTURED, SHELL_TWO, SECOND, SEARCH)


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        separators=(",", ":"),
        sort_keys=True,
        ensure_ascii=True,
    )


def compact_hash(value: object) -> str:
    return sha256(canonical_json(value).encode("ascii")).hexdigest()


def json_normalize(value: object) -> object:
    return json.loads(canonical_json(value))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def atomic_json_write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def resolve_local_module(module: str) -> Path | None:
    if not module.startswith("verify_"):
        return None
    relative = Path(*module.split(".")).with_suffix(".py")
    for directory in MODULE_SEARCH_PATHS:
        candidate = directory / relative
        if candidate.is_file():
            return candidate.resolve()
    return None


def dependency_source_paths() -> tuple[Path, ...]:
    """Return the transitive local Python source closure.

    The closure starts at the three frozen v1 auditors and follows every
    local ``verify_*`` import through the same search order used at runtime.
    The new runner, verifier, and this shared module are pinned explicitly.
    """

    pending = [path.resolve() for path in SOURCE_SEEDS]
    discovered: set[Path] = set()
    while pending:
        path = pending.pop()
        if path in discovered:
            continue
        if not path.is_file():
            raise FileNotFoundError(path)
        discovered.add(path)
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module)
            elif isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
        for name in names:
            dependency = resolve_local_module(name)
            if dependency is not None and dependency not in discovered:
                pending.append(dependency)
    for path in LOCAL_CERTIFICATE_SOURCES:
        resolved = path.resolve()
        if not resolved.is_file():
            raise FileNotFoundError(resolved)
        discovered.add(resolved)
    return tuple(sorted(discovered, key=lambda path: str(path.relative_to(SEARCH))))


def input_hashes() -> dict[str, str]:
    return {
        str(path.relative_to(SEARCH)): file_sha256(path)
        for path in dependency_source_paths()
    }


def action_element(group: int) -> dict[str, object]:
    if not 0 <= group < 24:
        raise ValueError("action element must lie in range(24)")
    return {
        "group": group,
        "rotation": group // 4,
        "star_a": bool((group // 2) % 2),
        "star_b": bool(group % 2),
    }


def image_partition_and_target(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    values = shell.values_from_ids(identifiers_a, identifiers_b)
    physical = shell.all_correlations(values)
    if physical[0] != (167, 0) or any(
        value != (0, 0) for value in physical[1:]
    ):
        raise AssertionError("an action image failed exact profile replay")
    target: list[int] = []
    for channel in range(2):
        total = (0, 0)
        for value in values[channel][1:]:
            total = shell.add(total, value)
        target.extend(total)
    skeleton = (
        shell.signed_skeleton(identifiers_a),
        shell.signed_skeleton(identifiers_b),
    )
    local_states = tuple(
        (
            skeleton[0][pair],
            skeleton[0][pair + 6],
            skeleton[1][pair],
            skeleton[1][pair + 6],
        )
        for pair in range(shell.PAIRS)
    )
    partition = tuple(
        sorted(
            (
                sum(value != 0 for value in state)
                for state in local_states
            ),
            reverse=True,
        )
    )
    return partition, tuple(target)


def build_action_manifest() -> dict[str, object]:
    """Derive and freeze all distinct labelled images of the five orbits."""

    images: list[dict[str, object]] = []
    seen_global: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    source_counts: dict[str, int] = {}
    for source_index, candidate in enumerate(shell.CANDIDATES):
        source_label, expected_partition, _, base_a, base_b = candidate
        image_actions: dict[
            tuple[tuple[int, ...], tuple[int, ...]], list[dict[str, object]]
        ] = {}
        for group in range(24):
            action = action_element(group)
            pair = (
                tuple(
                    shell.transform_identifiers(
                        base_a,
                        int(action["rotation"]),
                        bool(action["star_a"]),
                    )
                ),
                tuple(
                    shell.transform_identifiers(
                        base_b,
                        int(action["rotation"]),
                        bool(action["star_b"]),
                    )
                ),
            )
            image_actions.setdefault(pair, []).append(action)
        source_counts[source_label] = len(image_actions)
        for local_index, pair in enumerate(sorted(image_actions)):
            if pair in seen_global:
                raise AssertionError("two shell-two source orbits overlap")
            seen_global.add(pair)
            identifiers_a, identifiers_b = pair
            partition, target = image_partition_and_target(
                identifiers_a, identifiers_b
            )
            if partition != tuple(expected_partition):
                raise AssertionError("action changed the shell partition")
            image_digest = compact_hash(
                {
                    "identifiers_a": identifiers_a,
                    "identifiers_b": identifiers_b,
                }
            )
            images.append(
                {
                    "global_index": len(images),
                    "source_index": source_index,
                    "source_label": source_label,
                    "source_orbit_size": len(image_actions),
                    "local_index": local_index,
                    "image_id": (
                        f"{source_label}-image-{local_index:02d}-"
                        f"{image_digest[:12]}"
                    ),
                    "image_sha256": image_digest,
                    "identifiers_a": identifiers_a,
                    "identifiers_b": identifiers_b,
                    "partition": partition,
                    "target": target,
                    "action_elements": tuple(
                        sorted(
                            image_actions[pair],
                            key=lambda item: int(item["group"]),
                        )
                    ),
                }
            )
    if len(images) != EXPECTED_IMAGE_COUNT:
        raise AssertionError(
            f"expected {EXPECTED_IMAGE_COUNT} images, found {len(images)}"
        )
    if len(seen_global) != EXPECTED_IMAGE_COUNT:
        raise AssertionError("action image deduplication failed")
    expected_sizes = {
        str(candidate[0]): len(shell.full_orbit(candidate[3], candidate[4]))
        for candidate in shell.CANDIDATES
    }
    if source_counts != expected_sizes:
        raise AssertionError("action orbit sizes disagree with v1")
    action_law = tuple(action_element(group) for group in range(24))
    core = {
        "schema": "h668-shell-two-action-manifest-v1",
        "action_law": action_law,
        "action_law_sha256": compact_hash(action_law),
        "source_orbit_counts": source_counts,
        "image_count": len(images),
        "images": tuple(images),
    }
    return {
        **core,
        "semantic_sha256": compact_hash(core),
    }


def family_objects() -> tuple[object, ...]:
    by_name = {family.name: family for family in structured.FAMILIES}
    if any(name not in by_name for name in FAMILY_NAMES):
        raise AssertionError("a frozen structured family disappeared")
    return tuple(by_name[name] for name in FAMILY_NAMES)


def image_candidate(image: dict[str, object]) -> tuple[object, ...]:
    return (
        image["image_id"],
        tuple(image["partition"]),
        tuple(image["target"]),
        tuple(image["identifiers_a"]),
        tuple(image["identifiers_b"]),
    )


def direct_survivor_record(
    profiles: Sequence[Sequence[Sequence[int]]],
    trits: Sequence[int],
) -> dict[str, object]:
    trit_tuple = tuple(map(int, trits))
    equations = structured.first_digit_equations(profiles)
    zeros = (0,) * len(equations)
    symbolic_first = structured.symbolic_first_digits(
        equations, trit_tuple
    )
    direct_first = structured.direct_first_digits(profiles, trit_tuple)
    if symbolic_first != zeros or direct_first != zeros:
        raise AssertionError("digit-two survivor failed digit-one replay")
    term_data = structured.second_digit_term_data(profiles)
    symbolic_second = structured.symbolic_second_digits(
        term_data, trit_tuple
    )
    direct_second = structured.direct_second_digits(profiles, trit_tuple)
    if symbolic_second != zeros or direct_second != zeros:
        raise AssertionError("digit-two survivor failed digit-two replay")
    exact_values = structured.displayed_values(profiles, trit_tuple)
    digit_records = tuple(
        structured.lambda_digits(value, 6) for value in exact_values
    )
    digit_three = tuple(int(digits[3]) for digits in digit_records)
    digit_four = tuple(int(digits[4]) for digits in digit_records)
    digit_five = tuple(int(digits[5]) for digits in digit_records)
    exact_phase = all(value == (0, 0) for value in exact_values)
    defect = sum(value != 0 for value in digit_three)
    masks = masks_from_trits(profiles, trit_tuple)
    rotation_images = []
    for rotation in range(6):
        rotated_profiles = tuple(
            tuple(
                channel[(class_index + 2 * rotation) % 12]
                for class_index in range(12)
            )
            for channel in profiles
        )
        rotated_masks = tuple(
            tuple(
                channel[(class_index + 2 * rotation) % 12]
                for class_index in range(12)
            )
            for channel in masks
        )
        rotated_trits = trits_from_masks(
            rotated_profiles, rotated_masks[0], rotated_masks[1]
        )
        if structured.direct_first_digits(
            rotated_profiles, rotated_trits
        ) != zeros:
            raise AssertionError("C6 rotation failed digit-one covariance")
        if structured.direct_second_digits(
            rotated_profiles, rotated_trits
        ) != zeros:
            raise AssertionError("C6 rotation failed digit-two covariance")
        rotated_values = structured.displayed_values(
            rotated_profiles, rotated_trits
        )
        rotated_defect = sum(
            structured.lambda_digits(value, 4)[3] != 0
            for value in rotated_values
        )
        if rotated_defect != defect:
            raise AssertionError("C6 rotation changed digit-three defect")
        rotation_images.append(rotated_masks)
    canonical_rotation_image = min(rotation_images)
    memberships = tuple(
        identifier
        for identifier, generator in structured.SUPERGROUP_GENERATORS
        if structured.point_satisfies_constraints(
            trit_tuple,
            structured.multiplier_constraints(profiles, generator),
        )
    )
    return {
        "trits": trit_tuple,
        "trit_sha256": compact_hash(trit_tuple),
        "normalized_masks": masks,
        "normalized_masks_sha256": compact_hash(masks),
        "c6_rotation_orbit_sha256": compact_hash(
            canonical_rotation_image
        ),
        "c6_rotation_orbit_size": len(set(rotation_images)),
        "c6_rotation_replays_checked": len(rotation_images),
        "direct_digit_one_residual": direct_first,
        "direct_digit_two_residual": direct_second,
        "lambda_digit_3": digit_three,
        "lambda_digit_3_defect": defect,
        "lambda_digit_4": digit_four,
        "lambda_digit_5": digit_five,
        "exact_phase_equations_zero": exact_phase,
        "minimal_proper_supergroup_memberships": memberships,
        "proper_supergroup_free": not memberships,
        "consecutive_through_digit_3": defect == 0,
        "gate_progress": defect == 0,
    }


class ConsecutiveSurvivor(RuntimeError):
    def __init__(self, payload: dict[str, object]):
        super().__init__("a consecutive digit-three survivor was found")
        self.payload = payload


def replay_structured_survivors(
    image: dict[str, object],
    family_name: str,
    audit: dict[str, object],
) -> tuple[dict[str, object], ...]:
    profiles = structured.profiles_from_ids(
        image["identifiers_a"], image["identifiers_b"]
    )
    source_records = tuple(audit["second_digit_witness_records"])
    if len(source_records) != int(audit["second_digit_survivors"]):
        raise AssertionError("v1 structured survivor records are incomplete")
    records = []
    for survivor_index, source_record in enumerate(source_records):
        record = direct_survivor_record(profiles, source_record["trits"])
        source_normalized = json_normalize(source_record)
        for key in (
            "trit_sha256",
            "lambda_digit_3",
            "lambda_digit_4",
            "lambda_digit_5",
            "exact_phase_equations_zero",
        ):
            if source_normalized[key] != json_normalize(record[key]):
                raise AssertionError(
                    f"frozen v1 witness field {key} failed replay"
                )
        records.append(record)
        if record["consecutive_through_digit_3"]:
            raise ConsecutiveSurvivor(
                {
                    "schema": "h668-consecutive-digit-three-alert-v1",
                    "image": image,
                    "family": family_name,
                    "survivor_index": survivor_index,
                    "survivor": record,
                }
            )
    return tuple(records)


def locate_f27_survivors(
    image: dict[str, object],
    submodules: Sequence[dict[str, object]],
) -> tuple[int, str, tuple[tuple[int, ...], ...]]:
    """Repeat the frozen F27 union construction and retain all d2 hits."""

    profiles = f27.profiles_from_ids(
        image["identifiers_a"], image["identifiers_b"]
    )
    coordinates = f27.active_trit_coordinates(profiles)
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    equations = f27.first_digit_equations(profiles)
    equation_rows = f27.augmented_system(equations)
    channel_bases: dict[tuple[int, int], tuple[tuple[int, ...], ...]] = {}
    for submodule_index, submodule_record in enumerate(submodules):
        submodule = tuple(
            tuple(map(int, row)) for row in submodule_record["basis"]
        )
        for channel in range(2):
            embedded: list[tuple[int, ...]] = []
            for residue in range(3):
                embedded.extend(
                    f27.slice_intersection_basis(
                        profiles,
                        coordinate_index,
                        channel,
                        residue,
                        submodule,
                    )
                )
            channel_bases[(submodule_index, channel)] = (
                f27.independent_span(embedded)
            )

    placements: set[tuple[int, ...]] = set()
    for submodule_a in range(len(submodules)):
        for submodule_b in range(len(submodules)):
            basis = f27.independent_span(
                channel_bases[(submodule_a, 0)]
                + channel_bases[(submodule_b, 1)]
            )
            restricted = f27.compose_first_digit(equation_rows, basis)
            affine = f27.affine_trit_space(restricted, basis)
            if affine is not None:
                origin, kernel = affine
                placements.update(f27.affine_points(origin, kernel))
    term_data = f27.second_digit_term_data(profiles)
    survivors = tuple(
        trits
        for trits in sorted(placements)
        if f27.symbolic_second_digits(term_data, trits)
        == (0,) * len(equations)
    )
    return (
        len(placements),
        compact_hash(tuple(sorted(placements))),
        survivors,
    )


def enrich_f27_audit(
    image: dict[str, object],
    audit: dict[str, object],
    submodules: Sequence[dict[str, object]],
) -> dict[str, object]:
    reported = int(audit["second_digit_survivors"])
    records: tuple[dict[str, object], ...] = ()
    if reported:
        placement_count, placement_hash, survivors = locate_f27_survivors(
            image, submodules
        )
        if placement_count != int(audit["distinct_first_digit_placements"]):
            raise AssertionError("F27 placement recount changed")
        if placement_hash != audit["first_digit_placements_sha256"]:
            raise AssertionError("F27 placement digest changed")
        if len(survivors) != reported:
            raise AssertionError("F27 survivor recount changed")
        profiles = f27.profiles_from_ids(
            image["identifiers_a"], image["identifiers_b"]
        )
        mutable_records = []
        for survivor_index, trits in enumerate(survivors):
            record = direct_survivor_record(profiles, trits)
            mutable_records.append(record)
            if record["consecutive_through_digit_3"]:
                raise ConsecutiveSurvivor(
                    {
                        "schema": "h668-consecutive-digit-three-alert-v1",
                        "image": image,
                        "family": F27_FAMILY_NAME,
                        "survivor_index": survivor_index,
                        "survivor": record,
                    }
                )
        records = tuple(mutable_records)
    enriched = dict(audit)
    enriched["second_digit_witness_records"] = records
    enriched["following_digit_direct_replay_checked"] = True
    return enriched


def semantic_payload(result: dict[str, object]) -> dict[str, object]:
    return {
        key: value
        for key, value in result.items()
        if key not in ("runtime", "semantic_sha256")
    }


def compute_image(
    image: dict[str, object],
    inputs: dict[str, str],
    manifest_sha256: str,
    submodules: Sequence[dict[str, object]],
) -> dict[str, object]:
    started = time.perf_counter()
    candidate = image_candidate(image)
    structured_audits = []
    for family in family_objects():
        audit = structured.audit_family_on_profile(family, candidate)
        audit["family"] = family.name
        audit["second_digit_witness_records"] = (
            replay_structured_survivors(
                image, family.name, audit
            )
        )
        audit["following_digit_direct_replay_checked"] = True
        structured_audits.append(audit)
    f27_audit = f27.audit_profile(candidate, submodules)
    f27_audit["family"] = F27_FAMILY_NAME
    f27_audit = enrich_f27_audit(image, f27_audit, submodules)
    result: dict[str, object] = {
        "schema": RESULT_SCHEMA,
        "complete": True,
        "inputs": inputs,
        "action_manifest_sha256": manifest_sha256,
        "image": image,
        "structured_audits": tuple(structured_audits),
        "f27_audit": f27_audit,
    }
    result["runtime"] = {
        "elapsed_seconds": time.perf_counter() - started,
        "maximum_resident_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "processes": 1,
    }
    result["semantic_sha256"] = compact_hash(semantic_payload(result))
    return result


def replay_record_list(
    image: dict[str, object],
    records: Iterable[dict[str, object]],
) -> None:
    profiles = structured.profiles_from_ids(
        image["identifiers_a"], image["identifiers_b"]
    )
    for stored in records:
        regenerated = direct_survivor_record(profiles, stored["trits"])
        if json_normalize(stored) != json_normalize(regenerated):
            raise AssertionError("stored survivor record failed exact replay")
        if regenerated["consecutive_through_digit_3"]:
            raise AssertionError("certificate contains a consecutive survivor")


def validate_semantic_result(
    record: dict[str, object],
    image: dict[str, object],
    inputs: dict[str, str],
    manifest_sha256: str,
) -> None:
    if record["schema"] != RESULT_SCHEMA or not record["complete"]:
        raise AssertionError("image record is not complete")
    if record["inputs"] != inputs:
        raise AssertionError("image record input hashes changed")
    if record["action_manifest_sha256"] != manifest_sha256:
        raise AssertionError("image record action manifest changed")
    if json_normalize(record["image"]) != json_normalize(image):
        raise AssertionError("image record identity changed")
    audits = tuple(record["structured_audits"])
    if tuple(audit["profile"] for audit in audits) != (
        image["image_id"],
    ) * len(FAMILY_NAMES):
        raise AssertionError("structured audit image label changed")
    if len(audits) != len(FAMILY_NAMES):
        raise AssertionError("structured family count changed")
    for expected_name, audit in zip(FAMILY_NAMES, audits):
        if audit["family"] != expected_name:
            raise AssertionError("structured family order changed")
        expected_family = next(
            family for family in family_objects()
            if family.name == expected_name
        )
        if int(audit["parameters"]) != int(
            expected_family.parameter_dimension
        ):
            raise AssertionError("structured family order changed")
        records = tuple(audit["second_digit_witness_records"])
        if len(records) != int(audit["second_digit_survivors"]):
            raise AssertionError("structured survivor count changed")
        if not audit["following_digit_direct_replay_checked"]:
            raise AssertionError("structured survivor replay flag missing")
        replay_record_list(image, records)
        histogram_total = sum(
            int(value)
            for value in audit["second_digit_zero_row_histogram"].values()
        )
        if histogram_total != int(audit["first_digit_distinct_placements"]):
            raise AssertionError("structured histogram coverage changed")
    f27_audit = record["f27_audit"]
    if f27_audit["profile"] != image["image_id"]:
        raise AssertionError("F27 audit image label changed")
    if f27_audit["family"] != F27_FAMILY_NAME:
        raise AssertionError("F27 family label changed")
    f27_records = tuple(f27_audit["second_digit_witness_records"])
    if len(f27_records) != int(f27_audit["second_digit_survivors"]):
        raise AssertionError("F27 survivor count changed")
    if not f27_audit["following_digit_direct_replay_checked"]:
        raise AssertionError("F27 survivor replay flag missing")
    replay_record_list(image, f27_records)
    f27_histogram_total = sum(
        int(value)
        for value in f27_audit["second_digit_zero_row_histogram"].values()
    )
    if f27_histogram_total != int(
        f27_audit["distinct_first_digit_placements"]
    ):
        raise AssertionError("F27 histogram coverage changed")


def validate_result(
    path: Path,
    image: dict[str, object],
    inputs: dict[str, str],
    manifest_sha256: str,
) -> dict[str, object]:
    stored = json.loads(path.read_text(encoding="utf-8"))
    if compact_hash(semantic_payload(stored)) != stored["semantic_sha256"]:
        raise AssertionError(f"{path}: semantic digest failed")
    validate_semantic_result(
        semantic_payload(stored), image, inputs, manifest_sha256
    )
    return stored


def aggregate_summaries(
    records: Sequence[dict[str, object]],
) -> dict[str, object]:
    family_summaries: dict[str, dict[str, object]] = {}
    defect_histogram: Counter[int] = Counter()
    all_occurrences: list[dict[str, object]] = []
    for family_index, family_name in enumerate(FAMILY_NAMES):
        audits = [
            record["structured_audits"][family_index] for record in records
        ]
        family_occurrences = []
        for record, audit in zip(records, audits):
            for item in audit["second_digit_witness_records"]:
                occurrence = {
                    "image_id": record["image"]["image_id"],
                    "source_label": record["image"]["source_label"],
                    "family": family_name,
                    "trit_sha256": item["trit_sha256"],
                    "c6_rotation_orbit_sha256": (
                        item["c6_rotation_orbit_sha256"]
                    ),
                    "lambda_digit_3_defect": (
                        item["lambda_digit_3_defect"]
                    ),
                    "minimal_proper_supergroup_memberships": (
                        item["minimal_proper_supergroup_memberships"]
                    ),
                    "proper_supergroup_free": item["proper_supergroup_free"],
                }
                family_occurrences.append(occurrence)
                all_occurrences.append(occurrence)
                defect_histogram[int(item["lambda_digit_3_defect"])] += 1
        family_unique = {
            occurrence["c6_rotation_orbit_sha256"]
            for occurrence in family_occurrences
        }
        family_summaries[family_name] = {
            "images": len(audits),
            "total_family_placements": sum(
                int(audit["distinct_family_placements"])
                for audit in audits
            ),
            "total_first_digit_placements": sum(
                int(audit["first_digit_distinct_placements"])
                for audit in audits
            ),
            "total_second_digit_survivors": sum(
                int(audit["second_digit_survivors"]) for audit in audits
            ),
            "unique_c6_rotation_classes_of_second_digit_survivors": len(
                family_unique
            ),
            "proper_supergroup_free_second_digit_survivors": sum(
                bool(occurrence["proper_supergroup_free"])
                for occurrence in family_occurrences
            ),
            "total_exact_phase_survivors": sum(
                int(audit["exact_phase_survivors"]) for audit in audits
            ),
            "maximum_second_digit_zero_rows": max(
                (
                    int(audit["maximum_second_digit_zero_rows"])
                    for audit in audits
                    if audit["maximum_second_digit_zero_rows"] is not None
                ),
                default=None,
            ),
        }
    f27_audits = [record["f27_audit"] for record in records]
    f27_occurrences = []
    for record, audit in zip(records, f27_audits):
        for item in audit["second_digit_witness_records"]:
            occurrence = {
                "image_id": record["image"]["image_id"],
                "source_label": record["image"]["source_label"],
                "family": F27_FAMILY_NAME,
                "trit_sha256": item["trit_sha256"],
                "c6_rotation_orbit_sha256": (
                    item["c6_rotation_orbit_sha256"]
                ),
                "lambda_digit_3_defect": item["lambda_digit_3_defect"],
                "minimal_proper_supergroup_memberships": (
                    item["minimal_proper_supergroup_memberships"]
                ),
                "proper_supergroup_free": item["proper_supergroup_free"],
            }
            f27_occurrences.append(occurrence)
            all_occurrences.append(occurrence)
            defect_histogram[int(item["lambda_digit_3_defect"])] += 1
    f27_unique = {
        occurrence["c6_rotation_orbit_sha256"]
        for occurrence in f27_occurrences
    }
    family_summaries[F27_FAMILY_NAME] = {
        "images": len(f27_audits),
        "submodule_pairs_tested_per_image": (
            int(f27_audits[0]["submodule_pairs_tested"])
            if f27_audits
            else 0
        ),
        "total_first_digit_placements": sum(
            int(audit["distinct_first_digit_placements"])
            for audit in f27_audits
        ),
        "total_second_digit_survivors": sum(
            int(audit["second_digit_survivors"]) for audit in f27_audits
        ),
        "unique_c6_rotation_classes_of_second_digit_survivors": len(
            f27_unique
        ),
        "proper_supergroup_free_second_digit_survivors": sum(
            bool(occurrence["proper_supergroup_free"])
            for occurrence in f27_occurrences
        ),
        "maximum_second_digit_zero_rows": max(
            (
                int(audit["maximum_second_digit_zero_rows"])
                for audit in f27_audits
                if audit["maximum_second_digit_zero_rows"] is not None
            ),
            default=None,
        ),
    }
    total_second = sum(
        int(summary["total_second_digit_survivors"])
        for summary in family_summaries.values()
    )
    if sum(defect_histogram.values()) != total_second:
        raise AssertionError("following-digit defect coverage changed")
    equivalence_classes: dict[str, list[dict[str, object]]] = {}
    for occurrence in all_occurrences:
        equivalence_classes.setdefault(
            str(occurrence["c6_rotation_orbit_sha256"]), []
        ).append(occurrence)
    class_records = []
    for orbit_hash, occurrences in sorted(equivalence_classes.items()):
        defects = {
            int(occurrence["lambda_digit_3_defect"])
            for occurrence in occurrences
        }
        memberships = {
            tuple(occurrence["minimal_proper_supergroup_memberships"])
            for occurrence in occurrences
        }
        if len(defects) != 1:
            raise AssertionError(
                "C6-equivalent witnesses changed digit-three defect"
            )
        if len(memberships) != 1:
            raise AssertionError(
                "C6-equivalent witnesses changed supergroup membership"
            )
        class_records.append(
            {
                "c6_rotation_orbit_sha256": orbit_hash,
                "raw_occurrences": len(occurrences),
                "lambda_digit_3_defect": next(iter(defects)),
                "minimal_proper_supergroup_memberships": next(
                    iter(memberships)
                ),
                "proper_supergroup_free": not next(iter(memberships)),
                "occurrences": tuple(occurrences),
            }
        )
    unique_free = sum(
        bool(record["proper_supergroup_free"]) for record in class_records
    )
    return {
        "families": family_summaries,
        "raw_second_digit_survivor_occurrences": total_second,
        "unique_c6_rotation_classes_of_second_digit_survivors": len(
            class_records
        ),
        "unique_proper_supergroup_free_c6_classes": unique_free,
        "second_digit_equivalence_classes": tuple(class_records),
        "lambda_digit_3_defect_histogram": {
            str(key): defect_histogram[key] for key in sorted(defect_histogram)
        },
        "consecutive_through_digit_3_survivors": defect_histogram[0],
        "gate_progress": {
            "criterion": (
                "a digit-two survivor must also have zero defect at "
                "lambda digit three"
            ),
            "raw_digit_two_occurrences_not_counted_as_progress": total_second,
            "qualifying_consecutive_survivors": defect_histogram[0],
            "passed": bool(defect_histogram[0]),
        },
    }


def build_certificate(
    manifest: dict[str, object],
    inputs: dict[str, str],
    records: Sequence[dict[str, object]],
) -> dict[str, object]:
    images = tuple(manifest["images"])
    if (
        len(records) != len(images)
        or len(images) != EXPECTED_IMAGE_COUNT
    ):
        raise AssertionError("certificate does not cover exactly 84 images")
    normalized_records = tuple(
        json_normalize(semantic_payload(dict(record))) for record in records
    )
    for record, image in zip(normalized_records, images):
        validate_semantic_result(
            record, image, inputs, manifest["semantic_sha256"]
        )
    summaries = aggregate_summaries(normalized_records)
    if summaries["consecutive_through_digit_3_survivors"]:
        raise AssertionError("refusing to certify a consecutive survivor")
    core: dict[str, object] = {
        "schema": CERTIFICATE_SCHEMA,
        "scope": (
            "Exact action closure over all 84 distinct labelled images of "
            "the five shell-two profile orbits for three opposite structured "
            "phase families and all asymmetric pairs of minimal F27 "
            "submodules, through placement digit two with direct replay of "
            "every survivor at lambda digit three."
        ),
        "inputs": inputs,
        "action_manifest": manifest,
        "action_manifest_sha256": manifest["semantic_sha256"],
        "image_count": len(images),
        "family_names": ALL_FAMILY_NAMES,
        "records": normalized_records,
        "record_semantic_sha256": tuple(
            compact_hash(record) for record in normalized_records
        ),
        "summaries": summaries,
        "status": "EXHAUSTIVE_NO_CONSECUTIVE_SURVIVOR",
    }
    core["semantic_sha256"] = compact_hash(core)
    return core


def current_rss_bytes() -> int:
    # ru_maxrss is bytes on macOS and KiB on Linux.
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else value * 1024
