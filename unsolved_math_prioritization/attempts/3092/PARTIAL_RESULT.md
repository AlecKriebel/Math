# Additive-coloring barriers for the associahedron

**ID 3092 / OPG-59984. Status:** original conjecture unresolved, 2/5 substantive approaches. Independent review pending. The results below concern a restricted coloring scheme, not arbitrary colorings.

## Exact problem and known bounds

Let A_n be the graph of triangulations of a fixed convex n-gon, with adjacency given by one diagonal flip. Its vertices are triangulations, not the polygon's vertices or its diagonals. The [Open Problem Garden conjecture](https://www.openproblemgarden.org/op/chromatic_number_of_associahedron) asks whether chi(A_n) is unbounded as n tends to infinity.

[Fabila-Monroy et al.](https://dmtcs.episciences.org/460), Theorem 4.1, gave a ceil(n/2)-coloring by summing fixed edge weights. [Addario-Berry, Reed, Scott and Wood](https://arxiv.org/abs/1811.08972) later proved an O(log n) upper bound. [Cioaba and Gupta](https://arxiv.org/abs/2210.08516) discuss the known lower bound four and the limitation of the elementary Hoffman spectral approach. None of these results proves unboundedness. We do not claim new unrestricted upper or lower bounds, or independently re-prove those papers' main theorems.

## 1. Exact characterization of fixed additive colorings

Let G be an abelian group, finite or infinite. Assign a fixed weight w(d) in G to every internal diagonal d, and color a triangulation T by

    c(T)=sum_(d in T) w(d).                                  (1)

Boundary-edge weights, if included, add the same constant to every color and are irrelevant. No additional nonlinear recoloring is included in this definition.

**Proposition.** Formula (1) is proper if and only if crossing internal diagonals always have distinct weights.

For necessity, let a<b<c<d be the cyclically ordered endpoints of crossing diagonals ac and bd. Insert the four sides of this quadrilateral where they are internal diagonals, and triangulate all complementary polygonal regions. Adding ac or bd produces two triangulations differing by exactly that flip. Their color difference is w(bd)-w(ac), so it must be nonzero.

For sufficiency, the two exchanged diagonals in every flip cross. All unchanged summands cancel in the group, so distinct weights imply distinct colors.

Thus fixed additive colorings correspond to proper weight assignments on the crossing graph of the polygon's diagonals. This crossing graph is a different graph from A_n.

## 2. Sharp finite-group order requirement

For n>=4, every proper coloring of the form (1) with finite G satisfies

    |G| >= ceil(n/2).                                        (2)

Indeed each equal-weight class is a noncrossing set of diagonals, containing at most n-3 diagonals. There are n(n-3)/2 internal diagonals, so at least ceil(n/2) distinct weights are required. This counts weights and bounds the size of G; it does not automatically count the distinct sums realized by triangulations.

The bound on group order is sharp. Label polygon vertices 0,...,n-1 and put m=ceil(n/2). Define

    w(ij)=floor(((i+j) mod n)/2) in Z/m.                      (3)

To verify crossing diagonals ac and bd have different weights, take 0<=a<b<c<d<n. Their integer endpoint sums differ by

    delta=(b-a)+(d-c),       2<=delta<=n-2.

Therefore their residues modulo n are neither equal nor adjacent on the cyclic residue set. Each fiber of r->floor(r/2) consists of two consecutive residues, or the final singleton when n is odd. So the weights differ, and Proposition 1 applies. This is another explicit realization of the already known ceil(n/2) additive upper-bound method, not an improvement on the logarithmic bound.

## 3. A lower bound on the number of actually used additive colors

Let C={c(T):T is a triangulation}, let k=|C|, and allow G to be arbitrary. The image is finite because A_n is finite. Set m=floor(n/2). For n>=4, every proper additive coloring satisfies

    m <= k(k-1)+1.                                          (4)

In particular no fixed number of realized colors can work within this additive scheme, even if the ambient abelian group is allowed to grow with n.

Proof: choose m pairwise crossing diagonals d_i=(i,i+m), for i=0,...,m-1. When n is odd the unused final vertex has no effect. Their weights are distinct by Proposition 1. Fix d_0. For every i, the flip construction in Proposition 1 realizes w(d_i)-w(d_0) as a difference of two colors in C (with i=0 giving zero). These m differences are distinct, so

    m <= |C-C| <= k(k-1)+1.

The last inequality counts zero and the at most k(k-1) ordered differences of unequal colors. It remains valid with torsion or coincidences in G. This proves (4), or equivalently k>=(1+sqrt(4m-3))/2 with integer rounding upwards.

The crossing clique is used only in the diagonal crossing graph. It is not a clique in the associahedron. This distinction prevents a false lower bound for arbitrary colorings of A_n.

## 4. Scope of the obstruction and remaining gap

The linear group-order lower bound and square-root used-color lower bound apply only when all triangulation colors are a fixed sum of diagonal weights. They say nothing about general colorings, nonlinear functions of several statistics, or schemes where the contribution of a diagonal depends on the rest of the triangulation. In particular they do not conflict with the known logarithmic general coloring: that coloring need not have form (1).

No reduction from arbitrary colorings to (1) is proved or assumed. Such a reduction with unchanged color count would itself carry the central difficulty and would conflict with the known bounds for large n. The original unboundedness conjecture remains unresolved. Finite computations below are checks on the formulas and flip construction, never evidence promoted to an all-n chromatic theorem. No novelty claim is made for these elementary restricted observations.

## Verification

`verify.py` enumerates convex-polygon triangulations through n=10, checks Catalan counts and all graph edges, and verifies that (3) colors every flip properly. It also checks crossing-diagonal weights through n=30 and constructs the pairwise-crossing families used in (4). The written proofs establish all-n statements. The checker does not compute exact chromatic numbers or certify the original conjecture.

Work used the inherited native runtime without a model or reasoning-setting change; its exact model identifier was not exposed to this worker. No human peer review is claimed. Primary PDFs are kept outside the publication package.
