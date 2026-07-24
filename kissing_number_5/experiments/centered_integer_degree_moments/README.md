# Centered quarter-grid integer degree moments

This experiment tests whether the exact centered quarter-grid pair/triple
pseudodistribution can be the first two moments of actual integer row-degree
vectors.

For a row, let `d_i` count neighbours at inner product `i/4`, with indices
shifted so that `i=-4,-3,...,2`.  Any centered 41-point quarter-grid code
satisfies

```text
sum_i d_i = 40,
sum_i i d_i = -4,
0 <= d_{-4} <= 1,
d_i in Z_{\ge 0}.
```

There are exactly 27,041 such row types.  The certificate gives an integral
quadratic polynomial `P(d)` which is nonnegative on every one of them.
The pair/triple witness prescribes the first two degree moments, however, and
its exact expected value is

```text
-298897510609152269959977158772724413
------------------------------------------------
             3198650000000000000
```

This contradiction refutes that particular pseudodistribution as a
finite-population moment shadow.  It is **not** an upper bound for arbitrary
spherical codes: centering and the quarter-grid support are restrictive.

Run the independent standard-library verifier from the repository root:

```bash
python3 verifiers/verify_centered_quarter_integer_degree_obstruction.py
python3 -m unittest tests.test_centered_quarter_integer_degree_obstruction
```

The polynomial was discovered by a floating-point LP over all row types, then
reconstructed from the exact nullspace of its 16 active types.  The verifier
does not trust either discovery calculation; it reconstructs the prescribed
moments from the source certificate and exhaustively checks every exact
integer row type.

## The obstruction is repairable

The first obstruction is not a proof that the combined relaxation is
infeasible.  We added its inequality to the atomic BV search, reconstructed
the next witness exactly, separated it again, and repeated.  Three exact
finite-population facets were needed.  The third repaired witness,
`repaired_pair_triple_local_3.json`, has SHA-256

```text
df2d3f2e4de387e3af61bf18e03b1d8950928c09b61e01d71a03544dbe19db55
```

and passes all of the following exact checks:

- every full-radial BV block through degree 660, with an analytic proof for
  all degrees at least 661;
- every ordinary pair harmonic through degree 137, with an analytic proof
  for all degrees at least 138;
- the two forced centered kernels and exact ranks `rank(W0)=6`,
  `rank(W1)=5`;
- all 27 sharp low-harmonic rank cuts;
- robust one-sided pair mass, all 18 stratified common-pair rows, and both
  weighted rows;
- an exact positive 18-atom mixture of integer row-degree vectors matching
  every first and second degree moment;
- an exact positive 51-atom local Gram-PSD K5 mixture;
- an exact positive 51-atom local rank-five Gram-PSD K6 mixture.

Thus the claim that centered all-degree pair/BV constraints, present cap
rows, the 27 rank cuts, integer row moments, and local rank-five consistency
through six vertices exclude cardinality 41 is **refuted**.  These are still
separate symmetrized local marginals, not overlapping-subset consistency or
a 41-point Gram matrix.

Reproduce the principal exact checks:

```bash
python3 verifiers/verify_centered_quarter_bv_all_harmonics.py \
  --source experiments/centered_integer_degree_moments/repaired_pair_triple_local_3.json \
  --tail experiments/centered_integer_degree_moments/repaired_local_3_all_harmonics.json

python3 verifiers/verify_centered_quarter_integer_degree_mixture.py

python3 verifiers/verify_centered_quarter_k5_extension.py \
  --source experiments/centered_integer_degree_moments/repaired_pair_triple_local_3.json \
  --certificate experiments/centered_integer_degree_moments/repaired_k5_extension.json

python3 experiments/centered_quarter_k6_rank/verify_direct_k6_triangle_extension.py \
  --source experiments/centered_integer_degree_moments/repaired_pair_triple_local_3.json \
  --certificate experiments/centered_integer_degree_moments/repaired_k6_extension.json
```

The intermediate exact witnesses and their separating facets are retained to
make the cutting-plane history auditable.  `separate.py` reproduces a facet
from a named source; only the standard-library verifier is used to certify
the resulting integer inequality.
