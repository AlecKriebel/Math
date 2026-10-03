# Independent adversarial review: problem 30004865

Date: 2026-10-03 UTC  
Reviewer: independent audit worker, uninvolved in authoring the five frozen turns  
Repository / checkpoint supplied: AlecKriebel/Math, `dot/math-30004865`, `3cdf054fcc4534408bc2c906e8b81166b47a59d9`  
Frozen input: `attempt/TURN_5_MANIFEST.json`  
Input manifest SHA-256: `8016d13bc34c45147548324d9b70b2a598340a3ffe50cef0eff446a1f9f0c98b`

## 1. Verdict

**PASS for the stated mathematical results, with the scope/presentation corrections in section 9.** No blocking mathematical error or missing essential proof step was found in TURN_1 through TURN_5. In particular, TURN_1 supplies a complete negative answer to the central, unreshuffled, all-local-tester completeness question. It is not merely a failure example for the two fixed testers.

**The entire OWR research agenda remains exhausted/scoped partial, with 5/5 author turns consumed.** The audit does not solve unrestricted mixed-state detection classification, a broader quantitative comparison, or the output-dimension/computational-efficiency question. It neither certifies novelty nor authorizes publication. The parent still owns the publication gate.

The unavailable historical favorable review was not used as evidence. All five proofs were inspected anew. The source statement was checked directly against the locally hash-bound OWR contribution, printed pp. 2696–2698, and Jivulescu–Lancien–Nechita (JLN), arXiv:2010.06365v1, Definition 3.1, Corollary 3.3 and Section 13, p. 35. The present verdict is independent of earlier state labels saying “reviewed.”

All 40 files bound by the final author manifest match their recorded sizes and hashes. All nine source files bound by the source manifests also match. This is a verification of the local frozen packet; the supplied checkpoint receipt identifies its remote WIP, but this review did not independently inspect the current remote branch tip.

## 2. Exact defensible claim scope

The following statements are supported by complete proofs in the frozen packet.

1. For every d ≥ 3 and f ∈ [2/d − 1, 0), the Werner state

   ρ_f = [(d−f)I + (df−1)F] / [d(d²−1)]

   is entangled, and the supremum of ‖(E ⊗ G)(ρ_f)‖π over all complex-linear contractions E:S₁ᵈ→H_A and G:S₁ᵈ→H_B is exactly 1. The output Hilbert spaces may have arbitrary, unequal finite dimensions. The specific full-rank two-qutrit example is (19I−9F)/144. The upper bound also holds for the larger real-linear-on-Hermitian class satisfying the stated pure-projector bound.
2. Appending arbitrary local density matrices preserves the counterexample to full-separability detection; embedding its two qutrit factors into larger local spaces also preserves it. These are not claimed to be genuinely multipartite entangled, and they do not cover every choice of local dimensions.
3. For every m ≥ 3, the fixed full-projective-norm realignment and qubit SIC criteria are incomparable on mixed m-qubit states. Pure factors propagate the explicit three-party realignment-only and two-party SIC-only examples. This is a qualitative detection-set comparison, not a formula for their values on all mixed states.
4. The even-party noisy-GHZ formulas in TURN_2 and the Schmidt-correlated formulas in TURN_3 are exact **complex, individual-factor projective norms**, including arbitrary coefficient phases and odd party counts in TURN_3. Statements about actual SIC measurements retain the existence qualification; the canonical SIC-Gram map exists independently of that qualification.
5. On the stated p ∈ [0,1] three-qubit noisy/dephased GHZ family, the physical region, both exact tester values, all strict detector inequalities and their equality boundaries in TURN_4 are correct. TURN_5 correctly compares them with the credited full-separability and biseparability thresholds. The complete threshold ordering is θ_F < θ_R < θ_B < θ_S for 0 ≤ p < 1, intersected with positivity; all thresholds are zero at p=1.

No claim concerning arbitrary input regroupings, tensor-power activation, normalized postselected filtering, all mixed states, or SIC existence in every dimension follows from the packet.

## 3. Central completeness theorem: analytic audit

### 3.1 All required maps are covered

