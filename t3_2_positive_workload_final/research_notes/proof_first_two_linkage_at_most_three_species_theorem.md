# Classwise recurrence with two active linkages and at most three species

**Proof-first composition, 2026-08-12 PDT.  Independent audit pending.**
This note composes the exact two-linkage support reduction with the analytic
pair theorems.  Finite computation is used only for finite support and tier
set identities.  No orientation, reaction history, or population box is
searched to prove a stochastic estimate.

## 1. Theorem

> **Theorem 1.1.**  Let every complex of a finite weakly reversible
> stochastic mass-action network have molecularity at most two.  Fix a
> closed irreducible population class \(\Gamma\), delete coordinates constant
> on \(\Gamma\), delete linkages having no enabled source on \(\Gamma\), and
> merge projected linkages which share a projected complex, retaining
> parallel labelled channels and discarding projected zero-displacement
> labels, which make no state transition.  If the reduced network has at most
> three dynamic species and exactly two active linkage classes, then its physical
> CTMC is nonexplosive and positive recurrent on \(\Gamma\).

The assertion is uniform over every strongly connected orientation of each
linkage support and every fixed positive rate vector.

## 2. Exact reduction and the finite support universe

The fixed-class projection is a CTMC conjugacy.  Indeed, if
\(X_i\equiv m_i\) on \(\Gamma\), closure forces every enabled reaction to
have zero \(i\)-increment.  From an enabled complex, a directed path in its
strong linkage is physically executable with one fixed residual population;
hence the deleted stoichiometry is constant throughout that linkage and its
falling-factorial factor is absorbed into the labelled rates.  Projected
strong linkages which share a vertex have strongly connected union, and
parallel propensities add exactly.

A projected zero-displacement label contributes no off-diagonal transition
and may be discarded without changing the CTMC.  An active projected linkage
has at least two distinct vertices; otherwise every one of its labels has
zero displacement.

After merging, the two active linkage supports are disjoint subsets of

\[
 \mathcal C_2=\{0,A,B,C,2A,2B,2C,A+B,A+C,B+C\},           \tag{2.1}
\]

each of size at least two.  Species permutation and linkage ordering are
finite symmetries; neither changes recurrence.

A reaction with a degree-two source cannot increase total population.
Population-increasing channels therefore have aggregate rate
\(O(1+|x|_1)\), and all jumps are bounded.  Finite-sublevel localization
followed by Gronwall proves that total population cannot escape in finite
time; within a population sublevel the state space and total rates are
bounded.  The minimal CTMC is nonexplosive.

## 3. Pre-residual classwise branches

Apply the following tests in the displayed order to an ordered disjoint
support pair.

1. A strictly positive common stoichiometric invariant makes every fixed
   class finite.
2. A common invariant positive on the chart-active coordinates excludes the
   corresponding escape sequence.
3. A weakly reversible deficiency-zero reduced network is complex balanced
   for every positive rate vector.  Anderson--Craciun--Kurtz (2010,
   Theorems 4.1--4.2), together with nonexplosion, gives the normalized
   class-restricted product form and positive recurrence.
4. The exact seven-support, signed-service, and residual-pair physical-time
   theorems cover their literal supports for arbitrary strong orientations
   and rates.
5. If every class-feasible proper tier sequence has a top-S source of a
   D-descending reaction, the class-local restriction of Anderson--Kim
   (2018, journal Theorem 9) gives entropy drift outside a finite classwise
   set and hence positive recurrence.

The support and tier geometry behind item 5 is exact.  Every weak order of
the ten binary monomials is a cell of the rational comparison-plane
arrangement on the normalized nonnegative simplex.  Boundary coordinate
availability is recorded by the cap \(0,1,\ge2\).  This yields 259 exact
descriptor types.  Let \(E\) be the global top stochastic tier and let
\(a_E\) be its deterministic-tier level.  For a linkage support \(L\), put

\[
 U_L=\{y\in L:\text{the deterministic tier of }y\text{ is at least }a_E\}.
\]

Then **every** strong orientation has an \(E\)-sourced descending edge
exactly when

\[
 \text{for some }L,\qquad
 \varnothing\ne U_L\subsetneq L\quad\text{and}\quad U_L\subseteq E. \tag{3.1}
\]

For sufficiency, the first edge of a directed path from \(U_L\) to its
complement works.  Its source is in \(E\), and its target is in a strictly
lower deterministic tier.  For necessity, when (3.1) fails choose, in each
linkage, a strong directed cycle whose unique exit from a nontrivial
\(U_L\) is sourced at a vertex of \(U_L\setminus E\); if \(U_L\) is empty or whole,
that linkage has no descending edge.  Thus (3.1) is an analytic graph
lemma, not an orientation enumeration.

