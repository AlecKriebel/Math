# A strict-disjointness lower bound for local line pinning

Version: 1-reconstructed, 2026-10-06. This is a rebuilt author packet, not an independently accepted solution.

## Scope, sources and priority

Problem 30001066 / OWR-2090-019 asks whether a dimension-dependent bound controls the subfamily needed to isolate a specified transversal of arbitrary pairwise disjoint convex sets. **That broad question is not resolved here.** We prove that the suggested bound `2d-1` fails for every `d>=3`, even for compact, full-dimensional, pairwise disjoint boxes: any possible general bound `h(d)` must be at least `3d-3`.

The six-object obstruction in dimension three is known. Cheong, Goaoc, Holmsen and Petitjean credit a six-cylinder example to Günter Rote [2, section 6]. No novelty claim is made for the lower-bound phenomenon or this product construction. Our deliverable is an explicit compact box realization, a complete all-dimensional proof, and exact continuous deletion certificates. The printed cylinders in [2] are not strictly pairwise disjoint as closed sets: two same-side cylinders touch. The boxes below establish the required separation independently.

The source report [1, p. 2543] proves the `2d-1` bound for disjoint balls and poses further generalization. Its extensions have shape or regularity assumptions; “similar statements” does not assert the same numerical bound for all convex sets. In [3], the upper bound six for disjoint polytopes is restricted to `R^3` and excludes facet planes containing the pinned line. Their unbounded construction allows intersecting polytopes. Neither resolves the unrestricted disjoint-body question.

## Line-space convention

A transversal may meet a body on its boundary. A family pins a line when that line is isolated in its transversal space with the ordinary affine-line topology. Minimality means that deletion of any body destroys isolation. This local question is different from a global Helly theorem for the existence of any transversal.

Near the last coordinate axis in `R^d`, every unoriented line has a unique expression

`L(a,b)={(a_1+b_1 t,...,a_(d-1)+b_(d-1)t,t):t in R}`.

These are coordinates in `R^(2d-2)`. Selecting orientation along increasing `t` is only a local convention and does not change isolation.

## Theorem 1: `3d-3` disjoint boxes minimally pin an axis

Put `k=d-1>=1`. For `j=0,...,k-1` and `r=0,1,2`, let `q=3j+r`. Define `B_(j,r)` by:

- last coordinate in `[2q,2q+1]`;
- transverse coordinate `j+1` in `[0,1]` for `r=0,2`, and in `[-1,0]` for `r=1`;
- every other transverse coordinate in `[-1,1]`.

The `3k` boxes have the last coordinate axis as their unique common transversal. Every deletion has non-axis transversals arbitrarily close to that axis.

### Compactness, dimension and separation

Every defining interval is closed, bounded and has positive length. The boxes are compact convex bodies with nonempty interiors. Distinct last-coordinate intervals have gaps of at least one, so even the boundaries of distinct boxes are disjoint. The axis meets each box in its full last-coordinate interval.

### Exact pinning proof

A line with constant last coordinate cannot meet two distinct slabs. Any common transversal therefore has the displayed form `L(a,b)`, globally.

Fix `j`, and choose parameters `t_0,t_1,t_2` at which the line intersects the three boxes of its block. Their slabs imply `t_0<t_1<t_2`. The affine function `f(t)=a_(j+1)+b_(j+1)t` has `f(t_0)>=0`, `f(t_1)<=0`, `f(t_2)>=0`. But

`f(t_1)=((t_2-t_1)/(t_2-t_0))f(t_0)+((t_1-t_0)/(t_2-t_0))f(t_2)`.

Both coefficients are strictly positive. All three values must consequently vanish. Two distinct zeros force `f` to vanish identically. Applying this to every transverse coordinate proves that the common line is the axis. This is global uniqueness, and hence also local pinning.

### Exact deletion motions, valid for all sufficiently small real parameters

Delete `B_(j,r)` and put `s=6j`. All transverse coordinates of the following line are zero except coordinate `j+1`, which is `epsilon f_r(t)`, where

- `f_0(t)=t-(s+4)`;
- `f_1(t)=1`;
- `f_2(t)=(s+1)-t`.

Take any real `0<epsilon<=1/(6k+2)`. For `0<=t<=6k-1`, every displayed function has absolute value less than `6k+2`; thus other blocks permit the moving coordinate.

At the retained slab midpoints of its own block, the unscaled values are `(-3/2,1/2)` after deleting the first box, `(1,1)` after deleting the middle box, and `(1/2,-3/2)` after deleting the last box. They have the required signs and scaled magnitude at most one. At each other box's midpoint, its active coordinate remains zero and all other coordinates lie in `[-1,1]`. Thus the line meets every retained box.

