# Independent audit of KP-4.104 / 2980

## Verdict

**Accept the mathematical partial result, with one minimal source-completeness correction in Section 4. The target remains unresolved after five substantive approaches.** No counterexample, impossibility theorem, or infinite family in one smooth isotopy class has been established. No mathematical checker correction is needed.

The independent audit read the complete seven-file public packet, compared its archive against the directory byte for byte, inspected the primary passages behind every main imported result, reconstructed the algebra independently, and ran genuine UID/EUID 1000 read-only tests and meaningful mutations in normal, `-O`, and `-OO` modes.

The correction credits an existing Lagrangian-to-symplectic perturbation and complex-realization route. It sharpens the remaining obstacle to control of the required boundary convention and, principally, survival of a non-isotopy invariant. It does not alter the valid Stokes obstruction for a boundary that remains Legendrian.

### Frozen inputs

- Original source-free archive: 17,306 bytes; SHA256 `5a15ce6890e0bfd750f3f67e18043a33200fabd4e3dd8b5ed963ce19691f9881`.
- Original `REPORT.md`: 25,467 bytes; SHA256 `b05408b043af27f7ad7ca28e737bfd3f92a47a37badceaaad7b1a3d3662fe7b5`.
- Original `verify_exact.py`: SHA256 `208b1f8a05fbfc03c5efb5fc8aa64ab626eb1f1911bf7737e0bfe160371efc1b`.
- Original expected output: SHA256 `9ed8e2898b651ea06f20a3e7c4eb2742bda3ba8d955ae7f7b23fa22e546054ca`.

All seven ZIP members match the original public directory exactly. Every entry in its frozen manifest matches the listed size and SHA256. The original archive, report, other public files, and original source files were not modified.

## 1. Target identity and boundary conventions

The April 2026 author-hosted K3 PDF, printed pages 277–278, contains the relevant question. Its target is a pair of complex curves in the standard four-ball that are smoothly isotopic but not complex-isotopic, the stronger symplectic separation question, and the infinite-family question. The report retains all three clauses and the requirement of embedded nonsingular surfaces. This is not the different Problem 4.104 in the older Kirby collection. [K3](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf)

The source does not specify pointwise boundary, analytic collar germs, parametrizations, or labels. Its discussion of differing braid representatives and stabilization supports the report's explicitly declared unmarked transverse-link-type convention. That convention should remain visible: a transverse boundary isotopy is not a proof that a particular analytic boundary point set or collar can be fixed throughout a complex deformation.

The report correctly separates the following settings:

1. The target: one transverse boundary type, without an added marking.
2. Lemma 1.1: an already symplectic path, stationary on a whole boundary collar.
3. Capping: a distinguished generic projective line, with the labeling/incidence conventions of the imported configuration theorem.

No unproved identification of these three equivalence relations is used to claim a solution. For properly embedded surfaces, a smooth isotopy extends to an ambient isotopy with the corresponding boundary behavior; the branched-cover obstruction therefore applies to the target's smooth-equivalence hypothesis.

## 2. Mathematical review of all five approaches

### 2.1 Symplectic isotopy extension and the global gap

Lemma 1.1 is valid as a statement about images of compact symplectic surfaces, not about preserving a chosen parametrization. Symplecticity gives the direct-sum splitting of ambient tangent vectors into tangential and symplectic-normal parts. The covector `-i_N omega` annihilates the tangent bundle of the surface, so it is the compatible differential of a first jet with function value zero on the surface. A tubular extension and cutoff give the Hamiltonian. Its vector field agrees with the prescribed normal velocity; the remaining tangential velocity is absorbed by a time-dependent reparametrization. Stationarity on a collar makes the normal field vanish there and permits support away from the boundary collar. Compactness supplies a uniform neighborhood and finite-time flow.

This would not establish extension of an arbitrary parametrized symplectic embedding path without reparametrization, and it says nothing about an arbitrary smooth path staying symplectic. The report makes the appropriate image-level statement and identifies this global gap.

