#!/usr/bin/env python3
"""Independent integer-fibre certificate for the Potts censoring witness.

Requires only Python >= 3.9. Run: python3 verification/independent.py
No local conditional-neighbour formula and no Fraction propagation is used.
For each coordinate, partition all configurations into Gibbs fibres; replace
the total mass of a fibre by its Gibbs proportions. All evolving probabilities
share one integer denominator. Fractions are used only for output statistics.
"""

from collections import Counter
from fractions import Fraction
from functools import reduce
from itertools import product
from math import gcd, lcm
import json


VERTICES = "ABCDE"
EDGES = ("AB", "AC", "AD", "BC", "BE", "DE")
FULL = "CEBCBAEBE"
CENSORED = "CEBCBABE"


def require(condition, message):
    """Checks remain active when Python is invoked with -O."""
    if not condition:
        raise RuntimeError(message)


class FibreChain:
    def __init__(self, q=3, coupling=30):
        require(q >= 2 and isinstance(coupling, int) and coupling >= 1, "invalid parameters")
        self.states = list(product(range(q), repeat=5))
        edge_indices = [(VERTICES.index(a), VERTICES.index(b)) for a, b in EDGES]
        energies = [sum(s[a] == s[b] for a, b in edge_indices) for s in self.states]
        self.energy_counts = dict(sorted(Counter(energies).items()))
        self.weights = [coupling**energy for energy in energies]
        self.z = sum(self.weights)
        self.fibres = {}
        self.scales = {}
        for site in range(5):
            partition = {}
            for index, state in enumerate(self.states):
                key = state[:site] + state[site+1:]
                partition.setdefault(key, []).append(index)
            fibres = []
            for indices in partition.values():
                require(len(indices) == q, "fibre size")
                weights = [self.weights[index] for index in indices]
                common = reduce(gcd, weights)
                local = [weight // common for weight in weights]
                denominator = sum(local)
                # Detailed balance on every allowed pair, using global weights.
                for i, wi in zip(indices, local):
                    for j, wj in zip(indices, local):
                        require(self.weights[i] * wj == self.weights[j] * wi, "detailed balance")
                fibres.append((indices, local, denominator))
            self.fibres[site] = fibres
            self.scales[site] = reduce(lcm, (d for _, _, d in fibres), 1)
        self.stationary = self.canonical(self.weights, self.z)

    @staticmethod
    def canonical(numerators, denominator):
        require(denominator > 0, "positive denominator")
        require(all(isinstance(n, int) and n >= 0 for n in numerators), "nonnegative integer masses")
        require(sum(numerators) == denominator, "normalization")
        common = reduce(gcd, numerators, denominator)
        return tuple(n // common for n in numerators), denominator // common

    def initial(self):
        return self.canonical([1] + [0] * (len(self.states)-1), 1)

    def update(self, law, vertex):
        numerators, denominator = law
        site = VERTICES.index(vertex)
        scale = self.scales[site]
        result = [0] * len(self.states)
        for indices, weights, local_denominator in self.fibres[site]:
            total = sum(numerators[index] for index in indices)
            multiplier = scale // local_denominator
            require(multiplier * local_denominator == scale, "integer scaling")
            for index, weight in zip(indices, weights):
                result[index] = total * weight * multiplier
        return self.canonical(result, denominator * scale)

    def tv(self, law):
        numerators, denominator = law
        return Fraction(sum(abs(n*self.z-w*denominator)
                            for n, w in zip(numerators, self.weights)),
                        2*denominator*self.z)

    def run(self, word):
        law = self.initial()
        trace = [self.tv(law)]
        for vertex in word:
            next_law = self.update(law, vertex)
            # Every individual update remains a contraction to Gibbs measure.
            require(self.tv(next_law) <= trace[-1], "single-step TV contraction")
            # Heat-bath resampling is a projection.
            require(self.update(next_law, vertex) == next_law, "heat-bath idempotence")
            law = next_law
            trace.append(self.tv(law))
        return law, trace


def as_ratio(value):
    return {"numerator": value.numerator, "denominator": value.denominator}


def certificate():
    chain = FibreChain()
    for vertex in VERTICES:
        require(chain.update(chain.stationary, vertex) == chain.stationary, "Gibbs stationarity")
    require(len(chain.states) == 243, "state count")
    require(chain.z == 2207656998, "partition function")
    require(chain.energy_counts == {0: 18, 1: 66, 2: 90, 3: 42, 4: 24, 6: 3}, "energy histogram")
    mu, full_trace = chain.run(FULL)
    nu, censored_trace = chain.run(CENSORED)
    tv_mu, tv_nu = chain.tv(mu), chain.tv(nu)
    gap = tv_mu-tv_nu
    require(tv_mu == Fraction(511715038479158504505751178946687363011,
                             766036711510586802141859485820665762204), "full TV fraction")
    require(tv_nu == Fraction(9300189570967998685056395332640723,
                             13922371260779084768671794660693282), "censored TV fraction")
    require(gap == Fraction(7905357280856578194954129502105,
                            766036711510586802141859485820665762204), "gap fraction")
    require(gap > 0, "strict counterexample")
    require(sum(w for s, w in zip(chain.states, chain.weights) if s[3] == 0) * 3 == chain.z,
            "Gibbs slice mass")
    sign_rows = []
    expected_full = {"101", "111", "121", "122"}
    expected_censored = expected_full | {"112"}
    for law in (mu, nu):
        ns, den = law
        require(sum(n > 0 for n in ns) == 81, "support size")
        require(all(n == 0 for s, n in zip(chain.states, ns) if s[3] != 0), "support D=0")
        # The final E update matches Gibbs proportions on every E fibre.
        for indices, local, _ in chain.fibres[4]:
            for i, wi in zip(indices, local):
                for j, wj in zip(indices, local):
                    require(ns[i] * wj == ns[j] * wi, "final E conditional factor")
    for abc in product(range(3), repeat=3):
        swapped = tuple(0 if v == 0 else 3-v for v in abc)
        if abc > swapped:
            continue
        key = "".join(map(str, abc))
        indices = [i for i, s in enumerate(chain.states) if s[:3] == abc and s[3] == 0]
        stationary_mass = Fraction(sum(chain.weights[i] for i in indices), chain.z)
        differences = [stationary_mass-Fraction(sum(ns[i] for i in indices), den)
                       for ns, den in (mu, nu)]
        require(all(value != 0 for value in differences), "nonzero signs")
        require((differences[0] > 0) == (key in expected_full), "full marginal sign")
        require((differences[1] > 0) == (key in expected_censored), "censored marginal sign")
        sign_rows.append({"abc": key, "stationary_minus_full": as_ratio(differences[0]),
                          "stationary_minus_censored": as_ratio(differences[1])})
    # Boundary controls for this graph and these two words, not universal claims.
    controls = {}
    for q, coupling in ((3, 1), (2, 30)):
        control = FibreChain(q=q, coupling=coupling)
        left, _ = control.run(FULL)
        right, _ = control.run(CENSORED)
        difference = control.tv(left)-control.tv(right)
        require(difference <= 0, "boundary control")
        controls[f"q={q},coupling={coupling}"] = as_ratio(difference)
    return {
        "method": "global Gibbs weights; integer mass redistribution on fibres",
        "states": len(chain.states), "edges": EDGES, "coupling": 30,
        "full_word": FULL, "censored_word": CENSORED,
        "partition_function": chain.z, "energy_counts": chain.energy_counts,
        "tv_full": as_ratio(tv_mu), "tv_censored": as_ratio(tv_nu),
        "gap": as_ratio(gap), "gap_decimal_for_orientation_only": float(gap),
        "full_trace": [as_ratio(value) for value in full_trace],
        "censored_trace": [as_ratio(value) for value in censored_trace],
        "same_opportunity_gaps": {
            "7": as_ratio(full_trace[7]-censored_trace[6]),
            "8": as_ratio(full_trace[8]-censored_trace[7]),
            "9": as_ratio(gap),
        },
        "sign_representatives": sign_rows, "boundary_controls": controls,
        "checks": ["normalization at every step", "all-site stationarity",
                   "detailed balance on every fibre pair", "heat-bath idempotence",
                   "TV contraction at every applied step", "support is D=0",
                   "stationary D=0 mass is 1/3", "final E Gibbs proportions",
                   "all 14 candidate sign representatives", "exact claimed TV fractions"]
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
