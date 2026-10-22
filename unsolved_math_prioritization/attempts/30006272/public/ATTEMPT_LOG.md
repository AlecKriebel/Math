# Five substantive approaches

This pass addresses the source-corrected all-orbit canonical-basis/Catalan
question, not Ekedahl–Oort stratification. These are five mathematical
approaches in one research pass on 2026-10-04 UTC, not five separate model
sessions. Source identification and update checks are prerequisites and
are not counted as proof attempts.

## 1. Determinantal blocks and direct sparse extrapolation

Derived the complete two-vertex stalk formula using the smaller of the
image and kernel resolutions, in both dimension chambers. Extended it
to products on separated active edges. Tested the tempting unrestricted
sparse formula: ranks (1), homology (1,1) give true polynomial 1+q but
extrapolated polynomial 1. This decisively rejects the simple extrapolation,
while leaving the actual unspecified Catalan extension intact.
Retained argument: PROOF.md §§3–4.

## 2. Gaussian elimination and transverse slices

Constructed an explicit invertible-minor chart, using a Schur complement
and the adjacent zero-composition equations to cancel contractible
summands. Iteration reduces every lower-rank stalk to the origin of
X(k,h), without changing h. This proves independence from unused ambient
ranks, but does not compute the zero stalk for arbitrary homology.
Retained argument: PROOF.md §2.

## 3. Global image/kernel resolution and smallness

Constructed the smooth incidence vector bundle, proved projectivity,
surjectivity and birationality, computed every fiber, and compared its
dimension with independently computed orbit codimensions. Obtained exact
smallness criteria, not just sufficient estimates, and full Gaussian-product
formulas for all n in the two monotonicity chambers. The smallest active
one-edge drop proves necessity. Retained argument: PROOF.md §§1 and 3.

## 4. Semismall decomposition and constrained path combinatorics

Decomposed rank-drop vectors into superlevel intervals. Proved that
semismallness is equivalent to a net homology rise of at most one on
every active interval; equality gives a bounded Motzkin-path condition.
Applied the semismall decomposition theorem with verified rank-one
constant component local systems. Completely evaluated all four strata
for r=(1,1), h=(1,2,1), including the origin polynomial
1+2q+q^2+q^3+q^4. Also exhibited a relevant support leaving the same
semismall class, preventing an unjustified closed recurrence.
Retained argument: PROOF.md §5.

## 5. Full-flag repair and general canonical-basis extension

Added both image and kernel data in a smooth full-flag incidence resolution,
computed its fibers, and tested the non-sparse high-rise case
r=(1,1), h=(1,3,1). All-image and all-kernel maps violate semismallness
(2*3>5 at their respective one-edge drops); full flags are worse (2*4>5).
Translated the established stalk formulas into PBW coefficients and checked
strict negative-degree triangularity. The unrestricted step still needs
additional supported/shifted summands or a different explicit construction;
neither a uniform Catalan rule nor its bar-invariance proof was found.
Retained argument: PROOF.md §6.

## Final state

**Unsolved, 5/5 substantive approaches.** Partial theorems and precise
obstructions are frozen for independent review. No general proof or
counterexample to the source's extension question is claimed. Existing
sparse-support and determinantal results are credited; no novelty claim
is made for the partial formulas or criteria. No remote write, PR, merge,
release, DOI action or third-party communication was performed in this
author pass.
