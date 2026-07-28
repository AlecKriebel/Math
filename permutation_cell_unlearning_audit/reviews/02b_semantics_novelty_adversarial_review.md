# Checkpoint 2B — Semantics and Novelty Adversarial Review

**Date:** 2026-07-28  
**Reviewer role:** standing novelty and scope adversary  
**Initial verdict:** CONDITIONAL GO

## Required scope corrections

1. Describe PC-Audit as a sound, incomplete rejection certificate, never as a
   decision or semidecision procedure.
2. Restrict the sharpness claim to the fixed observed outputs, at the
   population/geometric level, with no target information beyond membership in
   the declared space. Do not claim a statistically optimal finite-sample
   bound.
3. Distinguish route laws conditional on one cloned checkpoint from marginal
   algorithm-level laws over independent training and unlearning reruns.
4. Give stochastic route failures explicit semantics: a failure symbol in the
   output law or a separate failure-probability audit.
5. Restrict the necessity of stateless pairwise commutation to equality for
   every subset endpoint/all request words.
6. State the trusted-affine-promise, common-domain, reachability, exact
   evaluation, and state-injection requirements for finite affine tests.
7. Permit simple multiplicity correction only for a predeclared finite kernel
   family; continuous adaptive kernel selection requires splitting or a
   uniform confidence bound.
8. Mark Chebyshev geometry, Hilbert identities, MMD, cubical confluence,
   affine interpolation, and quadratic deletion algebra as established
   ingredients.
9. Restrict the audit to a single common reset target or law, excluding
   route-conditioned, seed-coupled, or set-valued targets.

## Defensible contribution after correction

PC-Audit supplies the sharp population lower bound obtainable from a fixed
observed route family when the common target is otherwise unconstrained,
together with a valid conservative finite-sample MMD rejection rule. It can
falsify, but cannot certify, all-order retrain-equivalence.

## Disposition

Every requested scope correction was incorporated into the revised checkpoint
before the pass review. The first pass independently caught the false
injectivity adjective on \(W\). After correction, the same reviewer performed
a final clean reread and returned **PASS** with no remaining scope, semantics,
or novelty blocker.
