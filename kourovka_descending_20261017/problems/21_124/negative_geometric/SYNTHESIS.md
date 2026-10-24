# Negative geometric family synthesis

UTC: 2026-10-24T22:38:18.412523+00:00. Family outcome: **unsolved**. No complete negative or affirmative answer to Kourovka21.124, no solved_verified label, no preprint, no DOI. Discovery estimate toward the original full target: **3%**. Substantial independent family research produced exact supporting results and actively falsified its strongest initial negative route.

## Strongest conclusions and proof inputs

1. FINITE_HOLONOMY_FILTER.md: for the genuine CAT(0) groups G_k with a fixed, b→ba^k, c→caba^-1b^-1, k>2, every homomorphism into R^n⋊Q with finite Q and trivial linear action of a kills a. Strict convexity proves this in every finite dimension. Induced characters give rational homology invisibility in normal finite-index subgroups containing a, and non-RFRS of G_k itself. **Virtual RFRS is not excluded.**
2. NONNORMAL_COVER_DELTA.md: an exact four-sheet nonnormal cover of G_4 retracts onto<a>, directly falsifying arbitrary finite-index extensions of that obstruction. A separate six-sheet action detects a in G_3.
3. ALL_K_RETRACTION_DELTA.md: a uniform explicit integral affine representation detects a^k for every k≥2 and yields a literal virtual retraction onto<a>. Together with the k=1 witness, this holds for every positive k. This closes the a-specific negative VRC route for the whole family.
4. FLAT_RETRACTION_DELTA.md: the same representation gives virtual retractions onto the natural Z² subgroups<a,t> and<[a,b],t> for k≥2. It does not inject the nonabelian fixed free group. Its affine image there is metabelian; commuting linear parts do not imply commuting affine maps.
5. SECONDARY_MECHANISMS.md: quadratic rank-two fiber distortion obstructs direct embedding but loses its rank hypothesis in arbitrary finite-index intersections. A residual-finiteness negative example is excluded, even with infinite-rank free kernel, by Linton's primary embedding theorem and an elementary characteristic-cover argument. Fixed-centralizer commutator twists cannot evade the genuine CAT(0) hypothesis.

## Reproducible exact evidence

- check_covers.py: exact rational cellular boundary computations, k=1/2 cocycles, and four8-/27-sheet nonabelian UT4 actions.
- search_small_covers.py and search_degree6_covers.py: bounded permutation searches, explicitly stopping at the first visibility witness; never infer a universal obstruction from absence in a finite range.
- check_nonnormal_witness.py:12 lifted relators evaluate to0 and the a-loop evaluates to1 in the explicit G_4 four-cover, hence a literal virtual retraction.
- check_uniform_retraction.py:39 exact integer affine tests for k=2,...,40, plus135 lifted-relator evaluations and exact rational homology checks for the9-/15-/21-sheet covers at k=3,5,7. The uniform proof handles all k; tests are supporting reproduction.

## Adversarial review and priority

Root appointed fresh nonauthor p21124_holonomy_adversary, writing sibling negative_review/. That reviewer has reported theoretical agreement with the frozen strict-convexity, normal/core and abelian-projection scope and has independently reproduced the boundary cases. The all-k construction and flat-retraction delta were separately supplied for audit. Read that review's final receipt, exact hashes, and objections before promoting any partial claim; author does not substitute this summary for its final acceptance.

Primary source metadata are in SOURCE_MANIFEST.json, referencing authenticated existing program caches. Delage's CAT(0) construction is prior mathematics. Wu–Ye already provide other CAT(0) non-RFRS examples. No exhaustive priority audit or first-discovery claim was made for these partial deductions. None settles the original problem, so publication as a solved Kourovka problem is disallowed.

## Precise remaining obstruction

The negative strategy needs an invariant surviving every finite-index subgroup and genuinely arbitrary finite holonomy, or a different explicitly geometric CAT(0) free-by-Z family. For this family, the virtual retractions of<a> and the two natural flats are positive evidence defeating those proposed obstructions. No RAAG injection of a finite-index subgroup has been obtained; no failure of one has been proved. A character on a higher derived word of the fixed free subgroup, or a materially new obstruction, remains unconstructed. Reopening any blocked route requires new evidence beyond the same trivial-holonomy restriction or bounded negative search.
