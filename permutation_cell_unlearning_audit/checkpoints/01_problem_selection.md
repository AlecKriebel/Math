# Checkpoint 1 — Problem Selection and Claim Boundary

**Date:** 2026-07-28  
**Status:** GO for the sharply scoped one-sided audit

## Selected problem

Let a fixed trained checkpoint receive a finite set of non-adaptive deletion
requests. The external endpoint is the retained dataset, so request permutations
are equivalent at the dataset level. A stateful approximate-unlearning protocol
may nevertheless return different models or output distributions.

Suppose the intended deterministic target is a selected retrained model \(t_D\),
or in the stochastic case a selected retraining distribution \(Q_D\). Full
retraining is too expensive to use merely as an audit oracle.

The problem is to construct a low-cost, target-free procedure that can soundly
**reject** a claim of the form

\[
  d(Y_\pi,T_D)\le \varepsilon
  \quad\text{for every permitted deletion order }\pi.
\]

The procedure need not, and generally cannot, certify successful deletion when
the competing paths agree.

## NCS formulation

- External states are subsets of deletion requests already processed.
- Edges add one deletion request.
- Relation cells exchange adjacent independent deletions.
- Carry response is the implemented sequential unlearning update.
- Reset response is a selected retraining procedure on the retained dataset.
- A cell value defect compares two deletion orders; partial domains would record
  asymmetric numerical or certification failure separately.

This is the Boolean-cube intervention presentation native to NCS.

## Anticipated solution

For observed path outputs \(Y=\{y_\pi\}\) in a metric space, define

\[
  r(Y)=\inf_z\max_\pi d(y_\pi,z).
\]

Every common target \(t\) obeys

\[
  \max_\pi d(y_\pi,t)\ge r(Y)\ge \tfrac12\operatorname{diam}(Y).
\]

For two normed-space endpoints, the sharp value is
\(\|y_{ij}-y_{ji}\|/2\). Therefore a cell defect exceeding
\(2\varepsilon\) falsifies a uniform \(\varepsilon\)-target claim without
computing the target.

The intended stochastic extension lower-bounds a metric between the two route
distributions with finite-sample confidence and then applies the same cell
argument.

## Direct collisions and exclusions

1. Gradient-ascent unlearning path dependence under different orderings of the
   same forget samples is already documented in 2026. We do not claim its
   discovery or its second-order commutator.
2. Training-history path dependence and impossibility of path-oblivious retrain
   equivalence are already documented. Our paths begin at one fixed trained
   checkpoint and exchange deletion requests.
3. General retraining-free audits appeared in 2026. The proposed result is only
   a necessary-condition rejection test and uses no verification model.
4. Metamorphic testing already uses symmetry relations when a test oracle is
   unavailable. NCS supplies the presented path structure, directional failure
   signature, filling logic, and target-error interpretation.
5. Chebyshev radii, affine interpolation, influence functions, kernel two-sample
   distances, and concentration bounds are established ingredients.

## Falsification conditions

Terminate or reframe the project if a mapped source already:

- compares two permutations of the same deletion set specifically to obtain the
  sharp half-defect lower bound against every common retraining target;
- gives the corresponding level-controlled stochastic distribution test; and
- develops the pair-cell/affine-basis audit as a complete all-order test for
  affine deletion operators.

Even if no exact collision is found, the final paper must call the result a
candidate application and not a priority proof.

## Final adversarial decision

The standing novelty adversary completed the narrowed search and returned GO.
No mapped source combined deletion-order metamorphic tests with the optimal
output-only radius lower bound and a finite-sample stochastic margin rule for
falsifying an all-order retrain-equivalence tolerance without a retrained
model.

The reviewer imposed four qualifications:

1. “Largest” means largest bound obtainable from the observed route outputs
   when the target is otherwise unconstrained in the declared metric space.
2. A stochastic audit must lower-bound a distance margin, not merely reject
   equality of route laws.
3. Boolean-cube square checks reduce factorial path enumeration but do not in
   general remove the exponentially many contextual squares.
4. Zero radius proves route consistency only; all routes can agree at an
   arbitrarily wrong output.
