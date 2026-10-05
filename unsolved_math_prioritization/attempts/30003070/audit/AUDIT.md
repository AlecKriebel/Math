# Independent audit: plabic Newton–Okounkov bodies via birational root sequences

## Verdict

**PASS, strictly scoped to the retained partial results and the explicit unsolved disposition.** Problem 30003070 / OWR-14221-006 remains **unsolved after five approaches** in this packet. This audit certifies neither a full solution nor a counterexample, a complete prior resolution, originality, or worldwide current openness.

No blocking mathematical error or mandatory correction was found in the frozen packet. Four precision improvements are recorded below. The author freeze was not edited, and no remote writes were performed.

The independent exact verifier performs **68,198 explicit runtime checks** when the author freeze, archive and six private source PDFs are supplied. It does not import the author's mathematical implementation. Its standalone mathematical mode performs 68,132 checks. The independent harness rejects **18 deliberate corruptions** and exercises normal Python, `-O`, `-OO`, and `PYTHONOPTIMIZE=2`. Each mode produces byte-identical mathematical output and still rejects an explicitly false runtime requirement. All checked Python programs contain zero `assert` statements.

The author's own 32,332-check replay and all 13 author corruption controls also pass in each of those four modes. These counts describe finite checks; the universal partial assertions are supported by the proof audit, not inferred from the counts.

## Frozen identity and evidence boundary

- Author archive: `PLABIC_30003070_AUTHOR_SAFE.zip`, 24,377 bytes, SHA-256 `4ae7e2309f630c0008eed27ebdc297dee0817e23669eae5f5cefa35e595013fe`.
- Author manifest SHA-256: `6dc7b5dc2209ed8ef3285b4b7da123df2285d328236b907fd7bad4ff17098c9e`.
- The archive's 11 unique members match the strict author tree byte for byte. The manifest lists ten members and excludes itself; this is consistent with eleven archive files.
- A separately read, already present descriptor catalog has 21,735,099 bytes and SHA-256 `891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566`. Exactly one selected record matches the ID, rank 729, OWR identifier, title, scholarly source URL, statement hash and review hash recorded in the packet. Only match metadata is retained here.
- The exact imported raw statement and prior AI report were not inspected. The previously denied raw-record retrieval was not retried or circumvented. The numeric problem landing page also remains uninspected in this audit.
- All six scholarly PDFs were freshly downloaded independently from their recorded public URLs. All six byte counts and SHA-256 values match the author metadata. These files and their extracted text remain private and are excluded from the audit deliverable. Byte identity does not mean every page or cited proof was independently verified.
- Repository absence claims are treated as the author's bounded historical observations. This audit does not independently certify exhaustive repository history or an absence of prior attempts.

## Exact target and prior-result scope

