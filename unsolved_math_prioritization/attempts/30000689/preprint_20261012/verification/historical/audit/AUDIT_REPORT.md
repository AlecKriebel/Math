# Independent adversarial audit: 30000689 / OWR-1455-008

## Verdict

**PASS: no substantive mathematical gap found in the frozen full affirmative argument.**

This verdict concerns the exact statement for arbitrary finite triangulations of a topological `S^(2d)` and arbitrary topological embeddings of the augmented d-skeleton. It does not silently restrict the source to standard PL spheres or the proposed embedding to a tame one. The delicate dimension-four extension survives the checks below.

This is an independent AI-assisted mathematical audit, not formal verification or independent human peer review. It establishes neither novelty nor priority. Acceptance of the published theorems cited below remains part of the proof's ordinary mathematical dependency structure.

- Audited date: 3 October 2026 UTC.
- Frozen proof SHA-256: `ededf69202a381a209eaca65bd57bf49fef5da46a8b4e40742a37e65170fbe4c`.
- All six manifest-listed author files matched their recorded hashes before and after review.
- Every author-public file was read. No frozen author file was modified.
- The earlier author-side targeted checks were not used as premises.
- This directory contains first-party review and compact verification artifacts only. Source PDFs, complete foreign papers, and source-page images are excluded.

## 1. Target and prior-result boundary

The original Oberwolfach statement, Conjecture 4 on printed p. 238, agrees with the manuscript's target. Its page was checked as text and visually. The later Nevo–Wagner author paper distinguishes Theorem 1.2 (standard PL source sphere) from Conjecture 1.3 (arbitrary triangulated sphere). Its Theorem 1.4 addresses reconstruction as a whole skeleton, which would not suffice for the present embedding claim. The candidate does not make that substitution.

