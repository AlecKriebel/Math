#!/usr/bin/env python3
"""Independent exact anchors for Paper A; does not import the release implementation."""

from __future__ import annotations

import hashlib
import json
from itertools import product
from pathlib import Path

import sympy as sp

import mutants


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
CASES_PATH = HERE / "cases.json"


def rat(value) -> sp.Rational:
    return sp.Rational(str(value))


def matrix(values: list[list[str]]) -> sp.Matrix:
    return sp.Matrix([[rat(value) for value in row] for row in values])


def assert_zero(value, label: str) -> None:
    if isinstance(value, sp.MatrixBase):
        simplified = value.applyfunc(sp.simplify)
        is_zero = simplified == sp.zeros(*simplified.shape)
    else:
        simplified = sp.simplify(value)
        is_zero = simplified == 0
    if not is_zero:
        raise AssertionError(f"{label}: expected zero, got {simplified}")


def require(condition, label: str) -> None:
    """Enforce a verifier condition even when Python assertions are optimized out."""
    if not condition:
        raise AssertionError(label)


def check_pair_generators(cases: dict) -> dict:
    s = sp.symbols("s", positive=True)
    names = []
    for case in cases["pair_generators"]:
        q = matrix(case["generator"])
        pi = sp.Matrix([[rat(value) for value in case["stationary"]]])
        d_pi = sp.diag(*list(pi))
        require(q.trace() == -1, f"{case['name']} trace normalization")
        assert_zero(q * sp.ones(q.rows, 1), f"{case['name']} row sums")
        assert_zero(pi * q, f"{case['name']} stationarity")
        assert_zero(d_pi * q - q.T * d_pi, f"{case['name']} reversibility")
        transition = (q * s).exp()
        assert_zero(
            transition.diff(s) * transition.inv() - q,
            f"{case['name']} generator",
        )
        assert_zero(transition.det() - sp.exp(-s), f"{case['name']} determinant")
        joint = d_pi * transition
        assert_zero(
            d_pi.inv() * joint - transition,
            f"{case['name']} stationary scaling",
        )
        if "repeated" in case["name"]:
            multiplicities = q.eigenvals()
            require(
                max(multiplicities.values()) >= 2,
                f"{case['name']} repeated eigenvalue",
            )
        names.append(case["name"])
    return {"cases": names, "count": len(names)}


def check_tensor_mixture(cases: dict) -> dict:
    case = cases["tensor_mixture"]
    atoms = [[rat(value) for value in atom] for atom in case["atoms"]]
    weights = [rat(value) for value in case["weights"]]
    require(sum(weights) == 1, "tensor mixture weights sum to one")

    def word_probability(length: int, zeros: int) -> sp.Expr:
        return sp.simplify(
            sum(
                weight * atom[0] ** zeros * atom[1] ** (length - zeros)
                for weight, atom in zip(weights, atoms)
            )
        )

    for length in range(1, 5):
        for zeros in range(length + 1):
            assert_zero(
                word_probability(length, zeros)
                - word_probability(length + 1, zeros)
                - word_probability(length + 1, zeros + 1),
                f"moment marginalization L={length} zeros={zeros}",
            )
        all_zero = word_probability(length, length)
        direct_moment = sum(
            weight * atom[0] ** length for weight, atom in zip(weights, atoms)
        )
        assert_zero(all_zero - direct_moment, f"all-zero moment L={length}")
    return {"checked_lengths": [1, 2, 3, 4]}


def check_ultrametric(cases: dict) -> dict:
    case = cases["ultrametric_tree"]
    labels = case["labels"]
    distances = matrix(case["distances"])
    n = len(labels)
    for i in range(n):
        require(distances[i, i] == 0, f"ultrametric diagonal {i}")
        for j in range(n):
            require(
                distances[i, j] == distances[j, i],
                f"ultrametric symmetry {i},{j}",
            )
            for k in range(n):
                require(
                    distances[i, j]
                    <= max(distances[i, k], distances[k, j]),
                    f"ultrametric inequality {i},{j},{k}",
                )

    levels = sorted(
        {
            distances[i, j] / 2
            for i in range(n)
            for j in range(i + 1, n)
        }
    )
    clusters: set[tuple[str, ...]] = set()
    for level in levels:
        unused = set(range(n))
        while unused:
            seed = min(unused)
            component = {
                index
                for index in unused
                if distances[seed, index] / 2 <= level
            }
            changed = True
            while changed:
                changed = False
                for index in list(unused - component):
                    if any(
                        distances[index, member] / 2 <= level
                        for member in component
                    ):
                        component.add(index)
                        changed = True
            unused -= component
            if len(component) > 1:
                clusters.add(
                    tuple(labels[index] for index in sorted(component))
                )
    expected = {tuple(cluster) for cluster in case["expected_clusters"]}
    require(clusters == expected, "ultrametric cluster reconstruction")
    root_height = max(distances) / 2
    require(
        root_height == rat(case["root_height"]),
        "ultrametric root height",
    )
    return {
        "clusters": [list(cluster) for cluster in sorted(clusters)],
        "root_height": str(root_height),
    }


