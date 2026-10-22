#!/usr/bin/env python3
"""Independent exact-rational controls; no candidate checker imported or executed."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import datetime
import hashlib
import json
import math
import random
import time

OUT = Path(__file__).resolve().parent


def summary(v):
    v = F(v)
    payload = f"{v.numerator}/{v.denominator}".encode()
    return {"float": float(v), "sign": (v > 0) - (v < 0),
            "numerator_bits": v.numerator.bit_length(),
            "denominator_bits": v.denominator.bit_length(),
            "exact_fraction_sha256": hashlib.sha256(payload).hexdigest()}


def ceil(v):
    return -((-v.numerator) // v.denominator)


class Candidate:
    def __init__(self, lam):
        self.lam = F(lam)
        self.alpha = self.lam / 2
        self.beta = 17 * self.lam / 8
        self.q = F(7, 8)
        self.c = 2 * (self.beta + 4)
        self.m = 4 * self.c
        self.theta = self.beta + self.c + 4
        self.gamma = (self.theta + 1) / (self.theta + 2)
        self.eta = (1 + self.gamma) / 2
        self.ell = 1 / (self.eta - self.gamma)
        w = F(1)
        sw, skw = F(1), F(0)
        R = 0
        while R < 1 or skw / sw <= self.theta or self.q * (R + 1) <= self.beta + self.c + 2:
            R += 1
            w *= self.gamma
            sw += w
            skw += R * w
        self.R = R
        self.mu = skw / sw
        numerator = F(0)
        power = F(1)
        increments = []
        for k in range(R):
            numerator += power * (k - self.mu)
            increments.append(numerator / (power * self.gamma * (k + 1)))
            power *= self.gamma
        self.gvals = [F(0)] * (R + 1)
        for k in range(R - 1, -1, -1):
            self.gvals[k] = self.gvals[k + 1] - increments[k]
        self.G = self.gvals[0]
        self.N = max(R + 2, 3 * (R + 1),
                     ceil((self.m + (1 + self.eta) * R + self.eta) / (1 - self.eta)),
                     ceil(self.ell * self.G * (self.lam + 4 * (2 * R + 1))))
        self.B = (self.N + R + 1) * (self.beta + self.c + self.G * (self.lam + 2 * (self.N + R)) + 1)

    def g(self, k):
        assert k >= 0
        return self.gvals[k] if k < self.R else F(0)

    def cutoff(self, t):
        return max(F(0), min(F(1), (t - self.gamma) * self.ell))

    def h(self, z):
        return z * z / (2 * self.m) + self.m / 2 if abs(z) <= self.m else abs(z)

    def hp(self, z):
        return max(F(-1), min(F(1), F(z) / self.m))

    def Z(self, state):
        a, b, x, y = state
        return a + x - b - y

    def W(self, state):
        a, b, x, y = state
        return 2 * a + 2 * b + x + y

    def base(self, state):
        return self.W(state) + self.c * self.h(self.Z(state))

    def J(self, state):
        a, b, x, y = state
        D = x + y + 1
        return self.cutoff(F(b, D)) * self.g(y) + self.cutoff(F(a, D)) * self.g(x)

    def V(self, state):
        return self.base(state) + self.J(state)

    def events(self, state, seed=True, visible_denominator=True):
        a, b, x, y = state
        D = x + y + 1 if visible_denominator else a + b + x + y + 1
        e = int(seed)
        rates = [self.alpha, self.alpha, F(a * (x + e), D), F(b * (y + e), D),
                 F(x * (y + e), D), F(y * (x + e), D)]
        increments = [(1, 0, 0, 0), (0, 1, 0, 0), (-1, 0, 1, 0),
                      (0, -1, 0, 1), (0, 0, -1, 0), (0, 0, 0, -1)]
        return [(r, tuple(v + d for v, d in zip(state, delta)), i)
                for i, (r, delta) in enumerate(zip(rates, increments)) if r]

    def generator(self, state, fn, **kwargs):
        old = fn(state)
        return sum((rate * (fn(new) - old) for rate, new, _ in self.events(state, **kwargs)), F(0))

    def samples(self):
        states = set(product(range(3), repeat=4))
        for x in [self.N - 1, self.N, self.N + 1, 10 * self.N]:
            for y in [0, 1, self.R, self.R + 1]:
                D = x + y + 1
                targets = [0, 1, int(self.gamma * D) - 1, int(self.gamma * D),
                           int(self.gamma * D) + 1, int(self.eta * D) - 1,
                           int(self.eta * D), int(self.eta * D) + 1, D, 10 * D]
                for b in targets:
                    if b < 0:
                        continue
                    for a in [0, max(0, b + y - x), max(0, b + y - x + ceil(self.m))]:
                        states.add((a, b, x, y))
                        states.add((b, a, y, x))
        for x, y in [(0, 0), (1, 0), (self.R, self.R), (self.N - 1, self.R)]:
            for wait in [ceil(self.B), ceil(self.B) + 1]:
                states.add((wait, 0, x, y))
                states.add((0, wait, x, y))
        return sorted(states)

    def exact_checks(self):
        for k in range(self.R + 1):
            qg = F(0)
            if k < self.R:
                qg += self.gamma * (k + 1) * (self.g(k + 1) - self.g(k))
            if k:
                qg += k * (self.g(k - 1) - self.g(k))
            assert qg == k - self.mu, ("Poisson equation", k)
        assert self.mu > self.theta
        assert self.q * (self.R + 1) > self.beta + self.c + 2
        assert self.G > 0 and all(self.g(k) >= self.g(k + 1) >= 0 for k in range(self.R))
        minimum_margin = None
        regions = [0, 0, 0]
        outside = 0
        states = self.samples()
        for state in states:
            a, b, x, y = state
            D = x + y + 1
            u = F(a * (x + 1) + b * (y + 1), D)
            d = F(2 * x * y + x + y, D)
            z = self.Z(state)
            assert self.generator(state, self.W) == 2 * self.lam - u - d
            assert self.generator(state, self.Z) == F(y - x, D)
            assert self.generator(state, lambda s: self.Z(s) ** 2) == 2 * z * F(y - x, D) + self.lam + d
            assert self.generator(state, lambda s: sum(s)) == self.lam - d
            assert self.generator(state, self.base) <= self.beta - u - self.q * d + self.c * self.hp(z) * F(y - x, D)
            j_drift = self.generator(state, self.J)
            main = self.cutoff(F(b, D)) * self.generator(state, lambda s: self.g(s[3]))
            main += self.cutoff(F(a, D)) * self.generator(state, lambda s: self.g(s[2]))
            assert j_drift <= main + self.ell * self.G * (self.lam + 4 * d) / D
            assert j_drift <= self.G * (self.lam + 2 * d)
            for rate, new, kind in self.events(state):
                aa, bb, xx, yy = new
                DD = xx + yy + 1
                interface = self.g(yy) * (self.cutoff(F(bb, DD)) - self.cutoff(F(b, D)))
                interface += self.g(xx) * (self.cutoff(F(aa, DD)) - self.cutoff(F(a, D)))
                if kind in [2, 3]:
                    assert interface <= 0
                if kind in [4, 5]:
                    assert interface <= 4 * self.ell * self.G / D
            if min(x, y) >= self.R + 1:
                region = 0
                assert j_drift == 0
            elif max(x, y) >= self.N:
                region = 1
                small = min(x, y)
                assert self.q * d >= small
            else:
                region = 2
            regions[region] += 1
            if x + y > self.N + self.R or a + b > self.B:
                outside += 1
                drift = self.generator(state, self.V)
                assert drift <= -1, ("outside-F Foster failure", state, summary(drift))
                margin = -1 - drift
                minimum_margin = margin if minimum_margin is None else min(minimum_margin, margin)
        return {"lambda": str(self.lam), "R": self.R, "N": self.N,
                "mu": summary(self.mu), "G": summary(self.G), "B": summary(self.B),
                "exact_states_checked": len(states), "regions_I_II_III": regions,
                "outside_F_states": outside,
                "minimum_checked_Foster_margin": summary(minimum_margin),
                "failures": []}


def negative_controls(c):
    L = 10 * c.N
    state = (0, L, L, 0)
    uncorrected = c.generator(state, c.base)
    corrected = c.generator(state, c.V)
    assert uncorrected > 0 and corrected < -1
    old_y = c.generator(state, lambda s: c.g(s[3]))
    changed_y = c.generator(state, lambda s: c.g(s[3]), visible_denominator=False)
    assert F(L, L + 1) >= c.gamma
    assert old_y <= -c.mu and changed_y > -c.mu
    wait = ceil(c.B) + 1
    void = (wait, wait, 0, 0)
    seedless = c.generator(void, c.V, seed=False)
    assert seedless > 0
    D = (c.R + 2) * 100
    b = int((c.gamma + c.eta) * D / 2)
    at = (0, b, D - c.R - 1, c.R)
    new = (0, b, D - c.R - 1, c.R - 1)
    positive_departure_interface = c.g(c.R - 1) * (c.cutoff(F(b, D - 1)) - c.cutoff(F(b, D)))
    assert positive_departure_interface > 0
    return {
        "corrector_omission": {"state": state, "base_drift": summary(uncorrected),
                                "full_drift": summary(corrected), "caught": True},
        "wrong_total_population_denominator": {"state": state, "original_Lg_y": summary(old_y),
            "modified_Lg_y": summary(changed_y), "required_upper_bound": summary(-c.mu), "caught": True},
        "seed_numerator_removal": {"state": void, "modified_LV": summary(seedless),
            "mechanism": "Visible zero is absorbing; only arrivals occur and both waiting rooms grow.", "caught": True},
        "all_departure_interfaces_nonpositive_false": {"state": at, "successor": new,
            "positive_interface": summary(positive_departure_interface), "caught": True}
    }


def finite_horizon_experiment():
    # Simulation is a reproducible limiting diagnostic, not recurrence evidence.
    lam, alpha, b0, n, R, reps = 10.0, 5.0, 5, 0, 1000000, 5000
    rng = random.Random(202610210323)
    rows = []
    for horizon in [1.0, 10.0]:
        total, total2, events = 0.0, 0.0, 0
        for _ in range(reps):
            a, b, x, y = R, b0, n, R
            t = 0.0
            while True:
                D = x + y + 1
                rates = [alpha, alpha, a * (x + 1) / D, b * (y + 1) / D,
                         x * (y + 1) / D, y * (x + 1) / D]
                rate = sum(rates)
                t += rng.expovariate(rate)
                if t > horizon:
                    break
                pick = rng.random() * rate
                kind = 0
                while pick >= rates[kind]:
                    pick -= rates[kind]
                    kind += 1
                if kind == 0: a += 1
                elif kind == 1: b += 1
                elif kind == 2: a, x = a - 1, x + 1
                elif kind == 3: b, y = b - 1, y + 1
                elif kind == 4: x -= 1
                else: y -= 1
                events += 1
            value = y - R
            total += value
            total2 += value * value
        observed = total / reps
        variance = (total2 - total * total / reps) / (reps - 1)
        p = 1 - math.exp(-horizon)
        predicted = (alpha - n - 1) * horizon - horizon ** 2 / 2 + (b0 - alpha) * p
        limiting_var = b0 * p * (1 - p) + alpha * (horizon - p)
        limiting_var += (n + 1) * horizon + horizon ** 2 / 2 + (2 * n + 1) * horizon ** 3 / 3 + horizon ** 4 / 6
        se = math.sqrt(variance / reps)
        rows.append({"horizon": horizon, "observed_Y_increment_mean": observed,
                     "sample_variance": variance, "sample_standard_error": se,
                     "limiting_mean": predicted, "limiting_variance": limiting_var,
                     "mean_difference_in_standard_errors": (observed - predicted) / se,
                     "effective_events": events})
    return {"lambda": lam, "initial_state": [R, b0, n, R], "replicates_each": reps,
            "seed": 202610210323, "rows": rows,
            "classification": "finite-horizon Monte Carlo diagnostic; no stationarity or recurrence claim"}


def limiting_generator_controls():
    checks = 0
    for rho in [F(0), F(1, 2), F(1), F(3, 2)]:
        for x in range(12):
            lx = rho * (x + 1) - x
            lx2 = rho * (x + 1) * (2 * x + 1) + x * (-2 * x + 1)
            assert lx == rho + (rho - 1) * x
            assert lx2 == 2 * (rho - 1) * x * x + (3 * rho + 1) * x + rho
            if rho == 1:
                assert lx == 1 and lx2 == 4 * x + 1
            checks += 1
    # Initial exact generators on the empty-rare-waiting-room sequence.
    model = Candidate(F(10))
    exact = []
    for R in [10, 1000, 1000000]:
        state = (0, 5, 0, R)
        ln = model.generator(state, lambda s: sum(s))
        assert ln == 10 - F(R, R + 1) and ln > 9
        assert model.generator(state, lambda s: s[0]) == 5
        assert model.generator(state, lambda s: s[1]) == 0
        assert model.generator(state, lambda s: s[2]) == 0
        exact.append({"R": R, "LN": summary(ln)})
    return {"exact_rare_moment_identities_checked": checks,
            "rho_values": ["0", "1/2", "1", "3/2"],
            "empty_rare_room_exact_initial_generators": exact,
            "positive_fixed_horizon_limit": "For rho=0,n=0, E delta N=(lambda-1)t. For rho=1/2,n=0, lambda=10, E delta N >= 7t.",
            "limitation": "These are fixed-ratio, fixed-horizon limits; no infinite-time exchange or recurrence inference."}


def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    clock = time.monotonic()
    candidates = [Candidate(F(1, 100)), Candidate(F(1)), Candidate(F(10))]
    result = {"started_utc": started, "method": "independent exact Fraction generator; no candidate checker imported",
              "positive_controls": [c.exact_checks() for c in candidates],
              "negative_controls": negative_controls(candidates[1]),
              "limiting_generator_controls": limiting_generator_controls(),
              "finite_horizon_diagnostic": finite_horizon_experiment()}
    result["elapsed_seconds"] = time.monotonic() - clock
    result["finished_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (OUT / 'CONTROL_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({"positive_checks": [{k: row[k] for k in ['lambda', 'R', 'N', 'exact_states_checked', 'outside_F_states', 'failures']} for row in result['positive_controls']],
                      "negative_controls_caught": list(result['negative_controls']),
                      "finite_horizon": result['finite_horizon_diagnostic']['rows'],
                      "elapsed_seconds": result['elapsed_seconds']}, indent=2))


if __name__ == '__main__':
    main()
