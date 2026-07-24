# Common-pair capacity hierarchy: discovery record

> **Status: REFUTED as a full-hierarchy barrier.**  The numerical and exact
> calculations below concern cumulative base thresholds only.  Exact
> base-color strata reject the five-node candidate (by 88 and 120) and the
> seven-node source witness.  See
> `../proofs/common_pair_capacity_hierarchy_adversarial_audit.md`.

This file records discovery computations only.  The exact theorem and exact
certificate checks are in:

- `proofs/common_pair_capacity_hierarchy.md`;
- `certificates/common_pair_capacity_degree4_pseudodistribution.json`; and
- `verifiers/verify_common_pair_capacity_hierarchy.py`.

## Software

- Python 3.14.6
- NumPy 2.5.1
- SciPy 1.18.0
- CVXPY 1.9.2
- CLARABEL through CVXPY

The exact verifier uses only the Python standard library.

## Five-node integral reoptimization

Command:

```text
PYTHONPATH=. .venv/bin/python \
  experiments/search_common_pair_capacity_hierarchy.py --support five
```

This is the degree-four local-hybrid cutting-plane model with:

- exact pair/triple marginals;
- all common-pair capacity rows on the support;
- the previously used local wedge and forced-clique rows;
- a necessary outer rational C047 band;
- two necessary outer centered-skew bands;
- degree-four Bachoc--Vallentin PSD blocks; and
- full colored-degree covariance.

The continuous warm start became positive after 43 separation rounds.  The
subsequent integral MILP produced the triple counts now stored in the exact
certificate.  Its strongest hierarchy row is saturated:

```text
a=-11/25, b=499/1000, p=249001/280000, M=1:
left=219, right=219.
```

The solver-reported common harmonic margin was approximately
\(2.9348510\cdot10^{-5}\).  This number is not used in the proof.  Exact
principal-minor checks replace it.

## Seven-node continuous reoptimization

Command:

```text
PYTHONPATH=. .venv/bin/python \
  experiments/search_common_pair_capacity_hierarchy.py --support seven
```

The pair measure is fixed to the exact seven-node all-harmonic witness.  Its
51 triple-orbit weights are reoptimized subject to exact marginals (entered
as floating-point coefficients), every hierarchy row, and all degree-four
Bachoc--Vallentin PSD blocks.  CLARABEL reported:

```text
status optimal
degree-four common PSD margin 0.00369886412584361
minimum orbit weight 1.3977760428919073e-05
```

This numerical solve is only a tractability check.  The stronger result is
the independent exact audit: the original rational all-harmonic witness
already satisfies every hierarchy row, with minimum positive exact slack
\[
 \frac{155474701215499}{60000000000000}.
\]
Thus no numerical solver claim is needed to demonstrate the hierarchy's
limit on the seven-node support.

## Interpretation

The hierarchy decisively refutes all four earlier local five-node triple
witnesses, but it does not close that support: reoptimization finds a new
exact degree-four pseudodistribution saturating the strongest cut.  It also
does not refute the much stronger seven-node all-harmonic
pseudodistribution.  Neither surviving object is asserted to be a graph or
a spherical code.
