# Adversarial priority audit: PR1071 / problem30002170

Completed 14 October 2026 UTC. Exact submitted head: `fc37aa5169a0fe6adae0a254c9ee6c1531a2911f`. This is an independent priority review of a mathematically accepted claim, not a new mathematical acceptance, human referee report, or publication action.

## Verdict

**Full novelty and historical priority: UNKNOWN. Priority is not cleared.** The bounded fresh search did not locate a read primary theorem that proves the exact optimal conditional lower rate for `1/4<H<1/2`. The Brownian slice is exactly prior; the smooth asymptotic rate is prior; the core localization and Gaussian projection ingredients have clear antecedents. The acceptable promotion route at this checkpoint is a qualified, attributed proof/exposition of the exact result, with no firstness, new-method, worldwide-open, or global-priority claim. A newly found exact prior rough theorem would require credited exposition rather than an independent novelty claim.

This verdict does not undo `ROOT_MATH_ACCEPTANCE.json`. That record proves a mathematical claim under its stated source qualification. Mathematical truth and discovery priority are different questions. Search failure is not evidence of worldwide absence. In particular, inaccessible or incompletely readable method bodies are recorded as UNKNOWN, not dismissed as irrelevant.

There is also a material source-access improvement. A fresh journal-formatted NTU copy from Tindel's institutional publication page was obtained and checked. Its Euler coefficient retains the full distant-lag series and its proof has a different lag cutoff from the pinned arXiv v1. This limits the documented error to the specific arXiv body. Future source notes should incorporate this new access record while preserving all historical records unchanged.

## Frozen scope and exact claim

Before reading earlier priority labels, this review SHA256-pinned112 protected inputs: the existing files in the PR1071 audit tree and the applicable root `AGENTS.md`. Private existing source files were frozen as bytes as well. All nine submitted bodies were completely read and compared byte-for-byte with the previously frozen actual-Git-body copies in `fourier_witness_01/pinned_objects`; all nine agree. The full root mathematical audit, acceptance and current source qualification were read. Both independent derivation families and the detailed source-convergence reconstruction were read. Acceptance banners and earlier bounded-search labels were not treated as priority evidence.

The exact target has independent, centered standard two-dimensional fBm with the same fixed H in `(1/4,1)`, covariance `R_H(s,t)=(s^(2H)+t^(2H)-|s-t|^(2H))/2`, canonical **iterated** integral `X_T=integral_0^T B^1 dB^2`, and the sigma-field of **both complete uniform grids** `B^i_{jT/n}`, `i=1,2`, `j=1,...,n`. For every `T>0`, every integer `n>=1`, and every `F in L2` of that sigma-field, the claim is

    ||X_T-F||_2 >= c_H T^(2H)n^(1/2-2H),

with an explicitly defined positive H-only constant. Taking conditional expectation makes the claim an information lower bound, not merely the error rate of Euler or trapezoid quadrature.