The source permits complex-linear S₁-to-Euclidean norm-one maps. Allowing norm at most one in the upper bound is harmless, and scalar trace has norm exactly one. The proof makes no positivity, symmetry, covariance, identical-tester, square-output, or Hermiticity-preserving assumption.

For every allowed E, a rank-one orthogonal projector Q has trace norm one, hence ‖E(Q)‖₂≤1. Restriction of E to the real space of Hermitian matrices is real-linear. Its values on a Hermitian basis can be arbitrary complex output vectors. This is exactly the input needed for the energy identity; it does not invoke JLN's real-to-complex extension claim.

### 3.2 Finite second moment and energy constant

The ensemble weights sum to one: the d coordinate projectors each carry 1/[d(d+1)], and the flat-phase ensemble has total weight d/(d+1). For a flat rank-one projector, the phase exponent for each independent fourth root lies in {−2,−1,0,1,2}. Thus a surviving expectation requires exponent zero, not merely an unexamined congruence class. The two pairings of indices yield (I+F)/[d(d+1)], with the all-equal-index correction supplied by the coordinate projectors. This is valid over the complex field and needs no SIC/design-existence theorem.

If Q=Σ_a r_aG_a with G₀=I/√d and a Hermitian Hilbert–Schmidt orthonormal basis, the coefficients r_a are real. The second moment gives the exact covariance claimed in TURN_1. Expanding the squared output norm, including the real parts of complex inner products, therefore gives

E‖L(Q)‖² = ‖L(G₀)‖²/d + Σ_{a>0}‖L(G_a)‖²/[d(d+1)] ≤ 1.

The constant d(d+1) and the separate identity-direction coefficient are correct. Averaging projectors does not average, symmetrize or restrict the map being optimized.

### 3.3 Flip identity and tensor bound

For a Hermitian Hilbert–Schmidt orthonormal basis, F=Σ_aG_a⊗G_a, **without a transpose or conjugate on the second factor**. The trace identity Tr(F(A⊗B))=Tr(AB) establishes its coefficients. Including imaginary off-diagonal Hermitian basis elements is essential; this identity was independently checked in dimensions 2–5. It is not the formula for the maximally entangled rank-one operator.

Since ad+b=1/d, the state expansion in TURN_1 is correct. The projective crossnorm and triangle inequality, then Cauchy–Schwarz over the traceless index, give

‖(E⊗G)(ρ_f)‖π ≤ u_Eu_G/d + |b|√(S_ES_G).

When |b|≤1/[d(d+1)], the last expression is bounded by the inner product of the two nonnegative energy-coordinate vectors (u/√d, √S/√[d(d+1)]). A second Cauchy–Schwarz bound is ≤1 by the energy budgets. Neither inequality depends on the number of coordinates in either output. This is a universal analytic bound, not a sampled optimization.

The condition is exactly |df−1|≤d−1, equivalently 2/d−1≤f≤1. Intersecting with f<0 is nonempty precisely for d≥3. No d=2 counterexample is claimed. Both endpoint inclusions and the strict entanglement endpoint at f=0 are handled correctly.

### 3.4 Explicit state and entanglement

The flip has +1 and −1 eigenspaces of dimensions six and three when d=3. For (19I−9F)/144 the resulting eigenvalues are 5/72 and 7/36, respectively. They are strictly positive and sum to one with multiplicities. The flip expectation is −1/6.

For positive A and B, Tr(AB)=Tr(A^{1/2}BA^{1/2})≥0. Consequently every separable state has nonnegative flip expectation, which independently certifies that the displayed density matrix is entangled. The exact matrix control additionally finds a partial-transpose eigenvalue −1/18; this is a redundant reviewer check, not a replacement proof or an added author theorem.

The pair of trace maps yields Trρ=1, establishing attainment and **exactly one**, rather than only “at most one,” for the optimized value. The coefficient margin 1/16<1/12 is correct but does not make the optimized value strictly less than one, since the trace pair remains available.

### 3.5 Extensions and excluded operations

Adjoining local output vectors multiplies the projective norm by their Euclidean norms. Each appended local density matrix has output norm at most one. Partial trace of a hypothetically fully separable extension would make the original pair separable, so the extension remains non-fully-separable. The embedding argument uses trace-norm isometries and positive local compression and is valid.

