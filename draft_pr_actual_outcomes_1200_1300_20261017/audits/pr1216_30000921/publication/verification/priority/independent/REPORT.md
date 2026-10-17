# Independent priority audit: PR1216 / problem 30000921

Audit date: **17 October 2026**. This report was prepared independently of the other priority family. It is a literature/implication audit, not a paper, publication, or historical-priority certificate.

## Verdict

**Do not promote either the submitted negative answer or the proposed dense simultaneous-counterexample theorem as a first resolution or a new existence theorem.** There is positive, checkable prior overlap: Nikula's random-function theorem, available as arXiv:1209.6209v1 (repository submission 27 September 2012; journal publication online 8 October 2013, issue 2014), has an elementary corollary giving a dense family of **frequently** differentiation-hypercyclic entire functions \(f\) satisfying
\[
\forall p\in\mathbb C[z]\setminus\mathbb C,\qquad |(pf)^{(n)}(0)|\to\infty.
\]
The exact proposed relative annular-space conclusion also follows after an elementary coefficient-clipping argument. The complete implication, including full support and density, has passed an independently assigned adversarial verification in [verification/VERIFICATION.md](verification/VERIFICATION.md).

This is a **deduction from an earlier theorem**, reconstructed during this audit. I did **not** locate a source explicitly saying that Nikula's theorem answers Costakis Question 5, and I do not attribute that explicit multiplier statement to Nikula. The first date on which somebody expressly stated or published the negative answer remains **unestablished**. Absence of an exact search hit does not establish that nobody did.

The original question is authenticated. Its description as open in 2008 is historically supported; its description as still open in 2026 is **not supported** by this audit. The positive prior implication already defeats treating the mathematical existence conclusion as a new resolution.

## 1. Claims and comparison rules