def check_hazard(cases: dict) -> dict:
    case = cases["hazard_schedule"]
    breakpoints = [rat(value) for value in case["breakpoints"]]
    rates = [rat(value) for value in case["rates"]]
    threshold = rat(case["support_threshold"])
    require(breakpoints[0] == threshold, "hazard support threshold")

    def cumulative_hazard(time: sp.Rational) -> sp.Expr:
        if time <= threshold:
            return sp.Integer(0)
        total = sp.Integer(0)
        starts = breakpoints
        ends = [*breakpoints[1:], None]
        for start, end, rate in zip(starts, ends, rates):
            if time <= start:
                break
            duration = (
                time - start if end is None else min(time, end) - start
            )
            if duration > 0:
                total += rate * duration
            if end is not None and time <= end:
                break
        return sp.simplify(total)

    probes = [(rat("3/2"), 0), (rat("3"), 1), (rat("5"), 2)]
    recovered = []
    for time, index in probes:
        epsilon = rat("1/10")
        local_rate = sp.simplify(
            (
                cumulative_hazard(time + epsilon)
                - cumulative_hazard(time - epsilon)
            )
            / (2 * epsilon)
        )
        require(local_rate == rates[index], f"hazard rate probe {index}")
        recovered.append(str(local_rate))
    symbolic_rate = sp.symbols("lambda", positive=True)
    require(
        sp.binomial(1, 2) * symbolic_rate == 0,
        "single lineage has zero Kingman pair hazard",
    )
    return {
        "recovered_rates": recovered,
        "support_threshold": str(threshold),
    }


def check_finite_jets(cases: dict) -> dict:
    case = cases["finite_jet_case"]
    before = matrix(case["generator_before"])
    after = matrix(case["generator_after"])
    mark = matrix(case["mark"])
    left = sp.Matrix([[rat(value) for value in case["left"]]])
    right = sp.Matrix([rat(value) for value in case["right"]])
    s = sp.symbols("s", real=True)
    response = sp.simplify(
        (left * (before * s).exp() * mark * (-after * s).exp() * right)[0]
    )

    basis = []
    for row in range(mark.rows):
        for column in range(mark.cols):
            elementary = sp.zeros(mark.rows, mark.cols)
            elementary[row, column] = 1
            image = before * elementary - elementary * after
            basis.append(sp.Matrix(image).reshape(mark.rows * mark.cols, 1))
    sylvester = sp.Matrix.hstack(*basis)
    coefficients = sylvester.charpoly().all_coeffs()
    order = len(coefficients) - 1
    recurrence = sp.diff(response, s, order)
    for index, coefficient in enumerate(coefficients[1:], start=1):
        recurrence += coefficient * sp.diff(response, s, order - index)
    assert_zero(recurrence, "Sylvester finite-jet recurrence")

    prefix_case = cases["fixed_cut_prefix_case"]
    generator = matrix(prefix_case["generator"])
    routed = sp.Matrix([[rat(value) for value in prefix_case["routed_row"]]])
    fixed_cut_rank = routed.rank()
    unrestricted = sp.Matrix.vstack(
        routed,
        routed * generator,
        routed * generator**2,
        routed * generator**3,
    ).rank()
    require(fixed_cut_rank == 1, "fixed-cut prefix rank")
    require(unrestricted == 3, "unrestricted generator-power rank")
    return {
        "jet_recurrence_order": order,
        "fixed_cut_prefix_rank": fixed_cut_rank,
        "unrestricted_power_rank": unrestricted,
        "unrestricted_prefix_closure_rejected": True,
    }