Local transposition is itself a complex-linear trace-norm isometry and can be absorbed into a tester. Accordingly, the universal theorem also covers such precomposition. The sentence excluding “partial transpose” in SOURCE_SCOPE needs the clarification in section 9; it does not invalidate the theorem.

## 4. Fixed maps, complex tensor norms and TURN_2

The canonical map L_d has the stated Gram identity

⟨L_d(X),L_d(Y)⟩ = [Tr(X*Y)+overline(TrX)TrY]/2.

The inequalities ‖X‖₂≤‖X‖₁ and |TrX|≤‖X‖₁ prove complex S₁ contractivity directly. A SIC with the stated normalization has this same positive-definite Gram form. Since L_d is invertible, equality of Gram forms makes S L_d^{-1} an output unitary. Thus actual-SIC values equal canonical-map values when that SIC exists. The tetrahedral qubit construction is valid and removes the existence issue for every explicit incomparability example.

The orthogonal-block lemma is sound. Summing phase-adjusted block dual functionals has norm ≤1 because Hölder with m factors gives Σ_α∏_i a_{iα}≤∏_i‖a_i‖_m≤∏_i‖a_i‖₂. It works over the complex field, for unequal block dimensions and m≥2. It is not an assertion that every arbitrary tensor decomposition is blockwise.

The even real-power lemma is likewise genuinely complex: B(x,y)=Σ_kx_ky_k is complex bilinear and satisfies |B(x,y)|≤‖x‖₂‖y‖₂. Products of B have norm at most one on arbitrary complex arguments and give the desired positive value on the real repeated vectors. No real/complex projective-norm identification or bipartite flattening is being assumed.

With these lemmas, the diagonal noisy-GHZ tensor and each individual off-diagonal matrix-unit block have precisely the norms stated in TURN_2. The threshold denominators are positive; the q=1 equalities and q≥2 strict ordering are correct. The bound (1/2)^q+(3/4)^q<1 already holds for q=2 and decreases thereafter. The values 9/8 and 29/32 for the four-qubit example are correct.

For the three-qubit example p=9/20, 83/80 is a valid realignment lower bound and 627/640 a strict SIC upper bound. No odd-party equality is asserted at that turn. For η_p the Pauli correlation matrix and both triangular-block nuclear norm calculations are correct. The detection thresholds p>2−√3 and p>1/4 have the right direction, and p=4/15 lies strictly between them. Independently applying the actual tetrahedral SIC matrix reproduces the formulas. State the convex-mixture domain 0≤p≤1 explicitly in a polished presentation.

Pure local projectors have image norm one for both maps, so appending pure qubit factors preserves both strict separations. Those examples need not be GME; the author appropriately says so. This does not contradict the cited two-party implication that realignment detection implies SIC detection.

## 5. TURN_3: Schmidt-correlated family and trilinear certificate

The isometric embedding of the positive trace-one coefficient matrix A makes ρ_A a density matrix. The local diagonal Gram matrix has entries (1+δ_ik)/2, independent of ambient local dimension. Equal Gram matrices yield the local isometries used to identify the diagonal configurations. The centroid computation gives c²=(r+1)/(2r), lying strictly above 1/2 and at most 3/4. The off-diagonal image vectors are orthonormal after multiplying by √2 and orthogonal to the diagonal span. The block lemma therefore applies with complex phases of a_ik intact.

The potentially delicate step, the odd-party diagonal norm, is correct. For c∈[1/√2,1], λ=(3c²−1)/(2c³) and h=1/(2c) are nonnegative and at most one. Absolute-value Cauchy–Schwarz applied to the complex bilinear perpendicular pairings gives exactly the 2×2 real symmetric matrix M(w) in TURN_3. Direct symbolic expansion confirms

det(I−M(w)) = (4c²−1)(w−c)²/(4c⁴).

Both diagonal minors of I−M are nonnegative. Its positive semidefiniteness bounds the larger eigenvalue of M by one; the nonnegative trace bounds the absolute value of the smaller eigenvalue by the larger. Therefore ‖M‖op≤1. This last argument is needed because M itself is not asserted to be positive semidefinite. It is present and valid in the packet. The factorization of 1−λ and evaluation T_c(v,v,v)=1 are also correct, including the endpoints.

