# Independent mathematical audit: homology-sphere covers

## Verdict and exact scope

The reviewed construction is accepted as a counterexample to the unqualified homology-sphere-cover assertion in Nevo's Problem 8 / Problem 3.7. It produces a finite two-dimensional simplicial complex that is doubly Cohen–Macaulay over the fixed field Q and has no two-dimensional homology-sphere subcomplex over any field, where homology sphere includes all face-link conditions.

There is consequently no cover even before imposing overlap or ordering conditions. This does not assert a counterexample over each individually prescribed positive characteristic. It also does not claim novelty or priority. The finite field used in the building is F_11; it is distinct from the homology coefficient field Q.

The review checked the entire authored proof, its scope and source audit, and the construction's load-bearing source passages. No blocking mathematical correction is required for the authenticated version. The following is an independent check of the substantive steps, not merely a report that diagnostic code ran.

## 1. Source-level construction

The building in LSV Section 2 is the affine building of PGL_3(F_11((y))). Its vertices are homothety classes of full lattices. Neighbors of a vertex represented by L_0 correspond to proper nonzero subspaces of L_0/yL_0; triangles correspond to proper flags. Thus the building is pure of dimension two, is connected, and each vertex link is the point–line incidence graph of PG(2,11). The integer 3 in PGL_3 corresponds to simplicial dimension 2.

The lattice used in LSV Sections 3–4 is unconditional. Proposition 4.8 states simple transitivity on the building vertices. Its preceding construction, proof and hypotheses do not depend on the Ramanujan theorem of Section 6. In particular, neither the conditional correspondence discussed in that manuscript's introduction nor any finite quotient's global spectrum is being imported into the present proof.

The representation is on the nine-dimensional central simple algebra, using conjugation. Its kernel before taking the projective quotient is exactly the center: an element inducing identity commutes with every algebra element. Passing to the projective group therefore makes the representation faithful. Scalar ambiguity cannot invalidate the inference from a conjugation matrix equal to I to the identity element of Γ.

There is an important ring subtlety that the proof handles correctly. LSV explicitly do not define the cyclic algebra A(R_0) for R_0=F_q[1/y], since it is not an R_T-algebra. They define G′(R_0) as the intersection of the image of G′(k) with GL_(d²)(R_0). Their group Γ′ lies in this intersection, and Proposition 4.8 identifies Γ with Γ′. Thus the claim is membership in a genuine general linear group over the polynomial ring; it is not an assertion that individual polynomial matrices have inverses only in a larger rational-function ring.

Equation (9), inspected in the rendered source, expresses every generator's conjugation matrix as C_0+t C_1 with C_0,C_1 over F_11 and t=1/y. Its finite-field quotients are constants, so they introduce no t-dependent denominator. Terms with a coefficient 1+t may equally be obtained by combining overlapping constant and t terms. Independently, determinant 1 follows by splitting the algebra: on M_3, conjugation has determinant (det A)^3(det A^−1)^3=1. Its polynomial inverse is then its adjugate. This also confirms that reduction modulo t^9 has no invertibility defect.

Corollary 4.6 applies to any lattice L contained in L_0 with index q^i. A neighbor has a representative strictly between yL_0 and L_0, hence i=1 or 2. Both neighbor types are consequently represented by positive words of length at most two in the stated generators. No unjustified inverse-generator degree bound is used.

## 2. Congruence depth and the actual abstract quotient

Reduction to GL_9(F_11[t]/(t^9)) is a homomorphism to a finite group. Its kernel Γ_9 is normal and has finite index. For an element taking the base vertex along a path of length at most four, use the unique Γ-labels of the path vertices. Consecutive labels differ by a neighbor element. Simple transitivity identifies the resulting product with the element itself; there is no residual vertex stabilizer factor. It is a product of at most eight degree-one generator matrices, so every entry has degree at most eight.

An entry of ρ(γ)−I with degree at most eight cannot be nonzero and divisible by t^9. Faithfulness therefore rules out every nontrivial kernel element of displacement at most four at the base vertex. Conjugating by the unique element carrying the base vertex to an arbitrary vertex preserves membership in the normal kernel and gives the same displacement conclusion everywhere.

