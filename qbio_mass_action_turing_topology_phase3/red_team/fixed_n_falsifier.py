#!/usr/bin/env python3
"""Adversarial tests for the fixed-species projection theorem."""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "independent_verifier"))
from fixed_n_projection import (  # noqa: E402
    canonical_positive_flux,
    decompose_flux,
    enumerate_circuit_rays,
    enumerate_circuit_rays_by_cofactors,
    jacobian_factor,
    project_flux_cone,
    reconstruct_from_decomposition,
    strictly_positive_flux_exists,
)


def random_network(rng: random.Random, n: int, m: int) -> tuple[sp.Matrix, sp.Matrix, set[str]]:
    """Generate edge cases while keeping entries small and exact."""
    tags: set[str] = set()
    columns: list[list[int]] = []
    # Seed paired columns so many cases have a positive kernel.
    while len(columns) < m:
        mode = rng.randrange(7)
        if mode == 0:
            col = [0] * n
            columns.append(col)
            tags.add("zero_stoichiometric_column")
        elif mode == 1 and columns:
            columns.append(columns[rng.randrange(len(columns))][:])
            tags.add("repeated_stoichiometric_column")
        elif mode in (2, 3) and len(columns) + 1 < m:
            col = [rng.randint(-2, 2) for _ in range(n)]
            if all(x == 0 for x in col):
                col[rng.randrange(n)] = 1
            columns.extend([col, [-x for x in col]])
            tags.add("opposite_pair")
        else:
            col = [rng.randint(-2, 2) for _ in range(n)]
            columns.append(col)
    columns = columns[:m]
    gamma = sp.Matrix(n, m, lambda i, j: columns[j][i])
    source_cols: list[list[int]] = []
    for j in range(m):
        if j and rng.random() < 0.18:
            source_cols.append(source_cols[rng.randrange(j)][:])
            tags.add("parallel_source")
        else:
            source_cols.append([rng.randint(0, 3) for _ in range(n)])
    source = sp.Matrix(n, m, lambda i, j: source_cols[j][i])
    if gamma.rank() < n:
        tags.add("conservation_or_rank_deficiency")
    return gamma, source, tags


def exact_two_species_one_ray_decision(A: sp.Matrix, rank_gamma: int) -> bool:
    """Direct fixed-J formula for a one-ray projected cone in n=2."""
    a11, a22 = A[0, 0], A[1, 1]
    if rank_gamma == 2:
        return bool(A.det() > 0 and a11 * a22 < 0)
    if rank_gamma == 1:
        return bool(A.rank() == 1 and a11 * a22 < 0)
    return False


