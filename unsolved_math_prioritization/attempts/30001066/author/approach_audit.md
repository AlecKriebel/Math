# Five bounded approaches

## 1. Ordinary Helly in affine-line coordinates

Dimension `2d-2` does not make transversal constraints convex. For the rectangle `[0,1] x [0,1]` in coordinates `(x,t)`, the nearby graphs `x=-3epsilon t` and `x=3epsilon(t-1)` meet opposite endpoints. Their coefficientwise average, `x=-3epsilon/2`, misses the rectangle. This holds for every `epsilon>0`, arbitrarily near the axis. Extra coordinates can be confined to a box factor containing zero. Outcome: exact failure of local convexity, so ordinary Helly cannot be invoked just from the chart dimension.

## 2. Alternating separated slabs

Three boxes with sign pattern positive/negative/positive force one affine coordinate to be zero by interpolation. Independent blocks give `3d-3` strictly disjoint compact bodies. Continuous exact deletion motions establish minimality, not merely first-order rigidity. Outcome: complete lower-bound theorem in `proof.md`; it does not settle finiteness of a bound at fixed `d`.

## 3. First-order positive spanning

Under a trivial linearized feasible cone, at most `4d-4` body constraints isolate the line. The positive spanning lemma and normalized-sequence argument are proved in `proof.md`. The quadratic pair there demonstrates why isolation does not force the hypothesis. Outcome: a conditional upper bound with an explicit missing higher-order step.

## 4. Polytope/quadric classification

The disjoint-polytope result in Aronov et al. is three-dimensional and excludes target lines in facet planes. Our boxes deliberately have contact segments in those planes. The paper's arbitrarily large construction uses overlapping bodies. Invertible affine transformations preserve intersections, and separate longitudinal translations change the actual line constraints. Neither operation therefore imports that example into the target class without a new proof. Outcome: no verified conversion, and no unrestricted upper bound.

## 5. Regularization or topological transfer

Positive outer parallel bodies destroy isolation of the original line: choose one original intersection point in each body; sufficiently close lines meet the small balls around all those points. Inner approximation can destroy the original transversal. Consequently approximation by nicer shapes needs additional pinning-preservation and limiting arguments, such as a uniform isolation neighborhood. No such argument was obtained.

A topological Helly proof likewise needs contractibility/homology control of the actual local intersections, across the relevant subfamilies. Known shape-specific direction-cone results cannot be transferred solely from ambient dimension. Outcome: the degenerate local configurations remain the precise gap.

## Classification

The candidate `2d-1` is refuted for `d>=3`. Any general `h(d)` must be at least `3d-3`; the existence of `h(d)` is unresolved in this investigation. The conditional first-order subclass has bound `4d-4`. No novelty claim is made for the known lower-bound phenomenon. Finite code checks supplement the written all-dimensional proofs; they do not establish the unrestricted theorem.
