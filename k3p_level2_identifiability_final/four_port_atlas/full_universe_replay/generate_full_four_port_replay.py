#!/usr/bin/env python3
"""Regenerate the complete K3P four-port relation universe.

The enumeration begins with the five primitive directed cores and does not
open the frozen 14-orbit lock, the frozen 405,216-row companion ledger, or the
missing cloud descriptor corpus.  It constructs the six rigid sources, all
2,814 complete targets, and all 24 labelled port permutations, then applies
the topology, exact-rank, quadratic, graph, and restoration-routing filters in
the order used by the bounded theorem.

This is the producing implementation.  ``verify_full_four_port_replay.py`` is
deliberately separate and does not import this file or the atlas compiler.
"""

from __future__ import annotations

import argparse
import collections
import dataclasses
import gzip
import hashlib
import importlib.util
import itertools
import json
import os
import sys
import time
from math import gcd
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS_PATH = PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py"
ARTIFACTS = HERE / "artifacts"

SOURCE_COUNT = 6
TARGET_COUNT = 2_814
PERMUTATION_COUNT = 24
RAW_PER_SOURCE = TARGET_COUNT * PERMUTATION_COUNT
RAW_TOTAL = SOURCE_COUNT * RAW_PER_SOURCE

# The normalized three-leaf H_14 quartic, written in the canonical
# conservation-supported K3P Fourier coordinates.  A transported four-port
# marginal is obtained by inserting character 0 at one omitted port and by
# applying an automorphism of Z_2 x Z_2 to the three nonzero characters.
H14_BASE_TERMS = (
    (+1, ((0, 0, 0), (1, 2, 3), (2, 3, 1), (3, 1, 2))),
    (-1, ((0, 0, 0), (1, 3, 2), (2, 1, 3), (3, 2, 1))),
    (-1, ((0, 1, 1), (1, 2, 3), (2, 0, 2), (3, 3, 0))),
    (+1, ((0, 1, 1), (1, 3, 2), (2, 2, 0), (3, 0, 3))),
    (+1, ((0, 2, 2), (1, 0, 1), (2, 1, 3), (3, 3, 0))),
    (-1, ((0, 2, 2), (1, 1, 0), (2, 3, 1), (3, 0, 3))),
    (-1, ((0, 3, 3), (1, 0, 1), (2, 2, 0), (3, 1, 2))),
    (+1, ((0, 3, 3), (1, 1, 0), (2, 0, 2), (3, 2, 1))),
)


def fail(code: str, detail: object | None = None) -> "None":
    raise SystemExit(code if detail is None else f"{code}: {detail}")


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        fail(code, detail)