The passage to the abstract orbit complex was checked directly. A simplex's vertices remain distinct because any two of them have distance one. More generally, two vertices in the closed star of x have distance at most two, so their quotient images are distinct. A quotient triangle containing the image of x has a representative triangle with some vertex in x's orbit; translating that triangle gives one containing x. Its other vertices are uniquely determined by their quotient images, since both are neighbors of x. This proves both surjectivity and injectivity of the link map. If two triangle orbits yielded the same abstract triangle, translating both to contain x would give the same two neighbors and hence the same original simplex; there is no hidden multiplicity.

Inversions or finite-order elements cannot stabilize a simplex nontrivially: a permutation of its vertices would move a vertex by at most one, contrary to the displacement bound. No standalone claim that a free vertex action always gives a simplicial quotient is needed. Likewise, no clique completion is used. Finite index gives finitely many vertices; dimension two, purity and connectedness survive because all building faces retain their dimensions and every one extends to a triangle.

## 3. Link spectrum and irregular deletion

There are q²+q+1=133 points and the same number of lines, each of degree q+1=12. The incidence matrix satisfies MM^T=11I+J. Its singular values are 12 and √11, which gives the adjacency spectrum ±12 and ±√11 and the ordinary Laplacian gap 12−√11. The unique positive top eigenspace also shows connectedness. The point–line graph is bipartite, and two distinct points share exactly one line, ruling out four-cycles. Its girth is at least six.

For H=G−w, extending an unweighted-mean-zero vector by zero gives the claimed lower bound E_H(x)≥(11−√11)||x||². Only one deleted incident edge can contribute at each surviving vertex. To pass to the irregular normalized gap, for arbitrary f subtract its unweighted mean c_0. Its weighted variance satisfies

    min_c Σ_a deg_H(a)(f(a)−c)²
      ≤ Σ_a deg_H(a)(f(a)−c_0)²
      ≤ 12 Σ_a (f(a)−c_0)².

Thus the denominator comparison is in the correct direction and yields λ(H)≥(11−√11)/12>1/2. It does not assume the unweighted and degree-weighted means coincide. Positivity of the ordinary gap proves connectivity of H as well.

As an independent exact check, the deleted normalized gap can be computed more sharply. Delete one point p and write M′ for the remaining incidence matrix. Partition the remaining 132 points into the 12 lines through p, with p removed; each block has size 11. If B is the block-diagonal matrix with a J_11 block for each class, then

    N N^T = (11 I + J)/144 + B/1584,

where N is the degree-normalized rectangular incidence matrix after deletion. The spaces of within-block zero sums, block constants of total sum zero, and all constants have dimensions 120, 11 and 1. The respective eigenvalues are 11/144, 1/12 and 1. Hence the exact normalized gap is 1−1/√12>1/2. Point–line duality handles a deleted line. This sharper computation is supplementary; the proof's weaker bound is already sufficient.

## 4. Weighted cohomology argument

The edge weight m(e) is the number of surviving triangles through that edge. Purity makes each weight positive, so the energy is a positive-definite norm on the real 1-cochains. A cohomology class is an affine translate of the finite-dimensional space of coboundaries, and therefore has an energy minimizer. Differentiating along a vertex coboundary gives precisely the weighted divergence equation Σ_u m(vu)a_vu=0.

For the link function f_v(u)=a_vu, the degree of u in the actual link is m(vu), so this is exactly the degree-weighted mean-zero condition. The cocycle relation on {v,u,w} gives f_v(u)−f_v(w)=−a_uw. Applying the normalized link inequality and summing gives E≥2λE: an edge is counted on the left once for each triangle containing it and on the right once at each of its two endpoints, with its weight. All signs disappear only after the cocycle relation is used and squared. Since λ>1/2, the minimizing representative is zero.

