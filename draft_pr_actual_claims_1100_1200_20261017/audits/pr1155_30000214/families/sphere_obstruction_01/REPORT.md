# Independent adversarial audit of PR 1155, problem 30000214

Decision: **PASS**. No required mathematical repair was found in the pinned `PROOF.md`. This report audits the whole proof, with particular attention to sphere subcomplexes, coefficient fields, local links, quotient identification, deletion conditions, and weighted cohomology.

## Exact claim and original question

The claim proved is existence of a finite two-dimensional simplicial complex K that is doubly Cohen-Macaulay over Q, hence over every characteristic-zero field, and has no two-dimensional homology-sphere subcomplex over any field. This implies a negative answer to Nevo's sphere-cover question, since no first sphere piece exists. No prescribed positive-characteristic CM construction, priority, or comprehensive literature result follows.

The original OWR Problem 8 follows Theorem 7, which ranges over d-dimensional 2-CM complexes over a fixed field, d>=1. It gives a cover by minimal d-cycle subcomplexes with full-dimensional overlaps and admissible reorderings beginning with any designated member. The preprint's Theorem 3.4 and Problem 3.7 agree. The sphere question naturally retains these quantifiers and requirements. Dimension two over Q is within the original scope, and lack of even an unordered cover is a sufficient refutation. Some old supporting prose writes d>1, emphasizing the non-graph case; the original theorem begins at d>=1. This difference does not affect the counterexample or require a mathematical repair.

The source separately defines 2-CM over a fixed field and invokes all face links for CM; it does not give a stand-alone homology-sphere definition. The standard simplicial meaning requires the homology of the appropriate-dimensional sphere in every face link, including the empty face. This is also the convention consistent with Nevo's statement that homology spheres are 2-CM. The candidate explicitly uses this convention. Merely having the global homology of S^2 would be a different and weaker condition. All conclusions below retain the local requirements.

## Source-dependent construction and actual quotient

LSV Section 2, with d=3 and residue field F_11, describes vertices as lattice homothety classes and simplices as flags between yL and L. Every vertex link is therefore the incidence graph G of PG(2,11), and the building is connected, locally finite, pure, and two-dimensional. Sections 3-4 give a faithful conjugation representation in dimension nine, and Proposition 4.8 gives simple transitivity on building vertices. Faithfulness is exact: conjugation has kernel the center before taking the projective quotient, and that center is already factored out.

The polynomial-ring membership is genuine GL_9(F_11[t]) membership, including polynomial inverses. LSV deliberately define G'(R_0) as an intersection inside GL_(d^2)(R_0), rather than defining an algebra A(R_0); Gamma=Gamma' lies in that intersection. Equation (9) maps every basis element to a constant-plus-t combination, so each generator matrix has degree at most one. There is no t-dependent denominator left after expansion in the fixed finite-field basis. Corollary 4.6 represents either type of base-vertex neighbor by one or two positive generators, because its lattice index is 11 or 11^2. Thus a path of length at most four gives an element with matrix degree at most eight. Simple transitivity prevents an unidentified stabilizer factor.

Reduction modulo t^9 is a homomorphism to a finite general linear group. A kernel element with displacement at most four has each entry of rho(gamma)-I divisible by t^9 and of degree at most eight; all entries vanish. Faithfulness gives the identity. Normality and vertex transitivity transfer this displacement bound from the base vertex to every vertex.

This bound suffices for the actual abstract orbit complex used in the proof. Distinct vertices in a closed star are distance at most two and cannot have the same quotient image. Any quotient edge or triangle incident to the image of x has a lift incident to x after translation by the kernel, and its other lift vertices are unique. Consequently every quotient vertex link is exactly G, with neither identified local simplices nor spurious triangles. Finite index gives a finite complex; purity, dimension two and connectedness descend. No clique completion or global type-preserving hypothesis is needed.

These are the only LSV inputs. I inspected the introduction and Sections 2-4, including the proof of Proposition 4.8 and its construction context; I visually checked pages 9, 12 and 13. A whole-text keyword search also exposed selected lines from later sections and the glossary, but I did not audit those later proofs. The Ramanujan/global correspondence result is not an input here. The construction therefore avoids the conditional statement flagged in that source version.

## Deleted-link gap and the weighted implication

G has 133 points, 133 lines, and degree 12. Its incidence matrix satisfies MM^T=11I+J, so the adjacency spectrum is +/-12 and +/-sqrt(11), and the unnormalized Laplacian has gap 12-sqrt(11). The positive top eigenspace is one-dimensional, proving connectivity. Bipartiteness and uniqueness of the joining line exclude cycles of lengths three, four and five.

For G-w, extending an ordinary-mean-zero function by zero at w retains mean zero in G. Subtracting exactly the lost edge energies removes at most its squared norm, giving energy at least (11-sqrt(11)) times that norm. This proves connectivity of G-w. If x is obtained from any f by subtracting its ordinary mean, its degree-weighted variance is at most 12 times the squared norm of x. Thus the normalized gap is at least (11-sqrt(11))/12>7/12>1/2. The comparison uses the correct inequality direction for the weighted-variance minimum and remains valid with degrees 11 and 12. No deleted-link regularity assumption enters.

