# Exact-byte audit of the complete 46,872-pair two-linkage theorem

**Independent proof-first hostile audit, 2026-08-12 PDT.**  The immutable
target is

~~~text
research_notes/proof_first_two_linkage_46872_final_theorem.md
SHA-256 dae2a58f170836427ffc053ff931c1909d64ac591d77b971591b0d5814526cde
206 lines, 7865 bytes
~~~

The verdict is **STRICT PASS** at these exact bytes.  The target proves
nonexplosion and positive recurrence on every closed irreducible population
class for every ordered pair of disjoint nontrivial linkage supports in the
three-species binary complex universe, under arbitrary strong labelled
orientations and arbitrary positive rates.  The proof is a disjoint union of
standalone fixed-support theorems.  It contains no statewise switching among
potentials and no finite search over stochastic paths.

## 1. Exact finite universe

The finite certificate and test are frozen at

~~~text
src/final_two_linkage_46872_union_certificate.py
SHA-256 5b249ded4b54801f7eb5ab9ced943ed566216e1228c0e07f3e205b1eef319288

tests/test_final_two_linkage_46872_union_certificate.py
SHA-256 dd51ce074aa43bb4722d176ef4c85face956c924150681d5cae32f3b615c5e76
~~~

All five dedicated tests pass at those exact bytes.  The certificate
explicitly sets recurrence_claim=False and performs support-set identities
only.

There are ten binary complexes.  Assigning each complex to the first support,
the second support, or neither gives \(3^{10}\) assignments.  For either
ordered support, the cases of size zero or one number
\(2^{10}+10\,2^9\).  Inclusion--exclusion restores
\(1+10+10+10\cdot9\) assignments in which both supports have size at most
one.  Thus the ordered disjoint nontrivial universe has

\[
 3^{10}-2(2^{10}+10\,2^9)+(1+10+10+90)=46872
 \tag{1.1}
\]

pairs.  Its exact fingerprint is

~~~text
00446e17dca5ce6b75e86cdc755b5660d7c94b68fa4f3e6f028efa40d02c6c60
~~~

## 2. Independent five-branch replay

I reconstructed the branch sets from their defining support predicates,
independently of the final manifest payload.  They are pairwise disjoint,
their cardinalities are

\[
             27462,\quad 432,\quad 146,\quad 336,\quad 18496,
 \tag{2.1}
\]

and their union is the full 46,872-pair universe.  More precisely,

* the first two sets form the entire 27,894-pair mixed orbit;
* the last three sets form the entire 18,978-pair outside-mixed complement;
* the outside-mixed remainder itself splits disjointly into 11,842
  no-failure and 6,654 failure pairs.

The branch-manifest fingerprint is

~~~text
bd6ae54bff3aed8fc4fedb9255fe0b7377a28dc67404d6a5bea41c6aa4ac1bba
~~~

The asserted identity is therefore a literal set partition, not count-only
arithmetic.

## 3. Completed mixed orbit: 27,462 pairs

The target and its independent audit are

~~~text
target a91e8c31f35312ef4b9063e8f5a48af534861145db2236e662ea6cc1eff8e30e
audit  32eec768b2d8d701664f3ace2b1a7c04fd3790a4811eba5e05d56a8fa903e73b
~~~

The seed-level proof removes all 110 active-only-invariant seeds before
symmetry closure.  The remaining 5,059 seeds are exhausted disjointly by
strict positive invariance, full deficiency zero, nine literal physical
seams, 1,378 corrected tier-pass seeds, and the audited 2,511-pair residual
union.  The independent audit replays every corrected tier incidence and the
full seed partition.

Species permutation conjugates population states and generators, while
linkage reversal changes only the order of two components of the same
network.  These symmetries carry completed seed theorems to exactly 27,462
pairs.  The 282 points also lying in the active-invariant orbit are charged
through eligible seed preimages, never through active-only invariance; the
exclusive 432-pair gap is disjoint.

## 4. Active-invariant orbit gap: 432 pairs

The exact standalone theorem and audit are

~~~text
target 7edab78daabbf7e492851efe5326ccc228adfcb57f02cd5ff55eaa7056e034c8
audit  1110efc0760ed8714fc4bf203739152820f6f9a18cbdc0e92716638a707140fd
~~~