def check_observable_cocycle(cases: dict) -> dict:
    """Recompute the law-only separator anchors without release imports."""
    case = cases["observable_cocycle"]
    segments = [tuple(rat(value) for value in row) for row in case["rate_segments"]]
    start = rat(case["start"])
    boundary = rat(case["boundary"])
    end = rat(case["end"])
    merger_time = rat(case["merger_time"])
    initial_blocks = int(case["initial_blocks"])

    def rate_integral(a: sp.Expr, b: sp.Expr, word) -> sp.Expr:
        total = sp.Integer(0)
        covered = sp.Integer(0)
        for left, right, rate in word:
            overlap_left = max(a, left)
            overlap_right = min(b, right)
            if overlap_right > overlap_left:
                width = overlap_right - overlap_left
                total += rate * width
                covered += width
        assert_zero(covered - (b - a), "cocycle rate-word coverage")
        return sp.simplify(total)

    def local_rate(time: sp.Expr, word) -> sp.Expr:
        matches = [rate for left, right, rate in word if left <= time < right]
        require(len(matches) == 1, "unique rate at labelled merger time")
        return matches[0]

    def word_density(
        a: sp.Expr,
        b: sp.Expr,
        merger_times: list[sp.Expr],
        blocks: int,
        word,
    ) -> sp.Expr:
        density = sp.Integer(1)
        previous = a
        current_blocks = blocks
        for event_time in [*merger_times, b]:
            density *= sp.exp(
                -sp.binomial(current_blocks, 2)
                * rate_integral(previous, event_time, word)
            )
            if event_time != b:
                density *= local_rate(event_time, word)
                current_blocks -= 1
            previous = event_time
        return sp.simplify(density)

    empty_left = word_density(start, boundary, [], initial_blocks, segments)
    empty_right = word_density(boundary, end, [], initial_blocks, segments)
    empty_spanning = word_density(start, end, [], initial_blocks, segments)
    assert_zero(
        empty_spanning - empty_left * empty_right,
        "empty-word spanning cocycle",
    )

    labelled_left = word_density(
        start, boundary, [merger_time], initial_blocks, segments
    )
    labelled_right = word_density(
        boundary, end, [], initial_blocks - 1, segments
    )
    labelled_spanning = word_density(
        start, end, [merger_time], initial_blocks, segments
    )
    assert_zero(
        labelled_spanning - labelled_left * labelled_right,
        "labelled-word spanning cocycle",
    )
    require(
        segments[0][2] != segments[1][2],
        "manifest must exercise an unequal demographic rate jump",
    )

    equal_split = [(rat("0"), rat("2"), rat("2")),
                   (rat("2"), rat("5"), rat("2"))]
    equal_merged = [(rat("0"), rat("5"), rat("2"))]
    equal_split_density = word_density(
        rat("0"), rat("5"), [rat("1"), rat("3")], 4, equal_split
    )
    equal_merged_density = word_density(
        rat("0"), rat("5"), [rat("1"), rat("3")], 4, equal_merged
    )
    assert_zero(
        equal_split_density - equal_merged_density,
        "equal-rate epoch composition",
    )

    beta_12 = sp.Matrix([[rat(value) for value in case["future_after_12"]]])
    beta_13 = sp.Matrix([[rat(value) for value in case["future_after_13"]]])
    entry_12 = sp.Matrix([rat(value) for value in case["entry_after_12"]])
    entry_13 = sp.Matrix([rat(value) for value in case["entry_after_13"]])
    kernel_12 = entry_12 * beta_12
    kernel_13 = entry_13 * beta_13
    require(kernel_12.rank() == 1, "first one-sided kernel rank")
    require(kernel_13.rank() == 1, "second one-sided kernel rank")
    require(sum(beta_12) == 1, "first all-completions normalization")
    require(sum(beta_13) == 1, "second all-completions normalization")
    assert_zero(kernel_12 * sp.ones(2, 1) - entry_12, "first entry masses")
    assert_zero(kernel_13 * sp.ones(2, 1) - entry_13, "second entry masses")

    joint_entry_table = sp.Matrix([[rat("2"), rat("3")], [rat("5"), rat("7")]])
    require(
        joint_entry_table.rank() == 2,
        "joint multi-cut entry mass need not factor by incident port",
    )
    joint_entry = sp.Matrix(list(joint_entry_table))
    joint_kernel = joint_entry * beta_12
    require(joint_kernel.rank() == 1, "joint multi-cut kernel rank")
    assert_zero(
        joint_kernel * sp.ones(beta_12.cols, 1) - joint_entry,
        "joint multi-cut all-completions entry mass",
    )

    labelled_word_mass = rat(case["labelled_word_mass"])
    reset_residual = labelled_word_mass * (beta_13 - beta_12)
    require(
        reset_residual != sp.zeros(1, 2),
        "labelled continuation columns detect the role reset",
    )
    assert_zero(sum(reset_residual), "role reset preserves all-completions mass")

    minor = case["private_minor"]
    gamma = rat(minor["gamma"])
    rate = rat(minor["rate"])
    exp_u_1 = rat(minor["exp_u1"])
    exp_u_2 = rat(minor["exp_u2"])
    exp_D = rat(minor["exp_D"])
    exp_delta = rat(minor["exp_delta"])

    def split_mass(exp_u: sp.Expr) -> sp.Expr:
        return gamma * (1 - gamma) * rate * exp_u

    def cooccupied_mass(exp_u: sp.Expr) -> sp.Expr:
        return gamma**2 * rate * exp_D * exp_u**2

    fixed_cut_minor = sp.simplify(
        (1 - exp_delta)
        * (
            cooccupied_mass(exp_u_1) * split_mass(exp_u_2)
            - cooccupied_mass(exp_u_2) * split_mass(exp_u_1)
        )
    )
    require(fixed_cut_minor > 0, "private-side fixed-cut rank minor")

    return {
        "all_completions_gauge_canonical": True,
        "empty_word_spans_rate_jump": True,
        "equal_rate_epochs_compose": True,
        "labelled_word_spans_rate_jump": True,
        "joint_entry_need_not_factor_by_port": True,
        "one_sided_rank_is_insufficient": True,
        "private_side_minor": str(fixed_cut_minor),
        "role_reset_residual": [str(value) for value in reset_residual],
    }


