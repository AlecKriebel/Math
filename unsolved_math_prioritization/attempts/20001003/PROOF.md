# Proof of determinant-bounded undirected Laplacian recognition

AI-assisted, unrefereed research. Acceptance means an internal AI mathematical audit; it is not human peer review, journal acceptance, or formal proof-assistant certification. This is a complete authored proof/audit edition, not a computational reproduction package.

## Disposition and scope

Accept the determinant-bounded recognition theorem, the complete rank-two arithmetic criterion, all 15 displayed small-index witness/obstruction rows, the smallest-index obstruction in rank two, and the same-Smith counterexample. The proofs supply exact recognition for each specified input lattice.

No efficient algorithm, broader structural classification, novelty, priority, current worldwide openness, or unqualified resolution of the original qualitative workshop question is established. The workshop question does not specify an algorithmic success criterion. Index-four minimality is asserted in rank two only.

Problem 20001003 / AIM-COMBINATORICS-0128: recognizing undirected reduced Laplacian lattices.

## Exact target and transpose convention

Let n >= 1, let M be a nonsingular n by n integer matrix, and fix the embedded row lattice Lambda = {zM : z in Z^n}, a subgroup of the specified coordinate copy of Z^n. Put D = |det M| = [Z^n : Lambda]. Vertices are labeled 1,...,n,s, with s the sink. An undirected edge's nonnegative integer weight is its parallel-edge multiplicity. All coordinates, labels, and the chosen sink position remain fixed.

We ask whether Lambda is exactly the integral row span of a reduced Laplacian of a connected undirected integer-weighted multigraph on those n+1 vertices. This is equivalent to asking for U in GL_n(Z) such that UM is that reduced Laplacian. Left multiplication changes only the choice of lattice basis. An arbitrary right multiplication would change the ambient embedding and is not permitted. Equality of quotient groups or Smith factors is insufficient.

The Perkinson–Perlman–Wilmes primer uses column images. For the present input, the corresponding column lattice is im_Z(M^T) = {v^T : v in Lambda}. A basis change M -> UM becomes M^T -> M^T U^T. An undirected target L satisfies L^T = L. Consequently, im_Z(L) = im_Z(M^T) is exactly equivalent to row_Z(L) = row_Z(M). It is not legitimate to replace im_Z(M^T) by im_Z(M) for an arbitrary nonsymmetric M.

A sink here is distinguished, not an absolute sink of an asymmetric digraph. Connectivity in the undirected support ensures access to it. The full Laplacian is singular and is not the n by n matrix being recognized.

## General recognition theorem

For each i < j <= n choose w_ij in Z_{≥0}, and for each i choose w_is in Z_{≥0}. Define

L_ij = -w_ij for i != j,

L_ii = w_is + sum_{j != i} w_ij.

Writing e_i for the fixed standard coordinate vectors, this is

L = sum_i w_is e_i e_i^T + sum_{i<j} w_ij (e_i-e_j)(e_i-e_j)^T.

The following conditions are equivalent.

1. Lambda is realized by a connected undirected integer-weighted multigraph on the specified vertices with the specified sink.
2. There are weights in {0,...,D} for every nonsink pair and sink pair, such that each row of L lies in Lambda and det L = D.
3. There is an integral symmetric L whose off-diagonal entries are nonpositive, whose row sums are nonnegative, whose row lattice equals Lambda, and whose determinant is positive.

Every loopless realization satisfies |L_ij| <= D for i != j, 0 <= (L1)_i <= D, and 0 < L_ii <= nD. Thus at most (D+1)^{n(n+1)/2} weight assignments must be tested. The bound does not apply to diagonal entries as D; the correct stated diagonal bound is nD.

### Graphs, loops, and the matrix cone