For even m the paired B certificate, and for odd m≥3 its product with T_c, have norm at most one and value one on every diagonal repeated unit vector. These prove diagonal projective norm one. Adding the separate off-diagonal blocks proves the full complex formulas 1+C(A) and 1+2^{-m/2}C(A).

The partial-transpose 2×2 blocks correctly show non-full-separability whenever any off-diagonal coefficient is nonzero. The GME assertion uses a separate valid support argument: every vector in a positive ensemble decomposition belongs to the correlated support; a vector in that support that is product across any nontrivial cut has only one nonzero correlated coefficient. Thus any biseparable mixture supported there is diagonal. It does **not** rely on the false general implication “NPT across every cut implies GME.” The known separability facts and grouped realignment value are credited to Zhao–Fei–Wang; no uniqueness-of-maximizer claim from that paper is imported.

## 6. TURN_4: exact three-party detector regions

The binary cubic's proposed two-vector decomposition expands exactly to T(A,B): Wu³=A and Wu(1−u²)=B. Because 0≤B≤A, u lies in the certified interval for T_u. The primal decomposition and complex dual certificate give matching values (A+B)^{3/2}/√A, also at B=0. This establishes a full three-factor projective norm rather than only a flattening norm.

For ρ_(p,z), the six background eigenvalues and the distinguished 2×2 block yield the stated physical bound |z|≤(1+3p)/4. The realignment diagonal coefficients A_R,B_R and SIC coefficients A_S,B_S are correct; the two off-diagonal blocks contribute t and t/(2√2), respectively. The resulting formulas

r₃=t+(1+p)^{3/2}/(2√2),

s₃=t/(2√2)+(3+p)^{3/2}/8

are exact. Coefficient phases are accounted for by separate complex one-dimensional blocks. A local phase unitary provides an independent invariance explanation.

The detector inequalities are strict; equality with one means no detection. The derivative proving θ_S>θ_R for p<1 has the right sign and endpoint. On z=p, both equations before squaring have nonnegative/positive right sides throughout [0,1], so the displayed cubic equations have no extra root in that interval. Strict monotonicity of the original tester values proves uniqueness. The p=1/2 radical certificates and the p=1 consistency with TURN_3 are correct.

## 7. TURN_5: separability regions and finite decompositions

The full-separability necessity follows from the explicit partially transposed block b±t/2. Sufficiency is independently established by the sixteen-product-vector phase average, not by an invalid general PPT sufficiency claim. The phase cancellation argument is correct for all phases: exponents δ₁−δ₃ and δ₂−δ₃ lie between −2 and 2, and the only surviving nondiagonal coordinates are the distinguished conjugate pair. Formula (4) reconstructs the state exactly, all weights are nonnegative under t≤2b, and they sum to one.

For biseparability, the matrix-element inequality is valid even when different pure components use different bipartitions. The author correctly assigns each component to a cut and applies weighted Cauchy–Schwarz and positivity of partial diagonal sums. On this family it gives t≤6b. Each four-phase τ_A is product across its specified cut; their average τ is biseparable and has the stated 1/4 and 1/12 diagonal entries and distinguished coherence 1/4. Formula (6) reconstructs the state with nonnegative weights under both physical positivity and t≤6b. These two conditions also imply 2t≤1, as follows from the nonnegative weights summing to one. Thus no hidden negative mixture coefficient is present.

The three threshold comparisons were independently expanded symbolically. Their signs, equality endpoints and derivative proof are correct. The physical upper bound is necessary when interpreting the vertical bands; below p=1/3, for example, no GME point exists in this family. The packet explicitly intersects the inequalities with positivity.

The noisy-line thresholds 1/5 and 3/7 and the ordering 1/5<α_R<3/7<1/2<α_S<1 are correct. All three examples have the claimed status. Most importantly, p=z=3/7 is biseparable yet realignment-detected, so realignment detection in this family cannot be advertised as an exact GME certificate. Conversely, every GME state in this family is realignment-detected, and SIC detection here implies GME. These are family-specific statements.

