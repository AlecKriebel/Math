"""Pure-standard-library replay of the K2P/K3P quartic certificates.

This verifier does not import SymPy or any code from ``fourier_models.py``.  It
reconstructs the displayed-tree Fourier polynomials from the machine-readable
network and invariant files, expands them as sparse dictionaries over Q, and
checks exact cancellation.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NETWORK_FILE = ROOT / "certificates" / "theta_pair_networks.json"
INVARIANT_FILE = ROOT / "certificates" / "model_robustness_invariants.json"
CERTIFICATE_FILE = ROOT / "certificates" / "model_robustness_certificate.json"


def add(left, right):
    answer = dict(left)
    for monomial, coefficient in right.items():
        value = answer.get(monomial, Fraction(0)) + coefficient
        if value:
            answer[monomial] = value
        elif monomial in answer:
            del answer[monomial]
    return answer


def scale(polynomial, scalar):
    scalar = Fraction(scalar)
    if not scalar:
        return {}
    return {monomial: scalar * coefficient for monomial, coefficient in polynomial.items()}


def multiply(left, right):
    answer = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(a + b for a, b in zip(monomial_left, monomial_right))
            answer[monomial] = answer.get(monomial, Fraction(0)) + coefficient_left * coefficient_right
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def constant(value, variable_count):
    value = Fraction(value)
    return {} if not value else {(0,) * variable_count: value}


def variable(index, variable_count):
    monomial = [0] * variable_count
    monomial[index] = 1
    return {tuple(monomial): Fraction(1)}


def load_data():
    with NETWORK_FILE.open() as stream:
        network = json.load(stream)
    with INVARIANT_FILE.open() as stream:
        invariants = json.load(stream)
    with CERTIFICATE_FILE.open() as stream:
        certificate = json.load(stream)
    return network, invariants, certificate


def edge_data(network):
    triples = network["internal_arcs"] + network["pendant_arcs"]
    return [(name, parent, child) for parent, child, name in triples]


def selected_edges(network, choice_c, choice_f):
    excluded = {
        network["reticulation_incoming_choices"]["C"][1 - choice_c],
        network["reticulation_incoming_choices"]["F"][1 - choice_f],
    }
    return [edge for edge in edge_data(network) if edge[0] not in excluded]


def descendant_labels(selected, labels):
    children = {}
    for _name, parent, child in selected:
        children.setdefault(parent, []).append(child)
    cache = {}

    def descend(node):
        if node in cache:
            return cache[node]
        if node in labels:
            answer = frozenset((int(labels[node]),))
        else:
            answer = frozenset().union(*(descend(child) for child in children.get(node, ())))
        cache[node] = answer
        return answer

    return {name: descend(child) for name, _parent, child in selected}


def class_count(model):
    return 2 if model == "K2P" else 3


def character_class(model, character):
    if model == "K2P":
        return 0 if character == 1 else 1
    return character - 1


def parameter_names(network, model):
    edge_names = [name for name, _parent, _child in edge_data(network)]
    names = []
    for edge in edge_names:
        for cls in range(class_count(model)):
            names.append(("edge", edge, cls))
    names.extend((("inheritance", "C"), ("inheritance", "F")))
    return names


def coordinate_polynomial(network, model, labels, assignment, variable_index):
    variable_count = len(variable_index)
    one = constant(1, variable_count)
    answer = {}
    for choice_c, choice_f in product((0, 1), repeat=2):
        selected = selected_edges(network, choice_c, choice_f)
        descendants = descendant_labels(selected, labels)
        term = one
        for reticulation, choice in (("C", choice_c), ("F", choice_f)):
            inheritance = variable(variable_index[("inheritance", reticulation)], variable_count)
            weight = inheritance if choice == 0 else add(one, scale(inheritance, -1))
            term = multiply(term, weight)
        for edge, _parent, _child in selected:
            character = 0
            for leaf in descendants[edge]:
                character ^= assignment[leaf - 1]
            if character:
                cls = character_class(model, character)
                term = multiply(
                    term,
                    variable(variable_index[("edge", edge, cls)], variable_count),
                )
        answer = add(answer, term)
    return answer


def invariant_polynomial(network, model, labels, terms):
    names = parameter_names(network, model)
    variable_index = {name: index for index, name in enumerate(names)}
    cache = {}
    answer = {}
    for coefficient, factors in terms:
        term = constant(coefficient, len(names))
        for factor in factors:
            assignment = tuple(factor)
            if assignment not in cache:
                cache[assignment] = coordinate_polynomial(
                    network, model, labels, assignment, variable_index
                )
            term = multiply(term, cache[assignment])
        answer = add(answer, term)
    return answer


def witness_values(network, model):
    edges = [name for name, _parent, _child in edge_data(network)]
    values = {}
    for edge_index, edge in enumerate(edges):
        if model == "K2P":
            values[("edge", edge, 0)] = Fraction(2, 5) + Fraction(edge_index % 5, 100)
            values[("edge", edge, 1)] = Fraction(1, 3) + Fraction(edge_index % 7, 120)
        else:
            values[("edge", edge, 0)] = Fraction(1, 2) + Fraction(edge_index % 5, 100)
            values[("edge", edge, 1)] = Fraction(2, 5) + Fraction(edge_index % 7, 120)
            values[("edge", edge, 2)] = Fraction(1, 3) + Fraction(edge_index % 11, 150)
    values[("inheritance", "C")] = Fraction(1, 2)
    values[("inheritance", "F")] = Fraction(1, 2)
    return values


def coordinate_value(network, model, labels, assignment, values):
    answer = Fraction(0)
    for choice_c, choice_f in product((0, 1), repeat=2):
        term = Fraction(1)
        for reticulation, choice in (("C", choice_c), ("F", choice_f)):
            inheritance = values[("inheritance", reticulation)]
            term *= inheritance if choice == 0 else 1 - inheritance
        selected = selected_edges(network, choice_c, choice_f)
        descendants = descendant_labels(selected, labels)
        for edge, _parent, _child in selected:
            character = 0
            for leaf in descendants[edge]:
                character ^= assignment[leaf - 1]
            if character:
                term *= values[("edge", edge, character_class(model, character))]
        answer += term
    return answer


def invariant_value(network, model, labels, terms, values):
    cache = {}
    answer = Fraction(0)
    for coefficient, factors in terms:
        term = Fraction(coefficient)
        for factor in factors:
            assignment = tuple(factor)
            if assignment not in cache:
                cache[assignment] = coordinate_value(network, model, labels, assignment, values)
            term *= cache[assignment]
        answer += term
    return answer


def transition_probabilities(model, edge, values):
    if model == "K2P":
        a1 = values[("edge", edge, 0)]
        a2 = a3 = values[("edge", edge, 1)]
    else:
        a1, a2, a3 = (values[("edge", edge, cls)] for cls in range(3))
    return (
        (1 + a1 + a2 + a3) / 4,
        (1 + a1 - a2 - a3) / 4,
        (1 - a1 + a2 - a3) / 4,
        (1 - a1 - a2 + a3) / 4,
    )


def verify_model(network, invariant_data, certificate, model):
    terms = invariant_data[model]["source_invariant_terms"]
    source_labels = network["source_leaf_labels"]
    target_labels = network["target_leaf_labels"]
    source_pullback = invariant_polynomial(network, model, source_labels, terms)
    assert source_pullback == {}

    values = witness_values(network, model)
    target_value = invariant_value(network, model, target_labels, terms, values)
    expected = Fraction(certificate[f"{model}_separation"]["target_pullback_nonzero_witness"])
    assert target_value == expected != 0

    edges = [name for name, _parent, _child in edge_data(network)]
    probabilities = [p for edge in edges for p in transition_probabilities(model, edge, values)]
    assert all(p > 0 for p in probabilities)
    expected_minimum = Fraction(certificate[f"{model}_separation"]["minimum_target_transition_probability"])
    assert min(probabilities) == expected_minimum
    return len(source_pullback), target_value, min(probabilities)


def main():
    network, invariants, certificate = load_data()
    for model in ("K2P", "K3P"):
        term_count, value, minimum = verify_model(network, invariants, certificate, model)
        print(model, "source_sparse_terms", term_count, "target_value", value, "min_transition", minimum)
    print("PASS: independent standard-library exact replay")


if __name__ == "__main__":
    main()

