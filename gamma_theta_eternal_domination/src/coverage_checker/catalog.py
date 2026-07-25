"""Strict, byte-bound reconstruction of the 55-host extension universe."""

from __future__ import annotations

import csv
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
from typing import Iterable

from .graph import Graph


KNOWN_CATALOG_SHA256 = (
    "801f054853d07652c795fb16217425869f857d7f5d74e427165d554faf4eae1d"
)
KNOWN_PARAMETERS_SHA256 = (
    "ef74175dfd81542a167feed5a2d7f66be723846993642fb65344d08655b594c6"
)

CATALOG_HEADER = ("catalog_id", "n", "graph6", "source")
PARAMETERS_HEADER = (
    "catalog_id",
    "n",
    "m",
    "graph6",
    "gamma",
    "i",
    "alpha",
    "gamma_infinity_one_guard",
    "theta",
    "gamma_witness",
    "minimum_dominating_set_count",
    "i_witness",
    "alpha_witness",
    "greatest_eternal_family_size",
    "greatest_eternal_family_sha256",
)
_DECIMAL = re.compile(r"(?:0|[1-9][0-9]*)\Z")


class CatalogError(ValueError):
    """The pinned catalog or its independently computed join is malformed."""


@dataclass(frozen=True, slots=True)
class UniversePolicy:
    """Expected immutable shape of an input universe.

    The production policy below is the only policy exposed by the CLI.
    Parameterization exists solely so bounded tests can exercise every audit
    stage without manufacturing the 110,537-row production artifact.
    """

    catalog_sha256: str
    parameters_sha256: str
    input_rows: int
    selected_hosts: int
    raw_origins: int
    target_guard_count: int
    distribution: tuple[tuple[int, int, int], ...]


PRODUCTION_POLICY = UniversePolicy(
    catalog_sha256=KNOWN_CATALOG_SHA256,
    parameters_sha256=KNOWN_PARAMETERS_SHA256,
    input_rows=56,
    selected_hosts=55,
    raw_origins=110_537,
    target_guard_count=3,
    distribution=((10, 2, 2), (11, 1, 2), (11, 2, 51)),
)


@dataclass(frozen=True, slots=True)
class HostRecord:
    index: int
    catalog_id: str
    order: int
    graph6: str
    graph: Graph
    gamma: int
    alpha: int
    gamma_infinity: int
    theta: int

    @property
    def raw_expected(self) -> int:
        return (1 << self.order) - 1


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _strict_nonnegative(value: object, field: str) -> int:
    if not isinstance(value, str) or _DECIMAL.fullmatch(value) is None:
        raise CatalogError(f"{field} is not a canonical nonnegative integer")
    return int(value)


def _read_csv(path: Path, header: tuple[str, ...]) -> tuple[dict[str, str], ...]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle, strict=True)
            try:
                actual_header = next(reader)
            except StopIteration as error:
                raise CatalogError(f"empty CSV: {path}") from error
            if tuple(actual_header) != header:
                raise CatalogError(
                    f"unexpected header in {path}: {tuple(actual_header)!r}"
                )
            rows: list[dict[str, str]] = []
            for line_number, values in enumerate(reader, 2):
                if len(values) != len(header):
                    raise CatalogError(
                        f"{path}:{line_number} has {len(values)} fields, "
                        f"expected {len(header)}"
                    )
                rows.append(dict(zip(header, values, strict=True)))
    except (OSError, UnicodeError, csv.Error) as error:
        raise CatalogError(f"cannot read strict CSV {path}: {error}") from error
    return tuple(rows)


def _is_connected(graph: Graph) -> bool:
    if graph.order == 0:
        return False
    reached = 1
    frontier = 1
    while frontier:
        bit = frontier & -frontier
        frontier ^= bit
        vertex = bit.bit_length() - 1
        new = graph.adjacency[vertex] & ~reached
        reached |= new
        frontier |= new
    return reached == (1 << graph.order) - 1


def _validate_sha256(value: str, field: str) -> None:
    if re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise CatalogError(f"{field} is not a lowercase SHA-256 digest")


