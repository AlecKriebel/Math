# Five-attempt research log

Date: 2026-10-03. All times below are UTC. Completion estimates measure progress
toward a **new underlying strict Calabi–Yau threefold satisfying the full target**,
not literature review or package preparation. The five numbered entries are
substantive mathematical approaches, not a count of tool calls.

## Source gate, 16:46–16:50

The problem endpoint was attempted first and was inaccessible. The pinned
problem record identified the official OWR report. The official report and the
original cited research papers were then read. The narrower new-threefold
question is explicit in OWR Question 12. The report's two known examples cannot
be counted as resolving that question. No mathematically matching completed
repository attempt was found in the bounded search described in SOURCE_GATE.md.
Initial completion estimate: 0%.

## Attempt 1 — 16:50: vary hyperbolic integral matrices

**Mechanism.** Replace the matrix parameter in the order-three scalar torus
quotient with the family having characteristic polynomial t³−mt+1, m≥3.

**Work.** Wrote the integral inverse, calculated determinant −1, isolated all
three roots by signs, and used the trace-zero relation to order their absolute
values. Computed both dynamical degrees. Checked that the matrix commutes with
the scalar group and that both it and its inverse lift through the invariant
blow-up. The published degree criterion establishes primitivity.

**Outcome.** A verified family of dynamical systems on X3, already encompassed
by the known construction mechanism. No new underlying variety. Taking powers
also leaves X3 unchanged. Complete argument: PROOF.md §2.

**Stop reason.** The parameter changes the map, not the requested threefold.
Completion estimate: 0%. Not reopened by testing more matrices.

## Attempt 2 — 16:51: change the quotient group or abelian variety

**Mechanism.** Vary the scalar quotient, then extend to arbitrary finite groups
with only isolated nonfree points.

**Work.** The invariant volume form forces a nontrivial scalar action to have
order three. For the broader isolated quotient, a general ample surface avoids
the singular set. Its étale pullback to the abelian cover trivializes the ambient
tangent bundle, forcing c2·ν*H=0. Verified the applicable birational
c2-contraction classification and its simple-connectedness restriction. Checked
the second known example by exact cyclotomic arithmetic, giving d2>d1>1.

**Outcome.** This isolated-quotient route yields only X3 and X7 under the stated
strictness assumptions. Quotients with fixed curves are outside this obstruction.
Complete argument: PROOF.md §3.

**Stop reason.** The broad construction class is already classified; dropping
its hypotheses would require a genuinely different construction with a proof
of all target properties. Completion estimate: 0%.

## Attempt 3 — 16:52: descend surface dynamics through a diagonal quotient

**Mechanism.** Start with a positive-entropy surface map, take a product with an
elliptic curve, and quotient/resolve to try to obtain a strict threefold.

**Work.** Constructed the quotient morphism to E/G_E. Proved that every
normalizing product automorphism semiconjugates to an automorphism of this
curve, and that the semiconjugacy persists as a rational map on any birational
model. This explicitly defeats primitivity, even if strictness can be achieved.

**Outcome.** The proposed induced maps are imprimitive. This does not assert
that every abstract automorphism of every such threefold is imprimitive.
Complete argument: PROOF.md §4.

**Stop reason.** Positive entropy alone does not remove the invariant fibration.
Completion estimate: 0%.

## Attempt 4 — 16:53: regularize known birational maps

**Mechanism.** Use low-Picard-rank or Wehler birational dynamics and seek a
biregular strict Calabi–Yau model.

**Work.** Proved directly from cubic intersection invariance that a rank-two
integral divisor action cannot have spectral radius greater than one; included
the rank-one case. Checked the stronger existing rank-two finiteness theorem.
Verified that generic three-dimensional Wehler varieties have trivial regular
automorphism group. Calculated the canonical discrepancy for an ordinary
blow-up to identify why arbitrary resolution loses the Calabi–Yau property.

**Outcome.** These immediate upgrades fail. General crepant changes of model
are not excluded. Complete argument: PROOF.md §5.

**Stop reason.** No candidate outside the proved obstructions was constructed.
Completion estimate: 0%.

## Attempt 5 — 16:54–16:56: nef eigenclasses, contractions, and deformations

**Mechanism.** Use an expanding nef eigenclass to produce a useful contraction,
or deform one of the two known examples.

**Work.** Proved D³=c2·D=0 and the irrationality of the expanding eigenray.
Identified the missing rationality and semiampleness steps. Using the original
maximal-contraction factorization direction, proved that any nonzero semiample
c2-null class on a primitive example forces X3 or X7. Checked the infinitesimal
deformation obstruction from the known examples' rigidity.

**Outcome.** A precise conditional obstruction, agreeing with the published
OWR proposition. It is not an unconditional nonexistence proof. Local
rigidity closes only the small-deformation route. Complete argument: PROOF.md §6.

**Stop reason.** The route transfers the central difficulty to open rationality
and semiampleness assertions. Completion estimate: 0%.

## Verification and disposition, 17:00 onward

The standard-library checker separately exercises the stated algebra using
exact rational and cyclotomic calculations. Its finite matrix checks supplement
the parameter-uniform proof; they do not replace it. No numeric approximation
is used as evidence of an exact inequality. Source texts and PDFs are excluded
from the public package. The author snapshot is frozen for an independent audit.

Disposition: exhausted after five attempts; exact target unresolved. No claim
of novelty is attached to the known examples or the obstruction arguments.