The affine-form counterexample is correct. With the coefficients in the report, independent exterior-algebra expansion gives

`omega_t wedge omega_t = (2 - 8t + 8t^2) dx1 wedge dx2 wedge dx3 wedge dx4`.

Both endpoints have the same positive square and restrict positively to the distinguished plane. All coefficients are constant in space, so the forms are closed and exact; for example, primitives can be obtained by replacing each `dx_i wedge dx_j` term with `x_i dx_j`. At `t=1/2` the form factors as

`(dx1 + dx4) wedge (dx2 + dx3)`.

It has rank two, with kernel spanned by `(1,0,0,-1)` and `(0,1,-1,0)`. Thus this is an exact degeneracy, not floating-point evidence. As the report says, it refutes automatic straight-line interpolation, not every possible connecting path.

### 2.2 Orevkov pair: raw Hurwitz distinction does not survive conjugation

The corrected 2019 v3 of Orevkov's paper is the proper source. It includes both the finite-orbit statement for a fixed three-braid and the exponent-two example used here, with a correction notice concerning the published version. The report correctly treats the orbit distinction as an imported theorem and does not infer it from a finite orbit search. [Orevkov v3](https://arxiv.org/abs/1409.4726v3)

The displayed factorizations are indeed those obtained by deleting positions `{1,5}` and `{3,7}` in `a^2 b^2 a^2 b^2`. Their products agree with the reported braid. The second deleted-word conjugator simplifies because `a^2 b a^2 = z b^-1`, and `z` is central.

The simultaneous conjugation is exact. For `g = a b^-1 a^-1`, the braid relation gives

- `g a g^-1 = a^2 b a^-2`;
- `g (a b^2) = a b`;
- `(a b) a (a b)^-1 = b`.

These three identities prove conjugacy factor by factor, and equality of the products then proves that `g` centralizes that product. The calculation removes the proposed obstruction even though the two factorizations occupy different raw Hurwitz orbits. It does not prove complex isotopy, and the report correctly refrains from claiming a complete geometric equivalence theorem.

A second independent check used integer `SL2(Z)` matrices and exponent sum, rather than the original free-group-automorphism implementation. It produced common matrix `[[-5,4],[-4,3]]`, exponent `2`, and conjugator matrix `[[2,-1],[1,0]]`. The two vanishing-cycle columns are exactly those stated in the report. These matrix calculations are corroboration; the direct braid-relation derivation above already proves the identities without requiring faithfulness of this numerical representation.

The braid-index-two exclusion and the limitation of fixed-three-braid finiteness are stated correctly. In particular, the latter is not promoted to a finiteness theorem for all stabilized representatives of a transverse link.

### 2.3 Branched covers and the infinite annulus family

The canonical double branched cover is preserved by an ambient isotopy: meridians retain their mod-two character, the induced complement cover is transported, and the map extends over the normal-disk branch model. Thus differing first homology of the covers obstructs smooth isotopy, even when no collar marking is retained.

BVHM Theorem 10 gives the relations encoded in the report's matrix. Its odd parameters produce connected annuli; its even parameters produce a disconnected surface. Those are not interchangeable subfamilies. [BVHM](https://arxiv.org/abs/1604.02945)

The integral presentation reduction is valid for every integer `n`. A universal unimodular reduction, independently implemented over `Z[n]`, is:

1. Subtract row 2 from row 1.
2. Add the new row 1 to row 3, then subtract row 2 from row 3.
3. Subtract row 2 from row 4.
4. Subtract twice column 1 from column 2.
5. Swap rows 3 and 4; swap columns 2 and 3; negate row 3.

The result is the rectangular diagonal matrix with entries `1,1,n` and a zero fourth row. Hence the group is `Z/n` for nonzero `n`, and `Z` at zero. For distinct positive odd parameters the group orders differ, excluding smooth isotopy. The original 201 determinantal-divisor calculations are consistent with this universal argument; they are not its logical basis.

Equal absolute parameters, equal Euler characteristic, or equality of a selected cover invariant would only remove a particular obstruction. The report correctly declines to infer a smooth isotopy from such equality.

