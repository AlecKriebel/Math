#!/usr/bin/env python3
"""Two-step transition-kernel obstructions for one-guard domination.

The mathematical result implemented here is stated and proved in
``math/lemmas/two_step_transition_kernel.md``.  The certificate checker
recomputes every local domination fact directly from the graph; it does not
call an eternal-domination fixed-point routine.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import tempfile
import time
from typing import Iterator

from search.private_obstruction import (
    find_private_obstruction,
    maximum_independent_masks,
)
from verifier_a.core import (
    BitGraph,
    alpha,
    domination_number,
    eternal_fixed_point,
    theta,
)


CAMPAIGN_ROOT = Path(__file__).resolve().parents[2]
MEASUREMENT_KEYS = (
    "population",
    "one_step_rejected",
    "two_step_rejected",
    "strict_two_step_additional",
    "survives_two_step",
)


def _vertex(singleton: int) -> int:
    return singleton.bit_length() - 1


def _first_undominated(graph: BitGraph, configuration: int) -> int | None:
    for vertex, closed in enumerate(graph.closed):
        if not closed & configuration:
            return vertex
    return None


@dataclass(frozen=True, slots=True)
class FailedSecondMove:
    """A second defender and a vertex its resulting state misses."""

    guard: int
    newly_undominated: int


@dataclass(frozen=True, slots=True)
class FailedFirstMove:
    """Why one possible first defender cannot lead to an eternal state.

    Exactly one of the following two modes is populated:

    * ``first_undominated`` names a vertex missed immediately; or
    * ``second_attack`` and ``second_failures`` prove that the dominating
      first successor is not secure.
    """

    guard: int
    first_undominated: int | None
    second_attack: int | None
    second_failures: tuple[FailedSecondMove, ...]


@dataclass(frozen=True, slots=True)
class TwoStepObstruction:
    """A forced independent state and an attack with no secure successor."""

    independent_set: int
    attack: int
    failed_first_moves: tuple[FailedFirstMove, ...]

    @property
    def genuinely_two_step(self) -> bool:
        return any(
            record.second_attack is not None
            for record in self.failed_first_moves
        )


def legal_dominating_successors(
    graph: BitGraph, configuration: int, attacked: int
) -> Iterator[tuple[int, int]]:
    """Yield ``(moved_guard, successor)`` for all legal dominating swaps."""

    if (
        type(configuration) is not int
        or configuration < 0
        or configuration & ~graph.full
        or type(attacked) is not int
        or not 0 <= attacked < graph.n
        or configuration & (1 << attacked)
    ):
        raise ValueError("require a valid state and an unoccupied attack")
    attacked_bit = 1 << attacked
    movable = configuration & graph.adj[attacked]
    while movable:
        guard_bit = movable & -movable
        movable ^= guard_bit
        successor = configuration ^ guard_bit ^ attacked_bit
        if graph.is_dominating(successor):
            yield _vertex(guard_bit), successor


def insecurity_certificate(
    graph: BitGraph, configuration: int
) -> tuple[int, tuple[FailedSecondMove, ...]] | None:
    """Return an attack defeating a dominating configuration, if one exists."""

    if not graph.is_dominating(configuration):
        raise ValueError("security is defined here only for dominating sets")
    unoccupied = graph.full ^ configuration
    while unoccupied:
        attacked_bit = unoccupied & -unoccupied
        unoccupied ^= attacked_bit
        attacked = _vertex(attacked_bit)
        failures: list[FailedSecondMove] = []
        movable = configuration & graph.adj[attacked]
        while movable:
            guard_bit = movable & -movable
            movable ^= guard_bit
            guard = _vertex(guard_bit)
            successor = configuration ^ guard_bit ^ attacked_bit
            witness = _first_undominated(graph, successor)
            if witness is None:
                break
            failures.append(FailedSecondMove(guard, witness))
        else:
            return attacked, tuple(failures)
    return None


def is_secure_configuration(graph: BitGraph, configuration: int) -> bool:
    """Whether every unoccupied attack has a dominating one-guard response."""

    return (
        graph.is_dominating(configuration)
        and insecurity_certificate(graph, configuration) is None
    )


def find_two_step_obstruction(
    graph: BitGraph,
) -> TwoStepObstruction | None:
    """Find a maximum independent state with no secure first successor.

    Returning ``None`` means only that this depth-two necessary condition
    passes.  It does not establish an eternal family.
    """

    for independent in maximum_independent_masks(graph):
        unoccupied = graph.full ^ independent
        while unoccupied:
            attacked_bit = unoccupied & -unoccupied
            unoccupied ^= attacked_bit
            attacked = _vertex(attacked_bit)
            failures: list[FailedFirstMove] = []
            movable = independent & graph.adj[attacked]
            while movable:
                guard_bit = movable & -movable
                movable ^= guard_bit
                guard = _vertex(guard_bit)
                successor = independent ^ guard_bit ^ attacked_bit
                immediate_witness = _first_undominated(graph, successor)
                if immediate_witness is not None:
                    failures.append(
                        FailedFirstMove(
                            guard=guard,
                            first_undominated=immediate_witness,
                            second_attack=None,
                            second_failures=(),
                        )
                    )
                    continue
                insecurity = insecurity_certificate(graph, successor)
                if insecurity is None:
                    break
                second_attack, second_failures = insecurity
                failures.append(
                    FailedFirstMove(
                        guard=guard,
                        first_undominated=None,
                        second_attack=second_attack,
                        second_failures=second_failures,
                    )
                )
            else:
                return TwoStepObstruction(
                    independent_set=independent,
                    attack=attacked,
                    failed_first_moves=tuple(failures),
                )
    return None


def verify_two_step_obstruction(
    graph: BitGraph, obstruction: TwoStepObstruction
) -> bool:
    """Verify a two-step lower-bound certificate from elementary predicates."""

    try:
        if not isinstance(obstruction, TwoStepObstruction):
            return False
        independent = obstruction.independent_set
        if (
            type(independent) is not int
            or independent < 0
            or independent & ~graph.full
            or independent.bit_count() != alpha(graph)
            or not graph.is_independent(independent)
        ):
            return False
        attack = obstruction.attack
        if (
            type(attack) is not int
            or not 0 <= attack < graph.n
            or independent & (1 << attack)
            or not isinstance(obstruction.failed_first_moves, tuple)
        ):
            return False

        expected_first_guards = {
            guard
            for guard in range(graph.n)
            if independent & (1 << guard)
            and graph.adj[attack] & (1 << guard)
        }
        if len(obstruction.failed_first_moves) != len(expected_first_guards):
            return False
        first_records: dict[int, FailedFirstMove] = {}
        for record in obstruction.failed_first_moves:
            if not isinstance(record, FailedFirstMove):
                return False
            if (
                type(record.guard) is not int
                or record.guard in first_records
            ):
                return False
            first_records[record.guard] = record
        if set(first_records) != expected_first_guards:
            return False

        attack_bit = 1 << attack
        for guard, record in first_records.items():
            successor = independent ^ (1 << guard) ^ attack_bit
            immediate = record.first_undominated
            if immediate is not None:
                if (
                    type(immediate) is not int
                    or not 0 <= immediate < graph.n
                    or record.second_attack is not None
                    or record.second_failures != ()
                    or graph.closed[immediate] & successor
                    or graph.is_dominating(successor)
                ):
                    return False
                continue

            if not graph.is_dominating(successor):
                return False
            second_attack = record.second_attack
            if (
                type(second_attack) is not int
                or not 0 <= second_attack < graph.n
                or successor & (1 << second_attack)
                or not isinstance(record.second_failures, tuple)
            ):
                return False
            expected_second_guards = {
                second_guard
                for second_guard in range(graph.n)
                if successor & (1 << second_guard)
                and graph.adj[second_attack] & (1 << second_guard)
            }
            if len(record.second_failures) != len(expected_second_guards):
                return False
            second_records: dict[int, FailedSecondMove] = {}
            for second_record in record.second_failures:
                if not isinstance(second_record, FailedSecondMove):
                    return False
                second_guard = second_record.guard
                if (
                    type(second_guard) is not int
                    or second_guard in second_records
                ):
                    return False
                second_records[second_guard] = second_record
            if set(second_records) != expected_second_guards:
                return False
            second_attack_bit = 1 << second_attack
            for second_guard, second_record in second_records.items():
                witness = second_record.newly_undominated
                second_successor = (
                    successor ^ (1 << second_guard) ^ second_attack_bit
                )
                if (
                    type(witness) is not int
                    or not 0 <= witness < graph.n
                    or graph.closed[witness] & second_successor
                    or graph.is_dominating(second_successor)
                ):
                    return False
        return True
    except (IndexError, TypeError, ValueError, OverflowError):
        return False


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _measurement(graphs: Iterator[BitGraph]) -> dict[str, int]:
    counters: Counter[str] = Counter()
    for graph in graphs:
        counters["population"] += 1
        one_step = find_private_obstruction(graph) is not None
        obstruction = find_two_step_obstruction(graph)
        two_step = obstruction is not None
        if one_step and not two_step:
            raise AssertionError("depth-two test must subsume the one-step test")
        if obstruction is not None and not verify_two_step_obstruction(
            graph, obstruction
        ):
            raise AssertionError("finder produced an invalid certificate")
        counters["one_step_rejected"] += one_step
        counters["two_step_rejected"] += two_step
        counters["strict_two_step_additional"] += two_step and not one_step
        counters["survives_two_step"] += not two_step
    return {key: counters[key] for key in MEASUREMENT_KEYS}


def _edge_toggle_population(ledger: Path) -> Iterator[BitGraph]:
    with ledger.open(newline="", encoding="ascii") as handle:
        reader = csv.DictReader(handle)
        required = {
            "canonical_graph6",
            "gamma_a",
            "gamma_b",
            "alpha_a",
            "alpha_b",
            "gamma_infinity_a",
            "gamma_infinity_b",
            "theta_a",
            "theta_b",
        }
        if reader.fieldnames is None or not required <= set(reader.fieldnames):
            raise ValueError("edge-toggle ledger has an unexpected schema")
        for row in reader:
            parameters = tuple(
                int(row[name])
                for name in (
                    "gamma_a",
                    "gamma_b",
                    "alpha_a",
                    "alpha_b",
                    "gamma_infinity_a",
                    "gamma_infinity_b",
                    "theta_a",
                    "theta_b",
                )
            )
            if parameters == (3, 3, 3, 3, 4, 4, 4, 4):
                yield BitGraph.from_graph6(row["canonical_graph6"])


def _small_order_measurement(geng: Path, order: int) -> dict[str, int]:
    process = subprocess.Popen(
        (str(geng), "-qc", str(order)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="ascii",
    )
    if process.stdout is None or process.stderr is None:
        raise RuntimeError("failed to capture geng streams")
    counters: Counter[str] = Counter()
    try:
        for line in process.stdout:
            graph = BitGraph.from_graph6(line)
            counters["connected_unlabeled_graphs"] += 1
            if alpha(graph) != 3 or domination_number(graph) != 3:
                continue
            if theta(graph) <= 3:
                continue
            counters["static_gamma_alpha_3_theta_gt_3"] += 1
            one_step = find_private_obstruction(graph) is not None
            obstruction = find_two_step_obstruction(graph)
            two_step = obstruction is not None
            if one_step and not two_step:
                raise AssertionError("depth-two test failed to subsume depth one")
            if obstruction is not None and not verify_two_step_obstruction(
                graph, obstruction
            ):
                raise AssertionError("invalid generated obstruction")
            eternal_three = eternal_fixed_point(graph, 3).exists
            if eternal_three and two_step:
                raise AssertionError("obstruction rejects an eternal graph")
            counters["eternal_three"] += eternal_three
            counters["one_step_rejected"] += one_step
            counters["two_step_rejected"] += two_step
            counters["strict_two_step_additional"] += two_step and not one_step
            counters["survives_two_step"] += not two_step
    except BaseException:
        process.terminate()
        process.wait()
        process.stdout.close()
        process.stderr.close()
        raise
    process.stdout.close()
    stderr = process.stderr.read()
    process.stderr.close()
    return_code = process.wait()
    if return_code:
        raise RuntimeError(f"geng exited {return_code}: {stderr}")
    counters["order"] = order
    keys = (
        "order",
        "connected_unlabeled_graphs",
        "static_gamma_alpha_3_theta_gt_3",
        "eternal_three",
        "one_step_rejected",
        "two_step_rejected",
        "strict_two_step_additional",
        "survives_two_step",
    )
    return {key: counters[key] for key in keys}


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--edge-toggle-ledger",
        type=Path,
        default=CAMPAIGN_ROOT / "results" / "edge_toggles_unique.csv",
    )
    parser.add_argument(
        "--geng",
        type=Path,
        default=CAMPAIGN_ROOT / "tools" / "nauty2_9_3" / "geng",
    )
    parser.add_argument("--orders", type=int, nargs="*", default=(5, 6, 7, 8, 9))
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    ledger = arguments.edge_toggle_ledger.resolve()
    geng = arguments.geng.resolve()
    if not ledger.is_file() or not geng.is_file():
        raise SystemExit("the edge-toggle ledger and geng binary must exist")
    if any(order < 1 for order in arguments.orders):
        raise SystemExit("orders must be positive")

    started = time.perf_counter()
    edge_measurement = _measurement(_edge_toggle_population(ledger))
    if edge_measurement.get("population") != 8_587:
        raise RuntimeError("edge-toggle target population is not 8,587")
    small_orders = [
        _small_order_measurement(geng, order)
        for order in arguments.orders
    ]
    usage = resource.getrusage(resource.RUSAGE_SELF)
    result = {
        "format": "gamma-theta-two-step-obstruction-measurement-v1",
        "status": "complete",
        "scope_note": (
            "Filter-performance measurement only; the proved theorem is in "
            "math/lemmas/two_step_transition_kernel.md."
        ),
        "edge_toggle_population": {
            "predicate": "gamma=alpha=3 and gamma_infinity=theta=4",
            **edge_measurement,
        },
        "small_connected_unlabeled": {
            "predicate": "gamma=alpha=3 and theta>3",
            "orders": small_orders,
        },
        "inputs": {
            "edge_toggle_ledger": str(ledger),
            "edge_toggle_ledger_sha256": _sha256_file(ledger),
            "geng": str(geng),
            "geng_sha256": _sha256_file(geng),
        },
        "implementation": {
            "source": str(Path(__file__).resolve()),
            "source_sha256": _sha256_file(Path(__file__).resolve()),
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "resources": {
            "wall_seconds": time.perf_counter() - started,
            "user_cpu_seconds": usage.ru_utime,
            "system_cpu_seconds": usage.ru_stime,
            "maximum_resident_set_size_raw": usage.ru_maxrss,
        },
    }
    if arguments.output is not None:
        _atomic_json(arguments.output.resolve(), result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