For a finite pure two-dimensional complex X with all such link gaps >1/2, weight an edge by the number m(e) of surviving incident triangles. Every real cohomology class has a minimum-energy representative a, by orthogonal projection in finite-dimensional cochain space. Orthogonality to vertex coboundaries gives sum_u m(vu)a_vu=0. In lk_X(v), the function f_v(u)=a_vu therefore has zero degree-weighted mean, since deg_lk(v)(u)=m(vu). The cocycle equation gives f_v(u)-f_v(w)=-a_uw. Applying each link inequality and summing counts every edge on the left once per incident triangle, yielding E(a), and on the right at both its endpoints with weight m(e), yielding 2 lambda E(a). Since lambda>1/2, E(a)=0 and H^1(X;R)=0. Every count and weight is computed in X itself, so the lemma applies after deletion as written.

## Every CM and same-dimension deletion condition

Each edge of K lies in 12 triangles, from its corresponding link vertex degree. Deleting z removes at most one triangle from any surviving edge; at least 11 remain. Every surviving vertex retains at least 265 of its 266 neighbors, hence lies in a surviving edge and a triangle. Thus K-z is pure and remains two-dimensional.

K-z is connected: replace each segment through z in a path of K by a path in the connected graph lk_K(z). Each surviving vertex link is exactly G or G minus the one vertex representing z. The strict link gap gives H^1 over R equal to zero for K and every K-z, and finite-dimensional duality gives H_1 over R equal to zero. Their integer boundary matrices have the same ranks over Q and R, proving the rational vanishing needed for the claimed example. The same ranks hold over any characteristic-zero field; no inference to positive-characteristic ranks is made.

All faces in Reisner's criterion have now been checked. The empty face needs connectedness and vanishing H_1; a vertex needs a connected nonempty one-dimensional link; an edge needs a nonempty zero-dimensional link; a triangle has link consisting of the empty face, with no additional vanishing below dimension -1. Nonemptiness also handles negative-degree reduced homology. Hence K and every same-dimensional induced deletion are CM over Q. This proves 2-CM over exactly the field asserted.

## Any-field sphere obstruction

Suppose S is an allowed two-dimensional k-homology-sphere subcomplex for any field k. Its local sphere conditions imply purity. For any edge e, the zero-dimensional link has reduced H_0 of dimension one, so exactly two triangles contain e. In any vertex link, each link vertex has degree two by this edge condition, and the vertex-link homology condition makes the graph connected. It is thus a simple cycle. Since this graph lies in G, every such cycle has length at least six.

Consequently 2f_1>=6f_0 and 3f_2=2f_1, implying chi(S)=f_0-f_1/3<=0. Euler-Poincare over k instead gives chi(S)=2. This contradiction is independent of characteristic, orientation choices, and surface classification. In particular characteristic two does not create an exception. The proof does not confuse a nonzero top cycle or a globally spherical-homology singular complex with a homology sphere. It excludes all permitted first pieces, and therefore the complete cover with any overlaps or reorderings.

## Diagnostics, historical comparison and limits

The independent authored diagnostic exactly constructs PG(2,11), checks all 17,689 entries of MM^T=11I+J, verifies its 1,596 incidences and regular degrees, exhibits a six-cycle, and checks all 266 single-vertex deletions for connectivity and degree multiplicities. Normal Python execution passed. It does not construct the finite quotient K or compute its full homology; the quotient existence and universal sphere obstruction are symbolic deductions above. No such enumeration is needed to justify the claim.

After sealing this independent derivation, I read the thirteen original PR inputs and the parent's retrieval and intake records. Their old acceptance and substantive explanations are consistent with the sealed result. All thirteen current input byte counts and hashes agree with the retrieval receipt; the twelve non-self manifest entries agree as well. The historically reviewed support-file hashes differ where the edition expressly reports later editorial revisions; the proof and source audit identities remain unchanged. I did not rerun the historical diagnostic code and do not adopt its execution claims as mine.

The original source PDFs match the parent's freshly retrieved pins. In this family they were supplied local sources, not downloads performed by me. I copied used source PDFs/text and original PR inputs to the family's private evidence directory after sealing. Other new family/reviewer bodies were never read. A filename inventory exposed their existence only. The reading-scope record spells out keyword-search exposure and corrects the overly terse LSV scope sentence in the immutable mathematical seal; the omitted keyword snippets did not include any prior verdict bodies.

The strongest verified result is the entire theorem at the start of this report. There is no remaining mathematical gap identified within its stated scope. This audit does not certify novelty, external peer review, formal proof-assistant verification, or positive-characteristic CM behavior. No operative repository, PR, publication, account, or external communication action occurred.

## Primary references

- Nevo, OWR 17/2005, printed pages 960-961, Definition 1, Theorem 7 and Problem 8: [original source](https://ems.press/content/serial-article-files/45990).
- Nevo, arXiv:math/0505334v2, Definition 3.1, Theorem 3.4 and Problem 3.7: [inspected version](https://arxiv.org/abs/math/0505334v2).
- Lubotzky, Samuels and Vishne, arXiv:math/0406217v2, Sections 2-4, especially the page 9 embedding, Corollary 4.6, Definition 4.7, Equation (9), Proposition 4.8: [inspected version](https://arxiv.org/abs/math/0406217v2).