It asserts no sharp constant, exact normalized-error limit, H-uniform positive constant, endpoint result, unequal Hurst indices, correlated components, arbitrary mesh, adaptive information, or arbitrary linear functionals. The original complete two-page [Neuenkirch contribution](https://ems.press/content/serial-article-files/46412?nt=1), OWR41/2012 printed2524-2525, was freshly fetched, read and visually checked. It uses the stated iterated integral and vector-valued conditioning. Its demanded positive lower-rate constant is weaker than an exact limiting constant. Its typography `0<c_H<C_H` can always be met by decreasing a positive lower constant. The fact that the historical report called this a conjecture in2012 establishes no current-open status.

## Search and reading coverage

`QUERY_LEDGER.json` records56 fresh technical searches in14 batches. They cover exact titles and accents/spellings; optimal conditional/mean-square/minimal errors; rough `H<=1/2`; information complexity; later numerical schemes and rate literature; Gaussian quadratic/multilinear information; Cameron-Martin/RKHS/local bump and isonormal routes; periodization/Gram mechanisms; author and institutional sources; and dissertation variants in English and Ukrainian. Selected recent-year queries were additional controls, not a date-based exclusion of older work. The engine aggregated each four-query batch; individual hit attribution is not inferred where unavailable.

Primary technical evidence came from EMS, arXiv author versions, author-uploaded NS text, author institutional journal copies, NUMDAM, Dagstuhl and the Ukrainian dissertation repository. Secondary indexes and generated summaries were used only to identify leads, never to establish a theorem. Several exact/rare searches produced noisy results; those results do not increase confidence by repetition. No citation-graph completeness, language completeness, dissertation completeness or exhaustive database search is claimed.

`SOURCE_LEDGER.json` records source identity, version, access date, read extent, exact implication and UNKNOWN fields. Downloaded bodies, extracted texts, rendered pages and raw web responses remain in this review's ignored `private_sources/`. Public outputs contain authored comparisons and metadata rather than third-party bodies. `FETCH_RECEIPTS*.json` bind the successful and failed accesses. `CHECKABLE_PRIOR_COMPARISONS.md` supplies explicit source-to-target deductions and failed implication tests.

## Primary controls and exact boundaries

| Control | Verified claim and actual comparison | Priority effect |
|---|---|---|
| Neuenkirch OWR2012, printed2524-2525 | Original conditional RMS target; Brownian optimum `T/(2sqrt(n))`; NTU trapezoid upper rate credited | Exact target identified; original historical conjecture only |
| NTU arXiv0902.0497v1 | Analytic canonical-area background and Euler/trapezoid assertions; inspected equation27 onp12 wrongly discards all distant lags | Use root convergence-only qualification; no error attribution to other versions |
| NTU institutional journal-formatted SPA120(2010)223-254 | Theorem1 p225 Euler coefficient `c0+2 sum_{k>=1}c_k`; Theorem2 p226 trapezoid upper bound; same conditional lower bound remains a conjecture | Exact upper/construction background; does not solve rough optimal lower target |
| NS July14,2015 author preprint, uploadedJuly23 | Theorem1 positive liminf/finite limsup for `H>1/2`, same target and information; main proof read in full online | Smooth asymptotic rate is prior; full journal-body bytes still UNKNOWN |
| Shalaiko dissertation2015, defended2016 | Section3.2 pp53-65; explicitly assumes `H>1/2` p54; Theorem3.3 p56 and full area proof pp59-63 match NS | Broad repository language does not supersede rough target; dissertation lead closed at exact theorem scope |
| Neuenkirch Dagstuhl2009 abstract p15 | Announces optimal fractional-area rate for `H>1/2`, including arbitrary linear functionals | Earlier primary announcement of smooth result; details/stronger information theorem UNKNOWN |
| Neuenkirch Dagstuhl2015 contribution3.14 | Describes smooth area optimum and conjectured noncommuting general-SDE order | Historical context, no rough theorem or contemporary open-status inference |
| Deya-Neuenkirch-Tindel journal copy2012 | Theorem1.1 a.s. Hölder approximation bound for a specified Milstein scheme; its sharpness example is first component path interpolation | Different criterion and quantifier; does not lower-bound all estimators of area |
| Friz-Riedel arXiv1108.1099v2 (4May2012), journal2014 | Theorem1 and Corollary1 Gaussian rough-path/Wong-Zakai upper rates | Canonical/convergence control; no conditional lower theorem in inspected claims |
| Huang arXiv2103.11544v1, journal2023 metadata | Theorem1.1 a.s. modified-Milstein upper rate in `(1/4,1/2)` with random constant; introduction distinguishes rough strong-rate question | The word optimal in title is not exact information-lower supersession |
| Liu-Tindel journal2019 copy | Theorem1.2 a.s. rate and weak limiting error for one modified-Euler scheme, rough `1/3<H<1/2` | Nonzero scheme error or a weak limit cannot alone bound optimum |
| Liu-Selk-Tindel journal2023 copy | Theorem3.12 convergence in probability/general partitions and a.s./uniform grid for trapezoid rough integrals | Stronger construction context, no positive information lower rate |
| NS rough-volatility arXiv1606.03854v1 | Rough fOU volatility with Brownian integrators, optimal grid rate `n^(-H)` | Different integrator/functional/exponent; unsupported substitution to two rough fBms |
| Neuenkirch scalar arXiv0706.2636v1 | Scalar smooth-noise SDE optimum `n^(-H-1/2)` or exact recovery | Different noise dimension/commutator and smooth H; no rough area corollary |
| Wu-Xiao author version26Feb2006, Theorem2.1 pp5-6 | Harmonizable local bump/Fourier/Cauchy-Schwarz proof of local nondeterminism | Explicit antecedent of localization idea; no area accumulation rate |
| Xiao2006, Theorem3.1 pp174-175 | Spectral conditions for strong local nondeterminism; first-chaos conditional variance | Established spectral dual-test lineage; no novel generic method claim |
| Dickinson2007, DOI10.1080/07362990701540592 | Publisher abstract concerns Brownian second iterated integral and arbitrary finite Gaussian linear information | Exact Brownian background; complete general statements/proof inaccessible, UNKNOWN |
| Dickinson2024/2025 SSRN5031388 | Author abstract concerns Brownian quadratic finite-Gaussian approximation | Full body unavailable; cannot certify method-equivalence or absence of broader lemmas |
| Jackowski1991, DOI10.1016/0885-064X(91)90047-2 | Primary journal-text OCR discusses Gaussian/product-measure multilinear average-case approximation and central algorithms | Generic projection antecedent; unverified formula/body details and rough-space applicability UNKNOWN |
| Shalaiko-Shevchenko2013/2014, DOI10.1090/S0094-9000-2014-00913-8 | Primary publisher/full PDF access failed; abstract and NS/thesis identify smooth increment lower bound | Independent article body UNKNOWN; no rough extension assumed |

The last method controls are not exact negative theorems. Their UNKNOWN cells are material to any assertion that the whole proof technique is new. The two inaccessible journal bodies already bounded by independently read author/thesis theorems are not silently claimed journal-identical. No theorem in a source was declared globally irrelevant solely because its title differs.

## Mechanism audit and corollary tests

The submitted proof does not invoke a prior optimal-area lower theorem. Its construction consists of smooth local covariance paths, their Fourier-dual isonormal directions, orthogonality to the entire observation vector, a second-chaos product witness, a simultaneous upper Gram bound and an exact deterministic area pairing. The cells are correlated; their vector's independence from the complete grid follows from joint Gaussianity, not from false cell independence. The trace upper bound allows signed off-diagonal covariances.

The choice `phi=x^4(1-x)^4`, `f=phi'`, `g=phi` provides `a=integral(phi')^2=4/45045`. Fourier periodization yields Gram upper bounds independent of n and cell size. The resulting witness has covariance with the target `n a (T/n)^(2H)` and variance at most `n M_f M_g`, hence the required rate. Extending alpha=`2H+1` from `(3/2,2)` to `(3/2,3)` does not alter the mechanism.

Local Fourier bump separation and Gaussian projection are established ideas, as the Wu-Xiao/Xiao controls show. The tensor formulation in `CHECKABLE_PRIOR_COMPARISONS.md` makes the proof a standard test of an unobserved bilinear kernel. What is not provided by those inspected controls is the particular simultaneous invisible family and its quantitative area pairing sufficient for the rough projected-kernel rate. An instruction to apply generic Gaussian projection and then prove the same kernel norm bound simply restates the central difficulty; that route is BLOCKED until an actual quantitative prior estimate is supplied. Conversely, if such an estimate exists in another primary source, changing to the polynomial witness is not proof of theorem novelty.

NS's smooth increment-coercivity proof cannot be extended formally below one half: equal coefficients contradict its necessary lower inequality. The present upper Gram mechanism avoids that obstacle. This establishes a mechanistic distinction from that particular published argument, not from all earlier Gaussian lower-bound methods. No invention claim for the named standard ingredients is appropriate.

Smooth finite-n coverage also does not rescue novelty. A positive asymptotic liminf together with finite-n nonrecoverability yields an all-n constant by taking a finite minimum. The submitted one-cell Fourier test verifies that nonrecoverability without the simultaneous-cell estimate. The new explicit constant is a concrete implementation, with no sharpness or first-explicitness claim. Brownian all-n coverage and exact constant are already prior without this argument.

## New version-specific NTU evidence

The fresh [institutional NTU journal-formatted copy](https://www.math.purdue.edu/~stindel/publication/papers-online/discretize-levy-area.pdf) has32 pages, printed223-254, journal headers and DOI10.1016/j.spa.2009.10.007, received3Feb2009/revised29Sep2009/accepted10Oct2009 dates; 1,211,802bytes; SHA256 `3f7467eea58ebf6998981bf0337a579f45ad1db1c544273eb955507fe2e55c68`. It was obtained14Oct2026 from the author's institutional link. This is a journal-formatted full-body copy, not an assertion that a current publisher-delivered PDF has identical bytes.

Theorem1 p225 explicitly uses `alpha1=c0+2 sum_{k>=1}c_k`. In its proof, pp235-236 separate lags `2<=|i-j|<=log(n)` from lags `|i-j|>log(n)`. Equation29 retains the near-distant-lag contribution; equation30 makes only the tail beyond log(n) little-o. Step5 p237 sums all lags. This directly differs from arXiv v1 equation27 p12, which declares every lag beyond1 negligible. The inspected journal-formatted version therefore does **not** support an attribution of that specific v1 error to the journal proof. Intermediate displayed formulas on p235 have a dropped factor2, corrected in equation29 and the final theorem; this review does not certify every exact coefficient or typographical detail in the journal paper.

The root's independent sufficient convergence derivation remains sound and adequate. For r>=2, c_r is bounded by a constant times `(r-1)^(4H-4)` and lag counts give the three vanishing Euler regimes. The left/polygonal correction also vanishes for H>1/4. The new journal-formatted version supplies independently inspectable area existence Proposition6 p229, the same canonical identification in Remark10, and Theorem2's upper convergence result. Every future publication surface must avoid re-promoting the historical unqualified v1 exact-coefficient endorsement. A new dated source addendum can record this access improvement; previous submissions and acceptance files should not be silently altered.

## Mandatory framing before any promotion

1. The theorem may be stated exactly as proved, with independent equal-H components, both uniform grids and canonical iterated-area convention. Present it as a localized Gaussian-witness proof. Do not label the full interval a first/new discovery.
2. Credit Brownian exact optimum to the original Clark-Cameron lineage as reported by the original source, and smooth optimal asymptotic rate to NS2015/2016. Include the earlier Dagstuhl2009 announcement and Shalaiko thesis where historical discussion warrants it. Do not portray2016 as the earliest demonstrated smooth announcement.
3. If novelty is discussed, use this precise evidence-limited statement: the inspected primary controls did not contain a matching optimal conditional lower theorem for `1/4<H<1/2`; historical priority and worldwide current-open status remain unverified. No wording such as first solution, newly solved open problem, novel general Gaussian method, or priority certified is cleared.
4. Use canonical-area existence and convergence as the external premise; do not endorse the pinned v1's exact coefficients. Incorporate the newly fetched journal-formatted body's correct lag-series distinction in an authored source note. No journal error follows from the v1 defect.
5. No stronger endpoints, adaptive/arbitrary sampling, correlated components, sharp constant, limiting law, exact normalized limit or H-uniform estimate may enter the abstract, supplement, metadata, PR description or public status text.
6. If later primary evidence matches the rough theorem or supplies a checkable corollary with the same assumptions, reclassify the affected claim as credited exposition. If a critical full body remains unreadable, keep its applicability UNKNOWN and do not clear methodological or theorem priority by exclusion.

These are factual framing restrictions, not a request for user confirmation. Nothing was submitted, published or sent to another individual. An external expert could help locate unpublished or poorly indexed precedents; that possible benefit is recorded only, with no outreach prepared or initiated.

## Custody, residual gaps and completion

All protected inputs remain byte-identical at the final recheck. No source/proof/status/acceptance record was edited. The review wrote only its new `reviews/priority_01` directory. A read-only workspace Git status was obtained at entry; no Git mutation, service operation, publication, external correspondence or other-shard contact occurred. Copyright source bodies remain ignored/private. Output hashes and a final seal bind the authored report and ledgers.

This bounded priority audit's requested work is complete. Completion estimate for the **audit execution** is100%; completion of **historical priority clearance** remains below100% and is not inferred from search count. The strongest verified priority findings are the exact Brownian supersession, smooth prior theorem/announcement, lack of a matching rough theorem among the read controls, and the version-specific NTU correction. Remaining gaps are unindexed/other-language or unpublished precedents, unread method-body generalities, exact source-to-rough-space implications, and journal-byte identity where only author copies were read. The mathematical result remains the root's accepted theorem; the promotion classification is qualified proof/exposition with full novelty UNKNOWN.
