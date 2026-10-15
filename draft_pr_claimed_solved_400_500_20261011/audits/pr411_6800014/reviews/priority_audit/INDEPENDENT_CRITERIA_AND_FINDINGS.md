# Independent priority criteria and initial findings

Sealed UTC: 2026-10-13T01:30:50Z. Effort: PR 411 / problem 6800014 only. Completion estimate: 20% of the priority audit; this estimates review completion, not probability of mathematical truth or novelty.

## Independence boundary

Before this seal, I have not opened the author's SOURCE_AUDIT, historical audit, parent MATH_GATE, or peer conclusions. The assignment supplied an accepted mathematical claim and names of potentially material primary sources; these are leads, not evidence of priority. Primary sources inspected independently: Morgan-Pansu Question 14 in its original PDF and TeX; Lauret-Will I arXiv v1 and v2; Lauret-Will II v2; Lauret's dated 2018 talk slides; and arXiv version-history pages. Filename inventory of the current packet was read without opening conclusions.

The first queue parser matched a bare identifier and consequently returned no row. That failed extraction is preserved in INITIAL_SCOPE_REFRESH.json. The corrected exact identifier parser in INITIAL_SCOPE_REFRESH_02.json verified the live row, claimed_solved, Turns 2/5. Neither receipt implies a remote status change.

## Exact claim and acceptance criteria

The target is the literal Question 14 in section 11, printed page 12 of Morgan-Pansu's problems_MTDG PDF: for a given solvable Lie group G, only metrics satisfying Ric = cI + D with D in Der(Lie(G)) should be local maxima of F = scal^2 / |Ric|^2 among left-invariant Riemannian metrics on G. The source imposes neither strict local maximality nor complete solvability. Its definition attaches the derivation to the given group.

The claim under review is a refutation: for every 0 < u < 1/2, the standard metric on the five-dimensional simply connected almost-abelian group with matrix A = J direct-sum uE12 is a non-strict local maximum on the full nearby metric space of that same group, with F = 1/3, but Ric-cI is never a derivation of that group. The claim includes neither novelty of the family nor absence of an isometric Ricci soliton presentation. Scaling and group automorphism invariances must be respected. A Hessian alone or restricted one-parameter maximum does not satisfy the all-nearby-metrics clause. A Ricci soliton isometric to a solvsoliton on another group need not satisfy the source's algebraic definition on G.

Priority acceptance requires a documented, dated, primary-source comparison to this entire claim, plus search coverage and explicit limits. It does not follow from not locating an earlier result. Priority of the actual local-maximality proof must be distinguished from priority of the matrix family, curvature formula, criticality criterion, Ricci-soliton interpretation, and methods.

## Priority classification rules

1. **Exact preexisting resolution / already_solved**: a dated earlier primary artifact supplies a checkable construction and proof of a local maximum outside the literal solvsoliton class for a given group, or a direct theorem yielding it with fully checked assumptions and no new central argument. An equivalent counterexample suffices; exact parameter or matrix identity is unnecessary. Recommend queue status already_solved and scope exclusion immediately if established.
2. **Earlier assertion / announcement**: a dated primary artifact explicitly states existence but gives no checkable construction or proof. This prevents an unqualified first-assertion claim. It does not alone establish a previously checkable resolution, especially if later primary papers explicitly leave the relevant existence question unresolved. Preserve rather than silently resolve contradictory chronology.
3. **Known family or partial ingredient**: earlier D_t, F=1/3, soliton classification, and second-variation formulas establish prior ingredients. They do not establish all-nearby-metric local maximality unless the remaining implication is already proved.
4. **Broader or different result**: global optimization, strictly maximal metrics, real-type groups, Ricci solitons up to isometry, or metrics on another group are compared at their exact quantifiers. Do not transfer conclusions without checking them.
5. **Bounded search with no direct earlier proof located**: this supports only “no checkable earlier proof located in the searched corpus as of the audit date.” It cannot prove novelty, firstness, or current community open status.
6. **Unresolved ambiguity / FINDINGS or BLOCKED**: state the exact missing artifact, logical assumption, or conflicting source. A route that shifts the central difficulty into an unsupported equivalent claim is blocked.

## Initial independent findings

Morgan-Pansu's original statement and definition confirm the group-relative interpretation. Non-strict local maxima satisfy its literal wording. Its reference is Lauret-Will I.

Lauret-Will I v2 was revised 9 May 2019, after v1 submitted 3 August 2018. Its Theorem 1.5(i) asserts local maxima are Ricci solitons, while (ii) characterizes global maxima as solvsolitons. These are different claims. Proposition 6.11 narrows possible local maxima to solvsolitons or a nilsoliton plus commuting skew part. Lemma 6.12 excludes sufficiently large nilpotent coefficient; the text immediately following it leaves small coefficient local maximality unknown. Section 6.4 displays the precise rotation-plus-rank-one-nilpotent family D_t, records F(D_t)=1/3, and uses it for failure of continuous extension, without asserting that D_t is locally maximizing. Thus the family and constant pinching are prior, while the displayed paper does not furnish the positive small-coefficient proof.

Lauret's Sao Paulo slides dated 23 July 2018, slide 13/17 (PDF pages 71-73), explicitly assert existence of Ricci solitons that are local maxima but not global and hence not solvsolitons. No construction or proof appears on that slide. This predates v1 and conflicts with the later paper's explicit unresolved existence statement. The appropriate provisional classification is earlier announcement with conflicting chronology, not evidence of an original first assertion and not automatically a checkable prior proof.

Lauret-Will II v2, revised 27 November 2019, states global-maximality theorems in Theorems 1.1-1.2, each assuming a solvsoliton exists. This is not a theorem ruling out local extrema on the rotation-plus-nilpotent group, which does not admit a solvsoliton. Later literature and the published version remain to be checked.

## Remaining work

Inspect published final versions, author publication pages and later primary papers, follow citation and exact-family search leads, explicitly test direct implications, then read the existing 19-file packet and reconcile every material discrepancy with this sealed assessment. Record actual search queries, failures, dates, and limits. Do not claim independently verified current aggregator wording or status.

