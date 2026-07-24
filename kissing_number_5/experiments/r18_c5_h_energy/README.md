# Five-point `C5` quartic-energy audit

This directory studies the following self-contained lemma.

Let \(z_0,\ldots,z_4\) be unit vectors whose Gram matrix is positive
semidefinite.  Suppose the five cycle inner products are in
\([-1,-1/2]\), while the five chord inner products are in
\([-1/2,1/2]\).  With

\[
h(t)=t^2(t^2-\tfrac14),
\]

the target is

\[
\sum_{0\le i<j<5} h(\langle z_i,z_j\rangle)\le \tfrac32.
\]

The actual application has strict cycle inequalities.  Proving the statement
on the closed domain is therefore sufficient.

Work here is independent of the frozen `r18_weighted_q_energy_independent_audit`
directory.  Numerical searches and metric-polytope vertex checks are discovery
artifacts only unless accompanied by an exact analytic certificate.

## Certified results in this directory

1. `lambda_max_c5_cell.md` proves the separately scoped frame bound
   \(\lambda_{\max}(G)\le3\) on the closed `C5` sign cell.
2. `adjacent_merge_certificate.md` proves
   \(\sum h(\langle z_i,z_j\rangle)\le3/2\) on the minimal angular-metric face
   \(\sum_iA_i=3\).  Its computer-assisted step is checked from scratch by
   `verify_adjacent_merge.py` using integer arithmetic.

Neither result currently controls the part of the metric polytope with
\(\sum_iA_i>3\), so this directory does not yet contain a proof of the full
five-point energy lemma.

## Verification

With Python 3.14 or later:

```bash
python3 verify_lambda_max_c5_cell.py
python3 test_verify_lambda_max_c5_cell.py
python3 verify_adjacent_merge.py
python3 test_verify_adjacent_merge.py
```

The verifiers have no third-party dependencies.  The `search_*.py` file is
floating-point discovery code and is not part of either proof.
