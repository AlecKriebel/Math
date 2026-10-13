# PR407 independent priority and status classification challenge

Frozen scope: open draft PR407, head `e3f8838a8eac68bbd186fc0234ac2e2a49194626`, problem 30003813 / OWR-16164-005, QUEUE status `claimed_solved`, one of five author attempts. This is an independent priority review, followed by a cross-check of the other priority family's new alcoved-polytope reference. No outside communication, Git writes, publication, or paper editing occurred.

**Recommendation: correct the literal target to `already_solved` on the basis of a checkable, earlier, full-covering theorem.** This is an inference from theorem coverage, not a claim that a publication explicitly declared the original OWR question closed. The candidate proof is sound within its stated literal scope. Its attribution is already appropriately cautious. The priority issue concerns promoting that scope as a newly resolved open problem.

## Exact target and competing interpretations

I read the entire Josuat-Vergès abstract in the official 2018 OWR report, printed pages 1408–1410, and visually checked PDF page 30. The final paragraph defines arbitrary weak signed adjacent-sum inequalities in the unit cube and asks for the combinatorics of their h-star polynomials. It does not explicitly require a statistic on the preceding cyclic-order objects. The candidate's ordinary-permutation interpretation answers this broad literal reading. The surrounding cyclic-order discussion can motivate a more specific refinement, but does not supply a formal restriction that can be imposed silently. Neither the source's old open-problem wording nor a bounded failure to locate a later explicit closure establishes that the target remains open today. [Official OWR report](https://publications.mfo.de/bitstream/handle/mfo/3645/OWR_2018_23.pdf?isAllowed=y&sequence=1).

The decisive priority comparison below uses exactly that same broad reading. A narrower cyclic-order-specific target is not proved solved or already solved by this audit; changing to it would require a separately defined problem and a different success test.

## Independently discovered descent-polytope route

Reflecting the even coordinates, on each dilation using `y_i=x_i` for odd i and `y_i=m-x_i` for even i, sends the complete signed family bijectively to arbitrary oriented-path order polytopes. The resulting descent set is `D={odd i with epsilon_i=+} union {even i with epsilon_i=-}`. This is a lattice bijection including boundary points and m=0.

Chebikin and Ehrenborg explicitly studied every descent polytope `DP_D` (all subsets D, every positive dimension), identified it as the order polytope of a ribbon poset in Section 2, and computed its Ehrhart polynomials in Section 4/Theorem 4.2. Their paper appeared in 2011, before the workshop. The corresponding arXiv v2 is dated 8 December 2010; its original arXiv identifier is from 2008. I checked the published paper through the web PDF reader and the complete downloaded v2; I visually checked its definition and theorem pages. [Published paper, DOI 10.1007/s00454-010-9316-6](https://doi.org/10.1007/s00454-010-9316-6), [primary arXiv v2](https://arxiv.org/pdf/0812.1249v2).

Stanley's natural-label P-partition formula already supplies the relative-descent interpretation after this identification. Coons–Sullivant Theorem 16 explicitly restates that general formula for every finite poset. Thus the candidate has no new h-star theorem beyond a short identification and specialization. This alone is strong classical-corollary evidence; it is not evidence that the signed identification was historically published or noticed by the original questioners. [Stanley 1986](https://math.mit.edu/~rstan/pubs/pubfiles/66.pdf), [Coons–Sullivant 2023, Theorem 16, page 8](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p44/pdf/).

## Decisive independent full-family prior coverage

After preserving that independent search, the parent supplied the other priority family's reference: Bullock and Jiang, *The Ehrhart series of alcoved polytopes*, arXiv 2412.02787v2, dated 22 April 2025. I independently read Definitions 2.1–2.4, the half-open-simplex argument, Corollary 4.6, Definitions 5.1 and Corollary 5.2, Lemma 5.3, and Theorem 5.4; the theorem page was visually checked. This is a prior arXiv preprint; a peer-reviewed journal publication has not been verified. Its theorem gives a finite dual-alcove-graph rule for the Ehrhart numerator. [Primary preprint](https://arxiv.org/pdf/2412.02787v2).

Here is an explicit verification of every hypothesis for this problem, independent of the candidate's reflection mechanism. Write `y_0=0` and `y_j=x_1+...+x_j`. The cumulative matrix is triangular with determinant one; its inverse is `x_j=y_j-y_{j-1}`. Consequently the original constraints become

- `0 <= y_j-y_{j-1} <= 1`, and
- `y_{i+1}-y_{i-1} <= 1` or `>= 1`, as specified by each sign.

For the root system A_n use `V={lambda in R^(n+1): sum lambda_j=0}` and roots `e_a-e_b`. Send y to `lambda_j=y_j-average(y_0,...,y_n)`. The relevant **coweight lattice** is

`Lambda^vee={lambda in V: lambda_a-lambda_b is an integer for every a,b}`.

This is distinct from the zero-sum integer **root lattice**. The map is a bijection from `Z^n` to `Lambda^vee`, with inverse `y_j=lambda_j-lambda_0`. Fractional individual lambda coordinates are therefore expected and cause no lattice-point loss. All inequalities are integer root-difference bounds. For each a<b, redundant bounds `-(b-a) <= (lambda,e_a-e_b) <= 0` follow from the unit-cube constraints. The signed length-two bounds replace one endpoint by -1. This gives precisely the required finite system of integer alcove halfspaces. The polytope is bounded and full dimensional: the reflected oriented path has a strictly order-preserving assignment with every coordinate strictly between zero and one.

Take simple roots `alpha_i=e_{i-1}-e_i`, i=1,...,n. Their sum is the highest root. Each coefficient in that highest root is one. In difference coordinates the fundamental coweight omega_i satisfies `y_j=0` for j<i and `y_j=-1` for j>=i. Thus all fundamental-alcove vertices have integral difference coordinates and denominator one in the correct lattice; all facet weights are one. They form a unimodular simplex, since their difference-coordinate matrix is triangular with diagonal -1. Weyl reflections preserve this lattice, and affine translations are integral in it, so every alcove has the same unimodularity.

It follows from the prior theorem that `h*_Q(z)` counts the alcoves of the transformed Q by the number of incoming edges in the breadth-first-search order of their finite dual graph, rooted at any chosen alcove. This is an explicit all-signs, all-dimensions combinatorial rule for the exact broad target. No conjecture or new h-star result is needed to apply it. The reduction uses only integer cumulative coordinates and the explicit lattice normalization above.

## Adversarial source and scope checks

Bullock–Jiang Lemma 3.2 omits, in its unrestricted wording, the gcd-one hypothesis present in the Theorem 3.1 base case. Taken for an arbitrary rational simplex, that wording is false: the integral interval [0,2] has numerator `1+z`, whereas using only its vertex denominators would predict numerator 1. I do **not** certify that unrestricted wording. Every A_n alcove here satisfies the missing hypothesis by the explicit determinant-one argument, so the specialization used above is unaffected. The proof reduces to disjoint half-open unimodular simplices and the shelling statement.

AJR2020 Theorem 2.5 gives signed-family integrality and volume; Theorem 2.9 concerns a different upper-bound family. Applying its cyclic descent statistic indiscriminately fails already for the two-dimensional greater-than triangle: its h-star is 1, while the corresponding reversed cyclic word has one descent. Coons–Sullivant's swap theorem covers the zig-zag specialization rather than arbitrary signed paths. Their general natural-label formula remains valid, with the prescribed relabeling. [AJR2020, Theorems 2.5 and 2.9](https://ahl.centre-mersenne.org/item/10.5802/ahl.33.pdf).

Beck–Hlavacek's similarly named signed-poset polytopes live in `[-1,1]^n`; the apparent map `u=2x-1` does not preserve the original lattice. I did not count that as direct prior coverage. The July 2026 adjacent-sum preprint found by search uses alternating upper bounds, not arbitrary choices of weak inequality direction; it was also excluded as a direct resolution.

## Reproduction and classification

The independently authored `independent_prior_controls.py` uses no candidate code. Normal Python execution, with assertions enabled, returned zero and empty stderr. It checks every sign family in dimensions 1–6: 63 families, 384 dilation evaluations matching the original adjacent-sum counts, reflected descent-polytope counts, and the actual noncommutative Ehrhart formula of Chebikin–Ehrenborg; 115 distinct dual-graph root choices produce exactly the original h-star coefficients. All 873 constructed alcoves have determinant of absolute value one. These are finite controls; the exact reductions and prior theorems supply the all-n conclusion. No optimized-mode certification is claimed.

The strongest defensible framing is: **an explicit attributed classical-corollary certificate for a literal target already covered by prior general theory**. This does not support novelty, firstness, a claim of newly settling a currently open problem, or a statement that a published historical notice closed the OWR question. Under the user's status definition I recommend `already_solved`, by verified full-family prior-theorem coverage. That recommendation is an editorial classification inference, explicitly broader than a requirement for a paper naming the OWR question. The source's 2018 open designation cannot override a checkable 2025 theorem covering that same literal scope.

One promotion blocker remains: the `claimed_solved`/open-problem disposition should be corrected if the root adopts this recommendation. There is no mathematical defect to repair in the candidate's stated formula, and no unresolved all-family gap in the prior-coverage reduction. The bounded literature search (31 queries) does not establish absence of an earlier signed identification or narrower cyclic-order result. Once status is corrected, the user's instruction requires skipping this PR entirely; this reviewer has not initiated any downstream action.
