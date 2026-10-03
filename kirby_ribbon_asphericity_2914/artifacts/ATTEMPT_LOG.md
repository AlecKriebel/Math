# Five substantive approaches: 2914 / KP-4.38

The target throughout is the unrestricted ribbon-disk asphericity question. All five approaches below were completed in this investigation on 2026-10-03. “Unresolved” is a statement about the result obtained, not a claim that a theorem of impossibility has been proved. Details and proofs are in PROOF.md.

## Attempt 1 — ordinary cellular homology

**Proposed route.** Exploit the ribbon disk's tree presentation to force vanishing higher homotopy.

**Work.** Derived the ordinary 2-boundary, proved every root-deleted incidence minor unimodular by leaf induction, and calculated the homology of the LOT complex in all degrees.

**Established.** Every LOT complex has the homology of a circle.

**Why it does not finish.** The complex is not simply connected, so this calculation does not compute its second homotopy group. The missing object is the universal cover's second homology. Continued with a contractible enlargement.

## Attempt 2 — a contractible enlargement

**Proposed route.** Attach a meridional 2-cell and inherit the resulting contractibility.

**Work.** Showed one killed vertex generator kills all others along the tree. Computed the enlarged square boundary matrix and established acyclicity and then contractibility of the enlarged complex.

**Established.** Every LOT complex embeds as a subcomplex of a finite contractible 2-complex.

**Why it does not finish.** Passing asphericity to this subcomplex is the Whitehead-type assertion at issue. Fundamental-group injectivity is unavailable. Continued with a specific intermediate cover that can be calculated directly.

## Attempt 3 — Fox calculus in the infinite cyclic cover

**Proposed route.** Lift the boundary calculation to Laurent polynomials rather than ordinary integers.

**Work.** Derived the full Fox matrix, including coincident endpoint-label cases. Proved its root-deleted determinant has value ±1 at t=1, and used integral-domain injectivity to compute H2 of the infinite cyclic cover.

**Established.** The infinite cyclic cover of every LOT complex has H2=0. If the entire fundamental group is Z, the LOT complex is aspherical.

**Why it does not finish.** The infinite cyclic cover is not generally the universal cover. Injectivity after abelianizing coefficients does not lift to injectivity over the group ring. Continued with combinatorial asphericity tests that do not rely on abelianization.

## Attempt 4 — reductions and the forest criterion

**Proposed route.** Extend the injective-LOT argument by reductions and generator inversions, hoping to make both signed link graphs forests.

**Work.** Checked the hypotheses of the established injective theorem. Constructed the five-vertex path with labels c,e,a,c; proved it reduced, noninjective and without a proper nontrivial sub-LOT. Examined all effective label reversals and all 32 generator-inversion subsets directly from signed relators. Tested all 16 independent edge reorientations separately.

**Established.** No generator-inversion subset passes the two-forest test. Only two independent edge reorientation patterns pass, both reversing the two c-labeled edges inconsistently with generator inversion. The eight-case cycle certificate is included in the proof.

**Why it does not finish.** Failure of a sufficient criterion is not failure of asphericity. This disproves one proposed universal tactic, not the ribbon-disk conjecture or every possible transformation of this example. Continued with the universal cellular boundary itself.

## Attempt 5 — augmentation completion of the universal boundary

**Proposed route.** Recover universal injectivity by inverting the augmented Fox matrix in a group-ring completion.

**Work.** Derived the actual group-ring Fox matrix and identified pi2 with its kernel. Normalized a root-deleted minor by its integral inverse. Proved every possible kernel vector has coordinates in every augmentation-ideal power. Tested the missing separation hypothesis using the lower central series of a group with cyclic abelianization.

**Established.** Every possible 2-cycle lies in the augmentation-adic intersection. For any nonabelian LOT group that intersection is nonzero: the lower central series stabilizes at the commutator subgroup, and any nontrivial commutator gives a nonzero element g−1 in every ideal power.

**Why it does not finish.** The completion does not embed the original group ring in the nonabelian case. The nonzero intersection does not itself produce a vector annihilated by the Fox matrix. The exact surviving task is to show that this matrix has no nonzero kernel for every LOT, or to exhibit a specific LOT and a nonzero kernel vector.

## Final disposition

Five substantive approaches completed. No unrestricted resolution. The partial propositions and failed-tactic certificate have exact proofs; their finite regression checks pass. The 2026 literature check retains the explicit distinction between known conditional results and the general question.
