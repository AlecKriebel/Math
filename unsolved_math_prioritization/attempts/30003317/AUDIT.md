# Complete independent audit of the corrected partial reductions

Problem 30003317 / OWR-15181-008. The original question remains unresolved by this work.

AI-assisted, unrefereed authored mathematics with an independent internal AI audit. This is not external human peer review or formal proof-assistant certification.

Only authored mathematical prose, the exact correction, acceptance records and public verification metadata are distributed. No executable code, raw datasets, copied source documents, extracted source text, source images, raw search responses or private coordination material are included. This is not a computational reproduction package.

## Historical decision and current disposition

The original audit is reproduced verbatim below, with all mathematical arguments and its conditional acceptance preserved. Its instructions to apply LEMMA2_SCOPE.patch concern the original unpatched proof. That exact one-line patch has now been applied to the separate proof copy in PROOF.md; ACCEPTANCE.md reproduces the patch and the complete original patch notes. The immutable original proof and audit are unchanged.

The audit's detailed arguments about arbitrary summable families, class pressing down, set-valued ordinal recursion, monomial descent and inverse-automorphism summability remain part of the accepted reasoning. No original audit section, proof, counterexample or limitation is omitted. Published structural dependencies remain dependencies; acceptance does not claim a complete independent re-proof of those sources, novelty, a uniqueness theorem or a nonuniqueness construction.

## Original independent audit, unchanged

# Independent audit: fixed-restriction surreal derivations

Target: Oberwolfach Report 60/2016, Question 8, ID 30003317. Audit date: 2026-10-11 UTC.

## Verdict

**Accept the partial reductions after the single required wording correction in Lemma 2. Do not accept a solution of the original problem.** No existence of two distinct extensions, uniqueness of extension, or novelty of these reductions has been established.

The audited text is `REDUCTIONS.md`, SHA-256 `9d446a6b3bf7c37c6e09b037962ab9cf8f5c152cd8507a6567b782b924fb7be8`, 21,310 bytes. Its containing manifest has SHA-256 `eb92c5378347a3d5cd6d777fb71fdefc20aed2310276eb63a62f1dbd17ba9dcf`. The original was preserved unchanged. The accompanying exact one-line patch changes only Lemma 2's hypothesis; this audit's supplementary arguments make explicit why no stronger foundational or summability assumption is needed elsewhere.

The required correction replaces “not asymptotic in magnitude to 1” by the explicit condition that the absolute value is infinite or infinitesimal. The present text defines asymptotic equivalence by equality of leading terms. On that reading the old wording includes 2 and is false: take a=2 and b=1/ω. Then b≺a and D(a)=0, whereas D(b)=-D(ω)/ω² is nonzero. The corrected hypothesis is exactly the one the proof establishes and every subsequent use requires. If the old phrase was intended to mean “not Archimedean-equivalent to 1,” the correction still removes a material ambiguity without altering the intended result.

No additional substantive error was found in Theorems 3, 4, 6, 9 or the remaining lemmas and corollary, with the published structural inputs identified below. In particular:

- the monomial criterion includes full preservation of summability and not just a formal identity;
- its smallness hypothesis extends from individual monomials to every non-real surreal;
- the transfinite integration proof uses set-valued recursion available in NBG with global choice;
- no sum indexed by a proper class is formed;
- the parametrized family does not purport to be a class whose members are class functions;
- the automorphism results are not derivation-uniqueness theorems.

## 1. Exact problem and scope

The target asks for distinct surreal derivations on all of No agreeing on K=R⟨⟨L⟩⟩, the full field closed under exp, positive log, and summable set-indexed sums. Agreement on the ordinary field R(L) is not an adequate substitute. Surjectivity is a conclusion in one part of the argument, not an extra requirement inserted into the definition of a surreal derivation.

