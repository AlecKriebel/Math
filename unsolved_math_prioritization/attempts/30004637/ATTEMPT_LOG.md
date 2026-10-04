# Five-approach attempt log

Problem 30004637 / OWR-4990379-007. All checkpoints on 2026-10-04 UTC.
Completion percentages below are rough planning judgments toward the broad
source goal, not measured probabilities or claims that fractional theorem
proofs imply fractional resolutions. Five substantive approach families were
worked through in this research pass; tool calls are not additional attempts.

## Readiness checkpoint — 06:59 UTC — approximately 5%

The exact OWR target was recovered after the catalogue failed. Its binary
special case is explicit, but its full generality and the word “fast” have no
specified computational model. The primary source's later numerical method
was read in full. No prior repository attempt was found. This is a valid
research question, with substantial existing numerical work and no verified
full resolution in the checked literature.

## Approach 1/5: endpoint scaling — proof saved 07:05 UTC — approximately 8%

Mechanism: transfer ordinary Sinkhorn's linear endpoint propagation. Derived
the one-ancestor pure-birth generating function and its strictly positive
second derivative. Even constant terminal data produce a nonlinear map.
Outcome: a precise obstruction to the unchanged linear-kernel step.
Gap: no obstruction to other fast methods and no controlled nonlinear endpoint
solver. Retired the naive transfer rather than describing it as a general
impossibility result.

## Approach 2/5: local convex proximal steps — 07:05 UTC — approximately 12%

Mechanism: perspective duality and projection onto a convex sublevel set.
Proved the projection formula and its monotone scalar equation, including the
correct squared derivative, an explicit outer bracket and inner residual bound.
Compared carefully with the inspected preprint's Lemma 6.17; this mechanism is
credited to existing work and not claimed as novel.
Outcome: a rigorous binary-offspring local operation, later tested in 144 cases.
Gap: scalar conditioning, arbitrary offspring laws, global iteration count,
and continuum error remain uncontrolled.

## Approach 3/5: accelerate the affine operation — 07:05 UTC — approximately 18%

Mechanism: spatial Fourier diagonalization of a specified periodic
backward-Euler continuity constraint. Derived every temporal diagonal and
off-diagonal entry. Proved an O(TN log N + TN) arithmetic projection with
O(TN) storage and included T=1 and N=1.
Outcome: the claimed projection was compared with dense direct linear algebra
on 60 small grids, including zero diffusion.
Gap: the affine projection does not enforce positivity and is not a full
optimization method; no continuum consistency/convergence theorem is claimed.

## Approach 4/5: global finite-grid rate — 07:05 UTC — approximately 20%

Mechanism: a bounded positive-density domain, explicit Hessian bound, and
projected gradient. Proved an O(1/n) objective bound and a separate valid
primal/dual gap certificate.
Outcome: exact finite-dimensional statements with all oracle and feasibility
assumptions stated.
Gap: the cheap affine projection from Approach 3 is not the boxed projection
required by the rate theorem. Positivity, singular endpoints, quantitative
mesh error, and reliable inexact computation remain genuine gaps. No unsupported
composition of the two results is made.

## Approach 5/5: recent surrogate route — 07:08 UTC — approximately 18%

Mechanism: replace the binary branching growth cost by its quadratic Taylor
model and transfer a scalable WFR solver. Inspected the June 2026 USB v2,
including its new Appendix C.11 numerical comparisons. Proved the global
quartic objective-error bound on the same admissible class and the failure of
uniform relative penalty equivalence at large growth.
Outcome: an explicit limited approximation guarantee, not identification of
RUOT with ordinary diffusion-free WFR.
Gap: growth/mass control of true optimizers, removal of the model changes,
and controlled solution of general RUOT. The recent method retains this gap.

## Verification and freeze — 07:14 UTC — approximately 18%

Three exact symbolic identities, 144 local proximal cases, 60 affine projection
cases, and 33 surrogate checks pass. Floating checks are regression tests, not
interval certificates or formal proofs. The analytic arguments are the proof
artifacts. The author packet is frozen with SHA-256 hashes for fresh independent
review. Status is **partial / unresolved**, with no full-solution, novelty,
priority, or impossibility claim. No remote changes have been made.