Let \(D f=f'\) on \(H(\mathbb C)\) with the compact-open topology. The submitted conclusions are:

1. Some \(f\in HC(D)\) has \(zf\notin HC(D)\).
2. For each fixed nonconstant \(p\), failures \(f\in HC(D)\), \(pf\notin HC(D)\) are dense in \(H(\mathbb C)\).
3. More locally, for every fixed \(p\), every given \(f\in HC(D)\), and every neighborhood of \(f\), there is such a failure \(F=f+h\) in the neighborhood with \(D^nh\to0\).
4. The only polynomial pointwise multipliers preserving **every** \(D\)-hypercyclic entire function are nonzero constants.

The separate source-question reconstruction proposes a stronger common family failing every nonconstant \(p\), with escaping scalar derivative evaluations, and relative Baire arguments in
\[
X_M=\{f:(n+1)^{-1/2}\le |f^{(n)}(0)|\le\log(n+e)\ \ (n\ge M)\}.
\]
I read its immutable reconstruction only to define this comparison target. I did not use it as evidence of historical novelty or mathematical clearance.

An earlier theorem need not contain the same formula or construction to overlap: a transparent implication establishing the same conclusion matters. Conversely, \(p(z)f(z)\), \(P(f(z))\), \(p(D)f\), scalar-weighted orbits \(n^bD^nf\), and translation orbits must be kept separate. Existential or residual selected families do not imply preservation for every hypercyclic input.

## 2. Original-source authentication

Freshly retrieved the whole [EMS report](https://ems.press/content/serial-article-files/46147), SHA-256
\[
\texttt{9bd27d84931841479eaf5e0915e4a99e720c4c135a7d57c97dff43e4687d03a5}.
\]
Read the Costakis contribution on PDF pp. 32–35; visually inspected PDF p. 34 / printed p. 330. Definition 4 uses the full derivative orbit. Question 5 asks the pointwise product question for an arbitrary \(f\in HC(D)\) and nonconstant polynomial. The same page's Theorem 6 asserts a residual family whose members work with all nonzero polynomial multipliers. That is compatible with dense exceptional families.

Crossref independently binds [DOI 10.4171/OWR/2008/06](https://doi.org/10.4171/OWR/2008/06) to the **whole** workshop report, *Oberwolfach Reports* **5**, issue 1 (2008), pp. 297–346. “Report 6/2008” is the report number, not journal volume 6. The contribution occupies printed pp. 328–331. This corrects a possible bibliographic ambiguity in secondary citations; it does not change the target.

Costakis cites a preprint of *Common Cesàro hypercyclic vectors* for Theorem 6. Freshly retrieved its [2010 publisher PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/90964), read the introduction/main statements and Section 6 plus references. Theorem 1.7 gives a residual common family for the sequences \((n^bD^n)\), over all real \(b\); Sections 6.1–6.2 prove positive/negative \(b\) cases. These generic conclusions do not assert universal pointwise preservation or explicitly give the required negative answer.

Freshly retrieved and read all 12 pages of the [2018 JOT paper](https://jot.theta.ro/jot/archive/2018-080-001/2018-080-001-011.pdf), including its final theorem and added-in-proofs note. Its groups of selected hypercyclic functions, powers/composition \(P\circ f\), convolution operators, and composition-operator products do not settle this universal pointwise question. Its references supply productive trails to Shkarin's algebra/subspace theorem and to the probabilistic/growth literature, but the paper's wording about multiplicative stability must not be substituted for the exact Question 5.

## 3. Decisive prior implication: Nikula

### Source identity and dated support

[Official version record](https://arxiv.org/abs/1209.6209v1): v1 submitted **2012-09-27 12:45:47 UTC**; only one version listed. Freshly downloaded the [version-specific PDF](https://arxiv.org/pdf/1209.6209v1). Its 14-page text was read, with close inspection and visual confirmation of Theorem 1 on PDF pp. 2–3; the standard complex Gaussian example is explicitly discussed on p. 10. The [publisher record](https://link.springer.com/article/10.1007/s11785-013-0328-0) independently gives online publication **8 October 2013**, volume 8 (2014), pp. 1455–1474. Journal body access was subscription-only; theorem numbering here refers to the inspected arXiv version.

Theorem 1 concerns IID coefficients with law supported on all of \(\mathbb C\) and
\[
\limsup_{r\to\infty}(\log r)^{1+\beta}\Pr(|X|\ge r)<\infty
\quad\text{for some }\beta>0.
\]
It gives almost sure entire convergence and frequent \(D\)-hypercyclicity for
\(F(z)=\sum X_nz^n/n!\).

**Provenance qualification:** the currently served v1 PDF has an internal “Date: August 2, 2018” line and PDF creation metadata in November 2018, alongside its 2012 arXiv margin/version and the official 2012 version history. An automatic recompilation is plausible but was not authenticated from an original source archive or a contemporaneous byte copy. This audit authenticates the present version-specific source and repository history, not byte-identical 2012 PDF contents. Independent journal metadata confirms publication before this project, so this qualification cannot rescue a 2026 novelty claim. Do not silently call the internal date a verified compilation date.

### Checkable Gaussian corollary

Use independent standard **complex** Gaussians with density \(\pi^{-1}e^{-|z|^2}\), not real Gaussians. This law has full-plane support and satisfies the theorem's tail condition. For any \(1/2<\alpha<1\), in particular \(\alpha=3/4\),
\[
\Pr(|X_n|<(n+1)^{-\alpha})\le(n+1)^{-2\alpha},
\qquad
\Pr(|X_n|>\log(n+e))=e^{-\log^2(n+e)}.
\]
Both sums converge. Borel–Cantelli gives a **single** probability-one event on which, eventually,
\[
(n+1)^{-\alpha}\le |X_n|\le\log(n+e).
\]
Intersect it with the probability-one event in Nikula's theorem.

On any resulting sample path, fix an arbitrary polynomial
\(p(z)=\sum_{j=0}^dc_jz^j\), \(d\ge1\), \(c_d\ne0\). The exact identity is
\[
(pF)^{(n)}(0)=\sum_{j=0}^dc_j(n)_jX_{n-j}.
\]
The leading contribution has size at least a positive \(p\)-dependent constant times \(n^{d-\alpha}\), and the sum of all lower-degree contributions is \(O_p(n^{d-1}\log n)=o(n^{d-\alpha})\). The reverse triangle inequality proves escape in modulus.

The polynomial was arbitrary **after** the coefficient event was fixed. There is no uncountable probabilistic intersection and no restriction to rational coefficients, roots, or monomials. The onset can depend on \(p\). A scalar sequence escaping in modulus, with any finite initial segment included, is not dense in \(\mathbb C\); continuous evaluation at zero therefore excludes hypercyclicity of every \(pF\).

The Gaussian function law has full support in \(H(\mathbb C)\): match finitely many jets with positive probability, and use the finite first moment and factorial denominators to make the expected remainder arbitrarily small; head/tail independence and Markov's inequality give positive probability in each compact-open neighborhood. Every neighborhood therefore meets the probability-one family above. Alternatively, a single good \(F\) gives the dense family \(F+\mathbb C[z]\): polynomial addition changes neither sufficiently high derivative orbits nor sufficiently high product jets. Both arguments are proved in the independent verification.

Thus the earlier theorem plus elementary deductions supplies a stronger frequent-hypercyclic version of submitted claims 1, 2, and 4 and of the proposed simultaneous conclusion.

### Exact annular bridge

Raw complex Gaussians do **not** eventually obey the stronger lower bound \((n+1)^{-1/2}\): independent small-value events have divergent probability sum and occur infinitely often almost surely. That distinction matters.

For each fixed \(M\), radially clip each jet \(X_n\), \(n\ge M\), into the closed annulus
\([(n+1)^{-1/2},\log(n+e)]\), leaving earlier jets free. Upper clipping occurs only finitely often almost surely; every lower correction tends to zero. If \(Y_n\) are the resulting jets and \(h=\sum(Y_n-X_n)z^n/n!\), then
\[
\|D^kh\|_R\le e^R\sup_{n\ge k}|Y_n-X_n|\to0.
\]
Frequent hypercyclicity survives this null-orbit perturbation, by using visits to a smaller target neighborhood and deleting finitely many indices.

The clipped coordinates remain independent and have full support on their respective annuli; every relative neighborhood in \(X_M\) has positive probability because a finite jet block can be matched and
\(2\sum_{n>L}\log(n+e)R^n/n!\to0\) bounds all remaining tails uniformly. Consequently **frequently** hypercyclic functions are dense in each exact \(X_M\). Since \(HC(D)\) is \(G_\delta\), \(HC(D)\cap X_M\) is dense \(G_\delta\) there. This does not assert residual frequent hypercyclicity. The deterministic highest-degree estimate applies to every \(f\in X_M\), and the union of these spaces is ambiently dense by adding arbitrarily late baseline tails to polynomials.

This subsumes the proposed annular existence/residual-HC and ambient simultaneous-failure conclusions at the level of implications from older literature. The new direct Baire construction can still be an independent elementary proof; its existence statement is not thereby historically new.

## 4. Remaining novelty distinctions

The statement
\[
\forall f\in HC(D)\ \forall p\text{ nonconstant}\ \forall W\ni f\
\exists h:\ D^nh\to0,\ f+h\in W\cap HC(D),\ p(f+h)\notin HC(D)
\]
is finer than density of the Gaussian family: it requires intersection with a specified null-orbit coset through each input. Nikula alone and the density deductions above do not establish that full assertion. Its elementary triangular/root recursion may be a useful proof feature, but **no novelty clearance for that refinement** is issued. General perturbation/preserver literature and inaccessible or uninspected bodies remain gaps.

Shkarin's *On the set of hypercyclic vectors for the differentiation operator* (journal 2010; inspected arXiv:1209.0984v1 posted 2012) proves hypercyclic algebras under \(P(f)\) and discusses why \(HC(D)\) contains no nontrivial ideals in \(H(\mathbb C)\). The latter permits an arbitrary entire multiplier depending on \(f\), not a polynomial multiplier. It does not replace the above reasoning; the residual positive polynomial-multiplier family makes that distinction unavoidable. Its \(p(D)\) discussion is also a different operation.

The older optimal-growth results cited by Costakis (Grosse-Erdmann 1990 and Shkarin 1993) concern allowable growth and explain his additive exponential perturbation result. Their original bodies were not acquired in this audit; no claim about their full consequences is made.

## 5. Search extent, citation trails, and limits

The full query ledger is [QUERIES.md](QUERIES.md); the source/lead ledger is [SOURCE_LEADS.md](SOURCE_LEADS.md); exact downloaded-file identities and inspection scope are in [SOURCE_RECEIPTS.json](SOURCE_RECEIPTS.json). Copied sources and search responses are in ignored \`sources/\` only.

Searches covered the exact question title/quantifiers; polynomial multiplication and hypercyclicity preservers; derivative coefficients, lower bounds and prescribed jets; Gaussian/random MacLane functions; the three original references' backward/forward trails; author publication records; and current results through May–June 2026. Two OpenAlex DOI-based citation queries returned one citing record for the 2018 paper and eight for Nikula. Those are the service's returned subsets, not complete citation counts for the field. Only identified useful leads were opened. No claim that every citation body was read is made.

The Costakis personal Papers link currently returns an “in progress” image-only page; its available CV ends with 2019-era publications. This is not a complete 2026 author record. Bernal-González's institutional list contains 2025/2026 work. The open 2026 article's body and final questions concern sequences \(\Phi_n(D)\), including \((c_nD^n)\), rather than \(p(z)f(z)\). The 2026 Mouze–Munnier arXiv abstract concerns countable polynomial families of weighted shifts on \(\ell_p\); its body was not inspected.

Access gaps include the Nikula journal body, original 1990/1993 growth articles, the Bayart–Grivaux 2006 AMS PDF (403), complete monographs, 2024/2025 random-weighted-shift subscription bodies, and potentially unindexed theses/preprints or explicit solutions under other titles/languages. The 2011 Bayart–Matheron v1 was inspected in its introduction and application section; a current author manuscript's later explicit Gaussian remark was not backdated to that v1.

The original submitted bounded-search absence claims were not adopted. No project-owned AI preprint is counted as independent earlier research. No contact with any individual, outreach draft, publication, external edit, Git commit, push, or release was made.

## 6. Defensible framing and decision

A safe future framing is an **elementary proof and refinement of polynomial-multiplier failure**, explicitly placing the existence/dense simultaneous conclusions as consequences of the older random-function theory and explaining the direct null-orbit construction. This is proposed framing, not an authored paper. A claim of novel discovery requires a separately bounded contribution beyond those corollaries and further review.

Avoid “first negative answer,” “resolves a question still open since 2008,” “the simultaneous result is new,” or attributing the explicit multiplier conclusion to Nikula without evidence. A defensible factual formulation is: the direct argument gives a negative answer to the question posed in 2008; the stronger existence conclusion can already be deduced from Nikula's earlier theorem, while the first explicit recording of the multiplier consequence has not been established.

**Scoped audit completion: 100%.** This means the assigned bounded priority audit and its positive prior-implication check are complete, not that the literature has been exhausted. **Firstness: not cleared. Current-open status: not cleared. Earlier implication: established. First explicit-disproof date: unestablished.**