This theorem uses a single fourth-power population factorial.  Its exact
support split is 174 full-deficiency-zero pairs, 234 direct corrected-tier
pairs, and 24 exceptional service pairs.  The exceptional Type I and Type II
generators have literal active-coordinate service estimates.  The proof does
not invoke active-only invariance on an all-active chart, a chart-exit SCC, or
a change of potential.

## 5. Strictly positive invariant: 146 pairs

For every pair in this branch, a vector \(h\in\mathbb R^3_{>0}\) annihilates
the complete support stoichiometric span.  Every labelled reaction vector
for every allowed orientation lies in that span, so \(h\cdot x\) is constant
on a fixed population class.  Each coordinate is bounded by that constant
divided by its positive coefficient.  The class is finite and hence positive
recurrent.  This argument is deliberately stronger than, and does not use,
an invariant positive on only two coordinates.

## 6. Level-set residual: 336 pairs

The exact pair theorem and audit are

~~~text
target 6e9ddcaccd03fe64b1c6a57cbaef052e984eaf7b7e2e87c4df52ca1240787a6c
audit  35b18c365ce954594397b4c48ed55f7d11c847af37594f0fb354517434f76d72
~~~

The certificate supplies the exact level-set normal forms.  The 312
homogeneous incidences are closed by the audited \(h=(1,1,1)\) workload
occupation theorem, including its carrier, dyadic, and common-catalyst
boundary macros.  The 24 anisotropic incidences are closed by the audited
\(h=(1,1,2)\) quotient-Foster theorem.  Both are global classwise
physical-time results; no all-active linear drift is glued to a separate
boundary potential.

\newpage

## 7. Outside-mixed remainder: 18,496 pairs

The exact wrapper and its audit are

~~~text
target e7b08be8b6ca3ff604f3975bdae18b526db532ea1168f25bf21170d8248b5106
audit  192dfc3d79401c57416b582b45aeb0140f0c1ad3e0f90ab80acaae48e3b9a090
~~~

The wrapper uses the exact disjoint support split

\[
 \mathcal R_{18496}
 =\mathcal N_{11842}\mathbin{\dot\cup}\mathcal F_{6654}.
 \tag{7.1}
\]

The 11,842-pair theorem is a statewise population-factorial Foster theorem
whose top-S/global-top-D premise is checked on all 3,010,738 affine-feasible
incidences.  The 6,654-pair theorem uses one actual-target marked factorial:
unconditional all-active corrected-tier episodes, unconditional two-active
AA episodes, and the globally-nonmixed one-active exhaustion with its
cap-free Flat0 killed resolvent.  Both inputs are standalone fixed-pair
theorems, so their union compares no potentials along a trajectory.

## 8. Pairwise composition and positive recurrence

The ordered support pair is immutable for a physical network.  The exact
partition in Section 2 therefore chooses one theorem once and for all.  The
five rows are not regions of state space and are not a finite-state chart
graph.

Each chosen theorem gives finite mean access or return to a finite subset of
the closed irreducible class.  From that finite subset, choose finite labelled
paths to one fixed state.  Their success probabilities have a positive
minimum and their mean durations a finite maximum.  After a failed attempt,
the finite-mean access theorem returns to the finite subset.  Geometric retry
therefore gives finite mean positive return to the fixed state, which is
positive recurrence of the class.

## 9. Nonexplosion

Let \(N(x)=1+|x|_1\).  A binary reaction with a degree-two source cannot
increase total population, because its target also has molecularity at most
two.  Thus all increasing channels have source degree at most one, bounded
jump size, and for a fixed finite network

\[
 \sum_r\lambda_r(x)(|z_r|-|y_r|)^+\le C N(x).
 \tag{9.1}
\]

Localization at the first \(N\)-level \(R\), Dynkin's formula, and Gronwall
give

\[
 \mathbb E_xN(X_{t\wedge\tau_R})\le N(x)e^{Ct}.
 \tag{9.2}
\]

Hence population cannot escape to infinity in finite time.  On every bounded
population set there are finitely many states and bounded total rates, so
population-neutral quadratic clocks cannot accumulate there.  The minimal
CTMC is nonexplosive.

## 10. Exact verdict and claim boundary

The immutable target at SHA \(dae2a58f\ldots\) strictly proves Theorem 1.1 at
the exact full 46,872-pair scope.  Its finite computations establish only
support, tier, affine, and set identities.  All stochastic conclusions come
from the pinned analytic theorems at literal support scopes.  The target does
not reuse the stale 2,511-pair global composition, its chart-exit argument, or
its failed audit.
