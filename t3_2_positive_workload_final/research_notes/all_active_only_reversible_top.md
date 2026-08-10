# All-active-only reversible-top Foster theorem

## 1. Exact scope and status

This note isolates a pair-level consequence of the independently audited
all-active generator theorem.  It concerns residual support pairs for which

1. every affine-stoichiometrically feasible failed descriptor is
   three-active;
2. the fixed whole-top linkage has two complexes, rank one, and deficiency
   zero; and
3. every failed descriptor satisfies the curvature-cofactor hypothesis of
   Proposition 5.2 in *three_active_shell_gluing_gate.md*.

The exact selector contains 51 ordered support pairs.  All 51 lie in the
positive-invariant table and none lies in the signed table.  Its SHA-256 is

```text
cc1d4b0941588f7b664a3266076789e548ae1f675924854eff18c9552d86e3ea
```

The finite selector is executable.  The analytic theorem below has been
independently replayed against the exact selector, including the boundary
descriptors and the classwise Foster step.  It is not a global T3-2 claim.

## 2. One potential on every divergent sequence

Fix one selected support pair, one closed irreducible population class
\(\Gamma\), arbitrary strongly connected orientations, and positive rates.
Let the fixed whole-top linkage be \(T=\{y,z\}\).  Strong connectivity on
two vertices supplies both directions (after aggregating parallel labelled
channels).  Choose \(\theta>0\) so that

\[
 \kappa_{yz}\theta^y=\kappa_{zy}\theta^z .             \tag{2.1}
\]

Use the rate-adjusted entropy

\[
 V_\theta(x)=
 \sum_i\left[x_i\left(\log\frac{x_i}{\theta_i}-1\right)
                  +\theta_i\right].                     \tag{2.2}
\]

with \(0\log0=0\).  It is proper and bounded below on
\(\mathbb N_0^3\).  This is exactly the potential in Proposition 5.2 of
the all-active note, which proves, for every affine-feasible failed
sequence of this pair,

\[
 {\cal L}V_\theta(x_n)\longrightarrow-\infty .          \tag{2.3}
\]

The curvature-cofactor premise is exactly what makes the positive discrete
remainder of the reversible top reaction no faster than the other
linkage's maximal source tier.  The strict lower-linkage exit then dominates
it.  No stationary start or shell mixing assertion is used.

Now take any divergent sequence in \(\Gamma\) which is not in one of those
failed descriptors.  Pass to an exact D-tier subsequence.  If its descriptor
were affine infeasible, it could not be realized in the fixed affine class
containing \(\Gamma\).  Hence it satisfies the ordinary top-S
descending-source condition.  The Anderson--Kim entropy estimate
applies.  The difference between (2.2) and ordinary entropy is the fixed
affine function

\[
 -\sum_i x_i\log\theta_i+\sum_i(\theta_i-1).             \tag{2.3a}
\]

Every reaction therefore changes the correction by a bounded constant.
The forced negative logarithmic exit diverges, while positive lower-tier
terms are bounded by the standard \(g e^{-g}\) estimate.  This argument is
unchanged when some coordinates are capped: an exact boundary descriptor
that failed the descending-source condition would be an affine-feasible
failed descriptor, whereas the selector certifies that every such
descriptor is three-active.  Therefore (2.3) also holds along this
subsequence.

We have proved the sequence statement

\[
 \text{every divergent sequence in }\Gamma
 \text{ has a subsequence on which }{\cal L}V_\theta\to-\infty . \tag{2.4}
\]

If \(\{{\cal L}V_\theta>-1\}\cap\Gamma\) were infinite, local finiteness of
\(\mathbb N_0^3\) would select a divergent sequence inside it, contradicting
(2.4).  Thus

\[
 {\cal L}V_\theta\le-1
 \quad\hbox{outside a finite subset of }\Gamma .         \tag{2.5}
\]

## 3. Classwise recurrence

Shift \(V_\theta\) by its finite lower bound so that it is nonnegative.  The
CTMC is nonexplosive.  In a binary network, a reaction sourced at a
bimolecular complex cannot increase total population; every
population-increasing reaction therefore has source molecularity at most
one, and its total rate is affine.  Localized Dynkin applied to (2.5), then
monotone removal of the finite-sublevel and time localizations using
nonexplosion and nonnegativity, gives

\[
 \mathbb E_x\tau_{K_\Gamma}\le V_\theta(x)<\infty        \tag{3.1}
\]

for the finite exceptional set (enlarged by one state if it is empty).
From a state in this finite set, the first holding time and the finitely
many possible successor states have finite expected cost to hit the set
again.  The finite trace therefore has a positive recurrent state;
irreducibility of \(\Gamma\) promotes this to every state of \(\Gamma\).
Hence every closed class is positive recurrent.

> **Theorem 3.1 (independently audited).** Every one of the 51 selected support
> pairs is positive recurrent on every closed irreducible class, for every
> strongly connected orientation and every positive vector of present
> rates.

This theorem uses one potential throughout; it has no chart-switch toll.
It neither covers the twelve all-active curvature-seam pairs nor promotes a
pair with a feasible one- or two-active failure.

## 4. Reproduction

```text
PYTHONPATH=src python3 -B src/all_active_only_recurrence.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_all_active_only_recurrence.py -v
```

The executable certifies the selector and its disjoint support count.  In
particular it checks all 209 selected failed incidences against the
all-active incidence table, the fixed whole-top support, and the exact
curvature-cofactor predicate.  It does not computationally prove the
analytic Foster argument.

## 5. Independent audit record

The proof replay checked the following three load-bearing implications.

1. Every one of the 209 failed incidences selected by the script occurs in
   the certified all-active table, has the pair's fixed two-node rank-one
   deficiency-zero whole-top linkage, and satisfies Proposition 5.2's
   cofactor hypothesis.  There is no selected boundary failure.
2. On every passing descriptor, including every realizable boundary
   descriptor, (2.3a) has bounded reaction increments and hence cannot
   cancel the diverging logarithmic exit in the Anderson--Kim argument.
3. The subsequence assertion (2.4) makes the bad-generator set finite on
   each class, and the stopped Dynkin argument above yields finite mean
   return.  No uniform finite box for an inactive coordinate and no
   embedded-jump occupation estimate enters this proof.

The original audit-pending draft wrote (2.2) with \(\log(x_i!)\).  That
formula is not literally the potential in Proposition 5.2: its difference
from ordinary entropy is not affine.  The certified statement uses the
continuous entropy (2.2), for which both the failed-cone proposition and
the passing-cone bounded-correction argument apply exactly.
