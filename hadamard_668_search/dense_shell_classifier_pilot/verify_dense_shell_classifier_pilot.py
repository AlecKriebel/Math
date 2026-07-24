#!/usr/bin/env python3
"""Independent verifier for the bounded dense-shell classifier pilot.

The verifier compiles the C++ stream into a temporary directory, pins two
small deterministic shard censuses, checks that a split --skip/--limit run
adds back to the unsplit h=1 run, and independently replays every emitted
witness on all 37 physical positions.  Its characteristic-two replay calls
the tracked public API in ``char2_profile_quotient``.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
CPP = HERE / "dense_shell_classifier_pilot.cpp"
CHAR2 = PARENT / "char2_profile_quotient"
sys.path.insert(0, str(CHAR2))

import verify_char2_profile_quotient as char2  # noqa: E402
from production_common import partition_audit, workload_audit  # noqa: E402


P = 37
H = (1, 26, 10)
PROFILE_TRIPLES = (
    (0, 0, 3),
    (0, 1, 2),
    (0, 2, 1),
    (0, 3, 0),
    (1, 0, 2),
    (1, 1, 1),
    (1, 2, 0),
    (2, 0, 1),
    (2, 1, 0),
    (3, 0, 0),
)
WITNESS_NAMES = (
    "witness_target",
    "witness_char2",
    "witness_mod9",
    "witness_char2_mod9",
    "witness_post_mod9_lambda",
    "witness_exact",
)
ADDITIVE_KEYS = (
    "canonical_decorations_processed",
    "weighted_decorations_processed",
    "high_phase_cases",
    "rejected_local_phase_cases",
    "primitive_flag_phase_leaves",
    "weighted_primitive_flag_phase_leaves",
    "affine_aggregate_hits",
    "weighted_affine_aggregate_hits",
    "exact_target_hits",
    "char2_hits",
    "mod9_hits",
    "char2_mod9_hits",
    "post_mod9_lambda_hits",
    "char2_post_mod9_lambda_hits",
    "mod27_hits",
    "exact_zero_hits",
    "weighted_exact_target_hits",
    "weighted_char2_hits",
    "weighted_mod9_hits",
    "weighted_post_mod9_lambda_hits",
    "weighted_exact_zero_hits",
)

EXPECTED = {
    ("h1", 0, 100): {
        "raw_decorations_seen": 183,
        "canonical_decorations_seen": 101,
        "canonical_decorations_processed": 100,
        "weighted_decorations_processed": 2400,
        "high_phase_cases": 300,
        "rejected_local_phase_cases": 258,
        "primitive_flag_phase_leaves": 7_440_174,
        "weighted_primitive_flag_phase_leaves": 178_564_176,
        "affine_aggregate_hits": 3_897_234,
        "weighted_affine_aggregate_hits": 93_533_616,
        "exact_target_hits": 159_116,
        "char2_hits": 82,
        "mod9_hits": 220,
        "char2_mod9_hits": 0,
        "post_mod9_lambda_hits": 1,
        "char2_post_mod9_lambda_hits": 0,
        "mod27_hits": 0,
        "exact_zero_hits": 0,
        "diagnostic_assignment_idlex_mod9_hits": 3,
        "diagnostic_weighted_assignment_idlex_mod9_hits": 72,
        "detached_replays": 222,
        "weighted_exact_target_hits": 3_818_784,
        "weighted_char2_hits": 1_968,
        "weighted_mod9_hits": 5_280,
        "weighted_post_mod9_lambda_hits": 24,
        "weighted_exact_zero_hits": 0,
        "checksum": "0xa4ac52a6e8bfb42f",
    },
    ("h0", 0, 10): {
        "raw_decorations_seen": 15,
        "canonical_decorations_seen": 11,
        "canonical_decorations_processed": 10,
        "weighted_decorations_processed": 180,
        "high_phase_cases": 10,
        "rejected_local_phase_cases": 8,
        "primitive_flag_phase_leaves": 3_188_646,
        "weighted_primitive_flag_phase_leaves": 76_527_504,
        "affine_aggregate_hits": 3_188_646,
        "weighted_affine_aggregate_hits": 76_527_504,
        "exact_target_hits": 105_954,
        "char2_hits": 50,
        "mod9_hits": 141,
        "char2_mod9_hits": 0,
        "post_mod9_lambda_hits": 1,
        "char2_post_mod9_lambda_hits": 0,
        "mod27_hits": 0,
        "exact_zero_hits": 0,
        "diagnostic_assignment_idlex_mod9_hits": 0,
        "diagnostic_weighted_assignment_idlex_mod9_hits": 0,
        "detached_replays": 143,
        "weighted_exact_target_hits": 2_542_896,
        "weighted_char2_hits": 1_200,
        "weighted_mod9_hits": 3_384,
        "weighted_post_mod9_lambda_hits": 24,
        "weighted_exact_zero_hits": 0,
        "checksum": "0x68c82f469906794f",
    },
}

EXPECTED_DECORATIONS = {
    "h1": {
        "raw_skeletons": 59_743_488,
        "raw_decorations": 537_691_392,
        "canonical_decorations": 22_426_752,
        "fixed_decorations": (
            537_691_392, 275_328, 275_328, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ),
    },
    "h0": {
        "raw_skeletons": 47_730_304,
        "raw_decorations": 47_730_304,
        "canonical_decorations": 1_999_128,
        "fixed_decorations": (
            47_730_304, 67_776, 67_776, 0, 32, 0, 0, 0,
            208, 24, 24, 0, 112_640, 0, 0, 0,
            208, 24, 24, 0, 32, 0, 0, 0,
        ),
    },
}


def e_add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def e_conjugate(value: tuple[int, int]) -> tuple[int, int]:
    return value[0] - value[1], -value[1]


def e_multiply(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def e_scale(scale: int, value: tuple[int, int]) -> tuple[int, int]:
    return scale * value[0], scale * value[1]


def raw_profile(identifier: int) -> tuple[int, int]:
    a, b, c = PROFILE_TRIPLES[identifier]
    return a - c, b - c


def classes() -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...]]:
    parts = []
    class_of = [-1] * P
    power = 1
    for _ in range(12):
        part = tuple(power * member % P for member in H)
        parts.append(part)
        for value in part:
            if class_of[value] != -1:
                raise AssertionError("classes overlap")
            class_of[value] = len(parts) - 1
        power = 2 * power % P
    if set().union(*(set(part) for part in parts)) != set(range(1, P)):
        raise AssertionError("classes do not cover F_37^*")
    return tuple(parts), tuple(class_of)


CLASSES, CLASS_OF = classes()


def coefficient(channel: int, class_index: int, identifier: int) -> tuple[int, int]:
    epsilon = 1 if class_index % 2 == 0 else -1
    factor = -epsilon if channel == 0 else epsilon
    return e_scale(factor, raw_profile(identifier))


def assignment_values(
    ids_a: tuple[int, ...], ids_b: tuple[int, ...]
) -> tuple[tuple[tuple[int, int], ...], ...]:
    result = []
    for channel, identifiers in enumerate((ids_a, ids_b)):
        row = [(-1, 0) if channel == 0 else (2, 0)]
        row.extend(
            coefficient(channel, class_index, identifier)
            for class_index, identifier in enumerate(identifiers)
        )
        result.append(tuple(row))
    return tuple(result)


def aggregate(
    values: tuple[tuple[tuple[int, int], ...], ...]
) -> tuple[int, int, int, int]:
    result = []
    for channel in range(2):
        total = (0, 0)
        for value in values[channel][1:]:
            total = e_add(total, value)
        result.extend(total)
    return tuple(result)  # type: ignore[return-value]


def physical_correlations(
    values: tuple[tuple[tuple[int, int], ...], ...]
) -> tuple[tuple[int, int], ...]:
    physical = []
    for channel in range(2):
        word = [values[channel][0]]
        word.extend(values[channel][CLASS_OF[position] + 1] for position in range(1, P))
        physical.append(tuple(word))
    result = []
    for lag in range(P):
        total = (0, 0)
        for channel in range(2):
            for source in range(P):
                total = e_add(
                    total,
                    e_multiply(
                        physical[channel][(source + lag) % P],
                        e_conjugate(physical[channel][source]),
                    ),
                )
        result.append(total)
    return tuple(result)


def mix64(value: int) -> int:
    mask = (1 << 64) - 1
    value &= mask
    value ^= value >> 30
    value = value * 0xBF58476D1CE4E5B9 & mask
    value ^= value >> 27
    value = value * 0x94D049BB133111EB & mask
    return (value ^ (value >> 31)) & mask


def assignment_digest(
    identifiers: tuple[int, ...],
    exact: tuple[tuple[int, int], ...],
    target_index: int,
) -> int:
    mask = (1 << 64) - 1
    digest = 0x66833337
    for slot, identifier in enumerate(identifiers):
        digest ^= mix64(identifier + 17 * (slot + 1))
    for lag, (a, b) in enumerate(exact):
        digest ^= mix64((a & mask) + 257 * (lag + 1))
        digest ^= mix64((b & mask) + 65537 * (lag + 1))
    digest ^= mix64(target_index + 1)
    return digest & mask


def parse_output(
    output: str,
    pass_line: str = "PASS: bounded exact dense-shell stream and detached replay",
) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    if pass_line not in output:
        raise AssertionError("pilot did not report PASS")
    return result


def parse_ints(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split(","))


def parse_exact(value: str) -> tuple[tuple[int, int], ...]:
    result = tuple(
        tuple(map(int, pair.split(",")))
        for pair in value.split(";")
    )
    if len(result) != 6 or any(len(pair) != 2 for pair in result):
        raise AssertionError("malformed compact correlation witness")
    return result  # type: ignore[return-value]


def norm(value: tuple[int, int]) -> int:
    a, b = value
    return a * a - a * b + b * b


def replay_witness(data: dict[str, str], prefix: str, shell: str) -> None:
    present = int(data[f"{prefix}_present"])
    if not present:
        return
    ids_a = parse_ints(data[f"{prefix}_ids_a"])
    ids_b = parse_ints(data[f"{prefix}_ids_b"])
    if len(ids_a) != 12 or len(ids_b) != 12:
        raise AssertionError("witness class word has wrong length")
    target = parse_ints(data[f"{prefix}_target"])
    target_index = int(data[f"{prefix}_target_index"])
    values = assignment_values(ids_a, ids_b)
    if aggregate(values) != target:
        raise AssertionError("independent aggregate replay failed")

    direct = physical_correlations(values)
    compact = parse_exact(data[f"{prefix}_exact"])
    for class_index in range(12):
        lag = CLASSES[class_index][0]
        expected = (
            compact[class_index]
            if class_index < 6
            else e_conjugate(compact[class_index - 6])
        )
        if direct[lag] != expected:
            raise AssertionError("independent 37-point replay failed")

    printed_mod9 = bool(int(data[f"{prefix}_mod9"]))
    printed_lambda = bool(int(data[f"{prefix}_post_mod9_lambda"]))
    printed_mod27 = bool(int(data[f"{prefix}_mod27"]))
    printed_zero = bool(int(data[f"{prefix}_exact_zero"]))
    actual_mod9 = all(a % 9 == 0 and b % 9 == 0 for a, b in compact)
    actual_lambda = actual_mod9 and all(
        (a // 9 + b // 9) % 3 == 0 for a, b in compact
    )
    actual_mod27 = all(a % 27 == 0 and b % 27 == 0 for a, b in compact)
    actual_zero = all(pair == (0, 0) for pair in compact)
    if (
        printed_mod9 != actual_mod9
        or printed_lambda != actual_lambda
        or printed_mod27 != actual_mod27
        or printed_zero != actual_zero
    ):
        raise AssertionError("printed exact-prefix flags failed replay")

    coefficients_a = tuple(values[0][1:])
    coefficients_b = tuple(values[1][1:])
    reduced_target = char2.reduce_aggregate_target(target)
    high_count = 1 if shell == "h1" else 0
    quotient = char2.check_eisenstein_profile(
        coefficients_a,
        coefficients_b,
        target_aggregate=reduced_target,
        high_count=high_count,
    )
    printed_char2 = bool(int(data[f"{prefix}_char2"]))
    if quotient["passes_unitary_quotient"] != printed_char2:
        raise AssertionError("tracked characteristic-two API disagrees")
    if not quotient["target_aggregate_holds"]:
        raise AssertionError("characteristic-two aggregate replay failed")
    if not quotient["shell_support_holds"]:
        raise AssertionError("characteristic-two support replay failed")

    identifiers = ids_a + ids_b
    expected_high = 1 if shell == "h1" else 0
    if sum(norm(raw_profile(identifier)) == 9 for identifier in identifiers) != expected_high:
        raise AssertionError("witness has wrong high count")
    expected_medium = 15 if shell == "h1" else 18
    if sum(norm(raw_profile(identifier)) == 3 for identifier in identifiers) != expected_medium:
        raise AssertionError("witness has wrong medium count")

    digest = assignment_digest(identifiers, compact, target_index)
    if data[f"{prefix}_digest"] != f"0x{digest:x}":
        raise AssertionError("witness digest failed independent replay")


@dataclass(frozen=True)
class Run:
    shell: str
    skip: int
    limit: int
    data: dict[str, str]


def run_pilot(binary: Path, shell: str, skip: int, limit: int) -> Run:
    completed = subprocess.run(
        [
            str(binary),
            "--shell",
            shell,
            "--skip",
            str(skip),
            "--limit",
            str(limit),
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )
    data = parse_output(completed.stdout)
    if data["shell"] != shell:
        raise AssertionError("pilot reported wrong shell")
    if int(data["skip"]) != skip or int(data["limit"]) != limit:
        raise AssertionError("pilot reported wrong deterministic shard")
    for prefix in WITNESS_NAMES:
        replay_witness(data, prefix, shell)
    return Run(shell, skip, limit, data)


def verify_decoration_census(binary: Path, shell: str) -> None:
    completed = subprocess.run(
        [str(binary), "--shell", shell, "--count-decorations"],
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )
    data = parse_output(
        completed.stdout,
        "PASS: exact Burnside decoration census",
    )
    if data["schema"] != "dense-shell-decoration-burnside-v1":
        raise AssertionError("decoration census schema changed")
    expected = EXPECTED_DECORATIONS[shell]
    for key in ("raw_skeletons", "raw_decorations", "canonical_decorations"):
        if int(data[key]) != expected[key]:
            raise AssertionError(
                f"{shell} decoration {key}: "
                f"{data[key]} != {expected[key]}"
            )
    fixed = parse_ints(data["fixed_decorations"])
    if fixed != expected["fixed_decorations"]:
        raise AssertionError(f"{shell} Burnside fixed vector changed")
    if sum(fixed) != 24 * int(data["canonical_decorations"]):
        raise AssertionError(f"{shell} Burnside average is not integral")
    if fixed[0] != int(data["raw_decorations"]):
        raise AssertionError(f"{shell} identity fixed count changed")


def verify_expected(run: Run) -> None:
    expected = EXPECTED[(run.shell, run.skip, run.limit)]
    for key, wanted in expected.items():
        actual: int | str
        if isinstance(wanted, int):
            actual = int(run.data[key])
        else:
            actual = run.data[key]
        if actual != wanted:
            raise AssertionError(
                f"{run.shell} {key}: expected {wanted}, got {actual}"
            )


def verify_resume_split(
    full: Run, first: Run, second: Run
) -> None:
    if first.skip != 0 or second.skip != first.limit:
        raise AssertionError("resume split was not contiguous")
    if first.limit + second.limit != full.limit:
        raise AssertionError("resume split did not cover full shard")
    for key in ADDITIVE_KEYS:
        joined = int(first.data[key]) + int(second.data[key])
        if joined != int(full.data[key]):
            raise AssertionError(
                f"resume split failed for {key}: "
                f"{joined} != {full.data[key]}"
            )


def compile_pilot(directory: Path) -> Path:
    compiler = os.environ.get("CXX", "clang++")
    binary = directory / "dense_shell_classifier_pilot"
    subprocess.run(
        [
            compiler,
            "-O3",
            "-DNDEBUG",
            "-std=c++20",
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-Werror",
            str(CPP),
            "-o",
            str(binary),
        ],
        check=True,
        timeout=120,
    )
    return binary


def verify() -> dict[str, int | str]:
    with tempfile.TemporaryDirectory(prefix="h668-dense-pilot-") as raw:
        binary = compile_pilot(Path(raw))
        h1 = run_pilot(binary, "h1", 0, 100)
        h0 = run_pilot(binary, "h0", 0, 10)
        verify_expected(h1)
        verify_expected(h0)
        first = run_pilot(binary, "h1", 0, 40)
        second = run_pilot(binary, "h1", 40, 60)
        verify_resume_split(h1, first, second)
        verify_decoration_census(binary, "h1")
        verify_decoration_census(binary, "h0")
        partition = partition_audit()
        workload = workload_audit()
    return {
        "h1_canonical_decorations": 100,
        "h0_canonical_decorations": 10,
        "h1_total_canonical_decorations": 22_426_752,
        "h0_total_canonical_decorations": 1_999_128,
        "independent_witness_replays": sum(
            int(run.data[f"{prefix}_present"])
            for run in (h1, h0)
            for prefix in WITNESS_NAMES
        ),
        "joint_char2_mod9_hits": (
            int(h1.data["char2_mod9_hits"])
            + int(h0.data["char2_mod9_hits"])
        ),
        "exact_zero_hits": (
            int(h1.data["exact_zero_hits"])
            + int(h0.data["exact_zero_hits"])
        ),
        "prefix_partition_shards": sum(
            int(partition["shells"][shell]["prefix_count"])
            for shell in ("h1", "h0")
        ),
        "residue_union_affine_upper": int(
            workload["combined_residue_union_affine_upper"]
        ),
        "primitive_leaf_upper": int(
            workload["combined_primitive_leaf_upper"]
        ),
        "status": "PASS",
    }


def main() -> None:
    result = verify()
    for key, value in result.items():
        print(f"{key}={value}")
    print("PASS: independent dense-shell pilot replay and resume audit")


if __name__ == "__main__":
    main()
