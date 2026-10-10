# Independent adversarial audit: five-segment unitary-multiplicity candidate

## Verdict

**PASS for the submitted mathematical argument, with one nonblocking citation-locator correction.** No fatal mathematical gap was found in the frozen argument. The complete-Hom basis, analytic specialization, nonzero diagonal transport, quotient-kernel containment, odd-cycle obstruction, and noninduction certificate all survive the requested checks. The final manuscript disposition is recorded separately in ACCEPTANCE.md; this report preserves the scope of the independent full audit.

The inspected candidate is the Langlands quotient over GL_15(E), where F=Q_3 and E/F is unramified quadratic, with ordered segments

E=[4,6], D=[2,5], C=[3,3], B=[1,4], A=[0,2].

The conclusion established by the supplied argument, using the cited published results, is that this quotient is irreducible, individually τ-invariant, not an entire proper parabolic induction, and has zero invariant-functional multiplicity for each of the two Hermitian forms. Consequently it violates the repaired p-adic complex target at k=1, where the proposed total is 2.

Only correction requested: FLO equation (4.5) is on printed p.225, not p.224. Its definition of the normalization begins on p.224. This does not affect any calculation.

## Scope and inputs

This is an audit of the existing argument. The mathematical source interfaces and their applications are reviewed below; no new proof approach is introduced.

The principal reviewed manuscript is the complete five-segment proof. The current public proof incorporates the p.225 locator correction and explicitly identifies the unnormalized forward M kernel. The exact target model appears in `MODEL.json`.

Primary dependencies checked in retained full texts:

- Feigon–Lapid–Offen, *On representations distinguished by unitary groups*, published IHES 115 (2012), pp.185–323, [DOI](https://doi.org/10.1007/s10240-012-0040-z). The key statement/formula pages 291, 293, and 294 were also visually checked.
- Lapid–Mínguez, *On parabolic induction on inner forms of the general linear group over a non-archimedean local field*, [arXiv:1411.6310v3](https://arxiv.org/abs/1411.6310v3). The matching relation on p.35 and Proposition 5.20 on p.38 were also visually checked.
- Jacquet–Piatetski-Shapiro–Shalika, *Rankin-Selberg Convolutions*, American Journal of Mathematics 105 (1983), pp.367–464, [author-hosted scan](https://www.math.columbia.edu/~hj/Rankin%20Selberg%20convolutions.pdf). The setup on p.444 and equation (5) on p.445 were visually checked.
- Lapid's 2011 workshop contribution, [OWR 14/2011](https://doi.org/10.4171/owr/2011/14), p.734, supplies the target's noninduced definition and conjectured total multiplicity.

Source results are used as mathematical dependencies; this audit does not reprove the cited classification or analytic theorems. Current FLO and LM primary landing pages were reopened to verify source identity. No comprehensive claim about historical novelty is made.

## 1. Representation conventions and target hypotheses

FLO's segment representation attached to [a,b] is the unique irreducible quotient of the ascending product ν^a×…×ν^b; it is essentially square-integrable. This agrees with LM's L([a,b]), not LM's Z([a,b]). Thus the candidate's standard module and its Langlands multisegment are correctly identified. The lengths 3,4,1,4,3 sum to 15, and the real central exponents 5,7/2,3,5/2,1 are strictly decreasing.

The field Q_3, the quadratic field extension, and smooth admissible complex coefficients are within the repaired target. The Langlands quotient is irreducible and admissible. Every character ν_E^j is fixed by entrywise τ, hence each segment and the unique quotient are τ-invariant. The F-side lifts D_F[a,b] and its η∘det twist are distinct: their cuspidal supports lie on distinct unramified character lines. Local quadratic base change identifies them with D_E[a,b].

Using k=1 is legitimate. The single target factor is the irreducible quotient π itself. The proof does not misidentify its five reducible standard-module factors as a target tuple. The target condition that the whole product be irreducible is automatic for the one-factor product. Being a quotient of a reducible induction does not violate the target's definition of noninduced; being the entire irreducible induction would, and is excluded separately below.

For n=15 there are two Hermitian isometry classes. The proof fixes an arbitrary nonsingular Hermitian matrix x and works with H=G_x throughout. It does not confuse two isometry classes with two nonisomorphic abstract groups. In odd dimension the associated unitary groups can be conjugate; both orbits still enter the target's sum. Proving vanishing for arbitrary x therefore gives the required total zero.

## 2. Completeness and regularity of the period bases

FLO Corollary 13.6, printed p.291, literally supplies a basis of the entire Hom_H(I(δ),C), and holomorphy at zero of the unnormalized J periods, provided all δ_i are τ-invariant essentially square-integrable and no earlier factor satisfies δ_i≼δ_j. It is not merely a selected family of invariant functionals and not a generic-parameter-only theorem.

The relevant FLO relation is a_i≤a_j≤b_i≤b_j. It differs from the linked-segment relation a_i<a_j≤b_i+1 and b_i<b_j. Both relations were checked separately. All ten earlier/later pairs in each of the three orders EDCBA, ECDBA, and EDBCA pass FLO's hypothesis; all three orders also satisfy LM's ordered-form condition. The only reversed endpoint-start pairs in the latter two orders are strict containments, so neither FLO precedence nor linkage is introduced.

Each of the five factors has two distinct F-side lifts. Modulo simultaneous η twist, choosing ε_E=0 gives exactly 16 lift labels. FLO (12.1) asserts independence after restricting the Levi functionals to the fixed orbit x·G∩M. Thus this quotient of the label set is valid for an arbitrary fixed x, not only after summing over x. Corollary 13.6 gives the corresponding 16-element complete basis on each I_r.

The author therefore expands every pullback ℓ∘p_r uniquely. There is no gap from possible hidden non-open-orbit functionals at the singular point.

## 3. Rankin–Selberg scalars and exact operator orientation

Let t=λ_i−λ_j. The author's reverse operator goes from the swapped order into the original order. FLO (12.5), after removing the open-period normalization (4.5), gives exactly the reverse/forward ratio

γ(−t,δ_i'^∨×δ_j'⊗χ)/γ(t,δ_i'×δ_j'^∨⊗χ),

up to nonzero constants or invertible exponential factors. Here χ=η^(1+ε_i+ε_j), so χ=η for equal labels and χ=1 for opposite labels. This is the same orientation and label alternative printed in FLO (13.3)–(13.4). Neither reciprocal inversion nor a covert label flip is present.

JPSS §8.2, equation (5), uses the top character of the longer segment and all characters of the shorter segment. Substituting the dual endpoints gives exactly the author's exponents b−c−j for 0≤j<min(lengths). This was also reconstructed independently from the highest weights of the tensor product of the two special Weil–Deligne representations. The latter check is a consistency calculation, not a replacement for JPSS.

The exact directional exponent lists for the pairs used are:

| Pair | Forward L(0) exponents | Reverse L(0) exponents | Ratio zero order if χ=1 |
|---|---|---|---|
| E,D | 4,3,2 | 1,0,−1 | 2 |
| D,B | 4,3,2,1 | 2,1,0,−1 | 2 |
| B,A | 4,3,2 | 1,0,−1 | 2 |
| E,C | 3 | −1 | 1 |
| C,A | 3 | −1 | 1 |
| D,C | 2 | 1 | 0 |
| C,B | 2 | 1 | 0 |

For χ=η, η(3)=−1 and all real-integer Euler factors are units, so every listed ratio has order zero. For the nested pairs the ratios are units for χ=1 too. After suppressing epsilon factors, their exact limits are 9/13 for χ=1 and 9/7 for χ=η. The actual epsilon factors are invertible monomials, so suppressing them cannot change a zero, pole, or nonvanishing assertion. The q_E=9 directional gamma factors of the nested pairs are likewise units.

These facts were checked as exact rational functions in z=3^(−t), rather than by floating point or solely by a count copied from the author. The diagnostics passed under ordinary Python, `python -O`, and `python -OO`, without relying on assertions that optimization could remove. Actual mutation and UID1000 read-only tests are documented in `DIAGNOSTIC_VALIDATION.md` and the machine-readable validation receipt.

## 4. Holomorphic, invertible transport through the nested swaps

This is the highest-risk analytic interface and is valid here. The swap D,C has centers 7/2>3; the swap C,B has centers 3>5/2. In either positive direction, FLO Lemma 1.1(3) makes the unnormalized rank-one M holomorphic in a neighborhood of the specified parameter. The Shahidi multiplier defining N is finite and nonzero there by the E-side exponent computation. Therefore the positive-direction N is holomorphic. The reverse-direction N is holomorphic by the negative-chamber assertion in the same lemma, after untwisting the factors to unitary discrete series.

The meromorphic inverse identity in FLO §1.4 then specializes: both operators are defined at zero and their compositions are the identity. Thus neither specialization vanishes or loses rank. Parabolic induction of the block isomorphism gives the required full-module isomorphism.

Both entire period bases are holomorphic at zero by Corollary 13.6. Their meromorphic functional equation has a scalar unit at zero for every label. Therefore pullback by the unlinked isomorphism takes each source basis functional to a nonzero scalar multiple of its corresponding target basis functional. The labels stay attached to their segments. E remains first, so even the chosen representative condition ε_E=0 is unchanged. There is no mixing of coordinates and no need to select a new basis at the singular parameter.

## 5. Linked kernels, specialization, and necessity only

For every linked pair used, the larger endpoints appear first and the center difference is positive. FLO Lemma 1.1(4) identifies the image of the holomorphic reverse N with a proper rank-one kernel inside that pair's standard product. Inducing with the remaining factors preserves exactness. Its image K_ij in I_r is proper because induction is faithful on the nonzero quotient. The full module has a unique maximal proper submodule, either directly by LM Theorem 2.6 or through its isomorphism with I_1. Hence K_ij is contained in ker(p_r).

It follows that ℓ∘p_r annihilates the reverse intertwiner image for every invariant functional ℓ on π. No assertion that these K_ij generate the full kernel is made or needed.

One must not simply evaluate an arbitrary swapped-order open period globally at a possible pole. The author's actual step correctly restricts the identity to the open-orbit subspace first. FLO (6.6) makes those restricted integrals entire and identifies them with the Levi-functional space. FLO (12.1) then gives their linear independence at zero. The left-hand side and every scalar ratio are holomorphic there. Specialization therefore gives a_ε c_ε(0)=0 separately for each label.

For linked pairs c_ε(0) is nonzero when the two labels agree. Every surviving coordinate must consequently assign opposite labels to that pair. This is the necessary-direction argument on FLO pp.293–294, extended only by exact valid isomorphisms of the specified orders. It does not import FLO's later sufficiency argument for ladders or any general standard-module-kernel-generation equality. Luo–Zha's reported counterexample to a related kernel conjecture has no dependency role here.

## 6. The parity contradiction

The constraints on a nonzero coefficient are:

- E≠D and B≠A in EDCBA;
- E≠C and D≠B in ECDBA;
- C≠A in EDBCA.

The transports in §4 preserve the support of the coefficient vector. Therefore these are simultaneous conditions on one fixed assignment to the five segments. They form E–D–B–A–C–E. Summing the five equations ε_u+ε_v=1 over F_2 gives 0=1. The independent diagnostic also enumerated the 16 representative assignments and found none.

Completeness then forces ℓ∘p_1=0; surjectivity of p_1 forces ℓ=0. This proves vanishing for arbitrary x. A zero upper bound already determines the multiplicity; no separate existence or descent theorem is needed.

## 7. Noninduction: exact convention and all partitions

Suppose π were an entire irreducible normalized induction from a proper Levi. An inducing module must itself be irreducible, by exactness and faithfulness. Grouping Levi factors yields an entire irreducible two-factor product L(m_1)×L(m_2). The Langlands analogue of LM Proposition 2.5(5), supplied by Theorem 2.6, says L(m_1+m_2) occurs. Since the whole product is irreducible and equals π, classification forces m_1+m_2 to be exactly the candidate multisegment. Both multisets are nonempty and therefore partition the five distinct segments.

There are 15 unordered nontrivial partitions. Every partition has a ladder side in the precise LM Definition 5.13 sense: strict start and end ordering, with no extra consecutive-linkage requirement. Singletons are ladders. Of the two-element sides, only DC and CB fail; their complements EBA and EDA are ladders.

LM Proposition 5.20 is indeed an if-and-only-if criterion when one side is a ladder, with both directed LC conditions required. Its LC relation on p.35 is exactly the relation transcribed by the author: X consists of u≺v, Y of (u−1)≺v, and a Y vertex (u_2,v_2) may cover X vertex (u_1,v_1) precisely when either u_1=u_2 and v_2≺v_1, or v_1=v_2 and u_1≺u_2. Visual checking confirms the shift is on u, not v.

The proposition is stated for Z(m)×Z(n). LM §A.5 supplies a ring involution taking every irreducible Z(m) to L(m). A product has length one if and only if its image under this positive basis permutation has length one. Thus the same reducibility test applies to the candidate's L multisegments without replacing them by incorrectly involuted multisegments.

A new checker enumerated all 15 partitions independently, built X,Y and every possible matching edge, and found at least one isolated X vertex in one directed LC problem for each partition. This verifies all 15 singleton Hall defects rather than merely running the author's matching program. The full independent lists are in `INDEPENDENT_RESULTS.json`; the author's displayed witnesses are consistent with them. Every possible proper factorization is therefore excluded.

## 8. Adversarial boundary checks and limitations

The asserted result would also contradict FLO Conjecture 6.12 in this τ-invariant pure case. That consequence was used as an extra reason to scrutinize the basis and transport steps; it is not a substitute for checking them. The inspected source proves its conjecture for generic, unramified, ladder-product, and unitarizable cases, none of which automatically includes this five-segment nonladder prime quotient. No applicable contrary theorem was supplied by the source packet. This audit makes no exhaustive modern-literature or novelty claim.

The finite scripts do not compute Hom spaces. Their role is checking the endpoint hypotheses, scalar valuations, parity, and Hall obstructions. The actual multiplicity conclusion depends on the precise FLO theorems and the analytic argument above. The model remains the explicit characteristic-zero p-adic smooth-complex repair. No all-local-fields theorem is asserted.

Subject to the cited primary theorems, the submitted argument is complete. The one locator correction is editorial and nonblocking. Publication status and any wider historical claim remain outside this audit.