Sources: [Oberwolfach Report 4/2007](https://ems.press/content/serial-article-files/46090), [Nevo–Wagner author paper](https://pi.math.cornell.edu/~eranevo/homepage/NevoWagner-EmbeddabilitySkeletaSpheres-Rev2.pdf).

The catalogue's dated open-status label is not evidence that the problem remained unresolved at the audit date. A bounded independent terminology/citation search did not locate an explicit prior resolution of this exact formulation; this negative result is not a novelty certification. Repository duplicate-history assertions were not independently rerun and are not part of the mathematical PASS.

## 2. Algebraic dimension jump: verified

The local homology of a triangulated topological manifold gives the required integral homology of every face link. For a sphere, the empty-face condition holds as well. Thus the Cohen–Macaulay and Dehn–Sommerville inputs apply even to a non-combinatorial triangulation in higher dimension.

The degree bookkeeping was independently reconstructed:

1. Removing faces of dimension above d first changes the Stanley–Reisner ideal in degree d+2. Thus A and C have the same multiplication in all degrees used to compute the total-degree-(d+1) first Koszul homology.
2. The missing-face assumption gives exactly one new degree-(d+1) monomial, namely x_T; lower degrees do not change.
3. Regularity is required on A, not on B or C. It gives vanishing of the first Koszul homology of A, hence of C in the one relevant degree.
4. In the long exact sequence for `0 -> M -> B -> C -> 0`, the degree-(d+1) zeroth Koszul homology of M equals M_(d+1), because M_d is zero.
5. Therefore this class injects after quotienting. The asserted dimensions are h_d and h_d+1, rather than just an unproved difference before quotienting.

Using 2d+1 linear forms on the lower-dimensional ring B is legitimate: they are restricted ambient parameters, not an alleged regular parameter sequence on B. The manuscript explicitly makes this distinction.

## 3. Ambient extension and Lefschetz input: verified

Adiprasito–Patáková Theorem 2 was checked both in the author version and the published full text. It retains the given finite abstract complex as a subcomplex of an ambient triangulation; merely retaining a subdivision would be insufficient here. It permits changing the embedding map. The relevant hypothesis is a PL embedding into a PL manifold, exactly the temporary hypothesis in Section 2.

Sources: [published full text, Theorem 2](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/blms.70036), [author version](https://arxiv.org/abs/2404.12265).

Karu–Xiao Theorems 1.2–1.3 were read in the published PDF and the theorem page was visually checked. The characteristic-zero assertion is over Q(a_ij), with the independent coefficient variables used for the linear parameters, and the Lefschetz element is the sum of the vertex variables. The relevant homology-sphere hypothesis is over F_2, which an integral homology sphere satisfies. With their n=2d+1 and m=d, the exponent n-2m is exactly 1. Hence multiplication by the sum is injective in degree d; symmetry makes it surjective onto degree d+1.

Source: [Karu–Xiao, published article](https://alco.centre-mersenne.org/articles/10.5802/alco.298/), printed p. 1314 and the homology-sphere definition in Section 2.

The simultaneous parameter choice is valid. Restriction to the source vertex set leaves algebraically independent coefficients. Enlarging the coefficient field by the other independent variables does not spoil regularity. The face-ring map from the ambient triangulation to the unchanged complex is a graded surjection, and quotienting by the same restricted forms preserves the commutative multiplication square. Surjectivity passes to this quotient, contradicting the dimensions above.

Only that the ambient triangulation is a topological sphere, hence an F_2-homology sphere, is needed for this algebraic conclusion. Thus no extra issue concerning the wording of the ambient PL structure is essential to the argument.

## 4. Topological versus PL embeddings in d >= 3: verified from the original theorem

Weber's original 1967 paper was recovered through the archive's expressly provided crawler link. Theorem 1 on printed p. 2 was read and visually checked; Section 1 defines its semilinear category as PL. The existence statement applies to finite n-polyhedra and assumes `2m >= 3(n+1)`. It is corroborated by Skopenkov Theorem 8.1.

Sources: [Weber archival article](https://www.e-periodica.ch/cntmng?pid=com-001%3A1967%3A42%3A%3A6), [Weber bibliographic record](https://link.springer.com/article/10.1007/BF02564408), [Skopenkov survey](https://arxiv.org/abs/math/0604045).

A topological embedding of the finite d-polyhedron into the 2d-sphere leaves a point outside its image, by topological dimension. Puncturing gives an embedding into Euclidean 2d-space and therefore an equivariant normalized-difference map on the full deleted product. Weber produces a possibly unrelated PL embedding. The substitution n=d, m=2d gives precisely d>=3, including equality at d=3. No tameness, PL approximation of the original embedding, or isotopy classification is being asserted. The excluded d=2 case is treated independently.

## 5. Dimension-four transfer: reconstructed in detail

### 5.1. Combinatorial structure, with no standard-S^4 assumption

The positive-dimensional links are manifolds by induction on their dimensions, and their homology identifies the links of dimensions at most two with standard spheres. Vertex links are closed triangulated 3-manifolds. To check simple connectivity, push any loop radially into a sufficiently small punctured coordinate 4-ball contained in the open vertex star; contract it there and retract back to the link. Poincare in dimension three and the PL uniqueness in dimension three complete the link argument.

Davis–Fowler–Lafont explicitly record the same triangulation fact on printed p. 797: [author paper](https://people.math.osu.edu/lafont.1/agt-DFL.pdf).

This proves combinatorial-manifold structure. It does not identify a potentially exotic PL 4-sphere with the standard one.

### 5.2. Complement lemma is sufficient and does not assert a false ball inference

At each boundary vertex of a bistellar 4-ball, the boundary link is a PL 2-sphere inside a PL 3-sphere. Three-dimensional PL Schoenflies gives the standard local pair, hence local flatness and a collar. The complementary closure is therefore a compact PL 4-manifold with boundary S^3.

Its complement is connected: every component must meet the boundary, and the boundary is connected. Collared van Kampen identifies its fundamental group with that of the entire S^4, since the ball and common S^3 are simply connected. Mayer–Vietoris, with the fundamental class mapping to the boundary generator, makes the complement acyclic. A simply connected acyclic CW complex is contractible.

The candidate never infers that this complement is a PL ball. The only filling needed is a continuous disk map extending the missing-triangle boundary. Contractibility supplies it. Collaring pushes the interior away from the move support, and relative general position in the PL complementary manifold keeps the disk interior off the 1-skeleton. Self-intersections of the disk are harmless for this use. In particular, no four-dimensional PL Schoenflies or smooth Poincare assertion is imported.

### 5.3. Exact structural hypotheses behind the transfer theorem

The original Nevo–Wagner Section 5 was read through, including its setup, Observation 5.1, Lemma 5.2, Theorem 5.3, and both new-face cases. Besides the cochain and homology conditions listed in the candidate, its setup requires inducedness of the skeletal support and containment of the removed simplex's star in that support. These conditions hold here:

- A bistellar support is induced on its vertices because the complementary simplex beta is a missing face.
- If a triangle M is missing before and after the move, M cannot be contained in the support's vertex set: the only minimal nonface there is beta, and beta is introduced by the move.
- Such M cannot contain the removed simplex alpha. Otherwise a proper face containing alpha disappears, contradicting that M remains missing, except M=alpha, which is a face before the move and therefore is not a common missing triangle.
- Thus adding M does not destroy inducedness or enlarge the removed star. Its boundary avoids the interior of the old support.

Use the complementary disk map and the natural embedding of the old skeleton to define f. Transport the new support by a relative-boundary homeomorphism of the two standard bistellar balls to define g. The maps agree on their common subcomplex. All forbidden disjoint-simplex pairs involving a support have disjoint compact images. Their positive separations survive a sufficiently small simultaneous PL approximation of the map on the union of the two complexes. This verifies both general-position/cochain requirements even if the chosen puncturing homeomorphism is not PL.

For the homological condition, write each common support face as rho=sigma*tau in boundary(alpha)*boundary(beta). Removing its vertices from the old support leaves a cone with a vertex in alpha minus sigma. Alexander duality in the topological sphere makes its complement acyclic. The complementary induced complex is a deformation retract, by normalizing the barycentric coordinates on vertices not removed. Taking its 2-skeleton preserves H_0 and H_1; adding a 2-face cannot create either. An outside vertex exists because an induced ball cannot be the whole closed sphere. These checks include the vertex-creating and vertex-deleting endpoint moves.

This supplies all needed hypotheses, without treating the original PL-sphere Observation 5.1 itself as an unrestricted theorem.

### 5.4. Newly missing triangles, especially the linking witness

The classification of the new cases follows directly by inspecting which faces a bistellar move changes. A newly missing triangle that was a face must be alpha, with p=q=2; augmenting then gives exactly the old skeleton augmented by beta. Otherwise it is v*beta, with p=3, q=1 and v outside the support.

For the latter case, use the old unaugmented 2-skeleton for the homological cones. The same induced-complement calculation applies, so there is no dependence on an old missing triangle. All edges on the six support vertices other than beta lie in that old skeleton. They can be coned homologically to v, avoiding the other support vertices. Map the formal Flores triangles on the seven vertices as follows: preserve support triangles, send v*beta to M itself, and send all other v-containing triangles to these cone chains. The disjointness property makes the formal disjoint-pair sum a deleted-product chain. The cone boundary identity makes its boundary zero. M is paired precisely with boundary(alpha); no cone chain contains M, since the cones lie in the old skeleton.

Inside the explicit ball boundary(alpha)*beta, one may fill boundary(alpha) by a 3-ball meeting the interior of beta once. The other two edges of boundary(M), with outside vertex v, miss that filling. Hence the mod-2 linking number of boundary(M) with boundary(alpha) is one. Under a homeomorphism of the punctured sphere this remains true. Extend to M and use linking/intersection duality. All pairs not containing M have zero intersection contribution from the naturally embedded skeleton, so the witness pairing is one. A sufficiently close general-position approximation preserves these mod-2 data. This completes the new-face case with only a topological ambient sphere and a standard local move ball.

### 5.5. Flag base and Pachner's theorem stay in the correct PL class

Barycentric subdivision is flag because a set of pairwise comparable faces is a chain. It therefore has no missing triangles. Its universal missing-triangle property is genuinely vacuous, which is a valid base for a property preserved by every bistellar move.

The identity between a PL complex and its barycentric subdivision is PL. Lickorish Theorem 5.9 applies to closed combinatorial manifolds in the same PL class, not merely to standard spheres. Hence it connects S to its own subdivision even if that PL class is exotic. Every intermediate complex is still topologically S^4. There is no induction from the boundary of a simplex hidden in this step.

Source: [Lickorish, Theorem 5.9](https://arxiv.org/abs/math/9911256), printed pp. 303 and 315.

A nonzero mod-2 van Kampen class prohibits arbitrary topological embeddings: an embedding's difference map factors the classifying map through the appropriate finite-dimensional projective space. Completeness of that obstruction in dimension four is neither asserted nor needed.

## 6. Low dimensions

For d=1, the triangulated 2-sphere has 3n-6 graph edges; one missing edge exceeds the planar simple-graph bound. For d=0, a missing singleton on the actual vertex set cannot occur. The manuscript also separately handles the convention allowing a new singleton. These boundary cases are consistent with the full statement.

## 7. Exact controls and their limits

The author's standard-library checker was inspected and rerun. Its output is byte-identical to the frozen `exact_results.json`. Its Vandermonde parameters have nonzero facet minors in the tested prime field. The monomial/quotient ranks, Flores cycles, flag check, and metastable inequalities have the stated limited roles.

An independently written checker, `check_independent.py`, adds Section 4 stress tests on 100 reproducible bistellar transitions of triangulated 4-spheres:

- All five move types appear: p=0,1,2,3,4 occur 9,20,28,30,13 times.
- 3,542 cone and complementary reduced-H_0/H_1 checks pass.
- 824 persistent missing-triangle checks verify the structural restrictions.
- 28 newly missing p=q=2 cases verify equality of the augmented complexes.
- 70 newly missing p=3,q=1 cases explicitly construct the homological-cone witness, check disjoint support for every cell, verify zero deleted-product boundary, and verify that M is paired exactly with boundary(alpha).
- For every one of those 70 cycles, the exact moment-curve intersection evaluation is odd.

The independent code imports no author checker functions. All calculations are combinatorial or over F_2, with a fixed seed and no floating-point geometry. They do not recognize exotic spheres, prove Schoenflies/Pachner, replace the universal algebraic argument, or turn this review into a formal proof.

## 8. Nonblocking exposition improvements

The frozen proof need not be altered for this verdict. A later explanatory revision could:

1. State explicitly the induced-support and star conditions, and the agreement of f and g on the common complex, rather than summarize only the numbered cochain/homology conditions.
2. Write “disk interior avoids the 1-skeleton” in Section 4.3. Its boundary necessarily lies in that skeleton.
3. In the new-face case, identify the old unaugmented 2-skeleton as the complex used for the cone construction.
4. Give Weber's original Theorem 1, printed p. 2, as the direct locator. Skopenkov Theorem 8.1 is accurate corroboration.

These are clarifications of valid steps, not repairs of a counterexample or missing essential hypothesis.

## 9. Reproducibility and publication boundary

Run both checkers and compare their JSON results. `AUDIT_MANIFEST.json` records file hashes and the frozen input verification. The author freeze remains intact. This audit performed no repository push, release, DOI creation, external outreach, or other remote mutation. Its public-safe deliverables contain no source PDFs or complete third-party articles.
