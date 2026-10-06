# Strong Heegaard diagrams and the alternating cover question

## Result and scope

Kirby Problem 3.53, catalog ID 2851, is not solved here. The outcome is a stalled partial investigation with an exact diagnostic: a concrete positive 7 by 7 Pólya matrix has nonplanar support, but it cannot be realized by coherent attaching curves on a genus-seven surface. The first fact blocks a purely algebraic planarity shortcut; the second prevents promoting this particular matrix to a counterexample. Neither fact classifies strong L-spaces. No novelty is claimed for the graph example or the restricted diagnostic.

The [K3 author version](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed page 169, asks whether every strong L-space is an alternating-link double branched cover of the three-sphere. Its definition requires a rational homology sphere and a diagram whose chain-group rank equals the order of first homology. It still records the question as open and distinguishes this condition from merely having a zero differential. The problem page could not be retrieved successfully on 6 October 2026; the exact local statement agrees with this primary problem source.

We work with closed, connected, oriented rational homology three-spheres. There is no genus bound. The conclusion is the existence of a link and a branched covering description of the manifold, not a prescribed presentation of every strong diagram. Allowing mirrors removes any ambiguity from reversing the orientation of the covering manifold: mirroring an alternating link preserves alternation. A genus bound below always refers to the strong diagram, not merely to the manifold's Heegaard genus.

[Greene and Levine](https://msp.org/agt/2016/16-6/agt-v16-n6-p03-p.pdf) prove the desired conclusion for genus-two strong diagrams and for homology order at most eight (Theorems 1.6 and 1.5). Their Proposition 3.1 permits a strong diagram to be made 1-extendible without changing its generator count. Propositions 7.7 and 7.8 give weak reducibility and sparse intersection constraints, not an all-genus classification. [Usui's 2012 preprint](https://arxiv.org/abs/1202.3333) states a genus-at-most-three result; K3 describes this as an announced result under mild hypotheses. We do not strengthen that assessment or independently certify the preprint's full proof.

## The algebraic reduction and its limit

Let H have g alpha curves and g beta curves. Write N_ij for the number of their geometric intersections and M_ij for their signed intersection number. A generator chooses one intersection on each curve of both families, hence the generator count is per(N). The signed count is det(M). Since M presents first homology, the strong condition is

    per(N) = |det(M)| > 0.

In the signed sum, every generator contributes either +1 or -1. Equality in the triangle inequality therefore says exactly that every generator has the same sign. If an intersection lies in a generator, replacing it by another intersection of the same pair shows that the two local signs coincide. Consequently a strong 1-extendible diagram is coherent, N = |M|, and M is a Pólya matrix. Intersections unused by all generators need not be coherent before this reduction.

None of this supplies cyclic orders of intersections on the curves, a surface embedding, a compatible covering involution, or an alternating branch diagram. Those are geometric data missing from the matrix alone.

## A precise nonplanar matrix diagnostic

Index rows and columns by residues modulo seven and put

    A_ij = 1 if j - i belongs to {0, 1, 3}, and A_ij = 0 otherwise.

Every row and column has three ones. Two different rows have exactly one common one, so A A^T = 2I + J. Thus |det(A)| = 24. The verifier examines all 7! permutations: precisely 24 contribute to the permanent, every one has positive sign, and det(A) = per(A) = 24. An independent rational Gaussian elimination also returns 24. Each of the 21 nonzero positions lies in eight perfect matchings.

The support graph has 14 vertices and 21 edges, is bipartite and connected, and has no bridges or four-cycles. In a planar embedding its face boundary lengths would therefore be at least six. Euler's formula would imply 21 <= 3(14 - 2)/2 = 18, a contradiction. The support is the familiar Heawood graph, which appears explicitly in the [McCuaig–Robertson–Seymour–Thomas extended abstract](https://thomas.math.gatech.edu/PAP/permstoc.pdf). A Pólya matrix need not have planar support. This does not say that intersection-graph planarity is necessary for an alternating branched cover.

## Why this matrix does not give a counterexample

Here is the exact restricted claim checked by the attached program:

There are no two families of seven oriented simple closed curves on an oriented surface of genus seven, disjoint within each family, with geometric intersection matrix A and positive sign at every intersection.

This is a statement about the positive, unweighted matrix A, not about all weighted Heawood patterns, all signings, stabilizations, or all strong diagrams.

To prove it, suppose such families existed and take a small regular neighborhood R of their union. The union is connected. It is a four-valent graph with 21 vertices and 42 edges, so

    chi(R) = 21 - 42 = -21,
    2 genus(R) + boundary_components(R) = 23.

Every curve contains exactly three distinct labeled intersections. Up to choice of starting point it has precisely two oriented cyclic orders. Fourteen curves therefore give exactly 2^14 = 16,384 possibilities. This exhausts all possibilities, without an assumption that the complement of the curves consists of disks.

At each crossing use the four outgoing halfedges in cyclic order

    alpha+, beta+, alpha-, beta-.

This rotation is forced by the positive intersection sign and the orientation of the surface. A chosen cyclic order along each curve pairs its outgoing halfedge at one crossing with its incoming halfedge at the next. Let tau be that edge-reversing involution, and let rho be the local four-cycle above. Boundary components of R are the cycles of rho tau. Reversing the global convention gives the same set of enumerated cases.

Exhaustive evaluation gives:

- 2,688 choices with 1 boundary component and neighborhood genus 11
- 11,680 choices with 3 boundary components and neighborhood genus 10
- 2,016 choices with 5 boundary components and neighborhood genus 9

The totals sum to 16,384. For every case a second tracer agrees: if a and b are the permutations sending an intersection to its successor on its alpha and beta curve, the boundary count is the number of cycles of b a^(-1) b^(-1) a on the 21 intersections. This follows by following four successive halfedges of rho tau, starting with an alpha-outgoing halfedge. Every boundary cycle meets that set of halfedges.

It follows that genus(R) >= 9. An orientable subsurface of a genus-seven surface cannot have genus nine: a symplectic family of 2 genus(R) homology curves in R retains its nondegenerate intersection pairing in the ambient surface, whose first homology has dimension fourteen. This is a contradiction.

The proof is computer-assisted only in the finite cyclic-order count. Its complete reduction and executable enumeration are included. The program uses exact integers, permutations, and rational arithmetic, with no third-party dependencies. It does not recognize arbitrary Heegaard diagrams and does not decide the original question.

## Remaining gap and stopping point

A valid affirmative argument must pass from an arbitrary geometric strong diagram to an alternating branched-cover description. Matrix sign coherence alone does not do this. The Fano test excludes one attempted candidate; it does not exclude a nonplanar component from every geometric strong diagram.

A second possible route is to use weak reduction and induct on diagram complexity. Weak reducibility is not a genus-reducing strong-diagram move. Cutting can produce positive-genus boundary pieces, and no argument here reconstructs compatible branched coverings or preserves the required generator equality through the decomposition and gluing. The necessary geometric induction step is missing.

A source check on [Agol's chainmail manuscript](https://arxiv.org/abs/2306.10918) also prevents conflating L-spaces with strong L-spaces. The inspected arXiv v1, section 8, asks whether any of its new examples are strong. The abstract record gives the 2026 journal publication; only the identified arXiv version was inspected in full. These examples are not established counterexamples to the present question.

Three approaches were used: algebraic planarity, explicit Fano realization, and weak-reduction induction. Stop at 3/5 with the full problem unresolved. The bounded literature and repository checks found no verified full solution or prior exact-ID proof, but negative search results are not evidence of novelty or a universal absence of prior work.