The weights yield an undirected multigraph by putting w copies on each indicated pair. Conversely, for a symmetric integral matrix with the stated signs and row sums, the assignments w_ij = -L_ij and w_is = (L1)_i recover precisely that matrix. In particular, this is an exact integral cone description, not a claim about arbitrary positive-definite matrices.

The quadratic identity

x^T L x = sum_i w_is x_i^2 + sum_{i<j} w_ij (x_i-x_j)^2

shows positive semidefiniteness. Its kernel consists of vectors constant on each nonsink support component and zero on every component attached to the sink. Therefore L is nonsingular if and only if the whole graph is connected to s. In that case L is positive definite and det L > 0. This proves the connectivity equivalence directly, with zero weights interpreted as absent edges.

Loops cancel in the primer's definition: their contribution to outdegree times the vertex is exactly subtracted by their adjacency contribution at that same vertex. They also occur in no spanning tree. Removing all loops preserves L, Lambda, and connectivity. Therefore a loopless representative may always be sought, even though the primer permits loops. Raw loop multiplicities can be arbitrarily large; no bound on them is claimed.

### Tree determinant identity and the edge bound

Here is a proof of the determinant identity sufficient for this audit. Expand the integer weights into individually distinguishable parallel edges. Orient every edge arbitrarily, form its incidence vector, and delete the sink coordinate. Place these vectors in the columns of an n by N matrix B. Reversing an orientation only negates one column, and L = BB^T.

By Cauchy–Binet, det L is the sum of det(B_T)^2 over n-element edge-copy subsets T. A cycle makes the relevant incidence columns dependent. A disconnected selection has a nonzero component-indicator in its reduced left kernel for a component not containing the sink. A connected acyclic selection is a tree; its reduced incidence determinant is +/-1 by repeatedly expanding at a nonsink leaf. Such a leaf exists until the one-vertex terminal case. Thus det L counts the spanning trees, with different parallel copies distinguished.

Suppose the graph is connected and has a parallel class of multiplicity m > 0 between distinct vertices. A chosen edge copy can be extended to a spanning tree: begin with that edge and iteratively add an edge joining different current components, possible by connectivity. A tree contains no second edge from its parallel class. Replacing its chosen copy by each of the m copies yields m different spanning trees. Hence m <= det L. This applies equally when one endpoint is the sink. If the row lattice is Lambda, positive definiteness and the index formula give det L = D. Consequently every non-loop multiplicity is at most D.

Each nonsink vertex has n possible distinct neighbors, including s. Its diagonal entry is the sum of those multiplicities, is positive by connectivity, and is at most nD. The bounds are valid without pretending that every edge belongs to every tree. For n=1 the single edge class can have multiplicity exactly D, so the uniform bound cannot be lowered in general.

### Inclusion plus index gives equality

If every row of L belongs to Lambda, then Lambda' = row_Z(L) is a sublattice of Lambda. When det L = D,

