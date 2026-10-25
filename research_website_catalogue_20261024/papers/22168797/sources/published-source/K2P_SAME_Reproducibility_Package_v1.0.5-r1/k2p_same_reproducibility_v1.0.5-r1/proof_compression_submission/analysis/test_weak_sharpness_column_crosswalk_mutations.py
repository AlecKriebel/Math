#!/usr/bin/env python3
"""Fail-closed mutations for the weak-sharpness named-column crosswalk."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from collections.abc import Callable

import verify_weak_sharpness_column_crosswalk as replay


REJECTED: list[str] = []


def reseal(value: dict[str, object]) -> None:
    value.pop("payload_sha256", None)
    value["payload_sha256"] = replay.object_sha(value)


def semantic_mutation(
    original: dict[str, object], action: Callable[[dict[str, object]], None]
) -> dict[str, object]:
    value = copy.deepcopy(original)
    action(value)
    reseal(value)
    return value


def must_reject(label: str, action: Callable[[], None]) -> None:
    try:
        action()
    except (RuntimeError, KeyError, IndexError, TypeError):
        REJECTED.append(label)
        return
    raise RuntimeError(f"MUTATION_SURVIVED:{label}")


def main() -> None:
    if not __debug__:
        raise SystemExit("WEAK_SHARPNESS_COLUMN_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    original = json.loads(replay.DEFAULT_INPUT.read_text(encoding="utf-8"))
    replay.verify_artifact(original)

    unsealed = copy.deepcopy(original)
    unsealed["networks"]["W"]["edge_class_order"][0] = "UX"
    must_reject("unsealed_payload_mutation", lambda: replay.verify_artifact(unsealed))

    def swap_edge_order(value):
        order = value["networks"]["W"]["edge_class_order"]
        order[0], order[1] = order[1], order[0]

    must_reject("reordered_edge_classes", lambda: replay.verify_artifact(semantic_mutation(original, swap_edge_order)))
    must_reject(
        "misnamed_edge_class",
        lambda: replay.verify_artifact(semantic_mutation(original, lambda value: value["networks"]["W_prime"]["edge_class_order"].__setitem__(0, "UX1"))),
    )
    must_reject(
        "misnamed_full_parameter_column",
        lambda: replay.verify_artifact(semantic_mutation(original, lambda value: value["networks"]["W"]["full_parameter_columns"][0].__setitem__("plain", "s_UX"))),
    )

    def swap_named_minor(value):
        columns = value["networks"]["W_prime"]["frozen_minor"]["named_columns"]
        columns[0], columns[1] = columns[1], columns[0]

    must_reject("reordered_named_minor_columns", lambda: replay.verify_artifact(semantic_mutation(original, swap_named_minor)))
    must_reject(
        "misnamed_minor_column",
        lambda: replay.verify_artifact(semantic_mutation(original, lambda value: value["networks"]["W"]["frozen_minor"]["named_columns"][8].__setitem__("tex", "s_{UX}"))),
    )
    must_reject(
        "wrong_minor_column_index",
        lambda: replay.verify_artifact(semantic_mutation(original, lambda value: value["networks"]["W_prime"]["frozen_minor"]["column_indices"].__setitem__(8, 9))),
    )
    must_reject(
        "wrong_minor_row",
        lambda: replay.verify_artifact(semantic_mutation(original, lambda value: value["networks"]["W"]["frozen_minor"]["row_indices"].__setitem__(8, 8))),
    )
    must_reject(
        "wrong_minor_determinant",
        lambda: replay.verify_artifact(semantic_mutation(original, lambda value: value["networks"]["W_prime"]["frozen_minor"].__setitem__("determinant", "1"))),
    )
    must_reject(
        "wrong_graph_hash",
        lambda: replay.verify_artifact(semantic_mutation(original, lambda value: value["networks"]["W"].__setitem__("graph_sha256", "0" * 64))),
    )
    must_reject(
        "wrong_descriptor_hash",
        lambda: replay.verify_artifact(semantic_mutation(original, lambda value: value["networks"]["W_prime"].__setitem__("descriptor_sha256", "0" * 64))),
    )
    must_reject(
        "wrong_frozen_certificate_hash",
        lambda: replay.verify_artifact(semantic_mutation(original, lambda value: value["bindings"].__setitem__("frozen_certificate_sha256", "0" * 64))),
    )
    must_reject(
        "wrong_frozen_payload_hash",
        lambda: replay.verify_artifact(semantic_mutation(original, lambda value: value["bindings"].__setitem__("frozen_certificate_payload_sha256", "0" * 64))),
    )
    must_reject(
        "wrong_atlas_hash",
        lambda: replay.verify_artifact(semantic_mutation(original, lambda value: value["bindings"].__setitem__("atlas_sha256", "0" * 64))),
    )
    must_reject(
        "wrong_reticulation_order",
        lambda: replay.verify_artifact(semantic_mutation(original, lambda value: value["networks"]["W"]["canonical_reticulation_order"].reverse())),
    )

    process = subprocess.run(
        [sys.executable, "-O", str(replay.HERE / "verify_weak_sharpness_column_crosswalk.py")],
        text=True,
        capture_output=True,
        check=False,
    )
    replay.need(process.returncode != 0, "OPTIMIZED_REPLAY_ACCEPTED")
    replay.need(
        "WEAK_SHARPNESS_COLUMN_REPLAY_OPTIMIZED_MODE_FORBIDDEN" in process.stdout + process.stderr,
        "OPTIMIZED_REPLAY_MARKER_MISSING",
    )

    print("K2P_WEAK_SHARPNESS_COLUMN_CROSSWALK_MUTATIONS_PASS")
    print(json.dumps({"mutation_count": len(REJECTED), "mutations_rejected": REJECTED, "optimized_mode_rejected": True}, sort_keys=True))


if __name__ == "__main__":
    main()
