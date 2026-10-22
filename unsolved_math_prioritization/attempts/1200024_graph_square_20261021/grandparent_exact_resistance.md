# Exact free spanning-forest degree of the binary grandparent graph

This is an authored calculation, not a claim about a source theorem. All conductances are one.

## Graph and result

Let T be the 3-regular tree with a distinguished end. Write p(v) for the neighbor of v toward that end; each vertex has two children. Let G have vertex set V(T), with edges {v,p(v)} and {v,p²(v)}. The end stabilizer acts transitively, so G is a connected infinite simple vertex-transitive graph of degree 8. At a vertex there are three parent-type incident edges and five grandparent-type incident edges. There are no other types.

The free effective resistances of these two types are

R_parent = (3√2 − 2)/7,
R_grandparent = (6 − 2√2)/7.

Consequently

E[deg_FUSF(o)] = 3 R_parent + 5 R_grandparent = (24 − √2)/7,
b_F(G) = (10 − √2)/14.

The expectation is approximately 3.22654091966. Only the expectation formula uses the spanning-tree transfer-current fact; the resistance calculation below is an explicit series-parallel exhaustion.

## Exhaustion and elimination

Fix o, and set v_j=p^j(o). For n≥2, let S_n consist of all descendants of v_n whose tree distance below v_n is at most 2n. Let G_n be the induced subgraph G[S_n]. These sets are finite, nested, and exhaust V(T). Indeed, going from v_n to v_(n+1) increases all old descendant depths by one, while the allowed depth increases by two. Every fixed tree vertex eventually lies in S_n because its ray to the distinguished end eventually merges with the ray from o.

Define

c_0=1,
c_m = 1 + 2 c_(m−1)/(1+c_(m−1)),   m≥1,
a_m = 1 + c_(m−1)/(1+c_(m−1)),      m≥1.

Consider a vertex x whose descendants down to depth m are present, together with its parent y. Eliminate all strict descendants of x, retaining x and y and the direct parent edge xy, but not the grandparent edge from x. The resulting conductance between x and y is c_m. For m=0 it is 1. For m≥1, each child z of x, together with its descendants, reduces to a conductance c_(m−1) between z and x and a unit edge between z and y. Their series combination contributes c_(m−1)/(1+c_(m−1)); the two children yield the recurrence.

Now eliminate from G_n every vertex off the ancestor spine v_0,...,v_n, apart from terminal branches that attach only at v_n and therefore have no effect on these terminal resistances. The remaining network has:

- conductance c_n on v_0 v_1;
- conductance a_(n+j) on v_j v_(j+1), for 1≤j≤n−1;
- conductance 1 on v_j v_(j+2), for 0≤j≤n−2.

For j≥1 there is only one off-spine child of v_j, explaining a rather than c. Its descendant depth is n+j−1. The two children of v_0 are both off-spine, explaining c_n.

Let u_(j,n) be the effective conductance between v_j and v_(j+1) in the remaining suffix v_j,...,v_n. Eliminating this triangular chain from its upper end gives

u_(n−1,n) = a_(2n−1),
u_(j,n) = a_(n+j) + u_(j+1,n)/(1+u_(j+1,n)),  1≤j≤n−2.

Therefore the network on the three terminals v_0,v_1,v_2 reduces to a triangle with conductances c_n, u_(1,n), 1. It follows that

R_parent(G_n) = 1/[c_n + u_(1,n)/(1+u_(1,n))],
R_grandparent(G_n) = 1/[1 + c_n u_(1,n)/(c_n+u_(1,n))].

These are exact finite-network identities, obtained solely by series and parallel reductions.

## Limits

The sequence c_m increases to the positive solution c of c=1+2c/(1+c), namely c=1+√2. This also follows from contraction on [1,∞), since the recurrence map has derivative 2/(1+x)²≤1/2 there. Hence a_m→a=1+c/(1+c). Notice c=a+c/(1+c).

The maps x↦a_m+x/(1+x) have derivative at most 1/4 for x≥1. All u_(j,n) lie in a fixed bounded interval and all coefficient indices n+j are at least n+1. If ε_n=sup_(m≥n+1)|a_m−a|, iteration gives

|u_(1,n)−c| ≤ ε_n/(1−1/4) + (1/4)^(n−2) C

for an absolute finite C. Thus u_(1,n)→c. Taking limits in the finite formulas yields

R_parent = (c+1)/[c(c+2)] = (3√2−2)/7,
R_grandparent = 2/(c+2) = (6−2√2)/7.

Since G_n is an induced connected exhaustion with no boundary wiring, these are precisely the free effective resistances. The FUSF edge-inclusion probabilities equal these resistances because conductances are one. The degree count gives the claimed exact result.

## Source dependencies actually inspected

Benjamini, Lyons, Peres, Schramm, *Uniform Spanning Forests*, author-hosted corrected version of 27 January 2009: https://rdlyons.pages.iu.edu/pdf/usf.pdf . Proposition 7.1 identifies the free current with the cycle-orthogonal projection, and Theorem 7.8 gives the infinite-graph transfer-current formula. Theorem 6.4 states WSF expected degree 2 for every transitive network, without a unimodularity assumption. The present exact grandparent calculation is independent of any unverified numerical approximation.
