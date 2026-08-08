# Hostile endpoint report

Date: 2026-08-07 (America/Los_Angeles)

No literature search or external contact was used.

## Outcome

The concentrated falsification cycle did **not** produce a product
counterexample or an endpoint simultaneous amplifier.  Therefore neither
the product conjecture nor the exact threshold is resolved by this branch.

The useful output is an independent exact verifier, one coefficient-positive
boundary-family theorem, a resolved extreme-conditioning artifact, and an
exact restriction on any fixed affine Bd--dB dual multiplier.

Write

\[
 x={\rho_{\rm Bd}(G,3/2)\over\rho_{\rm Bd}(K_n,3/2)},\qquad
 y={\rho_{\rm dB}(G,3/2)\over\rho_{\rm dB}(K_n,3/2)}.
\]

## Exact one-chord certificate

Split four vertices into two pairs.  Give all four cross edges weight one,
one internal pair weight `a>=0`, and omit the other internal edge.  Direct
solution of the strongly lumped two-count chain gives

\[
\rho_{\rm Bd}={27(66a^5+1333a^4+8629a^3+23300a^2+26300a+10000)
\over5(972a^5+17469a^4+110011a^3+299900a^2+341900a+130000)},
\]

\[
\rho_{\rm dB}={450a^4+6110a^3+27602a^2+48219a+28512
\over4(450a^4+5075a^3+20362a^2+33953a+20196)}.
\]

After normalization by the `K_4` baselines, the numerators of `2-x-y`,
`1-xy`, and `1-y` are coefficient-positive.  The first two are printed by
the verifier.  This proves strict product and normalized-arithmetic gaps for
all `a>=0`, and shows that the nearest five-edge numerical competitor is not
a boundary counterexample.

This is a class theorem only, not an order-four classification and not a
universal obstruction.

## Exact affine-multiplier corridor

Suppose one tries the fixed affine separator

\[
 \lambda x+(1-\lambda)y\le1.                         \tag{1}
\]

An exact rational seven-vertex windmill-like graph in the verifier has

```text
blade       center-left     center-right       internal
(1,2)       642311627470    641177352713       2172410361743
(3,4)       5               1665053            4231492313836
(5,6)       79              71                 5921340201086
```

with no other edges.  It has

\[
 x=0.827701009618\ldots,\qquad y=1.016737744242\ldots
\]

and violates (1) at `lambda=177/2000`.  The unit star on ten vertices has
crossing multiplier `0.582602655719...` and violates (1) at `lambda=7/12`.
Thus (1), if universal, necessarily has

\[
 {177\over2000}<\lambda<{7\over12}.                  \tag{2}
\]

The balanced choice `lambda=1/2` remains compatible with every exact and
numerical test here.  Relation (2) is guidance for a dual-certificate search;
it is not itself the desired separator.

## Numerical scope

The discovery implementation analytically deletes self-loops, checks the
linear residual and harmonic range, and optimizes edge logarithms.  The
cycle included:

- all 38 connected labelled supports of order four for `P`, `M`, and
  `(x+y)/2`;
- deterministic and random complete/sparse supports of orders five, six,
  and seven, including stars, paths, cycles, and irregular core-periphery
  supports;
- log-weight spans through 22;
- the known dB-amplifying three-blade support, optimized directly for the
  nonsmooth minimum and Pareto scalarizations.

No resolved `P>1` or `M>1` point was found.  These are numerical observations
only.  The exact verifier checks ten selected rational graphs from both
sides of the Pareto frontier.

### Order-eight adjoint-gradient continuation

`search_endpoint_adjoint.py` differentiates the full transient subset
systems analytically with respect to every logarithmic edge weight.  A
finite-difference audit on a generic weighted `K_5` agreed in both rules to
better than `10^-10`; this validates the discovery gradient, not a theorem.

On complete support at order eight, six hostile starts for the normalized
product, five for the balanced arithmetic mean, and five for a smooth
minimum surrogate were optimized with log-weight bounds `[-14,14]`.  No
endpoint violation was found.  The best product converged to `K_8` within
floating precision; the best nontrivial normalized arithmetic score was
`0.999257121546...`, and the best simultaneous minimum was
`0.999031296393...`.  These values are **NUMERICAL EVIDENCE ONLY** and are
not used in any universal claim.

## Reproduction

From the repository root:

```bash
.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_hostile_exact/verify_endpoint_candidates.py
```

The order-eight discovery continuation can be replayed, with no exact claim,
using for example

```bash
.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_hostile_exact/search_endpoint_adjoint.py --n 8 --objective product
```

Expected final lines include:

```text
PASS: 10 exact hostile rational endpoint graphs
PASS: exact affine-multiplier witnesses force lambda > 177/2000 and lambda < 7/12 (...)
```

## Classification

| Claim | Status |
|---|---|
| product inequality at `r=3/2` | **OPEN** |
| endpoint simultaneous amplifier | **NOT FOUND** |
| no simultaneous amplification at `r=3/2` | **OPEN** |
| one-chord boundary family | **PROVED** |
| separated-star floating violation | **FALSIFIED / EXACTLY REFUTED** |
| fixed affine multiplier outside (2) | **EXACTLY REFUTED** |
| balanced normalized-arithmetic separator | **OPEN** |