This verifies H^1(X;R)=0 without an unproved appeal to a spectral-vanishing theorem. The argument continues to hold when triangle counts vary after vertex deletion. A connected triangulated torus with six-cycle links and nonzero H^1 is an explicit adverse control for replacing the strict threshold by a non-strict one.

## 5. Complete Cohen–Macaulay and deletion checks

The abstract quotient has exactly 12 triangles through every edge because its vertex links are the incidence graph. Deleting a vertex removes at most one triangle through any surviving edge, leaving at least 11. The original 266 distinct neighbors of any surviving vertex lose at most one, so that vertex still lies on a surviving edge and hence a triangle. Thus deletion preserves purity and dimension two; it cannot secretly produce an isolated vertex or a lower-dimensional facet.

The original complex is connected. Every path using the deleted vertex can have the portion through that vertex replaced by a path in its connected link, establishing connectivity after deletion. The link of a surviving vertex is G or G minus the unique deleted neighbor. All these links have the required strict spectral gap and are connected.

The weighted lemma gives real first-cohomology vanishing for the original complex and each deletion. Duality gives real first-homology vanishing. Integer boundary matrices have the same rank over Q and R, so the claim is genuinely over the fixed field Q. The same rank reasoning extends the result to all characteristic-zero fields and makes no positive-characteristic assertion.

Reisner's criterion is then fully checked: the empty face requires reduced H_0 and H_1 to vanish; a vertex link must be a nonempty connected graph; an edge link must be nonempty; a triangle link has dimension −1 and imposes no vanishing below −1. Nonemptiness also handles the reduced negative-degree conventions. Both the original complex and every induced vertex deletion satisfy the criterion in dimension two. No simple connectivity or vanishing of top-dimensional homology is required for Cohen–Macaulayness here.

## 6. Excluding all permitted sphere pieces

For a two-dimensional homology-sphere subcomplex, an edge link is zero-dimensional with reduced H_0 of dimension one, so it has exactly two vertices. Consequently each edge is in exactly two triangles. A vertex link is connected by its local homology condition, and every link vertex has degree two by the edge condition. It is therefore a simple cycle. As a subgraph of a girth-at-least-six ambient vertex link, its length is at least six.

For its face numbers this gives 2f_1≥6f_0 and 3f_2=2f_1. Hence χ=f_0−f_1+f_2=f_0−f_1/3≤0. The global homology-sphere condition, over any field, instead gives χ=2. This contradiction is characteristic independent. It requires neither orientability in advance nor any classification of surfaces.

A complex with merely the global homology of a sphere would not justify the edge and vertex deductions. The reviewed proof explicitly requires local links. An independent adverse control formed by attaching an extra triangle at one vertex of a tetrahedral sphere retains Betti numbers (1,0,1) but has a non-spherical vertex link, demonstrating that this distinction was actually checked.

## 7. Original question and limitations

The original OWR source defines 2-CM over a fixed field and requires deletions of the same dimension. Its Theorem 7 gives the cover, a full-dimensional face in each successive intersection, and an admissible reordering starting with any chosen member. Problem 8 asks for homology-sphere pieces; the later manuscript poses the corresponding Problem 3.7. The present dimension-two counterexample meets the d>1 target and fails already at the existence of even one sphere piece.

The finite quotient was not enumerated facet by facet. Its existence and all needed properties are proved symbolically; the supplementary diagnostics do not pretend to compute its full boundary matrices or homology. Sources were checked only to the extent described, not audited in their entirety. The review establishes mathematical correctness of this counterexample, not its historical originality or the absence of an earlier answer.

## Public references

- Eran Nevo, OWR 17/2005, printed pp. 960–961, Definition 1, Theorem 7 and Problem 8: https://ems.press/content/serial-article-files/45990
- Eran Nevo, arXiv:math/0505334v2, Definition 3.1, Theorem 3.4 and Problem 3.7: https://arxiv.org/abs/math/0505334v2
- Alexander Lubotzky, Beth Samuels and Uzi Vishne, arXiv:math/0406217v2, Sections 2–4, especially Equation (9), Corollary 4.6 and Proposition 4.8: https://arxiv.org/abs/math/0406217v2
