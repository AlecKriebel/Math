# Checkpoint 2A — Formal Proof Adversarial Review

**Date:** 2026-07-28  
**Reviewer role:** independent proof auditor  
**Initial verdict:** NO-GO as written; GO after surgical corrections

## Blocking findings

1. The global ridge commutation characterization omitted the degenerate
   amplitude \(\tau=0\), when both update maps are identities. The theorem must
   restrict the iff statement to \(\tau>0\), separately state the zero-amplitude
   case, and define the unsuperscripted maps used later.
2. The first affine reconstruction formula tried to invert an ambient
   \(d\times r\) basis matrix when the reachable affine hull can have
   \(r<d\). The correct formulation uses the injective direction map \(V\) and
   the corresponding output-difference map \(W\), recovering only the
   restriction to the reachable hull.
3. The zero-defect no-go must exclude infinite-valued bounds, and a positive
   radius rejects only when it exceeds the declared tolerance. A merely
   positive radius does not reject a positive-tolerance claim.
4. The protocol cannot promise tractable computation of a Chebyshev radius in
   an arbitrary represented metric space. It may compute the radius when a
   certified solver exists or return a sound weaker bound such as half the
   diameter.

## Additional corrections requested

- Require a nonempty restricted target set \(T\), \(0<\delta<1\), and \(q\ge2\)
  where used.
- State that pairwise commutation is necessary only for equality at every
  subset endpoint/all request words, not merely for equality of all
  permutations at one full-set endpoint.
- Identify the triangle inequality or Theorem 2 as the source of the
  two-route lower bound.
- Define the Neumann remainder and verify the induced \(H\)-norm of \(PG\).
- Make the response-order statement conditional on a start state independent
  of \(\tau\).

## Verified material

The reviewer independently verified the Chebyshev-radius proof, Hilbert
identity, MMD concentration constants, radius perturbation bound,
contextual-square count and completeness, corrected affine-basis theorem,
ridge commutator, objective constants \(1/8\) and \(\lambda/8\),
Sherman--Morrison--Woodbury sign, and Neumann expansion.

## Disposition

All blocking and minor corrections were incorporated into the revised
checkpoint before the pass review. The first pass found one new one-line error:
the prose incorrectly called \(W\), as well as \(V\), injective. After that
correction, the same reviewer performed a full reread and returned **PASS**.