It also misses the omitted box: `f_0<0` on its positive slab, `f_1>0` on its negative slab, and `f_2<0` on its positive slab. The motions are nonconstant as lines and converge to the axis as `epsilon` tends to zero. Each deletion is therefore unpinned. A smaller subfamily inherits the motions of any containing one-box deletion. QED.

### Six boxes in dimension three

In order `(x,y,z)`, the boxes are:

1. `[0,1] x [-1,1] x [0,1]`
2. `[-1,0] x [-1,1] x [2,3]`
3. `[0,1] x [-1,1] x [4,5]`
4. `[-1,1] x [0,1] x [6,7]`
5. `[-1,1] x [-1,0] x [8,9]`
6. `[-1,1] x [0,1] x [10,11]`

They minimally pin the z-axis, whereas no five of them pin it. All line intersections and motions respect the same slab order. The construction does not use orientation reversals or another distant component of transversal space. Its contact segments lie in facet planes, which is allowed in the target problem.

Since `3d-3>2d-1` exactly when `d>2`, the suggested bound is false in every dimension at least three. Increasing dimension does not show unboundedness at a fixed dimension.

## Theorem 2: what a first-order argument actually proves

Let `m=2d-2`. Suppose local transversals satisfy finitely many differentiable necessary inequalities `g_i(u)>=0`, each necessary for meeting its individual associated body locally, with `g_i(0)=0`. Suppose moreover that

`{v: Dg_i(0)v>=0 for all i}={0}`.

Then at most `2m=4d-4` bodies suffice to pin the line. This is a conditional sufficient theorem, not a consequence of pinning alone.

### Positive spanning lemma and proof

A finite set positively spanning `R^m` contains a positively spanning subset of size at most `2m`. Induct on `m`, ignoring zero vectors. In positive dimension choose a minimal positive dependence supported on `S`; it exists because the cone is the entire space. Its coefficients are strictly positive. The nullspace of its columns is one-dimensional: otherwise a second independent dependence permits an adjustment of the positive coefficient vector until a coefficient first reaches zero, contradicting minimality. Thus `r=dim(span S)=|S|-1>=1`. Also `cone(S)=span(S)`, because the negative of each generator is a positive combination of the others.

The other vectors project to a positive spanning set in the quotient by `span(S)`. By induction choose at most `2(m-r)` projected vectors, and lift them. Together with `S` they positively span: any error in `span(S)` is corrected with its conical generators. The count is `(r+1)+2(m-r)<=2m`. The zero-dimensional base is empty. QED.

### First-order isolation proof

The gradients positively span `R^m`: otherwise separation of their closed finitely generated cone gives a nonzero vector with all the displayed inequalities nonnegative, contrary to the hypothesis. Select at most `2m` gradients by the lemma. If the selected inequalities allowed feasible nonzero `u_n->0`, compactness gives a subsequence of `u_n/||u_n||` tending to a unit vector `v`. Differentiability yields `Dg_i(0)v>=0` for every selected index. Positive span makes this impossible. Hence zero is isolated for those inequalities, and also for the bodies to which they belong. QED.

### The missing general step

Isolation can be higher-order: `y-x^2>=0` and `-y-x^2>=0` isolate `(0,0)`, but their linearizations allow the entire x-axis. This is an abstract constraint-space warning, not an asserted realization by disjoint bodies. Moreover, facet contacts can impose a disjunction instead of a conjunction. Neither control of these cases nor a uniform replacement theorem is supplied here.

## References

1. Xavier Goaoc, “Helly numbers and geometric permutations,” in *Discrete Geometry*, Oberwolfach Report 44/2008, pp. 2541-2543. Workshop 2008; report publication 2009. https://doi.org/10.4171/owr/2008/44
2. Otfried Cheong, Xavier Goaoc, Andreas Holmsen and Sylvain Petitjean, “Helly-Type Theorems for Line Transversals to Disjoint Unit Balls,” *Discrete & Computational Geometry* 39 (2008), 194-212. Inspected January 2006 preprint, section 6: https://www.ens-lyon.fr/LIP/Arenaire/SYMB/teams/vegas/vegas2.pdf ; later preprint https://arxiv.org/abs/cs/0702039
3. Boris Aronov, Otfried Cheong, Xavier Goaoc and Günter Rote, “Lines Pinning Lines,” *Discrete & Computational Geometry* 45 (2011), 230-260. https://arxiv.org/abs/1002.3294 ; https://doi.org/10.1007/s00454-010-9288-6

Searches on 2026-10-06 did not find a published resolution of the unrestricted disjoint-body question. This is a limited literature-search result, not proof that no resolution exists. Historical open labels are not substituted for current proof. The lower bound above is proved directly, independently of those labels.