### 2.4 Lagrangian conversion: valid obstruction, missing existing tool

The fixed-Legendrian-boundary Stokes lemma is correct and does not need exactness of the original Lagrangian. The restriction of the Liouville form to a Legendrian tangent line is zero, while a nonempty surface oriented by the ambient symplectic form has positive total area. These statements contradict Stokes if the whole boundary is kept Legendrian. The cotangent-graph calculation and the need for a nonzero boundary integral are also correct.

There is, however, an omitted primary source that changes how the remaining work should be described. Cao–Gallup–Hayden–Sabloff, Lemma 4.1, supplies the moved-boundary symplectic perturbation; §4.2 gives the quasipositive-to-complex realization route. Small perturbations and the stated smooth realization isotopies preserve the underlying unmarked smooth embedding class. These existence results do not preserve the Casals–Gao Hamiltonian distinction. [CGHS](https://arxiv.org/abs/1307.7998)

The separate minimal patch adds this credit and narrows the gap. It does not claim a canonical conversion on Hamiltonian-isotopy classes, arbitrary fixed analytic boundary control, or a new non-isotopy invariant. A common strong collar permits consistent local pushoff choices, while any further boundary marking needs its own verification.

Casals–Gao Corollary 1.5 and the accompanying text do include infinitely many smoothly isotopic, Hamiltonian-inequivalent exact Lagrangian fillings of the maximal-tb `(4,4)` link. The report's conditional degree-four capping test is therefore useful: a proposed conversion into that standard unmarked capped class cannot carry a distinction that remains invariant under symplectic isotopy. It does not follow that two Lagrangian Hamiltonian classes remain distinct after conversion. [Casals–Gao](https://arxiv.org/abs/2001.01334)

### 2.5 Capping, adjunction, and fixed-ball deformation

GS Proposition 5.1 is explicitly a theorem about labeled configurations. The paper also explains why a general unlabeled version would be false. The report has preserved that caveat and restricts its use to a nonsingular curve plus a generic transverse line; there are no pre-existing singular-incidence choices in this application. Forgetting labels after proving uniqueness in the allowed labeled setting cannot create additional isotopy classes. No conclusion is drawn for a line constrained through arbitrary selected singular points. [Golla–Starkston](https://arxiv.org/abs/1907.06787)

The standard capping correspondence is expressly imported from the K3 discussion rather than derived from an arbitrary closed isotopy fixing a chosen cap pointwise. ST Theorem C proves the required closed statement in degree at most 17. Together with connectedness of the smooth algebraic parameter space, this yields the report's uniqueness conclusion in the standard capped setting. It does not give a complex path in a fixed affine ball. [Siebert–Tian](https://annals.math.princeton.edu/2005/161-2/p09)

The adjunction calculation is correct: a compatible almost complex structure preserving the embedded symplectic tangent bundle yields `3d = chi(C) + d^2`. Removing `d` disks gives `chi(S) = 2d - d^2`. All displayed genus values check. Adding an ordinary interior handle while keeping the same cap and degree changes the Euler characteristic by minus two and violates adjunction if the result were symplectic. No stronger obstruction to changing the boundary or degree is claimed.

Finally, the family of affine complex lines `w=c` is an exact illustration of the boundary-transversality issue. Smoothness of the complex curve persists across `|c|=1`, while its intersection with the unit ball changes from a disk to a tangency point to empty. The wall is a real hypersurface in parameter space. Thus avoiding the complex discriminant alone is insufficient to maintain a filling's boundary type. This is a gap demonstration, not a target example.

## 3. Primary-source and current-status checks

The original nine PDF hashes and byte counts match their public metadata. The target pages were independently rendered and visually inspected. The relevant passages in BVHM, Orevkov, GS, ST, CG, and Hayden were read; public arXiv or publisher records were freshly checked, including version dates. The Golla 2025 notes remain background material, not a claimed solution. The separately retrieved CGHS source is pinned in `ADDITIONAL_SOURCE_METADATA.json`; no source document or extracted text is included in this audit packet.

Hayden's result concerns the topological-versus-smooth distinction, not the desired smooth-versus-complex or symplectic distinction. Its current arXiv record remains v2 dated 2021-03-23. The report's exclusion of it as a direct answer is justified. [Hayden](https://arxiv.org/abs/2003.13681)

A fresh bounded search on the exact contrasts, four-ball setting, and 2025/2026 found no verified complete solution. It did uncover the CGHS conversion reference. This negative search does not establish that no solution exists. The report's status should remain **UNRESOLVED_PARTIAL**, with no claim of novelty or exhaustive literature coverage.

## 4. Reproducibility and optimization-resilient adversarial tests

`independent_exact.py` uses only the Python standard library and does not read the original checker, source PDFs, or any private corpus. It independently checks matrix braid identities, the symbolic universal relation-matrix reduction, the full exterior square, the midpoint rank-two factorization, and polynomial adjunction/Euler relations. It writes only to stdout.

`run_readonly_audit.py ORIGINAL_PUBLIC_DIRECTORY` exercises both checkers and ten meaningful mutation families. The process itself and every subprocess require real and effective UID 1000; root is rejected. Every test copy has mode `0444` in a directory of mode `0555`. Before executing the checker, each subprocess actually tries to create a file in that directory and append to the script. Both attempts must fail with a permission error. A before/after directory snapshot verifies that nothing was written. These are filesystem-enforced read-only runs, rather than permissions recorded without a denial probe.

Results:

- Two baseline checkers times three optimization modes: **6 successful runs**.
- Six original-checker mutation families times three modes: **18 intended failures**.
- Four independent-checker mutation families times three modes: **12 intended failures**.
- The harness itself was repeated under normal, `-O`, and `-OO`; all three result JSON files were byte-identical.
- AST inspection found no `assert` statements in either checker or the harness. Validation uses explicit exceptions and remains active under optimization.
- The original output matched the frozen expected JSON byte for byte in every mode.
- All original public files remained byte-identical after the full audit.

The original-checker mutations corrupt an inverse action, the second braid product, the simultaneous conjugator, the homology parameter, a symplectic-form coefficient, and the genus. The independent mutations corrupt the conjugator, a universal row operation, a form coefficient, and the Chern/adjunction polynomial. Every mutation fails at the intended mathematical check, prints no successful JSON payload, and is rejected in all three optimization modes.

The 36 tests per harness invocation are recorded in `READONLY_RUNS.json` (SHA256 `e1467db134598f02b10f5e3fc4fdc8f925cc148ff98efbad93076938314f889c`). Repeating the harness in its three modes executed 108 subprocess tests in total. These tests verify arithmetic and validation behavior; none decides an isotopy problem or replaces a geometric proof.

## 5. Minimal correction and acceptance boundary

`SOURCE_COMPLETENESS.patch` changes only the Section 4 discussion, its exact-gap paragraph, and the addition of one bibliographic entry. It was dry-run checked and applied to a copy; the result is byte-identical to `REPORT.corrected.md`. The frozen original has not been patched in place.

- Corrected report: 26,685 bytes; SHA256 `1372f3c3de364d04472a17c67085324041ee6f7dbfc30e1fd2c1abbcd98910a0`.
- Exact patch: 5,556 bytes; SHA256 `ba36649ad1875f9ee1305274f4899e90410bbd3f8ddadc9667e861e7dafe4c9d`.

The acceptance remains limited to the authored partial results and their stated obstructions. A solution still needs actual complex fillings in one smooth class, exact boundary conventions, and a separating invariant valid in the requested category; infinitely many examples require this pairwise throughout a single smooth class. Nothing in the correction removes the principal invariant-survival gap. There are still five substantive approaches; auditing, source recovery, and the correction count as no additional attempt.

No publication, repository push, PR action, or global queue edit was performed by this audit. Only authored analysis, exact checker code, verification metadata, the minimal patch, and the corrected authored report belong to the source-free deliverable.