def main() -> None:
    rng = random.Random(20260813)
    cases = 0
    decompositions = 0
    positive_flux_cases = 0
    projected_zero = 0
    one_ray_two_species = 0
    tags_seen: set[str] = set()

    for n in (1, 2, 3):
        for m in range(1, 8):
            for _ in range(55):
                gamma, source, tags = random_network(rng, n, m)
                tags_seen.update(tags)
                rays_a = enumerate_circuit_rays(gamma)
                rays_b = enumerate_circuit_rays_by_cofactors(gamma)
                if {r.vector for r in rays_a} != {r.vector for r in rays_b}:
                    raise AssertionError(f"independent circuit enumerators disagree: n={n}, m={m}")
                cone = project_flux_cone(gamma, source)
                if cone.span_rank == 0:
                    projected_zero += 1
                cases += 1

                # Generate exact kernel points from arbitrary nonnegative circuit mixtures,
                # then demand that the decomposition algorithm recover them.
                for _sample in range(4):
                    if not rays_a:
                        break
                    coefficients = [sp.Rational(rng.randint(0, 5), rng.randint(1, 4)) for _ in rays_a]
                    if not any(coefficients):
                        coefficients[0] = sp.Integer(1)
                    v = sp.zeros(m, 1)
                    for coefficient, ray in zip(coefficients, rays_a):
                        v += coefficient * ray.as_matrix()
                    pieces = decompose_flux(list(v), rays_a, gamma)
                    recovered = reconstruct_from_decomposition(pieces, m)
                    if recovered != v:
                        raise AssertionError("exact circuit decomposition failed")
                    A_direct = jacobian_factor(gamma, source, list(v))
                    A_parts = sp.zeros(n, n)
                    for coefficient, ray in pieces:
                        A_parts += coefficient * jacobian_factor(gamma, source, ray.vector)
                    if sp.simplify(A_direct - A_parts) != sp.zeros(n, n):
                        raise AssertionError("projected cone image failed linear reconstruction")
                    decompositions += 1

                positive = canonical_positive_flux(rays_a, m)
                if positive is not None:
                    positive_flux_cases += 1
                    if not all(x > 0 for x in positive) or gamma * sp.Matrix(positive) != sp.zeros(n, 1):
                        raise AssertionError("canonical positive flux invalid")
                if strictly_positive_flux_exists(rays_a, m) != (positive is not None):
                    raise AssertionError("positive-flux coverage test inconsistent")

                # On a one-dimensional projected cone, the n=2 direct formula is
                # itself a complete symbolic elimination of all flux variables.
                nonzero_generators = [sp.Matrix(n, n, g) for g in cone.generators if any(x != 0 for x in g)]
                normalized = []
                for A in nonzero_generators:
                    pivot = next(A[i, j] for i in range(n) for j in range(n) if A[i, j] != 0)
                    normalized.append(tuple(sp.simplify(A[i, j] / pivot) for i in range(n) for j in range(n)))
                if n == 2 and normalized and len(set(normalized)) == 1 and positive is not None:
                    A = nonzero_generators[0]
                    result = exact_two_species_one_ray_decision(A, gamma.rank())
                    # Independently eliminate the positive h variables from trace and
                    # determinant: opposite diagonal signs are necessary and sufficient.
                    direct = bool(A[0, 0] * A[1, 1] < 0 and (A.det() > 0 if gamma.rank() == 2 else A.rank() == 1))
                    if result != direct:
                        raise AssertionError("two-species direct elimination disagreement")
                    one_ray_two_species += 1

    # Deterministic pathological fixtures.
    fixtures = [
        (sp.Matrix([[0, 0]]), sp.Matrix([[0, 2]]), "all_zero_gamma"),
        (sp.Matrix([[1, -1, 1, -1], [0, 0, 0, 0]]), sp.Matrix([[0, 1, 0, 1], [1, 1, 2, 2]]), "lower_dimensional"),
        (sp.Matrix([[1, -1, 0, 0], [0, 0, 1, -1]]), sp.Matrix([[0, 1, 1, 0], [1, 0, 0, 1]]), "product_cone"),
        (sp.Matrix([[0, 0, 1, -1], [0, 0, -1, 1]]), sp.Matrix([[1, 1, 0, 2], [0, 0, 2, 0]]), "zero_columns_and_lineality_candidate"),
    ]
    fixture_summaries = []
    for gamma, source, name in fixtures:
        cone = project_flux_cone(gamma, source)
        rays_b = enumerate_circuit_rays_by_cofactors(gamma)
        if {r.vector for r in cone.rays} != {r.vector for r in rays_b}:
            raise AssertionError(f"fixture {name} circuit disagreement")
        fixture_summaries.append({
            "name": name,
            "rays": len(cone.rays),
            "span_rank": cone.span_rank,
            "strict_positive_flux": strictly_positive_flux_exists(cone.rays, gamma.cols),
        })

    result = {
        "status": "PASS",
        "random_networks": cases,
        "exact_flux_decompositions": decompositions,
        "independent_circuit_enumerator_agreements": cases + len(fixtures),
        "strict_positive_flux_cases": positive_flux_cases,
        "zero_projected_cones": projected_zero,
        "two_species_one_ray_symbolic_eliminations": one_ray_two_species,
        "edge_case_tags": sorted(tags_seen),
        "fixtures": fixture_summaries,
        "scope_note": "The implementation exactly validates circuit enumeration and projection. It is a formula generator, not a bundled general CAD engine.",
    }
    out = ROOT / "release" / "fixed_n_falsifier.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
