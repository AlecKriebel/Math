**Integrated reader status.** Accepted source-to-theorem interpretation, including the required GL→SL and GU→SU transfer. This is the final scope statement. See the [integrated theorem](../README.md) and [dependency map](../DEPENDENCIES.md).

# Bray source scope acceptance

13 October 2026. Independent source-to-theorem adjudication for the Bray sampling problem OWR-14745-003.

## Decision

**The source's asymptotic random-sample question is resolved in the stated scope.** The accepted results, together with the credited linear/unitary literature and the elementary special-group transfer proved below, cover every natural classical family in the source's algorithmic setting. The mathematical claim must explicitly say sufficiently large natural dimension, independent uniform samples, any fixed desired confidence, and containment of the second derived subgroup of the centralizer.

This conclusion does not depend on inventing a broader meaning of classical group. It also does not regard every limitation printed in an individual proof as an unresolved part of the source problem. Projective involutions with order-four lifts, similitudes, characteristic two, non-natural representations, vanishing error at a fixed universal sample multiplier, and total running time are different statements.

There is a real wording issue in the source's displayed sufficient Problem: if interpreted literally without a large-dimension qualification, its marginal assertion is false in small dimensions. The small-dimension discussion below supplies an explicit counterexample. The source question is asymptotic, and the source's own credited linear resolution already imposes a dimension threshold. The all-dimensions marginal reading must not be silently advertised as proved.

## Sources and review basis