[Z^n : Lambda'] = D = [Z^n : Lambda].

Index multiplication gives [Lambda : Lambda'] = 1, so Lambda' = Lambda. Positivity of the determinant and the preceding kernel calculation enforce connectivity. This proves condition 2 implies condition 1. The edge-bound proof gives condition 1 implies condition 2. The matrix-cone equivalence proves equivalence with condition 3.

All tests are exact. Specifically v belongs to row_Z(M) if and only if every coordinate of v adj(M) is divisible by D; this is just integrality of vM^{-1}. If a candidate is accepted, the explicit multiplier U = L adj(M)/(det M) is integral and has determinant det L/det M = +/-1. This also verifies integral row equivalence, even when det M is negative. Searching the finite weight box terminates and either supplies this certificate or exhausts every possible loopless realization.

The formula is an exact decision procedure. A brute-force procedure with this search bound is not claimed to be polynomial-time, and the audit does not attempt a computational complexity classification. An unspecified demand for a conceptual classification requires separate interpretation.

## Complete rank-two arithmetic criterion

For n=2 put a=w_1s, b=w_2s, and c=w_12. Then

L(a,b,c) = ((a+c,-c),(-c,b+c)),

det L(a,b,c) = ab+ac+bc.

Thus Lambda is graphical if and only if a,b,c are integers between 0 and D such that ab+ac+bc=D and both displayed rows belong to Lambda. Necessity and sufficiency follow from the general theorem; a positive value of ab+ac+bc also directly forces the three-vertex support to be connected.

For clarity, the complete lower-triangular row normal forms are H(h,r,k)=((h,0),(r,k)), with h,k positive, hk=D, and 0<=r<h. This convention is derived as follows. The y-coordinate projection of Lambda is kZ; its intersection with the x-axis is hZ. Choose a vector with y-coordinate k and reduce its x-coordinate modulo h to r. Subtracting multiples of (r,k) and then (h,0) expresses every lattice vector, and the residues x mod h and y mod k show index hk. These data are unique. Hence the list over divisors h of D and r=0,...,h-1 exhausts the embedded lattices, without ambient coordinate changes.

Membership is exactly k|y and h|(x-(y/k)r). For a candidate triple this can equivalently be written

k|c, k|b,

h|(a+c+(c/k)r),

h|(c+((b+c)/k)r).

No rational division is tested until k divides its numerator.

## Small indices and the obstruction

The following are all eight normal forms with D<=3. Every listed triple was checked independently against the determinant and membership conditions.

| D | (h,r,k) | (a,b,c) |
|---|---|---|
| 1 | (1,0,1) | (0,1,1) |
| 2 | (1,0,2) | (1,0,2) |
| 2 | (2,0,1) | (0,1,2) |
| 2 | (2,1,1) | (0,2,1) |
| 3 | (1,0,3) | (1,0,3) |
| 3 | (3,0,1) | (0,1,3) |
| 3 | (3,1,1) | (1,1,1) |
| 3 | (3,2,1) | (0,3,1) |

Let Lambda_bad = row_Z((2,0),(1,2)). A vector (x,y) belongs to it precisely when y is even and 2x-y is divisible by 4. Membership of both L rows forces

c even, 2a+3c = 0 mod 4, b+3c = 0 mod 4.

If c=0 mod 4, then a is even and b=0 mod 4. For c=0 every positive ab is at least 8. For c>=4, either a=b=0 and the determinant vanishes, or ac or bc is at least 8. If c=2 mod 4, then a is odd, b=2 mod 4, and a>=1,b>=2,c>=2; hence ab+ac+bc>=8. The determinant can never be 4. This proves nongraphicality independently of any enumerator or finite cap.

The seven index-four normal forms are:

| (h,r,k) | Witness (a,b,c) or impossibility |
|---|---|
| (1,0,4) | (1,0,4) |
| (2,0,2) | (0,2,2) |
| (2,1,2) | none |
| (4,0,1) | (0,1,4) |
| (4,1,1) | none |
| (4,2,1) | none |
| (4,3,1) | (0,4,1) |

To make the negative entries fully transparent, positive a,b,c give value 3 at (1,1,1) and at least 5 if any entry increases; they never give 4. With a zero entry, the other two have product 4. Thus exactly nine ordered triples are possible: the six permutations of (0,1,4) and the three distinct permutations of (0,2,2). Substitution into the membership test yields exactly the four positive rows above.

There are also direct checks of the additional negative rows. For H(4,1,1), membership forces a=b=-2c mod 4. Odd c gives a,b>=2 and determinant>=8; even c gives a,b multiples of 4, and a positive determinant is at least 8 (at least 16 when c=0). For H(4,2,1), membership forces a=c mod 4 and 2b+3c=0 mod 4, so c is even. If c=0 mod 4, a is a multiple of 4 and b is even, making any positive determinant at least 8. If c=2 mod 4, then a>=2,b>=1,c>=2 and again the determinant is at least 8. No weight cap is needed for either argument.

Since all eight forms below index four are realized, Lambda_bad is a smallest-index **rank-two** obstruction. No minimality statement across every dimension is made.

## Smith data and the fixed embedding

Lambda_good = row_Z((1,0),(0,4)) is realized by L=((5,-4),(-4,4)), from (a,b,c)=(1,0,4). Its rows have second coordinates divisible by 4 and determinant 4, so they span Lambda_good.

Both input bases for Lambda_bad and Lambda_good have absolute determinant 4 and greatest common divisor of entries 1. Their Smith invariant factors are therefore (1,4), so their quotient groups are both Z/4Z. Only Lambda_good is graphical. This refutes recognition from the abstract quotient group alone. It does not refute any criterion retaining the embedded quotient map or additional data.

The distinction is substantive even at the matrix-convention level: (1,2) belongs to row_Z(((2,0),(1,2))) but does not belong to row_Z(((2,1),(0,2))). Transposing the input without also switching rows to columns changes the problem.

## Primary sources and exact reading scope

The recorder-hosted *Problems from the AIM Chip-Firing Workshop*, problem 38 on PDF pages 8–9, contains the final question “When does a undirected graph suffice?” This is the undirected question addressed by the scoped recognition results here. The recorder version cites Wilmes as [30].

The live AIM URL returned HTTP 403 during the source-qualification work. Its current edition was not inspected; no successful current AIM retrieval is claimed. The recorder PDF is the 234,256-byte copy from https://www.samuelfhopkins.com/docs/aim_chip-firing_problems.pdf, retrieved on 2026-10-10. Its SHA-256 is d50a703dcc3e77f7f2d34d80fb5fe5cbcf3581e819982231ea4ed45f3359d7bd. PDF pages 8–9 were read and page 8 was visually inspected during the mathematical audit.

The inspected *Primer for the algebraic geometry of sandpiles*, by David Perkinson, Jacob Perlman and John Wilmes, is the 685,899-byte copy retrieved from https://arxiv.org/pdf/1112.6163 with SHA-256 9e77eef5ba13d557fd322b7a6db529fd9c5972a4fca76785715d4191ac55fd5b. PDF pages 1,3–5,15–18 were read and page 17 was visually inspected. Its margin says arXiv:1112.6163v2, 31 Dec 2011, while its body date on page 1 is November 27, 2024. These markings are recorded without resolving their relationship or asserting identity with the 2013 publication. Pages 3–5 establish integer-weighted multigraphs, permitted loops, connected undirected graphs, and the transpose convention. Page 17 poses Question 4.15. Pages 15–17 describe a directed realization algorithm; it was read for context, not executed or independently audited. The Gorenstein example and its supporting theorem are attributed source claims, not additional results accepted here.

The inspected *The Laplacian lattice of a graph under a simplicial distance function*, by Madhusudan Manjunath, is the 488,694-byte copy from https://arxiv.org/pdf/1111.7246, SHA-256 d31df2a251ab4cdd7740e24735723ab0ddb602a78e9ddfbde8ebec1901384d53. Only PDF pages 1–3 were read. Its margin says v1, 30 Nov 2011, and its body date is October 25, 2021. No identity with its cited 2013 journal version is assumed. The introduction's reconstruction/finiteness claims concern full Laplacian lattices in the sum-zero space; their proofs were not inspected or used.

For perspective, the correct translation of an undirected reduced row lattice into that full setting is the fixed embedding iota(x)=(x,-sum_i x_i). The first n full Laplacian rows are the images under iota of the reduced rows; the sink row is their negative sum. Thus the full row lattice is exactly iota(Lambda). This observation does not import any uninspected geometric classification or change the permitted coordinates.

No PDF was inspected in full. PDF hashes authenticate bytes, not edition equivalence or source theorem correctness. No new source retrieval or inspection was performed in preparing this edition. No novelty or current worldwide-open claim follows from the bounded source reading.
