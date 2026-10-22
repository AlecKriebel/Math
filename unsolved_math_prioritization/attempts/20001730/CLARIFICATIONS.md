# Separate clarification of the frozen conditional proof

5 October 2026. This supplements, without replacing or modifying, the author proof with SHA-256 `77354e318baf41c5afc0d062b041fb7ca1a41b2380e2d8da78d058cfd342a93c` and the fresh independent audit with SHA-256 `e801ad818bc0211c43a07da2da80f3273050c2b7f6a754f74efc4dbcddb8f39c`.

## A chart-local uniform-radius set

Read Sections 3.3–3.4 in the ordinary second-countable smooth-foliation setting specified by the audit. Let V range over the countable open target foliation boxes, with smaller interiors covering M. Disintegration and the common rebasing identity give a measurable set of good plaques in each V, on each of which the local signed defect H_x vanishes whenever gx lies in that plaque and x is an allowed good basepoint. Restrict to the completed-measurable full-measure set where these local conclusions hold; take Borel representatives when needed.

For each such V and positive integer j, restrict further to basepoints x with gx in a good plaque of V and

    dist_M(gx, M minus V) > 1/j.

The distance condition is a continuous ambient test; good plaques and allowed basepoints are measurable by the stated kernel/disintegration assumptions. A leafwise path starting at gx with length less than 1/j cannot leave V, because ambient distance is no larger than its leafwise length. While it remains in the foliation box it remains in the same plaque. Consequently the intrinsic 1/j-ball about gx is contained in the local zero-defect plaque. This proves exactly the uniform-radius property needed in the recurrence step.

The countably many choices of box and j cover almost every allowed basepoint. At least one has positive measure. Choose a Borel subset of the same measure and apply backward recurrence to that set with delta=1/j. Exact defect covariance and intrinsic backward contraction then give the same compact-capture and whole-leaf conclusion as the frozen proof. This avoids treating an arbitrary whole intrinsic ball as one chart plaque or inferring that an ambient null set is null on every leaf.

This is an expansion of the audit's recommended reading, not an added construction or an additional dynamical conclusion. All strong Section 2 hypotheses remain essential, and the conclusion still holds only after passage to a possibly smaller invariant conull D'.

## Metric in the toral example

Equip T2 times T2 with the standard product flat metric inherited from Euclidean R2 times R2. Along the first expanding eigendirection, both f and g multiply intrinsic arclength by lambda=(3+sqrt(5))/2, and their arclength pushforwards have density lambda inverse. The whole-leaf Radon condition uses intrinsic topology, including for dense immersed leaves.

## Distinct orbit leaves do not assert genericity

The explicit point with sqrt(2) and sqrt(3) coordinates is used to prove that the leaves L_(m,n) are pairwise distinct. The irrationality and quadratic-field argument proves distinctness for all integer labels. No Haar-genericity, equidistribution, or statistical orbit claim is made or needed. The example takes D=M and removes its explicitly constructed invariant Haar-null union of exceptional leaves to obtain D'=M minus S.

## Remaining gap

The common invariant ergodic probability, whole-leaf family, measurable kernels, exact Gibbs rebasing, conditional classes, and transport/equivalence laws are assumed. This clarification does not construct them from the general AIM input. The original problem remains unsolved in this work.