def check_routing(cases: dict) -> dict:
    case = cases["routing_case"]
    gamma, gamma_prime, eta = sp.symbols("gamma gamma_prime eta")
    parent_1 = sp.Matrix([rat(value) for value in case["parent_1"]])
    parent_2 = sp.Matrix([rat(value) for value in case["parent_2"]])
    affine = gamma * parent_1 + (1 - gamma) * parent_2
    affine_prime = gamma_prime * parent_1 + (1 - gamma_prime) * parent_2
    difference = (affine - affine_prime).applyfunc(sp.factor)
    require(difference != sp.zeros(2, 1), "affine parent futures differ")
    require(
        all(
            sp.factor(entry / (gamma - gamma_prime)) != 0
            for entry in difference
            if entry != 0
        ),
        "affine inheritance coefficient",
    )

    route_sum = sp.expand(
        (gamma + (1 - gamma)) * (eta + (1 - eta))
    )
    require(route_sum == 1, "independent two-block route sum")

    split_mass = sp.expand(2 * gamma * (1 - gamma))
    inheritance_polynomial = sp.expand(
        2 * eta**2 - 2 * eta + split_mass
    )
    assert_zero(
        inheritance_polynomial.subs(eta, gamma),
        "pair-germ inheritance root gamma",
    )
    assert_zero(
        inheritance_polynomial.subs(eta, 1 - gamma),
        "pair-germ inheritance root complement",
    )

    singular = gamma**2 + (1 - gamma) ** 2
    require(
        sp.diff(singular, gamma).subs(gamma, rat("1/2")) == 0,
        "singular inheritance derivative",
    )
    assert_zero(
        singular
        - singular.subs(gamma, rat("1/2"))
        - 2 * (gamma - rat("1/2")) ** 2,
        "singular routing fiber",
    )
    return {
        "affine_gamma_identifiable": True,
        "pair_germ_gamma_identifiable_mod_exchange": True,
        "singular_tangent_witness": True,
    }


