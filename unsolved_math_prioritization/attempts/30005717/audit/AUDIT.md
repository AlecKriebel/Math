# Independent audit: 30005717

## Verdict

**PASS — partial research only.** Accept the frozen packet as an explicitly unsolved, five-approach research and reproduction record. This is **not** acceptance of a proof or disproof of the unrestricted conjecture, a novelty claim, or an exhaustive literature review. No mathematical error affecting the target-class results was found. One minor source-summary qualification is recommended below.

Audit date: 2026-10-03. The six frozen public files were checked before and after computation and were not changed. The author script was rerun in a separate copy. Its regenerated JSON agrees exactly with the frozen `exact_results.json`, including the reported SymPy version 1.14.0. An independently written original-coordinate solver reproduced all twelve cases.

## 1. Question, sources, and scope

The authoritative problem is Conjecture 2 in the official [OWR report, printed p. 3303](https://ems.press/content/serial-article-files/48169). Specializing its parameters to d = 2k gives the stated prohibition of missing faces of dimension at least k+1. The object supplied is the stress subspace in the polynomial ring on vertex labels. An abstract dimension alone would not carry the necessary affine information. The neighboring skeleton reconstruction statement is a different conjecture.

The key primary-source distinctions are correct:

- [Murai–Novik–Zheng, arXiv:2306.09816v2](https://arxiv.org/abs/2306.09816v2): Theorem 2.1 supplies the canonical-Lefschetz dimension statement for natural polytopal embeddings, not merely generic embeddings. Theorem 3.1 stops below the even middle degree. Proposition 3.2 has an equality below the endpoint and only an inequality at the endpoint. Remark 3.6 already announces failure of the stronger generation claim in even dimensions at least six.
- [Novik–Zheng, affine partition of unity](https://sites.math.washington.edu/~novik/publications/affine-equivalence-final.pdf): Theorem 6.3 assumes missing-face dimension at most d−2i+1 for natural polytopes. With d = 2i, this is the flag condition. It does not cover the full question here.
- [Novik–Zheng, April 23, 2026 author PDF](https://sites.math.washington.edu/~novik/publications/lower%20bound%20on%20g.pdf): Section 6 supplies the credited join family, failure of levelness/full lower-degree generation, and a natural-coordinate support obstruction. The natural four-dimensional case is explicitly left open. Those auxiliary failures do not assert that the top stress space loses degree-one information.
- [Novik–Zheng, arXiv:2601.10072v1](https://arxiv.org/abs/2601.10072v1): the checked abstract/introduction concern combinatorial classifications with g_k = 1. They do not give the claimed unrestricted determination of natural affine coordinates.

All five source-PDF hashes listed in the frozen source manifest match the inspected local source bytes. Live primary-source checks confirmed the OWR report, arXiv version metadata, the 2026 author PDF, and the author's publication list. Focused searches did not identify a later solution; that is a bounded negative finding. No repository-history search or exhaustive traversal of unpublished work was performed as part of this audit.

### Minor qualification C1

`RESEARCH.md`, §0, item 1 abbreviates Theorem 1.5 as edge participation for “prime simplicial polytopes.” In the cited paper's terminology, a simplex is prime, and §5 explicitly adds “not a simplex.” A simplex has no nonzero affine 2-stress. Recommended wording: **“non-simplex prime simplicial polytopes”**, or the theorem's precise condition **“no missing faces of dimension at least d−1.”** This is non-blocking for the packet's mathematical target: its missing-face restriction already excludes the simplex. The frozen source was not edited.

## 2. Exact reconstruction criterion

The inverse-system model and differential pairing are valid over the stated characteristic-zero field. The equality S_i ≅ B_i* is used as duality of embedded spaces; it does not replace the input by an abstract dimension.

For V = S_k, a linear form annihilates the span of the order-(k−1) derivatives precisely when it annihilates every member of V. The remaining homogeneous polynomial has degree k−1, so all its derivatives of that order vanish only if it is zero. Consequently W(V)⊥ = L(V), while S_1⊥ is the augmented coordinate row space J_1.

Sufficiency is correct: if W(V) = S_1(P) and Q has the same V on the same labels, W(V) lies in S_1(Q). Full dimension gives the same nullity n−d−1, hence equality of augmented row spaces. The last all-ones row makes the resulting change of coordinates affine, and invertibility follows from full dimension.

The necessity argument also survives the following adversarial checks:

1. Choosing a ∈ L(V) outside J_1 and replacing one coordinate row r by r+ta preserves every old stress equation; support remains valid once the face lattice is retained.
2. A sufficiently small perturbation of the vertices of a simplicial polytope preserves its facet inequalities. Each original facet remains a strict supporting simplex. Every ridge still has its two original incident facets, so there can be no edge of the new facet-adjacency graph from an original facet to an additional facet. The dual graph of any full-dimensional convex polytope is connected. Thus no new facets occur. This argument does not assume general position of all vertex subsets.
3. Fixed combinatorics alone would not justify equality of stress dimensions for arbitrary frameworks. Here the input is a natural polytope throughout, so MNZ Theorem 2.1 gives dim S_k = g_k for every small perturbation. The inclusion of stress spaces is therefore equality. Translation to keep an interior origin changes the coordinate ideal only by multiples of the all-ones form.
4. Modulo the span U of the other coordinate rows and the all-ones row, the classes of r and a are independent. The lines spanned by r+ta are distinct. Thus the augmented row spaces genuinely vary.
5. Unlabeled affine equivalence is not silently substituted for labeled equivalence. There are only finitely many coordinate permutations of the original row space, and each can meet this injective one-parameter row-space family at most once. Avoiding these finitely many parameters proves the required unlabeled conclusion.

Finally, a(∂)V = 0 is equivalent, under the perfect degree-k pairing, to aR_(k−1) ⊆ J_k. Passing to B gives exactly the stated first-factor annihilator condition. This is weaker than the absence of every lower-degree socle component. No missing-face assumption was smuggled into the linear-algebra equivalence; it is used only in the unresolved universal assertion.

The neighborly special case is correct, including the vacuous zero-dependency case: absence of Stanley–Reisner relations in degrees at most k leaves Sym^k(S_1), and powers of linear stresses recover their linear factors by repeated directional differentiation.

## 3. Three-triangle example and support obstruction

The specified triangles contain the origin in their relative interiors. Their free sum in complementary planes is a genuine simplicial six-polytope whose boundary is the join of three triangle boundaries. The independent supporting-facet certificate confirms this natural realization, without appealing to genericity.

The coordinate quotient identifies the three vertex variables in each block. Eliminating the affine equation gives

B = R[u,v]/(u³,v³,(u+v)³).

In degree three, use u²v as basis and uv² = −u²v. Multiplying a quadratic A u²+B uv+C v² by u and v gives coefficients B−C and A−B. The common kernel is exactly A=B=C, proving the stated nonzero one-dimensional quadratic socle. The linear-factor multiplication map has coefficient matrix with rows (0,1), (1,−1), (−1,0); it has rank two. This independently confirms that the quadratic socle defect does not lose degree-one information.

The inverse cubic X²Y−XY² is annihilated by the three cubic generators. Its first derivatives span dimension two; its second derivatives span both linear directions. The natural-coordinate polynomial (s_1−s_3)(s_2−s_3)(s_1−s_2) was directly checked against all seven augmented-coordinate differential equations and against the independently computed one-dimensional cubic-stress kernel. Exactly 27 of the 81 triangular faces have zero coefficient, namely the triples with one vertex in each block. These facts agree with the credited 2026 family; no new counterexample to the original reconstruction question results.

For the four-dimensional discussion, the sum-of-images/intersection-of-kernels formulation is correct. Edgewise participation alone does not establish that the common kernel has dimension five.

## 4. Suspension calculation

For the symmetric bipyramid, the apex coordinate and nonface relations are a−b and ab. Hence the linear-stress quotient is A[t]/(t²), and adding the affine relation gives A/(ell²). The original affine quotient is A/(ell), so the proposed lift lacks a layer of information.

At degree k, injectivity of ell² follows by composing the canonical Lefschetz injections in degrees k−2 and k−1. Thus the extra dimension is exactly g_(k−1), as claimed. The cross-polytope control independently returns degree-two stress dimensions two and five before and after suspension. This is a valid diagnosis of a gap in the direct lifting argument; it is not an impossibility theorem for every possible lifting strategy.

## 5. Computation and reproducibility

The author algorithm is mathematically appropriate: it exhausts supporting facets in exact arithmetic, constructs all faces, imposes nonface-support constraints on a full Gale-coordinate symmetric-power parametrization, and rechecks the resulting differential equations. Its missing-face threshold has the correct strict inequality. The derivative ranks in Gale coordinates equal those in vertex coordinates because the Gale linear map has full row rank.

The independent checker does not import or invoke any author function. It:

- constructs combinatorial facet candidates for the listed cross, cyclic, polygon-join, and stacked realizations;
- verifies exact strict supporting inequalities using cofactor normals, all vertex incidences, two facets per ridge, and connectivity;
- enumerates minimal nonfaces and checks the frozen missing-face lists;
- solves all affine differential equations on the original-coordinate face-supported monomial basis, using rational linear algebra;
- computes derivatives by coefficient/falling-factorial formulas in the original variables;
- matches every top-stress dimension and both derivative-span ranks in all twelve cases.

All ten target realizations recover n−d−1 linear dependencies. The odd-dimensional cross-polytope remains a separate positive control. The stacked four-polytope is a separate excluded negative control; its missing tetrahedron prevents its use as a target counterexample.

An additional negative-control test perturbs the first coordinate of the stacked vertex from 3/10 to 31/100. The same eight facets remain, and both top-stress spaces are zero. The union of augmented row spaces has rank six instead of five. The normalized absolute multisets of the unique affine dependencies differ, excluding every vertex permutation and scalar. Thus the test verifies a genuinely unlabeled affine change with fixed combinatorics and fixed top stresses, in a class explicitly outside the conjecture.

### Portable artifacts

- `check_independent.py`: independent verifier, Python 3 + SymPy 1.14.0; no network, source PDFs, or private inputs.
- `independent_results.json`: all independent check results and the six audited public hashes.
- `independent_run.log`: successful final execution output.
- `audit_status.json`: machine-readable verdict, source-hash checks, rerun agreement, and C1.
- `author_rerun/`: separate author-script copy, regenerated JSON, and execution log. The frozen public output was never overwritten.

Run `python check_independent.py PATH_TO_PUBLIC_DIRECTORY`. With the original directory layout, omitting the argument uses the sibling `public` directory. The checker pins the audited six-file revision and writes only its own result beside the checker. If editorial corrections alter public bytes, a later audit must explicitly update the pin; a hash failure is intentional.

## 6. Acceptance boundary

The five attempts are substantive but do not establish the universal condition that B_1 has zero annihilator against B_(k−1) for every permitted natural realization. The tests are exact finite certificates, not sampling-based evidence promoted to a theorem. Attribution and the explicit absence of historical novelty are appropriate. Preserve the **unsolved, 5/5 substantive approaches** disposition. This review is AI-assisted mathematical checking, not human peer review or proof-assistant certification.
