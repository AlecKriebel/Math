# Attempt 4 of 5: rational counterexamples and exact component decisions

## Goal and result

Try to turn a possible locked unit chain into a finitely checkable algebraic
object, rather than infer locking from failed numerical motion planning. We
prove an explicit local clearance bound and show that any counterexample at a
fixed bar count has a rational-coordinate counterexample at that same count.
Standard semialgebraic component algorithms decide each fixed-count question
in principle. None is executed here, and this is not a decision for all counts.

## Edge coordinates and local clearance

Fix `p_0=0`, which removes only translation. A unit chain is represented by
`d=(d_1,...,d_n)` in `(S²)^n`, with `p_j=sum_{i<=j} d_i`. Let `F_n` be the
strict-simple configurations. For `d in F_n`, define

    delta = min dist(e_i,e_j) over |i-j|>1,
    eta   = min |d_i+d_{i+1}| over 1<=i<n.

Use `+infinity` for the minimum over an empty list. Compactness and disjointness
give `delta>0`. Strict simplicity excludes antiparallel adjacent directed bars,
so `eta>0` as well.

Let `b_i` be other unit directions with `|b_i-d_i|<epsilon`, where

    epsilon < min(1/2, delta/(4n), eta/4).               (1)

Interpolate by

    d_i(t)=((1-t)d_i+t b_i)/|(1-t)d_i+t b_i|.            (2)

The unnormalized vector differs from `d_i` by less than `epsilon`, and its
norm is at least `1-epsilon>0`. By the reverse triangle inequality,

    |d_i(t)-d_i| < 2 epsilon.

Every vertex, and hence every corresponding point of every bar, moves less
than `2n epsilon`. The distance between a nonadjacent pair remains greater
than `delta-4n epsilon>0`. Meanwhile

    |d_i(t)+d_{i+1}(t)| > eta-4 epsilon > 0,

so no adjacent overlap occurs. Thus (2) is a strict-simple unit-bar motion
connecting `d` to `b`. Equation (1) is a quantitative same-component
neighborhood, not merely a static perturbation test.

## Consequences for connectivity and rational data

These neighborhoods show `F_n` is open and locally path connected in `(S²)^n`.
Its connected components therefore equal its path components and are open.
All straight chains are in one component: rotate their common unit direction
continuously on the sphere. Restoring arbitrary translations adds a connected
factor and does not affect this conclusion. Consequently the original
connectedness question is equivalent to every strict chain being straightenable.

Rational points are dense on `S²`, as is clear from stereographic coordinates

    q(s,t)=(2s,2t,1-s²-t²)/(1+s²+t²),   s,t in Q,

together with the omitted rational pole. Choose rational unit `b_i` within
(1). Their partial sums give rational vertices, and (2) keeps the chain in
the original component. Hence:

    If a locked unit n-chain exists, a locked unit n-chain with rational
    coordinates exists. In fact every locked configuration has a relative
    open neighborhood consisting entirely of locked configurations.       (3)

The last statement means openness inside the strict unit-chain space. A
boundary configuration with self-contact is not covered. Likewise, (3) does
not say that an arbitrary rational approximation is safe without a clearance
bound.

## A correct finite algebraic formulation

For every nonadjacent pair, nonintersection is exactly the assertion that
there do not exist `s,t in [0,1]` satisfying

    sum_{k<i} d_k + s d_i = sum_{k<j} d_k + t d_j.       (4)

Together with `|d_i|²=1` and `|d_i+d_{i+1}|²>0`, these quantified polynomial
conditions describe `F_n`. Quantifier elimination gives a semialgebraic
description. General algorithms compute the connected components of arbitrary
semialgebraic sets; for example Basu–Pollack–Roy,
[*Computing the First Betti Number and Describing the Connected Components
of Semi-algebraic Sets*](https://arxiv.org/abs/math/0603248).

Thus for a specified finite `n`, one can in principle decide whether `F_n`
has one component, or decide whether a rational candidate and a rational
straight chain share a component. This statement uses algorithms for general
semialgebraic sets: replacing the strict free space by its algebraic closure,
or applying a theorem only for smooth closed algebraic sets, would wrongly
include collision paths.

One could enumerate `n` and compute each component decomposition. If a locked
count exists this eventually finds one. No bound on the first locked `n` is
known here, so the process need not halt when every `F_n` is connected.
Rational candidate enumeration plus a valid exact component oracle has the
same limitation.

## What has and has not been certified

The local-motion estimate and rational reduction are proved above. No roadmap,
CAD, component count, or disconnectedness certificate was computed. A numerical
planner failing to find a path is not substituted for such a certificate.
Attempt 3's convex dependence still proves only failure of an axis condition.

This route supplies rigorous standards for a future counterexample search but
does not produce a locked equilateral chain or a universal straightening proof.
It uses standard semialgebraic machinery and makes no novelty claim.