The pre-residual exact count is

\[
\begin{array}{c|rrrrrrrr}
 &\text{input}&\text{finite}&\text{active invariant}&\text{DZ}
 &\text{seven}&\text{signed service}&\text{residual pair}&\text{tier pass}
 \\\hline
 \text{positive shield}&4761&187&110&924&6&2&1&1219\\
 \text{signed shield}&408&0&0&50&0&0&0&159.
\end{array}                                                \tag{3.2}
\]

For completeness, the input of (3.2) is itself exhaustive rather than an
assumed atlas.  In a two-active chart, exchange of the two active species
reduces the order of the six active monomials to the four rational workload
representatives

\[
 (1,1,0),\quad(2,3,0),\quad(1,2,0),\quad(1,3,0).           \tag{3.3}
\]

Assigning each binary complex to the first linkage, the second, or neither
is a finite \(3^{10}\) support problem.  The linkage-wise top alternative is
symbolic: an accessible top path gives an all-clock access episode; a
linkage without such a path is shielded for the chart workload.  If either
linkage is available, that episode ends at an actual physical endpoint.  If
both are shielded, exact nullspace and deficiency calculations give a common
active invariant, deficiency zero, or one of the exact physical service
seams in items 1--4.  The residual shielded/available interfaces, up to
species relabelling, have exactly the positive-invariant and signed shield
supports in the two input rows of (3.2).  They are the input to the tier and
pairwise stopped theorems below, not an unproved consequence of one bounded
access word.  A one-active boundary chart is included by the signed shield
row, not discarded as a finite phase.  The finite certificate verifies these
support identities; the access, invariant, product-form, service, and later
pairwise conclusions are analytic.

Exactly \(2312+199=2511\) ordered pairs remain.  The earlier classifier
which used the absolute global top deterministic tier in (3.1) is retired:
when that tier is wholly disabled, the correct cut is the superlevel
\(U_L\) at the top enabled source tier.  The corrected finite replay changes
208 conservative pair--descriptor labels but no pair-level set or fingerprint.
The stochastic implications in items 1--5 are the mathematical arguments
above and the cited physical-time theorems.

## 4. The affine class filter

For a descriptor weight \(w\), let its positive levels be
\(r_1>\cdots>r_k\), let \(E_r=\{i:w_i=r\}\), and let
\(L_r=\{i:w_i<r\}\).  If \(S\) is the stoichiometric subspace, a real
nonnegative sequence with this descriptor can lie in one affine class only
if, for every positive level \(r\), there is \(v_r\in S\) such that

\[
 (v_r)_i=0\ (i\in L_r),\qquad (v_r)_i>0\ (i\in E_r).       \tag{4.1}
\]

Necessity follows from Gordan's alternative: failure produces an invariant
\(q\in S^\perp\) which vanishes at higher levels and is nonnegative,
nonzero on \(E_r\), contradicting constancy of \(q\cdot x\) after division
by the level-\(r\) scale.  Conversely, rational feasible vectors give the
one-class realization

\[
                  x(n)=b+\sum_{j=1}^k n^{r_j}v_{r_j}.      \tag{4.2}
\]

For the recurrence implication only necessity is needed: an actual bad
sequence in \(\Gamma\) would make its failed descriptor affine feasible.
For 151 of the 2511 pairs, no failed descriptor is affine feasible.  Hence
every tier sequence contained in \(\Gamma\) satisfies (3.1), and the
class-local Anderson--Kim contradiction gives entropy drift outside a
finite subset of \(\Gamma\).  This is the analytic content of
`stoichiometric_gate_feasibility.md`, not an inference from its count.

## 5. Exact disjoint residual union

The 2511-pair set is the disjoint union in Table 1.  Each row names a
pair-level theorem; the finite certificate asserts only its pair set and the
disjoint equality.

