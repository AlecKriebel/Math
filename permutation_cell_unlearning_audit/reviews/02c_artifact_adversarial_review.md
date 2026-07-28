# Checkpoint 2C — Artifact and Implementation Adversarial Review

**Date:** 2026-07-28  
**Reviewer role:** artifact adversary  
**Initial verdict:** CONDITIONAL GO

## Independent checks

- Verified the MMD bounded-difference constant and family-wise union bound.
- Verified that the minimum-enclosing-ball radius is 1-Lipschitz under the
  paired point perturbation used in the confidence bound.
- Verified the affine-basis and ridge calculations, subject to the same
  lower-dimensional-coordinate and \(\tau=0\) corrections found by the proof
  auditor.

## Hidden assumptions exposed

- Replicates must estimate the same conditional or marginal law named by the
  guarantee.
- Each within-route replicate reruns the complete route with a fresh seed;
  cross-route common random numbers are permitted.
- The kernel diagonal bound must be global and known.
- The implemented statistic must be the RKHS norm of empirical means, not the
  unbiased estimator of squared MMD.
- Kernel, bandwidth, routes, tolerance, and transformations must be fixed
  independently or validly adjusted.
- An approximate minimum-enclosing-ball solver needs a certified lower bound
  or an explicit optimization-error subtraction.
- Random route failures, affine promises, floating-point conditioning, common
  domains, and state-injection access all require explicit treatment.
- “Strongest” applies only to exact population outputs/laws, not the proposed
  finite-sample confidence rule.

## Disposition

The revised formal checkpoint now states each of these assumptions and
limitations and received **PASS** on rereview. The first computational review
reproduced the JSON byte-for-byte and verified the arithmetic, but returned
NO-GO for publication labels: ambiguous metric names, top-25 checks described
too broadly, a one-seed event called coverage, a floating-point radius described
as certified, effect-calibrated stochastic design described as predeclared,
and incomplete provenance. Those findings define the required computation
rereview.