The primary contribution is Cheryl E. Praeger, joint with John D. Dixon and Ákos Seress, *Finding strong involutions in finite classical groups in odd characteristic*, OWR 37/2016, printed pp.2160–2161. Both pages were read in extracted text and visually inspected. [Report](https://ems.press/content/serial-article-files/46642); [DOI](https://doi.org/10.4171/OWR/2016/37).

The review read the recovered source statement; the symplectic and orthogonal marginal proofs; the generation bridge; its replacement class-generation theorem; and their independent audits. Their existing within-scope mathematical acceptances are retained. This review does not claim a new audit of every theorem in the established linear/unitary literature.

To settle terminology, I also retrieved the author manuscript of Leedham-Green–O'Brien, *Constructive recognition of classical groups in odd characteristic*, which the OWR contribution explicitly identifies as its algorithmic setting. Sections 1.1–1.2 list SL, SU, Sp, SO in all types, and Ω in all types in natural matrix representations. Section 2.1 uses sufficiently-large-dimension big-O and separately prescribes the failure probability. Author-manuscript pp.2–3 and 7 were read and visually inspected. The published Dixon–Praeger–Seress exposition, author-manuscript p.2, independently repeats the same family list. [LGO author manuscript](https://www.math.auckland.ac.nz/~obrien/research/classical.pdf); [LGO DOI](https://doi.org/10.1016/j.jalgebra.2009.04.028); [DPS author manuscript](https://people.math.carleton.ca/~jdixon/Strong%20Involutions.pdf).

The OWR contribution itself does not give an exhaustive group definition, a numerical success probability, or an explicit threshold. The identification just made uses its named algorithmic reference and the same authors' later exposition; it is a documented interpretation of the source context, not an assertion that the missing definitions were printed on pp.2160–2161.

## Source to theorem table

| Source obligation | Accepted result or credited input | Adjudication |
| --- | --- | --- |
| Natural finite classical matrix groups | Source-context list SL, SU, Sp, SO^ε, Ω^ε; ε includes both even types and odd dimension | All source families are covered below. O, GL, and GU also occur in the available theorems. No projective or similitude enlargement is needed. |
| Odd characteristic | Every new theorem assumes every odd prime power q; linear/unitary sources do likewise | Uniform in q, including q=3. Unitary natural dimension is over F_(q²), not restriction-of-scalars dimension. |
| Every fixed strong input involution t | Both natural ±1 eigenspaces have dimensions in the closed interval [n/3,2n/3] | Exactly the accepted hypothesis; no random choice of t or typical-class assumption. Membership t∈G is required. |
| Each separately fixed sign ε | Marginal proofs give the event on the selected eigenspace | Exact match. Neither simultaneous balance nor independence of the two marginal events is required. |
| Independent uniform g in the actual ambient G | New proofs and bridge use precisely that law | Exact match. Prior GU nearly-uniform theorems include uniform samples. Special-group transfer is proved below. |
| Positive absolute c'/log n marginal | Sp: c'=1/40000, n≥49152. O/SO/Ω: c'=1/5000000, n≥98304 | Both signs and all permitted dimensions/types above the cutoffs are included. |
| Linear/unitary marginal | DPS: GL, n≥700, c'=0.0002. GPRD: GU, n≥250, c'=0.0001 for nearly-uniform samples | Credited prior results. Transfer gives exact SL/SU uniform-sampling statements. |
| One statement across the source families | Minimum c'=1/5000000 and common marginal threshold n≥98304 | This is a valid all-source-family large-dimension marginal theorem, not merely an Sp/O theorem. |
| Modified algorithm target C_G(t)'' | New bridge identifies it exactly as Sp(A)×Sp(B) or Ω(A)×Ω(B); linear/unitary target is SL(A)×SL(B) or SU(A)×SU(B) | Derived-target identification for special linear/unitary groups is proved below. Full C_G(t) is not the modified source target. |
| Generation from class-random balanced outputs | Replacement theorem proves generation of natural Sp or Ω by 192 independent representatives from any prescribed sequence of strong classes | Its closed balance interval is exactly sufficient. The unverified PS2011 article is no longer a dependency of the new bridge. |
| Product containment rather than merely two surjective projections | Accepted bridge handles the simple-quotient subdirect obstruction and central lifts, then uses an independent extra output | No remaining projection-to-product gap. |
| O(log n) samples at high confidence | New bridge gives base probability >0.9 and arbitrary fixed confidence by repetition. GPRD Theorem 2 supplies the credited linear/unitary counterpart | Meets the fixed-error asymptotic interpretation justified below. |
| Dimension threshold | Marginal thresholds explicit; generation threshold includes an absolute d₀ from an inspected published constant | Existence of an absolute cutoff is sufficient for the source asymptotic question. No numerical overall cutoff is claimed. |
| Complexity being improved | Number of random group selections | No bit-operation, field-operation, random-sampler implementation, order-computation, or complete-recognition timing theorem is asserted. |

Here GPRD denotes Glasby–Praeger–Roney-Dougal, *Involution centralisers in finite unitary groups of odd characteristic*, J. Algebra 545 (2020), 245–299, Theorems 1–2. [Inspected preprint](https://arxiv.org/abs/1812.01362v2); [DOI](https://doi.org/10.1016/j.jalgebra.2019.09.009). DPS denotes Dixon–Praeger–Seress, *Strong involutions in finite special linear groups of odd characteristic*, J. Algebra 498 (2018), 413–447, Theorem 1.1. [DOI](https://doi.org/10.1016/j.jalgebra.2017.11.047).

## Exact consolidated claim

Let G be one of the natural matrix groups SL_n(q), SU_n(q), Sp_n(q), SO_n^ε(q), or Ω_n^ε(q), with odd q and an existing natural strong involution t. There is an absolute N such that, for every fixed δ∈(0,1), there is an absolute K_δ for which n≥N and M≥K_δ log n independent uniform samples g_i∈G satisfy

P( C_G(t)'' ≤ ⟨inv(t t^(g_i)) : 1≤i≤M⟩ ≤ C_G(t) ) ≥ 1−δ.

The constants are independent of q, t, the admissible natural dimension, and the form type. Here inv(y)=1 when |y| is odd, and y^(|y|/2) otherwise. This is an even-output version of Bray's procedure; retaining the odd outputs as well cannot reduce the generated subgroup.

For the new Sp/O/SO/Ω portion, write a=dim E_−(t), b=dim E_+(t), and take

- κ=1/40000 for Sp, and κ=1/10000000 for O/SO/Ω;
- L=ceil(κ^(−1)log n·log(385/η)), M=385L;
- n≥max(49152,3d₀) for Sp, or n≥max(98304,3d₀) for O/SO/Ω.

The accepted failure bound is η+q^(−a)+q^(−b)+13q^(−2b²/9). Setting η=1/20 gives success >0.9. Independent repetition r=ceil(log(1/δ)/log 10), retaining all outputs, supplies confidence ≥1−δ with O(log n·(1+log(1/δ))) samples.

For the credited GL/GU generation theorem, n≥n₁ and at least λ log n samples give probability >0.9(1−q^(−n/3)−q^(−2n/3)) of containing the product of SL/SU factors. At a common large threshold this exceeds 0.8, uniformly in q. The same elementary repetition argument therefore gives the consolidated claim. One may take a common N at least max(n₁,98304,3d₀); no explicit numerical value of n₁ or d₀ is asserted here.

## Special linear and special unitary sampling transfer

The difference between the groups named in theorem titles and the groups actually sampled cannot be ignored. The following elementary argument closes that precise scope issue.

Let D=GL(V), J=SL(V), or let D=GU(V), J=SU(V), with q odd. Fix a natural involution t∈J, and put V=A⊕B for its two eigenspaces. In the unitary case this decomposition is perpendicular and its summands are nondegenerate. The full centralizer is D(A)×D(B).

In GL, the determinant map from this centralizer onto F_q^× is surjective: scale a single basis vector of the nonzero space A and fix all other basis vectors. In GU, choose an orthogonal basis of A; scaling one vector by any scalar u with u^(q+1)=1 gives a unitary transformation of determinant u. Thus the centralizer determinant maps onto the full determinant image in this case too.

Since J is the determinant kernel, D=J C_D(t). Consequently t^D=t^J. A uniform conjugator in either finite group gives the uniform measure on this same conjugacy class, because all conjugation fibers have equal size. Therefore the entire random matrix inv(t t^g) has exactly the same law under uniform g∈D and uniform g∈J. For independent samples the joint laws are identical as well. This transfers both the marginal theorems and the even-output generation theorem, without asserting that a uniform SL sample is pointwise nearly uniform in GL or that a uniform SU sample is pointwise nearly uniform in GU.

Let L=SL(A)×SL(B), or SU(A)×SU(B), respectively. At the large dimensions in use, these factors are perfect. One has L≤C_J(t) and C_J(t)/L abelian, by the two determinant maps. Hence L=L'≤C_J(t)'≤L, giving C_J(t)'=C_J(t)''=L. The credited product-containment conclusion is exactly the requested second-derived target for the special groups. The same argument identifies the target in the full GL/GU groups.

This is a scope-transfer deduction from the existing theorems, not another asymptotic counting or generation construction. It needs to appear in the final integrated acceptance so that SL/SU are actually covered, rather than merely presumed to be covered by GL/GU theorem titles.

## Probability and complexity quantifiers

The intended quantifier order is: choose a desired fixed failure probability δ; obtain a sample multiplier depending on δ; the estimate then holds uniformly in q, t, and all sufficiently large natural dimensions. The source's reduction from a c'/log n marginal to O(log n) samples uses this interpretation. The same convention is explicitly supported by the named algorithmic reference's treatment of fixed failure parameters.

A fixed multiplier times log n need not make failure tend to zero merely from a c'/log n lower bound: the chance of no success can remain bounded by a positive constant. The accepted proofs give no stronger uniform assertion of 1−o(1) success with a single fixed multiplier. For δ=n^(−A), the stated amplification yields O((log n)²) samples. This is a boundary on the proven theorem, not a missing requirement supplied by the source.

The input involution t is given. The source separately discusses finding t and extracting recursive factors; those stages must not be folded into a claim that this work proves a new end-to-end field-operation bound. The sampling statement also does not furnish a certificate identifying which batch succeeded. It proves containment for the output subgroup with the stated probability, which is the quantified sampling question under review.

## Small dimensions and genuine characteristic restrictions

An absolute large-dimension threshold is mathematically substantive and must be displayed. It is nevertheless compatible with the source's asymptotic question and with its credited established cases. The later linear theorem already has n≥700; the later unitary marginal theorem has n≥250.

For an explicit failure of an all-n reading of the marginal Problem, take any odd q and G=Sp_4(q), with a perpendicular decomposition V=A⊥B into two symplectic planes and t=−I_A⊕I_B. This t is strong, since both dimensions are two. Every z=inv(t t^g) centralizes t, so z|_A∈Sp_2(q) and has square one. In odd characteristic it is diagonalizable with eigenvalues ±1. Since its determinant is one, its two eigenvalues cannot be one of each sign. Therefore z|_A is I or −I. Neither is strong on a two-dimensional space, where the two eigenspace dimensions would both have to be one. The required marginal probability is zero. The same holds on B.

Thus proving the literal unqualified marginal assertion in every dimension is impossible. This counterexample does not disprove logarithmic asymptotic centralizer generation, and it does not say the odd branch cannot help in small groups. No new small-dimensional marginal theorem is needed to resolve an asymptotic source question.

The new results genuinely exclude characteristic two, matching the source. Symplectic natural dimensions and both t-eigenspace dimensions are even. Special linear/unitary involutions have even negative dimension. Orthogonal membership imposes determinant and, for Ω, spinor conditions. The accepted theorems quantify over actual t∈G; they do not assume every putative pair of dimensions/types is realizable. The orthogonal proof includes odd ambient dimensions and both even Witt types, and all odd q. None of the small-dimensional perfectness or simple-quotient exceptions survives the displayed large thresholds.

## Remaining obligations and publication language

**No unresolved mathematical obligation remains for the source-faithful asymptotic sampling target**, once the existing accepted stages are combined with the credited prior theorems and the transfer above. There are integration obligations:

1. State the consolidated natural-family theorem with its threshold and confidence quantifiers; include the SL/SU transfer.
2. Present the replacement class-generation theorem as discharging the old conditional input. Preserve the historical fact that the original Praeger–Seress 2011 text was not verified, but do not leave its retrieval as a dependency of the new conclusion.
3. Identify C_G(t)'' correctly. The source's informal singular description as quasisimple must not override the actual product structure proved in the large-dimensional setting.
4. Keep the sample-count qualification and attribution. No conclusion about worldwide novelty follows from failing to locate an earlier Sp/O paper.

A useful narrow acceptance sentence is: “The source's asymptotic natural-classical sampling question is resolved: for every fixed confidence, O(log n) independent uniform samples generate a subgroup containing C_G(t)'' for all sufficiently large natural dimensions; GL/SL and GU/SU use credited prior results, while the audited new stages supply Sp and SO/Ω.” The full O family is an additional covered scope.

If a different problem is expressly demanded later, the exact additional obligations would be: establish a projective-centralizer/lift theorem for projective involutions; prove the relevant conjugacy and derived-target facts for similitude or other new ambient groups; derive a stronger success estimate for fixed-multiplier vanishing failure; or analyze computational operations and implementations for a total-time theorem. None should be added silently to this source question. An all-dimension positive marginal bound is already refuted by the example above, rather than merely left open.

## Evidence handling

The authored report contains source interpretation, mathematical deductions, and citations. Third-party PDFs, extracted text, and page renders remain private inspection evidence. The newly inspected LGO author PDF is 571,872 bytes, SHA-256 `8bceeabed3cd7fbf5bf40adc820d208bd0d661266b47e4c7d8fa560f0def688b`; its author-manuscript pagination is used above, not asserted to equal the journal pagination. A web screenshot attempt failed with a cache error, after which the author PDF was downloaded and rendered locally for successful inspection. No source text or page image is part of the authored acceptance claim.
