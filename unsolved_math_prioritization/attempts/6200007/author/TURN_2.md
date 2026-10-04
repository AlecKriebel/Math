# Attempt 2: construct an invariant annular geometry

## Annulus convention

An annulus is an ordered pair A=(A-,A+) of disjoint closed subsets of Z, with
nonempty complement of their union. Write K<A when K is contained in int(A-),
and A<K when K is contained in int(A+). Our nesting convention is

A<B iff int(A+) union int(B-) = Z.

It implies A- subset int(B-) and B+ subset int(A+). This is the consistent
convention explicitly used by Sun, Definition 6.1, and Azemar, Section 2.3.2.
For a symmetric annulus system A define (K|L) as the supremum of lengths of
strictly nested chains K<A_1<...<A_n<L. Intersecting K and L give value zero.
For finite sets braces are omitted.

## Credited sufficient criterion

Suppose Z is a perfect metrizable compactum and A is G-invariant and symmetric.
Consider the following conditions:

1. (A1) (a,b|c,d) is finite whenever a!=b and c!=d.
2. (A2) A single k bounds the smaller of (a,b|c,d) and (a,c|b,d), for every
   quadruple of distinct points and every relabeling.
3. (A3) (a,b|p)=infinity for every three distinct points a,b,p.

These are precisely a sufficient route to the requested realization. This is
a consequence of Bowditch's established construction, not a new solution:
Proposition 6.5 and Lemma 6.6 of [B98] give a compatible hyperbolic path
crossratio; Proposition 4.7 identifies the boundary of the resulting triple
quasimetric with Z. The triple quasimetric is

rho(x,y) = max (x_i,x_j | y_k,y_l),

over distinct indices within each triple. G-invariance of the annulus system
makes rho invariant. The natural boundary identification is equivariant.
The following explicit last step, also in Sun Proposition 6.6, turns it into
an isometric action.

## Lemma 2.1: equivariant graph realization with bounds

Let rho be an r-quasimetric, so its triangle inequality has additive error r.
Suppose any x,y can be joined by a finite sequence x=x_0,...,x_n=y satisfying
|rho(x_i,x_j)-|i-j||<=s for all i,j. Make a graph on these points by joining
distinct vertices when rho<=s+1, with every edge of length 1. For its vertex
metric d_Gamma,

rho(x,y)/(s+1+r) <= d_Gamma(x,y) <= rho(x,y)+s.

Indeed the displayed sequence provides a path of length at most n<=rho+s.
A graph path of m edges has rho(x,y)<=m(s+1)+(m-1)r<=m(s+1+r), proving the
other bound. Coincident successive points can simply be omitted in the first
argument. The graph is connected; its geometric realization is geodesic, and
vertices form a 1/2-net. Every rho-preserving permutation acts by isometries
on the graph, extending affinely on edges. Thus the inclusion is an equivariant
quasi-isometry. Hyperbolicity and the boundary homeomorphism follow from the
standard quasi-isometry invariance for hyperbolic path quasimetrics, as in
[B98, Section 3] and [S19, Proposition 6.6].

Combining this lemma with the credited crossratio theorem gives the requested
uniform quasi-action with constants (1,0): it is an actual isometric action.
The hard part is finding A satisfying all three conditions.

## Where the unconditional extension fails

For convergence actions a symmetric annulus system with finitely many G-orbits
satisfies (A1) and (A2), by [B98, Lemmas 7.2-7.4 and Proposition 7.5]. This
produces a hyperbolic action even without uniform convergence. It does not
produce (A3). In Bowditch's proof, triple cocompactness is used in Lemma 7.6
to obtain annuli separating an arbitrary closed K from a point p outside K.
Iterating that separation yields (A3). Omitting this use of cocompactness would
omit the boundary-realization step.

The finite-family obstruction proved in Attempt 4 shows why adding a few more
annulus orbits cannot repair this in the presence of the exhibited cusp.

## Literature scope

[B98] answers the extra triple-cocompact case. Sun's general existence of a
non-elementary hyperbolic action is a theorem about the group, not an
identification of its prescribed boundary. Azemar's Proposition 3.15 gives
a boundary homeomorphism only over a specified subset M_infinity; Proposition
3.21 gives full stationary measure to that subset. Equality up to a null set
does not imply equality as compact G-spaces. We do not make that inference.

Checkpoint: approximately 10% toward the universal target. The conditional
route is complete, with named literature dependencies; its input (A3) has not
been obtained from the general hypotheses.