The credited GHZ-symmetric source uses x=t/2, y=√3p/4 after removal of the phase. Its full-separability and biseparability lines reproduce the stated boundaries where the lines meet the physical region. The lower-p portion is handled by the intersection with positivity and by the explicit decompositions. Attribution is appropriate.

## 8. Sources, reproducibility and independence

### Direct source checks

- [OWR contribution](https://ems.press/content/serial-article-files/46927?nt=1), printed pp. 2696–2698: four distinct questions were verified, with central completeness separate from the mixed-state and dimensional-efficiency agenda.
- [JLN arXiv:2010.06365v1](https://arxiv.org/abs/2010.06365v1): Definitions 3.1/Corollary 3.3, Section 8.2, Theorem 10.1 and Section 13 were inspected. The source's fixed-Werner failure interval is prior knowledge; the all-tester upper bound is the additional claim audited here. The official arXiv page currently lists only v1. The [journal landing page](https://link.springer.com/article/10.1007/s00023-022-01187-9) does not establish that its inaccessible full text is identical.
- [Shang et al.](https://arxiv.org/abs/1805.03955v3): the SIC normalization and prior bipartite context are correctly credited.
- [Zhao–Fei–Wang](https://files-www.mis.mpg.de/mpi-typo3/preprints/2008/preprint2008_21.pdf): Proposition 1 and the grouped realignment calculation in Proposition 2 support the credited classical facts; the packet supplies its own full-factor complex norm proof.
- [Eltschka–Siewert](https://arxiv.org/abs/1304.6095v1), equations (11)–(12), and [Gühne–Seevinck](https://arxiv.org/abs/0905.1349v3), Observation 1: the separability boundaries and biseparable matrix-element inequality are appropriately attributed.
- [Shi–Sun](https://arxiv.org/abs/2211.04868v1), [Lu et al.](https://arxiv.org/abs/2512.22514v1) and [Nechita's 2025 lecture](https://nechita.net/assets/pages/teaching/icts-2025-tensor-norms-for-quantum-entanglement.html): the inspected scopes do not give an all-local-tester completeness resolution or the asserted full-projective-norm comparison as an existing theorem. In particular, bipartition matrix criteria must not be substituted for the m-factor norm.

The warning about the preprint's deformed canonical map for x<1 is justified: an off-diagonal rank-one matrix has trace norm one but image norm √[d/(d−1+x²)]>1. The present proofs neither use that normalization nor depend on Lemma 3.2. This review makes no claim about a correction in the journal edition.

A bounded independent web search on the exact title, all-tester completeness, Werner/factorization terms, and “counterexample”/“incomplete” did not locate a later universal resolution or a direct contradictory prior theorem. Search results about property-testing protocols or EPR communication testers were distinguished from the present Banach-space maps. This is **not** an exhaustive citation or historical-priority certification. PRIOR_GATE.json's earlier repository search is recorded evidence with its own stated limits; this reviewer did not repeat its all-reference search.

### Reproducibility

Running each frozen `verify_turnN.py` under Python 3.12.14 succeeds. Every rerun JSON is byte-for-byte equal to the corresponding frozen TURN_N_CHECKS.json. Counts are:

- Turn 1: 137,715
- Turn 2: 61,138
- Turn 3: 87,063
- Turn 4: 33,534
- Turn 5: 187,993
- Total: 507,443

The independent `independent_checks.py` passes 3,778 assertions under Python 3.12.14, NumPy 2.3.5 and SymPy 1.14.0. It checks generic symbolic identities; the exact 9×9 counterexample and its partial transpose; genuinely imaginary Hermitian-basis flip expansions; 300 certified complex tester pairs with unequal output dimensions; 2,000 complex trilinear samples plus equality controls; a directly constructed tetrahedral SIC; coefficient-matrix norm formulas; symbolic phase-selection rules; and all input/source hashes. Its sampled controls are explicitly labeled numerical and use tolerances. They are not universal proof, and their low sampled maxima are not optimality claims. The universal conclusions in this report rest on the written analytic arguments above.

The author scripts are standard-library-only as advertised. Their large finite counts are useful regression controls, but do not replace any quantifier in the proofs. No frozen author or source file was modified. No sixth author search, remote write, PR or queue edit was performed. Reviewer computations were confined to auditing frozen claims.

## 9. Required corrections and publication safeguards

There are **no required mathematical repairs** to the proved theorems. The following presentation requirements apply before a result is published:

1. **Clarify local transposition.** SOURCE_SCOPE's sentence saying no partial transpose is allowed can mislead. Transposition T:X↦Xᵀ is already a complex-linear S₁ isometry, so E∘T is an allowed tester. Say instead that the theorem concerns the original local matrix-factor partition and does not enlarge the family by nonlocal input-index reshufflings/regroupings. Local transpose precomposition is already covered by the universal bound. This is a strengthening/clarification of scope, not a proof repair.
2. **Supersede old review-status language in current packaging.** Do not cite the unavailable earlier review as verified evidence. Frozen TURN_3 and historical state files may remain intact as chronology, but a current README/result summary should point to this fresh audit and distinguish its verdict from the historical claim.
3. **Retain the exact split of statuses.** The central completeness question is negatively resolved by the scoped theorem; the broad OWR bundle remains exhausted/scoped partial at 5/5. Do not reset the turn count because of recovery or a missing global queue entry. Do not convert the subjective “65%” planning estimate into a mathematical-completion claim.
4. **Preserve the qualifications already present.** Actual SIC existence is conditional outside the explicit qubit cases; detection means >1; the norm is the full complex m-factor projective norm; non-full-separability is distinct from GME; prior separability and fixed-tester results retain attribution; no novelty certification is claimed.

Minor editorial recommendation: explicitly state 0≤p≤1 when introducing η_p in the polished TURN_2 presentation. Its use as a convex-mixture density matrix and all calculations already operate in that range.

Do not publish raw third-party PDFs or the review's source-page screenshots as original work. The shareable review deliverables are REVIEW.md, independent_checks.py, INDEPENDENT_CHECKS.json, the five rerun JSONs, AUDIT_METADATA.json and REVIEW_MANIFEST.json. Source screenshots are private audit aids and are excluded from the deliverable manifest.

### 9.1 Exact additive clarification and locations

The text requiring clarification is `attempt/SOURCE_SCOPE.md`, line 18, first sentence. Related wording in `TURN_1.md`, line 115 (the theorem's “without input index permutation”) and line 135 (“index-permuted tester family”) should be interpreted in the same fixed-local-partition sense. Those frozen proof lines do not need alteration.

Preserve the historical files and their existing manifest. Add a current `PUBLICATION_SCOPE_CLARIFICATION.md` (or an equivalently named additive note), link it from the current publication README, and bind it in a new administrative packaging manifest. Proposed complete paragraph:

> The theorem fixes the original local matrix-factor partition. It excludes enlarging the criterion by nonlocal input-index reshufflings or regroupings. Local transposition T(X)=Xᵀ is a complex-linear trace-norm isometry, so E∘T is already an allowed local tester whenever E is. Consequently the all-tester upper bound also covers precomposition by partial transposition on any chosen local factors. SOURCE_SCOPE.md's earlier “no partial transpose” wording is superseded by this clarification. No theorem, proof, five-turn count, or scoped-partial status changes.

The old review-status wording is located in `TURN_3.md`, line 117, and `CURRENT_STATE_T2.json` through `CURRENT_STATE_T4.json`. Preserve those files as historical records; the present current package should explain that this audit supersedes their unrecovered historical-review provenance. `README_CURRENT.md`, final paragraph, correctly says that the present audit was pending when it was frozen; a new administrative publication README may now report the final audit result without rewriting that frozen history.

The additive note is a presentation correction following this audit, not a sixth author research turn. Its final text and administrative rebind should be checked against this paragraph before publication.

## 10. Gate recommendation

The parent may treat the central counterexample and the enumerated supporting results as independently mathematically validated, subject to the presentation safeguards above and its own publication decision. The accurate full-bundle status is **exhausted/scoped partial, 5/5**, not an unrestricted solution of every question in the source. No additional author turn is needed or authorized for this audit's conclusions.