def canonical_data(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {
            field.name: canonical_data(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, dict):
        return {
            str(key): canonical_data(item)
            for key, item in sorted(value.items(), key=lambda pair: repr(pair[0]))
        }
    if isinstance(value, (tuple, list)):
        return [canonical_data(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        canonical_data(value), sort_keys=True, separators=(",", ":")
    ).encode()


def object_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    with temporary.open("wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_bytes(
        path,
        (json.dumps(canonical_data(value), indent=2, sort_keys=True) + "\n").encode(),
    )


def deterministic_gzip(path: Path, chunks: Iterable[bytes]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    plain = hashlib.sha256()
    plain_bytes = 0
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as encoded:
            for chunk in chunks:
                plain.update(chunk)
                plain_bytes += len(chunk)
                encoded.write(chunk)
        raw.flush()
        os.fsync(raw.fileno())
    os.replace(temporary, path)
    return {
        "sha256": file_sha256(path),
        "uncompressed_sha256": plain.hexdigest(),
        "uncompressed_bytes": plain_bytes,
    }


def load_atlas():
    spec = importlib.util.spec_from_file_location("k3p_full_four_port_core", ATLAS_PATH)
    require(spec is not None and spec.loader is not None, "ATLAS_IMPORT_SPEC_FAIL")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def descriptor_sha256(descriptor: object) -> str:
    # This literal-map hash is the historical map-binding convention, but no
    # historical hash is read or trusted by this producer.
    return hashlib.sha256(repr(descriptor).encode()).hexdigest()


def graph_sha256(graph) -> str:
    nodes = []
    for node, data in graph.nodes(data=True):
        nodes.append(
            {
                "id": repr(node),
                "role": data.get("role"),
                "label": data.get("label"),
                "dummy": bool(data.get("dummy", False)),
                "dummy_name": data.get("dummy_name"),
            }
        )
    edges = [
        {"tail": repr(u), "head": repr(v), "edge_role": data.get("edge_role")}
        for u, v, data in graph.edges(data=True)
    ]
    return object_sha256(
        {
            "nodes": sorted(nodes, key=lambda row: row["id"]),
            "edges": sorted(edges, key=lambda row: (row["tail"], row["head"], row["edge_role"] or "")),
        }
    )


def exact_rank(atlas, descriptor) -> dict[str, Any]:
    certificate = atlas.rank_certificate(descriptor, salt=0)
    rank = int(certificate["rank"])
    rows = tuple(int(x) for x in certificate["rows"])
    columns = tuple(int(x) for x in certificate["columns"])
    require(rank == len(rows) == len(columns), "RANK_MINOR_SIZE_FAIL")
    require(Fraction(certificate["determinant"]) != 0, "RANK_MINOR_ZERO_FAIL")
    return {
        "rank": rank,
        "rows": list(rows),
        "columns": list(columns),
        "determinant": certificate["determinant"],
        "edge_triples": [list(row) for row in certificate["edge_triples"]],
        "inheritance": list(certificate["lambdas"]),
    }


def _lcm(left: int, right: int) -> int:
    return abs(left // gcd(left, right) * right) if left and right else 0


def base_syzygy_rank_upper(atlas, descriptor) -> dict[str, Any]:
    """Prove an a priori generic rank upper from polynomial vector fields.

    For each K3P edge-sector parameter x_i and inheritance parameter l_j we
    solve coefficientwise for vector fields

        V(x_i)=x_i A_i(l),
        V(l_j)=l_j(1-l_j) C_j(l without l_j),

    with multilinear A_i and C_j.  Every solution is an exact polynomial
    identity J_f V=0.  The dimension of their evaluation span at one strict
    point therefore gives a rigorous generic rank upper; the sampled
    Jacobian rank is not used as an upper bound.
    """
    from sympy import ZZ
    from sympy.polys.matrices import DomainMatrix

    edge_variables = 3 * descriptor.edge_class_count
    inheritance_count = descriptor.retic_count
    parameter_count = edge_variables + inheritance_count
    labels = []
    for parameter in range(edge_variables):
        for mask in range(1 << inheritance_count):
            labels.append(("edge", parameter, mask))
    for parameter in range(inheritance_count):
        for mask in range(1 << inheritance_count):
            if not (mask >> parameter) & 1:
                labels.append(("inheritance", parameter, mask))
    column = {label: index for index, label in enumerate(labels)}
    constraints: dict[tuple[int, tuple[int, ...]], dict[int, int]] = collections.defaultdict(
        lambda: collections.defaultdict(int)
    )
    for output_index, polynomial in enumerate(atlas.output_sparse_polynomials(descriptor)):
        for exponents, coefficient in polynomial.items():
            exponents = tuple(exponents)
            for parameter in range(edge_variables):
                power = exponents[parameter]
                if not power:
                    continue
                for mask in range(1 << inheritance_count):
                    shifted = list(exponents)
                    for inheritance_index in range(inheritance_count):
                        if (mask >> inheritance_index) & 1:
                            shifted[edge_variables + inheritance_index] += 1
                    constraints[(output_index, tuple(shifted))][
                        column[("edge", parameter, mask)]
                    ] += coefficient * power
            for inheritance_index in range(inheritance_count):
                position = edge_variables + inheritance_index
                power = exponents[position]
                if not power:
                    continue
                for mask in range(1 << inheritance_count):
                    if (mask >> inheritance_index) & 1:
                        continue
                    shifted = list(exponents)
                    for other in range(inheritance_count):
                        if (mask >> other) & 1:
                            shifted[edge_variables + other] += 1
                    constraints[(output_index, tuple(shifted))][
                        column[("inheritance", inheritance_index, mask)]
                    ] += coefficient * power
                    shifted[position] += 1
                    constraints[(output_index, tuple(shifted))][
                        column[("inheritance", inheritance_index, mask)]
                    ] -= coefficient * power
    system = []
    for key in sorted(constraints):
        sparse = constraints[key]
        row = [sparse.get(index, 0) for index in range(len(labels))]
        if any(row):
            system.append(row)

    edge_triples, inheritance = atlas.default_exact_point(descriptor, salt=0)
    edge_values = tuple(value for triple in edge_triples for value in triple)
    evaluation = []
    for parameter in range(parameter_count):
        rational_row = []
        for kind, index, mask in labels:
            monomial = Fraction(1)
            for inheritance_index, value in enumerate(inheritance):
                if (mask >> inheritance_index) & 1:
                    monomial *= value
            entry = Fraction(0)
            if kind == "edge" and parameter == index:
                entry = edge_values[index] * monomial
            elif kind == "inheritance" and parameter == edge_variables + index:
                value = inheritance[index]
                entry = value * (1 - value) * monomial
            rational_row.append(entry)
        denominator = 1
        for value in rational_row:
            denominator = _lcm(denominator, value.denominator)
        evaluation.append([int(value * denominator) for value in rational_row])

    def integer_rank(rows):
        if not rows:
            return 0
        return int(DomainMatrix.from_list(rows, ZZ).rank())

    coefficient_rank = integer_rank(system)
    stacked_rank = integer_rank(system + evaluation)
    independent_fields = stacked_rank - coefficient_rank
    require(
        0 <= independent_fields <= parameter_count,
        "SYZYGY_FIELD_DIMENSION_FAIL",
        independent_fields,
    )
    return {
        "mechanism": "coefficientwise_multilinear_polynomial_vector_fields",
        "parameter_count": parameter_count,
        "unknown_coefficient_count": len(labels),
        "coefficient_equation_count": len(system),
        "coefficient_system_rank": coefficient_rank,
        "stacked_system_rank": stacked_rank,
        "independent_kernel_fields": independent_fields,
        "certified_rank_upper": parameter_count - independent_fields,
    }


def primitive_universe(atlas):
    sources = tuple(atlas.source_supports())
    selected = tuple(atlas.target_completions(4, True))
    marginalized = tuple(atlas.target_completions(4, False))
    targets = selected + marginalized
    permutations = tuple(itertools.permutations(range(4)))
    require(len(sources) == SOURCE_COUNT, "SOURCE_CENSUS_FAIL", len(sources))
    require(len(selected) == 831, "SELECTED_TARGET_CENSUS_FAIL", len(selected))
    require(len(marginalized) == 1_983, "MARGINAL_TARGET_CENSUS_FAIL", len(marginalized))
    require(len(targets) == TARGET_COUNT, "TARGET_CENSUS_FAIL", len(targets))
    require(len(permutations) == PERMUTATION_COUNT, "PERMUTATION_CENSUS_FAIL")
    return sources, targets, permutations


def topology_filter(atlas, sources, targets, permutations):
    target_signatures = tuple(
        atlas.topology_signature(atlas.selected_graph_from_completion(target))
        for target in targets
    )
    compatible: list[list[tuple[int, int, tuple[int, ...]]]] = []
    reasons: list[collections.Counter[str]] = []
    for source in sources:
        source_signature = atlas.topology_signature(source.graph)
        accepted_rows = []
        rejected = collections.Counter()
        for target_index, target_signature in enumerate(target_signatures):
            for permutation_index, permutation in enumerate(permutations):
                accepted, reason = atlas.immediate_compatible(
                    source_signature,
                    atlas.permute_signature(target_signature, permutation),
                )
                if accepted:
                    accepted_rows.append((target_index, permutation_index, permutation))
                else:
                    require(
                        reason in {"quartet", "tree_sunlet"},
                        "TOPOLOGY_REASON_FAIL",
                        reason,
                    )
                    rejected[reason] += 1
        compatible.append(accepted_rows)
        reasons.append(rejected)
    require(sum(map(len, compatible)) == 27_834, "POST_TOPOLOGY_CENSUS_FAIL")
    return target_signatures, compatible, reasons


def compile_maps(atlas, sources, targets, compatible):
    source_descriptors = tuple(atlas.model_descriptor_fast2(source.graph) for source in sources)
    keys = sorted(
        {
            (target_index, permutation)
            for lane in compatible
            for target_index, _, permutation in lane
        },
        key=lambda key: (key[0], key[1]),
    )
    require(len(keys) == 13_686, "COMPATIBLE_KEY_CENSUS_FAIL", len(keys))
    target_descriptors = {}
    descriptors_by_hash = {}
    for ordinal, (target_index, permutation) in enumerate(keys):
        relabelled = atlas.relabel_record(targets[target_index], permutation)
        descriptor = atlas.model_descriptor_fast2(relabelled.graph)
        digest = descriptor_sha256(descriptor)
        previous = descriptors_by_hash.setdefault(digest, descriptor)
        require(previous == descriptor, "DESCRIPTOR_HASH_COLLISION", digest)
        target_descriptors[(target_index, permutation)] = descriptor
        if ordinal and ordinal % 2_000 == 0:
            print(
                json.dumps(
                    {
                        "compiled_target_keys": ordinal,
                        "target_key_total": len(keys),
                        "unique_target_maps": len(descriptors_by_hash),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    for descriptor in source_descriptors:
        digest = descriptor_sha256(descriptor)
        previous = descriptors_by_hash.setdefault(digest, descriptor)
        require(previous == descriptor, "SOURCE_DESCRIPTOR_HASH_COLLISION", digest)
    return source_descriptors, target_descriptors, descriptors_by_hash


def rank_all(atlas, descriptors_by_hash):
    rows = []
    by_hash = {}
    for ordinal, digest in enumerate(sorted(descriptors_by_hash)):
        descriptor = descriptors_by_hash[digest]
        certificate = exact_rank(atlas, descriptor)
        by_hash[digest] = certificate["rank"]
        rows.append(
            {
                "descriptor_sha256": digest,
                "edge_class_count": descriptor.edge_class_count,
                "reticulation_count": descriptor.retic_count,
                "parameter_count": 3 * descriptor.edge_class_count + descriptor.retic_count,
                **certificate,
            }
        )
        if ordinal and ordinal % 750 == 0:
            print(
                json.dumps(
                    {"rank_certificates": ordinal, "rank_total": len(descriptors_by_hash)},
                    sort_keys=True,
                ),
                flush=True,
            )
    return rows, by_hash


def sparse_hash(polynomial: dict[tuple[int, ...], object]) -> str:
    payload = [
        [list(exponents), str(coefficient)]
        for exponents, coefficient in sorted(polynomial.items())
    ]
    return object_sha256(payload)


def strict_witness(atlas, source_descriptor, salt: int) -> dict[str, Any]:
    edges, inheritance = atlas.default_exact_point(source_descriptor, salt=salt)
    margins = []
    for c, g, t in edges:
        margins.extend(
            (
                c,
                g,
                t,
                1 - c,
                1 - g,
                1 - t,
                1 + c - g - t,
                1 - c + g - t,
                1 - c - g + t,
                c - g * t,
                g - c * t,
                t - c * g,
            )
        )
    for value in inheritance:
        margins.extend((value, 1 - value))
    require(min(margins) > 0, "QUADRATIC_WITNESS_NOT_STRICT")
    return {
        "edge_triples": [[str(x) for x in row] for row in edges],
        "inheritance": [str(x) for x in inheritance],
        "minimum_margin": str(min(margins)),
    }


def evaluate_quadratic(atlas, descriptor, certificate, salt: int) -> Fraction:
    edges, inheritance = atlas.default_exact_point(descriptor, salt=salt)
    outputs = atlas.eval_descriptor(descriptor, edges, inheritance)
    value = Fraction(0)
    for pair, coefficient in zip(
        certificate["coordinate_pairs"], certificate["coefficients"]
    ):
        value += Fraction(coefficient) * outputs[pair[0]] * outputs[pair[1]]
    return value


def transported_h14_terms(
    atlas,
    omitted_port: int,
    retained_port_order: tuple[int, ...],
    character_permutation: tuple[int, ...],
) -> tuple[dict[str, Any], ...]:
    assignments = atlas.k3p_assignments(4)
    coordinate_index = {assignment: index for index, assignment in enumerate(assignments)}
    character_map = {0: 0, **{old: new for old, new in zip((1, 2, 3), character_permutation)}}
    symbols = "0CGT"
    rows = []
    for coefficient, coordinate_triples in H14_BASE_TERMS:
        indices = []
        labels = []
        for triple in coordinate_triples:
            assignment = [0, 0, 0, 0]
            require(assignment[omitted_port] == 0, "H14_OMITTED_INITIALIZATION_FAIL")
            for local_port, global_port in enumerate(retained_port_order):
                assignment[global_port] = character_map[triple[local_port]]
            assignment = tuple(assignment)
            require(assignment in coordinate_index, "H14_NONCONSERVING_TRANSPORT", assignment)
            indices.append(coordinate_index[assignment])
            labels.append("".join(symbols[value] for value in assignment))
        rows.append(
            {
                "coefficient": coefficient,
                "coordinate_indices": indices,
                "coordinate_labels": labels,
            }
        )
    return tuple(rows)


def quartic_pullback(atlas, descriptor, terms) -> dict[tuple[int, ...], Fraction]:
    outputs = atlas.output_sparse_polynomials_cached(descriptor)
    monomials = [
        atlas.sparse_mul_many([outputs[index] for index in term["coordinate_indices"]])
        for term in terms
    ]
    return atlas.sparse_lincomb(
        monomials, [term["coefficient"] for term in terms]
    )


def evaluate_quartic(atlas, descriptor, terms, salt: int) -> Fraction:
    edges, inheritance = atlas.default_exact_point(descriptor, salt=salt)
    outputs = atlas.eval_descriptor(descriptor, edges, inheritance)
    value = Fraction(0)
    for term in terms:
        monomial = Fraction(term["coefficient"])
        for index in term["coordinate_indices"]:
            monomial *= outputs[index]
        value += monomial
    return value


def transported_h14_separator(
    atlas,
    source_descriptor,
    target_descriptor,
    source_index: int,
    target_zero_cache: dict[str, tuple[tuple[object, ...], ...]],
) -> dict[str, Any] | None:
    """Find a literal target H_14 marginal identity nonzero on the source.

    This is used only after the coefficientwise syzygy upper is insufficient;
    it must never be used as a surrogate rank upper.  All target pullbacks are
    checked coefficientwise, and the selected source pullback is checked both
    coefficientwise and at a strict rational physical point.
    """
    target_digest = descriptor_sha256(target_descriptor)
    zero_charts = target_zero_cache.get(target_digest)
    if zero_charts is None:
        found = []
        ports = tuple(range(4))
        for omitted_port in ports:
            retained = tuple(port for port in ports if port != omitted_port)
            for retained_order in itertools.permutations(retained):
                for character_permutation in itertools.permutations((1, 2, 3)):
                    terms = transported_h14_terms(
                        atlas,
                        omitted_port,
                        retained_order,
                        character_permutation,
                    )
                    if not quartic_pullback(atlas, target_descriptor, terms):
                        found.append(
                            (
                                omitted_port,
                                retained_order,
                                character_permutation,
                                terms,
                            )
                        )
        zero_charts = tuple(found)
        target_zero_cache[target_digest] = zero_charts

    for omitted_port, retained_order, character_permutation, terms in zero_charts:
        source_pullback = quartic_pullback(atlas, source_descriptor, terms)
        if not source_pullback:
            continue
        source_evaluation = evaluate_quartic(
            atlas, source_descriptor, terms, salt=source_index
        )
        require(source_evaluation != 0, "H14_STRICT_EVALUATION_ZERO")
        return {
            "degree": 4,
            "base_identity": "normalized_three_leaf_H14_quartic",
            "omitted_port": omitted_port,
            "retained_port_order": list(retained_order),
            "character_permutation": list(character_permutation),
            "terms": list(terms),
            "target_pullback_term_count": 0,
            "source_pullback_term_count": len(source_pullback),
            "source_pullback_sha256": sparse_hash(source_pullback),
            "source_evaluation": str(source_evaluation),
            "strict_source_witness": strict_witness(
                atlas, source_descriptor, salt=source_index
            ),
        }
    return None


def classify_classes(
    atlas,
    sources,
    targets,
    compatible,
    source_descriptors,
    target_descriptors,
    rank_by_hash,
):
    class_rows = []
    raw_classification: dict[tuple[int, int, tuple[int, ...]], dict[str, Any]] = {}
    rank_excluded: list[set[tuple[int, tuple[int, ...]]]] = []
    source_rank_rows = []
    rank_upper_by_hash = {}
    h14_target_zero_cache: dict[str, tuple[tuple[object, ...], ...]] = {}

    for source_index, (source, source_descriptor, lane) in enumerate(
        zip(sources, source_descriptors, compatible)
    ):
        source_digest = descriptor_sha256(source_descriptor)
        source_rank = rank_by_hash[source_digest]
        source_rank_rows.append(source_rank)
        eligible: dict[object, list[tuple[int, int, tuple[int, ...]]]] = {}
        excluded = set()
        for target_index, permutation_index, permutation in lane:
            descriptor = target_descriptors[(target_index, permutation)]
            digest = descriptor_sha256(descriptor)
            if rank_by_hash[digest] < source_rank:
                upper = rank_upper_by_hash.get(digest)
                if upper is None:
                    upper = base_syzygy_rank_upper(atlas, descriptor)
                    upper["descriptor_sha256"] = digest
                    upper["point_minor_rank"] = rank_by_hash[digest]
                    rank_upper_by_hash[digest] = upper
                if upper["certified_rank_upper"] < source_rank:
                    excluded.add((target_index, permutation))
                    continue
            eligible.setdefault(descriptor, []).append(
                (target_index, permutation_index, permutation)
            )
        rank_excluded.append(excluded)

        for class_id, (target_descriptor, members) in enumerate(eligible.items()):
            target_digest = descriptor_sha256(target_descriptor)
            separator = atlas.quadratic_separator_fast(
                source_descriptor, target_descriptor, max_block_size=4
            )
            if separator is not None:
                source_pullback = separator.pop("source_pullback")
                certificate = {
                    "degree": 2,
                    "weight": list(separator["weight"]),
                    "coordinate_pairs": [list(pair) for pair in separator["coordinate_pairs"]],
                    "coefficients": [int(x) for x in separator["coefficients"]],
                    "source_nonzero_terms": int(separator["source_nonzero_terms"]),
                    "source_pullback_sha256": sparse_hash(source_pullback),
                    "strict_source_witness": strict_witness(
                        atlas, source_descriptor, salt=source_index
                    ),
                }
                source_evaluation = evaluate_quadratic(
                    atlas, source_descriptor, certificate, salt=source_index
                )
                require(source_evaluation != 0, "QUADRATIC_STRICT_EVALUATION_ZERO")
                certificate["source_evaluation"] = str(source_evaluation)
                class_category = "quadratic_separated"
            else:
                certificate = None
                class_category = "unresolved_after_quadratic"

            h14_certificate = None
            if (
                class_category == "unresolved_after_quadratic"
                and rank_by_hash[target_digest] < source_rank
            ):
                h14_certificate = transported_h14_separator(
                    atlas,
                    source_descriptor,
                    target_descriptor,
                    source_index,
                    h14_target_zero_cache,
                )
                if h14_certificate is not None:
                    class_category = "h14_marginal_separated"

            member_categories = collections.Counter()
            member_rows = []
            for target_index, permutation_index, permutation in members:
                relabelled = atlas.relabel_record(targets[target_index], permutation)
                selected_graph = atlas.selected_graph_from_completion(relabelled)
                relation = atlas.mixed_relation_exact(source.graph, selected_graph)
                require(relation in {"none", "isomorphic", "triangle"}, "GRAPH_RELATION_FAIL")
                has_dummy = bool(targets[target_index].dummy_labels)
                if class_category == "quadratic_separated":
                    category = class_category
                elif class_category == "h14_marginal_separated":
                    category = class_category
                elif relation == "isomorphic":
                    category = "isomorphic"
                elif relation == "triangle":
                    category = "ordinary_triangle"
                elif has_dummy:
                    category = "restoration_obligation"
                else:
                    category = "post_quadratic_residue"
                restoration_raw_id = None
                if category == "restoration_obligation":
                    # This primitive raw identity is the stable cross-package
                    # key.  Do not synthesize an active forest ``root_id``
                    # from this producer's K3P-local class ordinal: historical
                    # companion class ordinals differ for two source lanes.
                    # The independent verifier transports this raw identity
                    # through the frozen semantic crosswalk and then checks
                    # the active restoration/probe evidence row by row.
                    restoration_raw_id = (
                        source_index * RAW_PER_SOURCE
                        + target_index * PERMUTATION_COUNT
                        + permutation_index
                    )
                member_categories[category] += 1
                raw_key = (source_index, target_index, permutation)
                raw_classification[raw_key] = {
                    "category": category,
                    "class_id": class_id,
                    "target_descriptor_sha256": target_digest,
                    "target_rank": rank_by_hash[target_digest],
                    "graph_relation": relation,
                    "target_has_dummy_completion": has_dummy,
                    "restoration_raw_id": restoration_raw_id,
                }
                member_rows.append(
                    {
                        "target_index": target_index,
                        "permutation_index": permutation_index,
                        "port_permutation": list(permutation),
                        "category": category,
                        "graph_relation": relation,
                        "target_has_dummy_completion": has_dummy,
                        "restoration_raw_id": restoration_raw_id,
                        "target_graph_sha256": graph_sha256(relabelled.graph),
                        "selected_graph_sha256": graph_sha256(selected_graph),
                    }
                )
            class_rows.append(
                {
                    "source_index": source_index,
                    "class_id": class_id,
                    "source_descriptor_sha256": source_digest,
                    "source_rank": source_rank,
                    "target_descriptor_sha256": target_digest,
                    "target_rank": rank_by_hash[target_digest],
                    "raw_member_count": len(members),
                    "member_categories": dict(sorted(member_categories.items())),
                    "members": member_rows,
                    "quadratic_certificate": certificate,
                    "h14_marginal_certificate": h14_certificate,
                }
            )
        require(
            len(excluded) + sum(len(value) for value in eligible.values()) == len(lane),
            "RANK_ELIGIBLE_PARTITION_FAIL",
            source_index,
        )
    require(source_rank_rows == [20, 21, 21, 21, 23, 24], "SOURCE_RANK_CENSUS_FAIL", source_rank_rows)
    return class_rows, raw_classification, rank_excluded, rank_upper_by_hash


def compose_permutations(left, right):
    return tuple(left[right[index]] for index in range(4))


def mixed_automorphism_group(atlas, record, permutations):
    base = atlas.sd0_mixed(record.graph)
    group = []
    for permutation in permutations:
        relabelled = atlas.relabel_record(record, permutation)
        candidate = atlas.sd0_mixed(relabelled.graph)
        if atlas.mixed_exact_isomorphic(base, candidate):
            group.append(permutation)
    group = tuple(sorted(group))
    identity = (0, 1, 2, 3)
    require(identity in group, "AUTOMORPHISM_IDENTITY_MISSING")
    require(
        all(
            compose_permutations(first, second) in group
            for first in group
            for second in group
        ),
        "AUTOMORPHISM_GROUP_NOT_CLOSED",
    )
    return group


def double_coset(left_group, representative, right_group):
    return tuple(
        sorted(
            {
                compose_permutations(
                    left, compose_permutations(representative, right)
                )
                for left in left_group
                for right in right_group
            }
        )
    )


def derive_residue_quotient(
    atlas,
    sources,
    targets,
    permutations,
    source_descriptors,
    target_descriptors,
    rank_by_hash,
    raw_classification,
):
    identity = (0, 1, 2, 3)
    residue = sorted(
        (
            source_index,
            target_index,
            permutation,
            binding,
        )
        for (source_index, target_index, permutation), binding in raw_classification.items()
        if binding["category"] == "post_quadratic_residue"
    )
    require(len(residue) == 40, "POST_QUADRATIC_RESIDUE_CENSUS_FAIL", len(residue))
    by_pair: dict[tuple[int, int], set[tuple[int, ...]]] = collections.defaultdict(set)
    for source_index, target_index, permutation, _ in residue:
        by_pair[(source_index, target_index)].add(permutation)
    pair_sizes = sorted(len(value) for value in by_pair.values())
    require(pair_sizes == [2, 4, 4, 4, 4, 22], "RESIDUE_PAIR_CENSUS_FAIL", pair_sizes)

    h21_pair = next(pair for pair, members in by_pair.items() if len(members) == 22)
    sink_pair = next(pair for pair, members in by_pair.items() if len(members) == 2)
    lower_pairs = sorted(pair for pair, members in by_pair.items() if len(members) == 4)

    h_source, h_target = h21_pair
    source_group = mixed_automorphism_group(atlas, sources[h_source], permutations)
    target_group = mixed_automorphism_group(atlas, targets[h_target], permutations)
    remaining = set(by_pair[h21_pair])
    h_orbits = []
    while remaining:
        representative = min(remaining)
        orbit = set(double_coset(source_group, representative, target_group))
        require(orbit <= remaining, "H21_COSET_ESCAPES_RESIDUE", sorted(orbit - remaining))
        h_orbits.append(tuple(sorted(orbit)))
        remaining -= orbit
    require(len(h_orbits) == 6, "H21_ORBIT_CENSUS_FAIL", len(h_orbits))

    orbit_rows = []
    for index, members in enumerate(sorted(h_orbits), start=1):
        representative = min(members)
        target_descriptor = target_descriptors[(h_target, representative)]
        orbit_rows.append(
            {
                "orbit_id": f"H21-{index:02d}",
                "family": "rank21_nonautomorphic_relabelling",
                "source_index": h_source,
                "target_index": h_target,
                "source_rank": rank_by_hash[descriptor_sha256(source_descriptors[h_source])],
                "target_rank": rank_by_hash[descriptor_sha256(target_descriptor)],
                "representative_permutation": list(representative),
                "raw_members": [list(member) for member in members],
                "source_automorphism_group": [list(member) for member in source_group],
                "target_automorphism_group": [list(member) for member in target_group],
                "source_map_sha256": descriptor_sha256(source_descriptors[h_source]),
                "target_map_sha256": descriptor_sha256(target_descriptor),
            }
        )

    lower_name_counts = collections.Counter()
    for source_index, target_index in lower_pairs:
        target_group = mixed_automorphism_group(atlas, targets[target_index], permutations)
        remaining = set(by_pair[(source_index, target_index)])
        local_orbits = []
        while remaining:
            representative = min(remaining)
            orbit = set(double_coset((identity,), representative, target_group))
            require(
                orbit <= remaining,
                "LOWER_COSET_ESCAPES_RESIDUE",
                (source_index, sorted(orbit - remaining)),
            )
            local_orbits.append(tuple(sorted(orbit)))
            remaining -= orbit
        require(len(local_orbits) == 2, "LOWER_ORBIT_CENSUS_FAIL", source_index)
        rank = rank_by_hash[descriptor_sha256(source_descriptors[source_index])]
        if rank == 20:
            prefix = "L20"
        elif rank == 23:
            prefix = "L23"
        elif rank == 21:
            lower_name_counts[rank] += 1
            prefix = "L21a" if lower_name_counts[rank] == 1 else "L21b"
        else:
            fail("LOWER_SOURCE_RANK_LABEL_FAIL", (source_index, rank))
        for index, members in enumerate(sorted(local_orbits), start=1):
            representative = min(members)
            target_descriptor = target_descriptors[(target_index, representative)]
            orbit_rows.append(
                {
                    "orbit_id": f"{prefix}-{index:02d}",
                    "family": "lower_to_rank24",
                    "source_index": source_index,
                    "target_index": target_index,
                    "source_rank": rank,
                    "target_rank": rank_by_hash[descriptor_sha256(target_descriptor)],
                    "representative_permutation": list(representative),
                    "raw_members": [list(member) for member in members],
                    "source_automorphism_group": [list(identity)],
                    "target_automorphism_group": [list(member) for member in target_group],
                    "source_map_sha256": descriptor_sha256(source_descriptors[source_index]),
                    "target_map_sha256": descriptor_sha256(target_descriptor),
                }
            )

    require(len(orbit_rows) == 14, "CANONICAL_ORBIT_CENSUS_FAIL", len(orbit_rows))
    require(
        sum(len(row["raw_members"]) for row in orbit_rows) == 38,
        "ORBIT_RAW_MEMBER_CENSUS_FAIL",
    )
    sink_source, sink_target = sink_pair
    sink_rows = []
    for permutation in sorted(by_pair[sink_pair]):
        target_descriptor = target_descriptors[(sink_target, permutation)]
        sink_rows.append(
            {
                "source_index": sink_source,
                "target_index": sink_target,
                "port_permutation": list(permutation),
                "source_rank": rank_by_hash[descriptor_sha256(source_descriptors[sink_source])],
                "target_rank": rank_by_hash[descriptor_sha256(target_descriptor)],
                "source_map_sha256": descriptor_sha256(source_descriptors[sink_source]),
                "target_map_sha256": descriptor_sha256(target_descriptor),
            }
        )
    require(len(sink_rows) == 2, "SINK_SWAP_CENSUS_FAIL")
    return {
        "schema": "k3p-four-port-derived-residue-quotient-v2",
        "post_quadratic_raw_records": 40,
        "raw_records_in_fourteen_orbits": 38,
        "separate_sink_swap_records": 2,
        "canonical_orbits": 14,
        "orbits": sorted(orbit_rows, key=lambda row: row["orbit_id"]),
        "sink_swaps": sink_rows,
    }


def stream_raw_rows(
    atlas,
    sources,
    targets,
    permutations,
    target_signatures,
    source_descriptors,
    target_descriptors,
    rank_by_hash,
    raw_classification,
    rank_excluded,
    rank_upper_by_hash,
):
    for source_index, source in enumerate(sources):
        source_signature = atlas.topology_signature(source.graph)
        source_digest = descriptor_sha256(source_descriptors[source_index])
        source_rank = rank_by_hash[source_digest]
        for target_index, target_signature in enumerate(target_signatures):
            for permutation_index, permutation in enumerate(permutations):
                raw_id = (
                    source_index * RAW_PER_SOURCE
                    + target_index * PERMUTATION_COUNT
                    + permutation_index
                )
                accepted, reason = atlas.immediate_compatible(
                    source_signature,
                    atlas.permute_signature(target_signature, permutation),
                )
                base = {
                    "raw_id": raw_id,
                    "source_index": source_index,
                    "target_index": target_index,
                    "permutation_index": permutation_index,
                    "port_permutation": list(permutation),
                    "source_descriptor_sha256": source_digest,
                    "source_rank": source_rank,
                }
                if not accepted:
                    row = {
                        **base,
                        "category": "topology_excluded",
                        "topology_exclusion_reason": reason,
                    }
                elif (target_index, permutation) in rank_excluded[source_index]:
                    descriptor = target_descriptors[(target_index, permutation)]
                    digest = descriptor_sha256(descriptor)
                    row = {
                        **base,
                        "category": "rank_excluded",
                        "target_descriptor_sha256": digest,
                        "target_rank": rank_by_hash[digest],
                        "target_rank_upper": rank_upper_by_hash[digest][
                            "certified_rank_upper"
                        ],
                        "rank_upper_mechanism": rank_upper_by_hash[digest]["mechanism"],
                    }
                else:
                    binding = raw_classification.get((source_index, target_index, permutation))
                    require(binding is not None, "RAW_CLASSIFICATION_MISSING", raw_id)
                    row = {**base, **binding}
                yield canonical_bytes(row) + b"\n"


def main() -> None:
    if not __debug__:
        fail("OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=ARTIFACTS)
    parser.add_argument("--analysis-only", action="store_true")
    args = parser.parse_args()
    output_root = args.output_root.resolve()
    started = time.monotonic()

    atlas = load_atlas()
    sources, targets, permutations = primitive_universe(atlas)
    target_signatures, compatible, topology_reasons = topology_filter(
        atlas, sources, targets, permutations
    )
    source_descriptors, target_descriptors, descriptors_by_hash = compile_maps(
        atlas, sources, targets, compatible
    )
    rank_rows, rank_by_hash = rank_all(atlas, descriptors_by_hash)
    class_rows, raw_classification, rank_excluded, rank_upper_by_hash = classify_classes(
        atlas,
        sources,
        targets,
        compatible,
        source_descriptors,
        target_descriptors,
        rank_by_hash,
    )
    residue_quotient = derive_residue_quotient(
        atlas,
        sources,
        targets,
        permutations,
        source_descriptors,
        target_descriptors,
        rank_by_hash,
        raw_classification,
    )

    raw_category_counts = collections.Counter(
        binding["category"] for binding in raw_classification.values()
    )
    raw_category_counts["rank_excluded"] = sum(map(len, rank_excluded))
    raw_category_counts["topology_excluded"] = RAW_TOTAL - sum(map(len, compatible))
    class_category_counts = collections.Counter()
    for row in class_rows:
        categories = tuple(row["member_categories"])
        require(len(categories) == 1, "MIXED_CATEGORY_MAP_CLASS_FAIL", categories)
        class_category_counts[categories[0]] += 1

    summary = {
        "schema": "k3p-full-four-port-universe-replay-v2",
        "scope": {
            "starts_from_primitive_graph_grammar": True,
            "reads_frozen_fourteen_orbit_lock": False,
            "reads_frozen_companion_raw_ledger": False,
            "reads_missing_cloud_descriptor_corpus": False,
            "rank_note": "Exact nonzero Jacobian minors are regenerated for every literal map; target upper-rank binding is verified independently by the verifier.",
        },
        "bindings": {
            "atlas_path": "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py",
            "atlas_sha256": file_sha256(ATLAS_PATH),
            "producer_sha256": file_sha256(Path(__file__)),
        },
        "primitive_counts": {
            "sources": len(sources),
            "selected_incoming_targets": 831,
            "marginalized_incoming_targets": 1_983,
            "targets": len(targets),
            "port_permutations": len(permutations),
            "raw_total": RAW_TOTAL,
            "post_topology": sum(map(len, compatible)),
            "compatible_target_permutation_keys": len(target_descriptors),
            "unique_map_descriptors_including_sources": len(descriptors_by_hash),
        },
        "topology_reasons_by_source": [dict(sorted(row.items())) for row in topology_reasons],
        "raw_category_counts": dict(sorted(raw_category_counts.items())),
        "class_member_category_counts": dict(sorted(class_category_counts.items())),
        "eligible_map_class_count": len(class_rows),
        "rank_upper_certificate_count": len(rank_upper_by_hash),
        "rank_upper_mechanism": "coefficientwise multilinear polynomial vector fields J_f V=0",
        "source_ranks": [rank_by_hash[descriptor_sha256(row)] for row in source_descriptors],
        "residue_quotient": {
            "post_quadratic_raw_records": residue_quotient["post_quadratic_raw_records"],
            "raw_records_in_fourteen_orbits": residue_quotient[
                "raw_records_in_fourteen_orbits"
            ],
            "separate_sink_swap_records": residue_quotient["separate_sink_swap_records"],
            "canonical_orbits": residue_quotient["canonical_orbits"],
        },
    }

    if args.analysis_only:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return

    upper_artifact = deterministic_gzip(
        output_root / "exact_rank_upper_registry.json.gz",
        (
            canonical_bytes(
                {
                    "schema": "k3p-four-port-rank-upper-vector-fields-v2",
                    "records": [rank_upper_by_hash[key] for key in sorted(rank_upper_by_hash)],
                }
            ),
            b"\n",
        ),
    )
    quotient_artifact_path = output_root / "DERIVED_RESIDUE_QUOTIENT.json"
    atomic_json(quotient_artifact_path, residue_quotient)

    rank_artifact = deterministic_gzip(
        output_root / "exact_rank_minor_registry.json.gz",
        (canonical_bytes({"schema": "k3p-four-port-rank-minors-v2", "records": rank_rows}), b"\n"),
    )
    class_artifact = deterministic_gzip(
        output_root / "eligible_class_registry.json.gz",
        (
            canonical_bytes(
                {"schema": "k3p-four-port-eligible-classes-v2", "records": class_rows}
            ),
            b"\n",
        ),
    )
    ledger_artifact = deterministic_gzip(
        output_root / "full_directional_ledger.jsonl.gz",
        stream_raw_rows(
            atlas,
            sources,
            targets,
            permutations,
            target_signatures,
            source_descriptors,
            target_descriptors,
            rank_by_hash,
            raw_classification,
            rank_excluded,
            rank_upper_by_hash,
        ),
    )
    summary["artifacts"] = {
        "exact_rank_minor_registry.json.gz": rank_artifact,
        "exact_rank_upper_registry.json.gz": upper_artifact,
        "eligible_class_registry.json.gz": class_artifact,
        "full_directional_ledger.jsonl.gz": ledger_artifact,
        "DERIVED_RESIDUE_QUOTIENT.json": {
            "sha256": file_sha256(quotient_artifact_path),
            "bytes": quotient_artifact_path.stat().st_size,
        },
    }
    summary["payload_sha256_without_hash"] = object_sha256(summary)
    atomic_json(output_root / "FULL_FOUR_PORT_REPLAY.json", summary)
    print("K3P_FULL_FOUR_PORT_UNIVERSE_REGENERATION_PASS")
    print(json.dumps({"runtime_seconds": time.monotonic() - started}, sort_keys=True))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
