# Five-Dimensional Kissing Number Research Program

This directory is a self-contained research program for determining
\(\tau(5)=A(5,1/2)\), the largest cardinality of a subset \(C\subset S^4\)
whose distinct points satisfy \(\langle x,y\rangle\leq 1/2\).

## Current rigorous baseline

\[
40\leq \tau(5)\leq 44.
\]

The lower bound is independently verified here using the exact \(D_5\) root
configuration.  The upper bound is the published baseline imported from
Mittelmann--Vallentin; it is not a resolution of the problem.

Nothing in this repository assumes that 40 is optimal.  Construction searches
for 41, 42, 43, and 44 points run independently of the obstruction program.

## Integrity rules

- `CLAIMS_LEDGER.md` is authoritative about epistemic status.
- Floating-point output is never promoted to a theorem without an exact or
  directed-interval certificate and an independent verifier.
- Run verifiers with ordinary Python, not `python -O`; their exact rejection
  checks deliberately use assertions.
- Search code belongs under `experiments/`; certificate checkers belong under
  `verifiers/`.
- A restriction to symmetric, antipodal, lattice, rigid, rational, or
  few-distance codes is never treated as universal without a proof.
- No external person is contacted on behalf of this project.

## Reproduce the certified lower bound

From this directory, using Python 3.11 or later:

```sh
python3 verifiers/verify_d5.py certificates/d5_roots.json
python3 -m unittest discover -s tests -v
```

Both commands use only the Python standard library and exact integer
arithmetic.  The stored integer vector \(r\) denotes the unit vector
\(r/\sqrt2\).

## Reproduce the certified one-sided bound

The exact degree-11 cap-SDP certificate in
[`proofs/one_sided_cap_degree11_bound.md`](proofs/one_sided_cap_degree11_bound.md)
proves
\[
B(5)\leq34.
\]
It uses rational Gram factors and a complete exact Bernstein subdivision of
the full three-dimensional cap-pair domain.  Consequently, every open
hemisphere contains at least seven points of a hypothetical 41-code, and
deleting any six points leaves the origin in the interior of the remaining
convex hull.  A separately implemented adversarial test rebuilds all 650
polynomial terms and all 5,995 tree leaves.  The independent
tangent-projection lemma proves that every point has at least seven strictly
negative neighbors.

The strengthened certificate in
[`proofs/one_sided_cap_degree11_robust.md`](proofs/one_sided_cap_degree11_robust.md)
uses the same positive kernel on the larger closed cap
\(\langle e,x\rangle\ge-1/300\).  Its exact objective is
\(16939/484=35-1/484\), so a hypothetical 41-code has at least seven
points below \(-1/300\) and seven above \(1/300\) in every direction.
The independent verifier rebuilds all 650 terms and all 6,053 Bernstein
leaves using exact rational arithmetic.

The earlier proof
[`proofs/one_sided_tukey_bound.md`](proofs/one_sided_tukey_bound.md)
also establishes \(A(4,1/\sqrt3)\leq33\) exactly.  It remains a dependency
of the tangent-neighborhood lemma.  The degree-10 cap proof
\(B(5)\le35\) remains as a smaller independent certificate.

From this directory:

```sh
python3 verifiers/verify_one_sided_cap_degree11.py
python3 verifiers/verify_one_sided_cap_degree11_robust.py
python3 verifiers/verify_one_sided_cap_degree10.py
python3 verifiers/verify_tangent_nonnegative_neighborhood.py
python3 verifiers/verify_one_sided_tukey.py
python3 -m unittest \
  tests.test_one_sided_cap_degree11 \
  tests.test_one_sided_cap_degree11_independent_audit \
  tests.test_one_sided_cap_degree11_robust \
  tests.test_one_sided_cap_degree10 \
  tests.test_tangent_nonnegative_neighborhood \
  tests.test_one_sided_tukey -v
```

## Reproduce the rank and frame certificates

The exact cap certificate in
[`proofs/improved_frame_cap_bound.md`](proofs/improved_frame_cap_bound.md)
proves \(A(4,7123/12877)\le30\) and the strict frame floor
\((15059/40000)I_5\).  The notes
[`proofs/rank_five_spectral_moment.md`](proofs/rank_five_spectral_moment.md)
and
[`proofs/rank_five_four_cycle_moments.md`](proofs/rank_five_four_cycle_moments.md)
give sharp rank-five spectral constraints and exact cycle expansions.  These
are necessary conditions and witness separators, not a 41-point exclusion.

From this directory:

```sh
python3 verifiers/verify_improved_frame_cap_bound.py
python3 verifiers/verify_rank_five_spectral_moment.py
python3 verifiers/verify_weighted_residual_barrier.py
python3 verifiers/verify_local_hybrid_degree3.py
python3 verifiers/verify_local_hybrid_degree3_rank.py
python3 verifiers/verify_local_hybrid_degree3_rank_color.py
python3 verifiers/verify_harmonic_combination_centered_skew.py
python3 verifiers/verify_harmonic_rank_frame_barrier.py
python3 verifiers/verify_local5_degree5_necessary_rank_separator.py
python3 verifiers/verify_edge_conditioned_k4_exact_obstruction.py
python3 verifiers/verify_anchored_negative_cap_kernel.py
python3 verifiers/verify_positive_circuit_pair_catalog.py
python3 verifiers/verify_fixed41_rank_mixture_separator.py
python3 verifiers/verify_sparse_deep_graph_stability.py
python3 verifiers/verify_quantitative_root_system_stability.py
python3 verifiers/verify_split_kernel_abstract.py
python3 verifiers/verify_split_kernel_full_interval.py
python3 -m unittest \
  tests.test_improved_frame_cap_bound \
  tests.test_rank_five_spectral_moment \
  tests.test_weighted_residual_barrier \
  tests.test_local_hybrid_degree3 \
  tests.test_local_hybrid_degree3_rank \
  tests.test_local_hybrid_degree3_rank_color \
  tests.test_harmonic_combination_centered_skew \
  tests.test_harmonic_rank_frame_barrier \
  tests.test_local5_degree5_necessary_rank_separator \
  tests.test_edge_conditioned_k4_exact_obstruction \
  tests.test_anchored_negative_cap_kernel \
  tests.test_positive_circuit_pair_catalog \
  tests.test_fixed41_rank_mixture_separator \
  tests.test_sparse_deep_graph_stability \
  tests.test_quantitative_root_system_stability \
  tests.test_split_kernel_abstract \
  tests.test_split_kernel_full_interval -v
```

## Reproduce the Lorentzian structure and countermodel

The exact note
[`proofs/lorentzian_inertia_graph.md`](proofs/lorentzian_inertia_graph.md)
proves the inertia, Perron interval, six-core star-complement formulation,
and critical rank-one-shift lemma for \(A=2G-J\).  It also supplies an exact
rational 41-row countermodel showing that separate inertia, interval, graph,
depth, and unnormalized-circuit conditions do not recover the Gram lift.
The countermodel is explicitly indefinite and is not a kissing code.

```sh
python3 verifiers/verify_lorentzian_inertia_graph.py
python3 -m unittest tests.test_lorentzian_inertia_graph -v
```

## Reproduce the anchored barrier and tight-frame challenge

The exact note
[`proofs/anchored_local_energy_bv_barrier.md`](proofs/anchored_local_energy_bv_barrier.md)
shows why a natural pure-BV row-energy bound cannot cross the rank-five
threshold \(36/5\).  Construction round 8 exactly exhausts cyclic
41-vector harmonic tight frames, including all row-sign switchings, and
records separate numerical searches on larger UNTF families.  Neither result
is a universal upper bound.

```sh
PYTHONPATH=. .venv/bin/python \
  verifiers/verify_anchored_local_energy_bv_barrier.py
PYTHONPATH=. .venv/bin/python -m unittest \
  tests.test_anchored_local_energy_bv_barrier -v
PYTHONPATH=. .venv/bin/python \
  experiments/construction_round8_tight_frames/check_results.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.construction_round8_tight_frames.test_results -v
```

The independent checker for construction round 9 recomputes all maxima,
Gram spectra, active components, and the finite extracted core graph:

```sh
PYTHONPATH=. .venv/bin/python -m \
  experiments.construction_round9_core_rattler.check_results \
  experiments/construction_round9_core_rattler/results/core_rattler_portfolio.json
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.construction_round9_core_rattler.test_core_rattler_search -v
```

All round-9 configurations remain above \(1/2\); these commands reproduce a
numerical construction search, not an upper-bound certificate.

## Reproduce the corrected common-pair audit

The original cumulative-only pseudo-certificate is retained with an explicit
refutation notice.  The corrected exact-stratum theorem and fixed-support
Farkas certificate are independently checked here:

```sh
PYTHONPATH=. .venv/bin/python \
  verifiers/verify_common_pair_capacity_stratified_dual.py
PYTHONPATH=. .venv/bin/python -m unittest \
  tests.test_common_pair_capacity_hierarchy \
  tests.test_common_pair_capacity_hierarchy_independent_audit \
  tests.test_common_pair_capacity_stratified_dual -v
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.continuous_rank_bv_search.test_search -v
sha256sum -c \
  experiments/continuous_rank_bv_search/MANIFEST.sha256
```

The last two commands reproduce a discovery-only continuous-grid barrier:
corrected capacities eliminate the old witnesses, but reoptimized
finite-grid measures survive.  They are explicitly numerical-only.

## Layout

- `STATUS.md`: live theorem-level status and bottlenecks.
- `APPROACH_REGISTRY.md`: routes grouped by mathematical mechanism.
- `CLAIMS_LEDGER.md`: status of every important claim.
- `research_log/`: timestamped research checkpoints.
- `proofs/`: human-readable proofs and candidate arguments.
- `experiments/`: discovery code and numerical output.
- `certificates/`: exact or interval-certified proof objects.
- `verifiers/`: small programs that check certificates without trusting search
  software.
- `tests/`: positive and negative tests for verifiers.
- `literature/`: primary-source notes and imported hypotheses.

## Exact target

A resolution must establish one integer \(K\) by:

1. giving an exact \(K\)-point code in \(S^4\), and
2. proving that no \((K+1)\)-point code exists.

Until both items have passed independent adversarial audit, the project remains
incomplete.