The target and its historical formulation were independently checked against Question 8 on printed p.3316 and the report on printed pp.3339–3341 of [OWR](https://ems.press/content/serial-article-files/46663). The historical survey passages agree with this interpretation. Their statements about what was open in 2016 or 2020 do not certify present-day openness.

The partial results are conditional structural statements about an arbitrary fixed surreal derivation D. Failure to find a nonzero perturbation of the canonical derivation alone would not prove uniqueness for every possible restriction to L. This distinction is preserved correctly in the audited text.

## 2. Independently checked mathematical dependencies

The principal source is Berarducci–Mantova, [Surreal numbers, derivations and transseries, arXiv v3](https://arxiv.org/abs/1503.00315v3), subsequently JEMS 20 (2018), 339–390. The checked inputs are normal-form summability, finite termination of the dominant path, the canonical path-sum construction, its preservation of K, and T4. The cited locations are Definitions 2.9 and 6.13, Proposition 2.13, Corollary 5.11, Definition 6.22 and Lemma 6.23, Theorem 6.30 and Remark 6.31, and Theorem 8.10. Lemma 7.5 and Proposition 7.6 supply the model for the integration argument. These are genuine source results with the stated scope.

The dominant-path termination input is especially important: it is a fact about the underlying exponential series structure, not an assertion that all derivations use the canonical path-sum recipe. The proof of Theorem 3 legitimately combines this structural fact with the differential axioms for any D.

The selected source passages were read independently, and key formulas on BM PDF pp.31, 35, and 40 were checked visually against newly rendered pages. This audit does **not** independently reconstruct the whole nested-truncation theory or all the foundational work behind the canonical derivation. The deductions below are accepted relative to those explicitly identified published inputs.

For later literature, [Kaplan–Krapp–Serra, arXiv:2509.22374v3](https://arxiv.org/abs/2509.22374v3), Proposition 5.2 on PDF p.10, states rigidity for strongly R-linear exponential-field 1-automorphisms. Its proof and the class-theoretic conventions were inspected. [Bagayoko, arXiv:2409.16251v2](https://arxiv.org/abs/2409.16251), Definition 3.6, Proposition 5.9 and Theorem 6.3 concern structured, monomial-preserving embeddings with additional hypotheses. Neither inspected result asserts uniqueness of surreal derivations with a fixed restriction to K. Full proofs of the embedding machinery and of the separate general Lie correspondence were not audited or required for the elementary obstruction lemmas below.

## 3. Agreement closure: Lemma 1

**Accepted.** For a summable family, both derivative-image families are summable. Their finite union still has reverse well-ordered support and finite multiplicities, so their termwise difference is summable. Thus E=D1-D0 is strongly additive in the full sense.

The zero class of E is a field because E is a derivation. Exponential compatibility makes it closed under exp and under log of positive elements. Strong additivity makes it closed under all the relevant set-indexed sums. It contains R and L, hence K. No construction by finitely many operations and no claim that K is a set appears here.

The use of the existing class K is legitimate. It can also be recognized by the path characterization in BM Proposition 8.2; no new intersection over a hypothetical class of all subclasses of No is required in this argument.

## 4. Dominance and the finite dominant path: Lemma 2 and Theorem 3

**Lemma 2 requires the one-line scope correction. Theorem 3 is accepted after that correction.**

If |a| is infinite, the positivity axiom applied to a+tb, after adjusting the sign of a, proves the smallness implication. If |a| is positive infinitesimal, the inverse of a+tb is positive infinite; its derivative has sign opposite to D(a)+tD(b). Varying real t proves the same absolute-value inequality. This includes the case D(b)=0. Applying the result to b-a proves preservation of asymptotic equivalence when a has the corrected scope.

For any non-real x, removing the real coefficient leaves a nonzero u whose leading monomial is not 1. Hence |u| and the absolute value of its leading term are either infinite or infinitesimal. Along the subsequent dominant path, log(m_i) is a nonzero purely infinite number. Its leading term is infinite in magnitude. These are precisely the hypotheses of the corrected lemma.

The source's leading-term logarithm ℓ(rm)=log(m) agrees with “log|rm| after removing its real coefficient,” because log|rm|=log|r|+log(m). Therefore the manuscript uses the same dominant path as the cited source. That path enters L after finitely many steps even when the initial term is negative or infinitesimal.

At every step the quantities being compared are nonzero, since the path terms and nonzero purely infinite logarithms are non-real. Multiplying by a nonzero q_i preserves asymptotic equivalence. Only finitely many such comparisons are multiplied, so no infinite product or limit argument is hidden. The resulting expression has the same value for both derivations once the terminal term is in L.

The conclusion is equality of derivative leading terms, not equality of derivatives. Agreement of the leading monomial alone would be weaker; the argument also retains the leading real coefficient.

### Complete downstream scope check for Lemma 2

1. Theorem 3 uses u and a non-real leading term, then nonzero purely infinite logarithms and their leading terms.
2. Theorem 6 removes the real coefficient before choosing m0; every monomial to which the lemma is applied is distinct from 1.
3. Lemma 8 chooses an asymptotic integral, removes its real coefficient, and retains a term rm with m≠1.
4. All comparisons between integration terms in Lemma 8 involve such nonconstant monomials. Equal monomials are handled by real proportionality rather than by the strict-dominance implication.
5. The other lemmas use Theorem 3 or Lemma 8, not an additional application at a finite appreciable argument.

Thus the required correction does not retract any downstream conclusion.

## 5. Affine perturbations and the proper-class family: Theorem 4 and Corollary 5

**Accepted.** Necessity follows from subtraction and leading-term rigidity. Sufficiency uses the strict relative-smallness condition to preserve both the nonzero derivative of every non-real input and its sign on positive infinite inputs. This proves the constant-field and positivity axioms rather than assuming them.

Multiplying a derivation E by a fixed field element c does preserve Leibniz and exponential compatibility. One does not differentiate c in this assertion: the operator is x↦cE(x), and the product rule is checked at the input x. Multiplication by c also preserves every summable family. If c is finite, multiplying an infinitesimal relative error by c keeps it infinitesimal, so cE remains admissible. No assertion about arbitrary infinite c is needed.

The map z↦z/(1+|z|) is injective: on nonnegative inputs its inverse on the image is c↦c/(1-c), and on negative inputs it is c↦c/(1+c); signs distinguish the two images. Each image lies in (-1,1). Evaluation at one a with E(a)≠0 separates the resulting derivations.

NBG supports the single class graph F(z,x)=D(x)+[z/(1+|z|)]E(x), since all arguments and values are sets and the definition uses existing class parameters. It does not require the class-sized derivations themselves to be elements of another class. The advertised family consequence is therefore appropriately formulated.

## 6. The exact monomial criterion: Theorem 6

**Accepted.** Conditions W, F, L0 and B are necessary and sufficient as stated, relative to the corrected dominance lemma. The condition W is essential; dropping it would invalidate the theorem.

### Necessity

For E=D'-D, apply full strong additivity to each summable family of distinct monomials in a reverse well-ordered set S. This gives W for w(m)=E(m). Exponential compatibility gives E(m)/m=E(log m), and strong additivity expands the latter into F. The restriction and leading-term results give L0 and B. If c vanished on all monomials, strong additivity on each normal form would force E=0 everywhere.

### Sufficiency: all summable families

Define E by the stated normal-form formula. For a summable family (x_i), let S be the union of its input supports. Fix an output monomial p. By W, only finitely many m∈S have p in supp(w(m)). For each such m, the original family has only finitely many i with a nonzero coefficient at m. Consequently only finitely many pairs (i,m) contribute at p.

The union of the expanded output supports is contained in the reverse well-ordered union provided by W. Real scalar coefficients cannot add new support monomials. Therefore the doubly indexed expanded family is genuinely summable. Regrouping first by i or first by m gives full strong additivity and R-linearity. This argument handles finite repetitions of individual input monomials without requiring a uniform bound on their repetition counts.

### Sufficiency: Leibniz and exponential compatibility

Equation F gives c(m)=E(log m). Additivity and log(mn)=log m+log n give c(mn)=c(m)+c(n), hence the monomial product rule. For arbitrary x and y, the family of normal-form pairwise products is summable. Applying the already established strong additivity of E is legitimate. The terms obtained on the other side are summable as products of two summable families: normal-form terms of one input and E-images of the other's terms. Hahn product summability gives both reverse well-ordering and finite multiplicities. This proves the full product rule.

For γ∈J, exp γ is a monomial and F gives the exponential rule directly. F at 1 gives c(1)=0, so E annihilates R. For infinitesimal ε, the exponential power series is summable. Strong additivity and the product rule identify its image with E(ε) times the differentiated scalar power series. The shifted power series is summable, and multiplication by the single surreal E(ε) is legitimate. Decomposition x=γ+r+ε proves exponential compatibility on all of No.

### Sufficiency: the bound on every non-real input

Let r0m0 be the leading term after removing x's real coefficient, and let δ be the leading monomial of D(m0). For m=m0, B puts every support monomial of E(m) strictly below δ. For any remaining m<m0, with m≠1, strict monomial order means m≺m0; the corrected Lemma 2 gives D(m)≺D(m0), and B gives E(m)≺D(m). Therefore all support monomials in every summand r_m E(m) lie strictly below δ. The monomial 1 contributes zero.

By W this family has a reverse well-ordered union. A sum cannot acquire a monomial absent from that union. If its sum is nonzero, its largest support monomial is still strictly below δ; if it is zero the bound is automatic. Thus E(x)≺D(m0), and D(x)∼r0D(m0) gives E(x)≺D(x).

There is no requirement to find a common positive gap below δ or to exchange an order-topological limit with a derivative. The support argument is what makes the pointwise monomial bounds sufficient.

## 7. Class pressing down and asymptotic integration: Lemmas 7–8

**Accepted in NBG with global choice.** This is set-valued class recursion, not a use of a stronger principle that recursively constructs an arbitrary class at each stage.

### Lemma 7

Under the contrary assumption, every fiber is a set. For a set of indices β≤g(α), class replacement collects their set fibers into a set, and their union has an ordinal supremum. Thus each successor value of g exists as a set ordinal. At a limit stage, the preceding values also form a set. The continuous, strictly increasing g with g(0)=1 exists by ordinary set-valued recursion.

The sequence 1,g(1),g²(1),... is strictly increasing, and its supremum α is a nonzero limit ordinal. Continuity gives g(α)=α. For β=f(α)<α, choose ξ<α with β≤g(ξ); for example g(ξ)≥ξ ensures sufficient cofinality. Then ξ+1<α. The successor requirement implies α<g(ξ+1), whereas strict increase gives g(ξ+1)<g(α)=α. This is the required contradiction. The initial offset g(0)=1 prevents a vacuous fixed point at 0.

### Selecting asymptotic integral terms

For each nonzero f, the witness class is nonempty by assumption. There is a least birthday at which a witness exists, and the surreals of that birthday form a set. Global choice selects a witness from this nonempty set. The witness-selector graph is definable with set quantifiers and existing class parameters. Removing the real coefficient and taking the leading term gives the class function A(f) required in the proof.

This does not assume a choice function on an arbitrary collection of proper classes.

### Existence of the recursion

One may totalize the step rule by returning a distinguished stop symbol once the residual is zero, and also on any malformed sequence. Given a set sequence s of length α, the valid step is computed from its set-indexed terms, their D-images, the residual, and A. It produces a single set, not a new proper class. Its graph is an elementary class definition using D and A as class parameters.

For every set ordinal θ, ordinary transfinite recursion yields a unique sequence of length θ following this rule. Those sequences agree on overlaps by induction. Define the global recursion graph by saying that a pair occurs in one such set-length sequence. This is elementary class comprehension, since the quantified sequences and ordinals are sets. Class replacement supplies each initial segment and its images when they are used. Nothing here asks for a truth predicate or a class-valued solution of an elementary transfinite recursion scheme.

The same justification applies to the g-recursion in Lemma 7. The construction may therefore be carried out in the stated NBG theory.

### Summability at limit stages is not circular

Assume all earlier integration terms have strictly decreasing monomials. Their union is reverse well ordered: a nonempty subset of indices has a least index, which supplies its largest monomial. There are no repeated monomials. Hence the family of earlier terms is summable before any assertion is made about the next term. Strong additivity of D then supplies summability of their image family and its tails.

For a fixed earlier γ, both Rγ-D(tγ) and the tail of D(tβ) for γ<β<α have support strictly below the leading monomial of D(tγ). The first bound comes from asymptotic integration. The second follows from already established derivative dominance and summability. Therefore Rα≺D(tγ), including when α is a limit. If the recursion has not stopped, D(tα)∼Rα gives D(tα)≺D(tγ).

### Why decreasing derivatives force decreasing terms

Write tα=r m and tγ=s n, where r,s are nonzero reals and m,n≠1. There are three possibilities.

1. If m=n, then D(tα)=(r/s)D(tγ), so their derivatives have the same nonzero Archimedean magnitude. This contradicts strict derivative smallness.
2. If m>n, then tγ≺tα. The corrected Lemma 2, applied with a=tα, gives D(tγ)≺D(tα), again a contradiction.
3. Therefore m<n, equivalently tα≺tγ.

This argument does not use an invalid converse of Lemma 2 for arbitrary surreals. It uses comparability of monomials and real proportionality in the equal-monomial case.

### Termination and proper-class issues

If the recursion never stopped, the residual leading monomials mα would form an injective class sequence. For α>0, mα lies in the original support or in the support of an earlier derivative. The manuscript's S0 includes the original support and the initial derivative support, so the least support index h(α) is genuinely less than α. There is no attempt to define a regressive value at α=0.

Lemma 7 gives a proper-class fiber. The image of this fiber under the injective map α↦mα is contained in one set support Sβ. Such an injection from a proper class into a set is impossible in NBG: its inverse on the image, together with replacement, would make the original fiber a set. Thus the process stops at some ordinal stage. Only the terms before that set ordinal are summed to obtain an actual integral.

## 8. Surjectivity invariance: Theorem 9

**Accepted.** A preimage y of nonzero f under a surjective D0 is non-real, so leading-term rigidity applies and gives D1(y)∼f. Hence D1 has asymptotic integration and Lemma 8 proves its surjectivity. The argument is symmetric. The canonical consequence uses the published surjectivity of the canonical derivation; it does not identify any other extension with it.

## 9. Active paths and local boundary data: Lemmas 10–11

**Accepted with the stated limitations.** A nonzero differentiated sum has at least one summand with nonzero derivative. After choosing such a normal-form term, exponential compatibility propagates nonzeroness into the logarithm, allowing another term to be chosen. The reverse well order supplies a first eligible term. The resulting countable path cannot enter L. T4 gives eventual coefficient ±1 and absence of terms to the right, not eventual entry into L.

For a fixed initial surreal, the finite-path tree is a set: each level is obtained from the preceding set of terms by taking set supports, and the levels are collected over ω. Infinite paths lie in a set of sequences. Thus the path manipulations do not introduce a proper-class summation index.

The cut in Lemma 11 has a set of right options b_i/k. All are positive, so it supplies c>0 smaller than each of them. For the displayed recurrence, A_n is a finite nonzero product and d_n=c/A_n satisfies both the equations and all stated bounds. This is a consistent formal chain, not a constructed derivation. A compatibility requirement over every well-based support remains absent, exactly as the manuscript says.

## 10. Valuation contraction and conjugation: Lemmas 12–13

**Accepted.** Lemma 12 does not need strong additivity. Exponential compatibility and contraction at exp(x) force E(x)≺1 for every x. If d=E(a)≠0, then b=1/d is infinite in magnitude. Setting ε=E(ab) gives aE(b)=-1+ε, and E(ab²)=b(-1+2ε) is infinite, contradicting the bounded-image conclusion. This is an elementary obstruction independent of the separate KKS Lie-correspondence dependency.

For Lemma 13, an R-fixing field automorphism of No preserves order because positive elements are precisely nonzero squares. If it maps M onto M, the induced map of monomials is an order isomorphism. Its inverse preserves reverse well-ordered set supports and coefficient multiplicities. For y=Σ r_n n, applying σ to Σ r_n σ⁻¹(n) gives y, so σ⁻¹ also acts termwise on normal forms and is strongly R-linear. Thus the inverse-preservation assertion used for the path bijection follows from the stated hypotheses rather than needing an extra hypothesis.

Fixing R and L and preserving the defining operations fixes K. The canonical values at L lie in K, hence are fixed. The monomial order isomorphism and exp compatibility identify the path sets in both directions. Entering L is preserved in both directions because L is fixed pointwise. The finite path products transform correctly, and paths never entering L have zero canonical path derivative on both sides. Strong additivity applies to the summable path-derivative family, proving commutation.

The monomial-preserving hypothesis is used essentially. No claim about conjugation by every exponential-field automorphism follows. Nor does the fact that all fixed-restriction derivations have identical leading terms produce a leading-term-preserving automorphism to which KKS Proposition 5.2 could automatically be applied.

## 11. Required action and unresolved gap

Apply the exact Lemma 2 patch. The supplementary explanations in Sections 6–7 and 10 of this audit are mathematically useful additions, but the audit found no missing assumption requiring a second substantive patch.

The corrected text may be described as independently audited **partial reductions and obstructions**, relative to the named published structural inputs. It must not be described as an accepted solution, a uniqueness proof, a nonuniqueness construction, or a proof that the question remains open in the entire current literature.

The remaining mathematical requirement is still a nonzero global monomial datum satisfying W, F, L0 and B for some surreal derivation D, or a proof that every such datum is zero for every D. The audit supplies neither. Its bounded later-literature check found no exact resolution in the inspected sources; that is a search limitation, not a mathematical theorem.

## Historical authored literature screen, unchanged

The following complete original literature screen records the earlier bounded inspection. Dates and statements about current versions refer to that inspection on 2026-10-11, not a new scholarly-source inspection during editorial preparation. No source contents are reproduced.

# Literature screen and source applicability

Checked on 2026-10-11 UTC. Searches were bounded and topic-specific, not exhaustive. Search snippets were used only as leads; mathematical reliance is on the primary sources identified below.

## Exact target and historical status

- Oberwolfach Report 60/2016, printed p.3316, Question 8 (PDF p.4), asks for distinct surreal derivations with the same restriction to R⟨⟨L⟩⟩. Printed pp.3339–3341 (PDF pp.27–29) explain the derivation axioms and distinguish choices on L from different extensions of one fixed choice. Primary source: https://ems.press/content/serial-article-files/46663.
- Berarducci–Mantova, arXiv:1503.00315v3, is the construction paper. Its path-sum recipe sets nonterminating path derivatives to zero. Existence of this recipe is not a uniqueness assertion. Primary source: https://arxiv.org/abs/1503.00315.
- Mantova–Matusinski, arXiv:1608.03413v2, pp.21–22 (repository PDF pp.22–23), explicitly leaves open the possibility of multiple extensions beyond K. Primary repository copy: https://eprints.whiterose.ac.uk/123644/1/1608.03413v2.pdf.
- Berarducci, arXiv:2008.06878, Theorem 24.2, PDF p.20, describes the canonical-restriction extension as possibly nonunique. Remark 24.7 changes the L-data, so it is not a solution of the fixed-restriction problem. Primary source: https://arxiv.org/abs/2008.06878.

These statements document what those sources say; the 2020 statement is not by itself evidence that no later resolution exists.

## Later primary sources inspected

### Bagayoko, Hyperseries subfields of surreal numbers

https://arxiv.org/abs/2409.16251, current landing page reports v2, revised 2024-10-04. Whole v2 PDF retrieved: https://arxiv.org/pdf/2409.16251v2.

Inspected the introduction, embedding definitions, and the relevant nested-extension/embedding statements and proof passages, especially Definition 3.6, Proposition 5.9, Theorem 6.3, and Section 6.3. These provide structured, monomial-preserving embeddings. They do not state that two derivations agree on all L while differing elsewhere. The naturality argument in REDUCTIONS.md explains why monomial-preserving conjugation of the canonical derivation, when the automorphism fixes L, leaves that derivation unchanged.

The author research page was also checked for later work: https://vincentbagayoko.neocities.org/research/research_en. It lists the 2024 manuscript, a 2025 Taylor-expansion manuscript, and a 2026 formal Lie-correspondence manuscript. A personal publication list is not an exhaustive literature index.

### Kaplan–Krapp–Serra, Decomposing the automorphism group of the surreal numbers

https://arxiv.org/abs/2509.22374. The current landing page reports v3, revised 2026-04-23. Whole v3 PDF retrieved: https://arxiv.org/pdf/2509.22374v3.

Inspected the class-theoretic conventions, Section 4's contraction correspondence statement, and Proposition 5.2 with its proof on PDF p.10. The proposition rules out a nontrivial strongly R-linear exponential-field automorphism preserving each leading term. It is an automorphism rigidity result, not an answer to the fixed-derivation-extension question. Its supporting general Lie correspondence was not fully audited here. The author's page listed the paper as to appear in the DDG40 proceedings when checked: https://elliotakaplan.github.io/.

An initial web result led to a v1 HTML endpoint whose displayed internal date was inconsistent with its version label. The mathematical reliance and local PDF hash were therefore pinned to the current v3 PDF, not that endpoint. No arXiv revision date was inferred from a search engine's crawl/publish label.

### Bagayoko–Mantova, Taylor expansions over generalised power series

https://arxiv.org/abs/2509.08473, v1 submitted 2025-09-10. Inspected the abstract, introduction, theorem statements, and Section 5.3 discussion through https://arxiv.org/html/2509.08473v1. The work starts with a given derivation and gives Taylor summability/expansion results, including applications involving the canonical surreal derivation. No exact fixed-restriction nonuniqueness or uniqueness theorem was found in those inspected portions. No whole PDF was retrieved and no full proof audit was done.

### Bagayoko, A formal Lie correspondence

https://arxiv.org/abs/2604.04224, submitted 2026-04-05. Abstract/metadata only were inspected. This is a formal nilpotent Lie/exponential-group correspondence, not an abstract statement resolving the present question. No conclusion about all its internal results is claimed.

## Search coverage

Queries included combinations of:

- surreal derivations / same restriction / log-atomic / unique extension;
- surreal derivation / nonuniqueness / fixed / extensions;
- surreal derivations / Bagayoko / automorphisms / hyperseries;
- arXiv:1503.00315 / corrigendum / erratum;
- topic searches with 2024, 2025, 2026 or an after-2020 filter.

The exact-topic searches repeatedly returned the original OWR question and historical surveys. The broader searches located the later papers above. No applicable correction or exact later resolution was located. This negative result is explicitly bounded by the searched terms, available indexes, and inspected sections.

## Excluded shortcuts

- Multiple derivations obtained by changing the prederivation on L do not answer the question.
- Ordinary differential-field universality or isomorphism statements need not respect strong summation or exp and need not fix K pointwise.
- A theorem about set-sized homogeneous structures cannot be invoked over the proper-class base K without an additional argument.
- Nontrivial automorphisms of the ordered field or exponential field need not preserve summability. Monomial-preserving automorphisms fixing L face the separate naturality obstruction proved in the artifact.
- Surjectivity is neither silently assumed nor discarded: the artifact proves that it is an invariant of the fixed-restriction family.