def load_host_universe(
    catalog_path: Path,
    parameters_path: Path,
    *,
    policy: UniversePolicy = PRODUCTION_POLICY,
) -> tuple[HostRecord, ...]:
    """Load and independently validate the exact selected host sequence."""

    _validate_sha256(policy.catalog_sha256, "catalog policy hash")
    _validate_sha256(policy.parameters_sha256, "parameter policy hash")
    catalog_hash = sha256_file(catalog_path)
    parameter_hash = sha256_file(parameters_path)
    if catalog_hash != policy.catalog_sha256:
        raise CatalogError(
            f"catalog SHA-256 mismatch: {catalog_hash} != "
            f"{policy.catalog_sha256}"
        )
    if parameter_hash != policy.parameters_sha256:
        raise CatalogError(
            f"parameter SHA-256 mismatch: {parameter_hash} != "
            f"{policy.parameters_sha256}"
        )

    catalog_rows = _read_csv(catalog_path, CATALOG_HEADER)
    parameter_rows = _read_csv(parameters_path, PARAMETERS_HEADER)
    if len(catalog_rows) != policy.input_rows or len(parameter_rows) != policy.input_rows:
        raise CatalogError(
            "input-row count mismatch: "
            f"catalog={len(catalog_rows)}, parameters={len(parameter_rows)}, "
            f"expected={policy.input_rows}"
        )

    catalog_ids = tuple(row["catalog_id"] for row in catalog_rows)
    parameter_ids = tuple(row["catalog_id"] for row in parameter_rows)
    if catalog_ids != parameter_ids:
        raise CatalogError("catalog and parameter identifiers/orders differ")
    if len(set(catalog_ids)) != len(catalog_ids):
        raise CatalogError("duplicate catalog identifier")
    parameter_by_id = {
        row["catalog_id"]: row
        for row in parameter_rows
    }

    all_graph6: set[str] = set()
    selected: list[HostRecord] = []
    for catalog_row in catalog_rows:
        identifier = catalog_row["catalog_id"]
        if not identifier:
            raise CatalogError("empty catalog identifier")
        parameter_row = parameter_by_id[identifier]
        if catalog_row["graph6"] != parameter_row["graph6"]:
            raise CatalogError(f"graph6 join mismatch for {identifier}")
        catalog_order = _strict_nonnegative(catalog_row["n"], f"{identifier}.n")
        parameter_order = _strict_nonnegative(parameter_row["n"], f"{identifier}.n")
        if catalog_order != parameter_order:
            raise CatalogError(f"order join mismatch for {identifier}")
        graph6 = catalog_row["graph6"]
        if graph6 in all_graph6:
            raise CatalogError(f"duplicate catalog graph6: {graph6}")
        all_graph6.add(graph6)
        graph = Graph.from_graph6(graph6)
        if graph.order != catalog_order or graph.to_graph6() != graph6:
            raise CatalogError(f"encoded order mismatch for {identifier}")
        edge_count = _strict_nonnegative(
            parameter_row["m"], f"{identifier}.m"
        )
        if graph.size != edge_count:
            raise CatalogError(f"encoded size mismatch for {identifier}")

        gamma = _strict_nonnegative(
            parameter_row["gamma"], f"{identifier}.gamma"
        )
        alpha = _strict_nonnegative(
            parameter_row["alpha"], f"{identifier}.alpha"
        )
        eternal = _strict_nonnegative(
            parameter_row["gamma_infinity_one_guard"],
            f"{identifier}.gamma_infinity_one_guard",
        )
        theta = _strict_nonnegative(
            parameter_row["theta"], f"{identifier}.theta"
        )
        if not (
            alpha == policy.target_guard_count
            and eternal == policy.target_guard_count
            and eternal < theta
        ):
            continue
        if not _is_connected(graph):
            raise CatalogError(f"selected host is disconnected: {identifier}")
        selected.append(
            HostRecord(
                index=len(selected),
                catalog_id=identifier,
                order=graph.order,
                graph6=graph6,
                graph=graph,
                gamma=gamma,
                alpha=alpha,
                gamma_infinity=eternal,
                theta=theta,
            )
        )

    if len(selected) != policy.selected_hosts:
        raise CatalogError(
            f"selected {len(selected)} hosts, expected {policy.selected_hosts}"
        )
    raw_total = sum(host.raw_expected for host in selected)
    if raw_total != policy.raw_origins:
        raise CatalogError(
            f"selected universe has {raw_total} origins, "
            f"expected {policy.raw_origins}"
        )
    distribution: dict[tuple[int, int], int] = {}
    for host in selected:
        key = (host.order, host.gamma)
        distribution[key] = distribution.get(key, 0) + 1
    actual_distribution = tuple(
        (order, gamma, count)
        for (order, gamma), count in sorted(distribution.items())
    )
    if actual_distribution != tuple(sorted(policy.distribution)):
        raise CatalogError(
            "selected-host distribution mismatch: "
            f"{actual_distribution!r} != {tuple(sorted(policy.distribution))!r}"
        )
    return tuple(selected)


def host_by_id(hosts: Iterable[HostRecord]) -> dict[str, HostRecord]:
    result: dict[str, HostRecord] = {}
    for host in hosts:
        if host.catalog_id in result:
            raise CatalogError(f"duplicate selected host {host.catalog_id}")
        result[host.catalog_id] = host
    return result
