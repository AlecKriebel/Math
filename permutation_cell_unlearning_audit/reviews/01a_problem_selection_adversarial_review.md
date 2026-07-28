# Checkpoint 1 Adversarial Review — Problem Selection

**Reviewer role:** standing novelty adversary  
**Verdict on broad machine-unlearning application:** NO-GO  
**Verdict on narrowed target-free falsification problem:** GO

## Broad-claim rejection

The broad statement that deletion order matters in machine unlearning is not a
defensible contribution. Direct and adjacent collisions include:

- Kumar, Nadimi, and Gogineni (2026), who directly study different orderings of
  the same forget samples under gradient-ascent unlearning and derive a local
  second-order path defect.
- Existing sequential and adaptive unlearning analyses.
- Recent order-independent continual-unlearning constructions.
- Work on adversarial deletion ordering and robustness thresholds.

Any claim to discover deletion-order noncommutativity would therefore be fatal.

## Surviving question sent for re-review

The revised problem does not claim discovery of path dependence. It asks whether
two or more deletion-order outputs can provide a sharp, statistically controlled
lower bound against every common retraining target, without producing that
target. It is explicitly a one-sided necessary-condition audit.

The reviewer was asked to search specifically for:

1. a deletion-order Chebyshev/half-diameter target-error certificate;
2. its finite-sample distributional version; and
3. an affine-basis completeness audit for all-order affine deletion maps.

## Narrowed-search result

The reviewer found no mapped source combining deletion-order metamorphic tests
with the optimal target-free radius lower bound and a finite-sample stochastic
margin rule to falsify an all-order retrain-equivalence tolerance without
constructing a retrained model.

The accepted positioning is:

> A gold-standard-free, one-sided falsification audit for universal all-order
> retrain-equivalence claims.

The reviewer emphasized that MMD auditing, equivalence testing, metamorphic
testing, Chebyshev radii, cubical confluence, and deletion-order sensitivity are
all prior art separately.

Additional constraints:

- use an infimum in arbitrary metric spaces because a center need not exist;
- predeclare or validly select the kernel and correct for multiple tested pairs;
- do not confuse ordinary two-sample rejection with a tolerance-margin test;
- contextual Boolean-cube squares can still be exponential in number;
- audit partial-domain and failure equality separately;
- promote the “zero defect proves no fidelity” warning to a formal proposition.