def check_balance_switch(cases: dict) -> dict:
    case = cases["balance_switch"]
    gamma = rat(case["gamma"])
    boundary = rat(case["boundary_exponential"])
    first_1, first_2 = [rat(value) for value in case["first_rates"]]
    suffix_1, suffix_2 = [rat(value) for value in case["suffix_rates"]]
    suffix_boundary = rat(case["suffix_exponential"])
    require(
        set(case["sampling"].values()) == {"A", "B"},
        "sampled-complete taxon image",
    )
    require(
        case["sampling"]["x"] == case["sampling"]["y"],
        "two child samples share taxon A",
    )
    require(
        all(rat(rate) > 0 for rate in case["common_rates"].values()),
        "strict common rates",
    )
    times = {
        name: rat(value)
        for name, value in case["times_in_log2_units"].items()
    }
    require(
        0 < times["h"] < times["switch"] < times["reconvergence"],
        "strict arm time order",
    )
    require(
        times["reconvergence"] < times["z_join"],
        "outside taxon joins after arm reconvergence",
    )
    require(
        boundary == sp.Integer(2) ** (-(times["switch"] - times["h"])),
        "first chamber exponential",
    )
    require(
        suffix_boundary
        == sp.Integer(2) ** (-(times["reconvergence"] - times["switch"])),
        "suffix chamber exponential",
    )
    graph = case["graph"]
    vertices = {vertex["id"]: vertex for vertex in graph["vertices"]}
    require(len(vertices) == len(graph["vertices"]), "unique graph vertex ids")
    graph_times = {
        identifier: rat(vertex["time"])
        for identifier, vertex in vertices.items()
    }
    edges = [tuple(edge) for edge in graph["edges"]]
    require(len(edges) == len(set(edges)), "unique graph edges")
    require(
        all(source in vertices and target in vertices for source, target in edges),
        "graph edge endpoints exist",
    )
    require(
        all(graph_times[source] < graph_times[target] for source, target in edges),
        "graph edges increase in time",
    )
    outgoing = {identifier: [] for identifier in vertices}
    incoming = {identifier: [] for identifier in vertices}
    for source, target in edges:
        outgoing[source].append(target)
        incoming[target].append(source)
    require(max(map(len, outgoing.values())) <= 2, "binary outdegree")
    require(max(map(len, incoming.values())) <= 2, "binary indegree")
    leaves = sorted(
        identifier
        for identifier in vertices
        if not incoming[identifier]
    )
    require(
        leaves == sorted(set(case["sampling"].values())),
        "graph leaves equal sampled taxa",
    )
    reticulations = [
        identifier
        for identifier, vertex in vertices.items()
        if vertex["kind"] == "reticulation"
    ]
    require(reticulations == ["h"], "one reticulation vertex")
    require(
        len(incoming["h"]) == 1 and len(outgoing["h"]) == 2,
        "backward-time reticulation degree",
    )
    require(graph_times["h"] == times["h"], "reticulation time")
    require(
        graph_times["u"] == times["reconvergence"],
        "reconvergence time",
    )
    for identifier, vertex in vertices.items():
        if vertex["kind"] == "demographic":
            require(
                len(incoming[identifier]) == len(outgoing[identifier]) == 1,
                f"demographic vertex degree {identifier}",
            )
        if vertex["kind"] == "root":
            require(len(incoming[identifier]) == 1, "root indegree")
            require(not outgoing[identifier], "root outdegree")

    arm_paths = [tuple(path) for path in graph["arm_paths"]]
    require(len(arm_paths) == 2, "two reticulation arms")
    require(
        all(path[0] == "h" and path[-1] == "u" for path in arm_paths),
        "arm endpoints",
    )
    require(
        set(arm_paths[0][1:-1]).isdisjoint(arm_paths[1][1:-1]),
        "internally disjoint arms",
    )
    for path in arm_paths:
        require(
            all(edge in edges for edge in zip(path, path[1:])),
            f"declared arm edges {path}",
        )

    def ancestors(start: str) -> set[str]:
        reached = {start}
        frontier = [start]
        while frontier:
            current = frontier.pop()
            for target in outgoing[current]:
                if target not in reached:
                    reached.add(target)
                    frontier.append(target)
        return reached

    b_ancestors = ancestors("B")
    arm_interiors = set(arm_paths[0][1:-1]) | set(arm_paths[1][1:-1])
    require(b_ancestors.isdisjoint(arm_interiors), "side-free B ancestry")
    first_common_ab = min(
        ancestors("A") & b_ancestors,
        key=lambda identifier: graph_times[identifier],
    )
    require(first_common_ab == "j", "first A-B common ancestor")
    require(
        graph_times[first_common_ab] > graph_times["u"],
        "A-B meet after arm reconvergence",
    )

    one_block_route_sum = sp.simplify(gamma + (1 - gamma))
    two_block_route_sum = sp.expand(
        gamma**2 + 2 * gamma * (1 - gamma) + (1 - gamma) ** 2
    )
    require(
        one_block_route_sum == two_block_route_sum == 1,
        "all routing probabilities sum to one",
    )
    weight_1 = sp.simplify(gamma**2 * boundary**first_1)
    weight_2 = sp.simplify((1 - gamma) ** 2 * boundary**first_2)
    require(weight_1 == weight_2 == rat("1/36"), "posterior balance")

    x, y = sp.symbols("x y", positive=True)
    split = 2 * gamma * (1 - gamma)
    survival = sp.expand(
        split + weight_1 * x**suffix_1 + weight_2 * x**suffix_2
    )
    swapped_survival = sp.expand(
        split + weight_1 * x**suffix_2 + weight_2 * x**suffix_1
    )
    density = sp.expand(
        weight_1 * suffix_1 * x**suffix_1
        + weight_2 * suffix_2 * x**suffix_2
    )
    swapped_density = sp.expand(
        weight_1 * suffix_2 * x**suffix_2
        + weight_2 * suffix_1 * x**suffix_1
    )
    assert_zero(survival - swapped_survival, "balanced survival")
    assert_zero(density - swapped_density, "balanced merger density")

    first_survival = (
        2 * gamma * (1 - gamma)
        + gamma**2 * x**first_1
        + (1 - gamma) ** 2 * x**first_2
    )
    first_density = (
        gamma**2 * first_1 * x**first_1
        + (1 - gamma) ** 2 * first_2 * x**first_2
    )
    assert_zero(
        first_survival
        - (rat("4/9") + rat("1/9") * x + rat("4/9") * x**2),
        "first-chamber survival",
    )
    assert_zero(
        first_density
        - (rat("1/9") * x + rat("8/9") * x**2),
        "first-chamber density",
    )
    mass_at_switch = sp.simplify(split + weight_1 + weight_2)
    mass_at_reconvergence = sp.simplify(
        split
        + weight_1 * suffix_boundary**suffix_1
        + weight_2 * suffix_boundary**suffix_2
    )
    suffix_merger_mass = sp.simplify(
        weight_1 * (1 - suffix_boundary**suffix_1)
        + weight_2 * (1 - suffix_boundary**suffix_2)
    )
    require(mass_at_switch == rat("1/2"), "mass at switch")
    require(
        mass_at_reconvergence == rat("259/576"),
        "mass at reconvergence",
    )
    require(suffix_merger_mass == rat("29/576"), "suffix merger mass")
    require(
        mass_at_reconvergence + suffix_merger_mass == mass_at_switch,
        "suffix mass conservation",
    )

    two_block_row = sp.Matrix([[
        weight_1,
        gamma * (1 - gamma),
        gamma * (1 - gamma),
        weight_2,
    ]])
    two_block_exchange = sp.Matrix([
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
    ])
    assert_zero(
        two_block_row * (two_block_exchange - sp.eye(4)),
        "two-block all-future balanced row",
    )
    completion = sp.symbols("completion")
    one_block_exchange = sp.Matrix([[0, 1], [1, 0]])
    one_block_future = sp.Matrix([completion, completion])
    assert_zero(
        (one_block_exchange - sp.eye(2)) * one_block_future,
        "one-block side-free future invariance",
    )

    schedules = {
        name: [tuple(rat(value) for value in word) for word in words]
        for name, words in case["arm_schedules"].items()
    }

    def routing_probability(assignment: tuple[int, ...]) -> sp.Expr:
        return sp.prod(
            gamma if parent == 0 else 1 - gamma
            for parent in assignment
        )

    def enumerate_local_kernel(model: str) -> dict[str, sp.Expr]:
        words_for_model = schedules[model]
        one_block_output = sp.Integer(0)
        for assignment in product((0, 1), repeat=1):
            one_block_output += routing_probability(assignment)

        first_chamber_density = sp.Integer(0)
        suffix_chamber_density = sp.Integer(0)
        two_block_output = sp.Integer(0)
        for assignment in product((0, 1), repeat=2):
            probability = routing_probability(assignment)
            if assignment[0] != assignment[1]:
                two_block_output += probability
                continue
            parent = assignment[0]
            first_rate, suffix_rate = words_for_model[parent]
            first_chamber_density += probability * first_rate * x**first_rate
            posterior = probability * boundary**first_rate
            suffix_chamber_density += (
                posterior * suffix_rate * y**suffix_rate
            )
            two_block_output += (
                posterior * suffix_boundary**suffix_rate
            )
        return {
            "one_block_output": sp.expand(one_block_output),
            "two_block_first_density": sp.expand(first_chamber_density),
            "two_block_suffix_density": sp.expand(suffix_chamber_density),
            "two_block_output": sp.expand(two_block_output),
        }

    kernel_n = enumerate_local_kernel("N")
    kernel_n_prime = enumerate_local_kernel("N_prime")
    require(kernel_n.keys() == kernel_n_prime.keys(), "kernel output keys")
    for key in kernel_n:
        assert_zero(
            kernel_n[key] - kernel_n_prime[key],
            f"all-partition local kernel {key}",
        )
    require(kernel_n["one_block_output"] == 1, "one-block output mass")
    require(
        kernel_n["two_block_output"] == mass_at_reconvergence,
        "two-block output mass",
    )

    words = schedules["N"]
    swapped_words = schedules["N_prime"]
    require(
        all(
            [words[index] for index in permutation] != swapped_words
            for permutation in ((0, 1), (1, 0))
        ),
        "parent words are not globally exchange equivalent",
    )
    require(
        not mutants.balanced_switch_requires_equal_suffixes(
            x**suffix_1, x**suffix_2
        ),
        "balanced-switch mutant is false",
    )
    return {
        "all_child_partitions_checked": ["{{x,y}}", "{{x},{y}}"],
        "balanced_weight": str(weight_1),
        "balanced_switch_all_future_pairing_certificate": True,
        "local_all_partition_kernel_equal_under_side_free_manifest": True,
        "one_block_route_sum": str(one_block_route_sum),
        "reconvergence_mass": str(mass_at_reconvergence),
        "raw_parent_words_distinct": True,
        "suffix_merger_mass": str(suffix_merger_mass),
        "side_free_graph_manifest_validated": True,
        "validated_graph_vertices": len(vertices),
    }


