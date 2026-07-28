# Checkpoint 1 Adversarial Review — Application Comparison

**Reviewer role:** application/artifact adversary  
**Verdict:** narrow GO for the unlearning audit; NO-GO for microgrid novelty

## Comparison

The reviewer compared two candidate applications:

1. cold-load-pickup microgrid restoration serializability; and
2. a deletion-order inconsistency audit for sequential machine unlearning.

The microgrid candidate was rejected as a novel solved problem because
delayed-exponential cold-load ordering and restoration-sequence optimization
substantially collide with Ucak and Pahwa (1994) and later work. Calling the
same ordering problem “serializability” would mainly reframe established
mathematics.

The unlearning audit received a narrow GO because its useful reduction appears
more specific: two externally equivalent deletion orders provide a retraining-
free falsification witness, with a sharp half-defect lower bound and a
level-controlled stochastic test.

## Mandatory language

The reviewer required the final result to be called a solved **one-sided
inconsistency-audit problem**, not a certificate:

- rejection proves that at least one path violates the common-target tolerance;
- non-rejection proves little;
- the paper must not claim novelty for MMD, Chebyshev radii, affine
  commutators, or broad retraining-free auditing.