| analytic branch | pairs | exact theorem SHA-256 |
|---|---:|---|
| affine classwise tier Foster | 151 | `d91f369d34cadfb28ddb872df8fb9f6d17799ec207da29933037f55ae95f0407` |
| rank-two return | 14 | `821478a8c4410a371f99fa9df02e18ab5dbcc7c24aafa78f7d0db20cb6ab0bbe` |
| all-active reversible top | 51 | `3f8c3662ed55d13133ef67f5e4e75e7ef9057075fa6e755faf33420e71ea0a26` |
| rank-one, no promotion | 141 | `adc325b740dd18bfa4cc9ee53c2a3632f3660df589369a14cc4d9c3ce16992c1` |
| post-rank-one one-active | 92 | `b4944d0bed95f92978a0eaf08336744813804ca7ddd6af0c4cd84005361c6113` |
| two-active promotion | 36 | `2f52d0ed580c70916fbe75f13e8ea09d77af53940bdf21048b43423830620f97` |
| suppressed promotion | 4 | `edbe0c4affe9735fb7cb650f9e0e3d653c75e7b37df5b5c8c8b838f43565a518` |
| critical one-active | 15 | `01a7827e96874171bc0f96be4fd05edb2a7ce607398be312b1378e762f62ea82` |
| universal one-active net | 1212 | `0ab1cff97dee0594db9981db451a9f26799a6f2cdd5cf5d00a19f03e12c6ea9c` |
| exact common-factorial | 26 | `c78e53f11aeb981b415a90a486583b409608ef2256b73b9e063db48ac8d4fc88` |
| easy common-workload | 416 | `4764849b05915b9005d68ac885c512a906af439430e8db8a7131f04645224e29` |
| rank-two common scalar | 13 | `0be8e4e0bb28fa2086c434ee459b7d2f2ab061c67f9d45d2ecdb6a059a764478` |
| rank-two stopped service | 7 | `e8045791f98334d706e058adab0f838f4bf902a71b08bc1b24a4f3493474355b` |
| hard common-workload | 333 | `ddcc1f054febae9f08bb4d78bd66569ff4eebdd367b5cb4479b9029c960ecf84` |

The counts sum to 2511.  The row fingerprint is

```text
9e9c6be443216f3a6d05795fcf0dcf25170ce020371c6bffde25eb316e52ad27
```

and the finite union payload is

```text
4a1542367400376de42fec24ddabe328bd3489c91c246e8d70def32bcd78cb33.
```

These hashes are regression evidence for (finite) set equality only.

## 6. Why the pair theorems compose without a cross-branch potential switch

Fix the reduced support pair, orientation, rates, and class.  Table 1 assigns
that **single pair** to exactly one row.  Its analytic theorem quantifies over
every escaping sequence of that pair, includes all physical clocks and every
cutoff-causing reaction, controls the actual terminal endpoints and physical
duration, and proves finite mean return to a finite target.  No trajectory
switches from one Table 1 row to another, because the support pair is fixed.

Thus no comparison between potentials belonging to different rows is
required.  Most rows use one population or reachable-marked potential
throughout.  The rank-two-return theorem instead has an internal, proved
two-stage argument: a proper outer workload returns the process to its core,
and a second core workload supplies the strict return estimate; its cleanup
lemma proves that the handoff has integrable physical time and endpoint cost.
This is a standalone Foster proof for that fixed pair, not a claim that its
two internal workloads are literally one common episode potential.  The
distinction is harmless here because Table 1 composes completed pair-level
recurrence theorems, rather than splicing their episodes.

In reflected rows, a hit of the finite marked target is recorded when it
occurs, marks are propagated through the first return used for accounting,
and the finite marked cycle occupation measure projects to an invariant
probability for the physical irreducible class.

Every Table 1 theorem therefore gives positive recurrence of its assigned
pair.  Sections 3--5 exhaust all possible reduced two-linkage pairs, proving
Theorem 1.1. \(\square\)

## 7. Exact audit boundary

Every analytic dependency in Sections 3--5 now has a strict scoped
exact-byte pass.  The three literal pre-residual physical seams are audited at
SHA-256

```text
e7e76b76cd1371f98d19da0a1f5362ab4a0696548fba62028b29ccd2950617c9.
```

This pass is deliberately nonmonotone: the signed-service theorem applies
only to its displayed supports, not to strict supersets.  The finite branch
map uses precisely those literal supports, so no deletion or restoration
argument is being imported.

Exact-byte independent passes also exist for the corrected affine branch,
suppressed-4, universal-1212, easy-416, rank-two-13, stopped-7, and hard-333.
A consolidated proof-first replay gives strict passes to the rank-one-141,
post-rank-one-92, critical-15, and exact-26 rows at audit SHA-256

```text
d68293a3d47f8f708b604467e90fdd1801f3b3ed583d07fb53e7b9e64b987239.
```

The remaining three residual rows have strict exact-byte passes at targets

```text
rank-two 14     821478a8c4410a371f99fa9df02e18ab5dbcc7c24aafa78f7d0db20cb6ab0bbe
all-active 51   3f8c3662ed55d13133ef67f5e4e75e7ef9057075fa6e755faf33420e71ea0a26
promotion 36    2f52d0ed580c70916fbe75f13e8ea09d77af53940bdf21048b43423830620f97
```

under consolidated audit SHA-256

```text
13f328883635ae832570620f3fabde0081af0358a0a5c69bcd316236f633df02.
```

Thus the only remaining audit gate for Theorem 1.1 is a hostile replay of
these exact composition bytes.  No global theorem is claimed by this note.
