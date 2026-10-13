#!/usr/bin/env python3
"""Independent finite adversarial controls; not a computation of an infinite event.

All temporal path tests use rational times and CLOSED recovery-free segments.
No stochastic simulations and no sampled huge offspring counts are used.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import product
import json

checks = Counter()
negative_controls = []

def check(statement, group):
    if not statement:
        raise AssertionError(group)
    checks[group] += 1

def finite_path_infected(vertices, arrows, recoveries, horizon, initial=(0,)):
    """Exhaust all finite arrow paths in a finite marked graph.

    Every reachable arrival record gives a finite path by induction. Multiple
    records preserve reinfections. Our fixtures have distinct arrow times;
    arrows incident to a recovery at the same time are explicitly rejected.
    """
    vertices = set(vertices)
    arrivals = defaultdict(set)
    for v in initial:
        if v in vertices and Q(0) not in recoveries.get(v, ()):
            arrivals[v].add(Q(0))
    for u, v, t in sorted(arrows, key=lambda a: a[2]):
        if u not in vertices or v not in vertices or not Q(0) <= t <= horizon:
            continue
        if t in recoveries.get(v, ()):
            continue
        if any(a <= t and not any(a <= r <= t for r in recoveries.get(u, ()))
               for a in arrivals[u]):
            arrivals[v].add(t)
    return {v for v in vertices if any(a <= horizon and
                not any(a <= r <= horizon for r in recoveries.get(v, ()))
                for a in arrivals[v])}

# Fixed-window arrows and recovery guards genuinely leave every finite prefix
# infected at one common horizon. Include extremely small and large rates.
for rate in (Q(1, 10**6), Q(1, 29), Q(1), Q(29), Q(10**6)):
    tau = 1 / (2 * rate)
    schedule = [tau * (1 - Q(1, 2**n)) for n in range(65)]
    for depth in (1, 2, 5, 16, 64):
        vertices = set(range(depth + 1))
        for mode in ('left_endpoint', 'strict_interior'):
            fraction = Q(0) if mode == 'left_endpoint' else Q(3, 7)
            arrows = [(n, n+1, schedule[n] + fraction *
                       (schedule[n+1] - schedule[n])) for n in range(depth)]
            check(finite_path_infected(vertices, arrows, {}, tau) == vertices,
                  'common_horizon_finite_paths')
            for n, (_, _, t) in enumerate(arrows):
                check(schedule[n] <= t < schedule[n+1] < tau,
                      'half_open_arrow_endpoints')
                check(rate * (schedule[n+1] - schedule[n]) == Q(1, 2**(n+2)),
                      'dimensionless_arrow_lengths')
            guard_sum = tau + sum((tau - schedule[n-1]
                                   for n in range(1, depth+1)), Q(0))
            check(guard_sum + 2*tau / 2**depth == 3*tau,
                  'recovery_product_exact_remainder')
            # Recovery before the child's guard begins is harmless. The root
            # cannot be assigned such a mark, because its guard begins at zero.
            old_recoveries = {n: (schedule[n-1] / 2,)
                              for n in range(2, depth+1)}
            check(finite_path_infected(vertices, arrows, old_recoveries, tau)
                  == vertices, 'pre_guard_recoveries_harmless')
            # Closed terminal segments make a recovery AT tau fatal at that
            # vertex; this is excluded by the proof's closed guards.
            terminal_recoveries = {n: (tau,) for n in vertices}
            check(not finite_path_infected(vertices, arrows, terminal_recoveries, tau),
                  'terminal_endpoint_recovery_negative_control')
            # Reverse all arrows: degree growth alone does not transmit away
            # from an initially infected root.
            reversed_arrows = [(v, u, t) for u, v, t in arrows]
            check(finite_path_infected(vertices, reversed_arrows, {}, tau) == {0},
                  'arrow_orientation_negative_control')
            check(not finite_path_infected(vertices, arrows, {}, tau, initial=()),
                  'no_initial_infection_negative_control')

# Counterexample mechanism if shrinking no-recovery guards are omitted:
# each ray vertex infects its successor, then recovers before the common limit.
# For arbitrary finite prefixes this leaves no infected vertex at tau, despite
# every vertex having been infected earlier and arrows accumulating at tau.
tau = Q(1)
for depth in (2, 4, 8, 32, 128):
    times = [1 - Q(1, 2**(n+1)) for n in range(depth)]
    arrows = [(n, n+1, times[n]) for n in range(depth)]
    recoveries = {n: ((times[n] + tau)/2,) for n in range(depth)}
    recoveries[depth] = ((times[-1] + tau)/2,)
    check(not finite_path_infected(range(depth+1), arrows, recoveries, tau),
          'fast_ray_not_simultaneous_infection_negative_control')
    for n in range(depth):
        check(n+1 in finite_path_infected(range(depth+1), arrows, recoveries, times[n]),
              'fast_ray_does_have_each_cumulative_infection')
negative_controls.append({'name': 'fast_ray_without_recovery_guards',
    'outcome': 'Every finite prefix has arbitrarily deep cumulative infection and no infection at the limit horizon; the proof explicitly rules this out.'})

# Finite-volume path union control with a path that exits an inner ball and
# returns. Restriction can lose a finite witness, while enlargement restores it.
arrows = [(0,1,Q(1,10)), (1,2,Q(2,10)), (2,3,Q(3,10)),
          (3,2,Q(5,10)), (2,1,Q(6,10))]
recoveries = {1: (Q(4,10),), 2: (Q(4,10),)}
inner = finite_path_infected({0,1,2}, arrows, recoveries, Q(1))
outer = finite_path_infected({0,1,2,3}, arrows, recoveries, Q(1))
check(inner == {0}, 'finite_volume_return_path_control')
check(outer == {0,1,2,3} and inner <= outer,
      'finite_volume_return_path_control')
for radius in range(4):
    a = finite_path_infected(set(range(radius+1)), arrows, recoveries, Q(1))
    b = finite_path_infected(set(range(radius+2)), arrows, recoveries, Q(1))
    check(a <= b, 'finite_volume_monotonicity')

# Conditional recovery independence for first eligible children. This records
# only the actually observed prefix, including failures before the selection.
# Child state = (degree qualifies, incoming arrow, fresh outgoing, recovery-free).
states = list(product((0,1), repeat=4))
histories_checked = 0
for width in range(1,5):
    table = defaultdict(Counter)
    for config in product(states, repeat=width):
        chosen = next((i for i, s in enumerate(config) if s[0] and s[1]), None)
        if chosen is None:
            continue
        observed_prefix = tuple((s[0],s[1]) for s in config[:chosen+1])
        table[(observed_prefix, chosen)][config[chosen][2:]] += 1
    for (prefix, chosen), counts in table.items():
        total = sum(counts.values())
        check(prefix[-1] == (1,1) and all(p != (1,1) for p in prefix[:-1]),
              'observed_prefix_selection_is_adaptive')
        check(all(Q(counts[b], total) == Q(1,4) for b in product((0,1),repeat=2)),
              'selected_fresh_outgoing_and_recovery_independent')
        histories_checked += 1
# Deliberately looking at recovery during selection destroys the untouched
# recovery law: the selected child's recovery-free flag is forced to one.
bad_selected = [s for s in states if s[0] and s[1] and s[3]]
check(all(s[3] == 1 for s in bad_selected), 'recovery_based_selection_bias_control')
check(Q(sum(s[3] for s in bad_selected), len(bad_selected)) != Q(1,2),
      'recovery_based_selection_bias_control')
negative_controls.append({'name': 'selecting_with_recovery_data',
    'outcome': 'The selected recovery-free bit is biased to probability one; the candidate selection never reads recovery data.'})

# Coarse fourth-power bins give exact telescoping, finite support almost surely
# in the limit, and divergent lower bounds for the mean. Analytic limit steps
# are proved in the report; these identities check their indexing.
for K in (1,2,8,64,256):
    bins = sum((Q(1,k)-Q(1,k+1) for k in range(1,K+1)), Q(0))
    check(bins == 1 - Q(1,K+1), 'offspring_coarse_bin_telescope')
    check(Q(1,K)**4 * K**4 == 1, 'fourth_power_tail')
    check(K**4 * Q(1,K) == K**3, 'infinite_mean_divergent_lower_bound')

# Hereditary bad-probability inequality depends on ξ≥1 and positive mass ≥2.
# The exact candidate has these. Allowing extinction removes the implication.
for x in (Q(1,100),Q(1,3),Q(1,2),Q(99,100)):
    check(x**2 < x, 'positive_offspring_strict_contraction')
    check(Q(1,4)*x + Q(3,4)*x**2 < x,
          'positive_offspring_strict_contraction')
# Supercritical law P(ξ=0)=1/4, P(ξ=2)=3/4 has mean 3/2, and the bad
# probability x=1/3 is a nonzero fixed point of its offspring generating function.
x = Q(1,3)
check(Q(1,4) + Q(3,4)*x*x == x,
      'extinction_breaks_unconditional_quenched_one_negative_control')
check(Q(3,4)*2 > 1,
      'extinction_breaks_unconditional_quenched_one_negative_control')
negative_controls.append({'name': 'allowing_zero_offspring',
    'outcome': 'A supercritical law can have nonzero extinction probability and a nonzero hereditary bad fixed point; ξ≥1 is essential for the candidate unconditional almost-sure conclusion.'})

print(json.dumps({'status':'PASS', 'assertions':sum(checks.values()),
    'groups':dict(sorted(checks.items())),
    'observed_prefix_histories_checked':histories_checked,
    'negative_controls':negative_controls,
    'arithmetic':'exact rational times, exact finite cylinder enumeration',
    'scope':'Finite path witnesses, orientation, recovery endpoints, finite-volume monotonicity, adaptive unused-field independence, and boundary counterexamples. These controls cannot certify infinite limits or the theorem; the accompanying report supplies those deductions.'},
    indent=2, sort_keys=True))