def check_divided_differences() -> dict:
    a, b, delta = map(rat, ("2", "3", "1"))
    u = sp.symbols("u", real=True)
    integral = sp.integrate(
        sp.exp(-a * u - b * (delta - u)), (u, 0, delta)
    )
    formula = (
        sp.exp(-b * delta) - sp.exp(-a * delta)
    ) / (a - b)
    assert_zero(integral - formula, "ordered simplex")
    b_symbol = sp.symbols("b")
    repeated = sp.limit(
        (
            sp.exp(-b_symbol * delta)
            - sp.exp(-a * delta)
        )
        / (a - b_symbol),
        b_symbol,
        a,
    )
    assert_zero(
        repeated - delta * sp.exp(-a * delta),
        "confluent limit",
    )
    return {"distinct": True, "confluent": True}


def check_vandermonde(cases: dict) -> dict:
    case = cases["vandermonde"]
    nodes = [rat(value) for value in case["nodes"]]
    ranks = []
    for order in range(1, case["max_order"] + 1):
        used = nodes[: order + 1]
        full = sp.Matrix(
            [
                [node**power for node in used]
                for power in range(1, order + 2)
            ]
        )
        first = full[:-1, :]
        require(full.det() != 0, f"Vandermonde determinant order {order}")
        require(first.rank() == order, f"Vandermonde first-row rank {order}")
        kernel = first.nullspace()
        require(len(kernel) == 1, f"Vandermonde kernel dimension {order}")
        require(
            all(entry != 0 for entry in kernel[0]),
            f"Vandermonde kernel support {order}",
        )
        ranks.append([order, full.rank()])
    return {"rank_pairs": ranks}


