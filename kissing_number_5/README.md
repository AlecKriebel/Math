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

The proof [`proofs/one_sided_tukey_bound.md`](proofs/one_sided_tukey_bound.md)
establishes \(A(4,1/\sqrt3)\leq33\), \(B(5)\leq38\), and the resulting
origin-depth constraints for any hypothetical 41-point code.  Its exact
\(\mathbb Q(\sqrt3)\) data are stored in
[`certificates/one_sided_tukey_bound.json`](certificates/one_sided_tukey_bound.json)
and checked by
[`verifiers/verify_one_sided_tukey.py`](verifiers/verify_one_sided_tukey.py).

From this directory:

```sh
python3 verifiers/verify_one_sided_tukey.py
python3 -m unittest tests.test_one_sided_tukey -v
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
  tests.test_fixed41_rank_mixture_separator \
  tests.test_sparse_deep_graph_stability \
  tests.test_quantitative_root_system_stability \
  tests.test_split_kernel_abstract \
  tests.test_split_kernel_full_interval -v
```

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
