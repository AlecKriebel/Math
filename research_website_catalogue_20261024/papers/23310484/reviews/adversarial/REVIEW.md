# Independent adversarial review — Zenodo 23310484

## Verdict

**PASS with scope limits. No unresolved substantive mathematical defect found.** The published proof supports the stated nonembedding theorem for a missing middle-dimensional face in any finite triangulation of a topological even-dimensional sphere. This is AI review, not human peer review, formal certification, or a priority certificate.

Version 1.0, 12 October 2026. PDF SHA-256: `055a6ff8f3451bedc7b75a106329bf2ffd1f02805a568f7f063c13a9b0eb9e59`. Source SHA-256: `74bb774b46c75deac52e8f77cdb690e30f509c7e5f34b030c69f461f7a6072e1`.

Read the complete 581-line published manuscript source. Extracted PDF pages 1–2 to bind the version, theorem and graded argument to that source. Read the current author checker, supplement README, reproduction driver and opening portion of the bitmask checker. No other new or archived reviewer verdict or mathematical report was read before this verdict. No coordination with the parallel analytic reviewer occurred; source-location information alone was exchanged with the parent.

## Exact claim and logical divisions

For d>=0, a finite simplicial S homeomorphic to S^(2d), and a missing d-face T on the actual vertex set, the augmented d-skeleton does not topologically embed in S^(2d). The d=0 case is vacuous. The proof establishes a PL obstruction in every positive dimension, uses topological-to-PL embedding existence for d>=3, proves a special mod-2 obstruction for d=2, and uses the planar graph bound for d=1.

## Independent reconstruction and attacks

### Graded algebra

Taking the d-skeleton first removes squarefree faces in degree d+2. Its ring therefore agrees with the original ring through degree d+1, including all maps in the total-degree d+1 first Koszul homology computation. The augmentation kernel is zero through degree d and one-dimensional in degree d+1. Regularity on the original source ring makes the relevant first Koszul homology vanish. The resulting exact sequence genuinely makes the additional class survive quotienting; it is not just a monomial count before imposing parameters.

Local integral sphere homology and global sphere homology supply Cohen–Macaulayness and the symmetric Hilbert function. Generic ambient parameters restrict to parameters on S because each facet determinant is a nonzero polynomial in independent coefficients. They are overlong on the augmented skeleton, but the proof correctly uses a quotient by that sequence rather than falsely treating it as an l.s.o.p. there.

The ambient completed PL sphere is an F2 homology sphere. Karu–Xiao anisotropy over Q(a_ij), with n=2d+1 and m=d, makes multiplication by l injective from degree d to d+1; symmetry makes it surjective. Surjectivity descends to any graded quotient by lifting a target, lifting its preimage upstairs, then projecting. The established dimension jump contradicts that surjection. No additional Lefschetz property of the augmented complex is presumed.

### Completion and metastable conversion

Adiprasito–Patáková Theorem 2 retains the original abstract complex as a subcomplex of an ambient triangulation and permits changing the embedding. This exact form is required: a result only retaining a subdivision would not suffice.

A topological embedding omits a point of S^(2d) by dimension, yielding an embedding in R^(2d) and its equivariant difference map. The sufficient existence inequality 2m>=3n+3 gives d>=3 after n=d,m=2d, including d=3. The proof needs existence of some PL embedding, not approximation or isotopy of the original one.

The original Weber scan was not freshly readable: E-Periodica served a verification page, which I did not bypass. The exact sufficient range and its equality case were directly checked in Skopenkov's author-written exposition, Theorem 8.1 (printed p.52) and the relevant proof discussion for m=2n>=6 and for the general range. This limitation concerns the original-page retrieval, not uncertainty in the existence threshold.

### Four-dimensional source and complement

Automatic combinatorial structure is invoked only in dimension four. Positive-dimensional links have dimensions at most two; vertex links become simply connected homology 3-spheres by the nested conical/coordinate neighborhood argument, then are PL spheres by three-dimensional Poincare and PL uniqueness. The Davis–Fowler–Lafont source explicitly confirms this. It does not imply that the resulting global PL 4-sphere is standard.

The boundary of a legal support ball is locally flat: its local pairs reduce to PL 2-spheres in PL 3-spheres and lower-dimensional pairs. The complementary PL manifold has a collar. Van Kampen on the collared decomposition gives trivial fundamental group. The fundamental-class map to the ball-relative-boundary group has degree one, so the pair sequence gives reduced integral homology zero, including H3. Hurewicz and Whitehead then give contractibility. No global PL four-dimensional Schoenflies theorem is used.

### Common missing triangles and Nevo–Wagner transfer

I checked the actual Section 5 setup and conditions (I.a), (I.b), (II.a), (II.b), not merely the name of Theorem 5.3. A self-intersecting disk map is enough; the theorem does not require an embedded filling disk.

The old support is induced because its faces are exactly the subsets not containing the full missing beta. A common missing triangle on support vertices would have to equal beta and would become a face. A common missing triangle also cannot contain alpha, since it or a proper face would disappear. Thus the augmentation respects the structural and removed-star conditions.