def check_mutants(cases: dict) -> dict:
    killed: dict[str, str] = {}
    a, b, delta = map(rat, ("2", "3", "1"))
    correct = (
        sp.exp(-b * delta) - sp.exp(-a * delta)
    ) / (a - b)
    if sp.simplify(
        mutants.wrong_divided_difference(a, b, delta) - correct
    ) != 0:
        killed["wrong_divided_difference_sign"] = (
            "ordered_simplex_integral"
        )

    q = matrix(cases["pair_generators"][0]["generator"])
    d_pi = sp.diag(rat("1/2"), rat("1/2"))
    s = rat("2")
    transition = (q * s).exp()
    joint = d_pi * transition
    if sp.simplify(
        mutants.unscaled_determinant_coordinate(joint) - s
    ) != 0:
        killed["omit_stationary_scaling"] = "determinant_coordinate"

    gamma = sp.symbols("gamma")
    if sp.expand(mutants.omit_mixed_funnel_routes(gamma)) != 1:
        killed["omit_mixed_funnel_routes"] = "route_sum"

    scale, rate, time = map(rat, ("3", "2", "5"))
    if mutants.wrong_scaled_hazard(
        rate, time, scale
    ) != rate * time:
        killed["wrong_gauge_rate"] = "hazard_unit_invariance"

    nodes = [
        rat(value) for value in cases["vandermonde"]["nodes"][:4]
    ]
    duplicate = mutants.duplicate_vandermonde_node(nodes)
    matrix_mutant = sp.Matrix(
        [
            [node**power for node in duplicate]
            for power in range(1, 5)
        ]
    )
    if matrix_mutant.det() == 0:
        killed["duplicate_vandermonde_node"] = (
            "collision_transversality"
        )

    if mutants.jacobian_kernel_is_exact_tangent():
        x = sp.symbols("x")
        if sp.solve(sp.Eq(x**2, 0), x) == [0]:
            killed["jacobian_kernel_equals_exact_tangent"] = (
                "singular_square_fiber"
            )

    switch = cases["balance_switch"]
    x = sp.symbols("x", positive=True)
    suffix_1, suffix_2 = [rat(value) for value in switch["suffix_rates"]]
    if not mutants.balanced_switch_requires_equal_suffixes(
        x**suffix_1, x**suffix_2
    ):
        killed["balanced_switch_requires_equal_suffixes"] = (
            "posterior_balance_suffix_exchange"
        )

    cocycle = cases["observable_cocycle"]
    beta_12 = sp.Matrix([[rat(value) for value in cocycle["future_after_12"]]])
    beta_13 = sp.Matrix([[rat(value) for value in cocycle["future_after_13"]]])
    word_mass = rat(cocycle["labelled_word_mass"])
    reset_residual = word_mass * (beta_13 - beta_12)
    empty_residual = sp.zeros(1, beta_12.cols)
    if (
        mutants.cocycle_all_completions_only(reset_residual)
        and reset_residual != sp.zeros(1, beta_12.cols)
    ):
        killed["cocycle_all_completions_only"] = "labelled_future_columns"
    if (
        mutants.cocycle_empty_word_only(empty_residual)
        and reset_residual != sp.zeros(1, beta_12.cols)
    ):
        killed["cocycle_empty_word_only"] = "nonempty_labelled_word"
    if (
        mutants.cocycle_aggregate_target_pairs(beta_12, beta_13)
        and beta_12 != beta_13
    ):
        killed["cocycle_aggregate_target_pairs"] = "target_pair_labels"
    if (
        mutants.cocycle_check_sides_without_spanning(True, True)
        and reset_residual != sp.zeros(1, beta_12.cols)
    ):
        killed["cocycle_check_sides_without_spanning"] = "spanning_word"
    if (
        mutants.cocycle_accept_physical_port_id("latent-P", "latent-P")
        and reset_residual != sp.zeros(1, beta_12.cols)
    ):
        killed["cocycle_accept_physical_port_id"] = "law_only_port_key"
    joint_entry_table = sp.Matrix([[rat("2"), rat("3")], [rat("5"), rat("7")]])
    if not mutants.multicut_entry_is_product_of_port_marginals(joint_entry_table):
        killed["multicut_entry_is_product_of_port_marginals"] = (
            "joint_all_completions_normalization"
        )

    expected = {
        "balanced_switch_requires_equal_suffixes",
        "cocycle_accept_physical_port_id",
        "cocycle_aggregate_target_pairs",
        "cocycle_all_completions_only",
        "cocycle_check_sides_without_spanning",
        "cocycle_empty_word_only",
        "duplicate_vandermonde_node",
        "jacobian_kernel_equals_exact_tangent",
        "multicut_entry_is_product_of_port_marginals",
        "omit_mixed_funnel_routes",
        "omit_stationary_scaling",
        "wrong_divided_difference_sign",
        "wrong_gauge_rate",
    }
    survivors = sorted(expected - set(killed))
    unexpected = sorted(set(killed) - expected)
    require(not unexpected, f"unexpected mutant outcomes: {unexpected}")
    require(not survivors, f"surviving mutants: {survivors}")
    return {
        "killed": killed,
        "mutants_killed": len(killed),
        "mutants_survived": len(survivors),
        "survivors": survivors,
    }