The original 2016 Fang contribution is the controlling source for the mathematical question used here. Its surrounding definitions concern Grassmannians, reduced top-cell plabic graphs, and positive powers of the Plücker line bundle. Its final question allows changing both birational sequences and suitable total orders. The neighboring mirror-graph theorem and complement-cluster conjecture are distinct. Thus neither a Gr(2,n)-only result nor an iterated-sequence classification answers the full target. The source does not itself formally specify an equivalence relation in that final sentence; the packet transparently chooses affine unimodular comparison as its working formulation. [Original OWR report](https://ems.press/content/serial-article-files/46617)

For Gr(2,n), the cited comparison is stronger than an abstract isomorphism of unpolarized toric special fibers. The plabic paper's Theorem 4.6 and Remark 4.9, together with Bossinger's Theorem 2, provide the matched homogeneous initial-ideal and degree-one Khovanskii-basis route. Bossinger's Corollary 2 directly compares sequence-side bodies; it alone is not the entire plabic-to-sequence argument. Remark 4.9 states rather than fully develops its comparison, and this audit does not reconstruct that published theorem from first principles. [Plabic paper](https://arxiv.org/abs/1612.03838), [Bossinger](https://doi.org/10.1016/j.jalgebra.2021.04.028)

Here is the required ambient-lattice justification. For a birational chart valuation, each chart coordinate is a rational function of value a standard basis vector. Every rational function on the projective Grassmannian is a quotient of equal-degree homogeneous sections. The difference of their graded values is therefore `(0,e_i)`. The reference section gives `(1,0)`. The full graded value semigroup generates `Z^(d+1)` as a group. If that semigroup is generated in degree one, its degree-one columns generate this same lattice. Matching the homogeneous toric kernel, after the source's variable permutation, therefore meets Lemma 3.2's hypotheses. This closes the lattice step without replacing it by a rational-rank argument.

The 2025 work studies a restricted iterated family with a prescribed height-weighted opposite-lex order. Its Gr(3,6) computation reports 240 initial ideals in four S6-orbits, of sizes 48, 48, 48 and 96. The orbit types are EEFF1, EFFG, EEFF2 and EEFG; the reported omissions include EEEG and GG. This is not a classification of arbitrary root sequences and arbitrary permitted orders. Its computational enumeration was source-checked, not rerun. The arXiv record inspected on 2026-10-05 is v1 and has no journal reference. [Torres Henestroza](https://arxiv.org/abs/2511.03885)

A bounded independent search found no verified all-k/all-graph resolution in the inspected primary material. That is an evidence limit, not a global openness claim.

## Proof-by-proof audit

### Normalization, grading and powers of O(1): PASS

Changing the reference section subtracts its fixed integral valuation from normalized values. The O(r) scaling argument correctly uses powers of every section to recover the same closed normalized convex hull from degrees divisible by r. It does not discard higher-degree sections. The warning that unpolarized toric isomorphism does not determine a polarized lattice polytope is correct.

### Lemma 1.1, PBW chart: PASS

For the indicated cross-block roots, every product of two corresponding elementary matrices vanishes. The product is therefore a block-unipotent matrix with an arbitrary lower rectangular block, and its inverse is the unique normalized representative on the highest-Plücker big cell. This proves an isomorphism, not merely generic dominance. The independent matrix implementation checks all 24 root orderings for Gr(2,4).

### Lemma 1.2, row extension: PASS

The old k-plane is recovered by projection on the dense open where that projection has rank k. A normalized representative is fixed there. Any chosen k-row minor is nonzero somewhere on the full Grassmannian, so its determinant is not identically zero on the dense old chart. Solving the row equation gives a rational inverse. The new negative-root factors commute and act by the claimed row operations. This supplies birationality rather than relying on a Jacobian or dimension count. The independent program checks 88 exact row-subset instances of the inverse. The word “append” concerns the construction; under column-vector conventions the new factors are placed to the left of the old product.

### Lemma 2.1, all-function monomial transport: PASS

The unimodular exponent map is injective on Laurent exponents, so distinct terms cannot cancel after substitution. The explicitly required order compatibility transports the least exponent. Quotients extend the statement to the full rational function field, hence to every section degree. The warning that a transported ordered-group structure need not restrict to a permitted monomial order is essential and correctly retained.

The birational countercontrol also works: two different y-coordinate generators have the same least x-exponent, while their difference exposes a larger exponent. Therefore general rational chart equivalence cannot be replaced by one invertible linear transformation of valuations. The independent verifier also checks 1,176 Laurent-support pairs under a genuinely compatible unimodular monomial change.

### Lemmas 3.1 and 3.2, graded semigroups: PASS

Degree-one semigroup generation gives convex combinations of degree-one values in every degree, hence an integral polytope. Generation of the section algebra alone does not give this conclusion, because linear combinations can cancel leading terms.

Equality of integral kernels plus full generation of the ambient graded lattice defines a unique automorphism by `A z -> B z`. Preservation of the first coordinate forces the displayed affine block form. Merely equal rational rank is insufficient: the two column sets `(1,0),(1,2)` and `(1,0),(1,1)` have equal zero kernels and full rational rank, but the first spans an index-two sublattice. This independent negative example confirms the necessity of the hypothesis.

### Proposition 3.3, complete Gr(2,4) semigroup: PASS

The relation and its leading-value kernel are correct. Reduction removes a factor z0*z5 and strictly decreases the sum of the two relevant exponents. The remaining normal monomials therefore span the Plücker algebra. Distinct normal monomials cannot differ by a nonzero multiple of the kernel vector: either sign would force one of them to contain both z0 and z5. Their distinct leading exponents prove linear independence and prevent leading cancellation in an arbitrary nonzero linear combination.

The use of the entire section ring relies on projective normality, equivalently surjectivity of Plücker multiplication; this is supplied explicitly later in Theorem 5.1 and is standard for the Grassmannian. The proof is all-degree. Independently, 20,196 normal monomials through degree 14 are checked against both the binomial-count formula and the representation-theoretic Hilbert count `(r+1)(r+2)^2(r+3)/12`. Exact row reduction of the complete spaces spanned by Plücker products through degree 5 finds every possible leading value, including those exposed by cancellation, and matches the generated semigroup.

### Lemma 4.1 and mutation control: PASS

The 3-by-3 braid identity is correct. The independent verifier checks all nine entries as symbolic rational functions, not just at numerical samples. The two tropical matrices both have determinant one. The specified two-point witness genuinely violates additivity. A grid of 1,331 lattice inputs checks both chamber formulas and the tropical involution.

One domain clarification is advisable: the matrix identity holds wherever a+c is nonzero, but the stated rational inverse also needs A+C=b nonzero. Birationality is on this smaller dense open; it is not an everywhere inverse on the whole identity domain. The packet does not need the stronger statement.

The packet correctly does not equate a local rank-two factorization, a general plabic square move, and a globally linear unimodular transformation. Positive coordinate expressions also do not exclude cancellation in arbitrary sections.

### Theorem 5.1, all-degree unit-cube bound: PASS

This is the strongest retained universal partial result. On the exterior representation, the root derivation replaces i by j, and a second application is zero. Each parameter position therefore enters its exponential factor linearly. This remains true when the same root is used at several distinct positions. The highest Plücker coefficient is one because the product is lower unipotent.

Plücker multiplication is surjective: its image is a nonzero invariant subspace of the irreducible section representation in degree r, hence all of it. Consequently every degree-r section pulls back to a polynomial with each individual parameter degree at most r. Addition or cancellation can remove monomials but cannot introduce exponents outside `[0,r]^d`. Any allowed least-term order chooses an exponent in that finite box. Division by r and closure preserve containment in the closed unit cube. No finite-generation, saturation, degree-one Khovanskii-basis, or integrality assumption enters this proof.

The torus-weight and root-height formulas also follow term by term. The qualification about sums of different weights is correct. The independent implementation uses actual n-by-k matrix products and determinant expansions, structurally different from the author's wedge replacement routine. It checks the author's two examples plus a birational Gr(2,4) chart with a repeated root, and expands all degree-two and degree-three Plücker products in these charts.

### Proposition 5.2, exact Gr(3,6) cube certificate: PASS

Private visual inspection of page 22 confirms that the source is the left graph G1 in Figure 9 and that all nine diagram positions and the fractional coordinate vector in Table 3 are transcribed exactly. Section 9 identifies the body as the convex hull of its Plücker values and that extra vertex. Theorem 15.1 and Definition 14.3 give the max-diagonal rule used by the packet; constant row-minus-column is the correct diagonal convention. [Rietsch–Williams](https://arxiv.org/abs/1712.00447)

The independent computation enumerates partitions via three-element subsets of a six-element set, forms Young-diagram set differences, and counts full diagonals. Fraction-free Bareiss elimination gives det(U)=1; exact inversion produces an integral inverse and verifies every inverse column. All twenty transformed integral points lie in `{0,1}^9`; the extra point maps to `(1/2,0,1/2,0,0,0,0,0,1/2)`. The displayed degree-one value columns have determinant -1. The separating functional takes only 0 and 1 at the twenty degree-one points and -1/2 at the extra vertex.

Thus the extra point is genuinely outside the degree-one hull, while the complete source body still satisfies the root-sequence cube obstruction. Nonintegrality rules out degree-one value-semigroup generation; it does not rule out arbitrary root sequences. The packet draws exactly that limited conclusion.

## Precision improvements, not blockers

1. In the target paragraph, keep the phrase “working affine-unimodular formulation”; the final OWR question does not formally define that relation.
2. Add the explicit ambient-lattice argument above when citing the Gr(2,n) comparison. Do not attribute the entire plabic-to-sequence step to Bossinger's Corollary 2 alone.
3. In the 2025 discussion, “four S6-orbits of initial ideals for PBW-started iterated sequences with the prescribed order” is more precise than “four types.”
4. Specify `b != 0` as well as `a+c != 0` when displaying the inverse of the braid change of variables.

None changes a claimed partial theorem or the disposition. No author-file patch is required for this scoped PASS; future revisions may incorporate the clarifications under a new manifest.

## What this audit does not establish

The packet still supplies neither a root factorization and admissible order for every reduced plabic graph, nor an invariant that excludes every sequence and order for one verified graph. It does not reconstruct the source classifications, independently audit every proof in the six papers, compare the unavailable imported raw statement, or prove no later solution exists. The cube-embedding matrix constructs no root sequence and proves no equality of value semigroups. Further finite successes cannot silently close those gaps.