The common boundary loop lies in the complement. Contractibility gives a disk map. A collar moves its interior off the complementary boundary, and relative general position avoids the old 1-skeleton because 2+1<4. Exterior triangle intersections and disk self-intersections are allowed; support-triangle intersections are excluded. The two maps agree on the common complex. Their finitely many forbidden disjoint compact pairs have positive separations; a sufficiently close simultaneous general-position approximation preserves those separations and common restrictions. The puncturing homeomorphism need not itself be PL.

There is one harmless implicit choice: select the puncture away from both the old support 2-skeleton and the image of the new one under the chosen ball homeomorphism. Choose that homeomorphism first, then a point outside their union. A finite union of these closed 2-dimensional images has empty interior in the 4-ball. This is a routine existential choice, not an unresolved substantive defect or an extra topological hypothesis.

An induced ball cannot exhaust the sphere's vertices. The outside vertices agree under every move type. For W=R0 minus a common-boundary face rho, Q[W] has a nonempty simplex join factor and is a cone. Alexander duality gives acyclicity of its complement. Normalizing the barycentric coordinates outside W supplies the deformation retraction onto Q-W. The 2-skeleton has the same H0,H1, and triangle augmentation can only quotient H1. These are the precise transfer homology assumptions.

Applying the same argument to the old unaugmented skeleton gives the support-avoiding cone chains. Their inductive boundary cycles bound in the required deleted complexes; actual cone simplices are retained when present. For a face meeting the exterior, its intersection with the support supplies a common-boundary face and the same deletion argument. Thus the proof does not assume geometric cones that need not exist.

### Newly missing triangles and witness

The only nontrivial cases are (2,2), where augmentation by the new missing alpha equals old augmentation by beta, and (3,1), where M is an outside vertex joined to the newly introduced beta edge. The other three types introduce no new missing triangles. In vertex insertion, any candidate triangle whose proper edges exist is already a support face.

The formal seven-vertex Flores deleted-product chain has each boundary edge/triangle pair twice. At most one factor of each disjoint pair contains the outside vertex. Support avoidance therefore keeps the coned factors disjoint, including boundary cells, and the chain map produces a genuine cycle. All cones lie in the old unaugmented skeleton, so M only arises from its explicit assignment. Its partner chain is precisely the four triangles in boundary(alpha).

In the explicit move ball, alpha and beta lie in complementary R3/R1 subspaces with one transverse interior intersection. The other two boundary edges of M miss the ball interior. Thus the loop links boundary(alpha) with parity one. The linking/intersection boundary relation evaluates the M contribution as one; all other pairs belong to the embedded unaugmented new skeleton and contribute zero. This verifies the new-triangle case without assuming it was previously missing.

### Base and edge cases

Barycentric subdivision is flag because pairwise comparable faces form a chain, so its missing-triangle assertion is vacuous. Pachner's theorem connects it to S within their actual shared PL class. No equivalence with the standard PL sphere is needed. Every intermediate remains topologically S4, as required for the complement and duality arguments.

For d=1, one extra edge exceeds 3n-6. For d=0, no missing actual singleton exists. I found no omitted dimension or hidden ghost-vertex convention.

## Fresh source-reading scope

- Nevo–Wagner: relevant definitions, Section 5 setup, assumptions, Lemma 5.2, Theorem 5.3 statement and local new-face witness discussion. https://pi.math.cornell.edu/~eranevo/homepage/NevoWagner-EmbeddabilitySkeletaSpheres-Rev2.pdf
- Adiprasito–Patáková: Theorem 2 and permission to change the embedding. https://arxiv.org/html/2404.12265v3
- Karu–Xiao: Theorems 1.2–1.3 and the characteristic-zero hypothesis. Publisher PDF returned 403; author arXiv version was accessible. https://arxiv.org/pdf/2204.07758
- Davis–Fowler–Lafont: printed p.797, automatic PL triangulations in dimension four. https://msp.org/agt/2014/14-2/agt-v14-n2-p06-p.pdf
- Lickorish: Theorem 5.9 with its closed combinatorial manifold hypotheses. https://arxiv.org/pdf/math/9911256
- Skopenkov: Theorem 8.1 and relevant Weber proof discussion. https://webhomes.maths.ed.ac.uk/~v1ranick/papers/skop.pdf

These are focused dependency readings, not complete readings of all cited publications or an exhaustive novelty search. No inaccessible original is claimed as inspected.

## Reproducibility and fresh bounded controls

The published driver completed six normal/optimized checker cases and matched expected outputs byte for byte; see `reproduction.json`. Its manifest checks and explicit runtime guards were inspected.

The new `independent_checks.py` constructs a support ball plus a cone on its boundary for each of the five move types. It checks inducedness, newly missing triangle classification, the middle-move identity, and 166 deleted-complement H0/H1 calculations. It separately checks the 70-cell Flores cycle, zero boundary, the four partner triangles for M, exact rational moment-curve circuits and seven crossings, and rejection of a one-cell deletion mutation. Complementary-subspace coordinates are rational.

Normal and optimized executions passed. A disk-full error prevented saving the separate optimized output; its successful rerun is in captured tool output. The saved normal result is `independent_checks.json`.

These standard finite examples do not certify arbitrary topology, exotic structures, generic anisotropy, contractibility or the universal conclusion. Those checks rely on the reconstructed argument and imported theorems above.

## Recommendation

Proceed to the parent's publication gate for this exact version, retaining the unrefereed/AI disclosure and credit to imported mechanisms. No defect deferral is warranted from this review.