def main() -> None:
    cases = json.loads(CASES_PATH.read_text())
    checks = {
        "balance_switch": check_balance_switch(cases),
        "divided_differences": check_divided_differences(),
        "finite_jets": check_finite_jets(cases),
        "hazard_schedule": check_hazard(cases),
        "observable_cocycle": check_observable_cocycle(cases),
        "pair_generators": check_pair_generators(cases),
        "routing": check_routing(cases),
        "tensor_mixture": check_tensor_mixture(cases),
        "ultrametric_tree": check_ultrametric(cases),
        "vandermonde": check_vandermonde(cases),
    }
    mutation_report = check_mutants(cases)
    require(
        mutation_report["mutants_survived"] == 0,
        "independent mutation suite has survivors",
    )
    report = {
        "case_manifest_sha256": hashlib.sha256(
            CASES_PATH.read_bytes()
        ).hexdigest(),
        "checks": checks,
        "implementation_independence": (
            "does not import code/core_exact.py"
        ),
        "scope": (
            "exact computational anchors; noncomputational theorems "
            "require proof audit"
        ),
        "status": "PASS",
    }
    certificate_dir = ROOT / "certificates"
    certificate_dir.mkdir(exist_ok=True)
    (certificate_dir / "independent_verifier_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    (certificate_dir / "mutation_kill_report.json").write_text(
        json.dumps(mutation_report, indent=2, sort_keys=True) + "\n"
    )
    print(
        "INDEPENDENT_VERIFIER_PASS "
        f"anchors={len(checks)} "
        f"mutants={mutation_report['mutants_killed']}"
    )


if __name__ == "__main__":
    main()
